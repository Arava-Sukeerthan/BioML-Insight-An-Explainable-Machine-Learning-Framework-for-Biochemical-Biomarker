# D-038 (Q-043): reporting of qualified records with an unresolved component

| Field | Value |
|---|---|
| Task | Q-043-DECISION (2026-10-24) |
| Question | **Q-043** (raised 2026-10-24, PR10-AUDIT-DECISIONS; status **Open** until this record): D-034(4)/Q-038-4 says a record with ≥ 4 confirmed `yes` and an `unclear` fifth qualifies with the "flag kept". Under D-037-A1 such a record has `rq5_coverage_provisional = false`. Is the component-level `unclear` enough, or should qualified records with an `unclear` component get a separate derived marker? (`unresolved_questions.md`) |
| Owner response | Owner prompt of 2026-10-24, "Decision 1: Q-043": approves the proposed resolution that no separate stored or derived marker is added; the five confirmed component statuses remain the source of evidence; reporting distinguishes three subgroups of `qualified` records; only records with five confirmed `yes` may be described as covering all five components; thresholds and the D-037-A1 meaning of `rq5_coverage_provisional` unchanged; screening stays inactive |
| Basis | The proposed resolution delivered in the session on 2026-10-24 (in the conversation, not committed), after the read-only audit of PR #10 and PR #11 |
| Recorded as | **D-038 — APPROVED — CONDITIONAL, inactive for screening** (`logs/DECISION_LOG.md`). ID verified as the next free one: D-037 is the highest ID on every branch, and D-038 is not used anywhere |
| Approved by | The researcher (owner), 2026-10-24, through the explicit approval above. No other approval is claimed |
| Screening | **Not started.** No screening decision exists, so no record has a coverage group |

## 1. Decision

| ID | Content |
|---|---|
| D-038-1 | **No separate marker.** No stored or derived field is added for a `qualified` record with an `unclear` component. The five confirmed statuses in `rq5_components.confirmed.statuses` are the source of evidence for the unresolved component. D-033-4 already makes each `unclear` a human-review flag; this is how D-034(4)'s "flag kept" is met |
| D-038-2 | **Reporting rule.** Any RQ5 count, table or text based on coverage groups reports `qualified` records in three separate subgroups: **(a)** five confirmed `yes`; **(b)** four confirmed `yes` and one `unclear`, naming the unclear component; **(c)** four confirmed `yes` and one `no`. **Only (a)** may be described as covering all five components. The subgroup is computed from the confirmed statuses when the report is produced |
| D-038-3 | **Unchanged:** the D-034 thresholds, `rq5_coverage_group`, the D-037-A1 meaning of `rq5_coverage_provisional`, `needs_human`, the schemas, the code and the inventory |

## 2. Rationale `[EVIDENCE: PR #10 / PR #11 audit, 2026-10-24]`
- **No information is lost.** The confirmed statuses name every `unclear` and `no` component. The three subgroups are a function of those five values, so a stored marker would duplicate them and could drift from them.
- **The risk is in reporting, not in the data.** Someone reading only `rq5_coverage_group` (or `rq5_coverage_provisional`, which is false for every `qualified` record under D-037-A1) could describe a record as five-component when it is not. D-038-2 closes that gap by a rule on the reports.
- **`needs_human` is not used as the marker.** It is entered by the screener; setting it automatically would mix a screener field with a derived one.

## 3. Relationship to existing decisions

| Decision | Effect of D-038 | Status |
|---|---|---|
| D-033 | D-033-4 ("`unclear` … flagged for human review") is the flag referred to in D-034(4). Unchanged | No status change (inactive) |
| D-034 | (4) "flag kept; no five-component claim" is met by D-038-1 and D-038-2. Thresholds and groups unchanged | No status change (inactive) |
| D-035 | Unchanged. G4 researcher verification is still triggered by `qualified` and `near_rq5` | No status change (inactive) |
| D-037 | A1 unchanged. Its `[OPEN]` point (Q-043, record §2) is answered | No status change (inactive) |

## 4. Not done, and not activated
- No code, schema, test or inventory change. No report exists yet; D-038-2 applies to the first RQ5 report and must be carried into criteria v1.1 / protocol v0.2 when they are drafted.
- No screening decision, pilot or model training. D-031–D-038 remain inactive. Activation conditions unchanged (D-035 record §6).
- Q-042 stays Open; no `lr_only` rule.
