"""Deterministic execution settings and run records (protocol draft section 22; D-002 PROPOSED)."""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import random
import subprocess
import sys
from pathlib import Path

import numpy as np

THREAD_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")
PACKAGES = ("numpy", "pandas", "scipy", "scikit-learn", "xgboost", "lightgbm", "shap", "statsmodels", "matplotlib")


def set_deterministic(seed, threads=1):
    """Seed the standard-library and legacy numpy RNGs and set single-threaded BLAS variables.
    Thread variables only take effect for libraries loaded afterwards; they are also recorded so a
    run can be repeated under the same settings. Code in scripts/models uses explicit numpy
    Generators seeded from the configuration, so results do not depend on global state."""
    random.seed(seed)
    np.random.seed(seed % (2 ** 32))
    for v in THREAD_VARS:
        os.environ[v] = str(threads)
    return {"seed": seed, "threads": threads, "PYTHONHASHSEED": os.environ.get("PYTHONHASHSEED")}


def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def config_hash(config):
    return hashlib.sha256(canonical_json(config).encode("utf-8")).hexdigest()


def data_fingerprint(X, y):
    """SHA-256 over the feature matrix and labels (values and shape), for the run record."""
    h = hashlib.sha256()
    for a in (np.asarray(X, dtype=float), np.asarray(y, dtype=float)):
        h.update(str(a.shape).encode())
        h.update(np.ascontiguousarray(a).tobytes())
    return h.hexdigest()


def git_commit(repo=None):
    repo = repo or Path(__file__).resolve().parents[2]
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, timeout=30)
        dirty = subprocess.run(["git", "status", "--porcelain"], cwd=repo, capture_output=True, text=True, timeout=30)
        return {"commit": r.stdout.strip() or "unknown", "dirty": bool(dirty.stdout.strip())}
    except (OSError, subprocess.SubprocessError):
        return {"commit": "unknown", "dirty": None}


def environment_record():
    pkgs = {}
    for p in PACKAGES:
        try:
            pkgs[p] = importlib.metadata.version(p)
        except importlib.metadata.PackageNotFoundError:
            pkgs[p] = None
    return {"python": sys.version.split()[0], "implementation": platform.python_implementation(),
            "platform": platform.platform(), "machine": platform.machine(), "cpu_count": os.cpu_count(),
            "packages": pkgs, "thread_env": {v: os.environ.get(v) for v in THREAD_VARS},
            "PYTHONHASHSEED": os.environ.get("PYTHONHASHSEED")}
