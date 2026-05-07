CREATE OR REPLACE TABLE `extended-altar-423112-j9.Walmart.dim_weather` AS
SELECT
    ROW_NUMBER() OVER(ORDER BY weather_conditions) AS weather_id,
    weather_conditions
FROM (
  SELECT DISTINCT weather_conditions
  FROM `extended-altar-423112-j9.Walmart.Initial`
  WHERE weather_conditions IS NOT NULL
);

ALTER TABLE `extended-altar-423112-j9.Walmart.dim_weather`
ADD PRIMARY KEY(weather_id) NOT ENFORCED;