# Session log — 2026-11-11 — STAGE-B-AUDIT-CORRECTIONS

**Objective** (researcher prompt "The final audit returned PASS WITH ISSUES. Implement the necessary corrections before the first commit", 2026-11-11):
- correct L1, L2, M2, M5, L3, M4 and L5 in the uncommitted Stage B preparation package;
- propose procedures for H1 and M1.

**Not authorised and not done**:
- real-data processing; a Stage-0 run or pilot sampling; real screening sheets;
- run authorisations or activation-condition records; a freeze;
- decisions on Q-085, Q-088, Q-091, Q-092, H1, M1 or M3;
- commit, stage or push.

## State
- **Start:** branch `claude/eloquent-mccarthy-bqtxr3-part1`, HEAD `8d9bd79b923e4ed52d104c33c6766414240999b8`, the 17 uncommitted STAGE-B-PREPARATION files, nothing staged.
- **End:** HEAD unchanged; uncommitted; nothing staged.

## Corrections
1. **M2:** `pilot_sample.verify_stage0_rows` and `APPROVED_STAGE0_CODES`, checked against the F1 row of D-063 by a test. The draw stops before drawing unless the seven Stage-0 rows match. The frame-only mode does not check the rows, so that it can run before Stage 0.
2. **M5:** `pilot_agreement.adjudicated_decisions`. An adjudication row must be for a pilot paper, at `title_abstract`, by `screener=researcher`, with a pilot decision; otherwise nothing is computed. The latest row is the agreed decision.
3. **L3:** the queue lists every duplicate pair; a member without a decision gets an empty `stage`.
4. **L5:**
   - `pubrecords.run_lock` (`O_EXCL`; released on normal exit or exception; a lock left by a killed process stays, and the run is treated as interrupted);
   - ledger events "started" and "completed" with a consistency check (`authorisation_uses`);
   - `check_authorisation_unused` refuses a started-but-never-completed run (fail closed); `require_completed_use` makes the sheet wait for the draw;
   - `write_new_file_atomically` (temporary file, `fsync`, hard link, so an existing file is never overwritten). The sheet's temporary file must be ignored by Git.
   - The sheet's output path is checked before the authorisation is consumed.
5. **M4:** D-092, D-094 and D-095 corrected. The conventions are now PROPOSED D-097 (formats, for Q-092) and D-098 (pass-rule definitions, for Q-091). M3 is referred to Q-095, and the procedure's freeze status to Q-094.
6. **H1 (proposal only):** D-099 (PROPOSED), Q-093. Already implemented as run safety: the lock, the two ledger events, fail-closed interruption. Proposed, not implemented:
   1. a dedicated commit and push after each run;
   2. a status-history row per use;
   3. the tools refuse a ledger that differs from `HEAD`;
   4. a hash chain;
   5. the ledger SHA-256 in the session log.
7. **M1 (proposal only):** D-100 (PROPOSED), Q-094.
   - Option A (recommended): merge the procedure into protocol v0.2, so that the two-file freeze covers it.
   - Option B: amend criteria v1.1 §11 (D-084) and add `procedure_path` and `procedure_sha256` to the registry.
8. **L1 and L2:** the Q-088 cell, the docstrings, criteria §11 step 1, and the protocol §10 heading.

## Audit history: decision text removed from D-092, D-094 and D-095
These rows were written in STAGE-B-PREPARATION earlier on 2026-11-11 and had not been committed. The pre-commit audit (finding M4) found that they presented assistant conventions as researcher decisions. The removed text is kept here; status-history rows in `DECISION_LOG.md` record the correction.

- **D-092** — removed or replaced text, verbatim:

  > Implementation convention (D-095), for the researcher to confirm before the first such row (Q-092): the Decision cell of each row begins with the bold sentence "D-035 §6 condition N recorded as met." for exactly one N (a decision that only mentions a condition, such as D-091, is not a condition record); a run authorisation names all six rows. Records no condition as met

