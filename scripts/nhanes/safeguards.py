"""Leakage and data-handling safeguards for the planned NHANES analysis (WP3; synthetic-tested).

Status: software safeguards only. Nothing here reads NHANES files, downloads data, fits a model or
evaluates performance. They are standalone helpers: no experimental pipeline calls them yet, and they
have been tested only on clearly labelled SYNTHETIC frames (tests/nhanes), never against real data.
The rules implement the DRAFT experimental protocol
(research/methodology/experimental_protocol_v0.1_draft.md, revision 5; not approved, not frozen):
  * section 7 (leakage audit of variables)          -> predictor_violations(), check_predictors();
  * section 3.3 (no participant in both periods)    -> check_disjoint_participants();
  * section 12 (D-train / D-cal / validation)       -> check_partitions();
  * section 9/12 (preprocessing fitted in-fold)     -> check_folds(), fit_within_folds();
  * section 4 (eligibility cascade E0-E8)           -> eligibility_cascade().
If the protocol's rules change, this module must change with them.

Name-based predictor checks cannot be complete: a column renamed to something unforeseen can still
pass. The aliases below are a safety net, not a guarantee; the strong control is the allow-list
argument of check_predictors() once the approved predictor lists exist (Q-050, pending).

Not decided here (scientific decisions reserved for the researcher): harmonisation across periods
(Q-044, Q-046, Q-047, Q-060), the outcome source (Q-061, FA-2), predictor groups A/B/C (Q-050), the
insulin sensitivity analysis (S-06), weighting (FA-7), the FA-1 age alternative. Fasting insulin
(LBXIN, or an "insulin" alias) is therefore NOT on the universal prohibited list: the draft excludes it
from the primary sets but allows it in S-06; group-level lists are to be checked once approved.

Standard library and pandas only (pandas/numpy are used only by eligibility_cascade).
"""
from __future__ import annotations

import math
import re

# Protocol draft section 7: variables that are never predictors (exact NHANES names).
OUTCOME_VARIABLES = frozenset({"LBXGH", "LBXGLU", "LBDGLUSI"})                 # outcome definition
# serum glucose (biochemistry panel); OGTT two-hour glucose (LBXGLT/LBDGLTSI: NHANES naming as
# recalled, not re-checked against a codebook here; OGTT was not collected after 2015-16, section 7)
OTHER_GLUCOSE_VARIABLES = frozenset({"LBXSGL", "LBDSGLSI", "LBXGLT", "LBDGLTSI"})
SURVEY_AND_PROCESSING = frozenset({"SEQN", "SDMVSTRA", "SDMVPSU", "RIDEXMON",
                                   "PHAFSTHR", "PHAFSTMN", "PHDSESN", "PHDSESNZ"})
# prefixes: diabetes questionnaire (DIQ/DID), medication (RXQ/RXD), every survey weight (WT...)
PROHIBITED_PREFIXES = ("DIQ", "DID", "RXQ", "RXD", "WT")
# NHANES comment-code variables end in LC (section 7, "*LC"). Applied only to NHANES-style names
# (letters and digits only, at most 8 characters, the SAS transport-file limit), so analyst-made
# names such as BMI_CALC are not caught by accident.
COMMENT_CODE = re.compile(r"[A-Z][A-Z0-9]{1,5}LC")
# Derived glycaemic indices (section 7), matched as whole name tokens (see _tokens), never as
# substrings: FRACTION or INFECTION do not contain the token CTI.
DERIVED_INDEX = re.compile(r"HOMA\d*(IR|B|BETA|S|%B|%S)?|QUICKI|TYG(BMI|WC|WHTR)?|METSIR|CTI|EGDR|SPISE")
# Aliases for section 7 categories, matched as whole tokens or adjacent token pairs. Deliberately
# conservative (no "GLU": glutamate; no "WEIGHT" alone: body weight; no "INSULIN": S-06 undecided).
ALIAS_TOKENS = {
    "outcome or glucose measurement": {"GLUCOSE", "FPG", "FBG", "FSG", "HBA1C", "A1C", "GLYCOHEMOGLOBIN",
                                        "GLYCOHAEMOGLOBIN", "OGTT"},
    "diabetes questionnaire or medication": {"DIABETES", "DIABETIC", "PREDIABETES", "PREDIABETIC",
                                             "MEDICATION", "MEDICATIONS", "PRESCRIPTION", "METFORMIN",
                                             "ANTIDIABETIC", "HYPOGLYCAEMIC", "HYPOGLYCEMIC"},
    "survey design or processing variable": {"STRATUM", "STRATA", "PSU", "SESSION"},
}
ALIAS_PAIRS = {
    "outcome or glucose measurement": {("GLYCATED", "HEMOGLOBIN"), ("GLYCATED", "HAEMOGLOBIN"),
                                        ("GLYCATED", "HB"), ("HB", "A1C")},
    "survey design or processing variable": {("SURVEY", "WEIGHT"), ("SAMPLE", "WEIGHT"), ("MEC", "WEIGHT"),
                                             ("FASTING", "WEIGHT"), ("FASTING", "HOURS"), ("FASTING", "HRS"),
                                             ("FASTING", "DURATION"), ("FASTING", "TIME"),
                                             ("FASTING", "MINUTES"), ("FAST", "HOURS"), ("EXAM", "MONTH"),
                                             ("COMMENT", "CODE")},
}
# Declared inputs of a derived feature that make it a derived glycaemic measure (section 7). LBXIN is
# included as before (HOMA/QUICKI-type use); whether an insulin-only transform such as log(insulin)
# in S-06 counts is NOT decided here (see the module docstring).
GLYCAEMIC_INPUTS = OUTCOME_VARIABLES | OTHER_GLUCOSE_VARIABLES | frozenset({"LBXIN"})


