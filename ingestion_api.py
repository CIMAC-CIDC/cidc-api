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
import requests
from functools import wraps
from os import environ as env
from jose import jwt
from urllib.parse import urlparse, parse_qs, urlencode
from urllib.request import urlopen
from bson import json_util, ObjectId
from bson.json_util import loads
from uuid import uuid4
from kombu import Connection, Exchange, Producer
from eve import Eve
from eve.auth import TokenAuth
from eve_swagger import swagger, add_documentation
from flask import (
    current_app as app,
    abort,
    jsonify,
    request,
    _request_ctx_stack,
    redirect,
    render_template,
    session,
    url_for
)
from flask_cors import cross_origin
from flask_oauthlib.client import OAuth
from celery import Celery
from rabbit_handler import RabbitMQHandler
from dotenv import load_dotenv, find_dotenv
import constants

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-t', '--test', help='Run application in test mode', action='store_true')
ARGS = PARSER.parse_args()
LOGGER = logging.getLogger('ingestion-api')
LOGGER.setLevel(logging.DEBUG)
ALGORITHMS = ["RS256"]

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)
if AUTH0_AUDIENCE is '':
    AUTH0_AUDIENCE = 'https://' + AUTH0_DOMAIN + '/userinfo'


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

    # Close Connection
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
        abort(500, 'Error, wrong number of params passed')

    if 'username' not in query_params:
        request = None
        abort(500, 'Username is the only valid query param!')

    username = query_params['username'][0]

    lookup['collaborators'] = username


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

    print("Process data upload fired")
    google_path = app.config['GOOGLE_URL'] + app.config['GOOGLE_FOLDER_PATH']
    start_celery_task(
        "framework.tasks.cromwell_tasks.move_files_from_staging",
        [original, google_path],
        uuid4().int
    )


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

    for record in items:
        query['$or'].append({
            'assay': ObjectId(record['assay']),
            'trial': ObjectId(record['trial']),
            'file_name': record['file_name']
        })

    data = app.data.driver.db['data']
    data_results = list(data.find(query, projection=['file_name']))
    return [x['file_name'] for x in data_results]


def check_for_analysis(items):
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


def serialize_objectids(items: dict) -> None:
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

app = Eve(
    'ingestion_api',
    auth=TokenAuth,
    settings='settings.py'
)

app.register_blueprint(swagger)

app.config['SWAGGER_INFO'] = {
    'title': 'CIDC API',
    'version': '0.1',
    'description': 'CIDC Data Upload AI',
    'termsOfService': '',
    'contact': {
        'name': 'L'
    },
    'license': {
        'name': 'MIT'
    },
    'schemes': ['http', 'https']
}

add_documentation({'paths': {'/status': {'get': {'parameters': [
    {
        'in': 'query',
        'name': 'foobar',
        'required': False,
        'description': 'special query parameter',
        'type': 'string'
    }]
}}}})

app.secret_key = constants.SECRET_KEY
app.debug = True


# Format error response and append status code.
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=ex.message)
    return response

oauth = OAuth(app)


auth0 = oauth.remote_app(
    'auth0',
    consumer_key=AUTH0_CLIENT_ID,
    consumer_secret=AUTH0_CLIENT_SECRET,
    request_token_params={
        'scope': 'openid profile',
        'audience': AUTH0_AUDIENCE
    },
    base_url='https://%s' % AUTH0_DOMAIN,
    access_token_method='POST',
    access_token_url='/oauth/token',
    authorize_url='/authorize',
)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated


@app.route('/callback')
def callback_handling():
    resp = auth0.authorized_response()
    if resp is None:
        raise AuthError({'code': request.args['error'],
                         'description': request.args['error_description']}, 401)

    url = 'https://' + AUTH0_DOMAIN + '/userinfo'
    headers = {'authorization': 'Bearer ' + resp['access_token']}
    resp = requests.get(url, headers=headers)
    userinfo = resp.json()

    session[constants.JWT_PAYLOAD] = userinfo

    session[constants.PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    return redirect('/dashboard')


@app.route('/login')
def login():
    return auth0.authorize(callback=AUTH0_CALLBACK_URL)


@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.base_url + '/v2/logout?' + urlencode(params))


@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session[constants.PROFILE_KEY],
                           userinfo_pretty=json.dumps(session[constants.JWT_PAYLOAD], indent=4))


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
    app.on_inserted_data += check_for_analysis

    # Analysis Hooks
    app.on_insert_analysis += register_analysis
    app.on_pre_GET_status += get_job_status

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
