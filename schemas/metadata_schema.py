"""
Schema for shipping manifests
"""
from schemas.coercers import INT_COERCER, FLOAT_COERCER


def fielder(field_name: str, d_type:str="string", subschema:dict=None, **kwargs) -> dict:
    """
    Time saving method for generating cerberus schemas. Generates a key-value pair that
    can be passed as a tuple to an update function. Schema nesting should work as long as
    you pass in the appropriate type (dict for a simple subschema, list for a list-of-type).
    If its a simple subschema e.g., "list of str", simply pass the subschema type ('str')
    as the subschema value.

    Arguments:
        field_name {str} -- Name of the field.

    Keyword Arguments:
        d_type {str} -- The cerberus-format data type of the field. (default: {"string"})
        subschema {[type]} -- Any schema nested below the parent schema. (default: {None})

    Returns:
        [type] -- [description]
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


SAMPLESCHEMA = {}
SAMPLESCHEMA.update(
    [
        fielder("pathology_report"),
        fielder("time_point"),
        fielder("specimen_type"),
        fielder("specimen_format"),
        fielder("collection_date"),
        fielder("processing_date"),
        fielder("quantity", d_type="int", coercer=INT_COERCER),
        fielder("volume", d_type="float", coercer=FLOAT_COERCER),
        fielder("units"),
        fielder("sample_source"),
        fielder("comments"),
    ]
)
OLINK_META = {}
OLINK_META.update(
    [
        fielder("manifest_id", required=True),
        fielder("protocol_id", required=True),
        fielder("request"),
        fielder("assay_priority"),
        fielder("assay_type"),
        fielder("batch_number", required=True),
        fielder("courier"),
        fielder("tracking_number"),
        fielder("shipping_condition"),
        fielder("date_shipped"),
        fielder("number_shipped"),
        fielder("account_number"),
        fielder("sender_name"),
        fielder("sender_address"),
        fielder("sender_email"),
        fielder("receiver_name"),
        fielder("receiver_address"),
        fielder("receiver_email"),
        fielder("samples", d_type="list", subschema=SAMPLESCHEMA),
    ]
)
