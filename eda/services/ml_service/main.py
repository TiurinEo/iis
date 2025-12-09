from fastapi import FastAPI
from pydantic import BaseModel
from api_handler import FastAPIHandler

app = FastAPI(title="ML Prediction Service", version="1.0.0")

class PredictionInput(BaseModel):
    age: float
    sex: int
    cp: int
    trestbps: float
    chol: float
    fbs: int
    restecg: int
    thalach: float
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

handler = FastAPIHandler()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/prediction")
def predict(item_id: int, input_data: PredictionInput):
    try:
        prediction = handler.predict(input_data.dict())
        return {
            "item_id": item_id,
            "predict": prediction
        }
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}