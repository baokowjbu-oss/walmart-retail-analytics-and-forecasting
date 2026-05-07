CREATE OR REPLACE TABLE `extended-altar-423112-j9.Walmart.dim_supplier` AS
SELECT 
    supplier_id,
    ANY_VALUE(supplier_lead_time) AS supplier_lead_time
FROM `extended-altar-423112-j9.Walmart.Initial`
WHERE supplier_id IS NOT NULL    
GROUP BY supplier_id;

ALTER TABLE `extended-altar-423112-j9.Walmart.dim_supplier`
ADD PRIMARY KEY(supplier_id) NOT ENFORCED;