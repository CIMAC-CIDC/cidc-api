#!/usr/bin/env python3
"""
Schema for olink data
"""
from schemas.coercers import FLOAT_COERCER as float_coercer
from schemas.coercers import INT_COERCER as int_coercer
from schemas.validation_error_schema import VALIDATION_ERROR
from schemas.tools import create_biomarker_schema

OLINK_SAMPLE_DATA = {
    'sample_id': {
        'type': 'string',
        'required': True
    },
    'value': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer,
        'nullable': True
    },
    'qc_fail': {
        'type': 'boolean',
        'required': True
    },
    'below_lod': {
        'type': 'boolean',
        'required': True
    }
}

OLINK_ASSAY = {
    'assay': {
        'type': 'string',
        'required': True
    },
    'uniprot_id': {
        'type': 'string',
        'required': True
    },
    'panel': {
        'type': 'string',
        'required': True
    },
    'lod': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer,
        'nullable': True
    },
    'missing_data_freq': {
        'type': 'integer',
        'required': True,
        'coerce': int_coercer
    },
    'results': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': OLINK_SAMPLE_DATA
        }
    },
    'olink_id': {
        'type': 'string',
        'required': True
    }
}

SAMPLE_SCHEMA = {
    'sample_id': {
        'type': 'string',
        'required': True
    },
    'qc_status': {
        'type': 'string',
        'allowed': ['Warning', 'Pass', 'Fail'],
        'required': True
    },
    'plate_id': {
        'type': 'string',
        'required': True
    }
}

OLINK = create_biomarker_schema({
    'npx_m_ver': {
        'type': 'string',
        'nullable': True,
    },
    'ol_assay': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': OLINK_ASSAY
        },
        'nullable': True,
    },
    'ol_panel_type': {
        'type': 'string',
        'nullable': True,
    },
    'samples': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': SAMPLE_SCHEMA
        },
        'nullable': True,
    },
    'validation_errors': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': VALIDATION_ERROR
        }
    }
})
