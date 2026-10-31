"""Leakage and data-handling safeguards for the planned NHANES analysis (WP3; synthetic-tested).

Status: software safeguards only. Nothing here reads NHANES files, downloads data, fits a model or
evaluates performance. The rules implement the DRAFT experimental protocol
(research/methodology/experimental_protocol_v0.1_draft.md, revision 5; not approved, not frozen):
  * section 7 (leakage audit of variables)  -> check_predictors();
  * section 3.3 (no participant in both periods) -> check_disjoint_participants();
  * section 9/12 (preprocessing fitted in-fold) -> check_folds() and fit_within_folds();
  * section 4 (eligibility cascade E0-E8)    -> eligibility_cascade().
If the protocol's rules change, this module must change with them. The tests in tests/nhanes use
clearly labelled SYNTHETIC frames only; synthetic values are never NHANES observations.

Not decided here (scientific decisions reserved for the researcher): harmonisation across periods
(Q-044, Q-046, Q-047, Q-060), the outcome source (Q-061, FA-2), predictor groups A/B/C (Q-050), the
insulin sensitivity analysis (S-06), weighting (FA-7). Fasting insulin (LBXIN) is therefore NOT on the
universal prohibited list: the draft excludes it from the primary sets but allows it in S-06; the
predictor-group definitions are to be checked separately once approved.

Standard library and pandas only (pandas is used only by eligibility_cascade).
"""
from __future__ import annotations

import re

# Protocol draft section 7: variables that are never predictors.
OUTCOME_VARIABLES = frozenset({"LBXGH", "LBXGLU", "LBDGLUSI"})                 # outcome definition
OTHER_GLUCOSE_VARIABLES = frozenset({"LBXSGL", "LBDSGLSI"})                   # serum glucose (biochemistry panel)
SURVEY_AND_PROCESSING = frozenset({"SEQN", "SDMVSTRA", "SDMVPSU", "RIDEXMON",
                                   "PHAFSTHR", "PHAFSTMN", "PHDSESN", "PHDSESNZ"})
# prefixes: diabetes questionnaire (DIQ/DID), medication (RXQ/RXD), every survey weight (WT...)
PROHIBITED_PREFIXES = ("DIQ", "DID", "RXQ", "RXD", "WT")
COMMENT_CODE_SUFFIX = "LC"   # NHANES comment-code variables end in LC (section 7, "*LC")
# Derived glycaemic indices (section 7). A derived feature is prohibited when its declared inputs
# include a glycaemic measurement, whatever it is called; the name tokens catch undeclared ones.
GLYCAEMIC_INPUTS = OUTCOME_VARIABLES | OTHER_GLUCOSE_VARIABLES | frozenset({"LBXIN"})
DERIVED_INDEX_TOKENS = ("HOMA", "QUICKI", "TYG", "METSIR", "METS_IR", "CTI", "EGDR", "SPISE")


class LeakageError(ValueError):
    """A prohibited variable would enter a predictor matrix, or folds/periods overlap."""


def predictor_violations(columns, derived_inputs=None):
    """List of (column, rule) for every column that may not be a predictor.
    derived_inputs: optional {derived feature name: [source variable names]}."""
    derived_inputs = derived_inputs or {}
    out = []
    for col in columns:
        name = str(col)
        up = name.upper()
        if up in OUTCOME_VARIABLES:
            out.append((name, "outcome variable"))
        elif up in OTHER_GLUCOSE_VARIABLES:
            out.append((name, "other glucose measurement"))
        elif up in SURVEY_AND_PROCESSING:
            out.append((name, "survey design or processing variable"))
        elif up.startswith(PROHIBITED_PREFIXES):
            out.append((name, "diabetes questionnaire, medication or survey weight"))
        elif up.endswith(COMMENT_CODE_SUFFIX) and len(up) > len(COMMENT_CODE_SUFFIX):
            out.append((name, "comment code"))
        elif any(tok in re.sub(r"[^A-Z_]", "", up) for tok in DERIVED_INDEX_TOKENS):
            out.append((name, "derived glycaemic index"))
        elif {str(v).upper() for v in derived_inputs.get(name, ())} & GLYCAEMIC_INPUTS:
            out.append((name, "derived from a glycaemic measurement"))
    return out


