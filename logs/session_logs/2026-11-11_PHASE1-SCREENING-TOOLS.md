# Session log — 2026-11-11 — PHASE1-SCREENING-TOOLS

Covers the Phase 1 implementation (2026-11-01), the independent read-only review that followed, and the five corrections (2026-11-11). No separate session log was written for the 2026-11-01 implementation, so it is recorded here.

**Objective** (researcher prompts):
- 2026-11-01: approve the Phase 1 design defaults A1–A5, B2–B4, C2–C4, D1–D3 and D5 (D-085), and authorise Phase 1 implementation and testing with 12 restrictions (D-086).
- 2026-11-11: fix the five weaknesses found by the independent review, add regression tests, update the logs, and record the Phase 1 decisions. The blinded sheet keeps exactly seven columns, and responses stay in `pilot_decisions_researcher.csv` (D-087).

**Not authorised and not done**:
- any tool run against the real inventory, `publications.jsonl` or `source_records.jsonl`;
- real Stage-0 rows, screening rows, pilot sample or pilot sheet;
- a freeze or a final criteria identifier;
- a `.gitignore` change;
- resolving Q-082 to Q-089;
- commit, push, fetch, merge, or PR #17 changes.

## State
- **Branch and HEAD:** `claude/eloquent-mccarthy-bqtxr3-part1`, HEAD `4b56345`, unchanged throughout. Nothing staged.
- **At the start of the corrections (2026-11-11 02:34 UTC):** the uncommitted Phase 1 changes from 2026-11-01:
  - modified: `scripts/literature/pubrecords.py`, `research/literature/schemas/screening_decision.schema.json`;
  - new: `scripts/literature/stage0.py`, `pilot_sample.py`, `pilot_sheet.py`, `tests/literature/test_phase1_screening_tools.py`.

## Phase 1 implementation (2026-11-01)
- **Stage-0 generator** (`stage0.py`):
  - D-082 types (E5/E7); D-074 (a)–(c) for several types; E7 over E5 (D-074 (d), D-080);
  - A1 union guard; A2 closed list with a variant stop, *Clinical Trial Protocol* never qualifying;
  - A3 `title_abstract`; A4 UTC run date; A5 justification template;
  - append-only and idempotent.
- **Criteria-version check** (`pubrecords.py`):
  - registry file `research/literature/criteria_registry.json`, which does not exist until a freeze;
  - each entry needs the identifier, decision ID, both paths, freeze commit, both SHA-256 values and effective date (criteria v1.1 §11 step 9), and is cross-checked against the decision-log row;
  - with no registry, validation behaves as before; once one exists, a registered frozen `criteria_version` is required;
  - fail closed on any malformed or contradictory content;
  - schema: format-only `pattern`.
- **Pilot sampler** (`pilot_sample.py`):
  - D-025, D-063 and D-077 parameters unchanged: 60 records; seed 4004; frame 1,463; F 8, D 7, C 7, E 7, A 8, Q 7, B 8, untagged 8; the random-key draw;
  - CSV fields as in D-063 and protocol v0.2 §7, including `sampling_script`;
  - JSON sidecar (C2); exact frame check (C3); duplicate-pair report (C4).
- **Blinded pilot sheet** (`pilot_sheet.py`):
  - allow-list of seven columns (D5); verbatim types (D1); default name (D2); refuses non-ignored paths (D3);
  - abstract statuses use only the D-068 (8) and D-079 labels and are never inferred.
- **Tests run 2026-11-01 17:48:22 UTC:** literature 259 OK (42 new); data protection (strict) 10 OK; NHANES 29 OK; query table PASS (168 rows); `git diff --check` and the CRLF-aware check exit 0.

## Independent review (read-only)
- No governance conflict found.
- Points A, B and D verified: the format-only pattern; D-063/C2 metadata complete; the Stage-0 reading is literal to D-074 (b) "only if" plus the D-082 base rule.
- Point C (response columns) open; settled on 2026-11-11 by D-087.
- Five implementation weaknesses found; corrected below.

