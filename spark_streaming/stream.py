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



transaction_schema = StructType([
    StructField("transactionId", StringType(), nullable=False),
    StructField("productId", StringType(), nullable=False),
    StructField("productName", StringType(), nullable=False),
    StructField("productCategory", StringType(), nullable=False),
    StructField("productPrice", DoubleType(), nullable=False),
    StructField("productQuantity", IntegerType(), nullable=False),
    StructField("productBrand", StringType(), nullable=False),
    StructField("currency", StringType(), nullable=False),
    StructField("customerId", StringType(), nullable=False),
    StructField("transactionDate", TimestampType(), nullable=False),
    StructField("paymentMethod", StringType(), nullable=False),
    StructField("totalAmount", DoubleType(), nullable=False),
])

# Schema for customer_feedback topic
feedback_schema = StructType([
    StructField("feedbackId", StringType(), nullable=False),
    StructField("customerId", StringType(), nullable=False),
    StructField("productId", StringType(), nullable=False),
    StructField("rating", IntegerType(), nullable=False),
    StructField("comment", StringType(), nullable=False),
    StructField("feedbackDate", TimestampType(), nullable=False),
])

# Schema for product_views topic
view_schema = StructType([
    StructField("productId", StringType(), nullable=False),
    StructField("viewCount", IntegerType(), nullable=False),
    StructField("lastViewed", TimestampType(), nullable=False),
])

# Schema for website_traffic topic
traffic_schema = StructType([
    StructField("pageUrl", StringType(), nullable=False),
    StructField("visitCount", IntegerType(), nullable=False),
    StructField("lastVisit", TimestampType(), nullable=False),
])


# Load data from Kafka with data quality checks
def load_data_with_quality_check(topic, schema):
    try:
        return spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", kafka_server) \
            .option("subscribe", topic) \
            .option("startingOffsets", "earliest") \
            .load() \
            .selectExpr("CAST(value AS STRING)") \
            .select(from_json(col("value"), schema).alias("data")) \
            .select("data.*") \
            .withColumn("ingestion_time", current_timestamp()) \
            .withColumn("year", year("ingestion_time")) \
            .withColumn("month", month("ingestion_time")) \
            .withColumn("day", dayofmonth("ingestion_time")) \
            .withColumn("hour", hour("ingestion_time"))
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
            .partitionBy("year", "month", "day", "hour") \
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
