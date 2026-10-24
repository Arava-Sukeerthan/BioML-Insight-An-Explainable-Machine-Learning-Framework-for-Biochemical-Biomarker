# Clarification Addendum — LIT-004 (for owner review)

| Field | Value |
|---|---|
| Task | LIT-004-CLARIFICATION-ADDENDUM (2026-10-24) |
| Status | **PROPOSED. Not recorded, not approved, not implemented.** It clarifies five open points in `proposed_owner_responses_LIT-004.md` (v1). The ballot (`owner_review_ballot_LIT-004.md`) and `logs/DECISION_LOG.md` are unchanged |
| Answers | Section 5 has one response field per unresolved choice. The other items of the proposed response set are unaffected |

Labels: `[EVIDENCE]` from project files/data; `[RECOMMENDATION]` assistant proposal; `[OPEN]` owner choice.

---

## 1. D-024 and Q-034 (`extraction_status`), presented separately

**Current state `[EVIDENCE]`.**
- In `schemas/paper_inventory.schema.json`, `extraction_status` is a free string or null. Its description reads "not_extracted / abstract_only / full_text", but nothing enforces those values.
- All 2,979 inventory rows are `not_extracted`, which is the value the report script writes.
- The workflow needs extraction from the abstract only in two cases:
  - Tier-3 records "coded from the abstract" (`screening_criteria.md` §5);
  - full text unavailable (`search_strategy.md` §6.3; `research_plan.md` §7: values "flagged `abstract_only`").
- It needs extraction from full text for Tier 1 and 2 records. The researcher spot-checks 5 extracted records (`search_strategy.md` §8.1).

**D-024 on its own** = the LIT-003 evidence-table fields and sentinels, with `extraction_status` remaining a free string as now. Approving D-024 does **not** approve any value list for `extraction_status`.

**Q-034 (separate): proposed value lists**
| Option | Values |
|---|---|
| (a) Minimal: the three values already in the description | `not_extracted`, `abstract_only`, `full_text` |
| (b) Minimal + work in progress | `not_extracted`, `in_progress`, `abstract_only`, `full_text` |

| Value | Definition | Example |
|---|---|---|
| `not_extracted` | No extraction has started. **Default for every record**, whatever its screening status | All 2,979 records today; an included record waiting in the queue |
| `in_progress` (option b only) | Extraction started but not finished: some fields are still "REQUIRES FULL-TEXT REVIEW" | The assistant has coded the dataset and models of P0123 but not yet the metrics table |
| `abstract_only` | Extraction finished **from the abstract only**. Every field has a value or "NOT REPORTED"/"NOT APPLICABLE", and the record is flagged for synthesis | A Tier-3 study coded from its abstract; a study whose full text cannot be obtained |
| `full_text` | Extraction finished from the full text. Every field has a value or "NOT REPORTED"/"NOT APPLICABLE"; none is "REQUIRES FULL-TEXT REVIEW" | A Tier-1 study extracted from the PMC full text |

**How the five states are told apart, without adding eligibility to this field:**
| State | Represented by |
|---|---|
| Ineligible | `screening_status = exclude` (one source of truth). Proposed check: `extraction_status` must stay `not_extracted` for such records. There is no separate "ineligible" value, which would duplicate the screening decision and could contradict it |
| Pending | `screening_status = include` (or full-text `abstract_only`) **and** `extraction_status = not_extracted` |
| Incomplete | Option (b): `in_progress`. Option (a): not represented; only visible from remaining "REQUIRES FULL-TEXT REVIEW" sentinels |
| Completed from the abstract | `abstract_only` |
| Completed from full text | `full_text` |

Proposed consistency checks (to be implemented only after approval):
- `full_text` requires no remaining "REQUIRES FULL-TEXT REVIEW" sentinel;
- `abstract_only` / `full_text` require an `include` (or full-text `abstract_only`) screening status;
- a screening decision `abstract_only` (full-text stage) allows at most `extraction_status = abstract_only`.

Note: the name `abstract_only` is used both as a screening decision and as an extraction status. The meanings are related but not identical.

**Necessary for the planned workflow:** `not_extracted`, `abstract_only`, `full_text`. `in_progress` is optional. It helps when extraction runs over several sessions, which is likely at roughly 1 h/day of owner time.
`[RECOMMENDATION]` option (b). This is not a choice made for the owner.

---

## 2. A-3 / Q-028 and the pilot

**The three options, verbatim from the ballot (Item 16):**
> **(a)** Keep four components, with calibration or uncertainty counted as one.
> **(b)** Five components (uncertainty and calibration separate), still ≥ 3.
> **(c)** Five components, ≥ 4.

