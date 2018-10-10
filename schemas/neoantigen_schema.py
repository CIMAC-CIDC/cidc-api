"""
Schema for neoantigen prediction files.
"""
from schemas.coercers import FLOAT_COERCER as float_coercer
from schemas.tools import create_biomarker_schema


NEOANTIGEN = create_biomarker_schema({
    'sample': {
        'type': 'string'
    },
    'transcript': {
        'type': 'string'
    },
    'gene': {
        'type': 'string'
    },
    'gene_number': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'cdna_change': {
        'type': 'string'
    },
    'protein_change': {
        'type': 'string'
    },
    'neoORF_status': {
        'type': 'string'
    },
    'peptide_length': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'hla': {
        'type': 'string'
    },
    'peptide_mut': {
        'type': 'string'
    },
    'affinity_mut': {
        'type': 'string'
    },
    'peptide_wit': {
        'type': 'string'
    },
    'affinity_wt': {
        'type': 'string'
    },
    'rank_mut': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'rank_wt': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'strong_binder_threshold': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'weak_binder_threshold': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'nearest_neighbor': {
        'type': 'string'
    },
    'score': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'rank': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'ratio': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'long': {
        'type': 'string'
    },
    'flank': {
        'type': 'string'
    },
    'hydrophobicCount': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'hydrophilicCount': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'positive': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'negative': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'hydrophobicFraction': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'hydrophilicFraction': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'charge': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'cysCount': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'glnStatus': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'apCount': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'glyStatus': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'oncogeneStatus': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'pos20': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'ell_score_mut': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'ell_rank_mut': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'ell_score_wt': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'ell_rank_wt': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    },
    'core_ba': {
        'type': 'string'
    },
    'iCore_ba': {
        'type': 'string'
    },
    'core_ell': {
        'type': 'string'
    },
    'iCore_ell': {
        'type': 'string'
    },
    'core_equal': {
        'type': 'float',
        'nullable': True,
        'coerce': float_coercer
    }
})
