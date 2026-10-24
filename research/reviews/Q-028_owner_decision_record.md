# Q-028 / A-3 (RQ5 part): owner decision record

| Field | Value |
|---|---|
| Task | LIT-004-Q028-DECISION (2026-10-24) |
| Owner response | "For Q-028, I select Option C: five separate components with an inclusion threshold of at least 4 out of 5. Please treat this as my owner response for Q-028 only." (owner prompt, 2026-10-24) |
| Recorded as | **D-031 — APPROVED — CONDITIONAL** in `logs/DECISION_LOG.md` (conditions in §5). No other decision is affected |
| Not done | No change to `screening_criteria.md`, `screening_protocol.md`, `search_strategy.md`, `research_plan.md`, schemas, code or data. Those changes follow once the conditions are met (§6) |
| Provenance of option (c) | Q-028 as first written (LIT-004-PREPARATION) offered two options: ≥ 3 of 4, or ≥ 3 of 5. Option (c) (≥ 4 of 5) was added in the owner ballot (LIT-004-OWNER-BALLOT, Item 16) and reproduced unchanged in the final confirmation sheet (R3), where the owner selected it |

## 1. The five components

The component list comes from `screening_criteria.md` §3 (RQ5 row), with "calibration or uncertainty estimation" split into two (ballot Item 16, option (c)):

| # | Component | Existing definition | Status of the definition |
|---|---|---|---|
| 1 | Biomarker/feature selection | **None for screening.** Only the search concept block F (`search_strategy.md` §3: "feature/variable/biomarker selection; recursive feature elimination; stability selection") | **Missing** (open issue Q-037a) |
| 2 | Classification | `screening_criteria.md` §2.3: supervised classification or risk-probability models (regularised regression, PLS-DA/OPLS-DA as classifiers, tree ensembles, SVM, k-NN, naive Bayes, neural networks, AutoML, tabular foundation models) | Exists (draft criteria v1.0) |
| 3 | Explainability | Proposed in D-029 (`final_confirmation_sheet_LIT-004.md` R5: `dim_explainability`) | **Proposed, not approved** (R5) |
| 4 | Probability calibration | Proposed in D-029 (`dim_calibration`) | **Proposed, not approved** (R5) |
| 5 | Uncertainty estimation | Proposed in D-029 (`dim_uncertainty`) | **Proposed, not approved** (R5) |

Calibration (4) and uncertainty estimation (5) are separate components. A framework that reports both counts two.

Also undefined: what it means for a framework to **cover** a component (open issue Q-037b). The question is whether the component must be part of the proposed or evaluated pipeline, or whether it is enough that the study reports it. The RQ5 row says "proposes or evaluates an integrated pipeline/framework covering …" but does not settle this.

## 2. Effect of ≥ 4 of 5 on RQ5 eligibility

A record is RQ5-eligible only if it covers at least 4 of the 5 components. Exactly six combinations qualify (S = selection, K = classification, X = explainability, C = calibration, U = uncertainty):

| Qualifying combination | Missing component |
|---|---|
| S + K + X + C | U |
| S + K + X + U | C |
| S + K + C + U | X |
| S + X + C + U | K |
| K + X + C + U | S |
| S + K + X + C + U | — |

Properties that follow from the rule `[EVIDENCE: arithmetic]`:
- Every qualifying framework covers **at least one of calibration and uncertainty**, and **at least one of selection and explainability**.
- A framework with classification covers at least three of {S, X, C, U}.

The hypothetical examples from the ballot and v1 §16:
- "Selection + classification + calibration" does **not** qualify (3 of 5).
- "Classification + calibration + uncertainty" does **not** qualify (3 of 5).
- "Selection + classification + explainability + calibration" qualifies.

**Compared with the current rule (≥ 3 of 4)** in draft criteria v1.0:
- Records that fall out of RQ5:
  - frameworks with three components, e.g. S + K + X (a classifier with feature selection and SHAP);
  - S + K + C/U, where calibration-or-uncertainty counted once.
