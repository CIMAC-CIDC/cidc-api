'''[summary]

Returns:
    [type] -- [description]
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
            'trial': {'type': 'string', 'required': True},
            'assay': {'type': 'string', 'required': True},
            'record_id': {'type': 'string', 'required': True},
        },
    }
    base_dict['schema'].update(schema)
    return base_dict
