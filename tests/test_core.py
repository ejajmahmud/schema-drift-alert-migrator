"""Tests for DriftMigrator."""
import unittest
from schema_drift_alert_migrator.core import DriftMigrator

class TestDriftMigrator(unittest.TestCase):
    def test_drift_detection(self):
        live = {"id": "int", "title": "text"}
        contract = {"id": "int", "title": "text", "created_at": "timestamp"}

        rep = DriftMigrator.compare_schemas("articles", live, contract)
        self.assertTrue(rep.has_drift)
        self.assertIn("created_at", rep.added_fields)
        self.assertTrue(any("ADD COLUMN created_at" in s for s in rep.ddl_statements))
