# D-035 (Q-041): RQ5 component evidence standard

| Field | Value |
|---|---|
| Task | Q-041-DECISIONS (2026-10-24) |
| Owner response | Owner prompt of 2026-10-24 ("Record Q-041 Decisions and Prepare RQ5 Updates"): G1 Option A, G2 Option A, G3 Option I, G4 Option B, G5 Option A, G6 approve, with the safeguards stated in that prompt |
| Recorded as | **D-035 — APPROVED — CONDITIONAL, inactive for screening** (`logs/DECISION_LOG.md`) |
| Basis | The Q-041 investigation report delivered in the session on 2026-10-24 (in the conversation, not committed). Its option tables are summarised in §1 |
| Screening | **Not started.** No component status is recorded for any record |

## 1. Decisions and governance check

| ID | Owner choice | Recorded content | Governance check |
|---|---|---|---|
| G1 | A | D-033's "applied **or** evaluated" is kept. A `yes` needs evidence of a qualifying procedure actually applied to the study's data or model, **with a documented output** (component-specific, §2). A mention or a conceptual proposal is not a component | D-033 is **not** amended (no "and") |
| G2 | A | Title/abstract statuses are allowed for preliminary triage only and **never count** toward D-031/D-034 | Consistent with `search_strategy.md` §6.3 (abstract-only records "never used for detailed methodological claims") |
| G3 | I | A component is **confirmed** only when the status comes from a qualifying **full-text** assessment. A full-text-stage `abstract_only` decision (full text unavailable) confirms nothing | Defines "confirmed" in D-034. **Clarification, not a change** to D-034's groups |
| G4 | B | Researcher verification of records reaching `qualified` or `near_rq5`, through the workflow in §4 | Not a second independent reviewer. Builds on the protocol's proposed `screener=researcher` convention (`screening_protocol.md` §6.3) |
| G5 | A | A completed full-text RQ5 assessment records **all five** component statuses. `unclear` = assessed but unresolved; empty/null = not assessed | Matches D-033-4 (missing information is never `no`) |
| G6 | Approve | The component-specific evidence definitions in §2 are adopted for RQ5 component statuses | Overlaps the **proposed** D-029 (R5) and D-026 (protocol §2) wording for explainability, calibration and uncertainty, which scored what the abstract "states" or "claims". Neither is approved, so there is no conflict with an approved decision. D-035 governs RQ5 component statuses; **D-029 and D-026 stay PROPOSED** for their other content (validation design, required-descriptor rule, triggers) and keep their status. Whether to mark their component wording as superseded is the owner's call (§7) |

**Precedence.**
- Where D-035 and the proposed D-026 (`screening_protocol.md` §2) or D-029 (R5) define evidence for the same component differently, **D-035 applies to RQ5 component statuses**.
- D-026 and D-029 **remain PROPOSED**, with their status unchanged. Their other content (validation design, the required-descriptor rule, human-review triggers, non-RQ5 uses of the descriptors) is not affected.

D-031 (threshold), D-032 (feature-selection definition), D-033 and D-034 are unchanged. D-031 condition **C1** (approved definitions for explainability, calibration and uncertainty) is now met at decision level by D-035/G6.

## 2. Component evidence definitions (G1, G6)

Shared rule:
- `yes` = a qualifying procedure **applied to this study's data or model**, plus a **documented output** of that procedure.
- `no` = explicit evidence, or a fully described design, establishing that the procedure was not performed.
- `unclear` = assessed, but the evidence does not establish either. This is also used for mentions in the introduction, related work or a conceptual architecture when the methods are not fully described; when they are, such a mention gives `no`.

Component presence is **not** methodological quality: quality is appraised at full text (`search_strategy.md` §8.2). Public code and full reproducibility are not required (D-033-3).

| Component | `yes` requires | Insufficient on its own | `no` when | `unclear` when |
|---|---|---|---|---|
| Feature selection (D-032, unchanged) | A qualifying data-driven selection procedure **and** the retained subset of original variables, used as model input or reported as the panel | Importance used only to explain a model trained on all predictors; PCA or other projection alone; shrinkage without exclusion; a reused published panel alone; "biomarkers identified" with no link to the model | All variables explicitly used; inputs are latent components only; panel taken solely from prior work with no new procedure | Method named without the retained subset; panel of unstated origin; link between discovered markers and the model not stated |
| Classification | A classification or relevant risk-prediction model applied to the study data, **with predictive output reported** (performance under any validation design, or predictions used in the analysis) | A model mentioned only as background or future work; "a classifier is proposed" with no training or results; continuous-only regression targets | No predictive model is built (e.g., purely univariate association), or targets are continuous only | Unclear whether a model was trained or applied on the study data, or whether the target is a class or risk |
| Explainability | An explanation or attribution method applied to **the study's model**, **with explanation output reported** (e.g., ranked attributions, explanation plots, rules, coefficients presented as the explanation) | "Interpretable", "explainable" or "transparent" without a method; importance without stating how it was computed; explainability shown only in an architecture figure. **Explanation-quality evaluation is not required** for `yes` (appraisal item) | The fully described analysis contains no explanation of model predictions, or the paper says none was produced | Method named but not clearly applied to the model, or output not reported |
| Probability calibration | **Calibration assessment with a reported result** (calibration plot or curve, slope or intercept, ECE, Hosmer–Lemeshow, Spiegelhalter), **or** a documented **recalibration procedure** (Platt, isotonic, temperature scaling) applied to model outputs | **A Brier score alone**; reported probabilities, AUC or accuracy; "well-calibrated" without a method; calibration in the analytical-chemistry sense | The fully described analysis contains no calibration assessment or recalibration; only analytical calibration is meant | Calibration mentioned without method or result; Brier score only; the sense of "calibration" is ambiguous |
| Uncertainty estimation | A **prediction-level** uncertainty method (conformal sets or intervals, Bayesian predictive uncertainty, MC dropout, ensembles **used to quantify uncertainty**, abstention driven by an uncertainty score) applied to the study's model, **with its output reported or used** (e.g., set sizes, intervals, coverage, abstention results) | Confidence intervals of performance metrics; predicted probabilities or "confidence scores" without an uncertainty method; an ensemble used only as a model type; "robust" or "reliable" | Point predictions only, with the analysis fully described; explicitly not done | Method named but no output; unclear whether the uncertainty concerns predictions or a performance estimate |

