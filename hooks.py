#!/usr/bin/env python3
"""
Hooks responsible for determining the endpoint behavior of the application.
"""
import datetime
import json
import logging
from typing import List
from uuid import uuid4
from urllib.parse import parse_qs, urlparse
from bson import json_util, ObjectId
from flask import current_app as app, abort, _request_ctx_stack
from kombu import Connection, Exchange, Producer


LOGGER = logging.getLogger('ingestion-api')


def get_current_user() -> str:
    """
    Gets the current user in the flask context

    Returns:
        str -- User GID
    """
    current_user = _request_ctx_stack.top.current_user
    print(current_user)
    return current_user


def get_job_status(request, lookup):
    """
    Fetches all jobs started by the given user.

    Arguments:
        request {[type]} -- [description]
        lookup {[type]} -- [description]
    """
    url = request.url
    query_params = parse_qs(urlparse(url).query)

    if not len(query_params) == 1:
        request = None
        abort(500, 'Error, wrong number of params passed')

    if 'started_by' not in query_params:
        request = None
        abort(500, 'Name is the only valid query param!')

    username = query_params['started_by'][0]

    lookup['started_by'] = username


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

    print(query)

    data = app.data.driver.db['data']
    data_results = list(data.find(query, projection=['file_name']))
    print(data_results)
    return [x['file_name'] for x in data_results]

# Return a list of any duplicate records


# on insert ingestion.
def register_upload_job(items: List[dict]) -> None:
    """
    Logs when file upload begins

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
    connection = Connection('amqp://rabbitmq')
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
    # The first task is to tell Celery to move the files.
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
        message = "Google Upload for item: " + item['_id'] + " completed."
        LOGGER.debug(message)


def filter_on_id(resource: str, request: dict, lookup: dict) -> None:
    """
    Adds a filter to every get request ensuring that only data that a person
    is authorized to see is sent to them.

    Arguments:
        resource {str} -- Resource endpoint being queried.
        request {[type]} -- Request being sent to endpoint.
        lookup {[type]} -- Filter condition.
    """
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
        elif resource == 'ingestion' or resource == 'analysis':
            lookup['started_by'] = user_id
        else:
            accounts = app.data.driver.db['trials']
            trials = accounts.find({'collaborators': user_id}, {'_id': 1, 'assays': 1})
            if resource == 'assays':
                assay_ids = []
                for trial in trials:
                    assays = trial['assays']
                    for assay in assays:
                        assay_ids.append(str(assay['assay_id']))
                lookup['_id'] = {'$in': assay_ids}

            else:
                trial_ids = [x['_id'] for x in trials]
                lookup['trial'] = {'$in': trial_ids}

    except TypeError as err:
        print(err)
        abort(500, "There was an error processing your credentials.")
