INSERT INTO `black-machine-422712-b7.staging_streamcommerce.transactions` (
    transactionId,
    productId,
    productName,
    productCategory,
    productPrice,
    productQuantity,
    productBrand,
    currency,
    customerId,
    transactionDate,
    paymentMethod,
    totalAmount,
    ingestion_time
)
SELECT
    transactionId,
    productId,
    productName,
    productCategory,
    productPrice,
    productQuantity,
    productBrand,
    currency,
    customerId,
    transactionDate,
    paymentMethod,
    totalAmount,
    ingestion_time
FROM `black-machine-422712-b7.staging_streamcommerce.transactions_external`
WHERE ingestion_time > (
    SELECT (COALESCE(max(ingestion_time),TIMESTAMP('1900-1-1 00:00:00')))
    FROM `black-machine-422712-b7.staging_streamcommerce.transactions`
);
