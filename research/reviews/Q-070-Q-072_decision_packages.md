# Decision Packages — Q-070, Q-071, Q-072

| Field | Value |
|---|---|
| Task | Q-070-Q-072-DECISION-PACKAGES (2026-10-29, Day 16; assistant label, no researcher task ID) |
| Status | **Proposals for the researcher's decision. Nothing is approved, recorded, implemented or activated by this document.** Q-070, Q-071 and Q-072 stay Open; every decision status is unchanged |
| Repository state | `claude/eloquent-mccarthy-bqtxr3` at `0c85634`, with the uncommitted R5-GROUP1-DECISIONS changes (D-046, D-047, Q-070–Q-072) in the working tree |
| Screening | **INACTIVE** (D-035 record §6 conditions 3–6 not met) |
| Labels | `[EVIDENCE]` = stated in the cited file or shown by a read-only command; `[RECOMMENDATION]` = assistant proposal, not approval |

A recommendation here is **not** researcher approval (`CLAUDE.md` rule 7). The response meanings are those of `research/reviews/final_confirmation_sheet_LIT-004.md` lines 13–21: APPROVE; APPROVE (conditional); REJECT; MODIFY (not approved; reworded and returned); DEFER.

---

## 1. Q-070 — `dim_calibration` wording

**Decision required:** confirm, amend, reject or defer the reworded `dim_calibration` definition in D-046 line 1c (`logs/DECISION_LOG.md`, D-046).

### 1.1 Current wording `[EVIDENCE]`
| Source | Status | Brier score alone | Analytical-chemistry calibration | `yes` requires |
|---|---|---|---|---|
| D-035 §2, `research/reviews/Q-041_decision_record_D035.md` line 42 (RQ5 component statuses) | **APPROVED — CONDITIONAL (inactive)** | "Insufficient on its own"; `unclear` when "Brier score only" | Insufficient; `no` when "only analytical calibration is meant" | Calibration assessment **with a reported result**, or a documented recalibration procedure applied to model outputs |
| D-046 line 1c (general descriptor) | MODIFIED, awaiting confirmation (Q-070) | "never `yes`"; `unclear` unless a named assessment or recalibration is also reported | `no`, stated in the justification | Assessed with a named method or corrected by a named recalibration |
| R5 line c, `final_confirmation_sheet_LIT-004.md` line 195 (original proposal) | superseded by D-046 1c once confirmed | `unclear` ("mixes calibration and discrimination") | `no` | Named assessment or recalibration |
| `research/literature/screening_protocol.md` v0.1 §2, line 50 (draft, D-025 PROPOSED) | draft | **Listed as an example of calibration evidence** ("e.g., calibration plot/slope, Brier score, recalibration") | not addressed | "States that probability calibration is assessed or corrected" |
| `research/literature/screening_criteria.md` v1.0 | draft | No descriptor definition (§3 RQ3/RQ5 rows mention calibration only as a topic) | — | — |
| Schemas and build (`screening_decision.schema.json`, `pubrecords.py` line 70) | implemented | values only: `"" / yes / no / unclear` | — | — |
| `research/literature/search_strategy.md` §3, line 93 (theme C) | search terms | "Brier score" is a **retrieval** term, not an evidence rule | — | — |

**Only conflict:** `screening_protocol.md` line 50 versus D-035 §2 and D-046 1c. The difference in what `yes` requires between D-035 (a reported result) and D-046 (a named method) is intended: D-035 governs RQ5 component statuses, D-046 the general descriptor (D-046 part 3).

### 1.2 Proposed consistent definition `[RECOMMENDATION]`
> **`dim_calibration`** (general screening descriptor; for RQ5 component statuses D-035 §2 applies)
> - **`yes`**: the record states that the **probability calibration of the model's predicted probabilities** was assessed with a named method (calibration plot or curve, calibration slope or intercept, calibration-in-the-large, ECE/MCE, Hosmer–Lemeshow, Spiegelhalter's test) **or** corrected with a named recalibration (Platt scaling, isotonic regression, temperature scaling).
> - **Brier score:** a Brier score **alone is never `yes`**: it combines calibration and discrimination. With no named calibration assessment or recalibration it gives **`unclear`**. When a named assessment or recalibration is also reported, `yes` rests on that, not on the Brier score.
> - **`no`**: the absence is stated, or the fully described analysis contains no calibration assessment or recalibration, or "calibration" is used **only in the analytical-chemistry sense** (instrument, assay or standard calibration curves); the reason is stated in the justification.
> - **`unclear`**: "well-calibrated" or "calibration" without a method; a Brier score alone; the sense of "calibration" (probability vs analytical) cannot be determined.

