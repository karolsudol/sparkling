from pyspark.sql import SparkSession

from dagster import ConfigurableResource

from ..config import SPARK_REMOTE


class SparkConnectResource(ConfigurableResource):
    remote_url: str

    def get_session(self, app_name: str) -> SparkSession:
        return (
            SparkSession.builder.appName(app_name).remote(self.remote_url).getOrCreate()
        )


spark_conn = SparkConnectResource(remote_url=SPARK_REMOTE)