Components (`screening_criteria.md` §3, RQ5): biomarker/feature selection; classification; explainability; calibration or uncertainty estimation. RQ5 accepts any domain as closest prior art.

| Option | Definition | Consequence |
|---|---|---|
| (a) | ≥ 3 of 4, with calibration and uncertainty together counting as one | Current definition. Frameworks that combine calibration and uncertainty without selection or explainability are outside RQ5 |
| (b) | ≥ 3 of 5 | Largest RQ5 set; more theme F full-text work. The closest-prior-art table (needed before any novelty claim) is broadest |
| (c) | ≥ 4 of 5 | Smallest RQ5 set; only more complete frameworks. Partial combinations are described under RQ2–RQ4 |

**Why the timing matters `[EVIDENCE]`.** 141 publications were retrieved by theme F queries, and the pilot draws 6 records from the F stratum. For a non-metabolic framework, RQ5 can be the *only* route to inclusion. Its include/exclude decision therefore depends on which option is chosen.

**Comparison of the two approaches**
| Criterion | I. Decide Q-028 before generating the pilot | II. Defer Q-028; provisional RQ5 labels in the pilot |
|---|---|---|
| Bias | Rule fixed **before** any record is screened: no risk of choosing the definition after seeing which papers it admits (a known source of bias when a novelty claim depends on it) | Rule chosen **after** pilot records have been seen. The risk is limited by the safeguards below but not removed |
| Validity of the pilot | Pilot tests the final rule. κ and code agreement cover the F stratum | F records whose eligibility depends on RQ5 are removed from the main agreement statistics. With only 6 F records, the pilot may then say little about theme F |
| Operational load | One owner decision now | A new flag, separate statistics, later re-adjudication, possible second look at F records |
| Re-screening risk | None from Q-028 | Re-adjudication of every flagged record after the decision |
| Delay | The owner must decide before the pilot | None now |

**If approach II is chosen: specification of the provisional labels**
1. **Representation.**
   - Screeners record the component evidence (the D-029 descriptors for explainability, uncertainty and calibration) as usual.
   - Each record whose RQ5 status would differ between options (a), (b) and (c) gets `scope_flags` value `rq5_provisional`.
   - If such a record's eligibility depends on RQ5 alone, its decision is `uncertain` with `needs_human=yes` and the justification "RQ5 rule pending (Q-028)".
   - *Gap:* feature selection is not a recorded descriptor. Deriving RQ5 mechanically under any option would need an extra descriptor (`dim_feature_selection`: yes/no/unclear), which is a schema addition requiring separate approval.
2. **Excluded from final eligibility.** No `rq5_provisional` record may be `include`d or `exclude`d on RQ5 grounds until Q-028 is recorded. Final eligibility is set by applying the recorded rule to the recorded components.
3. **Later adjudication.**
   - After Q-028 is recorded, each flagged record is re-decided by both screeners with the fixed rule, blind to each other.
   - The new decision is a new row; the provisional row is kept, since the file is append-only.
   - Disagreements are adjudicated by the owner.
4. **No contamination of agreement statistics.**
   - The main κ and code agreement are computed on non-flagged records only. The number of flagged records is reported.
   - Agreement on flagged records is reported separately, first on the component descriptors and later on the re-adjudicated decision.
   - The pass criteria apply to the main statistics only.
   - The flag is assigned by a written rule fixed before screening, never chosen to improve agreement.

**`[RECOMMENDATION]`: approach I** (decide Q-028 before generating the pilot) is the least biased and the most operationally reliable:
- it pre-specifies a rule that later novelty conclusions depend on;
- it keeps the F stratum inside the pilot's agreement statistics;
- it needs no new flag or re-adjudication.

This is a recommendation only. The approach, and the option (a)/(b)/(c), are the owner's choices.

---

## 3. D-030: revised retraction procedure (for approval)

**Principles.**
1. Every record keeps its paper ID, metadata and provenance. Nothing is merged or deleted.
2. A retraction applies to the retracted article. **A related version is never excluded automatically because its primary (or any linked record) is retracted.**
3. Every decision is a row with evidence and a reviewer, so it can be reversed.

