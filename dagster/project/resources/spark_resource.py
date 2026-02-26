import os

from pyspark.sql import SparkSession

from dagster import ConfigurableResource


class SparkConnectResource(ConfigurableResource):
    remote_url: str

    def get_session(self, app_name: str) -> SparkSession:
        return (
            SparkSession.builder.appName(app_name).remote(self.remote_url).getOrCreate()
        )


spark_conn = SparkConnectResource(
    remote_url=os.getenv("SPARK_REMOTE", "sc://spark-connect:15002")
)