class LeakageError(ValueError):
    """A prohibited variable would enter a predictor matrix, or folds/periods/partitions overlap."""


def _tokens(name):
    """Upper-case name tokens: split on non-alphanumerics and lower-to-upper case changes
    (homaIR -> HOMA, IR; TyG-BMI -> TY, G, BMI). Single tokens and joined neighbours are both returned,
    so TyG and METS_IR are recognised as TYG and METSIR."""
    parts = [p.upper() for p in re.split(r"[^A-Za-z0-9%]+|(?<=[a-z])(?=[A-Z])", str(name)) if p]
    joined = {a + b for a, b in zip(parts, parts[1:])}
    joined |= {a + b + c for a, b, c in zip(parts, parts[1:], parts[2:])}
    return parts, set(parts) | joined


def predictor_violations(columns, derived_inputs=None):
    """List of (column, rule) for every column that may not be a predictor.
    derived_inputs: optional {derived feature name: [source variable names]}."""
    derived_inputs = derived_inputs or {}
    out = []
    for col in columns:
        name = str(col)
        up = name.upper()
        parts, toks = _tokens(name)
        pairs = set(zip(parts, parts[1:]))
        alias = next((rule for rule, words in ALIAS_TOKENS.items() if words & toks), None) or \
            next((rule for rule, prs in ALIAS_PAIRS.items() if prs & pairs), None)
        if up in OUTCOME_VARIABLES:
            out.append((name, "outcome variable"))
        elif up in OTHER_GLUCOSE_VARIABLES:
            out.append((name, "other glucose measurement"))
        elif up in SURVEY_AND_PROCESSING:
            out.append((name, "survey design or processing variable"))
        elif up.startswith(PROHIBITED_PREFIXES):
            out.append((name, "diabetes questionnaire, medication or survey weight"))
        elif name.isalnum() and len(name) <= 8 and COMMENT_CODE.fullmatch(up):
            out.append((name, "comment code"))
        elif any(DERIVED_INDEX.fullmatch(t) for t in toks):
            out.append((name, "derived glycaemic index"))
        elif alias:
            out.append((name, alias + " (name alias)"))
        elif {str(v).upper() for v in derived_inputs.get(name, ())} & GLYCAEMIC_INPUTS:
            out.append((name, "derived from a glycaemic measurement"))
    return out


def check_predictors(columns, derived_inputs=None, allowed=None):
    """Raise LeakageError if any column may not be a predictor (protocol draft section 7).
    allowed: optional approved predictor list; when given, every column must be in it (or be a
    declared derived feature whose inputs are all in it). This is the strong check against renamed
    columns; the list itself is a researcher decision (Q-050) and is not defined here."""
    columns = list(columns)
    bad = predictor_violations(columns, derived_inputs)
    if allowed is not None:
        ok = set(allowed)
        for c in columns:
            if c in ok:
                continue
            inputs = (derived_inputs or {}).get(c)
            if not inputs or not set(inputs) <= ok:
                bad.append((c, "not in the approved predictor list"))
    if bad:
        raise LeakageError("prohibited predictors: " + "; ".join(f"{c} ({r})" for c, r in bad))
    return columns


