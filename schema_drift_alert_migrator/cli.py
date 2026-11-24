"""CLI for Schema Drift Migrator."""
import argparse
from .core import DriftMigrator

def main():
    parser = argparse.ArgumentParser(description="Schema Drift Alert Migrator CLI")
    parser.add_argument("--demo", action="store_true", help="Run schema drift demo")
    args = parser.parse_args()

    live = {"id": "int", "name": "varchar"}
    contract = {"id": "int", "name": "varchar", "email": "varchar(255)"}

    report = DriftMigrator.compare_schemas("users", live, contract)
    print(f"Drift detected: {report.has_drift}")
    print("DDL Migration Statements:")
    for stmt in report.ddl_statements:
        print(" ", stmt)

if __name__ == "__main__":
    main()
