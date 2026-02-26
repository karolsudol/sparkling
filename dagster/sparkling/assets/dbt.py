from dagster_dbt import DbtCliResource, dbt_assets

from dagster import AssetExecutionContext, AssetMaterialization, MetadataValue
from sparkling.resources.dbt import DBT_MANIFEST_PATH, SparklingDbtTranslator
from sparkling.resources.spark import SparkConnectResource


@dbt_assets(
    manifest=DBT_MANIFEST_PATH,
    dagster_dbt_translator=SparklingDbtTranslator(),
)
def sparkling_dbt_assets(
    context: AssetExecutionContext, dbt: DbtCliResource, spark: SparkConnectResource
):
    # 1. Run dbt and stream the results
    dbt_run = dbt.cli(["build"], context=context)

    for event in dbt_run.stream():
        # Correct way to identify and augment materialization events
        if isinstance(event, AssetMaterialization):
            # The asset_key is available directly on the event
            # Path is [catalog, schema, table]
            table_path = ".".join(event.asset_key.path)

            try:
                session = spark.get_session("DagsterDbtMetadataGatherer")
                row_count = session.table(table_path).count()

                # Add metadata to the existing event
                event = event._replace(
                    metadata={
                        **event.metadata,
                        "row_count": MetadataValue.int(row_count),
                    }
                )
            except Exception as e:
                context.log.warning(f"Could not fetch row count for {table_path}: {e}")

        yield event