This is D-046 1c with two additions taken from D-035 §2: "calibration-in-the-large" in the method list and "the fully described analysis contains no …" under `no`.

### 1.3 Options
| Option | Meaning | Consequence |
|---|---|---|
| **A [RECOMMENDED]** APPROVE §1.2 | Line 1c becomes APPROVED with this text | R5 complete except 1g (conditional); D-024 condition 1 met for this line; D-026 can be recorded "revised by D-029" (sheet line 227) |
| B APPROVE D-046 1c as worded | Same effect, without the two additions | As A |
| C MODIFY | Your wording; returned again | Q-070 stays open |
| D REJECT the rewording | Original R5 line c stands as proposed (not approved) | Line c stays unapproved; R5 incomplete |
| E DEFER | Stays open | As C |

**Rationale for A:** identical Brier and analytical-chemistry treatment to approved D-035 §2; the two additions remove the remaining wording differences without changing meaning.

**Files likely to change after approval:** `logs/DECISION_LOG.md` (Status history: D-046 line 1c; D-026 "revised by D-029"); `research/reviews/unresolved_questions.md` (Q-070 Answered); later, `screening_protocol.md` v0.2 §2 (replace line 50) and `screening_criteria.md` v1.1 (descriptor reference) — both under D-035 record §6 condition 5. No schema change (values unchanged).

---

## 2. Q-071 — `non_metabolic_near_rq5_comparator` flag

**Decision required:** approve, amend, reject or defer a specification of the D-047 flag.

### 2.1 Fixed constraints `[EVIDENCE]`
- D-031 (APPROVED — CONDITIONAL): RQ5 needs **at least 4 of 5** components; D-034: `qualified` ≥ 4 confirmed `yes`, `near_rq5` exactly 3, `below_threshold` 0–2; `unclear` never counts as `yes`; `rq5_coverage_group` is derived, never assigned by screeners.
- D-047: the flag never qualifies a record as RQ5; three components never bypass the threshold; exemplar treatment unchanged.
- `screening_criteria.md` §2.1 (lines 49–62): in-scope disorders [PROVISIONAL — Q-001]; obesity, thyroid dysfunction, PCOS `scope_pending` (kept); out of scope (E4): complications as the target; cardiovascular events, cancer, infectious disease unless a methodological exemplar.
- `scope_flags`: a `;`-separated token string; **no enum or validation** in `screening_decision.schema.json` or `paper_inventory.schema.json`; the build adds `retracted` itself (`make_literature_reports.py` lines 193–194).

### 2.2 Proposed specification `[RECOMMENDATION]`
| Element | Proposal |
|---|---|
| Purpose | Keep non-metabolic integrated frameworks with exactly three D-031 components available for the D-034 near-RQ5 comparison, which would otherwise lose them to E4 |
| Scope | Records that would be `exclude E4` **only** because the target condition is outside `screening_criteria.md` §2.1, and that propose or evaluate an integrated framework on biomarker/omics/clinical tabular data. Not for `scope_pending` disorders (they are not E4) |
| Allowed values | Token `non_metabolic_near_rq5_comparator` present in `scope_flags`, or absent. No other values |
| Metabolic status | Decided from the target condition against §2.1 of the criteria version in force (`criteria_version`). A record with at least one in-scope metabolic target is metabolic (RQ1 path, no flag). Unclear target → decision `uncertain`, `needs_human = yes` |
| Title/abstract | Set provisionally when yes + unclear components ≥ 3 **and** the potential-RQ5 rule (yes + unclear ≥ 4) is not met; decision `uncertain`, `needs_human = yes`, justification names the components. If the potential-RQ5 rule is met, the record goes to full text as a potential RQ5 record instead (D-046 1g); the flag is not set |
| Full text | Kept only with **exactly 3 confirmed `yes`**. With ≥ 4 confirmed: RQ5 under D-031 (draft criteria §3 retains RQ5 records of any domain); flag removed. With ≤ 2 confirmed: `exclude E4` (unless `non_metabolic_method_exemplar`); flag removed |
| RQ5 threshold | Unaffected. The flag is never read when deriving `rq5_coverage_group`; RQ5 counts never include flagged records |
| Exemplars | Independent of `non_metabolic_method_exemplar`; both tokens may co-occur. Exemplar retention keeps its own rule |
| Reporting and audit | Counts of flagged records at each stage; flagged records listed only in the near-RQ5 comparison (D-034 (3)), never in RQ5 tables; justification and component statuses on every flagged row; every change of the flag is a new decision row (existing rows kept) |
| Missing abstracts | All components `unclear` → the potential-RQ5 rule applies, not the flag (see open point 5) |

