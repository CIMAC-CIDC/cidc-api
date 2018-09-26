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
        'email': {
            'type': 'string',
            'regex': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'required': True,
            'unique': True
        },
        'preferred_contact_email': {
            'type': 'string',
            'regex': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'required': True
        },
        'organization': {
            'type': 'string',
        },
        'last_access': {
            'type': 'date',
        },
        'account_create_date': {
            'type': 'date',
        },
        'registration_submit_date': {
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
        'registered': {
            'type': 'boolean',
            'required': True
        },
        'role': {
            'type': 'string',
            'oneof': ['registrant', 'reader', 'uploader', 'lead', 'admin', 'developer'],
        },
        'position_description': {
            'type': 'string',
            'required': False
        }
    }
}

DB_ACCOUNTS_INFO = {
    'public_methods': [],
    'resource_methods': ['GET'],
    'allowed_roles': ['registrant', 'reader', 'uploader', 'lead', 'admin', 'developer'],
    'item_methods': [],
    'datasource': {
        'source': 'accounts'
    },
    'schema': {
        'username': {
            'type': 'string'
        },
        'e-mail': {
            'type': 'string'
        },
        'organization': {
            'type': 'string'
        },
        'last_access': {
            'type': 'date'
        },
        'registration_submit_date': {
            'type': 'date',
        },
        'first_n': {
            'type': 'string'
        },
        'last_n': {
            'type': 'string'
        },
        'registered': {
            'type': 'boolean'
        },
        'role': {
            'type': 'string'
        },
        'position_description': {
            'type': 'string'
        }
    }
}

DB_ACCOUNTS_UPDATE = {
    'public_methods': [],
    'resource_methods': ['GET'],
    'item_methods': ['PATCH', 'GET'],
    'allowed_item_roles': ['registrant', 'reader', 'uploader', 'lead', 'admin', 'developer'],
    'datasource': {
        'source': 'accounts'
    },
    'schema': {
        'preferred_contact_email': {
            'type': 'string',
            'regex': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'required': True
        },
        'organization': {
            'type': 'string',
            'required': True
        },
        'first_n': {
            'type': 'string',
            'required': True
        },
        'last_n': {
            'type': 'string',
            'required': True
        },
        'registered': {
            'type': 'boolean',
            'required': True
        },
        'registration_submit_date': {
            'type': 'datetime',
            'required': False
        },
        'position_description': {
            'type': 'string',
            'required': False
        }
    }
}


