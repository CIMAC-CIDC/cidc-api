#!/usr/bin/env python3
"""
Module that stores the record validators for eve.
"""
from schemas.coercers import FLOAT_COERCER as float_coercer, INT_COERCER as int_coercer
from schemas.analysis import ANALYSIS, ANALYSIS_STATUS
from schemas.assays import ASSAYS
from schemas.trials import TRIALS
from schemas.ingestion import INGESTION
from schemas.data import DATA, DATA_AGG_INPUTS, DATA_EDIT
from schemas.MAF_data_model import MAF_PT
from schemas.hla_schema import HLA
from schemas.neoantigen_schema import NEOANTIGEN
from schemas.tumor_purity_ploidy_schema import PURITY, CONFINTS_CP
from schemas.clonality_schema import CLONALITY_CLUSTER, LOCI, PYCLONE
from schemas.cnv_schema import CNV
from schemas.clinical_data_schema import CLINICAL_1021
from schemas.rsem_schema import RSEM_EXPRESSION, RSEM_ISOFORMS
from schemas.user_schema import DB_USER, DB_ACCOUNTS_INFO, DB_ACCOUNTS_UPDATE
from schemas.olink_schema import OLINK
from schemas.metadata_schema import BIOREPOSITORY
