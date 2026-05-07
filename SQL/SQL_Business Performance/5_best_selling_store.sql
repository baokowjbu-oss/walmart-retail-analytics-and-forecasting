SELECT 
    store_id, 
    SUM(quantity_sold) AS total_sales
FROM `extended-altar-423112-j9.Walmart.fact_transaction`
GROUP BY store_id 
ORDER BY SUM(quantity_sold) DESC 
LIMIT 5