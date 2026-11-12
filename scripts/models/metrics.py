"""Evaluation metrics M1-M10 of the DRAFT experimental protocol (section 14), numpy only.

All functions take observed labels y (0/1), predicted probabilities p and optional case weights w
(normalised internally; used for the secondary fasting-weighted analysis, section 10). They compute
numbers only; which metric is primary is fixed in the protocol, not here.
Software scaffolding: the protocol is a draft (not approved, not frozen); no real data are used.
"""
from __future__ import annotations

import numpy as np

from glm import EPS, fit_logistic, logit


def _check(y, p, w=None):
    y = np.asarray(y, dtype=float)
    p = np.asarray(p, dtype=float)
    if y.ndim != 1 or p.shape != y.shape or y.size == 0:
        raise ValueError("y and p must be non-empty 1-D arrays of equal length")
    if not np.isin(y, (0.0, 1.0)).all():
        raise ValueError("y must be 0/1")
    if not np.isfinite(p).all() or (p < 0).any() or (p > 1).any():
        raise ValueError("p must be probabilities in [0, 1]")
    w = np.ones_like(y) if w is None else np.asarray(w, dtype=float)
    if w.shape != y.shape or (w < 0).any() or not np.isfinite(w).all() or w.sum() <= 0:
        raise ValueError("weights must be finite, non-negative and not all zero")
    return y, p, w / w.sum() * w.size


def log_loss(y, p, w=None):
    y, p, w = _check(y, p, w)
    q = np.clip(p, EPS, 1 - EPS)
    return float(-np.average(y * np.log(q) + (1 - y) * np.log(1 - q), weights=w))


def auroc(y, p, w=None):
    """M1. (Weighted) probability that a random positive scores above a random negative; ties 1/2."""
    y, p, w = _check(y, p, w)
    if y.min() == y.max():
        raise ValueError("AUROC needs both classes")
    order = np.argsort(p, kind="mergesort")
    ps, ys, ws = p[order], y[order], w[order]
    total_neg = ws[ys == 0].sum()
    total_pos = ws[ys == 1].sum()
    neg_below = 0.0
    acc = 0.0
    i = 0
    while i < ps.size:
        j = i
        while j < ps.size and ps[j] == ps[i]:
            j += 1
        pos_w = ws[i:j][ys[i:j] == 1].sum()
        neg_w = ws[i:j][ys[i:j] == 0].sum()
        acc += pos_w * (neg_below + 0.5 * neg_w)
        neg_below += neg_w
        i = j
    return float(acc / (total_pos * total_neg))


def auprc(y, p, w=None):
    """M2. Average precision (step-wise area under the precision-recall curve); report it with the
    prevalence, which is its no-skill baseline."""
    y, p, w = _check(y, p, w)
    if y.sum() == 0:
        raise ValueError("AUPRC needs at least one positive")
    order = np.argsort(-p, kind="mergesort")
    ps, ys, ws = p[order], y[order], w[order]
    tp = np.cumsum(ws * ys)
    fp = np.cumsum(ws * (1 - ys))
    last = np.r_[np.nonzero(np.diff(ps))[0], ps.size - 1]   # end of each tie block
    tp, fp = tp[last], fp[last]
    precision = tp / (tp + fp)
    recall = tp / tp[-1]
    prev_recall = np.r_[0.0, recall[:-1]]
    return float(np.sum((recall - prev_recall) * precision))


def brier(y, p, w=None):
    """M3. Brier score."""
    y, p, w = _check(y, p, w)
    return float(np.average((p - y) ** 2, weights=w))


def scaled_brier(y, p, w=None):
    """M3. 1 - Brier / Brier of the prevalence-only prediction."""
    y, p, w = _check(y, p, w)
    prev = np.average(y, weights=w)
    ref = prev * (1 - prev)
    if ref == 0:
        raise ValueError("scaled Brier needs both classes")
    return float(1 - brier(y, p, w) / ref)


def calibration_intercept_slope(y, p, w=None):
    """M4 and M5. Slope: logistic regression of y on logit(p). Intercept (calibration-in-the-large):
    intercept-only logistic model with logit(p) as offset. Ideal values: intercept 0, slope 1."""
    y, p, w = _check(y, p, w)
    lp = logit(p)
    slope = fit_logistic(np.c_[np.ones_like(lp), lp], y, w)[1]
    intercept = fit_logistic(np.ones((lp.size, 1)), y, w, offset=lp)[0]
    return {"intercept": float(intercept), "slope": float(slope)}