| Record | What it is | Handling | Evidence required | Human review |
|---|---|---|---|---|
| **Retracted article** | The article that was retracted; PubMed type *Retracted Publication*, or the target of a linked retraction notice | `exclude E7` at Stage 0 (existing rule, `search_strategy.md` §6.1) | Source type, or a `retraction_of` link with the notice | Only if the metadata conflict |
| **Retraction notice** | The separate notice announcing the retraction (*Retraction of Publication*) | `exclude E5` (notice, not a study); linked `retraction_of` → article | Source type | No |
| **Correction notice** | Erratum/corrigendum (*Published Erratum*, *Correction*) | `exclude E5` at Stage 0 (existing for *Published Erratum*); linked `correction_of`. **The corrected article is screened normally**, and the correction is applied at extraction | Source type | No |
| **Expression of concern** | Editorial notice that the article's reliability is in question (*Expression of Concern*) | Notice: `exclude E5`, linked `correction_of`. **The article is not excluded**: it is screened normally, flagged `expression_of_concern` (a value already named in the schema's `scope_flags` description), and handled in the sensitivity analysis | Source type | Yes, if the article is included: the flag is checked at extraction |
| **Related preprint / journal version** | Another report of the same work (`version_of`), e.g. the preprint of a retracted journal article | **Not excluded automatically.** Set `uncertain`, `needs_human=yes`; decided by the evidence rules below | The retraction notice's stated reason; the version's own status at its server/journal | **Always** |
| **Duplicate web copy** | The same publication at another URL (`duplicate_of`) | Counted once as a duplicate (`duplicate_removed`) of its primary. If that primary is the retracted article, the copy shares the article's status, because it *is* that publication. It keeps its own ID and provenance | The `duplicate_of` link and its evidence | Only for the link itself |

**When E7 or E12 may apply to a related version.**
| Code | Allowed only when | Evidence to cite in the justification |
|---|---|---|
| E7 (Retracted) | The version **itself** has been retracted or withdrawn by its own server or journal | The notice or withdrawal statement for that version (identifier, date) |
| E12 (catch-all; justification mandatory under A-2) | The notice for the related article states a reason that invalidates the **shared** data or results (fabricated, falsified or unreliable data; unreliable analysis; duplicated data), and the version uses the same data/results | The notice identifier, its stated reason (quoted), and why the version shares the affected data |
| Neither | The stated reason does not concern the data or results (publisher error, journal-level duplicate publication, authorship/consent dispute not affecting findings) | The notice and its stated reason. The version is screened normally and flagged `related_to_retracted:Pxxxx` |
| — (insufficient evidence) | No notice text, or the reason is unclear | Stays `uncertain`, `needs_human=yes`, listed in the adjudication queue. **Not excluded** |

**Sensitivity analysis.**
- Every synthesis count or evidence table that includes a record flagged `related_to_retracted` or `expression_of_concern` is reported twice: with and without those records.
- Planned documentation:
  - the method in `search_strategy.md` §8.3 (a synthesis amendment, needing approval);
  - the results in the Stage C review document (`literature_review.md`, planned), in a section "Sensitivity: records related to retractions or expressions of concern";
  - each case in a proposed append-only register `records/retraction_review.csv` with columns `paper_id, related_paper_id, relation, notice_id, stated_reason, decision, code, reviewer, date, evidence`.

**Changes this would need (not made now):**
- **Stage 0 extension.** Stage 0 currently covers *Editorial, Comment, News, Published Erratum, Retracted Publication*. Adding *Retraction of Publication*, *Correction* and *Expression of Concern* (notices → E5) is a change to `search_strategy.md` §6.1 and needs approval.
- **E12 use.** Using E12 for invalidated evidence is an interpretation of the existing catch-all code. No code is added or changed.

**Current data `[EVIDENCE]`.** The 3 retracted articles (P0931, P0939, P1443) have no linked or flagged related records, and there are no retraction notices or expressions of concern. The procedure affects no current record.

---

## 4. D-029: complete proposed definitions

**Common rules.**
- Values describe what the **title and abstract state** (at title/abstract stage) or the full text states (at full-text stage).
- Silence is never `no`: abstracts omit methods, so absence of mention is not evidence of absence.
- Required for `include` and `uncertain`; optional for `exclude`.
- **Missing abstract** (119 records):
  - every method descriptor and `validation_design` = `unclear`;
  - the decision is `uncertain` unless a title-level Stage-0/E1/E4 reason applies (A-6);
  - the descriptors are completed at full text.

