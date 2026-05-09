"""
FastAPI Inference Service

Phase 1 deliverable: Basic inference API for ML model serving.
"""

from typing import List
from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prometheus_client import Counter, Gauge, generate_latest
from fastapi.responses import Response


# Prometheus metrics
INFERENCE_REQUESTS = Counter(
    "inference_requests_total", 
    "Total number of inference requests"
)
MODEL_LOAD_TIME = Gauge(
    "model_load_seconds", 
    "Time taken to load the model"
)
PREDICTIONS_MADE = Counter(
    "predictions_total", 
    "Total predictions made"
)

# Global model variable
model = None
model_path = Path("models/model.joblib")


def load_model() -> object:
    """Load model from disk with timing metric."""
    import time
    start = time.time()
    
    if not model_path.exists():
        return None
    
    model = joblib.load(model_path)
    MODEL_LOAD_TIME.set(time.time() - start)
    return model


app = FastAPI(
    title="ML Inference API",
    description="Production inference service for ML models",
    version="1.0.0"
)


# Request/Response models
class PredictRequest(BaseModel):
    features: List[float] = Field(
        ..., 
        description="Input features for prediction"
    )


class PredictResponse(BaseModel):
    prediction: float | int
    probabilities: List[float] | None = None
    model_version: str


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


@app.on_event("startup")
async def startup_event():
    """Load model on startup."""
    global model
    model = load_model()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None
    )


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """
    Make a prediction using the loaded model.
    
    Phase 1 deliverable: Basic inference endpoint.
    """
    global model
    
    INFERENCE_REQUESTS.inc()
    
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Model not loaded. Train a model first."
        )
    
    try:
        # Reshape for single prediction
        X = np.array(request.features).reshape(1, -1)
        
        # Get prediction
        pred = model.predict(X)
        
        # Get probabilities if available
        probs = None
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X)[0].tolist()
        
        PREDICTIONS_MADE.inc()
        
        return PredictResponse(
            prediction=float(pred[0]) if hasattr(pred[0], '__float__') else int(pred[0]),
            probabilities=probs,
            model_version="1.0.0"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/predict/batch")
async def predict_batch(features: str):
    """
    Batch prediction endpoint.
    
    Query param: features as comma-separated values (e.g., "1.0,2.0,3.0")
    """
    global model
    
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Model not loaded."
        )
    
    try:
        # Parse comma-separated features
        feature_list = [float(x) for x in features.split(",")]
        X = np.array(feature_list).reshape(1, -1)
        
        pred = model.predict(X)
        
        return {"prediction": float(pred[0])}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)