#!/usr/bin/env python3
"""
Hooks responsible for determining the endpoint behavior of the application.
"""
import datetime
import json
from typing import List
from uuid import uuid4
from bson import json_util, ObjectId
from flask import current_app as app, abort, _request_ctx_stack
from kombu import Connection, Exchange, Producer
from constants import RABBIT_MQ_ADDRESS, LOGGER


def get_current_user() -> str:
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
        [str] - List of duplicate filenames.
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
        record['start_time'] = datetime.datetime.now().isoformat()
        record['started_by'] = get_current_user()['email']
        for data_item in record['files']:
            files.append(data_item)
            data_item['assay'] = ObjectId(data_item['assay'])
            data_item['trial'] = ObjectId(data_item['trial'])

    duplicate_filenames = find_duplicates(files)

    if duplicate_filenames:
        print("Error, duplicate file, upload rejected")
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
        uuid4().int
    )

    # Start a scan for files that require postprocessing.
    start_celery_task(
        "framework.tasks.processing_tasks.postprocessing",
        [items],
        uuid4().int
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
        analysis['start_date'] = datetime.datetime.now().isoformat()
        analysis['started_by'] = get_current_user()['email']


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
        uuid4().int
    )


def log_file_patched(items: List[dict]) -> None:
    """
    Logs when the job has been updated with google URIs

    Arguments:
        items {[dict]} -- Items affected by operation.
    """
    for item in items:
        message = "Google Upload for item: " + str(item) + " completed."
        LOGGER.debug(message)


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
    # If the caller is a service, not a user, no need for filters.
    if 'gty' in current_user and current_user['gty'] == 'client-credentials':
        return

    user_id = current_user['email']

    # Logic for adding the appropriate filter based on the endpoint.
    try:
        if resource == 'trials':
            lookup['collaborators'] = user_id
        elif resource == 'ingestion':
            lookup['started_by'] = user_id
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
    except TypeError as err:
        print(err)
        abort(500, "There was an error processing your viewable data.")
