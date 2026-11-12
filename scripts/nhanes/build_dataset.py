"""Analytic-dataset assembly for the DRAFT experimental protocol (sections 4-10). SCAFFOLDING.

Status: software only. It has been run only on SYNTHETIC component frames (tests/nhanes). Reading
the real NHANES files requires an explicit authorisation reference (load_period_files); none exists
yet (D-014 and D-019 PENDING). Nothing here fits a model.

What it does, for one period:
  * merges the component frames on SEQN (one row per participant, checked);
  * derives in_fasting_glucose_file from the GLU merge and the mean of the available oscillometric
    blood-pressure readings (SBP, DBP);
  * maps the period-specific triglyceride variable to the common name TRIG (LBXTR 2017-2020;
    LBXTLG 2021-2023);
  * applies the eligibility cascade E0-E8 (safeguards.eligibility_cascade, shared with the
    descriptive-count script);
  * derives the outcome (primary or a prespecified sensitivity definition; never imputed);
  * returns predictor groups A (21 biochemical), C (6 clinical) and B (A + C), leakage-checked.
Harmonisation: "S-08" (reference in the draft revision-3 proposal: values as released) or "S-09b"
(CDC backward equations at cycle level for TRIG, ALT, ALP, GGT, BUN, total bilirubin; 2021-2023
only). The equations are transcribed from protocol Appendix B and are NOT yet re-checked against
the CDC pages (AB-9). Urine albumin-to-creatinine recomputation in S-09b is blocked until Q-046 is
decided. Which harmonisation is primary is a researcher decision (FA-5).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import warnings
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

import safeguards as sg

PERIODS = {
    "2017-2020": {"file": lambda c: "P_" + c, "fasting_weight": "WTSAFPRP", "tg": "LBXTR"},
    "2021-2023": {"file": lambda c: c + "_L", "fasting_weight": "WTSAF2YR", "tg": "LBXTLG"},
}
COMPONENTS = ("DEMO", "DIQ", "GHB", "GLU", "TCHOL", "HDL", "TRIGLY", "BIOPRO", "CBC", "ALB_CR", "BMX", "BPXO")

GROUP_A = ["LBXSATSI", "LBXSASSI", "LBXSGTSI", "LBXSAPSI", "LBXSTB", "LBXSAL", "LBXSTP",      # liver
           "LBXSCR", "LBXSBU", "LBXSUA", "URDACT",                                             # kidney, urate
           "LBXTC", "LBDHDD", "TRIG",                                                          # lipids
           "LBXWBCSI", "LBDNENO", "LBDLYMNO", "LBXHGB", "LBXMCVSI", "LBXRDW", "LBXPLTSI"]      # blood count
GROUP_C = ["RIDAGEYR", "RIAGENDR", "BMXBMI", "BMXWAIST", "SBP", "DBP"]
GROUPS = {"A": GROUP_A, "B": GROUP_A + GROUP_C, "C": GROUP_C}

OUTCOMES = ("primary", "S-01", "S-02", "S-03", "S-15a")

# Protocol Appendix B, backward equations (2021-2023 value -> 2017-2020 scale); AB-9 re-check pending.
BACKWARD = {
    "TRIG": (-12.19, 0.9785),
    "LBXSATSI": (-1.529, 1.035),
    "LBXSAPSI": (0.6098, 0.9041),
    "LBXSGTSI": (0.9735, 0.9444),
    "LBXSBU": (0.09386, 1.021),
    "LBXSTB": (0.01793, 1.012),
}


class DatasetError(ValueError):
    pass


@dataclass
class AnalyticDataset:
    period: str
    ids: np.ndarray
    y: np.ndarray
    features: pd.DataFrame          # all group-B columns
    fasting_weight: np.ndarray
    strata: np.ndarray
    psu: np.ndarray
    cascade: dict
    outcome_definition: str
    harmonisation: str
    synthetic: bool
    notes: list = field(default_factory=list)

    def matrix(self, group):
        if group not in GROUPS:
            raise DatasetError(f"unknown predictor group {group!r}")
        cols = GROUPS[group]
        sg.check_predictors(cols)
        return self.features[cols].copy()


def outcome(hba1c, fpg, definition="primary"):
    """Outcome labels (protocol section 5). Both measurements must be present (never imputed)."""
    h = pd.Series(hba1c, dtype=float).reset_index(drop=True)
    g = pd.Series(fpg, dtype=float).reset_index(drop=True)
    if h.isna().any() or g.isna().any():
        raise DatasetError("outcome needs both HbA1c and FPG for every participant (E5)")
    if definition == "primary":
        y = (h >= 5.7) | (g >= 100)
    elif definition == "S-01":
        y = h >= 5.7
    elif definition == "S-02":
        y = g >= 100
    elif definition == "S-03":
        y = (h >= 5.7) | (g >= 110)
    elif definition == "S-15a":
        y = (h >= 5.7) & (g >= 100)
    else:
        raise DatasetError(f"unknown outcome definition {definition!r}")
    return y.astype(int).to_numpy()


def harmonise(df, period, mode="S-08", urdact_policy="pending"):
    """Apply the harmonisation mode to the predictor columns of one period (copy returned)."""
    df = df.copy()
    if mode == "S-08":
        return df
    if mode != "S-09b":
        raise DatasetError(f"unknown harmonisation mode {mode!r}")
    if period == "2017-2020":
        return df
    for col, (a, b) in BACKWARD.items():
        df[col] = a + b * df[col]
    if urdact_policy == "pending":
        raise DatasetError("S-09b urine albumin-to-creatinine recomputation is blocked until Q-046 is decided")
    if urdact_policy != "unadjusted":
        raise DatasetError(f"unknown urdact_policy {urdact_policy!r}")
    return df


def _one_row_each(frame, name):
    if "SEQN" not in frame.columns:
        raise DatasetError(f"{name}: no SEQN column")
    sg.check_unique_participants(frame["SEQN"], f"SEQN values in {name}")


def assemble_period(frames, period, outcome_definition="primary", harmonisation="S-08", urdact_policy="pending"):
    """Build the analytic dataset of one period from its component frames ({component: DataFrame})."""
    if period not in PERIODS:
        raise DatasetError(f"unknown period {period!r}")
    missing = [c for c in COMPONENTS if c not in frames]
    if missing:
        raise DatasetError(f"missing component frames: {missing}")
    cfg = PERIODS[period]
    fw, tg = cfg["fasting_weight"], cfg["tg"]
    for name in COMPONENTS:
        _one_row_each(frames[name], name)
    synthetic = all(bool(frames[c].attrs.get("synthetic")) for c in COMPONENTS)

    d = frames["DEMO"][["SEQN", "RIDSTATR", "RIDAGEYR", "RIAGENDR", "RIDEXPRG", "SDMVSTRA", "SDMVPSU"]]
    d = d.merge(frames["DIQ"][["SEQN", "DIQ010", "DIQ070"]], on="SEQN", how="left")
    d = d.merge(frames["GHB"][["SEQN", "LBXGH"]], on="SEQN", how="left")
    d = d.merge(frames["GLU"][["SEQN", fw, "LBXGLU"]], on="SEQN", how="left", indicator="_glu")
    d["in_fasting_glucose_file"] = (d.pop("_glu") == "both").astype(bool)
    for comp in ("BIOPRO", "TCHOL", "HDL", "TRIGLY", "CBC", "ALB_CR", "BMX"):
        cols = [c for c in frames[comp].columns if c not in ("SEQN", "SYNTHETIC_FIXTURE")]
        d = d.merge(frames[comp][["SEQN"] + cols], on="SEQN", how="left")
    bp = frames["BPXO"]
    bp = pd.DataFrame({"SEQN": bp["SEQN"],
                       "SBP": bp[["BPXOSY1", "BPXOSY2", "BPXOSY3"]].mean(axis=1, skipna=True),
                       "DBP": bp[["BPXODI1", "BPXODI2", "BPXODI3"]].mean(axis=1, skipna=True)})
    d = d.merge(bp, on="SEQN", how="left")
    if tg not in d.columns:
        raise DatasetError(f"triglyceride variable {tg} missing for {period}")
    d = d.rename(columns={tg: "TRIG"})
    absent = [c for c in GROUP_A + GROUP_C if c not in d.columns]
    if absent:
        raise DatasetError(f"predictor columns missing after merge: {absent}")

    counts, mask = sg.eligibility_cascade(d, fw)
    a = d[mask].reset_index(drop=True)
    y = outcome(a["LBXGH"], a["LBXGLU"], outcome_definition)
    feats = harmonise(a[GROUP_A + GROUP_C], period, harmonisation, urdact_policy)
    sg.check_predictors(list(feats.columns))
    return AnalyticDataset(period=period, ids=a["SEQN"].to_numpy(), y=y, features=feats.reset_index(drop=True),
                           fasting_weight=a[fw].to_numpy(dtype=float), strata=a["SDMVSTRA"].to_numpy(),
                           psu=a["SDMVPSU"].to_numpy(), cascade=counts, outcome_definition=outcome_definition,
                           harmonisation=harmonisation, synthetic=synthetic)


def check_period_pair(development, validation):
    """Development and temporal-validation datasets must not share participants (protocol 3.3)."""
    sg.check_disjoint_participants(list(development.ids), list(validation.ids))
    if development.harmonisation != validation.harmonisation or \
            development.outcome_definition != validation.outcome_definition:
        raise DatasetError("development and validation must use the same outcome and harmonisation")


def load_period_files(raw_dir, period, expected_sha256, authorisation):
    """Read the real component files of one period after verifying each SHA-256.
    Requires a non-empty researcher authorisation reference (e.g. a decision-log ID); there is none
    yet, so this is not called anywhere. expected_sha256: {"<period>/<file>": sha256}."""
    if not authorisation or not str(authorisation).strip():
        raise DatasetError("reading real NHANES files needs an explicit researcher authorisation reference")
    raw_dir = Path(raw_dir)
    frames = {}
    for comp in COMPONENTS:
        fname = PERIODS[period]["file"](comp)
        path = raw_dir / period / (fname + ".xpt")
        key = f"{period}/{fname}"
        if key not in expected_sha256:
            raise DatasetError(f"no expected SHA-256 for {key}")
        if not path.is_file():
            raise DatasetError(f"missing file {path}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected_sha256[key]:
            raise DatasetError(f"SHA-256 mismatch for {path}")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df = pd.read_sas(path, format="xport")
        num = df.select_dtypes("number").columns
        df[num] = df[num].mask(df[num].abs() < 1e-70, 0.0)   # SAS XPORT stores 0 as ~5.4e-79
        frames[comp] = df
    return frames


REPO = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO / "data" / "derived" / "nhanes"


def _git_ignored(path):
    """True if Git ignores `path` (participant-level outputs must never be committable)."""
    try:
        r = subprocess.run(["git", "check-ignore", "-q", str(path)], cwd=REPO, capture_output=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return False
    return r.returncode == 0


def write_outputs(ds, out_dir):
    """Write one period's analytic dataset: participant-level CSV (Git-ignored location required) and
    an aggregate JSON summary (cascade counts, sizes, prevalence)."""
    out_dir = Path(out_dir)
    probe = out_dir / "participant_level.probe"
    if not _git_ignored(probe):
        raise DatasetError(f"{out_dir} is not Git-ignored; participant-level data cannot be written there")
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = f"{ds.period}_{ds.outcome_definition}_{ds.harmonisation}"
    frame = ds.features.copy()
    frame.insert(0, "y", ds.y)
    frame.insert(0, "SEQN", ds.ids)
    frame["fasting_weight"] = ds.fasting_weight
    frame["SDMVSTRA"], frame["SDMVPSU"] = ds.strata, ds.psu
    data_path = out_dir / f"analytic_{tag}.csv"
    frame.to_csv(data_path, index=False)
    summary = {"period": ds.period, "outcome_definition": ds.outcome_definition, "harmonisation": ds.harmonisation,
               "synthetic": ds.synthetic, "cascade": ds.cascade, "n": int(ds.y.size),
               "n_positive": int(ds.y.sum()), "complete_cases": {g: int(ds.features[c].notna().all(axis=1).sum())
                                                                 for g, c in GROUPS.items()},
               "data_sha256": hashlib.sha256(data_path.read_bytes()).hexdigest()}
    (out_dir / f"summary_{tag}.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return data_path, summary


def main(argv=None):
    """CLI: build the analytic dataset of one period from the real files. Needs --authorisation."""
    ap = argparse.ArgumentParser(description="Build the NHANES analytic dataset (draft protocol sections 4-10).")
    ap.add_argument("--period", required=True, choices=sorted(PERIODS))
    ap.add_argument("--authorisation", required=True, help="decision-log ID authorising real-data access")
    ap.add_argument("--raw-dir", default=str(REPO / "data" / "raw" / "nhanes"))
    ap.add_argument("--outcome", default="primary", choices=OUTCOMES)
    ap.add_argument("--harmonisation", default="S-08", choices=("S-08", "S-09b"))
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT))
    ap.add_argument("--expect-n", type=int, help="expected E8 analytic N (stops on a mismatch)")
    a = ap.parse_args(argv)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from descriptive_counts import EXPECTED_SHA256
    try:
        frames = load_period_files(a.raw_dir, a.period, EXPECTED_SHA256, a.authorisation)
        ds = assemble_period(frames, a.period, a.outcome, a.harmonisation)
        if a.expect_n is not None and ds.cascade["E8_analytic_N"] != a.expect_n:
            raise DatasetError(f"E8 analytic N {ds.cascade['E8_analytic_N']} != expected {a.expect_n}")
        path, summary = write_outputs(ds, a.out_dir)
    except (DatasetError, sg.LeakageError) as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    print(json.dumps({k: summary[k] for k in ("period", "n", "n_positive", "cascade")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
