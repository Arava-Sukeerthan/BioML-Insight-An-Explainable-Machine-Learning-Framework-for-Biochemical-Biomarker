# Session log — 2026-11-11 — STAGE-B-PREPARATION

**Objective** (researcher prompt "Proceed with the approved BioML-Insight Stage B preparation work", 2026-11-11):
- implement P1 (documentation refresh), P15 (frame-only validation), P16 (authorisation hardening), P17 (frame identity), P18 (pilot follow-on tools) and the D4 ignore rules, with synthetic fixtures only;
- record the approved decisions: P2, P3, Q-086, Q-087, Q-089, P19, and the agreement and blinding clarification;
- report the evidence on Q-085 without deciding it.

**Not authorised and not done**:
- processing of real research data, including a real frame-only check;
- a Stage-0 run, a pilot sample or sheet, screening outputs;
- a run-authorisation row, a freeze, a D-035 §6 record;
- any change to scientific criteria, research questions, exclusion rules or thresholds;
- commit or push.

## State
- **Start:** branch `claude/eloquent-mccarthy-bqtxr3-part1`, HEAD `8d9bd79b923e4ed52d104c33c6766414240999b8`, clean working tree, in sync with the remote.
- **End:** HEAD unchanged; uncommitted changes; nothing staged.

## Work
1. **P16 — `scripts/literature/pubrecords.py`.** `verify_run_authorisation` now refuses unless all of the following hold:
   - the reference has one decision row, and its Decision cell begins with the clause marker (D-088 (2));
   - the status is exactly `**APPROVED** — run authorisation (single use)` (D-088 (3));
   - the Decision cell binds `criteria_version`, `inventory_sha256`, `freeze_entry`, `d035_s6_records` (six IDs) and `single_use: yes`, each exactly once (D-088 (4), syntax under D-095);
   - the freeze entry is one approved decision row, and the registry entry of the bound version names it;
   - the six §6 rows are distinct and approved, and each begins with the bold sentence "D-035 §6 condition N recorded as met." for one N, covering 1–6 (D-092 convention);
   - the run's inventory SHA-256 and `criteria_version` equal the bound values, when the tool passes them.

   Single use is enforced by an append-only ledger, `screening/run_authorisation_ledger.jsonl`. The three tools pass their inputs and use the ledger.

   An earlier draft of the §6 check accepted any approved row that mentioned "D-035 §6 condition N". Then D-091, which only defines condition 6, could have been bound as a condition record. The check now requires the bold sentence at the start of the cell, and a test covers this case.
2. **P17 and P15 — `pilot_sample.py`.**
   - `load_scope_snapshot` checks the snapshot file against its recorded SHA-256 (`D-044_scope_snapshot.md`).
   - `verify_frame_identity` requires the frame to equal the snapshot minus the seven F1 Stage-0 IDs. Missing, additional and duplicated IDs are refused, and the check runs before any draw.
   - `--frame-only` runs the frame checks and prints counts and hashes. It does not draw, write or use an authorisation.
   - The frame constants are passed explicitly, so a test can replace them.
3. **P18 — `pilot_agreement.py`.**
   - Cohen's κ, cross-checked against a 2×2 example (κ = 0.40) and a three-level example worked by hand (κ = 0.36/0.66);
   - the agreement measures and the D-025 pass evaluation (thresholds unchanged);
   - the researcher decision template (paper IDs only);
   - the adjudication-queue builder.

   The assistant procedure is in `research/literature/pilot_procedure_assistant.md` (DRAFT).
4. **D4 — `.gitignore` and `tests/data_protection`.**
   - Ignored: the blinded sheet and the temporary files.
   - Trackable: the decision and audit files, and `criteria_registry.json`.
   - Data-protection tests: four ignored paths and nine trackable paths added.
5. **P1 — the two drafts.** Phase 1 and this package are reflected, and stale statements are corrected. No scientific rule changed; each change is listed in the traceability tables (criteria §9, protocol §11).
6. **Decisions and register.**
   - D-089 to D-096 recorded, with status-history rows. IDs were checked as unused first.
   - Q-086, Q-087 and Q-089 answered. Q-088 stays partly open.
   - Q-091 (pass-rule definitions) and Q-092 (authorisation formats; frame-only authorisation) added.

