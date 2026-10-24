# Final Confirmation Sheet — LIT-004

| Field | Value |
|---|---|
| Task | LIT-004-FINAL-CONFIRMATION-SHEET (2026-10-24) |
| Status | **For the owner's explicit confirmation. Nothing is recorded, approved or implemented.** `logs/DECISION_LOG.md`, schemas, code, criteria, screening data and the pilot are unchanged |
| Built from | `owner_review_ballot_LIT-004.md` (authoritative ballot), `proposed_owner_responses_LIT-004.md` (v1), `clarification_addendum_LIT-004.md`. Text marked *verbatim* was copied programmatically from those files; the only edit is one cross-reference, noted where it occurs |
| After confirmation | Only the items the owner selects in R6 are written to `logs/DECISION_LOG.md`, each with its conditions. Implementation is a separate, later task |

## How responses are recorded

| Response | Meaning when recorded | Never becomes |
|---|---|---|
| **APPROVE** | Approved as worded in this sheet | — |
| **APPROVE (conditional)** | Approved only once the stated condition is met. Recorded with the condition as `APPROVED — CONDITIONAL: <condition>` | Unconditional approval. Removing a condition needs a new owner response |
| **REJECT** | Not adopted. The current state stays, and any named alternative stays open | — |
| **MODIFY** | Not approved. Reworded per the owner's comment and returned for confirmation | Approval |
| **DEFER** | Stays PROPOSED/OPEN with the owner's reason | Approval or rejection |

Unticked lines are treated as DEFER.

---

## R1 — D-024 (inventory schema revision), on its own

D-024 = the LIT-003 evidence-table fields and sentinels ("REQUIRES FULL-TEXT REVIEW", "NOT REPORTED", "NOT APPLICABLE"), taken together with the revised D-028 and D-029 definitions once those are confirmed.
**Approving R1 does NOT approve Q-034.** `extraction_status` stays a free string with no enforced values until R2 is answered.

Recommended: APPROVE (conditional on R5 being confirmed, because D-024 includes the D-029 descriptor fields).

R1 — D-024: [ ] APPROVE  [ ] APPROVE (conditional on R5)  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Comments:

## R2 — Q-034 (`extraction_status` values), separate from R1

*Verbatim from the clarification addendum §1:*

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

Necessary for the planned workflow: `not_extracted`, `abstract_only`, `full_text`. `in_progress` is optional.
**Recommended: option (b)**, because extraction will run over several sessions at about 1 h/day of owner time, and an unfinished record should be visible as such. This needs the owner's explicit confirmation.

