"""
Schema for shipping manifests
"""
from schemas.fielder import fielder
from schemas.validation_error_schema import VALIDATION_ERROR
from schemas.tools import create_biomarker_schema


SAMPLESCHEMA = {}
SAMPLESCHEMA.update(
    [
        fielder("pathology_report", required=True),
        fielder("time_point", required=True),
        fielder("specimen_type", required=True),
        fielder("specimen_format", required=True),
        fielder("collection_date", required=True),
        fielder("processing_date"),
        fielder("quantity", d_type="integer"),
        fielder("volume", d_type="float"),
        fielder("units"),
        fielder("sample_source"),
        fielder("comments", nullable=True),
    ]
)
OLINK_META = {}
OLINK_META.update(
    [
        fielder("manifest_id", nullable=True),
        fielder("protocol_id", nullable=True),
        fielder("request", nullable=True),
        fielder("assay_priority", nullable=True),
        fielder("assay_type", nullable=True),
        fielder("batch_number", nullable=True),
        fielder("courier", nullable=True),
        fielder("tracking_number", d_type="integer", nullable=True),
        fielder("shipping_condition", nullable=True),
        fielder("date_shipped", nullable=True),
        fielder("number_shipped", nullable=True),
        fielder("account_number", nullable=True),
        fielder("sender_name", nullable=True),
        fielder("sender_address", nullable=True),
        fielder("sender_email", nullable=True),
        fielder("receiver_name", nullable=True),
        fielder("receiver_address", nullable=True),
        fielder("receiver_email", nullable=True),
        fielder("samples", d_type="list", subschema=SAMPLESCHEMA),
        fielder(
            "validation_errors",
            d_type="list",
            subschema=VALIDATION_ERROR,
            required=True,
        ),
    ]
)

BIOREPOSITORY = create_biomarker_schema(OLINK_META)
