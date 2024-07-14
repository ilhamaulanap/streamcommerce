# kafka_consumer.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

KAFKA_ADDRESS = '34.143.189.53'

# Create a Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .getOrCreate()

# Set log level to WARN to reduce verbosity
spark.sparkContext.setLogLevel("WARN")

# Define Kafka parameters
kafka_bootstrap_servers = f"{KAFKA_ADDRESS}:9092" # Change this to your Kafka broker address
kafka_topic = "financial_transactions"  # Change this to your Kafka topic

# Read data from Kafka
kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .load()

# Select the key and value columns and cast them to strings
kafka_df = kafka_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Function to print each batch of data
def foreach_batch_function(df, epoch_id):
    df.show(truncate=False)

# Start the streaming query
query = kafka_df.writeStream \
    .outputMode("append") \
    .foreachBatch(foreach_batch_function) \
    .start()

# Await termination
query.awaitTermination()
