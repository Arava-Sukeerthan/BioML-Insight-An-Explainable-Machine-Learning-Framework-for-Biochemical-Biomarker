# Session log — 2026-11-01 — DEFECT-CORRECTION-AB

**Objective**: correct the confirmed defects found by the independent read-only audit (2026-10-31) of Workstream A (Crossref verification lookups) and Workstream B (NHANES safeguards), with targeted synthetic regression tests (researcher prompt 2026-10-31). Then review the corrections, rerun the checks and record the task (researcher prompt 2026-11-01). The corrections were made on 2026-10-31; the review and this record were made on 2026-11-01. The task label was chosen by the assistant.

**Authorised**:
- code and test corrections for the listed defects (2026-10-31);
- append-only entries in `logs/CHANGELOG.md`, `logs/PROMPT_LOG.md` and `research/reviews/daily_review_log.md`, and this session log (2026-11-01).

**Not authorised and not done**: commit, push, fetch, merge, branch change, scientific decisions or decision-status changes, screening freeze or sample, external API calls or downloads, real-data experiments, model training, Workstream C, PR #17 changes.

## Starting state (verified 2026-11-01 07:24 UTC)
- **Repository:** `/home/user/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker`, branch `claude/eloquent-mccarthy-bqtxr3-part1`, HEAD `93dd16dbfa8ed5cd6764070309eb6695787f27d1` (preservation commit).
- **Staging:** nothing staged; no stashes.
- **Modified:** `scripts/literature/fetch_crossref.py`, `scripts/literature/pubrecords.py`, `scripts/nhanes/safeguards.py`, `tests/literature/test_crossref_verification.py`.
- **Untracked:** `tests/literature/test_crossref_robustness.py`, `tests/nhanes/test_safeguards_corrections.py`.
- **Modification times:** all from the corrections of 2026-10-31 (17:45–17:54 UTC); no later change.

## Corrections (2026-10-31)
### Workstream A — Crossref
1. **Persistence:**
   - the response is written to `CR_<date>_<nnn>.json.partial` (exclusive create, `fsync`) and read back by SHA-256;
   - it is hard-linked to the final name (never overwriting) and the run's own `.partial` is removed;
   - it is then registered with a single `fsync`'ed manifest append;
   - `register_raw` refuses a manifest whose last line is incomplete.
2. **Recovery:**
   - a damaged manifest (incomplete last line, wrong column count, wrong header), a malformed run date or an existing lock file refuses the run before any request;
   - already-registered papers are skipped, so a run resumes with the same date, and new files take the next free number;
   - unregistered `CR_*` files are reported as orphans and never deleted;
   - repair of a damaged manifest and removal of a stale lock are manual.
3. **Malformed structures:**
   - `title` and `container-title` must be lists of strings, `author` a list of objects with string name parts, `DOI` a string;
   - the year fields (inactive until the year rule is decided) need well-formed `date-parts`;
   - a non-object Crossref file stops the build.
4. **Route restriction:** `VERIFY-CR-` query IDs only with route `crossref_works`, and that route only for those IDs; checked in `register_raw` and in `build_source_records`.
5. **Per-record exceptions:**
   - an unexpected transport error is recorded for that paper and the run continues;
   - any exception during response checking is recorded as `malformed`;
   - a persistence error stops the run with the report returned;
   - the lock is released in all cases.
6. **Inline markup:**
   - Crossref-only `strip_inline_markup` removes inline tags (sub, sup, i, b, MathML and similar) without a space; other tags become a space;
   - PubMed connector titles contained 0 tags in all 3,273 articles checked (read-only), so ordinary parsing (`strip_markup`) was left unchanged.
7. **No-year behaviour:**
   - documented in `auto_verification` and tested; behaviour unchanged;
   - without a year rule Crossref never verifies, but its conflicts give `needs_review` (D-064 A4); changing that would need a decision.
8. **Retries and exit status:**
   - `http.client.HTTPException` is retried like `OSError`;
   - the exit status is 1 unless every paper ends saved, already registered or dry-run.

