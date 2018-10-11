'''[summary]

Returns:
    [type] -- [description]
'''


def fielder(field_name: str, d_type:str='string', subschema:dict=None, **kwargs) -> dict:
    '''
    Time saving method for generating cerberus schemas. Generates a key-value pair that
    can be passed as a tuple to an update function. Schema nesting should work as long as
    you pass in the appropriate type (dict for a simple subschema, list for a list-of-type).
    If its a simple subschema e.g., 'list of str', simply pass the subschema type ('str')
    as the subschema value.

    Arguments:
        field_name {str} -- Name of the field.

    Keyword Arguments:
        d_type {str} -- The cerberus-format data type of the field. (default: {'string'})
        subschema {[type]} -- Any schema nested below the parent schema. (default: {None})

    Returns:
        [type] -- [description]
    '''
    field_definition = {field_name: {'type': d_type}}

    for arg_name, arg_val in kwargs.items():
        field_definition[field_name][arg_name] = arg_val

    if subschema:
        if d_type == 'list':
            if isinstance(subschema, dict):
                field_definition[field_name]['schema'] = {
                    'type': 'dict',
                    'schema': subschema,
                }
            elif isinstance(subschema, str):
                field_definition[field_name]['schema'] = {'type': subschema}
        elif d_type == 'dict':
            field_definition[field_name]['schema'] = subschema

    (key, value), = field_definition.items()
    return key, value
