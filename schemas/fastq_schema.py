"""
Schema for FASTQ type files.
"""

from schemas.fielder import fielder

FASTQ_SCHEMA = {}
FASTQ_SCHEMA.update(
    [
        fielder("patient_id"),
        fielder("timepoint", d_type="integer"),
        fielder("timepoint_unit"),
        fielder("batch_id"),
        fielder("instrument_model"),
        fielder("read_length", d_type="integer"),
        fielder("avg_insert_size", d_type="integer"),
        fielder("sample_id"),
        fielder("pair_label"),
        fielder("sample_type")
    ]
)
