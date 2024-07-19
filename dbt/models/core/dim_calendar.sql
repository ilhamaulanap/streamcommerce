-- models/dim_time.sql

{{ config(
    schema=var('prod_dataset'),  
    materialized='table'  
) }}

with time_data as (
    select
        distinct
        cast(transactionDate as date) as date_key,
        extract(year from transactionDate) as year,
        extract(month from transactionDate) as month,
        extract(day from transactionDate) as day,
        extract(quarter from transactionDate) as quarter,
        FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', CURRENT_TIMESTAMP(), 'Asia/Jakarta') as last_update
    from
        {{ source('staging', 'transactions') }}  -- Reference staging transactions data
)

select
    date_key,
    year,
    month,
    day,
    quarter,
    last_update
from time_data