### 2.3 Options
| Option | Meaning |
|---|---|
| **A [RECOMMENDED]** APPROVE §2.2, together with answers to the open points in §2.4 | Q-071 Answered; D-047 implementable once criteria v1.1 is written |
| B MODIFY | Returned with your changes |
| C REJECT | D-047's approach stays approved without a flag definition; not implementable |
| D DEFER | Stays open |

### 2.4 Additional researcher decisions this flag needs
1. **Name**: keep `non_metabolic_near_rq5_comparator`? (recommended: yes)
2. **Title/abstract rule**: yes + unclear ≥ 3 (recommended) or confirmed-at-full-text only?
3. **Decision label and RQ tags of retained records** (not documented anywhere): the schema allows `include / exclude / uncertain / abstract_only`. Recommended: `include` with **no** `RQ5` tag at full text, so that retention cannot be read as RQ5 qualification. Needs your choice.
4. **Complications as the target** (§2.1 first E4 bullet): treat as non-metabolic for the flag? Not documented; needs your choice.
5. **Title-level E4 for records without an abstract** (D-046 1d allows exclusion for a title-level E4 reason): should an integrated-framework title prevent title-level E4? Not documented.
6. **Exemplar scope inconsistency** `[EVIDENCE]`: `screening_criteria.md` line 62 retains exemplars for **RQ2–RQ4**; `screening_protocol.md` lines 76 and 122 say **RQ2–RQ5**. To be settled before v1.1.
7. **Dependency on Q-001** (disorder scope, Open): membership changes if §2.1 changes.
8. **Validation**: should `scope_flags` tokens be validated against an approved list (schema change)? Today any string passes.

**Files likely to change after approval:** `logs/DECISION_LOG.md` (D-047 Status history), `unresolved_questions.md` (Q-071), `screening_criteria.md` v1.1 §2.1 and §3, `screening_protocol.md` v0.2 §2/§3/§5 (E4 row), and — only if item 8 is approved — the schemas, `pubrecords.py` and tests.

---

## 3. Q-072 — `validation_design` naming collision

**Decision required:** choose how the screening-level validation descriptor of D-029 option (a) is named, so that it is kept apart from the full-text extraction field.

### 3.1 Current state `[EVIDENCE]`
| Item | Fact |
|---|---|
| Extraction field | `validation_design` in `paper_inventory.schema.json` line 223 ("Sentinel 'REQUIRES FULL-TEXT REVIEW' until extracted"; LIT-002, commit `eee92c1`); in `make_literature_reports.py` `EXTRACTION_FIELDS` (line 41) with default `SENTINEL` (line 56); all **3,386** records hold `"REQUIRES FULL-TEXT REVIEW"`; CSV column 48 |
| Screening descriptor today | `dim_independent_validation` (`"" / external / temporal / internal_only / unclear`) in `pubrecords.py` lines 60, 71; `screening_decision.schema.json` line 126 and column order line 158; `paper_inventory.schema.json` line 380; `publication_record.schema.json` line 500; copied into the inventory by `make_literature_reports.py` line 197; CSV column 27; **null for all 3,386 records**; no screening rows exist |
| Naming convention | Screening descriptors carry the prefix `dim_` (`dim_explainability`, `dim_uncertainty`, `dim_calibration`, `dim_feature_selection`, `dim_classification`); extraction fields are unprefixed (`explainability`, `uncertainty_methods`, `calibration_methods`, `validation_design`) |
| Tests | `tests/literature/test_screening_and_ids.py`: lines 220–232 (round-trip of `dim_independent_validation`), lines 327–351 (schema vs code constants: column order, properties, enums), lines 556–557 (`dim_classification`) |
| Decisions | D-029 option (a) and D-046 1e/part 2 use the name `validation_design`; D-024 (APPROVED — CONDITIONAL) covers the evidence-table fields, including the extraction field |

