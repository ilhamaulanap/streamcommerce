INSERT INTO `black-machine-422712-b7.staging_streamcommerce.traffic` (
    pageUrl,
    visitCount,
    lastVisit,
    ingestion_time
)
SELECT
    pageUrl,
    visitCount,
    lastVisit,
    ingestion_time
FROM `black-machine-422712-b7.staging_streamcommerce.traffic_external`
WHERE ingestion_time > (
    SELECT MAX(COALESCE(ingestion_time, TIMESTAMP('1900-01-01 00:00:00')))
    FROM `black-machine-422712-b7.staging_streamcommerce.traffic`
);
