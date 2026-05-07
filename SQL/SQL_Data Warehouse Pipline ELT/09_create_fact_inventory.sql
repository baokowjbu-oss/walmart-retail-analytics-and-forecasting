CREATE OR REPLACE TABLE `extended-altar-423112-j9.Walmart.fact_inventory` AS
SELECT
    CAST(FORMAT_TIMESTAMP('%Y%m%d', transaction_date) AS INT64) AS date_id,
    store_id,
    product_id,
    MIN(inventory_level) AS inventory_level,
    ANY_VALUE(reorder_point) AS reorder_point,
    ANY_VALUE(reorder_quantity) AS reorder_quantity,
    ANY_VALUE(supplier_id) AS supplier_id,
    LOGICAL_OR(stockout_indicator) AS stockout_indicator

FROM `extended-altar-423112-j9.Walmart.Initial` 
WHERE transaction_date IS NOT NULL AND store_id IS NOT NULL AND product_id IS NOT NULL
GROUP BY date_id, store_id, product_id;

ALTER TABLE `extended-altar-423112-j9.Walmart.fact_inventory`
ADD PRIMARY KEY(date_id, store_id, product_Id) NOT ENFORCED;
