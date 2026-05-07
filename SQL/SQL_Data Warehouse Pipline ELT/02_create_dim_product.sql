CREATE OR REPLACE TABLE `extended-altar-423112-j9.Walmart.dim_product` AS
SELECT 
    product_id, 
    ANY_VALUE(product_name) AS product_name, 
    ANY_VALUE(category) AS category, 
    ANY_VALUE(unit_price) AS base_unit_price
FROM `extended-altar-423112-j9.Walmart.Initial`
WHERE product_id IS NOT NULL 
GROUP BY product_id;

ALTER TABLE `extended-altar-423112-j9.Walmart.dim_product` 
ADD PRIMARY KEY(product_id) NOT ENFORCED;