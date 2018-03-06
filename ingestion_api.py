#!/usr/bin/env python3
"""
This file defines the basic behavior of the eve application.

Users upload files to the google bucket, and then run cromwell jobs on them
"""

import os
import asyncio
import json
import logging
import argparse
import datetime
from bson import json_util, ObjectId
from bson.json_util import loads
from uuid import uuid4
from kombu import Connection, Exchange, Producer
from eve import Eve
from eve.auth import TokenAuth
from flask import current_app as app
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


def get_trials(username):
    """
    Takes a username, and returns a list of trials they are part of

    Arguments:
        username {string} -- Name of the user

    Returns:
        dict -- Mongo return object
    """
    trials = app.data.driver.db['trials']
    return trials.find(
        {'$or': [
            {'principal_investigator': username},
            {'collaborators': username}
        ]},
        {'_id': 1, 'name': 1, 'assays': 1}
    )


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
    start_celery_task(
        "framework.tasks.cromwell_tasks.move_files_from_staging",
        [original, google_path],
        uuid4().int
    )


def alert_data_upload_done(items):
    for item in items:
        print(item)


def alert_celery_kombu(item, original):
    """Sends the details of the uploaded job to Celery, which will in turn start Cromwell

    Arguments:
        item {dict} -- Updated mongo object represented completed job.
        original {dict} -- Original mongo object before update.
    """
    if item['status']['progress'] == 'Completed':
        # Create connection details
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
            "id": 1234,
            "task": "framework.tasks.cromwell_tasks.run_cromwell",
            "args": [json.dumps(item['files'])],
            "kwargs": {},
            "retries": 0
        }
        # Send data
        producer.publish(
            json.dumps(payload),
            content_type='application/json',
            content_encoding='utf-8'
        )
        connection.release()
        LOGGER.debug("Item upload complete, mongo patch complete")


def register_upload_job(items):
    """
    Logs when file upload begins

    Arguments:
        item {[dict]} -- [description]
    """
    print('triggered register upload job')
    for record in items:
        record['start_time'] = datetime.datetime.now().isoformat(),
        for data_item in record['files']:
            data_item['assay'] = ObjectId(data_item['assay'])
            data_item['trial'] = ObjectId(data_item['trial'])


def log_upload_complete(items):
    """
    Logs completed file uploads
    Arguments:
        items {[type]} -- [description]
    """
    for item in items:
        log_string = 'Record creation completed for: '


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


def display_analysis_entry(items):
    for item in items:
        item['status'] = {
            'progress': 'In Progress',
            'message': ''
        }


def create_app():

    # Ingestion Hooks
    app.on_updated_ingestion += process_data_upload
    app.on_insert_ingestion += register_upload_job
    app.on_inserted_ingestion += log_upload_complete

    # Data Hooks
    app.on_insert_data += serialize_objectids
    app.on_inserted_data += alert_data_upload_done

    # Analysis Hooks
    app.on_insert_analysis += display_analysis_entry
    app.on_inserted_analysis += run_analysis_job

    if ARGS.test:
        app.config['TESTING'] = True
        app.config['MONGO_HOST'] = 'localhost'
    else:
        add_rabbit_handler()


if __name__ == '__main__':
    create_app()
    app.run(host='0.0.0.0', port=5000)