- Records still in RQ5: those that cover calibration *and* uncertainty plus two others.

**Title/abstract stage** (as proposed in D-029; conditional on R5):
- Only `yes` counts toward the 4.
- A record that would reach 4 if its `unclear` components were `yes` is a *potential RQ5* record. It goes to full text (`uncertain`, `needs_human=yes`) and is not excluded.
- Final RQ5 membership is decided from full text.

**Retrieval context `[EVIDENCE]`.**
- `Q-PM-11` already requires selection terms ∧ ML ∧ explainability terms ∧ (uncertainty ∨ calibration ∨ Brier) terms. Its records were therefore retrieved because they *mention* roughly four components.
- `Q-PM-12` requires only a framework/pipeline title word and one of explainability, uncertainty or calibration.
- RQ5 eligibility applies to every screened record, not only to theme F retrievals.

## 3. Effect on the closest-prior-art assessment

- The closest-prior-art table (`research_plan.md` §8 item 3; `search_strategy.md` §8.3) is defined as the RQ5 set. Under ≥ 4/5 it contains fewer, more complete frameworks.
- Frameworks with exactly three components drop out of RQ5. They remain in the review only through RQ1–RQ4:
  - applied metabolic studies stay in RQ1, and in RQ2 or RQ3 where they qualify;
  - non-metabolic applied frameworks are `exclude E4` for RQ1. They are kept only if they qualify as `non_metabolic_method_exemplar` (they develop or evaluate the method itself).

  So some three-component frameworks from other domains will not be in the evidence base at all.
- `research_plan.md` §8 item 3 currently says "every pipeline that combines ≥ 3 components is described in detail". That wording conflicts with D-031 and must be updated when the conditions are met.

## 4. Is the threshold methodologically defensible?

This assessment does not consider which novelty conclusion either threshold would favour. It considers only the definition's fit to the research question and the risk of error.

**Points for the rule** `[EVIDENCE]` / reasoning:
1. **Pre-specified.** Chosen before any record is screened, so the definition cannot be tuned to the records found.
2. **Calibration and uncertainty are distinct properties.** Calibration concerns agreement between predicted probabilities and observed frequencies; uncertainty estimation concerns per-prediction uncertainty. The project already records them separately (D-026/D-029, proposed), and counting them separately is consistent with that.
3. **Matches the construct "integrated framework".** Every qualifying combination contains a reliability component (C or U) and an interpretability-or-selection component (X or S). That corresponds to the provisional research question's combination of explanation with calibrated probabilities and uncertainty (README, `research_plan.md` §1). A three-component rule admits routine combinations (e.g., selection + classifier + SHAP) that are already covered by RQ1/RQ2.
4. **Matches the retrieval design.** The main RQ5 query (`Q-PM-11`) was built around the same four-to-five components.

**Risks:**
1. **Overstated novelty.** A narrower closest-prior-art set makes "no prior framework combines …" easier to conclude. Three-component frameworks that are close to the provisional question would sit outside RQ5. Examples are classification + explainability + uncertainty, and classification + calibration + uncertainty.
2. **Loss at screening.** Non-metabolic three-component *applied* frameworks are E4 under the current criteria and would never reach the closest-prior-art assessment.
3. **Reporting incompleteness.** Abstracts often omit components. With silence = `unclear`, fewer records reach 4 at title/abstract. The potential-RQ5 rule mitigates this only if it is approved (R5).
4. **Undefined components.** Without operational definitions of feature selection and "covering", the count is not reproducible between screeners. This would show up as low pilot agreement on RQ5 tags.

**Conclusion `[RECOMMENDATION]`.** The threshold is defensible as a pre-specified definition of RQ5 membership, provided that:
- (i) all five components and "covering" are operationally defined before screening;
- (ii) the closest-prior-art assessment does not rely on the ≥ 4/5 set alone: frameworks with exactly 3 of 5 are identified and reported, so that a novelty conclusion does not depend on the threshold.

