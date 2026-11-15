"""Prespecified model comparisons (protocol draft section 13) on predictions for the same participants.

compare_to_reference: for each comparator, the paired bootstrap difference (comparator - reference)
of each metric on shared resamples, with Holm adjustment within each metric family (Q2: framework vs
the calibrated baselines). Which comparisons are primary, and the AUROC non-inferiority margin
(Q-054), are fixed in the frozen protocol, not here. numpy only; tested on synthetic predictions.
"""
from __future__ import annotations

import numpy as np

import metrics as M
from stats import bootstrap_indices, holm, paired_bootstrap

METRICS = {"auroc": M.auroc, "brier": M.brier, "ici": M.ici, "log_loss": M.log_loss}


def compare_to_reference(y, predictions, reference, metric_names=("auroc", "brier", "ici"),
                         n_boot=2000, seed=0, idx_sets=None, holm_within_metric=True):
    y = np.asarray(y).astype(int)
    if reference not in predictions:
        raise ValueError("reference model missing from predictions")
    for name, p in predictions.items():
        if np.asarray(p).shape != y.shape:
            raise ValueError(f"{name}: predictions do not match y")
    idx_sets = bootstrap_indices(y.size, n_boot, seed) if idx_sets is None else idx_sets
    others = [m for m in predictions if m != reference]
    out = {}
    for metric in metric_names:
        fn = METRICS[metric]
        rows = {m: paired_bootstrap(fn, y, predictions[m], predictions[reference], idx_sets=idx_sets) for m in others}
        if holm_within_metric and rows:
            adj = holm([rows[m]["p_value"] for m in others])
            for m, a in zip(others, adj):
                rows[m]["p_holm"] = float(a)
        out[metric] = rows
    return out


def non_inferior(diff_low, margin):
    """AUROC non-inferiority: lower CI bound of (comparator - reference) above -margin."""
    if margin <= 0:
        raise ValueError("margin must be positive (a researcher decision, Q-054)")
    return bool(diff_low > -margin)
