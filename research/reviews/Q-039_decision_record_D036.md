# D-036 (Q-039): RQ5 classification status and build-derived coverage group

| Field | Value |
|---|---|
| Task | Q-039-DECISION (2026-10-24) |
| Question | **Q-039** (raised 2026-10-24, RQ5-DECISIONS; status **Open** until this record): "`rq5_coverage_group` (D-034) is derived from five component statuses, but no status field exists for **classification**. Add `dim_classification` (`yes/no/unclear`, same convention as the other `dim_*` columns), or represent classification otherwise?" (`unresolved_questions.md`) |
| Owner response | Owner prompt of 2026-10-24. **Q-039 Choice 1: Option A**: add `dim_classification` as a screening field using the existing `dim_*` convention. **Q-039 Choice 2: Option A**: integrate RQ5 coverage-group derivation into the publication-record build now, while keeping all screening activity inactive until the remaining governance conditions are satisfied |
| Basis | The read-only Q-039 investigation delivered in the session on 2026-10-24 (options A, B and C plus the wiring sub-choice; in the conversation, not committed). Its option summary is in §2 |
| Recorded as | **D-036 — APPROVED — CONDITIONAL, inactive for screening** (`logs/DECISION_LOG.md`) |
| Approved by | The researcher (owner), 2026-10-24, through the explicit choices above. No other approval is claimed |
| Screening | **Not started.** No screening decision exists for any real paper, so no component status and no coverage group exist for any record |

## 1. Decisions

| ID | Owner choice | Recorded content |
|---|---|---|
| D-036-1 | Choice 1, Option A | Classification is recorded in a new optional screening column **`dim_classification`**, with values `""` (not assessed) / `yes` / `no` / `unclear`. This is the convention of `dim_feature_selection`, `dim_explainability`, `dim_calibration` and `dim_uncertainty`. It is the fifth RQ5 component status. Its evidence definition is the approved D-035 §2 classification row (`Q-041_decision_record_D035.md`, line 40). This record adds **no** new definition |
| D-036-2 | Choice 2, Option A | The build derives **`rq5_coverage_group`** and **`rq5_coverage_provisional`** for every publication record. It uses `derive_rq5_coverage_group()` on the **confirmed** (full-text) statuses in `rq5_components`, following D-034 (record §5.3 of `RQ5_component_decisions_D032-D034.md`) and D-035 G3. The derived fields are descriptors only. They activate nothing |

## 2. Rationale

**`dim_classification` (D-036-1)** `[EVIDENCE: Q-039 investigation]`
- D-031 counts classification as a separate component. D-035 G5 requires a completed full-text assessment to **record** all five statuses. Without a field, G5 was enforced for four columns only (D-035 record §5), and the D-034 group could not be derived.
- The `dim_*` column is the existing convention. D-032 set the precedent: an optional, inactive column, valid in files without it. The RQ5 record §5.1 already proposed `dim_classification` and had rejected a normalised one-row-per-component design.
- Owner-rejected alternatives:
  - **B**, inferring classification from the screening decision or reason codes, would turn screening outcomes into component evidence. That conflicts with D-035 G1/G5/G6 and risks D-033(4).
  - **C**, a separate long-format component file, would revise the proposed D-027 format.

**Build-derived coverage group (D-036-2)**
- D-034(5) defines `rq5_coverage_group` as a **derived** field, never assigned by screeners. Deriving it in the build makes the group reproducible from the recorded statuses and keeps it consistent with them.
- With all five statuses available, the D-035 G4 trigger (records reaching `qualified` or `near_rq5`) becomes computable from the build output.
- No screening rows exist. The derivation therefore gives `null` for all 2,979 records, and wiring it in changes no existing value.

## 3. Relationship to D-031 to D-035

| Decision | Effect of D-036 | Status |
|---|---|---|
| D-031 (≥ 4 of 5) | Classification can now be recorded, so the five-component count can be computed. Threshold unchanged | No status change (APPROVED — CONDITIONAL, not applied) |
| D-032 (feature selection) | None. `dim_classification` follows D-032's column precedent | No status change |
| D-033 (applied or evaluated) | Applies to classification unchanged: missing is never `no`, and `unclear` is flagged for review. One activation condition (Q-039) is now met | No status change (inactive) |
| D-034 (coverage groups) | Implements the derived `rq5_coverage_group` / `rq5_coverage_provisional` with D-034's vocabulary. It adds no `pending_review` value, does not interpret the groups as quality, and has no screener override | No status change (inactive) |
| D-035 (evidence standard) | G5 is now enforced for all five statuses. G2/G3 are unchanged: title/abstract values never produce a group. G4 audit trail unchanged; its trigger is now computable. The "pending verification" report (record §4 step 6) is **not** implemented here | No status change (inactive) |
| D-026, D-029 | Not affected. Both remain **PROPOSED** | Unchanged |
| D-027 (screening format) | The new optional column extends the screening schema in the same way as D-032. D-027 itself remains **PROPOSED** | Unchanged |

