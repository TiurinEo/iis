from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api_handler import FastAPIHandler
import time
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI(title="ML Prediction Service", version="2.0.0")

# Метрики Prometheus
prediction_histogram = Histogram(
    'ml_prediction_values',
    'Histogram of ML model predictions',
    buckets=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

request_counter = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

model_predictions_total = Counter(
    'model_predictions_total',
    'Total number of model predictions made'
)

high_risk_predictions = Counter(
    'high_risk_predictions_total',
    'Number of high risk predictions (>0.7)'
)

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

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    active_connections.inc()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    request_counter.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    ).inc()
    
    active_connections.dec()
    return response

@app.get("/")
def read_root():
    return {"Hello": "World", "version": "2.0.0"}

@app.post("/api/prediction")
def predict(item_id: int, input_data: PredictionInput):
    try:
        prediction = handler.predict(input_data.dict())
        
        # Записываем метрики
        prediction_histogram.observe(prediction)
        model_predictions_total.inc()
        
        if prediction > 0.7:
            high_risk_predictions.inc()
        
        return {
            "item_id": item_id,
            "predict": prediction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)