### Workstream B — NHANES safeguards
1. **E3:** only real booleans are accepted; missing, text (e.g. a merge indicator), numeric and NA values raise instead of being coerced to True.
2. **IDs:** `SEQN` must be unique and non-missing when present; `check_unique_participants`; missing IDs rejected in `check_disjoint_participants`, `check_partitions` and `check_folds`.
3. **Aliases:**
   - whole-token aliases for the protocol section 7 categories (glucose/HbA1c, survey and processing, diabetes questionnaire and medication);
   - OGTT names `LBXGLT`/`LBDGLTSI` added (from memory, **not checked against a codebook**);
   - optional allow-list in `check_predictors`; the approved list depends on Q-050.
   - Not prohibited: insulin, glutamate-like `GLU` tokens and body weight.
4. **Whole-word matching:** derived-index names are matched as whole tokens or joined neighbouring tokens, not as substrings; the comment-code rule is limited to NHANES-style names (letters and digits, at most 8 characters).
5. **Partitions:** `check_partitions` requires non-empty, unique, pairwise-disjoint partitions and optionally exact coverage of an expected ID set.
6. **Folds:**
   - `check_folds(..., ids=, require_partition=)` rejects participants with rows in both train and test, non-integer indices and length mismatches;
   - optionally, it requires every row to be tested exactly once and train plus test to cover all rows.
7. **Cascade:** optional `details` with the subcategory counts of `descriptive_counts.period_counts`, plus `E7_excluded_other_code` and the number excluded at each step.

## Review outcome (2026-11-01)
| Item | Classification | Remaining gap |
|---|---|---|
| A1 persistence | Corrected but insufficiently tested | Injected failures (fsync, read-back, link, registration) are tested. Manifest and directory `fsync` are not directly tested. Crash recovery only; atomicity not guaranteed (POSIX hard links and fsync assumed) |
| A2 recovery | Corrected and adequately tested | Manifest repair and stale-lock removal are manual by design |
| A3 malformed structures | Corrected and adequately tested | Real Crossref response layout not inspected |
| A4 route restriction | Corrected and adequately tested | — |
| A5 per-record exceptions and report | Corrected but insufficiently tested | No report if planning raises (e.g. unreadable inventory) or on a keyboard interrupt; the report goes to standard output only; malformed response bodies are reported, not retained |
| A6 inline markup | Corrected and adequately tested (synthetic) | The tag list is an assumption; real Crossref markup not inspected |
| A7 no-year and conflicts | Documented and tested; behaviour unchanged by design (D-064 A4) | A change would need a researcher decision |
| A8 retries and exit status | Corrected but insufficiently tested | Retries tested. Exit status 1 for failed or malformed outcomes is not tested through `main()` |
| B1 E3 flags | Corrected and adequately tested | — |
| B2 participant IDs | Corrected and adequately tested | `SEQN` check only when the column is present |
| B3 aliases | Partially corrected | Alias list is an unapproved assistant proposal and cannot be complete; OGTT names not codebook-checked; allow-list awaits Q-050; insulin-derived features undecided (S-06) |
| B4 whole-word matching | Corrected and adequately tested for the listed cases | Joined-token matching could still produce rare false positives |
| B5 partitions | Corrected and adequately tested | Not integrated into any pipeline |
| B6 fold coverage | Corrected and adequately tested | Opt-in (`require_partition` defaults to False); stratification not checked |
| B7 cascade subcategories | Corrected and adequately tested (synthetic) | Equivalence with `descriptive_counts.py` on the real files unverified |

**Evidence handling**:
- Failure paths never overwrite or delete an existing file.
- Unregistered files are kept and reported.
- Authoritative publication fields and provenance are untouched: tested in `TestNoYearRuleAndConflicts` and in the existing build-safeguard tests.

## Checks
- **Rerun (2026-11-01, 07:26:02–07:27:10 UTC):**

