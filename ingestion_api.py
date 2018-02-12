#!/usr/bin/env python3
"""
This file defines the basic behavior of the eve application.

Users upload files to the google bucket, and then run cromwell jobs on them
"""

import os
import uuid
import asyncio
import json
import logging
import argparse
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


async def alert_celery_native(item, original):
    """Uses celery's native send task to get a response object. Async, waits for the
    status to change on ready(), then prints the result
    Arguments:
        item {dict} -- Updated mongo object representing completed upload
        original {dict} -- Original mongo object before update
    """
    celery = Celery()
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        broker_url='amqp://localhost',
        result_backend='rpc://'
    )
    response = celery.send_task("tasks.hello_world", ["hello, world1"])
    while not response.ready():
        print('waiting')
        await asyncio.sleep(0.5)
    print('done: ' + response.get())


def celery_event_loop(item, original):
    """Schedules asynchronous celery tasks to demonstrate that
    waiting for the job to return is non-blocking.

    Arguments:
        item {[type]} -- [description]
        original {[type]} -- [description]
    """
    loop = asyncio.get_event_loop()
    task1 = asyncio.ensure_future(alert_celery_native(item, original))
    task2 = asyncio.ensure_future(do_something())
    wait_tasks = asyncio.wait([task1, task2])
    loop.run_until_complete(wait_tasks)


def log_file_upload(items):
    """
    Logs when file upload begins

    Arguments:
        item {[dict]} -- [description]
    """
    for item in items:
        LOGGER.debug('Record insertion for job begun')


def log_upload_complete(items):
    """
    Logs completed file uploads
    Arguments:
        items {[type]} -- [description]
    """
    for item in items:
        log_string = 'Record creation completed for: '
        LOGGER.debug(log_string)


def test_endpoint_logger(items):
    """
    Simple endpoint to test features without running a pipeline

    Arguments:
        items {[type]} -- [description]
    """
    print('method called!!!!')
    for item in items:
        LOGGER.info('test endpoint called')


app = Eve('ingestion_api', auth=TokenAuth, settings='settings.py')


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


def create_app():
    app.on_updated_jobs += alert_celery_kombu
    app.on_insert_jobs += log_file_upload
    app.on_inserted_jobs += log_upload_complete
    app.post_GET_test += test_endpoint_logger
    if ARGS.test:
        app.config['TESTING'] = True
        app.config['MONGO_HOST'] = 'localhost'
    else:
        add_rabbit_handler()


if __name__ == '__main__':
    create_app()
    app.run(host='0.0.0.0', port=5000)
