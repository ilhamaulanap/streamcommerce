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
   SELECT (COALESCE(max(ingestion_time),TIMESTAMP('1900-1-1 00:00:00')))
    FROM `black-machine-422712-b7.staging_streamcommerce.traffic`
);
