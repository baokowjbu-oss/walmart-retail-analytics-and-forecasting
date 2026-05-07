WITH Daily_stats AS (
    SELECT 
        PARSE_DATE('%Y%m%d', CAST(date_id AS STRING)) AS full_date,
        SUM(quantity_sold * unit_price) AS total_revenue,
        SUM(quantity_sold * unit_price * 0.6) AS total_cost
    FROM `extended-altar-423112-j9.Walmart.fact_transaction`
    {where_clause}
    GROUP BY date_id
)
SELECT 
    DATE_TRUNC(full_date, {time_interval.upper()}) AS trend_date,
    SUM(total_revenue) AS revenue,
    SUM(total_cost) AS cost,
    (SUM(total_revenue) - SUM(total_cost)) AS profit, 
    SAFE_DIVIDE((SUM(total_revenue) - SUM(total_cost)), SUM(total_revenue)) * 100 AS gross_margin
FROM Daily_stats
GROUP BY trend_date 
ORDER BY trend_date ASC