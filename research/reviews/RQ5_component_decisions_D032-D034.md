# RQ5 component decisions: D-032 (Q-037a), D-033 (Q-037b), D-034 (Q-038)

| Field | Value |
|---|---|
| Task | RQ5-DECISIONS (2026-10-24) |
| Source of the decisions | The owner's prompt of 2026-10-24 ("Consolidated Decision Implementation and Governance Reconciliation"), which states 15 owner choices as authoritative. Recorded here by content |
| Recorded status | **D-032, D-033, D-034: APPROVED — CONDITIONAL. Inactive for screening.** None of them governs any screening decision until the activation conditions in §7 are met |
| Screening | **Not started.** No record has a component status; the pilot has not been generated |
| Related | D-031 (RQ5 ≥ 4 of 5, APPROVED — CONDITIONAL); D-029/R5 (descriptor definitions, PROPOSED); D-027 (screening format, PROPOSED); `Q-037a_feature_selection_proposal.md`; `Q-028_owner_decision_record.md` |

## 1. Provenance and option labels `[EVIDENCE]`

- **Q-037a.** The proposal in this repository (`Q-037a_feature_selection_proposal.md` §9) has five response fields. Their answer labels differ from those in the owner's prompt, so the choices are recorded by their stated content:

  | Owner's prompt | Repository field | How recorded |
  |---|---|---|
  | R-Q037a-1 "Option B" | R-Q037a-1 option B | Direct match |
  | R-Q037a-2 "Option C" | R-Q037a-2 offered "do not count / count / DEFER" | The owner's content: a reused panel alone does not count, a new procedure is assessed independently, the study is not excluded for this reason, and reuse is tracked. This adds to "do not count" |
  | R-Q037a-3 "Option A" (strict evidence) | R-Q037a-3 APPROVE / … | Recorded as approval of strict evidence rules, as stated by the owner (§2.3) |
  | R-Q037a-4 "Option A" (add descriptor) | R-Q037a-4 APPROVE | Direct match |
  | R-Q037a-5 "Option A" (conditionally approved) | R-Q037a-5 "Record" | Recorded; status APPROVED — CONDITIONAL |

- **Q-037b and Q-038.** The repository holds only the open questions (`unresolved_questions.md`, Q-037(b) and Q-038). No proposal or option list for them exists in the repository. The option letters in the owner's prompt refer to a review held outside the repository; the choices are recorded by their stated content.
- **Identifiers.** No D-ID existed for Q-037b or Q-038. Following the log's sequential convention, they are recorded as **D-033** (Q-037b) and **D-034** (Q-038). D-032 is the existing ID for Q-037a.

## 2. The 15 decisions

### 2.1 D-032: Q-037a, the feature/biomarker-selection component
| ID | Owner choice | Content recorded |
|---|---|---|
| R-Q037a-1 | Option B | Feature selection = a data-driven procedure in the current study that reduces candidate predictors to a **subset of original variables**, used as model input or reported as a panel. It is distinct from transformation (e.g., PCA alone) and from interpretation (importance used only to explain a model trained on all variables), and from shrinkage that removes nothing. Qualifying examples: filtering with a stated criterion; wrapper subset search; embedded retention (non-zero lasso/elastic-net terms); PLS-DA VIP thresholds used to retain variables. The full operational definition, caveats and human-review triggers in `Q-037a_feature_selection_proposal.md` §4–§6 apply; the examples do not replace them |
| R-Q037a-2 | Option C | Selection performed or evaluated in the current study is distinguished from reuse of a previously published panel. **Reuse alone does not satisfy** the component. A new qualifying procedure in the same study is assessed independently. Reuse of a panel is **not** a reason to exclude a study from the review: the rule concerns component classification, not relevance |
| R-Q037a-3 | Option A | Strict evidence. `yes`: a qualifying procedure **and** the retained subset of original variables are supported by evidence. `no`: evidence establishes that no qualifying procedure was performed. `unclear`: insufficient or ambiguous. Mentions of importance, a panel or a reduced predictor set are not enough for `yes`. Silence is not `no` |
| R-Q037a-4 | Option A | Add the descriptor `dim_feature_selection` (`yes` / `no` / `unclear`). Track reuse of published panels separately where the current schema supports it (§5.2) |
| R-Q037a-5 | Option A | D-032 is APPROVED — CONDITIONAL. The definition stays **inactive for screening** until its dependencies are resolved. This is not authorization to screen |

