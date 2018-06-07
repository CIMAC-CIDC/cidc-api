"""
Data schema for Tumor purity data (Facets)
"""
from schemas import float_coercer, create_biomarker_schema

PURITY = create_biomarker_schema({
    'name': {
        'type': 'string',
        'required': True
    },
    'mode': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'purity': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'ploidy': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'dipLogR': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    }
})

CONFINTS_CP = create_biomarker_schema({
    'cellularity': {
        'type': 'float',
        'coerce': float_coercer
    },
    'ploidy_estimate': {
        'type': 'float',
        'coerce': float_coercer
    },
    'ploidy_mean_cn': {
        'type': 'float',
        'coerce': float_coercer
    }
})
