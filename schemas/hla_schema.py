"""
Cerberus rules for HLA Types
"""
from schemas.tools import create_biomarker_schema

HAPLOTYPE = {
    'allele_group': {
        'type': 'integer',
    },
    'hla_allele': {
        'type': 'integer',
    },
    'synonymous_mutation': {
        'type': 'integer',
    },
    'non_coding_mutation': {
        'type': 'integer'
    },
    'suffix': {
        'type': 'string',
    }
}

HLA = create_biomarker_schema({
    'gene_name': {
        'type': 'string',
        'required': True,
    },
    'haplotypes': {
        'type': 'list',
        'schema': HAPLOTYPE
    },
})
