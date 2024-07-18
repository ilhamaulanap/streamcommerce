INSERT INTO `black-machine-422712-b7.staging_streamcommerce.feedback` (
    feedbackId,
    customerId,
    productId,
    rating,
    comment,
    feedbackDate,
    ingestion_time
)
SELECT
    feedbackId,
    customerId,
    productId,
    rating,
    comment,
    feedbackDate,
    ingestion_time
FROM `black-machine-422712-b7.staging_streamcommerce.feedback_external`
WHERE ingestion_time > (
    SELECT MAX(COALESCE(ingestion_time, TIMESTAMP('1900-01-01 00:00:00')))
    FROM `black-machine-422712-b7.staging_streamcommerce.feedback`
);