## Q-085 evidence (not a decision)
Q-085 asks whether D-027 and D-024 count as "approved" under D-035 record §6 condition 3, which reads "D-027 and D-024 (screening-file and inventory schemas) are approved".

- **D-027:** status **APPROVED (limited)** (researcher, 2026-10-30, ballot Item 1 option (a)). It covers `screening/decisions.csv`, its required columns and the key `source_record:<source_record_id>`. It does **not** cover:
  - the optional descriptor columns, which its row says follow D-028, D-029 and Q-035;
  - part (b), the inventory `screening_status` enum, which follows D-024.

  The descriptor columns were later fixed by D-028 and D-029 (APPROVED) and D-060 (APPROVED — CONDITIONAL), and implemented in T1-A (`d1aaceb`).
- **D-024:** status **APPROVED — CONDITIONAL**, "with the D-028 and D-029 revisions". Its row says:
  - the condition "R5 resolved" was met at decision level by D-060;
  - "the revised fields are not yet implemented". This wording predates T1-A (`d1aaceb`) and T2 (`bf0c579`), which implemented and rebuilt them (criteria v1.1 §9).
  - Q-034 (the `extraction_status` enum) is not included. It concerns extraction, not screening.
- **For "approved":** both are approved by the researcher. The parts excluded from D-027 are covered by other approved decisions, and D-024's condition is met at decision level.
- **Against:** D-027 is explicitly "limited", and D-024 is "CONDITIONAL". Condition 3 does not say whether limited or conditional approval suffices.

The decision is the researcher's (Q-085 stays Open).

## Tests updated
- Fixtures now write complete authorisations, because the checks are stricter.
- The fixture freeze entry is D-999. The "invented reference" case therefore uses D-977.
- `test_cli_write_path_hashes_and_idempotence` was renamed `…_and_single_use`. A second `--write` is now refused; dry-run idempotence is still tested.
- `test_default_path_in_this_repository_is_not_ignored` was renamed `…_is_ignored` (D4).
- A changed inventory is now refused by the inventory binding check, before the provenance check. The expected message changed accordingly.
- No test was skipped or removed.
- **Mutation check** (source restored from a backup afterwards and compared byte for byte):

  | Safeguard disabled | Tests failing |
  |---|---|
  | exact-status check | 1 |
  | single-use check | 4 |
  | identity check | 3 |

## Verification (2026-11-11 04:28:22–04:30:04 UTC; actual outcomes)

| Command | Outcome |
|---|---|
| `python3 -I -B -m unittest discover -s tests/literature -p "test_phase1_screening_tools.py"` | Ran 107, OK |
| `python3 -I -B -m unittest discover -s tests/literature` | Ran 324, OK |
| `DATA_PROTECTION_STRICT=1 python3 -I -B -m unittest discover -s tests/data_protection` | Ran 10, OK |
| `python3 -I -B -m unittest discover -s tests/nhanes` | Ran 29, OK |
| `python3 -I -B scripts/literature/validate_search_queries.py research/literature/search_queries.csv` | PASS: 168 rows |
| SHA-256 of `publications.jsonl`, `source_records.jsonl` and `paper_inventory.json`, before and after | unchanged |
| `git diff --quiet HEAD` on the inventory, records, scope and raw exports | unchanged |

- No `research/literature/screening/` directory and no `criteria_registry.json` exist.
- The whitespace checks after the log edits are reported in the task report.

## Remaining
- Researcher decisions: Q-085; Q-088 (status wording); Q-091; Q-092; confirmation of the D-090 reading ("ready" = the freeze commit).
- The remaining steps, in order:
  1. content approval of criteria v1.1, protocol v0.2 and the assistant procedure;
  2. approval of the §11 procedure (D-084);
  3. freeze, freeze entry and registry;
  4. six §6 condition rows;
  5. D-074 (f) authorisation, then Stage 0;
  6. D-077 (6) authorisation, then the draw and the private sheet.

## Git
Uncommitted; nothing staged; not pushed. PR #17 not changed.
