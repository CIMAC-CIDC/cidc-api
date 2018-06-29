#!/usrbin/env python3
"""
Schema for users of the database.
"""

DB_USER = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST'],
    'allowed_roles': ['admin'],
    'schema': {
        'username': {
            'type': 'string',
        },
        'e-mail': {
            'type': 'string',
            'regex': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        },
        'organization': {
            'type': 'string',
        },
        'last_access': {
            'type': 'date',
        },
        'first_n': {
            'type': 'string',
        },
        'last_n': {
            'type': 'string',
        },
        'role': {
            'type': 'string',
            'oneof': ['reader', 'uploader', 'lead', 'admin', 'developer'],
        }
    }
}
