CREATE OR REPLACE TABLE `extended-altar-423112-j9.Walmart.fact_transaction` AS
SELECT
    raw.transaction_id,
    CAST(FORMAT_TIMESTAMP('%Y%m%d', raw.transaction_date) AS INT64) AS date_id,
    raw.store_id,
    raw.customer_id,
    raw.product_id,
    pro.promotion_id,
    wth.weather_id,
    raw.quantity_sold,
    raw.unit_price,
    raw.payment_method,
    raw.actual_demand

FROM `extended-altar-423112-j9.Walmart.Initial` raw

LEFT JOIN `extended-altar-423112-j9.Walmart.dim_promotion` pro
ON raw.promotion_type = pro.promotion_type

LEFT JOIN `extended-altar-423112-j9.Walmart.dim_weather` wth
ON raw.weather_conditions = wth.weather_conditions

WHERE transaction_id IS NOT NULL;

ALTER TABLE `extended-altar-423112-j9.Walmart.fact_transaction`
ADD PRIMARY KEY(transaction_id) NOT ENFORCED;