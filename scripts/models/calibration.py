"""Post-hoc probability calibration (framework component F3; protocol draft section 11.2), numpy only.

Platt scaling is the draft primary method; isotonic regression is sensitivity analysis S-14. Both
are fitted on the calibration split (D-cal) only and applied unchanged afterwards.
Software scaffolding; the protocol is a draft (not approved, not frozen).
"""
from __future__ import annotations

import numpy as np

from glm import EPS, fit_logistic, logit, sigmoid


class PlattCalibrator:
    """p_cal = sigmoid(a + b * s), with s = logit(probability) (input="probability") or a raw margin
    (input="margin")."""

    def __init__(self, input="probability"):
        if input not in ("probability", "margin"):
            raise ValueError("input must be 'probability' or 'margin'")
        self.input = input
        self.coef_ = None

    def _s(self, scores):
        scores = np.asarray(scores, dtype=float)
        return logit(scores) if self.input == "probability" else scores

    def fit(self, scores, y, sample_weight=None):
        s = self._s(scores)
        self.coef_ = fit_logistic(np.c_[np.ones_like(s), s], y, sample_weight)
        return self

    def predict(self, scores):
        if self.coef_ is None:
            raise RuntimeError("calibrator not fitted")
        s = self._s(scores)
        return sigmoid(self.coef_[0] + self.coef_[1] * s)


def pava(y, w=None):
    """Pool-adjacent-violators: the non-decreasing sequence closest to y in weighted least squares."""
    y = np.asarray(y, dtype=float)
    w = np.ones_like(y) if w is None else np.asarray(w, dtype=float)
    vals, wts, cnt = [], [], []
    for yi, wi in zip(y, w):
        vals.append(yi); wts.append(wi); cnt.append(1)
        while len(vals) > 1 and vals[-2] > vals[-1]:
            wt = wts[-2] + wts[-1]
            v = (vals[-2] * wts[-2] + vals[-1] * wts[-1]) / wt
            c = cnt[-2] + cnt[-1]
            vals[-2:], wts[-2:], cnt[-2:] = [v], [wt], [c]
    return np.repeat(vals, cnt)


class IsotonicCalibrator:
    """Monotone (non-decreasing) map from score to probability; constant beyond the fitted range.
    Output is clipped to [eps, 1 - eps] so that log loss stays finite."""

    def __init__(self, eps=1e-6):
        self.eps = eps
        self.x_ = None
        self.y_ = None

    def fit(self, scores, y, sample_weight=None):
        s = np.asarray(scores, dtype=float)
        y = np.asarray(y, dtype=float)
        if s.shape != y.shape or s.size == 0:
            raise ValueError("scores and y must be non-empty and of equal length")
        w = np.ones_like(y) if sample_weight is None else np.asarray(sample_weight, dtype=float)
        order = np.argsort(s, kind="mergesort")
        s, y, w = s[order], y[order], w[order]
        # merge tied scores first so that equal scores always get the same output
        uniq, start = np.unique(s, return_index=True)
        ends = np.r_[start[1:], s.size]
        ym = np.array([np.average(y[a:b], weights=w[a:b]) for a, b in zip(start, ends)])
        wm = np.array([w[a:b].sum() for a, b in zip(start, ends)])
        self.x_ = uniq
        self.y_ = pava(ym, wm)
        return self

    def predict(self, scores):
        if self.x_ is None:
            raise RuntimeError("calibrator not fitted")
        s = np.asarray(scores, dtype=float)
        idx = np.clip(np.searchsorted(self.x_, s, side="right") - 1, 0, self.x_.size - 1)
        return np.clip(self.y_[idx], self.eps, 1 - self.eps)


def make_calibrator(name):
    if name == "platt":
        return PlattCalibrator("probability")
    if name == "isotonic":
        return IsotonicCalibrator()
    if name == "none":
        return None
    raise ValueError(f"unknown calibration method {name!r}")


__all__ = ["PlattCalibrator", "IsotonicCalibrator", "pava", "make_calibrator", "EPS"]
