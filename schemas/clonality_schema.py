"""
Schemas for the various clonality metrics
"""
from schemas.coercers import FLOAT_COERCER as float_coercer
from schemas.tools import create_biomarker_schema

CLONALITY_CLUSTER = create_biomarker_schema({
    'sample_id': {
        'type': 'string',
        'required': True
    },
    'cluster_id': {
        'type': 'float',
        'coerce': float_coercer,
        'required': True
    },
    'size': {
        'type': 'float',
        'coerce': float_coercer,
        'required': True
    },
    'mean': {
        'type': 'float',
        'coerce': float_coercer,
        'required': True
    },
    'std': {
        'type': 'float',
        'coerce': float_coercer,
        'required': True
    }
})

LOCI = create_biomarker_schema({
    'mutation_id': {
        'type': 'string',
        'required': True
    },
    'sample_id': {
        'type': 'string',
        'required': True
    },
    'cluster_id': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'cellular_prevalence': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'cellular_prevalence_std': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    },
    'variant_allele_frequency': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer
    }
})

PYCLONE = create_biomarker_schema({
    'mutation_id': {
        'type': 'string',
        'required': True
    },
    'ref_counts': {
        'type': 'float',
        'coerce': float_coercer,
        'required': True,
    },
    'var_counts': {
        'type': 'float',
        'coerce': float_coercer,
        'required': True,
    },
    'normal_cn': {
        'type': 'float',
        'coerce': float_coercer,
        'required': True,
    },
    'minor_cn': {
        'type': 'float',
        'coerce': float_coercer,
        'required': True,
    },
    'major_cn': {
        'type': 'float',
        'coerce': float_coercer,
        'required': True,
    },
    'variant_case': {
        'type': 'string',
        'required': True,
    },
    'variant_freq': {
        'type': 'float',
        'required': True,
        'coerce': float_coercer,
    },
    'genotype': {
        'type': 'string',
        'required': True,
    }
})