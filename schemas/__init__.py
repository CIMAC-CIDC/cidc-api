"""
Module that stores the record validators for eve.
"""
from schemas.coercers import FLOAT_COERCER as float_coercer, INT_COERCER as int_coercer


def create_biomarker_schema(schema: dict) -> dict:
    """[summary]

    Arguments:
        schema {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    base_dict = {
        'public_methods': [],
        'resource_methods': ['GET', 'POST'],
        'allowed_roles': ['user', 'admin'],
        'schema': {
            'trial': {
                'type': 'string',
                'required': True
            },
            'assay': {
                'type': 'string',
                'required': True
            },
            'record_id': {
                'type': 'string',
                'required': True
            }
        }
    }
    base_dict['schema'].update(schema)
    return base_dict
