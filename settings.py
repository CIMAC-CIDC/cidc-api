#!/usr/bin/env python3
"""
Settings file that lays out the database schema, as well as other constant variables.
"""
from os import environ as env
from schemas.MAF_data_model import MAF
from schemas.hla_schema import HLA
from schemas.neoantigen_schema import NEOANTIGEN
from schemas.tumor_purity_ploidy_schema import PURITY, CONFINTS_CP
from schemas.clonality_schema import CLONALITY_CLUSTER, LOCI, PYCLONE
from schemas.cnv_schema import CNV
from schemas.clinical_data_schema import CLINICAL_1021
from schemas.rsem_schema import RSEM_EXPRESSION, RSEM_ISOFORMS

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_REPLICA_SET = None
MONGO_USERNAME = 'python-eve'
MONGO_PASSWORD = 'apple'
MONGO_DBNAME = 'CIDC'

if env.get('IN_CLOUD'):
    MONGO_URI = "mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017/CIDC?replicaSet=rs0"
    MONGO_OPTIONS = {
        'connect': True,
        'tz_aware': True,
        'appname': 'flask_app_name',
    }

if env.get('JENKINS'):
    MONGO_URI = (
        "mongodb://mongo-0.mongo.default.svc.cluster.local," +
        "mongo-1.mongo.default.svc.cluster.local," +
        "mongo-2.mongo.default.svc.cluster.local" +
        ":27017/TEST?replicaSet=rs0"
        )
    MONGO_DBNAME = "TEST"

GOOGLE_URL = "gs://lloyd-test-pipeline/"
GOOGLE_FOLDER_PATH = "Experimental-Data/"


# If this line is missing API will default to GET only
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT), and delete
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']


DATA = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST'],
    'allowed_roles': ['admin', 'user'],
    'schema': {
        'file_name': {
            'type': 'string',
            'required': True,
        },
        'sample_id': {
            'type': 'string',
            'required': True,
        },
        'trial': {
            'type': 'objectid',
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
        }
    }
}

MAF_PT = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST'],
    'schema': MAF
}

# Aggregation query that groups data by Sample ID
DATA_AGG = {
    'datasource': {
        'source': 'data',
        'aggregation': {
            'pipeline': [
                {'$match': {'trial': '$trial', 'assay': '$assay', 'processed': False}},
                {
                    '$group': {
                        '_id': '$sample_id',
                        'records': {
                            '$push': {
                                'file_name': '$file_name',
                                'gs_uri': '$gs_uri'
                            }
                        }
                    }
                }
            ]
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

ANALYSIS = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST'],
    'allowed_roles': ['admin', 'superuser', 'user'],
    'schema': {
        'start_date': {
            'type': 'string'
        },
        'trial': {
            'type': 'objectid',
            'required': True
        },
        'assay': {
            'type': 'objectid',
            'required': True
        },
        'status': {
            'type': 'dict',
            'schema': {
                'progress': {
                    'type': 'string',
                    'allowed': ['In Progress', 'Completed', 'Aborted']
                },
                'message': {
                    'type': 'string'
                }
            }
        },
        'samples': {
            'type': 'list',
            'schema': {
                'type': 'string'
            }
        },
        'metadata_blob': {
            'type': 'string'
        },
        'files_generated': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'file_name': {
                        'type': 'string',
                        'required': True
                    },
                    'gs_uri': {
                        'type': 'string',
                        'required': True
                    }
                }
            }
        }
    }
}

ANALYSIS_STATUS = {
    'public_methods': [],
    'resource_methods': ['GET'],
    'allowed_roles': ['admin', 'superuser', 'user'],
    'allowed_filters': ['started_by'],
    'datasource': {
        'source': 'analysis',
        'projection': {
            'status': 1
        }
    }
}

ASSAYS = {
    'public_methods': [],
    'resource_methods': ['GET'],
    'allowed_roles': ['admin', 'superuser', 'user'],
    'schema': {
        '_id': {
            'type': 'objectid',
            'required': True,
            'unique': True
        },
        'wdl_location': {
            'type': 'string'
        },
        'assay_name': {
            'type': 'string',
            'required': True
        },
        'static_inputs': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'key_name': {
                        'type': 'string',
                    },
                    'key_value': {
                        'anyof_type': ['string', 'integer'],
                    },
                },
            },
        },
        "non_static_inputs": {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'key_name': {
                        'type': 'string',
                    },
                    'key_value': {
                        'anyof_type': ['string', 'integer'],
                    },
                },
            },
        },
    },
}

TRIALS = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST'],
    'allowed_roles': ['user', 'admin', 'superuser'],
    'allowed_filters': ['collaborators', 'principal_investigator', '_id', 'assays.assay_id'],
    'schema': {
        'trial_name': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'principal_investigator': {
            'type': 'string',
            'required': True,
        },
        'collaborators': {
            'type': 'list',
            'schema': {
                'type': 'string'
            },
        },
        'start_date': {
            'type': 'string',
            'required': True,
        },
        'assays': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'assay_name': {
                        'type': 'string',
                        'required': True
                    },
                    'assay_id': {
                        'type': 'string',
                        'required': True
                    },
                }
            },
        },
        'samples': {
            'type': 'list',
            'schema': {
                'type': 'string',
            }
        },
    },
}

# Schema that keeps track of jobs that users have started, as well as their ultimate status and
# fate
INGESTION = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH'],
    'allowed_roles': ['user', 'superuser', 'admin'],
    'allowed_filters': ['started_by'],
    'schema': {
        'number_of_files': {
            'type': 'integer',
            'required': True,
        },
        'started_by': {
            'type': 'string',
        },
        'status': {
            'type': 'dict',
            'schema': {
                'progress': {
                    'type': 'string',
                    'allowed': ['In Progress', 'Completed', 'Aborted']
                },
                'message': {
                    'type': 'string'
                },
            }
        },
        'start_time': {
            'type': 'string'
        },
        'end_time': {
            'type': 'string',
        },
        'files': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'assay': {
                        'type': 'objectid',
                        'required': True
                    },
                    'trial': {
                        'type': 'objectid',
                        'required': True
                    },
                    'file_name': {
                        'type': 'string',
                        'required': True
                    },
                    'sample_id': {
                        'type': 'string',
                        'required': True
                    },
                    'mapping': {
                        'type': 'string',
                        'required': True
                    }
                },
            },
        },
    },
}

TEST = {
    'schema': {
        'message': {
            'type': 'string',
            'required': False
        }
    },
    'authentication': None
}

X_DOMAINS = [
    'http://editor.swagger.io',
    'http://petstore.swagger.io'
]

X_HEADERS = ['Content-Type', 'If-Match']

DOMAIN = {
    'ingestion': INGESTION,
    'data': DATA,
    'trials': TRIALS,
    'test': TEST,
    'assays': ASSAYS,
    'analysis': ANALYSIS,
    'status': ANALYSIS_STATUS,
    'data/query': DATA_AGG_INPUTS,
    'vcf': MAF_PT,
    'hla': HLA,
    'neoantigen': NEOANTIGEN,
    'purity': PURITY,
    'clonality_cluster': CLONALITY_CLUSTER,
    'loci': LOCI,
    'confints_cp': CONFINTS_CP,
    'pyclone': PYCLONE,
    'cnv': CNV,
    'clinical_data': CLINICAL_1021,
    'rsem_expression': RSEM_EXPRESSION,
    'rsem_isoforms': RSEM_ISOFORMS
}