## Corrections (2026-11-11)
1. **Run authorisation** (`pubrecords.verify_run_authorisation`; used by all three command-line tools):
   - the reference must be a D-ID with exactly one decision row whose status starts "**APPROVED**" and whose decision text contains "Run authorisation under D-074 (f)" or "Run authorisation under D-077 (6)";
   - invented, malformed, conditional, in-principle, duplicated and wrong-clause references are refused;
   - the marker wording is a proposal (Q-090).
2. **Atomic Stage-0 write** (`stage0.write_rows_atomically`): the original bytes plus the new rows go to a temporary file in the same directory; `load_screening_decisions(lit, path=tmp)` validates it; only then `os.replace`. The temporary file is always removed.
3. **Shared guards:** `stage0.check_types` and `checked_classify`. `pilot_sample.build_frame(records, member_union_types)` uses them, so an unsupported variant or a union disagreement stops the draw.
4. **Provenance:** `stage0.load_member_union` returns the SHA-256 of `publications.jsonl` and `source_records.jsonl`. The Stage-0 report and the sampler sidecar record them.
5. **Validation:**
   - `stage0.valid_run_date` requires a real calendar date;
   - the type guards apply to D-044 in-scope records (out-of-scope records are never classified);
   - `pilot_sheet.verify_sample_provenance` refuses unless the sample and sidecar agree on size, seed, inventory SHA-256, script and stratum counts, the inventory is unchanged since the draw, and the authorisation matches.
   - `write_sheet` also refuses without a decision log to verify against.

## Tests updated and added
- **Updated (my own Phase 1 tests, for the stricter gates; no pre-existing repository test changed):**
  - `build_frame` calls now pass the member union;
  - command-line refusal tests use authorisations recorded in a fixture decision log;
  - sheet-writing tests verify their authorisation against a fixture log.
- **Added (22):**
  - run authorisation: valid; invented; malformed; wrong clause; conditional; in principle; no marker; duplicate rows; unknown clause; missing log; the real `DECISION_LOG.md` holds none;
  - Stage-0 command-line write path with input hashes and idempotent rerun; dry run; out-of-scope variant does not stop; hash mismatch;
  - atomic write: invalid combined content, forced validation failure, missing `criteria_version` column;
  - invalid calendar dates; union with a missing source record;
  - sampler shared guards: variant, disagreement, missing union, out-of-scope ignored, command line;
  - identical duplicate registry entries;
  - pilot-sheet command line: success; six sample/sidecar disagreements; inventory changed; missing sidecar; invented authorisation.
- One new test failed on its first run because of my own wrong assumption (more than 80 decision IDs; the log has 75). It now checks that specific IDs are present. No code change was needed.

## Verification (2026-11-11 02:41:02–02:42:38 UTC; actual outcomes)

| Command | Outcome |
|---|---|
| `python3 -I -B -m unittest discover -s tests/literature -p "test_phase1_screening_tools.py"` | Ran 64, OK |
| `python3 -I -B -m unittest discover -s tests/literature` | Ran 281, OK |
| `DATA_PROTECTION_STRICT=1 python3 -I -B -m unittest discover -s tests/data_protection` | Ran 10, OK |
| `python3 -I -B -m unittest discover -s tests/nhanes` | Ran 29, OK |
| `python3 -I -B scripts/literature/validate_search_queries.py research/literature/search_queries.csv` | PASS: 168 rows |
| Inventory files compared with HEAD; SHA-256 of `publications.jsonl` and `source_records.jsonl` before and after the runs | unchanged |

- No `research/literature/screening/` directory and no `criteria_registry.json` exist.
- The whitespace checks after the log edits are reported in the task report.

## Decision records
- **`logs/DECISION_LOG.md`:** D-085 (design defaults), D-086 (Phase 1 authorisation), D-087 (seven-column sheet; responses in `pilot_decisions_researcher.csv`), plus three status-history rows. IDs were checked as unused first.
- **`research/reviews/unresolved_questions.md`:** Q-090 (run-authorisation marker convention).

## Remaining
- Q-090.
- The real-frame check (1,463 and the F1 stratum sizes), at an authorised draw only.
- The freeze path: D-084, content approval, Q-088.
- The run gates: Q-085 to Q-089, D-074 (f), D-077 (6), the D4 `.gitignore` rule.

## Git
Uncommitted; nothing staged; not pushed. PR #17 not changed.
