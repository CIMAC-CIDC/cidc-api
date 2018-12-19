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
        "required": False,
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
        "required": False,
        "type": "string",
        "nullable": True
    },
    "UNIPARC": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "n_ref_count": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "DOMAINS": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "CLIN_SIG": {
        "required": False,
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
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "variant_id": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "RefSeq": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "Existing_variation": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "AA_AF": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "HGVSp_Short": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "MOTIF_SCORE_CHANGE": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "variant_qual": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "Gene": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "ENSP": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "ExAC_AC_AN_Adj": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "gnomAD_OTH_AF": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "PolyPhen": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "Reference_Allele": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "Transcript_ID": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "Entrez_Gene_Id": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "PICK": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "GENE_PHENO": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "gnomAD_AMR_AF": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "ExAC_AF_OTH": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "cDNA_position": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "n_depth": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "all_effects": {
        "required": False,
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
        "required": False,
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
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "ExAC_FILTER": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "t_depth": {
        "required": False,
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
        "required": False,
        "type": "string",
        "nullable": True
    },
    "SAS_AF": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "HGVS_OFFSET": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "ExAC_AF_AFR": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Validation_Method": {
        "type": "string",
        "empty": True
    },
    "ExAC_AC_AN": {
        "required": False,
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
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Protein_position": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "ExAC_AC_AN_EAS": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "ExAC_AC_AN_AMR": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "EA_AF": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "gnomAD_FIN_AF": {
        "required": False,
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
        "required": False,
        "type": "string",
        "nullable": True
    },
    "SYMBOL_SOURCE": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "Amino_acids": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "Tumor_Sample_Barcode": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "AMR_AF": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "STRAND_VEP": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "ExAC_AC_AN_AFR": {
        "required": False,
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
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "BIOTYPE": {
        "required": False,
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
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "CANONICAL": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "gnomAD_AF": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "TSL": {
        "required": False,
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
        "required": False,
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
        "required": False,
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
        "required": False,
        "type": "string",
        "nullable": True
    },
    "Codons": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "MOTIF_NAME": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "SIFT": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "Score": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True,
    },
    "ExAC_AF_SAS": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "gnomAD_ASJ_AF": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "CCDS": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "Allele": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "ExAC_AC_AN_OTH": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Feature_type": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "IMPACT": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "MINIMISED": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "HGVSp": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "ExAC_AF": {
        "required": False,
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
        "required": False,
        "type": "string",
        "nullable": True
    },
    "gnomAD_AFR_AF": {
        "required": False,
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
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "gnomAD_EAS_AF": {
        "required": False,
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
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "ALLELE_NUM": {
        "required": False,
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
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Tumor_Sample_UUID": {
        "type": "string",
        "empty": True
    },
    "flanking_bps": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "AF": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "PHENO": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "PUBMED": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "EXON": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "Consequence": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "HIGH_INF_POS": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "gnomAD_NFE_AF": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "EUR_AF": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "DISTANCE": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "VARIANT_CLASS": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "ExAC_AF_FIN": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "SOMATIC": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "gnomAD_SAS_AF": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "t_ref_count": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "FILTER": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "SWISSPROT": {
        "required": False,
        "type": "string",
        "nullable": True
    },
    "ExAC_AC_AN_FIN": {
        "required": False,
        "type": "float",
        "coerce": float_coercer,
        "nullable": True
    },
    "Sequencer": {
        "type": "string",
        "empty": True
    },
    "n_alt_count": {
        "required": False,
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