"""
Validator schema for copy numebr variant data.
"""
from schemas import int_coercer, float_coercer, create_biomarker_schema

CNV = create_biomarker_schema({
    'chromosome': {
        'type': 'string',
        'required': True
    },
    'start_pos': {
        'type': 'integer',
        'required': True,
        'coerce': int_coercer
    },
    'end_pos': {
        'type': 'integer',
        'required': True,
        'coerce': int_coercer
    },
    'Bf': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'N_BAF': {
        'type': 'integer',
        'required': True,
        'coerce': int_coercer
    },
    'sd_BAF': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'depth_ratio': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'N_ratio': {
        'type': 'integer',
        'required': True,
        'coerce': int_coercer
    },
    'sd_ratio': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'CNt': {
        'type': 'integer',
        'required': True,
        'coerce': int_coercer
    },
    'A': {
        'type': 'integer',
        'required': True,
        'coerce': int_coercer
    },
    'B': {
        'type': 'integer',
        'required': True,
        'coerce': int_coercer
    },
    'LPP': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    }
})