def _is_missing(v):
    if v is None:
        return True
    try:
        return v != v or (isinstance(v, float) and math.isnan(v))   # NaN, pandas NA-like
    except (TypeError, ValueError):                                   # pandas.NA raises on bool()
        return True


def check_unique_participants(ids, what="participant IDs"):
    """Raise LeakageError on a missing or duplicated ID (one row per participant is required)."""
    ids = list(ids)
    missing = sum(_is_missing(i) for i in ids)
    if missing:
        raise LeakageError(f"{missing} missing {what}")
    if len(set(ids)) != len(ids):
        raise LeakageError(f"{len(ids) - len(set(ids))} duplicated {what}")
    return ids


def check_disjoint_participants(development_ids, validation_ids):
    """Raise LeakageError if a participant ID occurs in both periods (protocol draft section 3.3),
    or if either list has a missing ID."""
    for ids, what in ((development_ids, "development IDs"), (validation_ids, "validation IDs")):
        if any(_is_missing(i) for i in ids):
            raise LeakageError(f"missing {what}")
    both = set(development_ids) & set(validation_ids)
    if both:
        raise LeakageError(f"{len(both)} participant IDs occur in both periods")


def check_partitions(partitions, expected_ids=None):
    """partitions: {name: participant IDs}, e.g. D-train, D-cal and validation (section 12; the
    names and proportions are not fixed here). Each partition must be non-empty with unique,
    non-missing IDs; partitions must be pairwise disjoint; when expected_ids is given their union
    must equal it exactly (no participant lost or added). Raises LeakageError."""
    if len(partitions) < 2:
        raise LeakageError("at least two partitions are required")
    sets = {}
    for name, ids in partitions.items():
        ids = list(ids)
        if not ids:
            raise LeakageError(f"partition {name!r} is empty")
        check_unique_participants(ids, f"IDs in partition {name!r}")
        sets[name] = set(ids)
    names = list(sets)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            both = sets[a] & sets[b]
            if both:
                raise LeakageError(f"{len(both)} participants in both {a!r} and {b!r}")
    if expected_ids is not None:
        expected = set(check_unique_participants(expected_ids, "expected IDs"))
        union = set().union(*sets.values())
        if union != expected:
            raise LeakageError(f"partitions cover {len(union & expected)} of {len(expected)} expected IDs "
                               f"and add {len(union - expected)} unexpected IDs")
    return partitions


def check_folds(folds, n_rows, ids=None, require_partition=False):
    """folds: list of (train_indices, test_indices). Raise LeakageError on overlap, duplicates,
    non-integer or out-of-range indices; return the folds unchanged.
    ids: optional participant ID per row. When given, IDs must be non-missing and no participant may
    have rows in both train and test of a fold (catches duplicated participant rows).
    require_partition: every row must be in exactly one test set, and in each fold train and test
    together must cover all rows (K-fold)."""
    if ids is not None:
        ids = list(ids)
        if len(ids) != n_rows:
            raise LeakageError(f"{len(ids)} participant IDs for {n_rows} rows")
        if any(_is_missing(i) for i in ids):
            raise LeakageError("missing participant IDs")
    tested = []
    for k, (train, test) in enumerate(folds):
        tr, te = list(train), list(test)
        if any(isinstance(i, bool) or not isinstance(i, int) and not hasattr(i, "__index__") for i in tr + te):
            raise LeakageError(f"fold {k}: row indices must be integers")
        tr, te = [int(i) for i in tr], [int(i) for i in te]
        if len(set(tr)) != len(tr) or len(set(te)) != len(te):
            raise LeakageError(f"fold {k}: duplicated row indices")
        if set(tr) & set(te):
            raise LeakageError(f"fold {k}: {len(set(tr) & set(te))} rows in both train and test")
        if not tr or not te:
            raise LeakageError(f"fold {k}: empty train or test set")
        if any(not (0 <= i < n_rows) for i in tr + te):
            raise LeakageError(f"fold {k}: row index out of range")
        if ids is not None:
            shared = {ids[i] for i in tr} & {ids[i] for i in te}
            if shared:
                raise LeakageError(f"fold {k}: {len(shared)} participants have rows in both train and test")
        if require_partition and len(tr) + len(te) != n_rows:
            raise LeakageError(f"fold {k}: train and test do not cover all {n_rows} rows")
        tested += te
    if require_partition and sorted(tested) != list(range(n_rows)):
        raise LeakageError("test sets do not cover every row exactly once")
    return folds


