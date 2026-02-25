import os

from dagster_dbt import DbtCliResource
from pyspark.sql import SparkSession

from dagster import ConfigurableResource


class SparkConnectResource(ConfigurableResource):
    remote_url: str

    def get_session(self, app_name: str) -> SparkSession:
        return (
            SparkSession.builder.appName(app_name).remote(self.remote_url).getOrCreate()
        )


# Default to the container name in the spark-network
spark_resource = SparkConnectResource(
    remote_url=os.getenv("SPARK_REMOTE", "sc://spark-connect:15002")
)

# dbt Resource
dbt_resource = DbtCliResource(
    project_dir="/app/dbt",
    profiles_dir="/app/dbt",
)
