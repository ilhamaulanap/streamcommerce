from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

# Schema for financial_transactions topic
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
    StructField("ingestion_time", TimestampType(), nullable=False),  # Added ingestion_time
])

# Schema for customer_feedback topic
feedback_schema = StructType([
    StructField("feedbackId", StringType(), nullable=False),
    StructField("customerId", StringType(), nullable=False),
    StructField("productId", StringType(), nullable=False),
    StructField("rating", IntegerType(), nullable=False),
    StructField("comment", StringType(), nullable=False),
    StructField("feedbackDate", TimestampType(), nullable=False),
    StructField("ingestion_time", TimestampType(), nullable=False),  # Added ingestion_time
])

# Schema for product_views topic
view_schema = StructType([
    StructField("productId", StringType(), nullable=False),
    StructField("viewCount", IntegerType(), nullable=False),
    StructField("lastViewed", TimestampType(), nullable=False),
    StructField("ingestion_time", TimestampType(), nullable=False),  # Added ingestion_time
])

# Schema for website_traffic topic
traffic_schema = StructType([
    StructField("pageUrl", StringType(), nullable=False),
    StructField("visitCount", IntegerType(), nullable=False),
    StructField("lastVisit", TimestampType(), nullable=False),
    StructField("ingestion_time", TimestampType(), nullable=False),  # Added ingestion_time
])