def _lowess(x, y, w, frac):
    """Local linear regression with tricube kernel (no robustness iterations), evaluated at x."""
    n = x.size
    k = max(int(np.ceil(frac * n)), 3)
    fitted = np.empty(n)
    for i in range(n):
        d = np.abs(x - x[i])
        h = np.partition(d, k - 1)[k - 1]
        h = h if h > 0 else 1e-12
        kw = np.clip(1 - (d / h) ** 3, 0, None) ** 3 * w
        sw = kw.sum()
        mx = (kw * x).sum() / sw
        my = (kw * y).sum() / sw
        sxx = (kw * (x - mx) ** 2).sum()
        b = 0.0 if sxx <= 1e-15 else (kw * (x - mx) * (y - my)).sum() / sxx
        fitted[i] = my + b * (x[i] - mx)
    return np.clip(fitted, 0, 1)


def ici(y, p, w=None, frac=0.75):
    """M6. Integrated calibration index: weighted mean |p - smoothed observed rate at p|, smoothing y
    on p by local linear regression (span `frac`; the span is a protocol setting to be fixed at the
    freeze). O(n^2): adequate for n of a few thousand."""
    y, p, w = _check(y, p, w)
    smooth = _lowess(p, y, w, frac)
    return float(np.average(np.abs(p - smooth), weights=w))


def ece(y, p, w=None, bins=10):
    """M6 (secondary). Expected calibration error with equal-width bins."""
    y, p, w = _check(y, p, w)
    idx = np.minimum((p * bins).astype(int), bins - 1)
    total = 0.0
    for b in range(bins):
        m = idx == b
        if m.any():
            total += w[m].sum() * abs(np.average(y[m], weights=w[m]) - np.average(p[m], weights=w[m]))
    return float(total / w.sum())


def sensitivity_specificity(y, p, threshold, w=None):
    """M7. Positive prediction when p >= threshold."""
    y, p, w = _check(y, p, w)
    pred = p >= threshold
    pos, neg = y == 1, y == 0
    if not pos.any() or not neg.any():
        raise ValueError("sensitivity and specificity need both classes")
    return {"sensitivity": float(w[pred & pos].sum() / w[pos].sum()),
            "specificity": float(w[~pred & neg].sum() / w[neg].sum())}


def threshold_for_sensitivity(y, p, target=0.80):
    """Protocol section 12 item 6, read as: the LARGEST threshold t (a value of p) at which the
    sensitivity with rule p >= t is still >= target. (The draft's wording "smallest threshold" would
    always select the minimum score; this reading is flagged for the protocol freeze.)"""
    y, p, _ = _check(y, p)
    pos = np.sort(p[y == 1])[::-1]
    if pos.size == 0:
        raise ValueError("needs positives")
    k = int(np.ceil(target * pos.size))          # number of positives that must be at or above t
    return float(pos[k - 1])


def conformal_summary(sets, y):
    """M8 and M9. sets: (n, 2) boolean array, column c = class c included. Coverage (marginal and per
    class) and efficiency (mean set size, share of {0,1} and of empty sets)."""
    sets = np.asarray(sets, dtype=bool)
    y = np.asarray(y).astype(int)
    if sets.shape != (y.size, 2):
        raise ValueError("sets must be (n, 2)")
    covered = sets[np.arange(y.size), y]
    size = sets.sum(axis=1)
    out = {"coverage": float(covered.mean()), "mean_set_size": float(size.mean()),
           "share_both": float((size == 2).mean()), "share_empty": float((size == 0).mean())}
    for c in (0, 1):
        m = y == c
        out[f"coverage_class_{c}"] = float(covered[m].mean()) if m.any() else float("nan")
    return out


def net_benefit(y, p, thresholds, w=None):
    """M10 (secondary). Net benefit TP/n - FP/n * t/(1-t) for each threshold t in (0, 1)."""
    y, p, w = _check(y, p, w)
    out = {}
    n = w.sum()
    for t in thresholds:
        if not 0 < t < 1:
            raise ValueError("thresholds must be in (0, 1)")
        pred = p >= t
        tp = w[pred & (y == 1)].sum() / n
        fp = w[pred & (y == 0)].sum() / n
        out[float(t)] = float(tp - fp * t / (1 - t))
    return out


def all_metrics(y, p, threshold, sets=None, w=None):
    """Convenience bundle of M1-M9 for one set of predictions. threshold=None omits the threshold-
    dependent metrics (M7): a threshold is only meaningful on the probability scale it was fixed on."""
    res = {"auroc": auroc(y, p, w), "auprc": auprc(y, p, w), "prevalence": float(np.average(y, weights=w)),
           "brier": brier(y, p, w), "scaled_brier": scaled_brier(y, p, w), "log_loss": log_loss(y, p, w),
           **calibration_intercept_slope(y, p, w), "ici": ici(y, p, w), "ece": ece(y, p, w)}
    if threshold is not None:
        res.update(sensitivity_specificity(y, p, threshold, w), threshold=float(threshold))
    if sets is not None:
        res.update(conformal_summary(sets, y))
    return res
