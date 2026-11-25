"""Real REST API (FastAPI) serving the versioned model registry, with
real request/response performance logging."""
import time
import logging

from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

from .model_registry import ModelRegistry

logger = logging.getLogger("cloudmlserving")
logger.setLevel(logging.INFO)

app = FastAPI(title="CloudMLServing")
registry = ModelRegistry()
registry.register("v1", seed=1)
registry.register("v2", seed=2)

request_log = []


class PredictRequest(BaseModel):
    features: list[float]


@app.get("/health")
def health():
    return {"status": "ok", "current_version": registry.current_version}


@app.post("/predict")
def predict(req: PredictRequest):
    start = time.perf_counter()
    X = np.array(req.features).reshape(1, -1)
    pred = registry.predict(X)
    latency_ms = (time.perf_counter() - start) * 1000
    request_log.append({"version": registry.current_version, "latency_ms": latency_ms})
    logger.info("prediction served: version=%s latency_ms=%.3f", registry.current_version, latency_ms)
    return {"version": registry.current_version, "prediction": float(pred[0])}


@app.post("/rollback/{version}")
def rollback(version: str):
    registry.rollback(version)
    return {"status": "rolled_back", "current_version": registry.current_version}


@app.get("/metrics")
def metrics():
    if not request_log:
        return {"n_requests": 0}
    latencies = [r["latency_ms"] for r in request_log]
    return {"n_requests": len(request_log), "mean_latency_ms": round(sum(latencies) / len(latencies), 4)}
