import os
import subprocess
from pathlib import Path

from dagster_dbt import DagsterDbtTranslator, DbtCliResource

from sparkling.config import DBT_PROFILES_DIR, DBT_PROJECT_DIR, ICEBERG_CATALOG

DBT_MANIFEST_PATH = Path(DBT_PROJECT_DIR) / "target" / "manifest.json"


# Implementation details hidden in resource layer
class SparklingDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props):
        resource_type = dbt_resource_props.get("resource_type")
        name = dbt_resource_props.get("name")

        if resource_type == "source":
            return [ICEBERG_CATALOG, dbt_resource_props.get("source_name"), name]

        return [ICEBERG_CATALOG, dbt_resource_props.get("schema"), name]

    def get_group_name(self, dbt_resource_props):
        # Dagster group names must be [A-Za-z0-9_]+
        resource_type = dbt_resource_props.get("resource_type")
        if resource_type == "source":
            return "transactions_sources"

        schema = dbt_resource_props.get("schema")
        return f"transactions_{schema}"

    def get_tags(self, dbt_resource_props):
        return {"pipeline": "transactions", "compute_kind": "dbt"}


# Try to ensure manifest exists (only if writable)
if not DBT_MANIFEST_PATH.exists() and os.access(DBT_PROJECT_DIR, os.W_OK):
    try:
        subprocess.run(
            ["dbt", "parse"], cwd=DBT_PROJECT_DIR, check=True, capture_output=True
        )
    except Exception:
        pass

dbt_resource = DbtCliResource(
    project_dir=DBT_PROJECT_DIR,
    profiles_dir=DBT_PROFILES_DIR,
)