### 2.2 D-033: Q-037b, component-coverage evidence
| ID | Owner choice | Content recorded |
|---|---|---|
| Q-037b-1 | Option A | A component counts only with evidence that the procedure was **actually applied or evaluated**. A mention in the introduction, related work or proposed architecture is insufficient. A negative or unsuccessful result does not invalidate coverage if the procedure was genuinely performed and documented |
| Q-037b-2 | Option A | Only implemented or evaluated components count toward RQ5. Proposed but unimplemented components do not count. They may be recorded separately for description, provided they cannot be confused with implemented coverage |
| Q-037b-3 | Option A | Sufficient methodological evidence is required that the procedure was genuinely implemented or evaluated. Full independent reproducibility and public code are **not** universal requirements. A favourable metric alone is not evidence |
| Q-037b-4 | Option A | Three values: `yes` (evidence supports implementation/evaluation), `no` (evidence establishes it was not done), `unclear` (insufficient or ambiguous; flagged for human review). Missing information is never `no` |
| Q-037b-5 | Option A | A shared evidence framework across the five components, with component-specific criteria (§4) |

### 2.3 D-034: Q-038, studies with three of five components
| ID | Owner choice | Content recorded |
|---|---|---|
| Q-038-1 | Option A | D-031's threshold is kept. Coverage groups: `qualified` (≥ 4 confirmed `yes`), `near_rq5` (exactly 3), `below_threshold` (0–2). The threshold is not lowered. The group is not a quality measure |
| Q-038-2 | Option B | Exactly three confirmed `yes` → `near_rq5` (provisional), even with other components `unclear`. Unresolved statuses and human-review flags are kept. `unclear` never counts as `yes`. `qualified` requires ≥ 4 confirmed `yes` |
| Q-038-3 | Option B | A separate near-RQ5 analysis and a structured comparison with the qualified group are planned (counts, component combinations, commonly missing components, methodological patterns, comparable reported performance). No causal claim that more components improve performance. Differences in datasets, tasks and evaluation protocols are accounted for. **Nothing is counted before screening and validation** |
| Q-038-4 | Option A | ≥ 4 confirmed `yes` qualifies even if the fifth is `unclear`. The flag is kept, five-component coverage is not claimed, and resolving the fifth is not an eligibility condition |
| Q-038-5 | Option A | A derived field `rq5_coverage_group` is computed from the five component statuses, not assigned by screeners. Values `qualified` / `near_rq5` / `below_threshold`. A workflow value `pending_review` is allowed only if necessary, and never as a substantive category (§5.3) |

## 3. Reconciliation with existing decisions

| Existing item | Relationship | Conflict? |
|---|---|---|
| D-031 (≥ 4 of 5; APPROVED — CONDITIONAL) | D-034 keeps the threshold. D-032, D-033 and D-034 answer D-031's conditions **C2** (selection definition), **C3** ("covering") and **C4** (3-of-5 frameworks) at the decision level. **C1** (R5/D-029 definitions) remains open. D-031 is **not revised**; it stays conditional and inactive | No |
| D-029 / R5 (PROPOSED: `dim_explainability`, `dim_uncertainty`, `dim_calibration`, `validation_design`) | The R5 proposal defines `yes` as "the title/abstract **states**/names the method". D-033 requires evidence of **actual application or evaluation** for RQ5 coverage. An abstract stating "we propose a framework with uncertainty estimation" would be `yes` under the R5 wording but does not count under D-033-2. D-029 is unapproved, so this is not a conflict with an approved decision. **R5 must be reconciled with D-033 before activation** (new Q-041) | Open (Q-041) |
| D-029 / R5 "potential RQ5" rule | The proposed rule (count `unclear` as `yes` only to decide whether a record goes to full text) is compatible with D-034-2 and D-034-4. Its threshold is 4 (D-031) | No (pending R5) |
| Q-028 record, risk 2 (`Q-028_owner_decision_record.md` §3) | D-034 plans a near-RQ5 analysis but does **not** say whether non-metabolic frameworks with 3 components are retained at screening. Under draft criteria v1.0 they are `exclude E4` unless they are method exemplars, so the near-RQ5 group could be **incomplete** for other domains. This was one of the options listed under Q-038 and is not decided | **Open (Q-040)**. Not resolved here |
| D-027 (screening file and schema; PROPOSED) | `dim_feature_selection` was added as an **optional** column in the D-027 schema (§5.1). Approval of D-027 is still required for the format itself | No |
| D-024 (inventory schema; PROPOSED) | A matching inventory column was added (`null` for every record) | No |
| D-026 (descriptors; PROPOSED) | Unchanged; superseded only through R5 | No |
| Q-034 (`extraction_status`) | Unrelated; unchanged | No |

## 4. Component-specific evidence criteria (initial specification; INACTIVE)