Item (ii) changes what is retained at screening (risk 2), so it is an owner decision (Q-038). It is not filled in here.

## 5. Conditions recorded with D-031

| ID | Condition | Resolved by | Pilot-blocking? |
|---|---|---|---|
| C1 | Operational definitions of explainability, calibration and uncertainty approved | R5 (D-029) in `final_confirmation_sheet_LIT-004.md` | Yes |
| C2 | Operational definition of the feature-selection component (e.g., whether embedded selection such as LASSO, PLS-DA VIP ranking, univariate filtering, or dimensionality reduction such as PCA count) | **Q-037a** (new) | Yes |
| C3 | Definition of "covering" a component (part of the proposed/evaluated pipeline vs merely reported) | **Q-037b** (new) | Yes |
| C4 | Owner decision on how frameworks with exactly 3 of 5 components are handled for the closest-prior-art assessment and at screening | **Q-038** (new) | Yes, for theme F records and the pilot's F stratum |

D-031 is applied in screening only after C1–C4 are resolved and written into criteria v1.1. Until then the RQ5 wording in draft criteria v1.0 stays as written. D-031 is not yet in force for any record, and none has been screened.

## 6. Dependent decisions and documents

| Item | Needed change once C1–C4 are met | Done now? |
|---|---|---|
| `screening_criteria.md` §3, RQ5 row | "≥ 3 of 4" → "≥ 4 of 5 (selection; classification; explainability; calibration; uncertainty estimation)" + C2/C3 definitions | No |
| `screening_criteria.md` §5, Tier 1 ("all RQ5") | Tier 1 then means ≥ 4/5 frameworks. Tier for 3/5 frameworks follows Q-038. Review whether "calibration/uncertainty" in the RQ1 Tier-1 rule should also be split (consistency; not decided by D-031) | No |
| `search_strategy.md` §6.5 (tiering text, source of criteria §5) | As above | No |
| `search_strategy.md` §1.2, RQ5 question | Currently "biomarker selection, classification, explainability, and uncertainty estimation". Calibration is missing. Wording to be aligned (it describes the question, not the threshold) | No |
| `search_strategy.md` §8.3 / `research_plan.md` §8 item 3 | Closest-prior-art table: "≥ 3 components" → D-031, plus the Q-038 reporting rule | No |
| `research_plan.md` §2, theme F row | "≥ 3 of {…}" → D-031 | No |
| A-3 (`screening_protocol.md` §9) | RQ5 part answered by D-031. Descriptor part still depends on R5 (D-029). A-3 remains **partly open** | No (status noted in the decision log) |
| D-026 | Its "RQ5 counting rule left to Q-028" is now answered by D-031. D-026 itself stays PROPOSED (R5) | Decision log note only |
| D-029 / R5 | The "potential RQ5" rule and human-review trigger 3 use threshold 4 | No (R5 pending) |
| `rq_tags` (RQ5) in `screening/decisions.csv` | Assigned under D-031. Format unchanged (`RQ1`–`RQ6`); no schema change | No |
| Screening schema | Only if a `dim_feature_selection` descriptor is chosen under Q-037a. Otherwise none | No |
| `screening_protocol.md` §3 (separate-dimensions row) and §7 (pilot) | RQ5 counting reference; pilot report includes agreement on RQ5 tags in the F stratum | No |
| D-025 pilot | F stratum screened under D-031 once C1–C4 are met | No |
| Stage D / D-016 (contribution, novelty) | Closest-prior-art basis = D-031 set + Q-038 reporting | — |
| `final_confirmation_sheet_LIT-004.md` R3 | Owner response entered | **Yes** |
| `unresolved_questions.md` Q-028 | Answered → D-031 (conditional); Q-037, Q-038 added | **Yes** |
