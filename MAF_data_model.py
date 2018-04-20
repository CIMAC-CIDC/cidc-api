#!/usr/bin/env python3
"""
Validator for MAF data.
"""

MAF = {
    'trial_id': {
        'required': True,
        'type': 'string',
    },
    'assay_id': {
        'required': True,
        'type': 'string',
    },
    'record_id': {
        'required': True,
        'type': 'string'
    },
    "Clinical_ID": {
        "required": True,
        "type": "object",
        "empty": False
    },
    "NCBI_Build": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "ExAC_AF_EAS": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "Verification_Status": {
        "required": True,
        "type": "string",
        "empty": True
    },
    "SYMBOL": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "UNIPARC": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "n_ref_count": {
        "required": False,
        "type": "integer",
        "empty": True
    },
    "DOMAINS": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "CLIN_SIG": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "Start_Position": {
        "required": True,
        "type": "integer",
        "empty": False
    },
    "Variant_Classification": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "CDS_position": {
        "required": False,
        "type": "integer",
        "empty": True
    },
    "variant_id": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "RefSeq": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "Existing_variation": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "AA_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "HGVSp_Short": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "MOTIF_SCORE_CHANGE": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "variant_qual": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "Gene": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "ENSP": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "ExAC_AC_AN_Adj": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "gnomAD_OTH_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "PolyPhen": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "Reference_Allele": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "Transcript_ID": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "Entrez_Gene_Id": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "PICK": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "GENE_PHENO": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "gnomAD_AMR_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "ExAC_AF_OTH": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "cDNA_position": {
        "required": False,
        "type": "integer",
        "empty": True
    },
    "n_depth": {
        "required": False,
        "type": "integer",
        "empty": True
    },
    "all_effects": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "Mutation_Status": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "Center": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "ExAC_AF_Adj": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "Hugo_Symbol": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "ASN_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "ExAC_FILTER": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "t_depth": {
        "required": False,
        "type": "integer",
        "empty": True
    },
    "Tumor_Seq_Allele2": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "HGNC_ID": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "SAS_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "HGVS_OFFSET": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "ExAC_AF_AFR": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "Validation_Method": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "ExAC_AC_AN": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "Tumor_Seq_Allele1": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "ExAC_AC_AN_SAS": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "Protein_position": {
        "required": False,
        "type": "integer",
        "empty": True
    },
    "ExAC_AC_AN_EAS": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "ExAC_AC_AN_AMR": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "EA_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "gnomAD_FIN_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "Sequencing_Phase": {
        "required": True,
        "type": "string",
        "empty": True
    },
    "TREMBL": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "SYMBOL_SOURCE": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "Amino_acids": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "Tumor_Sample_Barcode": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "AMR_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "STRAND_VEP": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "ExAC_AC_AN_AFR": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "Tumor_Validation_Allele1": {
        "required": True,
        "type": "string",
        "empty": True
    },
    "Variant_Type": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "MOTIF_POS": {
        "required": False,
        "type": "integer",
        "empty": True
    },
    "BIOTYPE": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "dbSNP_Val_Status": {
        "required": True,
        "type": "string",
        "empty": True
    },
    "Match_Norm_Validation_Allele2": {
        "required": True,
        "type": "string",
        "empty": True
    },
    "Match_Norm_Validation_Allele1": {
        "required": True,
        "type": "string",
        "empty": True
    },
    "ExAC_AC_AN_NFE": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "CANONICAL": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "gnomAD_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "TSL": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "Sequence_Source": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "dbSNP_RS": {
        "required": True,
        "type": "string",
        "empty": True
    },
    "ExAC_AF_NFE": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "BAM_File": {
        "required": True,
        "type": "string",
        "empty": True
    },
    "AFR_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "Match_Norm_Seq_Allele2": {
        "required": True,
        "type": "string",
        "empty": True
    },
    "Feature": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "Codons": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "MOTIF_NAME": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "SIFT": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "Score": {
        "required": True,
        "type": "float",
        "empty": True
    },
    "ExAC_AF_SAS": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "gnomAD_ASJ_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "CCDS": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "Allele": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "ExAC_AC_AN_OTH": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "Feature_type": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "IMPACT": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "MINIMISED": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "HGVSp": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "ExAC_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "Validation_Status": {
        "required": True,
        "type": "string",
        "empty": True
    },
    "Matched_Norm_Sample_UUID": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "INTRON": {
        "required": False,
        "type": "integer",
        "empty": True
    },
    "End_Position": {
        "required": True,
        "type": "integer",
        "empty": False
    },
    "HGVSc": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "gnomAD_AFR_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "Tumor_Validation_Allele2": {
        "required": True,
        "type": "string",
        "empty": True
    },
    "Matched_Norm_Sample_Barcode": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "Match_Norm_Seq_Allele1": {
        "required": True,
        "type": "string",
        "empty": True
    },
    "t_alt_count": {
        "required": False,
        "type": "integer",
        "empty": True
    },
    "gnomAD_EAS_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "Strand": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "ExAC_AF_AMR": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "ALLELE_NUM": {
        "required": False,
        "type": "integer",
        "empty": True
    },
    "Exon_Number": {
        "required": False,
        "type": "integer",
        "empty": True
    },
    "EAS_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "Tumor_Sample_UUID": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "flanking_bps": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "PHENO": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "PUBMED": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "EXON": {
        "required": False,
        "type": "integer",
        "empty": True
    },
    "Consequence": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "HIGH_INF_POS": {
        "required": False,
        "type": "integer",
        "empty": True
    },
    "gnomAD_NFE_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "EUR_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "DISTANCE": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "VARIANT_CLASS": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "ExAC_AF_FIN": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "SOMATIC": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "gnomAD_SAS_AF": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "t_ref_count": {
        "required": False,
        "type": "integer",
        "empty": True
    },
    "FILTER": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "SWISSPROT": {
        "required": False,
        "type": "string",
        "empty": True
    },
    "ExAC_AC_AN_FIN": {
        "required": False,
        "type": "float",
        "empty": True
    },
    "Sequencer": {
        "required": True,
        "type": "string",
        "empty": False
    },
    "n_alt_count": {
        "required": False,
        "type": "integer",
        "empty": True
    },
    "Chromosome": {
        "required": True,
        "type": "string",
        "empty": False
    }
}
