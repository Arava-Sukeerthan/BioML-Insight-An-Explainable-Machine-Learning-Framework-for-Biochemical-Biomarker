"""Explanation-stability measures for framework component F5 (protocol draft sections 11.2 and 17).

The attributions themselves (TreeSHAP on the uncalibrated F2 margin) need the `shap` and `xgboost`
packages, which are not installed (D-002); this module implements the model-independent part: global
importance from an attribution matrix, rank stability across bootstrap refits and between periods,
and sign agreement with penalised-LR coefficients. Explanations describe the model, not causation.
numpy only; tested on synthetic matrices.
"""
from __future__ import annotations

import numpy as np


def _ranks(v):
    """Average ranks (ties share the mean rank), 1 = smallest."""
    v = np.asarray(v, dtype=float)
    order = np.argsort(v, kind="mergesort")
    ranks = np.empty(v.size)
    sv = v[order]
    i = 0
    while i < v.size:
        j = i
        while j + 1 < v.size and sv[j + 1] == sv[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    return ranks


def spearman(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if a.shape != b.shape or a.size < 2:
        raise ValueError("need two equal-length vectors with at least 2 values")
    ra, rb = _ranks(a), _ranks(b)
    if ra.std() == 0 or rb.std() == 0:
        raise ValueError("Spearman correlation undefined for a constant vector")
    return float(np.corrcoef(ra, rb)[0, 1])


def global_importance(attributions):
    """Mean absolute attribution per feature from an (n_cases, n_features) matrix."""
    a = np.asarray(attributions, dtype=float)
    if a.ndim != 2 or not np.isfinite(a).all():
        raise ValueError("attributions must be a finite 2-D matrix")
    return np.abs(a).mean(axis=0)


def mean_direction(attributions, X):
    """Sign of the association between each feature value and its attribution (Spearman per column);
    0 where undefined (constant column)."""
    a, X = np.asarray(attributions, dtype=float), np.asarray(X, dtype=float)
    out = []
    for j in range(a.shape[1]):
        try:
            out.append(np.sign(spearman(X[:, j], a[:, j])))
        except ValueError:
            out.append(0.0)
    return np.array(out)


def rank_stability(importances):
    """Mean and minimum pairwise Spearman correlation between global-importance vectors of repeated
    refits (rows = refits, columns = features); protocol: 50 bootstrap refits."""
    imp = np.asarray(importances, dtype=float)
    if imp.ndim != 2 or imp.shape[0] < 2:
        raise ValueError("need at least two importance vectors")
    vals = [spearman(imp[i], imp[j]) for i in range(imp.shape[0]) for j in range(i + 1, imp.shape[0])]
    return {"mean_spearman": float(np.mean(vals)), "min_spearman": float(np.min(vals)), "pairs": len(vals)}


def top_k_overlap(imp_a, imp_b, k):
    """Share of the top-k features (by importance) common to two importance vectors."""
    a, b = np.argsort(-np.asarray(imp_a))[:k], np.argsort(-np.asarray(imp_b))[:k]
    return len(set(a.tolist()) & set(b.tolist())) / k


def sign_agreement(directions, lr_coefficients):
    """Share of features (non-zero in both) whose attribution direction matches the sign of the
    penalised-LR coefficient on the same standardised features."""
    d, c = np.sign(np.asarray(directions, dtype=float)), np.sign(np.asarray(lr_coefficients, dtype=float))
    m = (d != 0) & (c != 0)
    if not m.any():
        raise ValueError("no feature with a non-zero direction and coefficient")
    return float((d[m] == c[m]).mean())
