"""
Validator schema for copy numebr variant data.
"""
from schemas.coercers import FLOAT_COERCER as float_coercer
from schemas.tools import create_biomarker_schema

CNV = create_biomarker_schema({
    'chromosome': {
        'type': 'string',
        'required': True
    },
    'start_pos': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'end_pos': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'Bf': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'N_BAF': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
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
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'sd_ratio': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'CNt': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'A': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'B': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'LPP': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    }
})
