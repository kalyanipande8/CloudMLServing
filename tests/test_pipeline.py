import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from src.api import app
from src.model_registry import ModelRegistry
import numpy as np

client = TestClient(app)


def test_01_health_returns_200():
    assert client.get("/health").status_code == 200


def test_02_health_status_ok():
    assert client.get("/health").json()["status"] == "ok"


def test_03_health_reports_current_version():
    assert client.get("/health").json()["current_version"] in {"v1", "v2"}


def test_04_predict_returns_200():
    resp = client.post("/predict", json={"features": [0.1] * 5})
    assert resp.status_code == 200


def test_05_predict_returns_prediction_field():
    resp = client.post("/predict", json={"features": [0.1] * 5})
    assert "prediction" in resp.json()


def test_06_predict_returns_version_field():
    resp = client.post("/predict", json={"features": [0.1] * 5})
    assert "version" in resp.json()


def test_07_metrics_initially_structured():
    resp = client.get("/metrics")
    assert "n_requests" in resp.json()


def test_08_metrics_increment_after_requests():
    before = client.get("/metrics").json()["n_requests"]
    client.post("/predict", json={"features": [0.1] * 5})
    after = client.get("/metrics").json()["n_requests"]
    assert after == before + 1


def test_09_rollback_to_registered_version_succeeds():
    resp = client.post("/rollback/v1")
    assert resp.status_code == 200
    assert resp.json()["current_version"] == "v1"


def test_10_rollback_to_unregistered_version_raises():
    registry = ModelRegistry()
    registry.register("v1", seed=1)
    try:
        registry.rollback("v99")
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_11_registry_predicts_with_correct_shape():
    registry = ModelRegistry()
    registry.register("v1", seed=1)
    preds = registry.predict(np.zeros((3, 5)))
    assert len(preds) == 3


def test_12_registry_tracks_current_version():
    registry = ModelRegistry()
    registry.register("v1", seed=1)
    assert registry.current_version == "v1"


def test_13_registry_switches_version_on_register():
    registry = ModelRegistry()
    registry.register("v1", seed=1)
    registry.register("v2", seed=2)
    assert registry.current_version == "v2"


def test_14_registry_holds_multiple_versions():
    registry = ModelRegistry()
    registry.register("v1", seed=1)
    registry.register("v2", seed=2)
    assert set(registry.versions.keys()) == {"v1", "v2"}


def test_15_predictions_after_rollback_use_old_version():
    registry = ModelRegistry()
    registry.register("v1", seed=1)
    registry.register("v2", seed=2)
    registry.rollback("v1")
    assert registry.current_version == "v1"


def test_16_app_has_predict_route():
    routes = [r.path for r in app.routes]
    assert "/predict" in routes


def test_17_app_has_rollback_route():
    routes = [r.path for r in app.routes]
    assert any("/rollback" in r for r in routes)


def test_18_mean_latency_is_nonnegative():
    client.post("/predict", json={"features": [0.1] * 5})
    metrics = client.get("/metrics").json()
    assert metrics["mean_latency_ms"] >= 0
