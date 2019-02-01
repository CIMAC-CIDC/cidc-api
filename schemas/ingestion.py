"""
Validator for data about jobs.
"""
from schemas.fastq_schema import FASTQ_SCHEMA

# Schema that keeps track of jobs that users have started, as well as their ultimate status and
# fate
INGESTION = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH'],
    'allowed_roles': ['user', 'superuser', 'admin', 'uploader'],
    'allowed_item_roles': ['user', 'superuser', 'admin', 'uploader'],
    'allowed_filters': ['started_by'],
    'schema': {
        'number_of_files': {
            'type': 'integer',
            'required': True,
        },
        'started_by': {
            'type': 'string',
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
            'type': 'string'
        },
        'end_time': {
            'type': 'string',
        },
        'files': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'assay': {
                        'type': 'objectid',
                        'required': True
                    },
                    "experimental_strategy": {
                        "type": "string",
                        "required": False
                    },
                    "data_format": {
                        "type": "string",
                        "required": False
                    },
                    "file_size": {
                        "type": "integer",
                        "required": False
                    },
                    "number_of_samples": {
                        "type": "integer",
                        "required": False
                    },
                    'trial': {
                        'type': 'objectid',
                        'required': True
                    },
                    'file_name': {
                        'type': 'string',
                        'required': True
                    },
                    "trial_name": {
                        "type": "string",
                        "required": False
                    },
                    'sample_ids': {
                        'type': 'list',
                        'schema': {
                            'type': 'string'
                        },
                        'required': False
                    },
                    'mapping': {
                        'type': 'string',
                        'required': False
                    },
                    'fastq_properties': {
                        'type': 'dict',
                        'nullable': True,
                        'schema': FASTQ_SCHEMA
                    },
                },
            },
        },
    },
}
