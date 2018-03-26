#!/usr/bin/env python3
"""
Hooks responsible for determining the endpoint behavior of the application.
"""
import datetime
import json
import logging
from typing import List
from urllib.parse import urlparse, parse_qs
from uuid import uuid4

import requests
from bson import json_util, ObjectId
from flask import current_app as app, abort, _request_ctx_stack
from kombu import Connection, Exchange, Producer


LOGGER = logging.getLogger('ingestion-api')


def find_duplicates(items):
    """
    Searches database for any items that are duplicates of already uploaded items and
    filters them out
    Arguments:
        items {[type]} -- [description]
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


def register_upload_job(items: List[dict]) -> None:
    """
    Logs when file upload begins

    Arguments:
        item {[dict]} -- [description]
    """
    files = []
    for record in items:
        record['start_time'] = datetime.datetime.now().isoformat(),
        for data_item in record['files']:
            files.append(data_item)
            data_item['assay'] = ObjectId(data_item['assay'])
            data_item['trial'] = ObjectId(data_item['trial'])

    duplicate_filenames = find_duplicates(files)

    if duplicate_filenames:
        print("Error, duplicate file, upload rejected")
        abort(500, "Upload aborted, duplicate files found")


def run_analysis_job(items: List[dict]) -> None:
    """
    Runs the specified pipeline

    Arguments:
        items {[type]} -- [description]
    """
    for item in items:
        run_id = str(item['_id'])
        _etag = str(item['_etag'])

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


def check_for_analysis(items: List[dict]) -> None:
    """
    Every time a new entry hits the "data" collection, the assay
    collection is checked to see if any runs can be started.

    Arguments:
        items {[Data]} -- List of data objects.
    """

    start_celery_task(
        "framework.tasks.analysis_tasks.analysis_pipeline",
        [],
        uuid4().int
    )


def serialize_objectids(items: List[dict]) -> None:
    """
    Transforms the ID strings into ObjectID objects for propper mapping.

    Arguments:
        items {[Data]} -- List of data objects.
    """
    for record in items:
        record['assay'] = ObjectId(record['assay'])
        record['trial'] = ObjectId(record['trial']),
        record['processed'] = False
        print(record)


def register_analysis(items: dict) -> None:
    """[summary]

    Arguments:
        items {[type]} -- [description]
    """
    for analysis in items:
        analysis['status'] = {
            'progress': 'In Progress',
            'message': ''
        }
        analysis['start_date'] = datetime.datetime.now().isoformat()


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


def process_data_upload(item: dict, original: dict):
    """[summary]

    Arguments:
        item {dict} -- [description]
        original {dict} -- [description]
    """
    # The first task is to tell Celery to move the files.

    print("Process data upload fired")
    google_path = app.config['GOOGLE_URL'] + app.config['GOOGLE_FOLDER_PATH']
    start_celery_task(
        "framework.tasks.cromwell_tasks.move_files_from_staging",
        [original, google_path],
        uuid4().int
    )


def get_trials(request, lookup):
    """
    Takes a username, and returns a list of trials they are part of

    Arguments:
        request {dict} -- request object

    Returns:
        dict -- Mongo return object
    """
    current_user = _request_ctx_stack.top.current_user
    gid = current_user['sub']
    lookup['collaborators'] = gid


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


def log_file_patched(items: List[dict]) -> None:
    """
    Logs when the job has been updated with google URIs

    Arguments:
        items {[dict]} -- Items affected by operation.
    """
    for item in items:
        LOGGER.debug("Google Upload for item completed")
