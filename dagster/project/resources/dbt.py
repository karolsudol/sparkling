from dagster_dbt import DbtCliResource

from ..config import DBT_PROFILES_DIR, DBT_PROJECT_DIR

dbt_resource = DbtCliResource(
    project_dir=DBT_PROJECT_DIR,
    profiles_dir=DBT_PROFILES_DIR,
)