Shared rule (D-033): `yes` = evidence that the procedure was actually applied or evaluated in the study; `no` = evidence that it was not; `unclear` = insufficient or ambiguous, flagged for human review. Mentions in the introduction, related work or proposed architecture do not count. A negative result still counts if the procedure was performed.

The minimum criteria stated by the owner are listed below, with the existing proposal each one must be reconciled with. **No further technical requirement is added here.**

| Component | Minimum criterion (owner, D-033-5) | Detailed definition | Status of the detail |
|---|---|---|---|
| 1. Feature selection | Evidence of a qualifying procedure **and** a retained subset of original variables | D-032 + `Q-037a_feature_selection_proposal.md` §4–§6 | Approved — conditional (D-032) |
| 2. Classification | Evidence that a classification model was trained or evaluated for the relevant prediction task | `screening_criteria.md` §2.3 (ML scope, draft v1.0) | Draft criteria; **no component status field exists** (Q-039) |
| 3. Explainability | Evidence that an explainability method was applied to interpret model predictions or behaviour | R5 proposal (`final_confirmation_sheet_LIT-004.md` R5) | PROPOSED; must align with D-033 (Q-041) |
| 4. Probability calibration | Evidence that a calibration procedure or calibration evaluation was actually performed | R5 proposal | PROPOSED; align (Q-041) |
| 5. Uncertainty estimation | Evidence that an uncertainty-estimation method was applied or evaluated | R5 proposal | PROPOSED; align (Q-041) |

## 5. Representation

### 5.1 Component statuses (current schema inspected)
The canonical screening file (`screening/decisions.csv`; schema `schemas/screening_decision.schema.json`, D-027 proposed) stores descriptors as flat optional `dim_*` columns, one row per paper and stage. The latest stage wins, and the latest row's values are copied to `screening_details` and the inventory.

Existing: `dim_explainability`, `dim_uncertainty`, `dim_calibration` (`""/yes/no/unclear`) and `dim_independent_validation`.

A normalised design (one row per component) was considered and **not** chosen: it would duplicate the existing `dim_*` convention.

| Field | State after this task |
|---|---|
| `dim_feature_selection` | **Implemented** as an optional column (`""/yes/no/unclear`) in the screening schema, `pubrecords.py` (`SCREENING_OPTIONAL`, `SCREENING_ENUMS`), the publication-record schema (`screening_details`) and the inventory schema and report. Files without the column stay valid. No record has a value; nothing was filled in for unscreened papers. **Inactive**: the column may only be filled once D-032 is active |
| `dim_classification` | **Not implemented, and not approved.** The five-status derivation needs it. Proposed: `""/yes/no/unclear`, same convention (Q-039) |
| `dim_explainability`, `dim_uncertainty`, `dim_calibration` | Existing columns; definitions pending R5/Q-041 |

### 5.2 Previously published panels (R-Q037a-2)
The current schema can track reuse without a new field: `scope_flags` is a free-text, semicolon-separated column in the screening file and the inventory.

Proposed token: **`published_panel_reused`**.
- **Purpose:** the study evaluates a previously published biomarker panel without new selection.
- **Values:** the token is present or absent.
- **Effect on selection:** none by itself. `dim_feature_selection` is assessed independently.
- **Migration:** none (no screening rows exist).

This is a documented convention; the schema does not validate it. **Not yet active** (follows D-032 activation).

### 5.3 `rq5_coverage_group` (Q-038-5): specification; implementation BLOCKED

Four separate concepts, never conflated:

| Concept | Where it is represented |
|---|---|
| (1) Is the screening record complete? | `screening_status` / a row in `screening/decisions.csv` (existing) |
| (2) Status of each component | Five `dim_*` columns, each `yes`/`no`/`unclear` (or empty = not assessed) |
| (3) Does the study meet the threshold? | `rq5_coverage_group`, derived from (2) only |
| (4) Is human review outstanding? | `needs_human` (existing) and the proposed derived flag `rq5_coverage_provisional` |

Proposed derivation (assessed only where the RQ5 evaluation applies; see the open point below):

```
statuses = the five component values from the latest screening row
if any status is empty (not assessed)          -> rq5_coverage_group = null   (not derived)
n_yes = number of "yes"; n_unclear = number of "unclear"
n_yes >= 4                                      -> "qualified"
n_yes == 3                                      -> "near_rq5"
n_yes <= 2                                      -> "below_threshold"
rq5_coverage_provisional = (n_unclear > 0)      # group could change once unclear components are resolved;
                                                # for "qualified" it only marks the unclear fifth (no eligibility effect)
```