## 3. Abstract versus full-text evidence (G2, G3, G5)

| Stage | Status meaning | Counts toward D-031/D-034? |
|---|---|---|
| `title_abstract` row | **Preliminary.** For triage only: a record with potential RQ5 status goes to full text | **Never** |
| `full_text` row, decision `include` / `exclude` / `uncertain` | **Confirmed**, when the row records all five component statuses (G5) | Yes |
| `full_text` row, decision `abstract_only` (full text unavailable) | Not confirmed. The record is reported as "full text unavailable" | Never |

A completed full-text RQ5 assessment records all five statuses (`unclear` when unresolved). An empty value means **not assessed**, never `no`.

## 4. Researcher verification workflow (G4)

1. **Trigger.** A record whose coverage group, derived from confirmed statuses, is `qualified` or `near_rq5`. The group cannot be derived until Q-039 adds a classification status, so the trigger is specified but **not yet computable**.
2. **Recording.**
   - The researcher appends a new `full_text` row to `screening/decisions.csv` with `screener=researcher`.
   - The row **restates all component statuses**, agreeing with or correcting the earlier full-text row.
   - Its `justification` starts with "verified:" and gives the reason for any change.
   - No new column is needed; the screening file is append-only by convention.
3. **Audit trail.**
   - The earlier assistant row stays in the file.
   - The build keeps it in `rq5_components.confirmed.history`.
   - The build derives `researcher_verified` (the latest full-text row is the researcher's) and `changed_by_verification` (the researcher's statuses differ from the latest earlier non-researcher full-text row).
4. **Authority.** The researcher's row is the confirmed assessment.
5. **Disagreement or unresolved evidence.**
   - The researcher records `unclear` for any component that cannot be resolved (optionally `needs_human=yes`).
   - The record stays provisional per D-034; no third reviewer is added.
   - A later decision is again a new row.
6. **Pending verification.** Once the group can be derived, `qualified`/`near_rq5` records without researcher verification are reported as pending verification. Specified, not implemented (blocked by Q-039).

## 5. Data-integrity rules

Each rule is implemented in `scripts/literature/pubrecords.py` (`rq5_component_evidence`) and tested.

| Rule | Behaviour |
|---|---|
| No silent erasure | A later row of the **same stage** that leaves blank a component recorded earlier at that stage stops the build (nothing written). Changing a value (e.g., `yes` → `unclear`) is allowed and stays visible in the file and the history |
| Stage separation | Title/abstract values (`preliminary`) and full-text values (`confirmed`) are kept separately. A full-text row cannot overwrite preliminary evidence, and preliminary evidence never becomes confirmed |
| Completeness | **Current limitation, dependent on Q-039:** the check covers the **four** existing component columns (feature selection, explainability, calibration, uncertainty). No classification definition or column is introduced here. A full-text row that records any component status must record **all four**, else the build stops. Classification has no column yet (Q-039). When Q-039 adds one, it joins this check, so the five-status rule (G5) is then fully enforced |
| Not assessed | A full-text row with no component values gives `confirmed = null` with the note "not assessed". Unscreened records have `rq5_components = null` |
| Unchanged | `screening_details`, `screening_decision`, the screening-file columns, the inventory and paper IDs behave exactly as before |

**Coverage group.** `derive_rq5_coverage_group()` implements D-034 on **confirmed** statuses:
- `qualified` = ≥ 4 `yes`;
- `near_rq5` = exactly 3;
- `below_threshold` = 0–2;
- `null` if any of the five is not assessed;
- `provisional` = any `unclear`.

It is tested but **not wired into the build**: the classification status does not exist (Q-039), so every derived group would be `null`.

## 6. Activation conditions and dependencies
D-035 governs no screening until:
1. **Q-039** — a classification status column exists, so G5 and the coverage group apply to all five components;
2. **Q-040** — screening retention of non-metabolic 3-of-5 frameworks is decided;
3. **D-027 and D-024** (screening-file and inventory schemas) are approved;
4. the remaining **R5/D-029** items (validation design, the required-descriptor rule, triggers) are decided;
5. D-031–D-035 are written into `screening_criteria.md` v1.1 and protocol v0.2, frozen as the pilot's `criteria_version`;
6. the other pilot-blocking items are resolved.

## 7. Open point for the owner (not decided here)
- Whether to mark the component wording of the proposed D-029 (R5) and D-026 (protocol §2) as superseded by D-035, or leave it until those decisions are taken as a whole. Under the BIO-001-REVIEW rule, an assistant does not change the status of a proposal under review.
