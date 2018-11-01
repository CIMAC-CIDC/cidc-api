"""
Validator for Analysis data.
"""

ANALYSIS = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST'],
    'allowed_roles': ['admin', 'superuser', 'user'],
    'schema': {
        'start_date': {
            'type': 'string'
        },
        'trial': {
            'type': 'objectid',
            'required': True
        },
        'assay': {
            'type': 'objectid',
            'required': True
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
                }
            }
        },
        'samples': {
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
    'datasource': {
        'source': 'analysis',
        'projection': {
            'status': 1
        }
    }
}