| Command | Exit | Result |
|---|---|---|
| `python3 -I -B -m unittest discover -s tests/literature` | 0 | Ran 177 tests, OK |
| `DATA_PROTECTION_STRICT=1 python3 -I -B -m unittest discover -s tests/data_protection -v` | 0 | Ran 10 tests, OK |
| `python3 -I -B -m unittest discover -s tests/nhanes -v` | 0 | Ran 27 tests, OK |
| `python3 -I -B scripts/literature/validate_search_queries.py research/literature/search_queries.csv` | 0 | PASS: 168 rows |
| `sh -n scripts/run_checks.sh` | 0 | OK |
| `git diff --check` | 0 | OK |

- **Warnings:** the literature tests emitted 470 warning lines: 146 "unclosed file" warnings (from `make_literature_reports.py` and older tests) and 89 "implicitly cleaning up" temporary-directory warnings, each with its traceback hint. None come from the new test files, and none are failures. The NHANES and data-protection runs emitted no warnings.
- **Read-only checks on the real manifest:**
  - `fetch_crossref.manifest_problems("research/literature")` returned `[]`, and `orphans(...)` returned `[]`;
  - the `MANIFEST.csv` SHA-256 was unchanged (`c79c3abf39212d2b…`).
- **Earlier evidence (2026-10-31), still present in the session scratchpad, which is not preserved:**
  - **Mutation check:** 26 defects reintroduced one at a time in scratch copies. The first run caught 24 of 26; that output was not kept and is recorded from the session transcript. Two tests were then tightened, and the second run caught 26 of 26 (`defectfix/mutation_results.txt`).
  - **Regression:** build and reports on two scratch copies of `research/literature`, one with the code at `93dd16d` and one with the corrected code. 284 of 284 files were identical; `build_report.json` differed only in `built_at` (`defectfix/regression_comparison.txt`).
  - **Code used:** on 2026-11-01 I confirmed that the scratch copy of the corrected code matches the current working-tree `scripts/`, and that the HEAD copy matches `git show HEAD`.
  - **Separate finding:** the generated files committed to the repository differ from both runs (`publication_type` in all 3,386 records; `collection_stats`; `verification_report`) because they predate the unauthorised T2 rebuild.

**Scope of the evidence**: unit tests on synthetic fixtures with a fake transport (`urlopen` patched to fail). No Crossref request was made and no NHANES file was read. Nothing here validates behaviour on real Crossref responses or real NHANES data.

## Scientific dependencies (not decided here)
- Q-050 (approved predictor lists; needed for the allow-list).
- S-06 and insulin-derived features.
- Approval of the NHANES alias list.
- Codebook check of `LBXGLT`/`LBDGLTSI`.
- Crossref year field.
- D-068 (5) reading; Workstream C; T2; screening freeze (D-035 §6 conditions 5 and 6).
- Q-044, Q-046, Q-047, Q-055, Q-060, Q-061; D-013 to D-020.
- **Observation (unverified, not changed):** protocol draft §7 says every listed derived index contains glucose, HbA1c or insulin; as recalled, SPISE uses only HDL, triglycerides and BMI.

## Files changed
- **On 2026-10-31 (corrections):** `scripts/literature/pubrecords.py`, `scripts/literature/fetch_crossref.py`, `scripts/nhanes/safeguards.py`, `tests/literature/test_crossref_verification.py` (modified); `tests/literature/test_crossref_robustness.py`, `tests/nhanes/test_safeguards_corrections.py` (created).
- **On 2026-11-01 (logging):** append-only entries in `logs/CHANGELOG.md`, `logs/PROMPT_LOG.md` and `research/reviews/daily_review_log.md`; this file (created).
- **Unchanged:** `logs/session_logs/2026-10-31_PRESERVATION-FIRST.md`, `logs/session_logs/2026-10-31_PR17-DESCRIPTION-UPDATE-2.md`, `DECISION_LOG.md`, `unresolved_questions.md`, the drafts, the inventory and generated outputs.

## Git state
- HEAD `93dd16d` (preservation commit, unchanged); all changes of this task are uncommitted and unstaged; not pushed; not fetched.
- The local tracking ref `origin/claude/eloquent-mccarthy-bqtxr3-part1` = `e0dd690`; the remote state is unverified.
- PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.
