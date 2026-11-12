"""Reproducible data partitioning (protocol draft section 12; sensitivity S-13), numpy only.

Every split is a pure function of the labels (or groups) and an integer seed, and is validated with
the leakage safeguards of scripts/nhanes/safeguards.py before it is returned.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "nhanes"))
import safeguards as sg  # noqa: E402


def derive_seeds(master_seed, n):
    """n reproducible, distinct 32-bit seeds derived from one master seed (numpy SeedSequence)."""
    if n < 1:
        raise ValueError("n must be >= 1")
    states = np.random.SeedSequence(int(master_seed)).generate_state(n)
    seeds = [int(s) for s in states]
    if len(set(seeds)) != n:
        raise ValueError("seed collision")
    return seeds


def stratified_split(y, holdout_fraction, seed):
    """Split row indices into (train, holdout) with the outcome proportion preserved per class
    (D-train 80% / D-cal 20% in the draft protocol)."""
    y = np.asarray(y)
    if not 0 < holdout_fraction < 1:
        raise ValueError("holdout_fraction must be in (0, 1)")
    rng = np.random.default_rng(seed)
    train, hold = [], []
    for c in np.unique(y):
        idx = np.nonzero(y == c)[0]
        idx = idx[rng.permutation(idx.size)]
        k = int(round(holdout_fraction * idx.size))
        if k == 0 or k == idx.size:
            raise ValueError(f"class {c!r} too small for the requested split")
        hold.extend(idx[:k].tolist())
        train.extend(idx[k:].tolist())
    train, hold = sorted(train), sorted(hold)
    sg.check_partitions({"train": train, "holdout": hold}, expected_ids=range(y.size))
    return np.array(train), np.array(hold)


def stratified_kfold(y, k, seed):
    """K folds as (train_idx, test_idx); each class spread evenly over the folds."""
    y = np.asarray(y)
    if k < 2:
        raise ValueError("k must be >= 2")
    rng = np.random.default_rng(seed)
    fold_of = np.empty(y.size, dtype=int)
    for c in np.unique(y):
        idx = np.nonzero(y == c)[0]
        if idx.size < k:
            raise ValueError(f"class {c!r} has fewer than k={k} members")
        idx = idx[rng.permutation(idx.size)]
        fold_of[idx] = np.arange(idx.size) % k
    folds = [(np.nonzero(fold_of != f)[0].tolist(), np.nonzero(fold_of == f)[0].tolist()) for f in range(k)]
    sg.check_folds(folds, y.size, require_partition=True)
    return [(np.array(a), np.array(b)) for a, b in folds]


def grouped_kfold(groups, k, seed):
    """K folds that keep every group (e.g. stratum x PSU, sensitivity S-13) inside one test fold."""
    groups = np.asarray(groups)
    uniq = np.unique(groups)
    if uniq.size < k:
        raise ValueError("fewer groups than folds")
    rng = np.random.default_rng(seed)
    perm = uniq[rng.permutation(uniq.size)]
    fold_of_group = {g: i % k for i, g in enumerate(perm)}
    fold_of = np.array([fold_of_group[g] for g in groups])
    folds = [(np.nonzero(fold_of != f)[0].tolist(), np.nonzero(fold_of == f)[0].tolist()) for f in range(k)]
    sg.check_folds(folds, groups.size, ids=None, require_partition=True)
    return [(np.array(a), np.array(b)) for a, b in folds]
