"""
Validator for Analysis data.
"""

ANALYSIS = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST'],
    'allowed_roles': ['admin', 'superuser', 'user'],
    'allowed_item_roles': ['admin', 'superuser', 'user'],
    'schema': {
        'start_date': {
            'type': 'string'
        },
        'end_date': {
            'type': 'string'
        }
        'trial': {
            'type': 'objectid',
            'required': True
        },
        'trial_name': {
            'type': 'string',
            'required': True
        }
        'assay': {
            'type': 'objectid',
            'required': True
        },
        'experimental_strategy': {
            'type': 'string',
            'required': True
        },
        'logs': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'job_id': {
                        'type': 'string',
                        'required': True
                    },
                    'log_location': {
                        'type': 'string',
                        'required': True
                    }
                }
            }
        },
        'status': {
            'type': 'str',
            'allowed': ['In Progress', 'Completed', 'Aborted', 'Failed'],
            'required': True
        },
        'error_message': {
            'type': 'str',
            'nullable': True
        },
        'sample_ids': {
            'type': 'list',
            'schema': {
                'type': 'string'
            }
        },
        'metadata_blob': {
            'type': 'string'
        },
        'files_generated': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'file_name': {
                        'type': 'string',
                        'required': True
                    },
                    'gs_uri': {
                        'type': 'string',
                        'required': True
                    }
                }
            }
        }
    }
}

ANALYSIS_STATUS = {
    'public_methods': [],
    'resource_methods': ['GET'],
    'allowed_roles': ['admin', 'superuser', 'user'],
    'allowed_filters': ['started_by'],
    'allowed_item_roles': ['admin', 'superuser', 'user'],
    'datasource': {
        'source': 'analysis',
        'projection': {
            'status': 1
        }
    }
}