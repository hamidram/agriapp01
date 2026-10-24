# src/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from pathlib import Path
import pandas as pd
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Agricultural Intelligence API",
    description="API for predicting agricultural outcomes based on soil and climate telemetry.",
    version="1.0.0"
)

# Initialize and instrument Prometheus metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# 1. Update schema to match the exact feature names used during model training
class AgriInput(BaseModel):
    soil_moisture_pct: float
    temperature_c: float
    ph_level: float
    rainfall_mm: float

MODEL_PATH = Path("models/model.pkl")
model = None

@app.on_event("startup")
def load_model():
    global model
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Model file not found at {MODEL_PATH}. Run your training pipeline first!")
    model = joblib.load(MODEL_PATH)

@app.get("/")
def home():
    return {"message": "Welcome to the Agricultural Intelligence API! Navigate to /docs for interactive documentation."}

@app.post("/predict")
def predict_crop(data: AgriInput):
    try:
        # 2. Construct DataFrame with exact column names expected by scikit-learn
        input_data = pd.DataFrame([{
            "soil_moisture_pct": data.soil_moisture_pct,
            "temperature_c": data.temperature_c,
            "ph_level": data.ph_level,
            "rainfall_mm": data.rainfall_mm
        }])
        
        prediction = model.predict(input_data)
        
        return {
            "status": "success",
            "prediction": prediction.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))