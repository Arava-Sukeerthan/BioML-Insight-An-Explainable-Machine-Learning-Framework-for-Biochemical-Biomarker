"""Result tables and calibration-curve data from harness outputs (protocol draft sections 14, 21).

* results_table(records, ...): Markdown table of internal (mean +/- SD over seeds) and temporal-
  validation metrics, one row per run record. Every table states the data label of its records;
  records with different labels (SYNTHETIC vs REAL) are never mixed in one table.
* calibration_curve(y, p, bins): binned calibration data (mean predicted, observed rate, count,
  Wilson 95% interval) for plotting; write_csv() stores it. Participant-level predictions are never
  written by this module; only aggregated bins are.
numpy only. Formatting does not round away information used in decisions: values are shown to 3
decimals and the raw records remain the source of truth.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

DEFAULT_METRICS = ("auroc", "brier", "intercept", "slope", "ici", "coverage_class_0", "coverage_class_1",
                   "mean_set_size")


def load_records(path):
    """Run records from a runs.jsonl file (one JSON object per line)."""
    out = []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            try:
                out.append(json.loads(line))
            except ValueError:
                raise ValueError(f"line {n} of {path} is not JSON") from None
    return out


def _fmt(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "—"
    return f"{v:.3f}"


def results_table(records, metrics=DEFAULT_METRICS, title=None, internal="internal_summary"):
    """internal: "internal_summary" (raw out-of-fold) or "internal_calibrated_summary" (out-of-fold
    after the D-cal calibrator; like-for-like with temporal validation). The choice is printed."""
    if internal not in ("internal_summary", "internal_calibrated_summary"):
        raise ValueError("internal must be internal_summary or internal_calibrated_summary")
    if not records:
        raise ValueError("no run records")
    labels = {r.get("data_label") for r in records}
    if len(labels) != 1:
        raise ValueError(f"records with different data labels cannot share a table: {sorted(map(str, labels))}")
    label = labels.pop()
    head = ["Model", "Seeds", "Config hash"] + [f"{m} (internal)" for m in metrics] + [f"{m} (temporal)" for m in metrics]
    lines = []
    if title:
        lines.append(f"**{title}**")
    lines.append(f"Internal estimate: `{internal}`.")
    lines.append(f"Data label: **{label}**." + (" Synthetic software-verification output; not evidence of model performance."
                                                 if label == "SYNTHETIC" else ""))
    lines.append("| " + " | ".join(head) + " |")
    lines.append("|" + "---|" * len(head))
    for r in records:
        summary = r.get(internal, {})
        temporal = r.get("temporal_validation", {})
        cells = [str(r.get("model")), str(len(r.get("seeds", []))), str(r.get("config_hash", ""))[:12]]
        for m in metrics:
            s = summary.get(m)
            cells.append("—" if s is None else f"{_fmt(s['mean'])} ± {_fmt(s['sd'])}")
        for m in metrics:
            cells.append(_fmt(temporal.get(m)))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def _wilson(k, n, z=1.959963984540054):
    if n == 0:
        return (float("nan"), float("nan"))
    ph = k / n
    den = 1 + z * z / n
    centre = (ph + z * z / (2 * n)) / den
    half = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / den
    return (centre - half, centre + half)


def calibration_curve(y, p, bins=10, strategy="uniform"):
    """Binned calibration data. strategy: "uniform" (equal-width) or "quantile" (equal-count).
    Empty bins are omitted. Returns a list of dicts."""
    y = np.asarray(y).astype(int)
    p = np.asarray(p, dtype=float)
    if y.shape != p.shape or y.size == 0 or not np.isin(y, (0, 1)).all():
        raise ValueError("y must be 0/1 and match p")
    if (p < 0).any() or (p > 1).any():
        raise ValueError("p must be probabilities")
    if strategy == "uniform":
        edges = np.linspace(0, 1, bins + 1)
    elif strategy == "quantile":
        edges = np.unique(np.quantile(p, np.linspace(0, 1, bins + 1)))
        edges[0], edges[-1] = 0.0, 1.0
    else:
        raise ValueError("strategy must be 'uniform' or 'quantile'")
    idx = np.clip(np.searchsorted(edges, p, side="right") - 1, 0, edges.size - 2)
    rows = []
    for b in range(edges.size - 1):
        m = idx == b
        n = int(m.sum())
        if n == 0:
            continue
        k = int(y[m].sum())
        lo, hi = _wilson(k, n)
        rows.append({"bin": b, "lower_edge": float(edges[b]), "upper_edge": float(edges[b + 1]), "n": n,
                     "mean_predicted": float(p[m].mean()), "observed_rate": k / n, "ci_low": lo, "ci_high": hi})
    return rows


def write_csv(rows, path, min_cell=0):
    """Write aggregated rows to CSV. min_cell > 0 refuses bins smaller than that count (small-cell
    protection for real-data outputs; the threshold is set by the frozen protocol)."""
    if not rows:
        raise ValueError("nothing to write")
    small = [r for r in rows if "n" in r and r["n"] < min_cell]
    if small:
        raise ValueError(f"{len(small)} bins have fewer than {min_cell} participants")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return path
