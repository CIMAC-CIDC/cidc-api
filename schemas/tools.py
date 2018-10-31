'''
Tools for creating eve schemas
'''

def create_biomarker_schema(schema: dict) -> dict:
    '''
    Factory method for creating a schema object.

    Arguments:
        schema {dict} -- Cerberus schema dictionary.

    Returns:
        dict -- EVE endpoint definition.
    '''
    base_dict = {
        'public_methods': [],
        'resource_methods': ['GET', 'POST'],
        'allowed_roles': ['user', 'admin'],
        'schema': {
            'trial': {'type': 'objectid', 'required': True},
            'assay': {'type': 'objectid', 'required': True},
            'record_id': {'type': 'objectid', 'required': True},
        },
    }
    base_dict['schema'].update(schema)
    return base_dict
