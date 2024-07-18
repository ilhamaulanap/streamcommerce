INSERT INTO `black-machine-422712-b7.staging_streamcommerce.views` (
    productId,
    viewCount,
    lastViewed,
    ingestion_time
)
SELECT
    productId,
    viewCount,
    lastViewed,
    ingestion_time  
FROM `black-machine-422712-b7.staging_streamcommerce.views_external`  
WHERE ingestion_time > (
    SELECT (COALESCE(max(ingestion_time),TIMESTAMP('1900-1-1 00:00:00'))) 
    FROM `black-machine-422712-b7.staging_streamcommerce.views`
);