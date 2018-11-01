"""[summary]
"""

CLINICAL_1021 = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST'],
    'allowed_roles': ['user', 'admin'],
    'schema': {
        'trial': {
            'type': 'string',
            'required': True
        },
        'assay': {
            'type': 'string',
            'required': True
        },
        'record_id': {
            'type': 'string',
            'required': True
        },
        "HEIGHT_AT_REG": {
            "required": True,
            "type": "float",
            "empty": True
        },
        "OS_STATUS": {
            "required": True,
            "type": "string",
            "empty": False,
            "allowed": [
                "LIVING",
                "DECEASED"
            ]
        },
        "OFF_STUDY_DT_RAW_ABS": {
            "required": False,
            "type": "integer",
            "empty": True
        },
        "PATIENT_ID": {
            "required": True,
            "type": "string",
            "empty": False
        },
        "DEATH_DT_RAW_ABS": {
            "required": False,
            "type": "integer",
            "empty": True
        },
        "GENDER": {
            "required": True,
            "type": "string",
            "empty": False,
            "allowed": [
                "Male",
                "Female"
            ]
        },
        "DZ_STG_CD": {
            "required": False,
            "type": "string",
            "empty": True
        },
        "OFF_TX_OTH_RSN": {
            "required": False,
            "type": "string",
            "empty": True
        },
        "MEDDRA_CODE_RAW": {
            "required": True,
            "type": "integer",
            "empty": True
        },
        "DEATH_CAUS_CD": {
            "required": False,
            "type": "string",
            "empty": True
        },
        "CRSE_START_DT_1_RAW_ABS": {
            "required": False,
            "type": "integer",
            "empty": True
        },
        "PRIM_SITE_DZ_NM": {
            "required": False,
            "type": "string",
            "empty": False
        },
        "HIST_CYTPATH_DESC": {
            "required": False,
            "type": "string",
            "empty": True
        },
        "BEST_RESPS_ASSMNT_TP_2": {
            "required": False,
            "type": "string",
            "empty": True
        },
        "RACE_CD_2": {
            "required": False,
            "type": "string",
            "empty": True
        },
        "RACE_CD_1": {
            "required": True,
            "type": "string",
            "empty": True
        },
        "ETHNICITY": {
            "required": True,
            "type": "string",
            "empty": False
        },
        "AGE_AT_REG": {
            "required": True,
            "type": "float",
            "empty": False,
        },
        "PROGRESSION_DT_2_RAW_ABS": {
            "required": False,
            "type": "integer",
            "empty": True
        },
        "PER_BIR_DT_RAW_ABS": {
            "required": True,
            "type": "integer",
            "empty": False
        },
        "OS_MONTHS": {
            "required": True,
            "type": "integer",
            "empty": True
        },
        "NEO_HIST_GD": {
            "required": False,
            "type": "string",
            "empty": True
        },
        "TX_PHASE_END_DT_RAW_ABS": {
            "required": False,
            "type": "integer",
            "empty": True
        },
        "ENROLL_TX_ASSIGN_CD_STD": {
            "required": False,
            "type": "string",
            "empty": True
        },
        "ENROLL_TX_ASSIGN_CD": {
            "required": False,
            "type": "string",
            "empty": True
        },
        "ECOG_K_PERF_STAT_SC": {
            "required": False,
            "type": "string",
            "empty": True
        },
        "project": {
            "required": True,
            "type": "string",
            "empty": False
        },
        "WEIGHT_AT_REG": {
            "required": True,
            "type": "float",
            "empty": True
        },
        "BSA_AT_REG": {
            "required": True,
            "type": "float",
            "empty": True
        },
        "PT_OFF_TX_OFF_ST_RSN_CD": {
            "required": False,
            "type": "string",
            "empty": True
        }
    }
}
