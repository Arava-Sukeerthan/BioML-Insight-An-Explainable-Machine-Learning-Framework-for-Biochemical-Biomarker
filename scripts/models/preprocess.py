"""In-fold preprocessing (framework component F1; protocol draft section 9), pandas/numpy only.

Every statistic (medians, modes, missingness shares, means and SDs) is learnt in fit() from the
training rows only and applied unchanged by transform(). Steps, in order:
  1. leakage check of the input columns (scripts/nhanes/safeguards.py, protocol section 7);
  2. prespecified natural-log(x + 1) transforms for right-skewed analytes;
  3. binary coding of sex (RIAGENDR: 1 male -> 0, 2 female -> 1);
  4. missingness indicators for variables with > 5% missing in the training rows;
  5. median imputation (continuous) and mode imputation (binary);
  6. optional standardisation (only for scale-sensitive learners: LR, SVM, MLP, k-NN).
No outliers are removed and no resampling or class weighting is applied (section 9 items 7-8).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "nhanes"))
import safeguards as sg  # noqa: E402

DEFAULT_LOG1P = ("TRIG", "URDACT", "LBXSATSI", "LBXSASSI", "LBXSGTSI")
DEFAULT_BINARY = {"RIAGENDR": {1: 0.0, 2: 1.0}}


class PreprocessingError(ValueError):
    pass


class InFoldPreprocessor:
    def __init__(self, columns, log1p=DEFAULT_LOG1P, binary=None, indicator_threshold=0.05, scale=False):
        self.columns = list(columns)
        if len(set(self.columns)) != len(self.columns):
            raise PreprocessingError("duplicated input columns")
        sg.check_predictors(self.columns)
        self.log1p = [c for c in log1p if c in self.columns]
        self.binary = {k: v for k, v in (DEFAULT_BINARY if binary is None else binary).items() if k in self.columns}
        self.indicator_threshold = indicator_threshold
        self.scale = scale
        self.fitted_ = False

    def _base(self, X):
        if not isinstance(X, pd.DataFrame):
            raise PreprocessingError("X must be a pandas DataFrame")
        missing = [c for c in self.columns if c not in X.columns]
        extra = [c for c in X.columns if c not in self.columns]
        if missing or extra:
            raise PreprocessingError(f"column mismatch: missing {missing}, unexpected {extra}")
        Z = X[self.columns].astype(float).copy()
        for c in self.log1p:
            v = Z[c]
            if (v.dropna() < 0).any():
                raise PreprocessingError(f"{c}: negative values cannot be log1p-transformed")
            Z[c] = np.log1p(v)
        for c, mapping in self.binary.items():
            bad = Z[c].dropna()[~Z[c].dropna().isin(list(mapping))]
            if not bad.empty:
                raise PreprocessingError(f"{c}: unexpected codes {sorted(set(bad.tolist()))[:5]}")
            Z[c] = Z[c].map(mapping)
        return Z

    def fit(self, X):
        Z = self._base(X)
        if len(Z) == 0:
            raise PreprocessingError("no training rows")
        frac = Z.isna().mean()
        self.indicators_ = [c for c in self.columns if frac[c] > self.indicator_threshold]
        self.fill_ = {}
        for c in self.columns:
            obs = Z[c].dropna()
            if obs.empty:
                raise PreprocessingError(f"{c}: no observed value in the training rows")
            self.fill_[c] = float(obs.mode().min()) if c in self.binary else float(obs.median())
        filled = Z.fillna(self.fill_)
        if self.scale:
            self.mean_ = filled.mean().to_dict()
            sd = filled.std(ddof=0)
            self.sd_ = {c: (float(s) if s > 0 else 1.0) for c, s in sd.items()}
        self.feature_names_ = self.columns + [c + "__missing" for c in self.indicators_]
        self.fitted_ = True
        return self

    def transform(self, X):
        if not self.fitted_:
            raise PreprocessingError("preprocessor not fitted")
        Z = self._base(X)
        ind = {c + "__missing": Z[c].isna().astype(float) for c in self.indicators_}
        Z = Z.fillna(self.fill_)
        if self.scale:
            for c in self.columns:
                Z[c] = (Z[c] - self.mean_[c]) / self.sd_[c]
        for k, v in ind.items():
            Z[k] = v
        out = Z[self.feature_names_].to_numpy(dtype=float)
        if not np.isfinite(out).all():
            raise PreprocessingError("non-finite values after preprocessing")
        return out

    def fit_transform(self, X):
        return self.fit(X).transform(X)
