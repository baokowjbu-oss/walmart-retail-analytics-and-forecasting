-- 1. Create table and Load deduplicate data
CREATE OR REPLACE TABLE `extended-altar-423112-j9.Walmart.dim_store` AS
SELECT store_id, ANY_VALUE(store_location) AS store_location
FROM `extended-altar-423112-j9.Walmart.Initial`
WHERE store_id IS NOT NULL
GROUP BY store_id;

--2. Add primary key
ALTER TABLE `extended-altar-423112-j9.Walmart.dim_store`
ADD PRIMARY KEY(store_id) NOT ENFORCED;