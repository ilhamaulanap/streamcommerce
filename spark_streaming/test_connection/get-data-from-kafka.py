from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Create a Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkIntegration") \
    .getOrCreate()

# Set log level to ERROR or WARN
spark.sparkContext.setLogLevel("ERROR")

# Kafka broker details
kafka_server = "34.143.189.53:9092"
topics = "financial_transactions"
group_id = "consumer-test-connection"

# Define the Kafka source for streaming
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_server) \
    .option("subscribe", topics) \
    .option("group.id", group_id) \
    .option("startingOffsets", "earliest") \
    .load()

# Convert the value column from binary to string (if necessary)
df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Process the data (example: print to console)
query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Wait for the termination of the query (you can customize based on your needs)
query.awaitTermination()
