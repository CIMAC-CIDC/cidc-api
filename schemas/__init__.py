"""
Module that stores the record validators for eve.
"""
from schemas.coercers import FLOAT_COERCER as float_coercer, INT_COERCER as int_coercer
from schemas.analysis import ANALYSIS, ANALYSIS_STATUS
from schemas.assays import ASSAYS
from schemas.trials import TRIALS
from schemas.ingestion import INGESTION
from schemas.data import DATA, DATA_AGG_INPUTS, DATA_EDIT, DATA_TOGGLE_VIS
from schemas.MAF_data_model import MAF_PT
from schemas.hla_schema import HLA
from schemas.clinical_data_schema import CLINICAL_1021
from schemas.user_schema import DB_USER, DB_ACCOUNTS_INFO, DB_ACCOUNTS_CREATE
from schemas.olink_schema import OLINK
from schemas.metadata_schema import BIOREPOSITORY
from schemas.hugo_schema import IDENTIFIER_SCHEMA
from schemas.fastq_schema import FASTQ_SCHEMA
from schemas.last_access import LAST_ACCESS