## 4. Derivation rules (D-034, D-035; implemented in `derive_rq5_coverage_group()`)
- **Input:** `rq5_components.confirmed.statuses`, i.e. the latest `full_text` row that records components and is not an `abstract_only` decision. Preliminary (title/abstract) statuses are never used.
- **Groups:**
  - `qualified`: ≥ 4 `yes`;
  - `near_rq5`: exactly 3 `yes`;
  - `below_threshold`: 0–2 `yes`.

  `unclear` never counts as `yes`.
- **Provisional:** `rq5_coverage_provisional = true` when any confirmed status is `unclear`. For example, 4 `yes` plus an `unclear` fifth component gives `qualified`, provisional.
- **Not assessed:** no confirmed assessment, or any confirmed status missing, gives `rq5_coverage_group = null` and `rq5_coverage_provisional = null`. A missing status is never treated as `no`. The completeness check rejects a full-text row with some but not all five statuses, so a confirmed assessment always has all five.
- **Scope of meaning:** a coverage descriptor, not a judgment of research quality. Differences between groups, such as reported performance, must not be interpreted causally (D-034(3)).

## 5. Implementation scope
- **`scripts/literature/pubrecords.py`:**
  - `dim_classification` added to `SCREENING_OPTIONAL` and `SCREENING_ENUMS`;
  - `RQ5_COMPONENT_FIELDS["classification"] = "dim_classification"`, so `RQ5_RECORDED_FIELDS` has five columns (erasure, completeness and preliminary/confirmed detection all cover classification);
  - `build()` sets `rq5_coverage_group` and `rq5_coverage_provisional`.
- **Schemas:**
  - `screening_decision.schema.json`: property and column order;
  - `publication_record.schema.json`: `screening_details.dim_classification`, `rq5_coverage_group`, `rq5_coverage_provisional`;
  - `paper_inventory.schema.json`: `dim_classification`.
- **`scripts/literature/make_literature_reports.py`:** inventory column `dim_classification`. The coverage group is in the publication records, not the inventory.
- **Tests:** `tests/literature/test_screening_and_ids.py`. The four-component fixtures are now five-component. The test that encoded the old limitation (`test_build_cannot_derive_group_without_classification`) is replaced by tests of the five-status behaviour and of the build-derived group.
- **Compatibility:**
  - Screening files without `dim_classification` still load. Title/abstract rows may be partial, as before.
  - A full-text row that records components without classification is now **rejected** as incomplete. This is the five-status G5 rule. No such row exists.
- **Validation required:** unit tests, schema-consistency tests, a real-data rebuild showing unchanged IDs and values (only the new keys and column added, all null), the raw-export manifest check and the archive checksum check. Results: `logs/session_logs/2026-10-24_Q-039-DECISION.md`.

## 6. Open: classification eligibility of `lr_only` studies `[OPEN]`
- `screening_criteria.md` §2.3 sets logistic-regression-only studies apart as `lr_only`: included only for RQ3/RQ4 relevance or as comparators, and not part of the RQ1 ML landscape.
- D-035 §2 counts "a classification or relevant risk-prediction model applied to the study data, with predictive output reported".
- Whether an `lr_only` study can have `dim_classification = yes` is **not decided**. This record does not decide it, and no rule for it is implemented. It is recorded as **Q-042** in `unresolved_questions.md`.

## 7. Not done, and not activated
- D-036 does **not** activate screening, the pilot, or D-031–D-035. No screening decision was created.
- **Remaining activation conditions** (D-035 record §6):
  - Q-040;
  - D-027 and D-024;
  - the remaining R5/D-029 items;
  - Q-042 (new);
  - criteria v1.1 and protocol v0.2, frozen as the pilot's `criteria_version`;
  - the other pilot-blocking items.
- `screening_criteria.md` is unchanged. `screening_protocol.md` §2a (INACTIVE) is updated only to describe the five columns and the derived group.
