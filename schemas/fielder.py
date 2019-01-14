"""
A module defining 'fielder' which is a shortcut method for generating cerberus schemas.
"""
from typing import Tuple, List


def fielder(
    field_name: str, d_type: str = "string", subschema: dict = None, **kwargs
) -> Tuple[str, object]:
    """
    Time saving method for generating cerberus schemas. Generates a key-value pair that
    can be passed as a tuple to an update function. Schema nesting should work as long as
    you pass in the appropriate type (dict for a simple subschema, list for a list-of-type).
    If its a simple subschema e.g., 'list of str', simply pass the subschema type ('str')
    as the subschema value.

    Arguments:
        field_name {str} -- Name of the field.

    Keyword Arguments:
        d_type {str} -- The cerberus-format data type of the field. (default: {'string'})
        subschema {dict} -- Any schema nested below the parent schema. (default: {None})

    Returns:
        Tuple[str, object] -- Key value pair to be added to the schema.
    """
    field_definition = {field_name: {"type": d_type}}

    for arg_name, arg_val in kwargs.items():
        field_definition[field_name][arg_name] = arg_val

    if subschema:
        if d_type == "list":
            if isinstance(subschema, dict):
                field_definition[field_name]["schema"] = {
                    "type": "dict",
                    "schema": subschema,
                }
            elif isinstance(subschema, str):
                field_definition[field_name]["schema"] = {"type": subschema}
        elif d_type == "dict":
            field_definition[field_name]["schema"] = subschema

    (key, value), = field_definition.items()
    return key, value


def fielder_array(fields: List[Tuple[str, dict]]) -> dict:
    """
    Applies the fielder function to an array of fields.

    Arguments:
        fields {List[Tuple[str, dict]]} -- List of field specifications, with item 0 being the field
            name, and item 1 being the named options.
    Returns:
        dict -- Cerberus schema, put this in the "schema" key of a new schema that you create.
    """
    return {}.update([fielder(x[0], **x[1]) for x in fields])
