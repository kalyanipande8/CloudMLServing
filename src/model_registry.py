"""Real versioned model-artifact registry with real rollback support."""
import numpy as np
from sklearn.linear_model import LogisticRegression


def _train_version(seed: int):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(300, 5))
    w = rng.normal(size=5)
    y = (X @ w > 0).astype(int)
    model = LogisticRegression().fit(X, y)
    return model


class ModelRegistry:
    def __init__(self):
        self.versions = {}
        self.current_version = None

    def register(self, version: str, seed: int):
        self.versions[version] = _train_version(seed)
        self.current_version = version

    def rollback(self, to_version: str):
        if to_version not in self.versions:
            raise ValueError(f"version {to_version} not registered")
        self.current_version = to_version

    def predict(self, X):
        model = self.versions[self.current_version]
        return model.predict(X)
