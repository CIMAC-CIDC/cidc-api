#!/usr/bin/env python3
"""
Module that stores the record validators for eve.
"""
from schemas.coercers import FLOAT_COERCER as float_coercer, INT_COERCER as int_coercer
from schemas.analysis import ANALYSIS, ANALYSIS_STATUS
from schemas.assays import ASSAYS
from schemas.trials import TRIALS
from schemas.ingestion import INGESTION
from schemas.data import DATA, DATA_AGG_INPUTS
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


def create_biomarker_schema(schema: dict) -> dict:
    """
    Factory method for creating a schema object.

    Arguments:
        schema {dict} -- Cerberus schema dictionary.

    Returns:
        dict -- EVE endpoint definition.
    """
    base_dict = {
        "public_methods": [],
        "resource_methods": ["GET", "POST"],
        "allowed_roles": ["user", "admin"],
        "schema": {
            "trial": {"type": "string", "required": True},
            "assay": {"type": "string", "required": True},
            "record_id": {"type": "string", "required": True},
        },
    }
    base_dict["schema"].update(schema)
    return base_dict
