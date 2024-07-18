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
    SELECT MAX(COALESCE(ingestion_time, TIMESTAMP('1900-01-01 00:00:00'))) FROM `black-machine-422712-b7.staging_streamcommerce.views`
);