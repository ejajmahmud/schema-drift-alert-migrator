"""Core Schema Drift Migrator implementation."""
from typing import Dict, List, Any

class SchemaDriftReport:
    def __init__(self, added_fields: List[str], removed_fields: List[str], modified_types: List[str], ddl_statements: List[str]):
        self.added_fields = added_fields
        self.removed_fields = removed_fields
        self.modified_types = modified_types
        self.ddl_statements = ddl_statements
        self.has_drift = bool(added_fields or removed_fields or modified_types)

class DriftMigrator:
    @classmethod
    def compare_schemas(cls, table_name: str, live_schema: Dict[str, str], contract_schema: Dict[str, str]) -> SchemaDriftReport:
        added = []
        removed = []
        modified = []
        ddl = []

        # Check for added fields in contract that live lacks
        for col, col_type in contract_schema.items():
            if col not in live_schema:
                added.append(col)
                ddl.append(f"ALTER TABLE {table_name} ADD COLUMN {col} {col_type.upper()};")
            elif live_schema[col].lower() != col_type.lower():
                modified.append(f"{col}: {live_schema[col]} -> {col_type}")
                ddl.append(f"ALTER TABLE {table_name} ALTER COLUMN {col} TYPE {col_type.upper()};")

        # Check for removed fields
        for col in live_schema:
            if col not in contract_schema:
                removed.append(col)
                # Warning: guarded drop
                ddl.append(f"-- WARNING: ALTER TABLE {table_name} DROP COLUMN {col};")

        return SchemaDriftReport(added, removed, modified, ddl)
