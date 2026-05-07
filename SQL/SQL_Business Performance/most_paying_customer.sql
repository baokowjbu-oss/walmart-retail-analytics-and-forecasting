SELECT 
    customer_id, 
    CAST(SUM(quantity_sold * unit_price) AS INT64) AS total_spent
FROM `extended-altar-423112-j9.Walmart.fact_transaction`
GROUP BY customer_id 
ORDER BY total_spent DESC
LIMIT 5