from dagster_dbt import DbtCliResource, dbt_assets

from dagster import AssetExecutionContext
from sparkling.resources.dbt import DBT_MANIFEST_PATH, SparklingDbtTranslator


@dbt_assets(
    manifest=DBT_MANIFEST_PATH,
    dagster_dbt_translator=SparklingDbtTranslator(),
)
def sparkling_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
