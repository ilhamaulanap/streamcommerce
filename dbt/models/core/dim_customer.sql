{{ config(
    materialized='table' 
) }}

with customers as (
    select distinct
        customerId,
        customerId as customerName,
        CONCAT(customerId,'@gmail.com') as customerEmail,
        FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', CURRENT_TIMESTAMP(), 'Asia/Jakarta') as last_update
    from
        {{ source('staging', 'transactions') }}  -- Referencing the staging table
)
select
    customerId,
    customerName,
    customerEmail,
    last_update
from customers
