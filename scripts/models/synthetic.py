"""SYNTHETIC test data generators. NOT NHANES DATA AND NOT CLINICAL EVIDENCE.

Every value is drawn from arbitrary, hand-chosen distributions with a fixed seed. No parameter is
estimated from NHANES or any other participant-level data (D-040 (2)). Participant IDs start at
9,000,001, outside the NHANES SEQN ranges; every frame carries attrs["synthetic"] = True and a
SYNTHETIC_FIXTURE column, following tests/nhanes conventions. Use only for software tests.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

SYNTHETIC_ID_START = 9_000_001

_RANGES = {   # arbitrary positive ranges; deliberately NOT derived from any dataset
    "LBXSATSI": (5, 80), "LBXSASSI": (5, 80), "LBXSGTSI": (5, 120), "LBXSAPSI": (20, 200),
    "LBXSAL": (3, 5.5), "LBXSTP": (5.5, 9), "LBXSTB": (0.1, 2), "LBXSCR": (0.4, 1.6), "LBXSBU": (5, 30),
    "LBXSUA": (2, 9), "LBXTC": (100, 300), "LBDHDD": (25, 100), "TRIG": (30, 400),
    "LBXWBCSI": (3, 12), "LBDNENO": (1, 8), "LBDLYMNO": (0.5, 4), "LBXHGB": (10, 18), "LBXMCVSI": (75, 100),
    "LBXRDW": (11, 17), "LBXPLTSI": (120, 450), "URDACT": (1, 300),
    "BMXBMI": (17, 50), "BMXWAIST": (60, 150),
}


def _mark(df):
    df["SYNTHETIC_FIXTURE"] = True
    df.attrs["synthetic"] = True
    return df


def synthetic_feature_frame(n, seed, columns, missing_rate=0.03):
    """A synthetic DataFrame with the given predictor columns and random missingness."""
    rng = np.random.default_rng(seed)
    data = {}
    for c in columns:
        if c == "RIAGENDR":
            v = rng.integers(1, 3, size=n).astype(float)
        elif c == "RIDAGEYR":
            v = rng.integers(20, 81, size=n).astype(float)
        elif c in ("SBP", "DBP"):
            v = rng.uniform(90, 170, size=n) if c == "SBP" else rng.uniform(50, 100, size=n)
        else:
            lo, hi = _RANGES.get(c, (0, 1))
            v = rng.uniform(lo, hi, size=n)
        v[rng.random(n) < missing_rate] = np.nan
        data[c] = v
    return pd.DataFrame(data)


def synthetic_binary_task(n, seed, n_features=5, signal=1.0):
    """X (n, n_features) standard-normal and y ~ Bernoulli(sigmoid(signal * X[:, 0])). Returns X, y, p_true."""
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, n_features))
    p = 1 / (1 + np.exp(-signal * X[:, 0]))
    y = (rng.random(n) < p).astype(int)
    return X, y, p


def synthetic_component_frames(n, seed, period="2017-2020"):
    """Synthetic stand-ins for the NHANES component files of one period, keyed by component name.
    Values are arbitrary; the column names follow the codebooks so the assembly code can be tested."""
    rng = np.random.default_rng(seed)
    ids = np.arange(SYNTHETIC_ID_START, SYNTHETIC_ID_START + n) + (0 if period == "2017-2020" else 500_000)
    tg = "LBXTR" if period == "2017-2020" else "LBXTLG"
    fw = "WTSAFPRP" if period == "2017-2020" else "WTSAF2YR"
    seqn = pd.Series(ids, name="SEQN")
    demo = pd.DataFrame({"SEQN": ids, "RIDSTATR": rng.choice([1, 2], n, p=[0.1, 0.9]),
                         "RIDAGEYR": rng.integers(12, 81, n), "RIAGENDR": rng.integers(1, 3, n),
                         "RIDEXPRG": np.where(rng.random(n) < 0.03, 1.0, 2.0),
                         "SDMVSTRA": rng.integers(1, 6, n), "SDMVPSU": rng.integers(1, 3, n)})
    diq = pd.DataFrame({"SEQN": ids, "DIQ010": rng.choice([1, 2, 3, 9], n, p=[0.1, 0.8, 0.07, 0.03]).astype(float),
                        "DIQ070": np.where(rng.random(n) < 0.05, 1.0, 2.0), "DIQ160": np.where(rng.random(n) < 0.1, 1.0, 2.0)})
    ghb = pd.DataFrame({"SEQN": ids, "LBXGH": np.round(rng.uniform(4.5, 7.5, n), 1)})
    in_glu = rng.random(n) < 0.6
    glu = pd.DataFrame({"SEQN": ids[in_glu], fw: np.where(rng.random(in_glu.sum()) < 0.9, rng.uniform(1, 5e4, in_glu.sum()), 0.0),
                        "LBXGLU": np.round(rng.uniform(70, 140, in_glu.sum()))})
    glu.loc[rng.random(len(glu)) < 0.01, "LBXGLU"] = np.nan
    feats = synthetic_feature_frame(n, seed + 1, list(_RANGES))
    frames = {
        "DEMO": demo, "DIQ": diq, "GHB": ghb, "GLU": glu,
        "BIOPRO": pd.concat([seqn, feats[["LBXSATSI", "LBXSASSI", "LBXSGTSI", "LBXSAPSI", "LBXSAL", "LBXSTP",
                                          "LBXSTB", "LBXSCR", "LBXSBU", "LBXSUA"]]], axis=1),
        "TCHOL": pd.concat([seqn, feats[["LBXTC"]]], axis=1),
        "HDL": pd.concat([seqn, feats[["LBDHDD"]]], axis=1),
        "TRIGLY": pd.concat([seqn, feats[["TRIG"]].rename(columns={"TRIG": tg})], axis=1),
        "CBC": pd.concat([seqn, feats[["LBXWBCSI", "LBDNENO", "LBDLYMNO", "LBXHGB", "LBXMCVSI", "LBXRDW", "LBXPLTSI"]]], axis=1),
        "ALB_CR": pd.concat([seqn, feats[["URDACT"]]], axis=1),
        "BMX": pd.concat([seqn, feats[["BMXBMI", "BMXWAIST"]]], axis=1),
        "BPXO": pd.DataFrame({"SEQN": ids, **{f"BPXOSY{i}": rng.uniform(90, 170, n) for i in (1, 2, 3)},
                              **{f"BPXODI{i}": rng.uniform(50, 100, n) for i in (1, 2, 3)}}),
    }
    return {k: _mark(v) for k, v in frames.items()}
