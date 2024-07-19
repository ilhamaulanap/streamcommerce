-- models/fact_page_views.sql

{{ config(
    materialized='table' 
) }}

select
    productId as product_id,
    viewCount as view_count,
    lastViewed as last_viewed,
    FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', CURRENT_TIMESTAMP(), 'Asia/Jakarta') as last_update
from
    {{ source('staging', 'views') }}  -- Reference staging views data
