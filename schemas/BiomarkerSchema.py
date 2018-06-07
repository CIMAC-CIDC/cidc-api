"""
Class for implementing cerberus schemas that inherit a few fields.
"""


class BiomarkerSchema:
    """
    Creates an object with basic types set that can be used to more easily
    generate conformant schema.
    """
    def __init__(self, schema):
        self._validator = {
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
        self._validator['schema'].update(schema)

    def return_validator(self):
        """[summary]

        Returns:
            [type] -- [description]
        """
        return self._validator
