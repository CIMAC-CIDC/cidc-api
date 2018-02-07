#!/usr/bin/env python
"""
Settings file that lays out the database schema, as well as other constant variables.
"""

MONGO_HOST = 'mongodb'
MONGO_PORT = 27017
MONGO_USERNAME = 'python-eve'
MONGO_PASSWORD = 'apple'
MONGO_DBNAME = 'CIDC'
GOOGLE_URL = "gs://lloyd-test-pipeline/"
GOOGLE_FOLDER_PATH = "Experimental-Data/"
RABBITMQ_URI = "rabbitmq:5762"

# If this line is missing API will default to GET only
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT), and delete
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

ACCOUNTS = {
    'public_methods': ['POST'],
    'resource_methods': ['GET', 'POST'],
    # Disable endpoint caching so clients don't cache account data
    'cache_control': '',
    'cache_expires': 0,
    'allowed_roles': ['superuser', 'admin'],
    'schema': {
        'token': {
            'type': 'string',
            'required': True,
        }
    },
}

# Schema that keeps track of jobs that users have started, as well as their ultimate status and
# fate
JOBS = {
    'allowed_roles': ['user', 'superuser', 'admin'],
    'schema': {
        'experiment_name': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'number_of_files': {
            'type': 'integer',
            'required': True,
        },
        'started_by': {
            'type': 'string',
            'required': True,
        },
        'status': {
            'type': 'dict',
            'schema': {
                'progress': {
                    'type': 'string',
                    'allowed': ['In Progress', 'Completed', 'Aborted']
                },
                'message': {
                    'type': 'string'
                },
            }
        },
        'start_time': {
            'type': 'string',
            'required': True,
        },
        'end_time': {
            'type': 'string',
        },
        'files': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'filename': {
                        'type': 'string'
                    },
                    'google_uri': {
                        'type': 'string'
                    },
                },
            },
        },
    },
}

DOMAIN = {
    'accounts': ACCOUNTS,
    'jobs': JOBS,
}
