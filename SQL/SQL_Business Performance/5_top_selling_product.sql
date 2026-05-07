SELECT 
    pro.product_name, 
    SUM(transac.quantity_sold) AS total_product_sale
FROM `extended-altar-423112-j9.Walmart.fact_transaction` transac
JOIN  `extended-altar-423112-j9.Walmart.dim_product`pro ON transac.product_id = pro.product_id
GROUP BY pro.product_name 
ORDER BY SUM(transac.quantity_sold) DESC
LIMIT 5