- **D-094** — removed or replaced text, verbatim:

  > and gives operational definitions for the pass rule: an include/exclude conflict is resolved by an adjudication row recording the agreed decision; a disagreement on a code is a record for which exactly one screener gives that code as its primary exclusion code; an undefined κ is reported as undetermined and decided by the researcher. The assistant follows `research/literature/pilot_procedure_assistant.md` (same seven fields as the researcher's sheet; its decision file committed before the researcher's decisions are received). The D-025 thresholds (κ ≥ 0.60; no unresolved include/exclude conflict; fewer than 3 disagreements on any single code) are unchanged. The two operational definitions await the researcher's confirmation at content approval (Q-091)

- **D-095** — removed or replaced text, verbatim:

  > P16 hardened run-authorisation checks: exact D-088 status, bindings written as `criteria_version: <id>; inventory_sha256: <64 hex>; freeze_entry: D-nnn; d035_s6_records: <six D-IDs>; single_use: yes` (implementation format for D-088 (4), to be confirmed under Q-092), cross-checks of the bound rows and the criteria registry, match with the run's inputs, and a single-use ledger `screening/run_authorisation_ledger.jsonl`;

- **D-095 (second sentence)** — removed or replaced text, verbatim:

  > Restrictions: no real-data processing, Stage-0 run, pilot sample or sheet, screening output, run authorisation, freeze or D-035 §6 record; no change to scientific criteria, research questions, exclusion rules or thresholds; no commit or push | **APPROVED** — implementation and synthetic-fixture testing only

## Tests
- **19 new tests:** `Stage0RowsBeforeDraw` 4, `AdjudicationEvidence` 4, `RunConcurrencyAndInterruption` 6, `NoOverwriteOutputs` 5.
- **Updated:**
  - fixtures add a completed draw to the ledger before the sheet, and Stage-0 rows before a draw;
  - ledger assertions expect the two events;
  - `adjudicated_ids` became `adjudication_rows`;
  - the queue expectation now includes all pairs.
- No test was skipped or removed.
- **Mutation check:**

  | Safeguard disabled | Tests failing |
  |---|---|
  | Stage-0 row check | 2 |
  | adjudication screener check | 1 |
  | lock `O_EXCL` | 3 |
  | interrupted run consumes the authorisation | 1 |

  The source was restored and compared byte for byte.

## Verification (2026-11-11 08:42:24–08:44:01 UTC; actual outcomes)

| Command | Outcome |
|---|---|
| `python3 -I -B -m unittest discover -s tests/literature -p "test_phase1_screening_tools.py"` | Ran 126, OK |
| `python3 -I -B -m unittest discover -s tests/literature` | Ran 343, OK |
| `DATA_PROTECTION_STRICT=1 python3 -I -B -m unittest discover -s tests/data_protection` | Ran 10, OK |
| `python3 -I -B -m unittest discover -s tests/nhanes` | Ran 29, OK |
| `python3 -I -B scripts/literature/validate_search_queries.py research/literature/search_queries.csv` | PASS: 168 rows |
| SHA-256 of the ignored data files before and after; `git diff --quiet HEAD` on the inventory, records, scope, raw exports, v1.0 and v0.1 | unchanged |

- **ID check:** D-097 to D-100 and Q-093 to Q-095 were checked as unused. "D-100" also occurs as the name of a laboratory instrument (Bio-Rad D-100) in the experimental protocol draft and the changelog. This is not a decision reference.

## Remaining
Researcher decisions:
- Q-085, Q-088 (status wording), Q-091 (D-098), Q-092 (D-097), Q-093 (D-099), Q-094 (D-100), Q-095;
- the D-090 reading.

Not changed (outside the requested scope):
- D-090 still contains an assistant reading inside an approved row, flagged for confirmation;
- D-091 item (a) is ambiguous.

## Git
Uncommitted; nothing staged; not pushed. PR #17 not changed.
