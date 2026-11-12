"""Model interfaces for baselines BL-1 to BL-6 and framework classifier F2 (protocol draft section 11).

Every model exposes fit(X, y) -> self and predict_proba(X) -> positive-class probabilities (1-D).
The learners themselves come from third-party packages that are NOT installed (D-002 PROPOSED;
see environment/README.md); the registry reports what is missing instead of failing late. No model
in this file has been fitted to any data in this repository.

Fitting any classifier, even on synthetic data, is outside the current permissions until the
synthetic-verification test plan and runs are authorised (D-040, Rule S); this module therefore only
defines the interfaces. FixedScoreStub is a NON-LEARNING test double used to test the harness
plumbing: it fits nothing and maps one input column through a fixed logistic function.
"""
from __future__ import annotations

import importlib.util

import numpy as np

# name: (description, required import, needs feature scaling)
REGISTRY = {
    "BL-1": ("elastic-net logistic regression", "sklearn", True),
    "BL-2": ("random forest", "sklearn", False),
    "BL-3": ("gradient-boosted trees (XGBoost; Q-048)", "xgboost", False),
    "BL-4": ("RBF support vector machine with Platt scaling", "sklearn", True),
    "BL-5": ("multilayer perceptron, 1-2 hidden layers", "sklearn", True),
    "BL-6": ("k-nearest neighbours (Q-049; no extra package)", "sklearn", True),
    "F2": ("gradient-boosted trees, same family and budget as BL-3", "xgboost", False),
}


def availability():
    """{model: (available, missing package or None)} for the current environment."""
    out = {}
    for name, (_, pkg, _) in REGISTRY.items():
        ok = importlib.util.find_spec(pkg) is not None
        out[name] = (ok, None if ok else pkg)
    return out


def needs_scaling(name):
    return REGISTRY[name][2]


def build_model(name, config, seed):
    """Construct an unfitted model. Raises RuntimeError naming the missing package if unavailable."""
    if name == "STUB":
        return FixedScoreStub(**config)
    if name not in REGISTRY:
        raise KeyError(f"unknown model {name!r}")
    ok, missing = availability()[name]
    if not ok:
        raise RuntimeError(f"{name} needs the package {missing!r}, which is not installed "
                           "(environment pinning D-002 and installation need researcher authorisation)")
    if name == "BL-1":
        from sklearn.linear_model import LogisticRegression
        return LogisticRegression(penalty="elasticnet", solver="saga", C=config["C"],
                                  l1_ratio=config["l1_ratio"], max_iter=5000, random_state=seed)
    if name == "BL-2":
        from sklearn.ensemble import RandomForestClassifier
        return RandomForestClassifier(random_state=seed, n_jobs=1, **config)
    if name in ("BL-3", "F2"):
        from xgboost import XGBClassifier
        return XGBClassifier(random_state=seed, n_jobs=1, eval_metric="logloss", tree_method="hist", **config)
    if name == "BL-4":
        from sklearn.svm import SVC
        return SVC(kernel="rbf", probability=True, random_state=seed, **config)
    if name == "BL-5":
        from sklearn.neural_network import MLPClassifier
        cfg = dict(config)
        layers = tuple(int(x) for x in str(cfg.pop("hidden_layer_sizes")).split("-"))
        return MLPClassifier(hidden_layer_sizes=layers, random_state=seed, max_iter=2000, **cfg)
    if name == "BL-6":
        from sklearn.neighbors import KNeighborsClassifier
        return KNeighborsClassifier(**config)
    raise KeyError(name)


def positive_proba(model, X):
    """Positive-class probability as a 1-D array for sklearn-style or stub models."""
    p = np.asarray(model.predict_proba(X), dtype=float)
    return p[:, 1] if p.ndim == 2 else p


class FixedScoreStub:
    """Non-learning test double: p = sigmoid(coef * x[:, column] + bias). fit() learns nothing."""

    def __init__(self, coef=1.0, bias=0.0, column=0):
        self.coef, self.bias, self.column = float(coef), float(bias), int(column)

    def fit(self, X, y):
        return self

    def predict_proba(self, X):
        z = self.coef * np.asarray(X, dtype=float)[:, self.column] + self.bias
        return 1.0 / (1.0 + np.exp(-z))