R2 — Q-034: [ ] APPROVE option (a)  [ ] APPROVE option (b)  [ ] REJECT  [ ] MODIFY  [ ] DEFER
R2b — the three consistency checks (addendum §1): [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Comments:

## R3 — A-3 / Q-028: RQ5 component counting, decided before the pilot

*Verbatim from proposed response set v1, §16 (options as in the ballot, Item 16):*

Exact options, as in the ballot:
> **(a)** Keep four components, with calibration or uncertainty counted as one.
> **(b)** Five components (uncertainty and calibration separate), still ≥ 3.
> **(c)** Five components, ≥ 4.

Components (from `screening_criteria.md` §3, RQ5): biomarker/feature selection; classification; explainability; calibration or uncertainty estimation. Under (b) and (c), calibration and uncertainty count separately.

Consequences, described without preference:

| Option | Which frameworks qualify as closest prior art (RQ5) | Example (hypothetical, for illustration only) | Effect on later work |
|---|---|---|---|
| (a) | ≥ 3 of 4. Calibration and uncertainty together contribute at most one | Selection + classification + calibration qualifies. Classification + calibration + uncertainty does **not** (2 components) | Keeps the current definition. Frameworks that combine calibration and uncertainty without feature selection or explainability fall outside RQ5 |
| (b) | ≥ 3 of 5 | Both examples qualify | The RQ5 set is the largest of the three, and more papers enter the closest-prior-art table that must be complete before any novelty claim. More full-text work for theme F |
| (c) | ≥ 4 of 5 | Neither example qualifies; e.g. selection + classification + explainability + calibration is needed | The RQ5 set is the smallest, limited to more complete frameworks. Fewer papers in the closest-prior-art table, and partial combinations are described under RQ2–RQ4 instead |

**Why decide before the pilot.**
1. *Pre-specification.* The rule decides which papers count as closest prior art, and later novelty conclusions rest on it. Fixing it before any record is screened prevents choosing the definition after seeing which papers it admits.
2. *Pilot validity.* For a non-metabolic framework RQ5 can be the only route to inclusion. With the rule fixed, the 6 theme-F pilot records stay inside the agreement statistics (κ, code agreement) instead of being set aside.
3. *Operational reliability.* There is no provisional flag, no separate statistics, no re-adjudication and no re-screening.

The alternative (defer, with `rq5_provisional` labels) is specified in the clarification addendum §2 and remains available. Choosing it requires DEFER here plus the addendum's R3 approach II.

**Every criterion and workflow item that depends on Q-028:**
| Dependent item | How it depends |
|---|---|
| `screening_criteria.md` §3, RQ5 row | The rule text itself (≥ 3 of 4, or of 5, or ≥ 4 of 5) |
| A-3 (`screening_protocol.md` §9) | A-3 = separate descriptors **and** the RQ5 counting rule; the A-3 response follows R3 |
| `screening_criteria.md` §5, Tier 1 ("all RQ5") | Which records are Tier 1, i.e. read in full text first |
| `rq_tags` (RQ5) in `screening/decisions.csv` | Which records receive the RQ5 tag |
| D-029 "potential RQ5" rule and human-review trigger 3 | The threshold the rule is applied to (see R5) |
| Inclusion of non-metabolic frameworks (E4/E12 vs include) | RQ5 is their only route to inclusion |
| D-025 pilot: F stratum (6 records), agreement statistics | Whether those records can be decided in the pilot |
| Full-text workload for theme F (141 retrieved publications) | Size of the RQ5 set |
| Closest-prior-art table (`search_strategy.md` §8.3) and RQ5 evidence table | Its membership |
| Gap assessment and any novelty claim (Stage D, D-016) | Its basis |
| Optional `dim_feature_selection` descriptor (addendum §2) | Needed only to derive RQ5 mechanically. Otherwise feature selection is read from the abstract with a written justification |

R3 — timing: [ ] APPROVE "decide before the pilot"  [ ] REJECT (use provisional labels, addendum §2)  [ ] MODIFY  [ ] DEFER
R3 — option (only if deciding now): [ ] (a)  [ ] (b)  [ ] (c)
R3 — A-3: [ ] APPROVE together with the option chosen above  [ ] DEFER
Comments:

## R4 — D-030 retraction procedure (CONDITIONAL)

The D-030 link model (reversible links, no merging, the counting specification in ballot Item 4) is proposed **with** this retraction procedure. The procedure is **conditional**: it is not adopted until **each** sub-item below is approved. If any sub-item is not approved, the procedure as a whole remains unapproved, and no record is excluded on retraction grounds except under the existing Stage-0 rule (*Retracted Publication* → E7).

*Verbatim from the clarification addendum §3:*

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

| Sub-item | Exact content to approve |
|---|---|
| R4a Stage 0 | Extend `search_strategy.md` §6.1: *Retraction of Publication*, *Correction* and *Expression of Concern* records → `exclude E5` (notice), alongside the existing *Editorial, Comment, News, Published Erratum* (E5) and *Retracted Publication* (E7) |
| R4b E5/E7 | E7 only for a record that is itself retracted or withdrawn (source type, linked notice, or the version's own server/journal notice). E5 for every notice type |
| R4c E12 | E12 for a related version only when the notice's quoted reason invalidates **shared** data or results, with the notice identifier and reason cited in the justification |
| R4d Human review | Every related preprint/journal version of a retracted record; every expression-of-concern article that is included; any case with no notice text or an unclear reason (stays `uncertain`, never excluded) |
| R4e Sensitivity analysis and records | With/without analysis for records flagged `related_to_retracted` or `expression_of_concern`. Method in `search_strategy.md` §8.3; results in the Stage C review (`literature_review.md`, planned); cases in an append-only `records/retraction_review.csv` |

R4a: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
R4b: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
R4c: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
R4d: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
R4e: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
R4 — D-030 link model (ballot Item 4 without its original group-retraction rule): [ ] APPROVE  [ ] APPROVE (conditional on R4a–R4e)  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Comments:

## R5 — D-029 complete definitions

*Verbatim from the clarification addendum §4 (one cross-reference adjusted to point to the addendum):*

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
- Feature selection has no descriptor. For the threshold it is read from the abstract and justified in writing, unless `dim_feature_selection` is added (see clarification addendum §2).

**Dependencies that must be settled before D-029 is implemented:**
| Dependency | Why |
|---|---|
| R5 itself (each definition below) | The definitions are not final until approved |
| D-026 | Revised by D-029. Recorded as "revised by D-029" only when R5 is approved |
| D-027 (v1 Item 1) | The screening-file columns: `dim_independent_validation` is replaced by `validation_design` |
| D-024 (R1) | The inventory schema carries the same fields |
| R3 / Q-028 | The threshold used by the "potential RQ5" rule and human-review trigger 3 |
| Q-035 `biomarker_class` (v1 Item 7) | Whether it is required with the descriptors for include/uncertain |
| A-6 (v1 Item 15) | The missing-abstract rule relies on it |
| `dim_feature_selection` (addendum §2) | Only if RQ5 is to be derived mechanically |
| `screening_criteria.md` v1.1 and protocol v0.2 | The approved wording must be written into them and frozen as the pilot's `criteria_version` |
| D-025 pilot | Measures descriptor agreement. Disagreements may lead to a new criteria version |

R5 — `dim_explainability`: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
R5 — `dim_uncertainty`: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
R5 — `dim_calibration`: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
R5 — `validation_design`: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
R5 — common rules (silence = `unclear`, missing abstracts): [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
R5 — human-review triggers: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
R5 — RQ5 handling of ambiguity: [ ] APPROVE  [ ] APPROVE (conditional on R3)  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Comments:

## Other items of proposed response set v1 (unchanged; for confirmation)

*Verbatim summary from v1:*

| # | ID | Proposed response | Conditions / open dependencies kept |
|---|---|---|---|
| 1 | D-027 | APPROVE (limited) | Only the file, key scheme and required columns. Descriptor columns follow Items 2, 3 and 7 |
| 2 | D-028 | 2a APPROVE · 2b APPROVE · 2c REJECT · 2d APPROVE | Mapping table versioned; every extension logged |
| 3 | D-029 (+ D-026) | APPROVE option (a), **conditional** | Final wording of the definitions (ballot Item 3, C-3 to C-6) to be confirmed before implementation; silence = `unclear` |
| 4 | D-030 | **MODIFY** | Group-level retraction rule replaced by the procedure in §4 below |
| 5 | Q-024 / Q-029 | APPROVE ballot option (c): defer all 15 pair decisions until after the pilot | Who decides after the pilot is still open. Q-029 follows D-030 |
| 6 | Q-001 | APPROVE (main list provisional) | Obesity, thyroid dysfunction and PCOS **remain pending** |
| 7 | Q-002 / Q-035 | APPROVE | `biomarker_class` values as in the ballot. Required status follows Item 3 |
| 8 | Q-033 | APPROVE option (a): proteomics **remains pending** | Flag `scope_pending_proteomics` |
| 9 | Q-007 / D-009 | APPROVE option (a): screen all 743 | Exclusions counted by code; recall limitations reported. Depends on Items 6–8 |
| 10 | Q-022 (D-005, D-006, D-007) | APPROVE option (a): as executed, with limitations | All 30 unexecuted searches listed; no comprehensiveness claim. Ballot option (b) (re-run when access exists) neither chosen nor excluded |
| 11 | D-012 / D-023 / Q-036 | APPROVE: arXiv spot-check to be run; web-file checks documented as not performed | D-012/D-023 approval **conditional on the arXiv spot-check outcome**. A failed check reopens the item |
| 12 | D-010 / Q-011 | APPROVE option (a) | **No off-device backup exists**; recorded as a limitation, not as resolved |
| 13 | D-008 / Q-008 | APPROVE | — |
| 14 | D-025 / Q-026 | APPROVE | Pilot generated only after every pilot-blocking item is recorded (section A) |
| 15 | A-1, A-2, A-5, A-6 / A-4 / A-3 | A-1, A-2, A-5, A-6 APPROVE · A-4 REJECT (in favour of D-030) · A-3 DEFER | A-3 depends on Item 16 |
| 16 | A-3 / Q-028 | **DEFER** | Options reproduced in §16 below without a recommendation |
| 17 | D-024 | APPROVE with the revised D-028 and D-029 | Q-034 enum not mentioned in the prompt; see §17 |

Changes from v1 introduced by this sheet:
- **Item 3 (D-029)** is now answered through R5.
- **Item 4 (D-030)** is answered through R4.
- **Item 16 (Q-028)** was DEFER in v1; R3 now asks whether to decide it before the pilot. v1's DEFER remains a valid answer.
- **Item 17 (D-024)** is answered through R1, and Q-034 through R2.

V1 items 1, 2, 5–15: [ ] CONFIRM all as in v1, with their conditions  [ ] CONFIRM except: …  [ ] DEFER all
Comments:

## R6 — Recording

[ ] **Record all confirmed items**: every line marked APPROVE / APPROVE (conditional) / REJECT above, with its conditions, plus MODIFY/DEFER lines recorded as still open
[ ] **Record selected confirmed items only**: …
[ ] **Record nothing yet**
Comments:

---

## Pilot-blocking items after confirmation

Even with every line approved, the pilot sample is **not** generated until:
1. **R3 / Q-028** is decided (option (a), (b) or (c)), or the owner chooses the provisional-label alternative instead.
2. **R5 / D-029** definitions are all approved.
3. **R1 / D-024** and **v1 Item 1 / D-027** are recorded, so the schema the pilot writes into is fixed.
4. **R2 / Q-034** — not pilot-blocking (extraction comes after screening), but needed before extraction.
5. **R4 / D-030** — not pilot-blocking for the current data (no retraction notices or related versions of the 3 retracted articles), and the 15 pairs are deferred until after the pilot (v1 Item 5). It must be decided before pair decisions or any new data containing notices.
6. **v1 Item 11:** the arXiv spot-check runs and passes, so that D-012/D-023, and with them Q-022 (v1 Item 10), can be recorded.
7. **v1 Items 6–9, 13–15** (scope, Q-PM-02, audit, pilot design, A-1/A-2/A-5/A-6) are recorded.
8. **Implementation** of D-027 (already built), D-028, D-029, `biomarker_class` and the scope flags, with tests and a rebuild that changes no paper ID or existing value.
9. `screening_criteria.md` **v1.1** and protocol **v0.2** are written with the approved wording and frozen as the pilot's `criteria_version`.

Not pilot-blocking: D-010 (v1 Item 12), Q-024 pair decisions (deferred until after the pilot), Q-034 (before extraction).
