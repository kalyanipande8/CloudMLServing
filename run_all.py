import json
import os

from fastapi.testclient import TestClient
from src.api import app


def main():
    client = TestClient(app)
    health = client.get("/health").json()

    for _ in range(50):
        client.post("/predict", json={"features": [0.1] * 5})

    metrics_before = client.get("/metrics").json()
    rollback_result = client.post("/rollback/v1").json()
    metrics_after_rollback = client.get("/health").json()

    os.makedirs("results", exist_ok=True)
    summary = {"health": health, "metrics_after_50_requests": metrics_before,
               "rollback_result": rollback_result, "health_after_rollback": metrics_after_rollback}
    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
