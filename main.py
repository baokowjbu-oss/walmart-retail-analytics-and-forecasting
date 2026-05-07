from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud import bigquery
from google.auth.exceptions import DefaultCredentialsError
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd

model = joblib.load('demand_model.pkl')

app = FastAPI(title="Walmart Demand API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)
class CleanRequest(BaseModel):
    price: float
    is_holiday: bool
    weather: str
    promotion: str
    day: str

@app.post("/predict")
def predict_demand(request: CleanRequest):
    expected_columns = model.feature_names_in_ 

    encoded_data = {col: 0 for col in expected_columns}
    encoded_data['unit_price'] = request.price
    encoded_data['is_holiday'] = 1 if request.is_holiday else 0
    
    if f'weather_conditions_{request.weather}' in encoded_data:
        encoded_data[f'weather_conditions_{request.weather}'] = 1
        
    if f'promotion_type_{request.promotion}' in encoded_data:
        encoded_data[f'promotion_type_{request.promotion}'] = 1
        
    if f'week_day_{request.day}' in encoded_data:
        encoded_data[f'week_day_{request.day}'] = 1
        
    df = pd.DataFrame([encoded_data])
    prediction = model.predict(df)
    
    return {"predicted_demand": round(float(prediction[0]), 2)}

@app.get("/analytics/top-sellers")
def get_top_sellers():
    try:
        client = bigquery.Client()
        query = """
        SELECT 
            pro.product_name, 
            SUM(transac.quantity_sold) AS total_product_sale
        FROM `extended-altar-423112-j9.Walmart.fact_transaction` transac
        JOIN  `extended-altar-423112-j9.Walmart.dim_product` pro ON transac.product_id = pro.product_id
        GROUP BY pro.product_name 
        ORDER BY SUM(transac.quantity_sold) DESC
        LIMIT 5"""
        
        query_job = client.query(query)
        results = query_job.result()
        
        top_sellers = []
        for row in results:
            top_sellers.append(
                {
                   "product_name": row.product_name,
                    "total_sales": row.total_product_sale
                }
            )
        return {"top_sellers": top_sellers}
        
    except Exception as e:
        return {"error": str(e)}
@app.get("analytics/worst-products")
def get_worst_sellers():
    try:
        client = bigquery.Client()
        query = """
            SELECT 
                pro.product_name, 
                SUM(transac.quantity_sold) AS total_product_sale
            FROM `extended-altar-423112-j9.Walmart.fact_transaction` transac
            JOIN  `extended-altar-423112-j9.Walmart.dim_product` pro ON transac.product_id = pro.product_id
            GROUP BY pro.product_name 
            ORDER BY SUM(transac.quantity_sold) ASC
            LIMIT 5"""
        query_job = client.query(query)
        query_result = query_job.result()
        worst_sellers = []
        for row in query_result:
            worst_sellers.append
            (
                {
                    "product_name" : row.product_name,
                    "total_sale" : row.total_product_sale
                }
            )
            return {"worst_sellers": worst_sellers}
    except Exception as e:
        return {"error" : str(e)}
@app.get("analytics/top-stores")
def get_top_stores():
    try:
        client = bigquery.Client()
        query = """
        SELECT 
            store_id, 
            SUM(quantity_sold) AS total_sales
        FROM `extended-altar-423112-j9.Walmart.fact_transaction`
        GROUP BY store_id 
        ORDER BY SUM(quantity_sold) DESC 
        LIMIT 5"""
        query_result = client.query(query).result()
        return {"top_stores" : [{"store_id": row.store_id, "total_sales" : row.total_sales} for row in query_result]}
    except Exception as e:
        return {"error" : str(e)}
@app.get("analytics/worst-stores")
def get_worst_stores():
    try:
        client = bigquery.Client()
        query = """
        SELECT 
            store_id, 
            SUM(quantity_sold) AS total_sales
        FROM `extended-altar-423112-j9.Walmart.fact_transaction`
        GROUP BY store_id 
        ORDER BY SUM(quantity_sold) ASC
        LIMIT 5"""
        query_result = client.query(query).result()
        return {"worst_stores" : [{"store_id": row.store_id, "total_sales" : row.total_sales} for row in query_result]}
    except Exception as e:
        return {"error" : str(e)}
@app.get("analytics/most-pay")
def get_most_paying_customer():
    try:
        client = bigquery.Client()
        query = """
        SELECT 
            customer_id, 
            CAST(SUM(quantity_sold * unit_price) AS INT64) AS total_spent
        FROM `extended-altar-423112-j9.Walmart.fact_transaction`
        GROUP BY customer_id 
        ORDER BY total_spent DESC
        LIMIT 5
        """
        query_result = client.query(query).result()
        return {"top_pay_customer" : [{"customer_id": row.customer_id, "total_spent" : row.total_spent} for row in query_result]}
    except Exception as e:
        return {"error" : str(e)}
@app.get("analytics/sales-recap")
def get_sales_trend(time_interval: str = "month"):
    try:
        valid_time_interval = ["day", "week", "month", "quarter"]
        if time_interval.lower() not in valid_time_interval:
            return {"error" : "invalid time interval. Valid time interval is day, week, month, quarter."}
        client = bigquery.Client()
        query = f"""
        WITH Daily_stats AS (
          SELECT 
              PARSE_DATE('%Y%m%d', CAST(date_id AS STRING)) AS full_date,
              SUM(quantity_sold * unit_price) AS total_revenue,
              SUM(quantity_sold * unit_price * 0.6) AS total_cost,
          FROM `extended-altar-423112-j9.Walmart.fact_transaction`
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
        """
        query_result = client.query(query).result()
        trend_data = []
        for row in query_result:
            trend_date.append({
                "trend_date" : str(row.trend_date),
                "revenue" : round(row.revenue,2),
                "cost" : round(row.cost,2),
                "profit" : round(row.profit,2),
                "gross_margin" : round(row.gross_margin,2) if row.gross_margin else 0
            })
        return {"time_interval" : time_interval, "sales_trend" : trend_data}
    except Exception as e:
        return {"error" : str(e)}
    
        
