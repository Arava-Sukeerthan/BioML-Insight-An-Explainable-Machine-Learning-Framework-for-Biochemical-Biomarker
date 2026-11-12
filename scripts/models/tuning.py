"""Equal tuning budget (protocol draft section 12 item 2; research_integrity.md section 7).

Every method gets exactly the same number of candidate configurations (draft: 40), sampled
reproducibly from a search space fixed in the configuration file before any data are seen; the
penalised-LR grid must have the same size. Selection uses the lowest cross-validated log loss.
"""
from __future__ import annotations

import itertools
import math

import numpy as np

SPEC_TYPES = ("uniform", "loguniform", "int", "logint", "choice", "fixed")


def _validate_spec(name, spec):
    t = spec.get("type")
    if t not in SPEC_TYPES:
        raise ValueError(f"{name}: unknown parameter type {t!r}")
    if t in ("uniform", "loguniform", "int", "logint"):
        lo, hi = spec["low"], spec["high"]
        if not lo < hi:
            raise ValueError(f"{name}: low must be < high")
        if t in ("loguniform", "logint") and lo <= 0:
            raise ValueError(f"{name}: log scale needs low > 0")
    if t == "choice" and not spec.get("values"):
        raise ValueError(f"{name}: choice needs values")


def sample_configurations(space, budget, seed):
    """`budget` configurations sampled independently from `space` with numpy Generator(seed).
    space: {param: {"type": ..., ...}}. Deterministic for a given (space, budget, seed)."""
    if budget < 1:
        raise ValueError("budget must be >= 1")
    for name, spec in space.items():
        _validate_spec(name, spec)
    rng = np.random.default_rng(seed)
    configs = []
    for _ in range(budget):
        cfg = {}
        for name in sorted(space):
            s = space[name]
            t = s["type"]
            if t == "uniform":
                cfg[name] = float(rng.uniform(s["low"], s["high"]))
            elif t == "loguniform":
                cfg[name] = float(math.exp(rng.uniform(math.log(s["low"]), math.log(s["high"]))))
            elif t == "int":
                cfg[name] = int(rng.integers(s["low"], s["high"] + 1))
            elif t == "logint":
                cfg[name] = int(round(math.exp(rng.uniform(math.log(s["low"]), math.log(s["high"])))))
            elif t == "choice":
                cfg[name] = s["values"][int(rng.integers(0, len(s["values"])))]
            else:
                cfg[name] = s["value"]
        configs.append(cfg)
    return configs


def grid_configurations(grid):
    """Cartesian product of {param: [values]} in a fixed order (penalised-LR grid)."""
    names = sorted(grid)
    return [dict(zip(names, vals)) for vals in itertools.product(*(grid[n] for n in names))]


def configurations_for(method_cfg, budget, seed):
    """Configurations for one method, enforcing the equal budget for random search and grids."""
    if "grid" in method_cfg:
        configs = grid_configurations(method_cfg["grid"])
    else:
        configs = sample_configurations(method_cfg["search_space"], budget, seed)
    if len(configs) != budget:
        raise ValueError(f"method has {len(configs)} configurations; the equal budget is {budget}")
    return configs


def check_equal_budget(experiment_cfg):
    """Raise unless every method in the configuration uses exactly the common budget."""
    budget = experiment_cfg["tuning_budget"]
    for name, mcfg in experiment_cfg["methods"].items():
        n = len(grid_configurations(mcfg["grid"])) if "grid" in mcfg else mcfg.get("budget", budget)
        if n != budget:
            raise ValueError(f"{name}: {n} configurations, expected the common budget {budget}")
    return budget


def select_best(scores):
    """Index of the lowest score (ties: the earliest configuration). NaN scores are never selected."""
    s = np.asarray(scores, dtype=float)
    if np.isnan(s).all():
        raise ValueError("no configuration produced a valid score")
    s = np.where(np.isnan(s), np.inf, s)
    return int(np.argmin(s))
