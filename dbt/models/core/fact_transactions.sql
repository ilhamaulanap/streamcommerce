-- models/fact_transactions.sql

{{ config(
    materialized='table' 
) }}
select
    transactionId as transaction_id,
    productId as product_id,
    productQuantity as product_quantity,
    customerId as customer_id,
    totalAmount as total_amount,
    currency,
    paymentMethod,
    transactionDate as transaction_date,
    FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', CURRENT_TIMESTAMP(), 'Asia/Jakarta') as last_update
    
from
    {{ source('staging', 'transactions') }}  -- Reference staging transactions data
