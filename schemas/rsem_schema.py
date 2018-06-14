#!/usr/bin/env python3
"""
Schema for rsem outputs
"""
from schemas import int_coercer, float_coercer, create_biomarker_schema


RSEM_EXPRESSION = create_biomarker_schema({
    'gene_id': {
        'type': 'string',
        'required': True
    },
    'transcript_id(s)': {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'string'
        }
    },
    'length': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'effective_length': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'expected_count': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'TPM': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'FPKM': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    }
})

RSEM_ISOFORMS = create_biomarker_schema({
    'transcript_id': {
        'type': 'string',
        'required': True
    },
    'gene_id': {
        'type': 'string',
        'required': True
    },
    'length': {
        'type': 'integer',
        'required': True,
        'coerce': int_coercer
    },
    'effective_length': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'expected_count': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'TPM': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'FPKM': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'IsoPct': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    }
})
