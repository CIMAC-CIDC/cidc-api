#!/usr/bin/env python3
"""
This file defines the basic behavior of the eve application.

Users upload files to the google bucket, and then run cromwell jobs on them
"""

import os
import json
import logging
import argparse
import datetime
from urllib.parse import urlparse, parse_qs
from bson import json_util, ObjectId
from bson.json_util import loads
from uuid import uuid4
from kombu import Connection, Exchange, Producer
from eve import Eve
from eve.auth import TokenAuth
from flask import current_app as app, abort, jsonify
from celery import Celery
from rabbit_handler import RabbitMQHandler

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-t', '--test', help='Run application in test mode', action='store_true')
ARGS = PARSER.parse_args()
LOGGER = logging.getLogger('ingestion-api')
LOGGER.setLevel(logging.DEBUG)


class TokenAuth(TokenAuth):
    """
    Function for using authorization tokens
    """
    def check_auth(self, token, allowed_roles, resource, method):
        """Method that receives an authorization token, and checks if it is
        a valid token.

        Arguments:
            token {str} -- Eve API Token.
            allowed_roles {[str]} -- List of strings indicating the allowed
            roles of the user.
            resource {str} -- The resource being accessed.
            method {str} -- The method being used.
        Returns:
            Object -- Returns the token object if found, None if not.
        """
        accounts = app.data.driver.db['accounts']
        return accounts.find_one({'token': token})


def start_celery_task(task, arguments, id):
    """
    Generic function to start a task through celery

    Arguments:
        task {[type]} -- [description]
        arguments {[type]} -- [description]
        id {[type]} -- [description]
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
        "id": id,
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
    connection.release()


def get_trials(request, lookup):
    """
    Takes a username, and returns a list of trials they are part of

    Arguments:
        username {string} -- Name of the user

    Returns:
        dict -- Mongo return object
    """
    url = request.url
    query_params = parse_qs(urlparse(url).query)

    if not len(query_params) == 1:
        request = None
        print("Error, wrong number of params passed")
        return

    if 'username' not in query_params:
        request = None
        print("Username is the only valid param!")
        return

    username = query_params['username'][0]

    lookup['collaborators'] = username


def log_file_patched(items):
    """
    Logs when the job has been updated with google URIs

    Arguments:
        items {[type]} -- [description]
    """
    for item in items:
        LOGGER.debug("Google Upload for item completed")


def add_rabbit_handler():
    RABBIT = RabbitMQHandler('amqp://rabbitmq')
    LOGGER.addHandler(RABBIT)


def process_data_upload(item, original):
    # The first task is to tell Celery to move the files.
    google_path = app.config['GOOGLE_URL'] + app.config['GOOGLE_FOLDER_PATH']
    # start_celery_task(
    #     "framework.tasks.cromwell_tasks.move_files_from_staging",
    #     [original, google_path],
    #     uuid4().int
    # )


def register_upload_job(items):
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
    print(duplicate_filenames)

    if duplicate_filenames:
        print("Error, duplicate file, upload rejected")
        abort(500, "Upload aborted, duplicate files found")


def run_analysis_job(items):
    """
    Runs the specified pipeline

    Arguments:
        items {[type]} -- [description]
    """
    for item in items:
        run_id = str(item['_id'])
        _etag = str(item['_etag'])
        trial = str(item['trial'])
        assay = str(item['assay'])
        samples = item['samples']
        start_celery_task(
            "framework.tasks.analysis_tasks.run_bwa_pipeline",
            [trial, assay, 'lloyd', run_id, _etag, samples],
            run_id
        )


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


def serialize_objectids(items):
    for record in items:
        record['assay'] = ObjectId(record['assay'])
        record['trial'] = ObjectId(record['trial'])


app = Eve(
    'ingestion_api',
    auth=TokenAuth,
    settings='settings.py'
)


@app.after_request
def after_request(response):
    """A function to add google path details to the response header when files are uploaded

    Decorators:
        app -- Flask decorator for application

    Arguments:
        response {dict} -- HTTP response.

    Returns:
        dict -- HTTP response with modified headers.
    """
    response.headers.add('google_url', app.config['GOOGLE_URL'])
    response.headers.add('google_folder_path', app.config['GOOGLE_FOLDER_PATH'])
    return response


@app.errorhandler(500)
def custom500(error):
    return jsonify({'message': error.description}), 500


def create_app():

    # Ingestion Hooks
    app.on_updated_ingestion += process_data_upload
    app.on_insert_ingestion += register_upload_job

    # Data Hooks
    app.on_insert_data += serialize_objectids

    # Analysis Hooks
    app.on_inserted_analysis += run_analysis_job

    # Trials Hooks
    app.on_pre_GET_trials += get_trials

    if ARGS.test:
        app.config['TESTING'] = True
        app.config['MONGO_HOST'] = 'localhost'
    else:
        add_rabbit_handler()


if __name__ == '__main__':
    create_app()
    app.run(host='0.0.0.0', port=5000)