### 3.2 Options
| | **A [RECOMMENDED]** `dim_validation_design` | B `validation_design` for screening; rename the extraction field | C keep `dim_independent_validation`, widen its values |
|---|---|---|---|
| Meaning | Screening-level design as stated in title/abstract or full text (6 values of D-046 1e) | Same meaning, under the extraction field's current name | Same 6 values under the old name |
| Conflict with extraction data | None: `validation_design` stays the extraction field | Yes: the 3,386 sentinel values and `EXTRACTION_FIELDS` must move to a new name (e.g., `validation_design_extracted`); the field set covered by D-024 changes | None |
| Schema / build changes | Replace `dim_independent_validation` by `dim_validation_design` in `pubrecords.py` (lines 60, 71), `screening_decision.schema.json` (property, enum, column order), `paper_inventory.schema.json` (line 380), `publication_record.schema.json` (line 500), `make_literature_reports.py` (lines 47, 197); enum `"" / external / temporal / internal_only / none / not_applicable / unclear` | All of A's changes under the name `validation_design`, plus renaming the extraction field in the schema, `EXTRACTION_FIELDS`, `MANUAL_DEFAULTS` and every manual-input reader | Enum change in code and schema only |
| Existing records and consumers | No screening rows exist and the old column is null everywhere, so no values are lost; the inventory CSV/JSON column name changes on the next build | The extraction column is renamed for all 3,386 records; any consumer of `validation_design` (reports, future extraction files) breaks or reads the wrong field | Unchanged columns |
| Migration / compatibility risk | Low: a rename of an empty column; regeneration needs a rebuild (raw exports, Q-063) | **High**: two fields swap meaning under similar names; D-024 scope affected (you asked that it not change) | Low technically, but it **contradicts approved D-029 option (a)**, whose option (b) was "keep `dim_independent_validation`" |
| Tests needed | Update the schema-consistency test (lines 327–351) and the round-trip test (220–232); new tests: the 6 values accepted and others rejected; the extraction field still holds the sentinel after a build; Q-032 enforcement (four descriptors required for `include`/`uncertain`, optional for `exclude`) | A's tests plus extraction-field migration tests | Enum tests; Q-032 enforcement tests |

**Recommendation: Option A**, recorded as the implementation name of D-029 option (a)'s `validation_design` (D-029 and D-046 texts kept; the mapping recorded in a new Status-history entry). Rationale: it follows the existing `dim_` / unprefixed convention, keeps screening-level classification apart from full-text extraction evidence, touches only an empty column, and leaves D-024's field set unchanged. Option C conflicts with approved D-029; Option B changes D-024's scope and risks confusing the two fields.

| Option | Response |
|---|---|
| A, B or C | APPROVE one; MODIFY (another name); DEFER |

**Files likely to change after approval:** `logs/DECISION_LOG.md` (Status history: naming of D-029/D-046), `unresolved_questions.md` (Q-072); then, under a separate implementation authorisation: `scripts/literature/pubrecords.py`, `scripts/literature/make_literature_reports.py`, the three schemas, `tests/literature/test_screening_and_ids.py`, and the descriptor wording in `screening_protocol.md` v0.2 and `screening_criteria.md` v1.1. Regenerating the inventory needs the restored raw exports (Q-063).

---

## 4. Order and dependencies
1. **Q-070** and **Q-072** are independent of each other and can be decided now; both are needed before D-029/D-046 can be implemented and before D-024 condition 1 and 3 can be met.
2. **Q-071** depends on Q-001 (disorder scope) for which records count as non-metabolic, and on the open points in §2.4.
3. None of the three activates screening. D-035 record §6 conditions 3–6 stay unmet until D-024/D-027 (full approval), criteria v1.1 / protocol v0.2, implementation and the other pilot-blocking items are done.

## 5. Response template
```
Q-070  [ ] A approve §1.2   [ ] B approve D-046 1c as worded   [ ] C MODIFY: …   [ ] D REJECT   [ ] E DEFER
Q-071  [ ] A approve §2.2   [ ] B MODIFY: …   [ ] C REJECT   [ ] D DEFER
       2.4-1 name:                 [ ] keep   [ ] other: …
       2.4-2 title/abstract rule:  [ ] yes+unclear ≥ 3   [ ] full text only
       2.4-3 retained label:       [ ] include, no RQ5 tag   [ ] other: …
       2.4-4 complications:        [ ] count as non-metabolic   [ ] do not   [ ] other: …
       2.4-5 title-level E4:       [ ] framework title prevents title-level E4   [ ] no change   [ ] other: …
       2.4-6 exemplar scope:       [ ] RQ2–RQ4   [ ] RQ2–RQ5
       2.4-8 validate scope_flags: [ ] yes (schema change, separate authorisation)   [ ] no
Q-072  [ ] A dim_validation_design   [ ] B rename extraction field   [ ] C keep dim_independent_validation   [ ] MODIFY: …   [ ] DEFER
Recording: [ ] record answered items   [ ] record nothing yet
```

## 6. Gaps and contradictions (reported, not reconciled)
1. `screening_protocol.md` line 50 lists "Brier score" as calibration evidence (conflicts with D-035 §2 and D-046 1c).
2. Exemplar scope: `screening_criteria.md` line 62 (RQ2–RQ4) vs `screening_protocol.md` lines 76 and 122 (RQ2–RQ5).
3. The decision label and RQ tags of retained comparator records are not documented anywhere.
4. `scope_flags` values are not validated; any token is accepted.
5. D-029 and D-046 name the field `validation_design`, which is already the name of an inventory extraction field (Q-072).
