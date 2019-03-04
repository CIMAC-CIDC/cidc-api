#!/usr/bin/env python3
"""
Validator for Trial data.
"""
from schemas.fielder import fielder


TRIALS = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['PATCH'],
    'allowed_read_roles': ['user', 'uploader', 'system'],
    'allowed_roles': ['admin', 'superuser', 'system'],
    'allowed_item_read_roles': ['user', 'uploader', 'system'],
    'allowed_item_roles': ['admin', 'superuser', 'system'],
    'allowed_filters': ['collaborators', 'principal_investigator', '_id',
                        'assays.assay_id'],
    'schema': {
        'trial_name': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'principal_investigator': {
            'type': 'string',
            'required': True,
        },
        'collaborators': {
            'type': 'list',
            'schema': {
                'type': 'string'
            },
        },
        'start_date': {
            'type': 'string',
            'required': True,
        },
        'assays': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'assay_name': {
                        'type': 'string',
                        'required': True
                    },
                    'assay_id': {
                        'type': 'objectid',
                        'required': True
                    },
                }
            },
        },
        'samples': {
            'type': 'list',
            'schema': {
                'type': 'string',
            }
        },
    },
}

CHILDDOCUMENTS = {}
CHILDDOCUMENTS.update([
    fielder('document_id', d_type='objectid', required=True),
    fielder('collection', required=True)
])

INPUTSCHEMA = {}
INPUTSCHEMA.update([
    fielder('record', d_type='objectid', required=True),
    fielder('file_name', required=True),
    fielder('gs_uri', required=True),
    fielder('children', d_type='list', subschema=CHILDDOCUMENTS)
])

RUNSCHEMA = {}
RUNSCHEMA.update([
    fielder('assay', d_type='objectid', required=True),
    fielder('inputs', d_type='list', subschema=INPUTSCHEMA)
])

TRIALS['schema'].update(
    [
        fielder("runs", d_type="list", subschema=RUNSCHEMA)
    ]
)
