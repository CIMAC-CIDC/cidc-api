#!/usr/bin/env python3
"""
Settings file that lays out the database schema, as well as other constant variables.
"""
import logging
from os import environ as env
from dotenv import find_dotenv, load_dotenv

import schemas

AUTH0_AUDIENCE = env.get('AUTH0_AUDIENCE')
AUTH0_CALLBACK_URL = env.get('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = env.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = env.get('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = env.get('AUTH0_DOMAIN')
ALGORITHMS = ["RS256"]
AUTH0_PORTAL_AUDIENCE = env.get('AUTH0_PORTAL_AUDIENCE')
GOOGLE_URL = env.get('GOOGLE_URL')
GOOGLE_FOLDER_PATH = env.get('GOOGLE_FOLDER_PATH')
RABBIT_MQ_ADDRESS = 'amqp://rabbitmq'

# Default credentials for a local mongodb, do NOT use for production
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = 'python-eve'
MONGO_PASSWORD = 'apple'
MONGO_DBNAME = 'CIDC'
MONGO_OPTIONS = None

# Rate limiting
RATE_LIMIT_GET_REQUESTS = env.get('RATE_LIMIT_GET_REQUESTS')
RATE_LIMIT_POST_REQUESTS = env.get('RATE_LIMIT_POST_REQUESTS')
RATE_LIMIT_PATCH_REQUESTS = env.get('RATE_LIMIT_PATCH_REQUESTS')
RATE_LIMIT_DELETE_REQUESTS = env.get('RATE_LIMIT_DELETE_REQUESTS')

RATE_LIMIT_GET_WINDOW = env.get('RATE_LIMIT_GET_WINDOW')
RATE_LIMIT_POST_WINDOW = env.get('RATE_LIMIT_POST_WINDOW')
RATE_LIMIT_PATCH_WINDOW = env.get('RATE_LIMIT_PATCH_WINDOW')
RATE_LIMIT_DELETE_WINDOW = env.get('RATE_LIMIT_DELETE_WINDOW')

RATE_LIMIT_GET = (int(RATE_LIMIT_GET_REQUESTS), int(RATE_LIMIT_GET_WINDOW))
RATE_LIMIT_POST = (int(RATE_LIMIT_POST_REQUESTS), int(RATE_LIMIT_POST_WINDOW))
RATE_LIMIT_PATCH = (int(RATE_LIMIT_PATCH_REQUESTS), int(RATE_LIMIT_PATCH_WINDOW))
RATE_LIMIT_DELETE = (int(RATE_LIMIT_DELETE_REQUESTS), int(RATE_LIMIT_DELETE_WINDOW))

if not env.get('IN_CLOUD'):
    logging.info({
        'message': 'notincloud',
        'category': 'INFO-EVE-DEBUG'
    })
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)

if env.get('IN_CLOUD'):
    MONGO_OPTIONS = {
        'connect': True,
        'tz_aware': True,
        'appname': 'flask_app_name',
    }
    MONGO_HOST = env.get('MONGO_HOST')
    MONGO_USERNAME = env.get('MONGO_USERNAME').strip()
    MONGO_PASSWORD = env.get('MONGO_PASSWORD').strip()
    MONGO_DBNAME = env.get('MONGO_DBNAME')
    MONGO_AUTH_SOURCE = env.get('MONGO_AUTH_SOURCE')
    MONGO_REPLICA_SET = env.get('MONGO_REPLICA_SET')
    if env.get('MONGO_PORT'):
        MONGO_PORT = int(env.get('MONGO_PORT'))
    RABBIT_MQ_ADDRESS = (
        'amqp://' + env.get('RABBITMQ_SERVICE_HOST') + ':' + env.get('RABBITMQ_SERVICE_PORT')
    )

if env.get('JENKINS'):
    MONGO_HOST = env.get('MONGO_HOST_JENKINS')
    MONGO_DBNAME = env.get('MONGO_DBNAME_JENKINS')

if AUTH0_AUDIENCE == '':
    AUTH0_AUDIENCE = 'https://' + AUTH0_DOMAIN + '/userinfo'

# If this line is missing API will default to GET only
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT), and delete
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

TEST = {
    'schema': {
        'message': {
            'type': 'string',
            'required': False
        }
    },
    'authentication': None
}

X_DOMAINS = [
    'http://editor.swagger.io',
    'http://petstore.swagger.io'
]

X_HEADERS = ['Content-Type', 'If-Match']

DOMAIN = {
    'ingestion': schemas.INGESTION,
    'data': schemas.DATA,
    'trials': schemas.TRIALS,
    'test': TEST,
    'assays': schemas.ASSAYS,
    'analysis': schemas.ANALYSIS,
    'status': schemas.ANALYSIS_STATUS,
    'data/query': schemas.DATA_AGG_INPUTS,
    'data_edit': schemas.DATA_EDIT,
    'vcf': schemas.MAF_PT,
    'hla': schemas.HLA,
    'neoantigen': schemas.NEOANTIGEN,
    'purity': schemas.PURITY,
    'clonality_cluster': schemas.CLONALITY_CLUSTER,
    'loci': schemas.LOCI,
    'confints_cp': schemas.CONFINTS_CP,
    'pyclone': schemas.PYCLONE,
    'cnv': schemas.CNV,
    'clinical_data': schemas.CLINICAL_1021,
    'rsem_expression': schemas.RSEM_EXPRESSION,
    'rsem_isoforms': schemas.RSEM_ISOFORMS,
    'accounts': schemas.DB_USER,
    'accounts_info': schemas.DB_ACCOUNTS_INFO,
    'accounts_update': schemas.DB_ACCOUNTS_UPDATE,
    'olink': schemas.OLINK,
    'olink_meta': schemas.BIOREPOSITORY
}
