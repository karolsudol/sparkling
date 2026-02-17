# Stage 2: Create Spark with Comet image
FROM docker.io/spark:4.0.1-scala2.13-java21-python3-ubuntu

# Download the Comet JAR from Maven Central
RUN apt-get update && apt-get install -y wget && \
    wget https://repo1.maven.org/maven2/org/apache/datafusion/comet-spark-spark4.0_2.13/0.11.0/comet-spark-spark4.0_2.13-0.11.0.jar -P /opt/spark/jars/
