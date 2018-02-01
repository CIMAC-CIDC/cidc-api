#!/usr/bin/env python
"""
This file defines the basic behavior of the eve application.

Users upload files to the google bucket, and then run cromwell jobs on them
"""

import os
import uuid
import asyncio
import json
from kombu import Connection, Exchange, Producer
from eve import Eve
from eve.auth import TokenAuth
from flask import current_app as app
from celery import Celery


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


def alert_celery_kombu(item, original):
    """Sends the details of the uploaded job to Celery, which will in turn start Cromwell

    Arguments:
        item {dict} -- Updated mongo object represented completed job.
        original {dict} -- Original mongo object before update.
    """
    print(item)
    if item['status']['progress'] == 'Completed':
        # Create connection details
        task_exchange = Exchange('', type='direct')
        connection = Connection('amqp://rabbitmq:5672/')
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
            "id": 12345,
            "task": "tasks.run_cromwell",
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


async def do_something():
    """Sample async function to demonstrate yielding behavior
    """
    print("test test test")
    asyncio.sleep(0.5)
    print("test2 test2 test2")


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

app = Eve(auth=TokenAuth, settings='settings.py')


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

app.on_updated_jobs += alert_celery_kombu

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
