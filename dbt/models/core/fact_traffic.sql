-- models/fact_page_views.sql

{{ config(
    materialized='table' 
) }}
select
    pageUrl as page_url,
    visitCount as visit_count,
    lastVisit as last_visit,
    FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', CURRENT_TIMESTAMP(), 'Asia/Jakarta') as last_update

from
    {{ source('staging', 'traffic') }}  -- Reference staging traffic data
