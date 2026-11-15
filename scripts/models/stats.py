"""Resampling statistics of the DRAFT protocol (section 15), numpy only: percentile bootstrap CIs,
paired bootstrap differences between models on the same resamples, a design-aware bootstrap that
resamples PSUs within strata (section 10), and the Holm adjustment.
"""
from __future__ import annotations

import numpy as np


def bootstrap_indices(n, n_boot, seed):
    rng = np.random.default_rng(seed)
    return rng.integers(0, n, size=(n_boot, n))


def cluster_bootstrap_indices(strata, psu, n_boot, seed):
    """Row indices for a bootstrap that resamples PSUs with replacement within each stratum."""
    strata, psu = np.asarray(strata), np.asarray(psu)
    rng = np.random.default_rng(seed)
    clusters = {}
    for i, key in enumerate(zip(strata.tolist(), psu.tolist())):
        clusters.setdefault(key, []).append(i)
    by_stratum = {}
    for (s, c), rows in clusters.items():
        by_stratum.setdefault(s, []).append(rows)
    out = []
    for _ in range(n_boot):
        rows = []
        for s in sorted(by_stratum):
            cl = by_stratum[s]
            for j in rng.integers(0, len(cl), size=len(cl)):
                rows.extend(cl[j])
        out.append(np.array(rows))
    return out


def _resample_values(metric, y, preds, idx_sets):
    vals = []
    for idx in idx_sets:
        yb = y[idx]
        if yb.min() == yb.max():          # a resample with one class: metric undefined, skipped
            continue
        vals.append([metric(yb, p[idx]) for p in preds])
    if not vals:
        raise ValueError("no valid bootstrap resample")
    return np.asarray(vals)


def bootstrap_ci(metric, y, p, n_boot=2000, seed=0, level=0.95, idx_sets=None):
    y, p = np.asarray(y), np.asarray(p)
    idx_sets = bootstrap_indices(y.size, n_boot, seed) if idx_sets is None else idx_sets
    vals = _resample_values(metric, y, [p], idx_sets)[:, 0]
    a = (1 - level) / 2
    return {"estimate": float(metric(y, p)), "low": float(np.quantile(vals, a)),
            "high": float(np.quantile(vals, 1 - a)), "n_valid": int(vals.size)}


def paired_bootstrap(metric, y, p_a, p_b, n_boot=2000, seed=0, level=0.95, idx_sets=None):
    """Difference metric(p_a) - metric(p_b) with a percentile CI and a two-sided bootstrap p-value,
    both models evaluated on the same resamples."""
    y = np.asarray(y)
    idx_sets = bootstrap_indices(y.size, n_boot, seed) if idx_sets is None else idx_sets
    vals = _resample_values(metric, y, [np.asarray(p_a), np.asarray(p_b)], idx_sets)
    d = vals[:, 0] - vals[:, 1]
    a = (1 - level) / 2
    p_two = min(1.0, 2 * min((d <= 0).mean(), (d >= 0).mean()))
    return {"difference": float(metric(y, np.asarray(p_a)) - metric(y, np.asarray(p_b))),
            "low": float(np.quantile(d, a)), "high": float(np.quantile(d, 1 - a)),
            "p_value": float(p_two), "n_valid": int(d.size)}


def holm(p_values):
    """Holm step-down adjusted p-values, returned in the input order."""
    p = np.asarray(p_values, dtype=float)
    m = p.size
    order = np.argsort(p, kind="mergesort")
    adj = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * p[i])
        adj[i] = min(1.0, running)
    return adj
