#!/usr/bin/env python3
"""
Hooks responsible for determining the endpoint behavior of the application.
"""
import datetime
import json
import logging
from typing import List
from bson import json_util, ObjectId
from flask import current_app as app, abort, _request_ctx_stack
from kombu import Connection, Exchange, Producer
from constants import RABBIT_MQ_ADDRESS


def get_current_user():
    """
    Gets the current user in the flask context

    Returns:
        str -- User GID
    """
    current_user = _request_ctx_stack.top.current_user
    return current_user


def find_duplicates(items: List[dict]) -> List[str]:
    """
    Searches database for any items that are duplicates of already uploaded items and
    filters them out

    Arguments:
        items {[dict]} -- Data records

    Returns:
        [str] -- List of duplicate filenames.
    """
    query = {'$or': []}

    for record in items:
        query['$or'].append({
            'assay': ObjectId(record['assay']),
            'trial': ObjectId(record['trial']),
            'file_name': record['file_name']
        })

    data = app.data.driver.db['data']
    data_results = list(data.find(query, projection=['file_name']))
    return [x['file_name'] for x in data_results]


# On insert ingestion.
def register_upload_job(items: List[dict]) -> None:
    """
    Logs when file upload begins, aborts if duplicates found.

    Arguments:
        item {[dict]} -- Upload record
    """
    files = []
    for record in items:
        record['start_time'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        record['started_by'] = get_current_user()['email']
        log = 'Upload job started by' + record['started_by']
        logging.info({
            'message': log,
            'category': 'FAIR-EVE-RECORD'
        })
        for data_item in record['files']:
            item_log = (
                'Concerning trial: ' + str(data_item['trial']) + 'On Assay: ' + str(data_item['assay'])
            )
            logging.info({
                'message': item_log,
                'category': 'FAIR-EVE-RECORD'
            })
            files.append(data_item)
            data_item['assay'] = ObjectId(data_item['assay'])
            data_item['trial'] = ObjectId(data_item['trial'])

    duplicate_filenames = find_duplicates(files)

    if duplicate_filenames:
        logging.error({
            'message': "Error, duplicate file, upload rejected",
            'category': 'ERROR-EVE-REQUEST'
            })
        abort(500, "Upload aborted, duplicate files found")


# On inserted data.
def check_for_analysis(items: List[dict]) -> None:
    """
    Every time a new entry hits the "data" collection, the assay
    collection is checked to see if any runs can be started.

    Arguments:
        items {[dict]} -- list of data records
    """
    start_celery_task(
        "framework.tasks.analysis_tasks.analysis_pipeline",
        [],
        678
    )

    # Start a scan for files that require postprocessing.
    start_celery_task(
        "framework.tasks.processing_tasks.postprocessing",
        [items],
        91011
    )


# On-inserted user.
def log_user_create(items: List[dict]) -> None:
    """
    Hook for posts to user endpoint, logs creation of user.

    Arguments:
        items {[dict]} -- List of user records inserted.
    """
    for new_user in items:
        for key in new_user:
            log = 'New user created'
            log += ', ' + key + ' : ' + new_user[key]
            logging.info({
                'message': log,
                'category': 'FAIR-EVE-NEWUSER'
            })


# On update trial
def patch_user_access(updates: dict, original: dict) -> None:
    """
    When a trial object is updated, if the list of collaborators changes,
    propagates the changes to modify google storage permissions.

    Arguments:
        updates {dict} -- Updates to trial object.
        original {dict} -- Original record.
    """
    if 'collaborators' in updates:
        n_col = updates['collaborators']
        start_celery_task(
            'framework.tasks.administrative_tasks.update_trial_blob_acl',
            [original['_id'], n_col],
            7889
        )


# On insert data.
def serialize_objectids(items: List[dict]) -> None:
    """
    Transforms the ID strings into ObjectID objects for propper mapping.

    Arguments:
        items {[dict]} -- List of data records.
    """
    for record in items:
        record['assay'] = ObjectId(record['assay'])
        record['trial'] = ObjectId(record['trial'])
        record['processed'] = False
        log = (
            'Record ' +
            record['file_name'] +
            ' for trial ' + str(record['trial']) + ' in assay ' + str(record['assay']) +
            'uploaded')
        logging.info({
            'message': log,
            'category': 'INFO-EVE-DATA'
        })


# On insert analysis.
def register_analysis(items: List[dict]) -> None:
    """
    Add fields that should be created only by the server like start date to
    each analysis object that is being inserted.

    Arguments:
        items {[dict]} -- List of analysis records.
    """
    for analysis in items:
        analysis['status'] = {
            'progress': 'In Progress',
            'message': ''
        }
        analysis['start_date'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        analysis['started_by'] = get_current_user()['email']
        log = (
            'Analysis starrted for trial' +
            str(analysis['trial']) + ' on assay ' + str(analysis['assay']) +
            ' by ' + analysis['started_by']
        )
        logging.info({
            'message': log,
            'category': 'INFO-EVE-DATA'
        })


def start_celery_task(task: str, arguments: object, task_id: int) -> None:
    """
    Generic function to start a task through celery

    Arguments:
        task {string} -- Name of the task to start.
        arguments {[object]} -- List of arguments to be supplied.
        id {int} -- Integer ID to uniquely identify the string.
    """
    task_exchange = Exchange('', type='direct')
    connection = Connection(RABBIT_MQ_ADDRESS)
    channel = connection.channel()

    # Generate Producer
    producer = Producer(
        exchange=task_exchange,
        channel=channel,
        routing_key='celery',
        serializer='json'
    )

    # Construct data
    # is the task ID necessary here?
    payload = {
        "id": task_id,
        "task": task,
        "args": arguments,
        "kwargs": {},
        "retries": 0
    }

    # Send data
    producer.publish(
        json.dumps(payload, default=json_util.default),
        content_type='application/json',
        content_encoding='utf-8'
    )

    # Close Connection
    connection.release()


# On updated ingestion.
def process_data_upload(item: dict, original: dict) -> None:
    """
    Tells celery to move the files from staging to an appropriate bucket.

    Arguments:
        item {dict} -- Records to be moved
        original {dict} -- Patched upload record with GSURL.
    """
    google_path = app.config['GOOGLE_URL'] + app.config['GOOGLE_FOLDER_PATH']
    start_celery_task(
        "framework.tasks.cromwell_tasks.move_files_from_staging",
        [original, google_path],
        12345
    )


def log_file_patched(items: List[dict]) -> None:
    """
    Logs when the job has been updated with google URIs

    Arguments:
        items {[dict]} -- Items affected by operation.
    """
    for item in items:
        message = "Google Upload for item: " + str(item) + " completed."
        logging.info({
            'message': message,
            'category': 'INFO-EVE-DATA'
            })


def filter_on_id(resource: str, request: dict, lookup: dict) -> None:
    """
    Adds a filter to every get request ensuring that only data that a person
    is authorized to see is sent to them.

    Arguments:
        resource {str} -- Resource endpoint being queried.
        request {str} -- Request being sent to endpoint.
        lookup {dict} -- Filter condition.
    """
    doc_id = None

    # Check for the case of a document ID query.
    if not request.args and not request.url.split('/')[-1] == resource:
        doc_id = request.url.split('/')[-1]

    # Get current user.
    current_user = get_current_user()

    # Log the request
    log = (
        'Data request made against resource ' +
        resource + ' by user ' + current_user['email'] +
        ' method: ' + request.method + ' request structure: ' + request.url
    )
    logging.info({
        'message': log,
        'category': 'INFO-EVE-REQUEST'
    })

    # If the caller is a service, not a user, no need for filters.
    if 'gty' in current_user and current_user['gty'] == 'client-credentials':
        return

    user_id = current_user['email']

    # Logic for adding the appropriate filter based on the endpoint.
    try:
        if resource == 'trials':
            pass
        elif resource == 'ingestion':
            lookup['started_by'] = user_id
        elif resource in ['accounts_info', 'accounts_update'] and request.method == "GET":
            lookup['username'] = user_id
        elif resource in ['accounts']:
            pass
        else:
            accounts = app.data.driver.db['trials']
            trials = accounts.find({'collaborators': user_id}, {'_id': 1, 'assays': 1})
            if resource == 'assays':
                # Get the list of assay_ids the user is cleared to know about.
                assay_ids = [str(x['assay_id']) for trial in trials for x in trial['assays']]
                if not doc_id:
                    lookup['_id'] = {'$in': assay_ids}
                elif doc_id not in assay_ids:
                    abort(500, "You are not cleared to view this item")
            else:
                trial_ids = [str(x['_id']) for x in trials]
                lookup['trial'] = {'$in': trial_ids}
    except TypeError:
        logging.error({
            'message': 'Error applying filters',
            'category': 'ERROR-EVE-REQUEST'
        }, exc_info=True)
        abort(500, "There was an error processing your viewable data.")