def check_predictors(columns, derived_inputs=None):
    """Raise LeakageError if any column may not be a predictor (protocol draft section 7)."""
    bad = predictor_violations(columns, derived_inputs)
    if bad:
        raise LeakageError("prohibited predictors: " + "; ".join(f"{c} ({r})" for c, r in bad))
    return list(columns)


def check_disjoint_participants(development_ids, validation_ids):
    """Raise LeakageError if a participant ID occurs in both periods (protocol draft section 3.3)."""
    both = set(development_ids) & set(validation_ids)
    if both:
        raise LeakageError(f"{len(both)} participant IDs occur in both periods")


def check_folds(folds, n_rows):
    """folds: list of (train_indices, test_indices). Raise LeakageError on overlap, duplicates or
    out-of-range indices; return the folds unchanged."""
    for k, (train, test) in enumerate(folds):
        tr, te = list(train), list(test)
        if len(set(tr)) != len(tr) or len(set(te)) != len(te):
            raise LeakageError(f"fold {k}: duplicated row indices")
        if set(tr) & set(te):
            raise LeakageError(f"fold {k}: {len(set(tr) & set(te))} rows in both train and test")
        if not tr or not te:
            raise LeakageError(f"fold {k}: empty train or test set")
        if any(not (0 <= i < n_rows) for i in tr + te):
            raise LeakageError(f"fold {k}: row index out of range")
    return folds


def fit_within_folds(rows, folds, fit, apply):
    """Run fit on the training rows of each fold only, then apply the fitted object to that fold's
    test rows. `fit(train_rows)` -> fitted object; `apply(fitted, test_rows)` -> result.
    The callables receive copies of the selected rows only, so a preprocessing step fitted here can
    never see test rows. Returns the list of per-fold results."""
    check_folds(folds, len(rows))
    results = []
    for train, test in folds:
        fitted = fit([rows[i] for i in train])
        results.append(apply(fitted, [rows[i] for i in test]))
    return results


def eligibility_cascade(d, weight_col):
    """Protocol draft section 4 cascade E0-E8 on one period's merged frame (pandas DataFrame).
    Required columns: RIDSTATR, RIDAGEYR, in_fasting_glucose_file (bool), <weight_col>, LBXGLU, LBXGH,
    RIDEXPRG, DIQ010, DIQ070. The rules follow scripts/nhanes/descriptive_counts.py period_counts();
    equivalence on the real files is NOT yet verified (needs the raw data). Returns (counts, mask)."""
    import pandas as pd
    m = pd.Series(True, index=d.index)
    counts = {"E0_all_participants": int(m.sum())}
    m &= d["RIDSTATR"] == 2
    counts["E1_mec_examined"] = int(m.sum())
    m &= d["RIDAGEYR"] >= 20
    counts["E2_age_ge_20"] = int(m.sum())
    m &= d["in_fasting_glucose_file"].astype(bool)
    counts["E3_in_fasting_glucose_file"] = int(m.sum())
    m &= d[weight_col] > 0
    counts["E4_fasting_weight_gt_0"] = int(m.sum())
    m &= d["LBXGLU"].notna() & d["LBXGH"].notna()
    counts["E5_valid_fpg_and_hba1c"] = int(m.sum())
    m &= ~(d["RIDEXPRG"] == 1)
    counts["E6_not_pregnant"] = int(m.sum())
    m &= d["DIQ010"].isin([2, 3])
    counts["E7_no_diagnosed_diabetes"] = int(m.sum())
    m &= ~(d["DIQ070"] == 1)
    counts["E8_analytic_N"] = int(m.sum())
    return counts, m
