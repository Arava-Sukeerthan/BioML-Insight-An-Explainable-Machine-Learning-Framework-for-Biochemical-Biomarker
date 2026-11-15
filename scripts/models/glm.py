"""Small weighted logistic-regression solver (IRLS), numpy only.

Used for calibration intercept/slope (metrics.py) and Platt scaling (calibration.py). It is a
numerical routine, not a predictive model of the study: it fits at most two parameters on given
scores. Software scaffolding for the DRAFT experimental protocol (not approved, not frozen).
"""
from __future__ import annotations

import numpy as np

EPS = 1e-15


def logit(p):
    p = np.clip(np.asarray(p, dtype=float), EPS, 1 - EPS)
    return np.log(p / (1 - p))


def sigmoid(z):
    z = np.asarray(z, dtype=float)
    out = np.empty_like(z)
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    ez = np.exp(z[~pos])
    out[~pos] = ez / (1.0 + ez)
    return out


def fit_logistic(design, y, weights=None, offset=None, max_iter=100, tol=1e-10, ridge=0.0):
    """Weighted logistic regression by iteratively reweighted least squares.

    design: (n, k) matrix (include a column of ones for an intercept); y: 0/1; weights: optional
    non-negative case weights; offset: optional fixed linear-predictor term. ridge: optional small
    L2 penalty for numerical stability (0 = maximum likelihood). Returns the coefficient vector.
    Raises ValueError on invalid input or non-convergence (fail closed, never a silent result)."""
    X = np.asarray(design, dtype=float)
    y = np.asarray(y, dtype=float)
    if X.ndim != 2 or X.shape[0] != y.shape[0]:
        raise ValueError("design must be (n, k) with n = len(y)")
    if not np.isin(y, (0.0, 1.0)).all():
        raise ValueError("y must be 0/1")
    if not np.isfinite(X).all():
        raise ValueError("design contains non-finite values")
    w = np.ones_like(y) if weights is None else np.asarray(weights, dtype=float)
    if w.shape != y.shape or (w < 0).any() or not np.isfinite(w).all() or w.sum() <= 0:
        raise ValueError("weights must be finite, non-negative and not all zero")
    off = np.zeros_like(y) if offset is None else np.asarray(offset, dtype=float)
    beta = np.zeros(X.shape[1])
    for _ in range(max_iter):
        eta = X @ beta + off
        mu = sigmoid(eta)
        v = np.clip(mu * (1 - mu), 1e-12, None) * w
        grad = X.T @ (w * (y - mu)) - ridge * beta
        hess = (X * v[:, None]).T @ X + ridge * np.eye(X.shape[1])
        try:
            step = np.linalg.solve(hess, grad)
        except np.linalg.LinAlgError as e:
            raise ValueError(f"singular information matrix: {e}") from None
        beta = beta + step
        if np.max(np.abs(step)) < tol:
            return beta
    raise ValueError("logistic regression did not converge (possible separation)")
