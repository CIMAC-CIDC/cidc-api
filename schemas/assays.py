#!/usr/bin/env python3
"""
Validator for assay data.
"""

ASSAYS = {
    'public_methods': [],
    'resource_methods': ['GET'],
    'allowed_roles': ['admin', 'superuser', 'user', 'uploader'],
    'schema': {
        '_id': {
            'type': 'objectid',
            'required': True,
            'unique': True
        },
        'wdl_location': {
            'type': 'string'
        },
        'assay_name': {
            'type': 'string',
            'required': True
        },
        'static_inputs': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'key_name': {
                        'type': 'string',
                    },
                    'key_value': {
                        'anyof_type': ['string', 'integer'],
                    },
                },
            },
        },
        "non_static_inputs": {
            'type': 'list',
            'schema': {
                'type': 'string'
            },
        },
    },
}