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
        'anyof': ['RAW', 'PARSE'],
        'required': True
    },
    'severity': {
        'type': 'string',
        'anyof': ['WARNING', 'CRITICAL'],
        'required': True
    }
}
