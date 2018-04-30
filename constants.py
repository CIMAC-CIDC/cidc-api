#!/usr/bin/env python3
"""
Constants file for computing some environmental variables.
"""

import logging
from os import environ as env
from dotenv import find_dotenv, load_dotenv
from cidc_utils.loghandler import RabbitMQHandler

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

if env.get('IN_CLOUD'):
    RABBIT_MQ_ADDRESS = (
        'amqp://' + env.get('RABBITMQ_SERVICE_HOST') + ':' + env.get('RABBITMQ_SERVICE_PORT')
    )

AUTH0_CALLBACK_URL = env.get('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = env.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = env.get('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = env.get('AUTH0_DOMAIN')
AUTH0_AUDIENCE = env.get('AUTH0_AUDIENCE')
ALGORITHMS = ["RS256"]
RABBIT_MQ_ADDRESS = 'amqp://rabbitmq'

# RABBIT_MQ_HANDLER = RabbitMQHandler(uri=RABBIT_MQ_ADDRESS)
LOGGER = logging.getLogger('ingestion-api')
LOGGER.setLevel(logging.DEBUG)
# LOGGER.addHandler(RABBIT_MQ_HANDLER)

if AUTH0_AUDIENCE is '':
    AUTH0_AUDIENCE = 'https://' + AUTH0_DOMAIN + '/userinfo'