def fit_within_folds(rows, folds, fit, apply, ids=None, require_partition=False):
    """Run fit on the training rows of each fold only, then apply the fitted object to that fold's
    test rows. `fit(train_rows)` -> fitted object; `apply(fitted, test_rows)` -> result.
    The callables receive the selected rows only; this cannot stop a callable that reads other data
    from outside (that remains the caller's responsibility). Returns the list of per-fold results."""
    check_folds(folds, len(rows), ids=ids, require_partition=require_partition)
    results = []
    for train, test in folds:
        fitted = fit([rows[i] for i in train])
        results.append(apply(fitted, [rows[i] for i in test]))
    return results


def _bool_flags(series, column):
    """Only real booleans are accepted; missing values, strings (e.g. a merge indicator such as
    "left_only"), numbers and pandas NA are rejected, never coerced."""
    import numpy as np
    if series.dtype == bool:
        return series
    invalid = [v for v in series if type(v) not in (bool, np.bool_)]
    if invalid:
        examples = sorted({repr(v) for v in invalid})[:5]
        raise ValueError(f"{column}: {len(invalid)} values are not True/False (e.g. {', '.join(examples)}); "
                         "missing or invalid values are not coerced")
    return series.astype(bool)


def eligibility_cascade(d, weight_col, details=None):
    """Protocol draft section 4 cascade E0-E8 on one period's merged frame (pandas DataFrame).
    Required columns: RIDSTATR, RIDAGEYR, in_fasting_glucose_file (True/False only; derive it from the
    merge indicator, e.g. in_glu == "both"), <weight_col>, LBXGLU, LBXGH, RIDEXPRG, DIQ010, DIQ070.
    If a SEQN column is present it must be unique and non-missing. The rules follow
    scripts/nhanes/descriptive_counts.py period_counts(); equivalence on the real files is NOT
    verified (needs the raw data). Returns (counts, mask).
    details: optional dict, filled with the subcategory counts that period_counts() also reports
    (E2_alt_age_ge_18, E5a_valid_fpg, E6_excluded_pregnant, E7_excluded_diagnosed,
    E7_excluded_refused_dk_missing, E8_excluded_diabetes_pills), plus E7_excluded_other_code (a DIQ010
    value outside 1/2/3/7/9/missing) and the number excluded at each step (excluded_at)."""
    import pandas as pd
    if "SEQN" in d.columns:
        check_unique_participants(d["SEQN"], "SEQN values")
    in_file = _bool_flags(d["in_fasting_glucose_file"], "in_fasting_glucose_file")
    sub = {}
    m = pd.Series(True, index=d.index)
    counts = {"E0_all_participants": int(m.sum())}
    m &= d["RIDSTATR"] == 2
    counts["E1_mec_examined"] = int(m.sum())
    sub["E2_alt_age_ge_18"] = int((m & (d["RIDAGEYR"] >= 18)).sum())
    m &= d["RIDAGEYR"] >= 20
    counts["E2_age_ge_20"] = int(m.sum())
    m &= in_file
    counts["E3_in_fasting_glucose_file"] = int(m.sum())
    m &= d[weight_col] > 0
    counts["E4_fasting_weight_gt_0"] = int(m.sum())
    m &= d["LBXGLU"].notna()
    sub["E5a_valid_fpg"] = int(m.sum())
    m &= d["LBXGH"].notna()
    counts["E5_valid_fpg_and_hba1c"] = int(m.sum())
    sub["E6_excluded_pregnant"] = int((m & (d["RIDEXPRG"] == 1)).sum())
    m &= ~(d["RIDEXPRG"] == 1)
    counts["E6_not_pregnant"] = int(m.sum())
    sub["E7_excluded_diagnosed"] = int((m & (d["DIQ010"] == 1)).sum())
    sub["E7_excluded_refused_dk_missing"] = int((m & (d["DIQ010"].isin([7, 9]) | d["DIQ010"].isna())).sum())
    sub["E7_excluded_other_code"] = int((m & ~d["DIQ010"].isin([1, 2, 3, 7, 9]) & d["DIQ010"].notna()).sum())
    m &= d["DIQ010"].isin([2, 3])
    counts["E7_no_diagnosed_diabetes"] = int(m.sum())
    sub["E8_excluded_diabetes_pills"] = int((m & (d["DIQ070"] == 1)).sum())
    m &= ~(d["DIQ070"] == 1)
    counts["E8_analytic_N"] = int(m.sum())
    if details is not None:
        steps = list(counts)
        details.update(sub)
        details["excluded_at"] = {b: counts[a] - counts[b] for a, b in zip(steps, steps[1:])}
    return counts, m