- `pending_review` is **not** proposed. The `null` group (components not yet assessed) together with `rq5_coverage_provisional` and `needs_human` represent unresolved states. No workflow value can override the ≥ 4 rule.
- A record with four `yes` and one `unclear` is `qualified` with `rq5_coverage_provisional = true` (Q-038-4).
- A record with three `yes` and two `unclear` is `near_rq5` and provisional (Q-038-2). It is never `qualified` until a fourth `yes` is confirmed.

**Open point (not decided):** whether "confirmed `yes`" means a value recorded at the `full_text` stage only. The R5 proposal says RQ5 membership is decided from full text, so title/abstract values would leave the group `null` or provisional. This is part of Q-041.

**Why blocked:**
- (a) no classification status field (Q-039);
- (b) the explainability, calibration and uncertainty definitions are not approved (R5) and not aligned with D-033 (Q-041);
- (c) the meaning of "confirmed" is open (Q-041);
- (d) the D-027 format is not approved.

Implementing the derived field now would mean computing a group from undefined inputs.

**Test plan for when it is unblocked** (not yet written):
- all five statuses;
- invalid values;
- 4 `yes` + 1 `unclear` → `qualified`, provisional;
- 3 `yes` + unresolved → `near_rq5`, provisional;
- 3 `yes` + 2 `no` → `near_rq5`, not provisional;
- ≤ 2 `yes` → `below_threshold`;
- any empty status → `null`;
- an unscreened record → `null`;
- a `needs_human` record keeps the derived group, with the flag separate;
- consistency between the group and the statuses;
- IDs and unrelated fields preserved.

### 5.4 Proposed-only components (Q-037b-2)
Proposed (not implemented): a `scope_flags` token `proposed_only:<component>` (e.g., `proposed_only:uncertainty`) for descriptive analysis. The component's `dim_*` value stays `no` or `unclear` per D-033, so a proposed component can never be confused with implemented coverage. Needs owner confirmation.

## 6. Screening criteria and protocol
`screening_criteria.md` and `screening_protocol.md` are **not changed**. The RQ5 rule (D-031) and these definitions enter criteria v1.1 only after the activation conditions are met. Until then, this document is the implementation specification.

## 7. Activation conditions (D-032, D-033, D-034)
All of the following are required before any of them governs screening:
1. R5 / D-029 definitions approved **and** reconciled with D-033 (Q-041), including the meaning of "confirmed".
2. A classification status field decided (Q-039).
3. Q-040 decided (screening retention of non-metabolic 3-of-5 frameworks), because it determines whether the near-RQ5 group is complete.
4. D-027 (screening format) and D-024 (inventory schema) approved.
5. `rq5_coverage_group` implemented and tested per §5.3.
6. D-031, D-032, D-033 and D-034 written into `screening_criteria.md` v1.1 and protocol v0.2, frozen as the pilot's `criteria_version`.
7. The other pilot-blocking items in `final_confirmation_sheet_LIT-004.md` resolved.

## 8. Addendum (2026-10-24, Q-041-DECISIONS)
D-035 (`Q-041_decision_record_D035.md`) settles the open points of §3 and §5.3 that depended on Q-041.
- **§3, D-029 / R5 row:** for RQ5 component statuses the evidence standard is now D-035 (applied or evaluated, with documented output). D-029 stays PROPOSED for its other content.
- **§4:** the component criteria are now the D-035 definitions (record §2).
- **§5.3 open point:** "confirmed `yes`" = a status from a full-text assessment (not `abstract_only`).
- **§5.3 implementation:** stage-separated evidence (`rq5_components` in the publication record), the erasure and completeness checks, and `derive_rq5_coverage_group()` are implemented and tested. The group is **not wired into the build** because Q-039 (classification status) is open.
- §7 condition 1 is met for the component definitions; the other conditions remain.

## 9. Addendum (2026-10-24, Q-039-DECISION)
D-036 (`Q-039_decision_record_D036.md`) answers Q-039 (§7 condition 2).
- **§5.1:** `dim_classification` is now **implemented** (`""/yes/no/unclear`, optional; inactive).
- **§5.3:** `rq5_coverage_group` and `rq5_coverage_provisional` are derived in the build from **confirmed** statuses (D-035 G3). Blocker (a) is resolved, and (b) and (c) were resolved by D-035. The §5.3 test plan is implemented in `tests/literature/test_screening_and_ids.py` (`TestRQ5ComponentEvidence`).
- **§7:** conditions 2 and 5 are met. Conditions 3, 4, 6 and 7 remain, plus Q-042 (`lr_only` classification eligibility).
