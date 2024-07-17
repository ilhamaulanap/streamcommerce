transaction_schema = [
    {"name": "transactionId", "type": "STRING", "mode": "NULLABLE"},
    {"name": "productId", "type": "STRING", "mode": "NULLABLE"},
    {"name": "productName", "type": "STRING", "mode": "NULLABLE"},
    {"name": "productCategory", "type": "STRING", "mode": "NULLABLE"},
    {"name": "productPrice", "type": "FLOAT", "mode": "NULLABLE"},
    {"name": "productQuantity", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "productBrand", "type": "STRING", "mode": "NULLABLE"},
    {"name": "currency", "type": "STRING", "mode": "NULLABLE"},
    {"name": "customerId", "type": "STRING", "mode": "NULLABLE"},
    {"name": "transactionDate", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "paymentMethod", "type": "STRING", "mode": "NULLABLE"},
    {"name": "totalAmount", "type": "FLOAT", "mode": "NULLABLE"},
    {"name": "ingestion_time", "type": "TIMESTAMP", "mode": "REQUIRED"}
]

traffic_schema = [
    {"name": "pageUrl", "type": "STRING", "mode": "NULLABLE"},
    {"name": "visitCount", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "lastVisit", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "ingestion_time", "type": "TIMESTAMP", "mode": "REQUIRED"}
]

feedback_schema = [
    {"name": "feedbackId", "type": "STRING", "mode": "NULLABLE"},
    {"name": "customerId", "type": "STRING", "mode": "NULLABLE"},
    {"name": "productId", "type": "STRING", "mode": "NULLABLE"},
    {"name": "rating", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "comment", "type": "STRING", "mode": "NULLABLE"},
    {"name": "feedbackDate", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "ingestion_time", "type": "TIMESTAMP", "mode": "REQUIRED"}
]

views_schema = [
    {"name": "productId", "type": "STRING", "mode": "NULLABLE"},
    {"name": "viewCount", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "lastViewed", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "ingestion_time", "type": "TIMESTAMP", "mode": "REQUIRED"}
]
