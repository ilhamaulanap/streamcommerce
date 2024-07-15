from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, year, month, dayofmonth, hour, minute, current_timestamp
from pyspark.sql.streaming import DataStreamReader
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
import logging

# Initialize logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Define the Spark session
spark = SparkSession.builder \
    .appName("KafkaDataIngestion") \
    .getOrCreate()

# Define Kafka IP Address and topics
kafka_server = "34.143.189.53:9092"
transactions_topic = 'financial_transactions'
feedback_topic = 'customer_feedback'
views_topic = 'product_views'
traffic_topic = 'website_traffic'

# Define GCS output path and checkpoints path
output_path = "gs://streamcommerce_202407/events_data/"
checkpoints_path = f"{output_path}checkpoints/"

# Define ingestion time format
ingestion_time_format = 'yyyy-MM-dd HH:mm:ss'

# Define schemas (import from schemas.py)
from schemas import transaction_schema, feedback_schema, view_schema, traffic_schema

# Load data from Kafka with data quality checks
def load_data_with_quality_check(topic, schema):
    try:
        return spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", kafka_server) \
            .option("subscribe", topic) \
            .load() \
            .selectExpr("CAST(value AS STRING)", "CAST(timestamp AS TIMESTAMP) as ingestion_time") \
            .select(from_json(col("value"), schema).alias("data"), col("ingestion_time")) \
            .select("data.*", "ingestion_time") \
            .withColumn("year", year("ingestion_time")) \
            .withColumn("month", month("ingestion_time")) \
            .withColumn("day", dayofmonth("ingestion_time")) \
            .withColumn("hour", hour("ingestion_time")) \
            .withColumn("minute", minute("ingestion_time"))
    except Exception as e:
        logger.error(f"Error loading data from topic {topic}: {e}")

# Write data to GCS with ingestion_time and error handling
def write_to_gcs(df, topic, output_path):
    try:
        query = df.writeStream \
            .outputMode("append") \
            .format("parquet") \
            .option("path", output_path + topic) \
            .option("checkpointLocation", f"{checkpoints_path}{topic}") \
            .partitionBy("year", "month", "day", "hour", "minute") \
            .start()
        return query
    except Exception as e:
        logger.error(f"Error writing data to GCS for topic {topic}: {e}")

# Load and process data with data quality checks
transactions_df = load_data_with_quality_check(transactions_topic, transaction_schema)
feedback_df = load_data_with_quality_check(feedback_topic, feedback_schema)
views_df = load_data_with_quality_check(views_topic, view_schema)
traffic_df = load_data_with_quality_check(traffic_topic, traffic_schema)

# Write data for each topic with error handling
query_transactions = write_to_gcs(transactions_df, "transactions", output_path)
query_feedback = write_to_gcs(feedback_df, "feedback", output_path)
query_views = write_to_gcs(views_df, "views", output_path)
query_traffic = write_to_gcs(traffic_df, "traffic", output_path)

# Wait for termination with error handling
try:
    query_transactions.awaitTermination()
    query_feedback.awaitTermination()
    query_views.awaitTermination()
    query_traffic.awaitTermination()
except Exception as e:
    logger.error(f"Error awaiting termination: {e}")

# Stop the Spark session
spark.stop()
