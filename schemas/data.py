"""
Data schema, each record represents a file in a google bucket.
"""

DATA = {
    'public_methods': [],
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
    'allowed_roles': ['admin', 'user', 'uploader'],
    'allowed_item_roles': ['admin', 'user', 'uploader'],
    'datasource': {
        'source': 'data',
        'filter': {
            'visibility': True
        },
    },
    'schema': {
        'data_format': {
            "type": "string",
            "required": True,
        },
        'file_name': {
            'type': 'string',
            'required': True,
        },
        'file_size': {
            'type': 'integer',
            'required': True
        },
        'sample_ids': {
            'type': 'list',
            'schema': {
                'type': 'string',
                'required': True
            }
        },
        'number_of_samples': {
            'type': 'integer',
            'required': True
        },
        'trial': {
            'type': 'objectid',
            'required': True,
        },
        'trial_name': {
            'type': 'string',
            'required': True,
        },
        'gs_uri': {
            'type': 'string',
            'required': True,
        },
        'assay': {
            'type': 'objectid',
            'required': True,
        },
        'experimental_strategy': {
            'type': 'string',
            'required': True,
        },
        'date_created': {
            'type': 'string',
            'required': True,
        },
        'analysis_id': {
            'type': 'objectid',
        },
        'mapping': {
            'type': 'string',
            'required': True,
        },
        'processed': {
            'type': 'boolean'
        },
        'visibility': {
            'type': 'boolean'
        },
        'children': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    '_id': {
                        'type': 'objectid',
                        'required': True
                    },
                    'resource': {
                        'type': 'string',
                        'required': True
                    }
                }
            }
        }
    }
}

DATA_EDIT = {
    "public_methods": [],
    "allowed_roles": ["admin"],
    "allowed_item_roles": ["admin"],
    "resource_methods": ["POST"],
    "item_methods": ["PATCH"],
    "datasource": {
        'source': 'data',
    },
    "schema": DATA["schema"]
}

DATA_TOGGLE_VIS = {
    "public_methods": [],
    "allowed_roles": ["admin", "user", "uploader"],
    "allowed_item_roles": ["admin", "user", "uploader"],
    "resource_methods": ["GET"],
    "item_methods": ["PATCH"],
    "datasource": {
        "source": "data",
        "projection": {
            "visibility": 1
        }
    },
    "schema": {
        "visibility": {
            "type": "boolean"
        }
    }
}

DATA_AGG_INPUTS = {
    'datasource': {
        'source': 'data',
        'aggregation': {
            'pipeline': [
                {
                    "$match": {
                        "mapping": {
                            "$in": "$inputs"
                        },
                        "processed": False
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "sample_id": "$sample_id",
                            "assay": "$assay",
                            "trial": "$trial"
                        },
                        "records": {
                            "$push": {
                                "file_name": "$file_name",
                                "gs_uri": "$gs_uri",
                                "mapping": "$mapping",
                                '_id': '$_id'
                            }
                        }
                    }
                }
            ]
        }
    }
}
