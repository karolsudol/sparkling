from dagster_dbt import DbtCliResource

# dbt Resource
dbt_resource = DbtCliResource(
    project_dir="/app/dbt",
    profiles_dir="/app/dbt",
)
