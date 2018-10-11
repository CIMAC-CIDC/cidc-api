'''
Schema for shipping manifests
'''
from schemas.fielder import fielder
from schemas.validation_error_schema import VALIDATION_ERROR
from schemas.coercers import INT_COERCER, FLOAT_COERCER
from schemas.tools import create_biomarker_schema


SAMPLE_SCHEMA = {
    'pathology_report': {
        'type': 'string',
        'required': True
    },
    'time_point': {
        'type': 'string',
        'required': True
    },
    'specimen_type': {
        'type': 'string',
        'required': True
    },
    'specimen_format': {
        'type': 'string',
        'required': True
    },
    'collection_date': {
        'type': 'string',
        'required': True
    },
    'processing_date': {
        'type': 'string',
        'required': True
    },
    'quantity': {
        'type': 'integer',
        'required': True,
    },
    'volume': {
        'type': 'float',
        'required': True,
    },
    'units': {
        'type': 'string',
        'required': True
    },
    'sample_source': {
        'type': 'string',
        'required': True
    },
    'comments': {
        'type': 'string',
        'nullable': True
    }
}

SAMPLESCHEMA = {}
SAMPLESCHEMA.update(
    [
        fielder('pathology_report'),
        fielder('time_point'),
        fielder('specimen_type'),
        fielder('specimen_format'),
        fielder('collection_date'),
        fielder('processing_date'),
        fielder('quantity', d_type='integer'),
        fielder('volume', d_type='float'),
        fielder('units'),
        fielder('sample_source'),
        fielder('comments'),
    ]
)
OLINK_META = {}

OL_SCHEMA = create_biomarker_schema({
    'manifest_id': {
        'type': 'string',
        'nullable': True
    },
    'protocol_id': {
        'type': 'string',
        'nullable': True
    },
    'request': {
        'type': 'string',
        'nullable': True
    },
    'assay_priority': {
        'type': 'string',
        'nullable': True
    },
    'assay_type': {
        'type': 'string',
        'nullable': True
    },
    'batch_number': {
        'type': 'string',
        'nullable': True
    },
    'courier': {
        'type': 'string',
        'nullable': True
    },
    'tracking_number': {
        'type': 'integer',
        'nullable': True
    },
    'shipping_condition': {
        'type': 'string',
        'nullable': True
    },
    'date_shipped': {
        'type': 'string',
        'nullable': True
    },
    'number_shipped': {
        'type': 'string',
        'nullable': True
    },
    'account_number': {
        'type': 'string',
        'nullable': True
    },
    'sender_name': {
        'type': 'string',
        'nullable': True
    },
    'sender_address': {
        'type': 'string',
        'nullable': True
    },
    'sender_email': {
        'type': 'string',
        'nullable': True
    },
    'receiver_name': {
        'type': 'string',
        'nullable': True
    },
    'receiver_address': {
        'type': 'string',
        'nullable': True
    },
    'receiver_email': {
        'type': 'string',
        'nullable': True
    },
    'validation_errors': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': VALIDATION_ERROR
        },
        'required': True
    },
    'samples': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': SAMPLE_SCHEMA
        },
        'required': True
    }
})

OLINK_META.update(
    [
        fielder('manifest_id', required=True),
        fielder('protocol_id', required=True),
        fielder('request'),
        fielder('assay_priority'),
        fielder('assay_type'),
        fielder('batch_number', required=True),
        fielder('courier'),
        fielder('tracking_number'),
        fielder('shipping_condition'),
        fielder('date_shipped'),
        fielder('number_shipped'),
        fielder('account_number'),
        fielder('sender_name'),
        fielder('sender_address'),
        fielder('sender_email'),
        fielder('receiver_name'),
        fielder('receiver_address'),
        fielder('receiver_email'),
        fielder('samples', d_type='list', subschema=SAMPLESCHEMA),
        fielder('validation_errors', d_type='list', subschema=VALIDATION_ERROR)
    ]
)

BIOREPOSITORY = create_biomarker_schema(OLINK_META)
