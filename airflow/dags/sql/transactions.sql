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
    SELECT MAX(COALESCE(ingestion_time, TIMESTAMP('1900-01-01 00:00:00')))
    FROM `black-machine-422712-b7.staging_streamcommerce.transactions`
);
