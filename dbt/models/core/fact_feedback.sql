-- models/fact_feedback.sql

{{ config(
    materialized='table' 
) }}

select
    feedbackId as feedback_id,
    customerId as customer_id,
    productId as product_id,
    rating as rating,
    comment as comment,
    feedbackDate as feedback_date
from
    {{ source('staging', 'feedback') }}  -- Reference staging feedback data
