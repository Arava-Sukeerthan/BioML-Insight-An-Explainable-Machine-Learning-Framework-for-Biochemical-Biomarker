"""Survey-design estimates and temporal-shift diagnostics (protocol draft sections 10 and 16).

* weighted_mean_taylor: weighted mean or prevalence with a design-based standard error by Taylor
  linearisation (with-replacement PSUs within strata; strata with a single PSU raise an error rather
  than being silently collapsed). Optional `domain` indicator for subpopulation estimates, as NCHS
  recommends (all non-zero-weight records + an indicator). Q-052 (software verification) remains
  open: compare with a reference implementation (e.g. R survey / SAS SURVEYMEANS) once installed.
* standardised_mean_difference and shift_diagnostics: prespecified development-vs-validation checks.
numpy only; tested on synthetic data.
"""
from __future__ import annotations

import numpy as np


def weighted_mean_taylor(x, w, strata, psu, domain=None):
    """Weighted mean of x and its Taylor-linearised SE (with-replacement PSUs within strata).

    domain: optional 0/1 indicator of the analysis subpopulation. NCHS guidance (NHANES variance
    estimation tutorial, wwwn.cdc.gov, read 2026-11-12) is to pass ALL records with a non-zero weight
    and a subpopulation indicator, not the subset alone, so that every design PSU contributes to the
    variance. With domain given, x may be NaN outside the domain (it is not used there); records
    outside the domain contribute zero to the linearised variable but keep their stratum/PSU.
    domain=None is the previous behaviour (the whole input is the analysis population)."""
    x, w = np.asarray(x, dtype=float), np.asarray(w, dtype=float)
    strata, psu = np.asarray(strata), np.asarray(psu)
    if not (x.shape == w.shape == strata.shape == psu.shape) or x.size == 0:
        raise ValueError("x, w, strata and psu must be equal-length and non-empty")
    d = np.ones(x.shape, dtype=bool) if domain is None else np.asarray(domain).astype(bool)
    if d.shape != x.shape:
        raise ValueError("domain must have the same length as x")
    if (w < 0).any() or np.isnan(x[d]).any() or w[d].sum() <= 0:
        raise ValueError("x must be complete in the domain and weights non-negative with a positive domain sum")
    xd = np.where(d, x, 0.0)
    wd = np.where(d, w, 0.0)
    W = wd.sum()
    est = float((wd * xd).sum() / W)
    z = wd * (xd - est) / W                     # linearised variable of the (domain) ratio estimator
    var = 0.0
    for h in np.unique(strata):
        mh = strata == h
        totals = np.array([z[mh & (psu == c)].sum() for c in np.unique(psu[mh])])
        nh = totals.size
        if nh < 2:
            raise ValueError(f"stratum {h!r} has a single PSU; variance not estimable without a collapsing rule")
        var += nh / (nh - 1) * ((totals - totals.mean()) ** 2).sum()
    return {"estimate": est, "se": float(np.sqrt(var))}


def standardised_mean_difference(a, b):
    """(mean_b - mean_a) / pooled SD, ignoring missing values."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a, b = a[~np.isnan(a)], b[~np.isnan(b)]
    if a.size < 2 or b.size < 2:
        raise ValueError("need at least two observed values in each group")
    pooled = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    return float("nan") if pooled == 0 else float((b.mean() - a.mean()) / pooled)


def shift_diagnostics(dev_frame, val_frame, y_dev, y_val):
    """SMD of every shared column and the outcome-prevalence difference (validation - development)."""
    cols = [c for c in dev_frame.columns if c in val_frame.columns]
    return {"smd": {c: standardised_mean_difference(dev_frame[c], val_frame[c]) for c in cols},
            "prevalence_dev": float(np.mean(y_dev)), "prevalence_val": float(np.mean(y_val)),
            "prevalence_difference": float(np.mean(y_val) - np.mean(y_dev))}
