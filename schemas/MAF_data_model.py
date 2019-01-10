#!/usr/bin/env python3
"""
Validator for MAF data.
"""

from schemas.coercers import FLOAT_COERCER as float_coercer


MAF = {
    'trial': {
        'required': True,
        'type': 'string',
    },
    'assay': {
        'required': True,
        'type': 'string',
    },
    'record_id': {
        'required': True,
        'type': 'string'
    },
    "NCBI_Build": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "ExAC_AF_EAS": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Verification_Status": {
        "required": True,
        "type": "string",
        "nullable": True
    },
    "SYMBOL": {
        "type": "string",
        "nullable": True
    },
    "UNIPARC": {
        "type": "string",
        "nullable": True
    },
    "n_ref_count": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "DOMAINS": {
        "type": "string",
        "nullable": True
    },
    "CLIN_SIG": {
        "type": "string",
        "nullable": True
    },
    "Start_Position": {
        "required": True,
        "type": "float",
        "coerce": float_coercer,
        "empty": False
    },
    "Variant_Classification": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "CDS_position": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "variant_id": {
        "type": "string",
        "nullable": True
    },
    "RefSeq": {
        "type": "string",
        "nullable": True
    },
    "Existing_variation": {
        "type": "string",
        "nullable": True
    },
    "AA_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "HGVSp_Short": {
        "type": "string",
        "nullable": True
    },
    "MOTIF_SCORE_CHANGE": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "variant_qual": {
        "type": "string",
        "nullable": True
    },
    "Gene": {
        "type": "string",
        "nullable": True
    },
    "ENSP": {
        "type": "string",
        "nullable": True
    },
    "ExAC_AC_AN_Adj": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "gnomAD_OTH_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "PolyPhen": {
        "type": "string",
        "nullable": True
    },
    "Reference_Allele": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "Transcript_ID": {
        "type": "string",
        "nullable": True
    },
    "Entrez_Gene_Id": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "PICK": {
        "type": "string",
        "nullable": True
    },
    "GENE_PHENO": {
        "type": "string",
        "nullable": True
    },
    "gnomAD_AMR_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "ExAC_AF_OTH": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "cDNA_position": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "n_depth": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "all_effects": {
        "type": "string",
        "nullable": True
    },
    "Mutation_Status": {
        "type": "string",
        "empty": True
    },
    "Center": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "ExAC_AF_Adj": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Hugo_Symbol": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "ASN_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "ExAC_FILTER": {
        "type": "string",
        "nullable": True
    },
    "t_depth": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Tumor_Seq_Allele2": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "HGNC_ID": {
        "type": "string",
        "nullable": True
    },
    "SAS_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "HGVS_OFFSET": {
        "type": "string",
        "nullable": True
    },
    "ExAC_AF_AFR": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Validation_Method": {
        "type": "string",
        "empty": True
    },
    "ExAC_AC_AN": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Tumor_Seq_Allele1": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "ExAC_AC_AN_SAS": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Protein_position": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "ExAC_AC_AN_EAS": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "ExAC_AC_AN_AMR": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "EA_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "gnomAD_FIN_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Sequencing_Phase": {
        "required": True,
        "type": "string",
        "nullable": True
    },
    "TREMBL": {
        "type": "string",
        "nullable": True
    },
    "SYMBOL_SOURCE": {
        "type": "string",
        "nullable": True
    },
    "Amino_acids": {
        "type": "string",
        "nullable": True
    },
    "Tumor_Sample_Barcode": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "AMR_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "STRAND_VEP": {
        "type": "string",
        "nullable": True
    },
    "ExAC_AC_AN_AFR": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Tumor_Validation_Allele1": {
        "required": True,
        "type": "string",
        "nullable": True
    },
    "Variant_Type": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "MOTIF_POS": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "BIOTYPE": {
        "type": "string",
        "nullable": True
    },
    "dbSNP_Val_Status": {
        "required": True,
        "type": "string",
        "nullable": True
    },
    "Match_Norm_Validation_Allele2": {
        "required": True,
        "type": "string",
        "nullable": True
    },
    "Match_Norm_Validation_Allele1": {
        "required": True,
        "type": "string",
        "nullable": True
    },
    "ExAC_AC_AN_NFE": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "CANONICAL": {
        "type": "string",
        "nullable": True
    },
    "gnomAD_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "TSL": {
        "type": "string",
        "nullable": True
    },
    "Sequence_Source": {
        "type": "string",
        "nullable": True
    },
    "dbSNP_RS": {
        "required": True,
        "type": "string",
        "nullable": True
    },
    "ExAC_AF_NFE": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "BAM_File": {
        "required": True,
        "type": "string",
        "nullable": True
    },
    "AFR_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Match_Norm_Seq_Allele2": {
        "required": True,
        "type": "string",
        "nullable": True
    },
    "Feature": {
        "type": "string",
        "nullable": True
    },
    "Codons": {
        "type": "string",
        "nullable": True
    },
    "MOTIF_NAME": {
        "type": "string",
        "nullable": True
    },
    "SIFT": {
        "type": "string",
        "nullable": True
    },
    "Score": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True,
    },
    "ExAC_AF_SAS": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "gnomAD_ASJ_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "CCDS": {
        "type": "string",
        "nullable": True
    },
    "Allele": {
        "type": "string",
        "nullable": True
    },
    "ExAC_AC_AN_OTH": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Feature_type": {
        "type": "string",
        "nullable": True
    },
    "IMPACT": {
        "type": "string",
        "nullable": True
    },
    "MINIMISED": {
        "type": "string",
        "nullable": True
    },
    "HGVSp": {
        "type": "string",
        "nullable": True
    },
    "ExAC_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Validation_Status": {
        "required": True,
        "type": "string",
        "nullable": True
    },
    "Matched_Norm_Sample_UUID": {
        "type": "string",
        "empty": True
    },
    "INTRON": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "End_Position": {
        "required": True,
        "type": "float",
        "coerce": float_coercer,
        "nullable": False
    },
    "HGVSc": {
        "type": "string",
        "nullable": True
    },
    "gnomAD_AFR_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Tumor_Validation_Allele2": {
        "required": True,
        "type": "string",
        "nullable": True
    },
    "Matched_Norm_Sample_Barcode": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "Match_Norm_Seq_Allele1": {
        "required": True,
        "type": "string",
        "nullable": True
    },
    "t_alt_count": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "gnomAD_EAS_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Strand": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "ExAC_AF_AMR": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "ALLELE_NUM": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Exon_Number": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "EAS_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Tumor_Sample_UUID": {
        "type": "string",
        "empty": True
    },
    "flanking_bps": {
        "type": "string",
        "nullable": True
    },
    "AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "PHENO": {
        "type": "string",
        "nullable": True
    },
    "PUBMED": {
        "type": "string",
        "nullable": True
    },
    "EXON": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "Consequence": {
        "type": "string",
        "nullable": True
    },
    "HIGH_INF_POS": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "gnomAD_NFE_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "EUR_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "DISTANCE": {
        "type": "string",
        "nullable": True
    },
    "VARIANT_CLASS": {
        "type": "string",
        "nullable": True
    },
    "ExAC_AF_FIN": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "SOMATIC": {
        "type": "string",
        "nullable": True
    },
    "gnomAD_SAS_AF": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "t_ref_count": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "FILTER": {
        "type": "string",
        "nullable": True
    },
    "SWISSPROT": {
        "type": "string",
        "nullable": True
    },
    "ExAC_AC_AN_FIN": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Sequencer": {
        "type": "string",
        "empty": True
    },
    "n_alt_count": {
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Chromosome": {
        "required": True,
        "type": "string",
        "empty": False
    }
}


MAF_PT = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST'],
    "allowed_roles": ["admin", "user", "superuser", "uploader"],
    "allowed_item_roles": ["admin", "user", "superuser", "uploader"],
    'schema': MAF
}