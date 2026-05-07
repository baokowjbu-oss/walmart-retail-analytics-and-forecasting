CREATE OR REPLACE TABLE `extended-altar-423112-j9.Walmart.dim_date` AS 
SELECT 
    CAST(FORMAT_TIMESTAMP('%Y%m%d', transaction_date) AS INT64) AS date_id,
    DATE(transaction_date) AS `date`,
    ANY_VALUE(weekday) AS week_day,
    ANY_VALUE(holiday_indicator) AS is_holiday   
FROM `extended-altar-423112-j9.Walmart.Initial`
WHERE transaction_date IS NOT NULL
GROUP BY date_id, `date`;

ALTER TABLE `extended-altar-423112-j9.Walmart.dim_date`
ADD PRIMARY KEY(date_id) NOT ENFORCED;