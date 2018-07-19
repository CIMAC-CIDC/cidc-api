#!/usr/bin/env python3
"""
Constants file for computing some environmental variables.
"""
from os import environ as env
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_AUDIENCE = env.get('AUTH0_AUDIENCE')
AUTH0_CALLBACK_URL = env.get('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = env.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = env.get('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = env.get('AUTH0_DOMAIN')
ALGORITHMS = ["RS256"]

GOOGLE_URL = env.get('GOOGLE_URL')
GOOGLE_FOLDER_PATH = env.get('GOOGLE_FOLDER_PATH')
RABBIT_MQ_ADDRESS = 'amqp://rabbitmq'
# Default credentials for a local mongodb, do NOT use for production

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
# MONGO_USERNAME = 'python-eve'
# MONGO_PASSWORD = 'apple'
MONGO_DBNAME = 'CIDC'
MONGO_OPTIONS = None
MONGO_URI = None

if env.get('IN_CLOUD'):
    MONGO_OPTIONS = {
        'connect': True,
        'tz_aware': True,
        'appname': 'flask_app_name',
    }
    MONGO_URI = env.get('MONGO_URI')
    # MONGO_USERNAME = env.get('MONGO_USERNAME')
    # MONGO_PASSWORD = env.get('MONGO_PASSWORD')
    MONGO_DBNAME = env.get('MONGO_DBNAME')
    if (env.get('MONGO_PORT')):
        MONGO_PORT = int(env.get('MONGO_PORT'))
    RABBIT_MQ_ADDRESS = (
        'amqp://' + env.get('RABBITMQ_SERVICE_HOST') + ':' + env.get('RABBITMQ_SERVICE_PORT')
    )

if env.get('JENKINS'):
    MONGO_URI = env.get('MONGO_URI_JENKINS')
    MONGO_DBNAME = env.get('MONGO_URI_JENKINS')

if AUTH0_AUDIENCE == '':
    AUTH0_AUDIENCE = 'https://' + AUTH0_DOMAIN + '/userinfo'
