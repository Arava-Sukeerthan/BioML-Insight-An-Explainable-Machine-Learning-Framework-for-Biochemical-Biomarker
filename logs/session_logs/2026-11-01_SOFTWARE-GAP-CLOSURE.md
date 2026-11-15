# Session log — 2026-11-01 — SOFTWARE-GAP-CLOSURE

**Objective** (researcher prompt 2026-11-01, "November 1 Software Gap Closure"): investigate and, where safe, close the remaining software-testing gaps listed in the DEFECT-CORRECTION-AB review, with offline synthetic tests. Document failure paths that cannot be tested safely or deterministically.

**Not authorised and not done**: staging, commit, push, fetch, pull, merge, rebase, reset, clean, stash, checkout or branch switch; PR #17 changes; network or external APIs; real NHANES records; screening sample or freeze; model training; decision-log entries or question-status changes; protocol changes.

## Starting state (verified 2026-11-01 07:31 UTC)
- **Branch and HEAD:** `claude/eloquent-mccarthy-bqtxr3-part1`, HEAD `93dd16dbfa8ed5cd6764070309eb6695787f27d1`; nothing staged.
- **Modified (7):** `logs/CHANGELOG.md`, `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, `scripts/literature/fetch_crossref.py`, `scripts/literature/pubrecords.py`, `scripts/nhanes/safeguards.py`, `tests/literature/test_crossref_verification.py`.
- **Untracked (3):** `logs/session_logs/2026-11-01_DEFECT-CORRECTION-AB.md`, `tests/literature/test_crossref_robustness.py`, `tests/nhanes/test_safeguards_corrections.py`.
- **Timestamps:** none later than the DEFECT-CORRECTION-AB logging (07:28–07:29 UTC). SHA-256 values were recorded in the session scratchpad.

## Changes and reasons
1. **`scripts/literature/fetch_crossref.py`:**
   - `save_raw(..., warnings=None)` records a failed directory `fsync` in `report["warnings"]`; previously the failure was ignored silently. The key is removed when empty, so successful reports keep their earlier shape.
   - A `persistence_error` entry records `file_saved` and `manifest_row_present`. A manifest `fsync` that fails after the row was written leaves a registered row, and the report previously did not show this.
   - Neither change alters what is written to disk.
2. **`scripts/literature/pubrecords.py`:** comment only. The inline-markup tag list is labelled as an implementation assumption (see "Markup evidence").
3. **`tests/literature/test_crossref_failure_paths.py`** (new, 20 tests).
4. **`tests/nhanes/test_cascade_equivalence.py`** (new, 2 tests).

## Tests added and what they cover (all synthetic; `urlopen` patched to fail; temporary directories)
| Gap | Test(s) | Behaviour shown |
|---|---|---|
| 1 Manifest `fsync` failure | `test_manifest_fsync_failure_is_reported_with_the_state_on_disk`; `…on_a_new_manifest_keeps_a_parseable_file` | Run stops (`aborted`) with the report. The row is present and parseable but its durability is unconfirmed. The lock is released, and on resume the paper is skipped as already registered (no duplicate) |
| 2 Directory `fsync` failure | `test_directory_fsync_failure_keeps_the_file_and_warns`; `test_no_warnings_key_when_nothing_went_wrong` | File saved and registered; one warning; no `warnings` key on a clean run |
| — `.partial` `fsync` failure | `test_partial_file_fsync_failure_stops_before_any_final_file` | No final file, no manifest; the `.partial` is reported as an orphan |
| 3 Exit status, failed responses | `test_failed_response_exits_1`; `test_exhausted_retries_exit_1` | `main()` returns 1; report printed as JSON |
| 4 Exit status, malformed responses | `test_malformed_response_exits_1` (non-JSON, wrong shape, DOI mismatch) | `main()` returns 1; nothing saved |
| — Other exit statuses | `test_all_saved_exits_0_and_dry_run_exits_0`; `test_refused_run_exits_1` | 0 for saved and dry-run; 1 for refused (no request) |
| 5 Report with failing records | `test_mixed_outcomes_produce_one_complete_report` | failed / malformed / error / saved in one report; only the saved paper registered; no orphans; lock released |
| 6 Planning failures | `test_missing_inventory_raises_…`; `test_unreadable_inventory_raises_…` | **Actual behaviour:** an exception is raised and no run report is produced (a limitation), but nothing is written: no lock, raw file or manifest |
| 6 Keyboard interrupt | `test_keyboard_interrupt_between_papers`; `…during_save_leaves_an_orphan_and_a_resumable_state` | **Actual behaviour:** the interrupt propagates and no report is produced (a limitation). The lock is released in `finally`, earlier saves stay registered, and an interrupted save leaves only a `.partial` orphan. The run resumes with the same date |
| 7 Recovery | `test_truncated_partial_file_from_a_crash`; `test_orphan_final_file_is_never_registered_by_a_later_run`; `test_incomplete_manifest_line_then_manual_repair`; `test_stale_lock_then_manual_removal`; `test_dry_run_never_takes_the_lock_or_writes` | Orphans are kept and skipped by numbering. A damaged manifest refuses the run until it is repaired by hand. A stale lock refuses until it is removed by hand |
| NHANES cascade vs `descriptive_counts.py` | `test_same_counts_as_period_counts_on_synthetic_tables`; `test_fixture_exercises_every_cascade_step` | Identical cascade and subcategory counts on synthetic tables covering every E0–E8 step, with `read` replaced and `pandas.read_sas` patched to fail |

**How failures were injected**: the module-level `os` reference of one module was replaced by a proxy that fails a chosen call (`fsync`, `link`), or a transport raised `KeyboardInterrupt`. These are deterministic points in the code. They do not reproduce a power loss or kernel crash.

**Mutation check of the new tests (scratch copies, then deleted)**: 10 of 11 reintroduced defects were caught. The survivor (E6 rule written as `RIDEXPRG != 1` instead of `~(RIDEXPRG == 1)`) gives the same result in pandas for missing values (both keep them), so it is an equivalent mutation, not a missed defect.

## Evidence categories
- **Tested behaviour (synthetic):** every row of the table above.
- **Inferred from code inspection only:**
  - the final file name either does not exist or holds the complete body, assuming POSIX hard-link semantics;
  - a single `write` followed by `fsync` limits a damaged manifest to one incomplete last line, which is then detected.
  - Neither is a guarantee of atomicity on every filesystem.
- **Untested failure paths:**
  - real power loss or kernel crash;
  - concurrent runs beyond the lock check (the race between the `exists` check and the exclusive create is covered by `O_EXCL` only);
  - a failure inside the bookkeeping in `finally` (orphan listing after a manifest read error);
  - the first planning-time read of the manifest when the file is unreadable.
- **Real-data validation outstanding:** real Crossref responses (layout and markup); real NHANES files (cascade equivalence, value encodings, XPT missing values). The NHANES data folder and any codebook are absent from this repository.

## Markup evidence (review, no tag-list change)
- **Documented project evidence:** none for Crossref markup. The repository has no document describing Crossref title markup (searched for JATS, MathML, `<sub>` and Crossref markup).
- **Only related project evidence:** PubMed connector titles in `raw_exports` carried no markup (0 tags in 3,273 articles, checked read-only on 2026-10-31).
- **Assumptions:** every entry in `INLINE_MARKUP_TAGS` (JATS/HTML inline formatting, MathML presentation elements), and the choice to replace unknown tags with a space.
- PubMed parsing (`strip_markup`) is unchanged.

## NHANES review (no change to `safeguards.py`)
- **Aliases and allow-list:** the alias list is an assistant proposal, not approved. The allow-list mechanism is tested, but the approved list depends on Q-050 (open). Insulin handling (S-06) is not decided.
- **`LBXGLT`/`LBDGLTSI`:**
  - The project contains no authoritative evidence for these names. Protocol draft §7 names only the OGTT category; there is no local codebook; `data/` is absent.
  - They remain unverified. They are kept on the prohibited list, where an error can only cause a false rejection, and are labelled as recalled, not verified, in the code.
- **Participant IDs, partitions and folds:** tested as reported in DEFECT-CORRECTION-AB; fold coverage is opt-in; stratification is not checked; nothing is integrated into a pipeline.
- **Cascade subcategories:** names match `period_counts`, and the counts match on synthetic tables (new test). Real-data equivalence remains unverified.
- **Protocol §7 derived-index wording (SPISE):** not changed. No evidence in the repository settles it, and no change is authorised.

## Checks (2026-11-01, 07:35:52–07:37:07 UTC; `python3 -I -B`)
| Command | Exit | Result |
|---|---|---|
| `python3 -I -B -m unittest discover -s tests/literature` | 0 | Ran 197 tests, OK |
| `DATA_PROTECTION_STRICT=1 python3 -I -B -m unittest discover -s tests/data_protection -v` | 0 | Ran 10 tests, OK |
| `python3 -I -B -m unittest discover -s tests/nhanes -v` | 0 | Ran 29 tests, OK |
| `python3 -I -B scripts/literature/validate_search_queries.py research/literature/search_queries.csv` | 0 | PASS: 168 rows |
| `sh -n scripts/run_checks.sh` | 0 | OK |
| `git diff --check` | 0 | OK |

**ResourceWarnings** (investigated, not suppressed): 470 warning lines in the literature run, the same count as before this phase.
- **Unclosed files (146):** 5 `open()` calls without a context manager in `scripts/literature/make_literature_reports.py` (lines 76, 78, 167, 239, 291; the same pattern exists at `eb79996`), plus files in older test modules.
- **Implicitly cleaned temporary directories (89):** from older test modules.
- **By test module:** `test_screening_and_ids.py` 264, `test_t1a_schema_validation.py` 138, `test_pubrecords.py` 58, `test_crossref_verification.py` 10 (its existing report test calls `make_literature_reports.main`), `test_crossref_robustness.py` 0, `test_crossref_failure_paths.py` 0.
- **NHANES and data-protection runs:** no warnings.

## Git state
HEAD `93dd16d` (preservation commit, unchanged); branch unchanged; nothing staged; nothing committed, pushed or fetched. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.
