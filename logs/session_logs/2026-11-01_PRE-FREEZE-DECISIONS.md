# Session log — 2026-11-01 — PRE-FREEZE-DECISIONS

**Objective** (researcher prompts, 2026-11-01): implement, documentation-only, the five recommendations of the pre-freeze decision sheet that the researcher approved, and the four procedural choices the researcher confirmed:
1. the primary-code rule (Q-081);
2. the final file names (Q-088);
3. the Stage-0 list confirmation;
4. Q-082 to Q-084 kept open;
5. the freeze procedure approved in principle.

**Not authorised and not done**:
- freezing either text, or approving its final content;
- setting an effective date, final status wording or superseded notes;
- resolving Q-082 to Q-087 or Q-089;
- recording any D-035 §6 condition as met;
- screening, sampling, extraction, pilot work or training;
- changes to code, schemas or v1.0/v0.1;
- network access; staging, commit, push, fetch, branch switch; PR #17 changes.

## State
- Start: branch `claude/eloquent-mccarthy-bqtxr3-part1`, HEAD `c036f47`, equal to the remote-tracking ref; clean tree; nothing staged.
- All relevant files were last changed in `c036f47`, so they match the reviewed state. D-080 to D-089 were unused anywhere in the repository. The final paths did not exist.

## Source checks before recording
- **Stage-0 list:** protocol v0.1 §3 (lines 81–83) and D-072 (1) give the same five types, the same E5/E7 codes, and the same statement that letters are not auto-excluded and *Retraction of Publication* is not a Stage-0 type. No conflict.
- **Q-081:** D-074 (line 362) approves only the Stage-0 E7-over-E5 exception; the general rule is protocol v0.1 §5 (line 116). No conflict.
- **"Needed by" restrictions:**
  - Q-082 "Before such a record is screened (may stay open at the freeze if recorded as open)" and Q-084 "Before expansion screening" match the plan.
  - Q-083 "Before a second pilot, if the first fails" is weaker than the plan's wording; the register wording was used unchanged (deviation reported).

## Changes (working tree; uncommitted)
- `logs/DECISION_LOG.md`:
  - seven status-history rows (D-080 to D-084 new; D-074 and D-068 with no status change; no earlier row edited);
  - new section with D-080 to D-084.
- `research/reviews/unresolved_questions.md`: status cells of Q-081 (answered → D-080), Q-082, Q-083, Q-084 (kept open, D-083) and Q-088 (partly answered → D-081). In Q-088, the reference to the procedure step was updated from step 3 to step 2, with the old number noted.
- Renamed by plain move, unstaged so that no staging occurred before review:
  - `research/literature/screening_criteria_v1.1_draft.md` → `research/literature/screening_criteria_v1.1.md` (20 of 203 lines differ from the committed draft);
  - `research/literature/screening_protocol_v0.2_draft.md` → `research/literature/screening_protocol_v0.2.md` (6 of 128 lines differ).
  - Git will detect the renames at staging.
- Criteria v1.1:
  - header Companion and governing decisions;
  - §1 heading and note (D-080);
  - §4 diagram and Stage-0 bullet (D-080; D-082);
  - §7 pilot reference;
  - §9 row;
  - §10 rows PREC, Q-074, D-076 (8), AUDIT-T;
  - §11 replaced by the amended freeze procedure (D-084; not executed), covering all ten requested elements and stating that the researcher reviews it before execution.
- Protocol v0.2: header Replaces and governing decisions; §3 (D-082); §6 (D-080); §7 retry and §8 audit (D-083); §11 row.
- `logs/CHANGELOG.md`, `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`: appended entries; this file is new.

## Verification
**Corrections after the read-only review** (researcher-approved, 2026-11-01), applied before the checks below:
- (A) the header line 7 of both texts now describes §11 as approved in principle only (D-084), to be reviewed and approved by the researcher before execution, and not executed;
- (B) the status cell of the criteria §9 row for D-080 to D-084 now states each decision's status, with D-084 "APPROVED IN PRINCIPLE";
- (C) this section now records actual results;
- (D) Q-082's "Needed by" is now quoted in full ("Before such a record is screened (may stay open at the freeze if recorded as open)") in D-083, the criteria §10 row D-076 (8) and this log.

**Checks run 2026-11-01, about 16:29 UTC (read-only; actual outcomes):**

| Check | Command or method | Outcome |
|---|---|---|
| Whitespace | `git diff --check` | exit 0 |
| CRLF-aware whitespace | `git -c core.whitespace=cr-at-eol diff --check` | exit 0 |
| Untracked files (two renamed texts, this log) | `grep` for trailing spaces/tabs and CR | 0 and 0 in each |
| Staging | `git diff --cached --name-only` | 0 files staged |
| v1.0 and v0.1 | `git diff --quiet HEAD --` on `screening_criteria.md` and `screening_protocol.md` | both identical to HEAD |
| Draft status | line 6 of both texts | "DRAFT for researcher review. NOT frozen. Not in force." in both; protocol §10 conditions 5 and 6 "Unmet" |
| Register | parse of `unresolved_questions.md` rows | 86 rows; no duplicate ID; every row 6 columns; Q-082 to Q-087 and Q-089 status "Open"; Q-081 Answered; Q-088 Partly answered |
| Decision IDs | parse of `DECISION_LOG.md` | IDs unique; tail D-079, D-080 to D-084, strictly increasing |
| Decision log append-only | `difflib` against `git show HEAD:logs/DECISION_LOG.md` | 0 lines removed |
| Logs append-only | prefix comparison with HEAD for CHANGELOG, PROMPT_LOG, daily review log | all three append-only |
| Procedure wording | `grep` in criteria §11 | researcher approval of the amended procedure before execution: present; explicit approval of the complete final text: present; non-authorisation statement: present; "proposed procedure" no longer used in either header |
| Q-082 quotation | `grep` for the full "Needed by" text | present in the register, D-083, criteria §10 and this log; no abbreviated quotation left |
| Active references | `grep` for `screening_criteria_v1.1_draft` / `screening_protocol_v0.2_draft` outside historical logs and reviews | 0 |
| Rename similarity | `git diff --no-index --numstat` against the HEAD drafts | criteria 26 added / 21 removed of 203 lines; protocol 8 added / 7 removed of 128 lines |
| Scope | SHA-256 of all files before and after the corrections | changed: `DECISION_LOG.md`, this log, the two renamed texts; status still shows only the 8 intended paths |

No test suite was run (no code changed). Not performed: scientific validation. The whitespace check after the final edit of this file is reported in the task report.

## Remaining
- Your review of the amended §11 procedure.
- Q-088 remainder: the final status wording and any superseded notes on v1.0/v0.1.
- Content approval of the final texts; the effective date.
- Then the freeze task. The D-035 §6 record (Q-085 to Q-087), Q-089, the tools and the D-077 (6) draw remain separate, later decisions.

## Git
Uncommitted; nothing staged; not pushed. PR #17 not changed. The researcher's choice: commit the rename separately from the later freeze commit.
