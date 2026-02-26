from dagster_dbt import DbtCliResource

from .spark_resource import spark_conn

# dbt Resource
dbt_resource = DbtCliResource(
    project_dir="/app/dbt",
    profiles_dir="/app/dbt",
)

__all__ = ["dbt_resource", "spark_conn"]
