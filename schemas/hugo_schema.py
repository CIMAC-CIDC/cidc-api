"""
Schema for hugo gene symbols for the purpose of validation:
"""
from schemas.fielder import fielder

HUGO_SCHEMA = {}
HUGO_SCHEMA.update(
    [
        fielder("#tax_id", d_type="integer", required=True),
        fielder("GeneID", d_type="integer", required=True),
        fielder("symbol", required=True),
        fielder("LocusTag"),
        fielder("Synonyms", d_type="list", subschema="string"),
        fielder("dbXrefs", d_type="list", subschema="string"),
        fielder("chromosome", d_type="integer", required=True),
        fielder("map_location", required=True),
        fielder("description"),
        fielder("type_of_gene", required=True),
        fielder("Symbol_from_nomenclature_authority", required=True),
        fielder("Full_name_from_nomenclature_authority", required=True),
        fielder("Nomenclature_status", d_type="integer", required=True),
        fielder("Other_designation", d_type="list", subschema="string"),
        fielder("Modification_date", d_type="integer", required=True),
        fielder("Feature_type"),
    ]
)

IDENTIFIER_SCHEMA = {
    "public_methods": [],
    "public_item_methods": [],
    "resource_methods": ["GET", "POST", "DELETE"],
    "item_methods": ["GET", "DELETE"],
    "allowed_roles": ["admin"],
    "allowed_item_roles": ["admin"],
    "id_field": "symbol",
    "mongo_indexes": {"symbol": ([("symbol", 1)], {"unique": True})},
    "schema": {},
}
IDENTIFIER_SCHEMA["schema"].update([fielder("symbol", required=True)])
