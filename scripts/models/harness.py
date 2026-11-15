"""Common experiment harness for the DRAFT experimental protocol (sections 11-16). SCAFFOLDING.

For one model and one predictor matrix:
  1. per seed: stratified D-train / D-cal split (80/20) and stratified 5-fold CV on D-train;
  2. equal-budget tuning: the same number of configurations for every method, selected by mean CV
     log loss, with the preprocessor refitted inside every training fold;
  3. internal performance from the out-of-fold predictions of the selected configuration (raw, and
     after the D-cal calibrator of step 4, as the like-for-like reference for temporal transfer);
  4. refit on all of D-train, then post-hoc calibration (F3) and class-conditional conformal sets
     (F4) fitted on D-cal; the decision threshold is fixed on D-cal; the model is then frozen;
  5. optional temporal validation: the frozen primary-seed model is applied ONCE; the validation
     data never reach tuning, calibration, conformal fitting or threshold selection.
Every run appends one JSON record (configuration hash, seeds, environment, Git commit, data
fingerprint, results) to <log_dir>/runs.jsonl.

Guard: only data labelled "SYNTHETIC" may be used unless an authorisation reference is given, the
configuration names a frozen (non-draft) protocol version AND binds it by file and SHA-256
(protocol_path, protocol_sha256), and the Git working tree is clean. No real data have been used. With the
current permissions only the non-learning FixedScoreStub is run in tests (D-040; see models.py).
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import numpy as np

import metrics as M
from calibration import make_calibrator
from conformal import MondrianConformal
from models import build_model, needs_scaling, positive_proba
from preprocess import InFoldPreprocessor
from reproducibility import config_hash, data_fingerprint, environment_record, git_commit
from splits import derive_seeds, stratified_kfold, stratified_split
from tuning import configurations_for, select_best


class HarnessError(ValueError):
    pass


def _guard(config, data_label, authorisation):
    if data_label == "SYNTHETIC":
        return
    if data_label != "REAL":
        raise HarnessError("data_label must be 'SYNTHETIC' or 'REAL'")
    if not authorisation:
        raise HarnessError("real data need an explicit researcher authorisation reference")
    version = str(config.get("protocol_version", ""))
    if not version or "draft" in version.lower():
        raise HarnessError("real data need a frozen (non-draft) experimental protocol version")
    # bind the run to the frozen protocol text: its file must hash to the value in the configuration
    path, expected = config.get("protocol_path"), str(config.get("protocol_sha256", "")).lower()
    if not path or len(expected) != 64:
        raise HarnessError("real data need protocol_path and protocol_sha256 (the frozen protocol hash)")
    p = Path(path)
    if not p.is_absolute():
        p = Path(__file__).resolve().parents[2] / p
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected:
        raise HarnessError("the protocol file does not match protocol_sha256")
    # the code that produces real-data results must be committed (no uncommitted changes)
    g = git_commit()
    if g.get("dirty") is not False or g.get("commit") in (None, "", "unknown"):
        raise HarnessError("real data need a clean, committed working tree (git status must be empty)")


def _fit_predict(model_name, cfg, seed, X_tr, y_tr, X_te, columns):
    pre = InFoldPreprocessor(columns, scale=model_name != "STUB" and needs_scaling(model_name))
    Z_tr = pre.fit_transform(X_tr)
    Z_te = pre.transform(X_te)
    model = build_model(model_name, cfg, seed).fit(Z_tr, y_tr)
    return np.clip(positive_proba(model, Z_te), 1e-9, 1 - 1e-9), (pre, model)


def run_seed(config, model_name, X, y, seed):
    """Steps 1-4 for one seed. X: pandas DataFrame of the predictor group; y: 0/1 array."""
    y = np.asarray(y).astype(int)
    columns = list(X.columns)
    tr, cal = stratified_split(y, config["calibration_fraction"], seed)
    X_tr, y_tr = X.iloc[tr].reset_index(drop=True), y[tr]
    folds = stratified_kfold(y_tr, config["cv_folds"], seed)
    configs = configurations_for(config["methods"][model_name], config["tuning_budget"], seed)
    cv_scores = []
    oof_by_cfg = []
    for cfg in configs:
        oof = np.full(y_tr.size, np.nan)
        for f_tr, f_te in folds:
            p, _ = _fit_predict(model_name, cfg, seed, X_tr.iloc[f_tr], y_tr[f_tr], X_tr.iloc[f_te], columns)
            oof[f_te] = p
        cv_scores.append(M.log_loss(y_tr, oof))
        oof_by_cfg.append(oof)
    best = select_best(cv_scores)
    oof = oof_by_cfg[best]
    # refit on all of D-train; calibrate, conformalise and fix the threshold on D-cal only
    p_cal_raw, fitted = _fit_predict(model_name, configs[best], seed, X_tr, y_tr, X.iloc[cal], columns)
    calibrator = make_calibrator(config["calibration"])
    if calibrator is not None:
        calibrator.fit(p_cal_raw, y[cal])
        p_cal = calibrator.predict(p_cal_raw)
    else:
        p_cal = p_cal_raw
    conformal = MondrianConformal(config["conformal_alpha"]).fit(p_cal, y[cal])
    threshold = M.threshold_for_sensitivity(y[cal], p_cal, config["threshold_sensitivity"])
    # Internal validation: uncalibrated out-of-fold predictions on D-train. The threshold was fixed on
    # CALIBRATED D-cal probabilities, so it is not applied to this different probability scale; the
    # threshold-dependent metrics are reported only where the frozen model is applied (apply_frozen).
    internal = M.all_metrics(y_tr, oof, None)
    # Like-for-like internal reference for Q3 (temporal transfer): the same out-of-fold predictions
    # passed through the calibrator fitted on D-cal (disjoint from D-train), on the scale on which the
    # threshold was fixed, so the threshold-dependent metrics apply. Which internal estimate is the Q3
    # reference is a protocol decision (freeze candidate section 9); both are recorded.
    oof_cal = calibrator.predict(oof) if calibrator is not None else oof
    internal_cal = M.all_metrics(y_tr, oof_cal, threshold, sets=conformal.predict_sets(oof_cal))
    frozen = {"preprocessor": fitted[0], "model": fitted[1], "calibrator": calibrator,
              "conformal": conformal, "threshold": threshold, "config": configs[best]}
    # The conformal sets keep their split-conformal guarantee although the calibrator is fitted on
    # the same D-cal only if the calibrator preserves the score order (Platt slope > 0); recorded so a
    # non-increasing fit is visible in the run record (tests: CalibrationThenConformalOnSameDcal).
    slope = getattr(calibrator, "coef_", None)
    order_preserving = None if slope is None else bool(slope[1] > 0)
    return {"seed": seed, "n_train": int(tr.size), "n_cal": int(cal.size), "best_index": best,
            "calibrator_order_preserving": order_preserving,
            "best_config": configs[best], "cv_log_loss": [float(s) for s in cv_scores],
            "internal_oof": internal, "internal_oof_calibrated": internal_cal,
            "_oof": {"index": tr, "p_raw": oof, "p_calibrated": oof_cal}}, frozen


def apply_frozen(frozen, X_val, y_val, w_val=None):
    """Apply a frozen model once to validation data. Nothing is refitted here."""
    Z = frozen["preprocessor"].transform(X_val)
    p = np.clip(positive_proba(frozen["model"], Z), 1e-9, 1 - 1e-9)
    if frozen["calibrator"] is not None:
        p = frozen["calibrator"].predict(p)
    sets = frozen["conformal"].predict_sets(p)
    return M.all_metrics(np.asarray(y_val).astype(int), p, frozen["threshold"], sets=sets, w=w_val), p


def run_experiment(config, model_name, X, y, data_label, log_dir, validation=None, authorisation=None,
                   return_predictions=False):
    """Run all seeds for one model and predictor matrix; optionally apply the primary-seed frozen
    model once to validation=(X_val, y_val[, w_val]). Returns the run record (also appended to log).
    return_predictions=True also returns {"oof_primary": {"index", "p_raw", "p_calibrated"},
    "validation": calibrated probabilities} for paired model comparisons (compare.py). Comparisons of
    calibrated models (Q2: ICI, Brier) must use "p_calibrated", the scale of the frozen model;
    "p_raw" is for the uncalibrated reporting and ablation AB-1 (without F3). Predictions are returned in memory only and never written to the log;
    for real data they must be stored outside Git (participant-level output)."""
    _guard(config, data_label, authorisation)
    if list(X.columns) != list(config.get("columns", X.columns)):
        raise HarnessError("feature columns differ from the configuration")
    seeds = derive_seeds(config["master_seed"], config["n_seeds"])
    started = time.time()
    per_seed, frozen_primary, oof_primary = [], None, None
    for i, s in enumerate(seeds):
        res, frozen = run_seed(config, model_name, X, y, s)
        oof = res.pop("_oof")
        per_seed.append(res)
        if i == 0:
            frozen_primary, oof_primary = frozen, oof
    record = {"model": model_name, "data_label": data_label, "authorisation": authorisation,
              "config_hash": config_hash(config), "protocol_version": config.get("protocol_version"),
              "protocol_sha256": config.get("protocol_sha256"),
              "seeds": seeds, "data_fingerprint": data_fingerprint(X.to_numpy(dtype=float, na_value=np.nan), y),
              "git": git_commit(), "environment": environment_record(), "per_seed": per_seed,
              "internal_summary": _summarise([r["internal_oof"] for r in per_seed]),
              "internal_calibrated_summary": _summarise([r["internal_oof_calibrated"] for r in per_seed])}
    if validation is not None:
        X_val, y_val = validation[0], validation[1]
        w_val = validation[2] if len(validation) > 2 else None
        record["validation_fingerprint"] = data_fingerprint(X_val.to_numpy(dtype=float, na_value=np.nan), y_val)
        record["temporal_validation"], p_val = apply_frozen(frozen_primary, X_val, y_val, w_val)
    else:
        p_val = None
    record["runtime_s"] = round(time.time() - started, 3)
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    with open(log_dir / "runs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True, default=str) + "\n")
    if return_predictions:
        return record, {"oof_primary": oof_primary, "validation": p_val}
    return record


def _summarise(results):
    """Mean, SD (ddof=1), min, max and count over seeds for every metric present in any seed result.
    Non-finite values (e.g. an undefined calibration slope) are excluded and counted in n_missing."""
    keys = sorted({k for r in results for k in r})
    out = {}
    for k in keys:
        v = np.array([r.get(k, np.nan) for r in results], dtype=float)
        ok = v[np.isfinite(v)]
        if ok.size == 0:
            out[k] = {"mean": None, "sd": None, "min": None, "max": None, "n": 0, "n_missing": int(v.size)}
            continue
        out[k] = {"mean": float(ok.mean()), "sd": float(ok.std(ddof=1)) if ok.size > 1 else 0.0,
                  "min": float(ok.min()), "max": float(ok.max()), "n": int(ok.size),
                  "n_missing": int(v.size - ok.size)}
    return out
