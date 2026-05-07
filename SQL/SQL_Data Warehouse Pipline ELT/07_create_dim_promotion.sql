CREATE OR REPLACE TABLE `extended-altar-423112-j9.Walmart.dim_promotion` AS
SELECT
    ROW_NUMBER() OVER(ORDER BY promotion_type) AS promotion_id,
    promotion_type
FROM(
  SELECT DISTINCT promotion_type
  FROM `extended-altar-423112-j9.Walmart.Initial`
  WHERE promotion_type IS NOT NULL
);

ALTER TABLE `extended-altar-423112-j9.Walmart.dim_promotion`
ADD PRIMARY KEY(promotion_id) NOT ENFORCED;