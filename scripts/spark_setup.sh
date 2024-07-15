#!/bin/bash

# Set JAVA_HOME if necessary
export JAVA_HOME=/usr/lib/jvm/temurin-11-jdk-amd64
# Set SPARK_HOME if necessary
export SPARK_HOME=/usr/lib/spark

# Fetch PySpark file from GitHub
echo "Fetching PySpark file from GitHub..."
git clone echo https://github.com/ilhamaulanap/streamcommerce.
cd streamcommerce/spark_streaming

# Submit PySpark job using spark-submit
echo "Submitting PySpark job..."
nohup spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 \
    stream_events_data.py \
> nohup.out 2>&1 &


# Clean up (optional)
echo "Cleaning up..."
rm my_pyspark_job.py