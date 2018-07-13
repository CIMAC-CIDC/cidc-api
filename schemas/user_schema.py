#!/usrbin/env python3
"""
Schema for users of the database.
"""

DB_USER = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'allowed_roles': ['admin'],
    'cache_control': '',
    'cache_expires': 0,
    'schema': {
        'username': {
            'type': 'string',
            'required': True,
            'unique': True
        },
        'e-mail': {
            'type': 'string',
            'regex': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'required': True,
            'unique': True
        },
        'organization': {
            'type': 'string',
        },
        'last_access': {
            'type': 'date',
        },
        'first_n': {
            'type': 'string',
            'required': True
        },
        'last_n': {
            'type': 'string',
            'required': True
        },
        'role': {
            'type': 'string',
            'oneof': ['reader', 'uploader', 'lead', 'admin', 'developer'],
        }
    }
}
