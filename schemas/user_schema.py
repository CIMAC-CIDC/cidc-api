#!/usrbin/env python3
"""
Schema for users of the database.
"""

DB_USER = {
    'public_methods': [],
    'public_item_methods': [],
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'allowed_roles': ['admin'],
    'allowed_item_roles': ['admin'],
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
            'type': 'string',
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
            'allowed': ['registrant', 'reader', 'uploader', 'lead', 'admin', 'developer',
                        'disabled'],
            'type': 'string',
            'required': True
        },
        'position_description': {
            'type': 'string',
            'required': False
        },
        'permissions': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'assay': {
                        'type': 'objectid',
                        'required': True,
                        'nullable': True
                    },
                    'trial': {
                        'type': 'objectid',
                        'required': True,
                        'nullable': True
                    },
                    'role': {
                        'allowed': ['read', 'write', 'trial_r', 'trial_w', 'assay_r', 'assay_w'],
                        'required': True,
                        'type': 'string'
                    }
                }
            }
        },
    }
}

DB_ACCOUNTS_INFO = {
    'public_methods': [],
    'resource_methods': ['GET'],
    'allowed_roles': ['registrant', 'reader', 'uploader', 'lead', 'admin', 'developer'],
    'allowed_item_roles': ['registrant', 'reader', 'uploader', 'lead', 'admin', 'developer'],
    'item_methods': [],
    'datasource': {
        'source': 'accounts'
    },
    'schema': {
        'username': {
            'type': 'string',
            'unique': True
        },
        'email': {
            'type': 'string',
            'regex': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'unique': True
        },
        'organization': {
            'type': 'string'
        },
        'last_access': {
            'type': 'date'
        },
        'registration_submit_date': {
            'type': 'string',
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
            'required': True,
            'unique': True
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
            'type': 'string',
            'required': False
        },
        'position_description': {
            'type': 'string',
            'required': False
        }
    }
}
