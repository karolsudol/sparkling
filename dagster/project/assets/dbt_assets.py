import os
import subprocess
from pathlib import Path

from dagster_dbt import DagsterDbtTranslator, DbtCliResource, dbt_assets

from dagster import AssetExecutionContext

DBT_PROJECT_DIR = "/app/dbt"
DBT_MANIFEST_PATH = Path(DBT_PROJECT_DIR) / "target" / "manifest.json"

# Generate manifest if it doesn't exist
if not DBT_MANIFEST_PATH.exists():
    os.makedirs(DBT_MANIFEST_PATH.parent, exist_ok=True)
    subprocess.run(["dbt", "parse"], cwd=DBT_PROJECT_DIR, check=True)


# We use a custom translator to ensure the asset keys match our Iceberg catalog
class SparklingDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props):
        # Maps dbt models to Dagster asset keys: spark_catalog.<schema>.<model>
        schema = dbt_resource_props.get("schema")
        name = dbt_resource_props.get("name")
        return ["spark_catalog", schema, name]


@dbt_assets(manifest=DBT_MANIFEST_PATH, dagster_dbt_translator=SparklingDbtTranslator())
def sparkling_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).get_artifacts()
