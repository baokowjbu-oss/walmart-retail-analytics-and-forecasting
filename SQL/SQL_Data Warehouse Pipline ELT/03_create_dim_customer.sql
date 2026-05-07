CREATE OR REPLACE TABLE `extended-altar-423112-j9.Walmart.dim_customer` AS
SELECT 
    customer_id, 
    ANY_VALUE(customer_age) AS customer_age,
    ANY_VALUE(customer_gender) AS customer_gender,
    ANY_VALUE(customer_income) AS customer_income,
    ANY_VALUE(customer_loyalty_level) AS customer_loyalty_level
FROM `extended-altar-423112-j9.Walmart.Initial`
WHERE customer_id IS NOT NULL 
GROUP BY customer_id;

ALTER TABLE `extended-altar-423112-j9.Walmart.dim_customer`
ADD PRIMARY KEY (customer_id) NOT ENFORCED;