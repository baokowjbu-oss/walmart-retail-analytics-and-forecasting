from fastapi import FastAPI
from pydantic import BaseModel
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
        
    if f'weekday_{request.day}' in encoded_data:
        encoded_data[f'weekday_{request.day}'] = 1
        
    df = pd.DataFrame([encoded_data])
    prediction = model.predict(df)
    
    return {"predicted_demand": round(prediction[0], 2)}