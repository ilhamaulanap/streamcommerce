#!/bin/bash


# Fetch PySpark file from GitHub
echo "Fetching PySpark file from GitHub..."
git clone echo https://github.com/ilhamaulanap/streamcommerce.git
cd streamcommerce/spark_streaming

# Submit PySpark job using spark-submit
echo "Submitting PySpark job..."
nohup spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 \
    stream.py \
> nohup.out 2>&1 &


