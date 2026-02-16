# Stage 1: Build Comet
FROM maven:3.8.4-openjdk-11 AS builder

# Install git
USER root
RUN apt-get update && apt-get install -y git

# Clone Comet repository
RUN git clone https://github.com/apache/arrow-datafusion-comet.git /comet
WORKDIR /comet

# Checkout a version compatible with Spark 3.5.0
RUN git checkout tags/apache-arrow-comet-0.4.0

# Build Comet
RUN ./build/mvn clean package -DskipTests -pl spark -am

# Stage 2: Create Spark with Comet image
FROM bitnami/spark:3.5.0

# Copy the Comet JAR
COPY --from=builder /comet/spark/target/comet-spark-spark3.5_2.12-0.4.0.jar /opt/bitnami/spark/jars/
