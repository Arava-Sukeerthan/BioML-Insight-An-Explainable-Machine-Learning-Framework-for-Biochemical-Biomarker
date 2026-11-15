"""Class-conditional (Mondrian) split conformal prediction for a binary outcome (framework component
F4; protocol draft section 11.2), numpy only.

Nonconformity score for candidate label c: 1 - p_c, with p_1 = p and p_0 = 1 - p. For each class c,
the threshold q_c is the ceil((n_c + 1)(1 - alpha))-th smallest score among the calibration cases with
label c; if that rank exceeds n_c, q_c = +inf (class c always included). Under exchangeability within
each class this gives class-conditional coverage >= 1 - alpha. Fitted on D-cal only.
Software scaffolding; the protocol is a draft (not approved, not frozen).
"""
from __future__ import annotations

import math

import numpy as np


class MondrianConformal:
    def __init__(self, alpha=0.10):
        if not 0 < alpha < 1:
            raise ValueError("alpha must be in (0, 1)")
        self.alpha = alpha
        self.q_ = None
        self.n_ = None

    def fit(self, p_cal, y_cal):
        p = np.asarray(p_cal, dtype=float)
        y = np.asarray(y_cal).astype(int)
        if p.shape != y.shape or not np.isin(y, (0, 1)).all():
            raise ValueError("p_cal and y_cal must align; y must be 0/1")
        if (p < 0).any() or (p > 1).any() or not np.isfinite(p).all():
            raise ValueError("p_cal must be probabilities")
        self.q_, self.n_ = {}, {}
        for c in (0, 1):
            pc = p[y == c] if c == 1 else 1 - p[y == c]
            scores = np.sort(1 - pc)
            n = scores.size
            k = math.ceil((n + 1) * (1 - self.alpha))
            self.n_[c] = n
            self.q_[c] = float("inf") if k > n else float(scores[k - 1])
        return self

    def predict_sets(self, p):
        if self.q_ is None:
            raise RuntimeError("conformal predictor not fitted")
        p = np.asarray(p, dtype=float)
        return np.c_[(1 - (1 - p)) <= self.q_[0], (1 - p) <= self.q_[1]]