| Descriptor | Values | Evidence required for `yes` | Conditions for `no` | Conditions for `unclear` |
|---|---|---|---|---|
| `dim_explainability` | yes / no / unclear | A **named** explanation or attribution method applied to the model's predictions: SHAP, LIME, permutation importance, partial dependence/ICE, counterfactuals, attention analysis, rule extraction, or model coefficients/odds ratios **presented as the explanation** | The abstract states that no explanation was produced, or describes the full analysis and it clearly contains none (e.g., "we report only AUC" with no model interpretation) | "Interpretable", "explainable" or "transparent" without a named method; built-in feature importance without a named procedure; "important biomarkers were identified" without saying how; no abstract |
| `dim_uncertainty` | yes / no / unclear | A **named** estimate of predictive uncertainty for individual predictions: conformal prediction sets/intervals, Bayesian posterior predictive uncertainty, Monte-Carlo dropout, deep or bootstrap ensembles **used to quantify uncertainty**, selective prediction/abstention with a stated uncertainty score | Stated absence, or a fully described analysis with point predictions only | "Ensemble" or "random forest" without an uncertainty use; confidence intervals of a **performance metric** only (this is uncertainty about the metric, not about predictions); "reliable"/"robust"; no abstract |
| `dim_calibration` | yes / no / unclear | **Probability** calibration assessed or corrected, named: calibration plot/curve, calibration slope or intercept, ECE/MCE, Hosmer–Lemeshow, Spiegelhalter's test, or recalibration (Platt, isotonic, temperature scaling) | Stated absence; or "calibration" used only in the **analytical-chemistry** sense (instrument or standard calibration curves), with this stated in the justification | Brier score alone (it mixes calibration and discrimination); "well-calibrated" without a method; no abstract |
| `validation_design` | external / temporal / internal_only / none / not_applicable / unclear | — (a design, not yes/no) | — | — |

| `validation_design` value | Assigned when the abstract states … |
|---|---|
| `external` | Evaluation on a different cohort, site, centre, country or public dataset than the one used for development |
| `temporal` | Evaluation on later patients from the same source (a time split) |
| `internal_only` | Only cross-validation, bootstrap, or a random hold-out split of the development cohort |
| `none` | Only apparent (training-set) performance |
| `not_applicable` | No predictive model is evaluated (reviews, guidelines, purely theoretical methods papers) |
| `unclear` | No design stated; "independent test set" / "validation cohort" without saying whether it is from the same cohort; no abstract |

The strongest stated design is recorded (external > temporal > internal_only > none).

**Human-review triggers (`needs_human=yes`).**
1. A term with two possible meanings that the abstract does not settle ("calibration", "ensemble", "interpretable", "validation cohort").
2. An otherwise RQ4-eligible record with `validation_design = unclear`.
3. Any **potential RQ5** record (next point).
4. A record without an abstract retained as `uncertain`.
5. Any descriptor disagreement between the two pilot screeners.

**How ambiguity affects RQ5.**
- At title/abstract, only `yes` counts toward the RQ5 component threshold.
- A record is a **potential RQ5** record if counting its `unclear` components as `yes` would reach the threshold (of the option chosen in Q-028).
- Potential RQ5 records go to full text (`uncertain`, `needs_human=yes`) rather than being excluded.
- The closest-prior-art table is built **only from components confirmed at full text**, so `unclear` never enters it as a component.
- Feature selection has no descriptor. For the threshold it is read from the abstract and justified in writing, unless `dim_feature_selection` is added (see §2).

---

## 5. Owner response fields

Mark one option per line. These answers will be recorded in `logs/DECISION_LOG.md` only after the owner confirms that they are to be recorded.

**R1 — D-024 (without any `extraction_status` value list)**
Owner response: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

**R2 — Q-034 (`extraction_status` values; §1)**
Owner response: [ ] APPROVE option (a) three values  [ ] APPROVE option (b) four values  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Also approve the three consistency checks in §1? [ ] YES  [ ] NO  [ ] MODIFY
Owner comments:

**R3 — Q-028 timing (§2)**
Owner response: [ ] Approach I: decide before the pilot  [ ] Approach II: defer with provisional labels  [ ] DEFER
If approach I, Q-028 option: [ ] (a)  [ ] (b)  [ ] (c)
If approach II, also add `dim_feature_selection`? [ ] YES  [ ] NO
Owner comments:

**R4 — D-030 retraction procedure (§3)**
Procedure as a whole: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Stage 0 extension (*Retraction of Publication*, *Correction*, *Expression of Concern* → E5): [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
E12 for evidence invalidated by a retraction (with mandatory justification): [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Register `records/retraction_review.csv` and the sensitivity analysis: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

**R5 — D-029 definitions (§4)**
`dim_explainability`: [ ] APPROVE  [ ] MODIFY  [ ] DEFER
`dim_uncertainty`: [ ] APPROVE  [ ] MODIFY  [ ] DEFER
`dim_calibration`: [ ] APPROVE  [ ] MODIFY  [ ] DEFER
`validation_design`: [ ] APPROVE  [ ] MODIFY  [ ] DEFER
Missing-abstract rule, human-review triggers, RQ5 handling: [ ] APPROVE  [ ] MODIFY  [ ] DEFER
Owner comments:

**R6 — Recording**
[ ] Record proposed response set v1 together with R1–R5 as answered above
[ ] Record only the following items: …
[ ] Do not record yet
Owner comments:
