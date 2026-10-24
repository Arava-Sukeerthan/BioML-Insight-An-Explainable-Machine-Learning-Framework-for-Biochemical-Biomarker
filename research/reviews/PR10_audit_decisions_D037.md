# D-037 (PR #10 audit): provisional coverage flag and Q-042 activation status

| Field | Value |
|---|---|
| Task | PR10-AUDIT-DECISIONS (2026-10-24) |
| Basis | Independent read-only pre-merge audit of PR #10 (Q-039 / D-036), delivered in the session on 2026-10-24 (in the conversation, not committed). Findings 1 and 2 of that audit led to these choices |
| Owner response | Owner prompt of 2026-10-24. **Decision A1:** `rq5_coverage_provisional` is true only when resolving one or more `unclear` statuses could change the derived coverage group; thresholds unchanged. **Decision B1:** do not add Q-042 as a new activation blocker for D-031–D-036 through D-036; Q-042 stays OPEN |
| Recorded as | **D-037 — APPROVED — CONDITIONAL, inactive for screening** (`logs/DECISION_LOG.md`). It revises part of D-036 (approved) by a new entry; D-036's text is kept as written |
| Approved by | The researcher (owner), 2026-10-24, through the explicit choices above. No other approval is claimed |
| Screening | **Not started.** No screening decision exists for any real paper, so every `rq5_coverage_group` and `rq5_coverage_provisional` is null |

## 1. Decisions

| ID | Owner choice | Recorded content |
|---|---|---|
| D-037-A1 | Decision A1 | `rq5_coverage_provisional` is **true only when** some resolution of the confirmed `unclear` statuses to `yes` or `no`, with every other status held fixed, gives a **different** `rq5_coverage_group`. It is false when every resolution gives the same group. The existence of an `unclear` status alone does not make a record provisional. Thresholds unchanged: `qualified` ≥ 4 confirmed `yes`, `near_rq5` exactly 3, `below_threshold` 0–2; `unclear` never counts as `yes`. Missing or not-assessed statuses keep the existing behaviour: group and flag are both null, and a missing status is never treated as `no` |
| D-037-B1 | Decision B1 | Q-042 (`lr_only` classification eligibility) is **not** an activation condition for D-031–D-036 by virtue of D-036. The wording added in the Q-039-DECISION work that listed Q-042 among the activation conditions is superseded (§3). Q-042 stays **Open**. No `lr_only` rule is decided or implemented. All other activation conditions stay as they are |

## 2. D-037-A1: the provisional rule

**Calculation** (`derive_rq5_coverage_group()` in `scripts/literature/pubrecords.py`):
1. If any of the five confirmed statuses is empty or missing, return group = null, provisional = null (unchanged).
2. Group from the number of `yes` (unchanged thresholds).
3. Enumerate every assignment of `yes`/`no` to the `unclear` statuses (2^k assignments for k unclear). Provisional = true if any assignment gives a different group.

Because the group depends only on the number of `yes`, this is equivalent to: the group for `n_yes` differs from the group for `n_yes + n_unclear`. The tests check both forms.

**Consequences by group:**

| Group | Provisional when | Examples |
|---|---|---|
| `qualified` (≥ 4 `yes`) | **Never**: resolutions can only add `yes` | 4 `yes` + 1 `unclear` → `qualified`, not provisional |
| `near_rq5` (3 `yes`) | Any `unclear` (one more `yes` gives `qualified`) | 3 `yes` + 2 `unclear` → provisional; 3 `yes` + 1 `unclear` + 1 `no` → provisional; 3 `yes` + 2 `no` → not provisional |
| `below_threshold` (0–2 `yes`) | `n_yes + n_unclear ≥ 3` | 1 `yes` + 1 `unclear` + 3 `no` → not provisional; 0 `yes` + 2 `unclear` + 3 `no` → not provisional; 2 `yes` + 1 `unclear` + 2 `no` → provisional; 5 `unclear` → provisional |

**What this revises** (dated addenda; the original text is kept):
- D-036 record §4, "Provisional" bullet (`Q-039_decision_record_D036.md` line 54): "true when any confirmed status is `unclear`", with the example "4 `yes` plus an `unclear` fifth … `qualified`, provisional".
- D-034 record §5.3 (`RQ5_component_decisions_D032-D034.md` lines 128–129 and 133): the proposed derivation `rq5_coverage_provisional = (n_unclear > 0)` and the example "four `yes` and one `unclear` is `qualified` with `rq5_coverage_provisional = true`".
- D-035 record §5 (`Q-041_decision_record_D035.md` line 91): "`provisional` = any `unclear`".

**Consistency with the approved D-034 text** (`logs/DECISION_LOG.md`, D-034 row; record §2.3):
- D-034(2)/Q-038-2, "3 confirmed `yes` → provisional `near_rq5` even with `unclear` components": unchanged in effect. Under A1, a `near_rq5` record with any `unclear` is provisional.
- D-034(4)/Q-038-4, "≥ 4 `yes` + an `unclear` fifth qualifies; flag kept; no five-component claim": the record **qualifies**, and resolving the fifth is still not an eligibility condition. Under A1 its `rq5_coverage_provisional` is **false**. The `unclear` status itself is kept in `rq5_components.confirmed.statuses`, and D-033-4 already defines `unclear` as "flagged for human review"; `needs_human` is unchanged. The D-034 record §5.3 had read "flag kept" as `rq5_coverage_provisional = true`. That reading is superseded by A1. `[OPEN]` Whether "flag kept" needs a separate derived marker for qualified records with an `unclear` component is recorded as **Q-043**. No marker is implemented.

## 3. D-037-B1: Q-042 activation status

**Superseded wording** (all added in the Q-039-DECISION work, PR #10):

| Location | Wording | Now |
|---|---|---|
| `logs/DECISION_LOG.md` line 77 (status-history row, Q-039-DECISION) | "Activation still needs Q-040, D-027/D-024, the remaining R5 items, Q-042 and criteria v1.1/protocol v0.2" | Q-042 is not an activation condition (D-037-B1). Row kept as written |
| `logs/DECISION_LOG.md` line 145 (D-036 entry, Status column) | "until D-035 record §6 is met (Q-040, D-027/D-024, remaining R5 items, Q-042, criteria v1.1/protocol v0.2)" | D-036 is inactive until D-035 record §6 is met. D-035 §6 does not contain Q-042. Entry kept as written |
| `Q-039_decision_record_D036.md` §7, line 85 | "Q-042 (new);" in the list of remaining activation conditions | Superseded by the addendum in that record (§8) |
| `RQ5_component_decisions_D032-D034.md` §9, line 187 | "Conditions 3, 4, 6 and 7 remain, plus Q-042" | Superseded by the addendum in that record (§10) |
| `unresolved_questions.md`, Q-042 row, "Needed by" | "Before activation of D-031–D-036" | Corrected in place (the question tracker is updated in place by convention). Status stays **Open** |

**Not changed:**
- D-035's activation conditions (`Q-041_decision_record_D035.md` §6). They never listed Q-042, so B1 needs no separate decision to amend D-035.
- D-034's activation conditions (`RQ5_component_decisions_D032-D034.md` §7). Items 3, 4, 6 and 7 remain open.
- Every other blocker: Q-040; D-027 and D-024; the remaining R5/D-029 items; criteria v1.1 and protocol v0.2 frozen as the pilot's `criteria_version`; the other pilot-blocking items.
- The substance of Q-042. Whether it should later become an activation condition is for the researcher; this record does not decide it.

**Not edited:** the PR #10 description, which lists Q-042 under "Remaining blockers". It is a GitHub text outside the repository; it is left for the owner.

## 4. Implementation scope
- `scripts/literature/pubrecords.py`: `derive_rq5_coverage_group()` computes the flag by enumerating the yes/no resolutions of the `unclear` statuses; a helper `_rq5_group_for()` holds the unchanged thresholds.
- `research/literature/schemas/publication_record.schema.json`: `rq5_coverage_provisional` description.
- `research/literature/screening_protocol.md` §2a (INACTIVE): coverage-group line.
- `tests/literature/test_screening_and_ids.py`: the A1 examples, an exhaustive check of all 3,125 status combinations against an independent form of the rule, and updated expectations in the existing build tests.
- Generated outputs: none committed change. `rq5_coverage_provisional` exists only in the git-ignored `publications.jsonl`, where it is null for every record. The inventory does not carry it.

## 5. Not done, and not activated
- No screening decision, pilot, criteria v1.1 or model training. D-031–D-037 remain inactive.
- Q-042 is not answered. No `lr_only` rule.
- Not part of this task (separate low-severity follow-ups from the audit): the `needs_human` test from the D-034 §5.3 test plan; the D-035 §4 step 6 "pending verification" report; the `abstract_only`-after-full-text behaviour (audit finding 5).
