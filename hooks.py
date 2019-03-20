"""
Hooks responsible for determining the endpoint behavior of the application.
"""
import base64
import datetime
import json
import logging
import time
import urllib
from typing import List

from cidc_utils.loghandler.stack_driver_handler import send_mail, log_formatted
from bson import ObjectId, json_util
from flask import _request_ctx_stack, abort
from flask import current_app as app
from kombu import Connection, Exchange, Producer
from oauth2client.service_account import ServiceAccountCredentials

from settings import GOOGLE_UPLOAD_BUCKET, RABBIT_MQ_ADDRESS, SENDGRID_API_KEY

CREDS = ServiceAccountCredentials.from_json_keyfile_name("../auth/.google_auth.json")
CLIENT_ID = CREDS.service_account_email


def update_last_access(email: str):
    """
    Updates a user's last access time when they touch an endpoint.

    Arguments:
        email {str} -- User's email.
    """
    last_access = app.data.driver.db["last_access"]
    if not last_access.find_one({"email": email}):
        last_access.insert(
            {
                "email": email,
                "last_access": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
        )
    else:
        last_access.update(
            {"email": email},
            {
                "$set": {
                    "last_access": datetime.datetime.now(
                        datetime.timezone.utc
                    ).isoformat()
                }
            },
        )

    log = "User: %s last login updated" % email
    logging.info({"message": log, "category": "FAIR-EVE-LOGIN"})


def sign_url(
    bucket_object: str,
    expires_after_seconds: int = 6,
    bucket: str = "lloyd-test-pipeline",
) -> str:
    """
    Function that generates signed URLs.

    Arguments:
        bucket_object {str} -- Path of file inside the bucket.

    Keyword Arguments:
        expires_after_seconds {int} -- Length of time url is valid. (default: {6})
        bucket {str} -- The google storage bucket the file is in. (default: {"lloyd-test-pipeline"})

    Returns:
        str -- A signed download url.
    """
    method = "GET"
    gcs_filename = urllib.parse.quote("/%s/%s" % (bucket, bucket_object))
    content_md5, content_type = None, None
    expiration_dt = datetime.datetime.utcnow() + datetime.timedelta(
        seconds=expires_after_seconds
    )
    expiration = int(time.mktime(expiration_dt.timetuple()))
    signature_string = "\n".join(
        [method, content_md5 or "", content_type or "", str(expiration), gcs_filename]
    )
    signature_bytes = CREDS.sign_blob(signature_string)[1]
    query_params = {
        "GoogleAccessId": CLIENT_ID,
        "Expires": str(expiration),
        "Signature": base64.b64encode(signature_bytes),
    }
    result = "{endpoint}{resource}?{querystring}".format(
        endpoint="https://storage.googleapis.com",
        resource=gcs_filename,
        querystring=urllib.parse.urlencode(query_params),
    )
    return result


def get_current_user():
    """
    Gets the current user in the flask context

    Returns:
        str -- User GID
    """
    # Try to get the user twice in case of any weird sync issues.
    current_user = None
    for i in range(4):
        try:
            current_user = _request_ctx_stack.top.current_user
            return current_user
        except AttributeError:
            pass
    if not current_user:
        logging.info(
            {"message": "Current user is undefined", "category": "ERROR-EVE-DEBUG"}
        )
        raise AttributeError("Unable to find a user")


def find_duplicates(items: List[dict]) -> List[str]:
    """
    Searches database for any items that are duplicates of already uploaded items and
    filters them out

    Arguments:
        items {[dict]} -- Data records

    Returns:
        List[str] -- List of duplicate filenames.
    """
    query = {"$or": []}

    for record in items:
        query["$or"].append(
            {
                "assay": ObjectId(record["assay"]),
                "trial": ObjectId(record["trial"]),
                "file_name": record["file_name"],
                "visibility": True,
            }
        )

    data = app.data.driver.db["data"]
    data_results = list(data.find(query, projection=["file_name"]))
    return [x["file_name"] for x in data_results]


def check_trial_locked(trial_id: str) -> bool:
    """
    Check if a trial is locked.

    Arguments:
        trial_id {str} -- Id of trial to check.

    Returns:
        bool -- [description]
    """
    trials = app.data.driver.db["trials"]
    locked = trials.find_one({"_id": trial_id, "locked": True})
    return bool(locked)


# On insert ingestion.
def register_upload_job(items: List[dict]) -> None:
    """
    Logs when file upload begins, aborts if duplicates found.

    Arguments:
        item {[dict]} -- Upload record
    """
    files = []
    current_user = None
    try:
        current_user = get_current_user()["email"]
    except AttributeError:
        current_user = "<User Undefined>"

    for record in items:
        record["start_time"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        record["started_by"] = current_user
        log = "Upload job started by: %s\n" % current_user
        for data_item in record["files"]:
            if check_trial_locked(data_item["trial"]):
                abort(401, "This trial has been locked, you may not upload files to it")
            log += "Concerning trial: %s On Assay: %s\n" % (
                str(data_item["trial"]),
                str(data_item["assay"]),
            )
            logging.info({"message": log, "category": "FAIR-EVE-RECORD"})
            files.append(data_item)
            data_item["assay"] = ObjectId(data_item["assay"])
            data_item["trial"] = ObjectId(data_item["trial"])

    duplicate_filenames = find_duplicates(files)

    if duplicate_filenames:
        logging.error(
            {
                "message": "Error, duplicate file, upload rejected",
                "category": "ERROR-EVE-REQUEST",
            }
        )
        abort(409, "Upload aborted, duplicate files found")


# On inserted data.
def check_for_analysis(items: List[dict]) -> None:
    """
    Every time a new entry hits the "data" collection, the assay
    collection is checked to see if any runs can be started.

    Arguments:
        items {[dict]} -- list of data records
    """
    start_celery_task("framework.tasks.snakemake_tasks.manage_workflows", [], 678)
    start_celery_task("framework.tasks.processing_tasks.postprocessing", [items], 91011)


# On updated trial.
def updated_trial(updates: dict, original: dict) -> None:
    """
    Hook for updates to a trial. Looks for user changes and alters permissions.

    Arguments:
        updates {dict} -- Updates to the record.
        original {dict} -- Original record.

    Returns:
        None -- [description]
    """
    admin = get_current_user()["email"]

    if "collaborators" in updates:
        new_collabs = updates["collaborators"]
        old_collabs = original["collaborators"]
        if new_collabs == old_collabs:
            return
        # Determine to be added
        to_add = list(filter(lambda x: x not in old_collabs, new_collabs))
        start_celery_task(
            "framework.tasks.administrative_tasks.grant_trial_access",
            [to_add, admin, original],
            474747,
        )

    if "locked" in updates and updates["locked"] != original["locked"]:
        verb = "unlocked" if updates["locked"] else "locked"
        log = "Trial %s %s by administrator %s" % (original["trial_name"], verb, admin)
        logging.info({"message": log, "category": "INFO-EVE-TRIALLOCK"})


# On updated data.
def data_patched(updates: dict, original: dict) -> None:
    """
    Hook to watch for changes to data records, specifically visibility changes.

    Arguments:
        updates {dict} -- Updates being made to the record.
        original {dict} -- Original record.

    Returns:
        None -- [description]
    """
    if updates["processed"] == original["processed"]:
        return

    if original["processed"] < updates["processed"]:
        for key in updates:
            original[key] = updates[key]
        start_celery_task(
            "framework.tasks.processing_tasks.postprocessing", [original], 91011
        )
        return


# On-inserted accounts.
def log_user_create(items: List[dict]) -> None:
    """
    Hook for posts to user endpoint, logs creation of user.

    Arguments:
        items {List[dict]} -- List of user records inserted.
    """
    for new_user in items:
        log = "New user created"
        for key in new_user:
            log += ", %s : %s" % (key, new_user[key])
        logging.info({"message": log, "category": "FAIR-EVE-NEWUSER"})


# On deleted accounts.
def remove_deleted_user(item: dict) -> None:
    """
    Starts the celery task to remove the user from trials
    and google buckets when they are deleted.

    Arguments:
        item {dict} -- [description]

    Returns:
        None -- [description]
    """
    start_celery_task(
        "framework.tasks.administrative_tasks.call_deactivate_account",
        [item, "deactivate"],
        187187187,
    )


# On insert accounts_create
def register_new_user(items: List[dict]) -> None:
    current_user = get_current_user()["email"]
    for new_user in items:
        new_user["email"] = current_user
        user_updates = {
            "email": current_user,
            "approved": False,
            "account_create_date": datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat(),
            "permissions": [],
        }
        send_mail(
            "New user registered.",
            "A new user: %s has registered" % new_user["email"],
            ["cidc@jimmy.harvard.edu"],
            "no-reply@cimac-network.org",
            SENDGRID_API_KEY,
        )
        start_celery_task(
            "framework.tasks.administrative_tasks.add_new_user", [user_updates], 9010102
        )


# On update user
def manage_user_updates(updates: dict, original: dict) -> None:
    """
    Hook that executes when an account is patched. Will stop any patch it can't
    determine the user for.

    Arguments:
        updates {dict} -- [description]
        original {dict} -- [description]
    """
    if "approved" in updates and updates["approved"]:
        updates["registration_approval_date"] = datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()
        logging.info({"message": "Approval recorded", "category": "INFO-EVE-NEWUSER"})
    else:
        logging.info({"message": "No approval", "category": "INFO-EVE-NEWUSER"})


def create_approval_email(user: dict) -> str:
    """
    Creates the registration approval email.

    Arguments:
        user {dict} -- User record from /accounts

    Returns:
        str -- Formatted email.
    """
    return '''
    Dear %s %s:

    Your registration for the CIMAC-CIDC DATA Portal has now been approved.
    To continue, please go to: https://portal.cimac-network.org.

    If you have any questions, please email us at: cidc@jimmy.harvard.edu.

    Thanks,
    The CIDC Project Team
    ''' % (user["first_n"], user["last_n"])


# On updated user.
def log_user_modified(updates: dict, original: dict) -> None:
    """
    Function to log whenever a user's details are altered.

    Arguments:
        updates {dict} -- Updates made to the user's record.
        original {dict} -- State of the user record before alteration.
    """
    current_user = get_current_user()

    log = "Update to user %s made by %s: \n" % (
        original["email"],
        current_user["email"],
    )
    for update in updates:
        log += "Changed: %s:%s\n" % (
            json.dumps(update),
            json.dumps(str(updates[update])),
        )

    if "permissions" in updates:
        if "trial" in updates["permissions"]:
            updates["permissions"]["trial"] = ObjectId(updates["permissions"]["trial"])
        if "assay" in updates["permissions"]:
            updates["permissions"]["assay"] = ObjectId(updates["assay"])

    if "role" in updates:
        if updates["role"] and "role" not in original:
            # Grant upload access
            start_celery_task(
                "framework.tasks.administrative_tasks.change_upload_permission",
                [GOOGLE_UPLOAD_BUCKET, [original["email"]], True],
                8787878,
            )
            send_mail(
                "Subject: CIMAC-CIDC Data Portal Registration Approved",
                create_approval_email(original),
                [original["preferred_contact_email"]],
                "no-reply@cimac-network.org",
                SENDGRID_API_KEY,
            )
        if updates["role"] == "disabled":
            # Revoke upload access
            start_celery_task(
                "framework.tasks.administrative_tasks.call_deactivate_account",
                [original, False],
                515151,
            )

    logging.info({"message": log, "category": "FAIR-EVE-USER-PATCHED"})


# On insert data.
def serialize_objectids(items: List[dict]) -> None:
    """
    Transforms the ID strings into ObjectID objects for propper mapping.

    Arguments:
        items {List[dict]} -- List of data records.
    """
    for record in items:
        record["assay"] = ObjectId(record["assay"])
        record["trial"] = ObjectId(record["trial"])
        record["processed"] = False
        record["visibility"] = True
        record["children"] = []
        log = "Record: %s, for Trial: %s, in Assay: %s uploaded" % (
            record["file_name"],
            str(record["trial"]),
            str(record["assay"]),
        )
        log_formatted(logging.info, log, "INFO-EVE-DATA")


# On delete gene_symbol.
def drop_gene_symbol(item):
    """
    When the endpoint gets a delete, removes all documents in the col.

    Arguments:
        item {[type]} -- [description]
    """
    symbols = app.data.driver.db["gene_symbol"]
    symbols.remove({})
    logging.info(
        {"message": "Gene collection dropped by celery", "category": "INFO-EVE-HUGO"}
    )


def start_celery_task(task: str, arguments: List[object], task_id: int) -> None:
    """
    Generic function to start a task through celery

    Arguments:
        task {string} -- Name of the task to start.
        arguments {List[object]} -- List of arguments to be supplied.
        id {int} -- Integer ID to uniquely identify the string.
    """
    task_exchange = Exchange("", type="direct")
    connection = Connection(RABBIT_MQ_ADDRESS)
    producer = Producer(
        exchange=task_exchange,
        channel=connection.channel(),
        routing_key="celery",
        serializer="json",
    )

    # is the task ID necessary here?
    payload = {
        "id": task_id,
        "task": task,
        "args": arguments,
        "kwargs": {},
        "retries": 0,
    }

    producer.publish(
        json.dumps(payload, default=json_util.default),
        content_type="application/json",
        content_encoding="utf-8",
    )
    connection.release()


# On updated ingestion.
def process_data_upload(item: dict, original: dict) -> None:
    """
    Tells celery to move the files from staging to an appropriate bucket.

    Arguments:
        item {dict} -- Records to be moved
        original {dict} -- Patched upload record with GSURL.
    """
    google_path = app.config["GOOGLE_URL"] + app.config["GOOGLE_FOLDER_PATH"]
    start_celery_task(
        "framework.tasks.storage_tasks.move_files_from_staging",
        [original, google_path],
        12345,
    )


def log_data_delete(item: dict) -> None:
    """
    Log the deletion of data.

    Arguments:
        item {dict} -- Deleted item.
    """
    current_user = get_current_user()
    log = "Record: %s deleted by user %s, google_uri: %s" % (
        item["file_name"],
        current_user["email"],
        item["gs_uri"],
    )
    logging.info({"message": log, "category": "INFO-EVE-FAIR"})


def log_file_patched(items: List[dict]) -> None:
    """
    Logs when the job has been updated with google URIs

    Arguments:
        items {List[dict]} -- Items affected by operation.
    """
    for item in items:
        message = "Google Upload for item: " + str(item) + " completed."
        logging.info({"message": message, "category": "INFO-EVE-DATA"})


def log_patch_request(resource: str, request: str, payload: dict) -> None:
    """
    Create a formatted log of all patch requests.

    Arguments:
        resource {str} -- Resource endpoint being queried.
        request {str} -- Request being sent to endpoint.
        payload {dict} -- Payload of the patch request.
    """
    current_user = get_current_user()["email"]
    # Log the request
    try:
        log = (
            "Patch request made against resource %s by user %s. Method: %s."
            "Request structure: %s. Patch status: %s"
            % (
                resource,
                current_user,
                request.method,
                request.url,
                str(payload.status_code),
            )
        )
        logging.info({"message": log, "category": "INFO-EVE-PATCH-REQUEST"})
    except TypeError:
        log = {"Patch request failed for resource %s, by user %s." % current_user}
        logging.info({"message": log, "category": "ERROR-EVE-PATCH-REQUEST"})


def log_post_request(resource: str, request: str, payload: dict) -> None:
    """
    Create a formatted log of all post requests.

    Arguments:
        resource {str} -- Resource endpoint being queried.
        request {str} -- Request being sent to endpoint.
        payload {dict} -- Payload of the post request.

    Returns:
        None -- [description]
    """
    # Get current user.
    current_user = get_current_user()
    log = (
        "Post request made against resource %s by user %s method: %s request structure: %s "
        " status: %s"
        % (
            resource,
            current_user["email"],
            request.method,
            request.url,
            str(payload.status_code),
        )
    )
    logging.info({"message": log, "category": "INFO-EVE-POST-REQUEST"})


def log_delete_request(resource: str, request: str, payload: dict) -> None:
    """
    Create a formatted log of all post requests.

    Arguments:
        resource {str} -- Resource endpoint being queried.
        request {str} -- Request being sent to endpoint.
        payload {dict} -- Payload of the delete request.

    Returns:
        None -- [description]
    """
    # Get current user.
    current_user = get_current_user()

    # Log the request
    log = (
        "Delete request made against resource %s by user %s method: %s request structure: %s"
        " Delete status: %s"
        % (
            resource,
            current_user["email"],
            request.method,
            request.url,
            str(payload.status_code),
        )
    )
    logging.info({"message": log, "category": "INFO-EVE-DELETE-REQUEST"})


def generate_signed_url(response: dict) -> None:
    """
    Generates a signed URL.

    Arguments:
        response {dict} -- [description]

    Returns:
        None -- [description]
    """
    url = response["gs_uri"]
    signed_url = sign_url(
        url.replace("gs://lloyd-test-pipeline/", ""), expires_after_seconds=1000
    )
    response["download_link"] = signed_url


def filter_on_id(resource: str, request: dict, lookup: dict) -> None:
    """
    Adds a filter to every get request ensuring that only data that a person
    is authorized to see is sent to them.

    Arguments:
        resource {str} -- Resource endpoint being queried.
        request {str} -- Request being sent to endpoint.
        lookup {dict} -- Filter condition.
    """

    # If it is a test call, don't bother filtering.
    if resource in ["test"]:
        return

    doc_id = None

    # Check for the case of a document ID query.
    if not request.args and not request.url.split("/")[-1] == resource:
        doc_id = request.url.split("/")[-1]

    # Get current user.
    current_user = None
    try:
        current_user = get_current_user()
    except AttributeError:
        logging.info(
            {
                "message": "Error: User context has not been set!",
                "category": "ERROR-EVE-AUTH",
            }
        )

    # Don't filter for machine.
    if current_user["email"] == "celery-taskmanager":
        return

    # Log the request
    log = (
        "Data request made against resource %s by user %s method: %s request structure: %s "
        % (resource, current_user["email"], request.method, request.url)
    )
    logging.info({"message": log, "category": "INFO-EVE-REQUEST"})

    user_id = current_user["email"]

    # Logic for adding the appropriate filter based on the endpoint.
    if resource == "ingestion":
        lookup["started_by"] = user_id
    elif resource == "trials":
        return
    elif resource == "accounts_info":
        lookup["email"] = user_id
    elif resource in ["assays", "accounts"]:
        return
    else:
        accounts = app.data.driver.db["accounts"]
        perms = accounts.find_one({"email": user_id}, {"permissions": 1})["permissions"]
        if not doc_id:
            get_resource(lookup, perms)
        if doc_id:
            if not get_document(doc_id, resource, perms):
                lookup["find"] = "nothing"


# Get id document
def get_document(_id: str, resource: str, permissions: List[dict]) -> bool:
    """
    Method for determining if a user is allowed to see a specific document.

    Arguments:
        _id {str} -- Id of the document.
        resource {str} -- Resource endpoint.
        permissions {List[dict]} -- User's permissions list.

    Returns:
        bool -- True if they are allowed to see it, else false.
    """
    resource_coll = app.data.driver.db[resource]
    document = resource_coll.find_one({"_id": _id})
    # If there is no document, no need to filter.
    if not document:
        return True

    for permission in permissions:
        trial_match = document["trial"] == permission["trial"]
        assay_match = document["assay"] == permission["assay"]
        if trial_match and assay_match:
            return True
        if trial_match and permission["role"] == "trial_r":
            return True
        if assay_match and permission["role"] == "assay_r":
            return True

    return False


# Get on a resource, not a specific document, e.g. /olink?where={"trial":"12345", "assay": "679"}
def get_resource(lookup: dict, permissions: List[dict]) -> None:
    """
    Filters requests against a resource endpoint.

    Arguments:
        lookup {dict} -- [description]
        permissions {List[dict]} -- [description]

    Returns:
        None -- [description]
    """
    conditions = []
    assay_read = []
    trial_read = []

    for permission in permissions:
        # If they have a broad role.
        if permission["role"] == "trial_r":
            # note the ID.
            conditions.append({"trial": permission["trial"]})
        if permission["role"] == "assay_r":
            assay_read.append(permission["assay"])
            if "assay" in lookup and lookup["assay"] != permission["assay"]:
                conditions.append({"assay": permission["assay"]})

    for permission in permissions:
        if permission["role"] == "read":
            # Check to see if rule is redundant.
            if (
                permission["trial"] not in trial_read
                and permission["assay"] not in assay_read
            ):
                conditions.append(
                    {"trial": permission["trial"], "assay": permission["assay"]}
                )

    # Only add the lookup key if there are any conditions to add.
    if conditions:
        lookup["$or"] = conditions
    else:
        lookup["find"] = "nothing"
