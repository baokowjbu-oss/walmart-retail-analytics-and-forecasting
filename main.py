from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud import bigquery
from google.auth.exceptions import DefaultCredentialsError
import joblib
import pandas as pd

model = joblib.load('demand_model.pkl')

app = FastAPI(title="Walmart Demand API")

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
    encoded_data['holiday_indicator'] = 1 if request.is_holiday else 0
    
    if f'weather_conditions_{request.weather}' in encoded_data:
        encoded_data[f'weather_conditions_{request.weather}'] = 1
        
    if f'promotion_type_{request.promotion}' in encoded_data:
        encoded_data[f'promotion_type_{request.promotion}'] = 1
        
    if f'week_day_{request.day}' in encoded_data:
        encoded_data[f'week_day_{request.day}'] = 1
        
    df = pd.DataFrame([encoded_data])
    prediction = model.predict(df)
    
    return {"predicted_demand": round(prediction[0], 2)}

@app.get("/analytics/top-sellers")
def get_top_sellers():
    try:
        # Moved the client inside the function so it doesn't crash the server on startup
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
        
    except DefaultCredentialsError:
        return {"error": "Server is not authenticated with Google Cloud yet!"}
    except Exception as e:
        return {"error": str(e)}
