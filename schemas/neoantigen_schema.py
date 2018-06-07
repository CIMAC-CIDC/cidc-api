"""
Schema for neoantigen prediction files.
"""
from schemas import int_coercer, float_coercer, create_biomarker_schema


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
        'type': 'integer',
        'nullable': True,
        'coerce': int_coercer
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
        'type': 'integer',
        'nullable': True,
        'coerce': int_coercer
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
        'type': 'integer',
        'nullable': True,
        'coerce': int_coercer
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
        'type': 'integer',
        'nullable': True,
        'coerce': int_coercer
    },
    'hydrophilicCount': {
        'type': 'integer',
        'nullable': True,
        'coerce': int_coercer
    },
    'positive': {
        'type': 'integer',
        'nullable': True,
        'coerce': int_coercer
    },
    'negative': {
        'type': 'integer',
        'nullable': True,
        'coerce': int_coercer
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
        'type': 'integer',
        'nullable': True,
        'coerce': int_coercer
    },
    'cysCount': {
        'type': 'integer',
        'nullable': True,
        'coerce': int_coercer
    },
    'glnStatus': {
        'type': 'integer',
        'nullable': True,
        'coerce': int_coercer
    },
    'apCount': {
        'type': 'integer',
        'nullable': True,
        'coerce': int_coercer
    },
    'glyStatus': {
        'type': 'integer',
        'nullable': True,
        'coerce': int_coercer
    },
    'oncogeneStatus': {
        'type': 'integer',
        'nullable': True,
        'coerce': int_coercer
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
        'type': 'integer',
        'nullable': True,
        'coerce': int_coercer
    }
})
