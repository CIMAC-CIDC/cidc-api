"""
Schema for standard error validation.
"""

VALIDATION_ERROR = {
    'explanation': {
        'type': 'string',
        'required': True,
    },
    'affected_paths': {
        'type': 'list',
        'schema': {
            'type': 'string',
            'required': True
        }
    },
    'raw_or_parse': {
        'type': 'string',
        'allowed': ['RAW', 'PARSE'],
        'required': True
    },
    'severity': {
        'type': 'string',
        'allowed': ['WARNING', 'CRITICAL'],
        'required': True
    }
}
