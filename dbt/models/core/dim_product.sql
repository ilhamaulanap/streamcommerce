{{ config(
    materialized='table' 
) }}

with products as (
    select distinct
        productId,
        productName,
        productCategory,
        productPrice,
        productBrand,
        FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', CURRENT_TIMESTAMP(), 'Asia/Jakarta') as last_update
    from
        {{ source('staging', 'transactions') }}  -- Referencing the staging table
)
select
    productId,
    productName,
    productPrice
    productCategory,
    productBrand,
    last_update
from products