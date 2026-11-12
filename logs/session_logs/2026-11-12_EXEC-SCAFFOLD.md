# Session log — 2026-11-12 — EXEC-SCAFFOLD

**Prompt**: researcher prompt "PROJECT: BioML-Insight. ABSOLUTE PROJECT DEADLINE: 27 NOVEMBER 2026" (2026-11-12).

**Decisions taken by the assistant (technical; within permissions)**:
1. numpy and pandas only, because nothing else is installed.
2. No classifier fitted, even on synthetic data (D-040 Rule S). The harness is tested with a non-learning stub; only post-hoc maps with at most two parameters (Platt) and preprocessing statistics are estimated in tests.
3. Reuse of `safeguards.eligibility_cascade` and the existing hash list.
4. A real-data guard in the harness and the loader.
5. A BL-1 grid of 8 x 5 = 40, matching the equal budget.
6. XGBoost proposed for BL-3 and F2 (Q-048); k-NN proposed for BL-6 (Q-049).
7. Threshold rule implemented as the largest threshold with sensitivity >= target (flagged).

**Files**: see CHANGELOG EXEC-SCAFFOLD.

**Tests** (2026-11-12, about 06:20–06:40 UTC):
- tests/models: 43 OK;
- tests/nhanes: 39 OK;
- tests/literature: 365 OK;
- data protection (strict): 10 OK;
- query table: PASS 168 rows;
- `sh scripts/run_checks.sh`: all passed.

**Mutation checks** (each detected):

| Mutation | Detected by |
|---|---|
| Preprocessing refit on test rows | 1/1 failing |
| Conformal under-coverage | 1/1 failing |
| Budget of 39 | 1/1 failing |
| AUROC ties | 1/1 failing |
| Calibrator refit on validation labels | 1/1 failing |

Restored: 0/12 failing.

**Not done**: no real data, download, classifier training, screening, Stage 0, sampling, decision-log change or Git operation.

## Follow-up (EXEC-SCAFFOLD-2, same day)
- Consolidated approval request written (`research/reviews/2026-11-12_CONSOLIDATED-APPROVAL-REQUEST.md`).
- Dry run in a temporary directory: the draft D-121 was refused ("binding 'single_use' is malformed"). The corrected text is accepted, and wrong hash, criteria version and clause are refused.
- Added `explain.py`, `survey.py` and `compare.py`; harness prediction return (in memory only).
- Tests: models 52 OK; nhanes 39 OK.

## Follow-up (EXEC-SCAFFOLD-3, same day)
- **Added:** `report.py`; the dataset CLI; protocol v1.0 freeze candidate (change set); manuscript methods draft; the evidence-status section in the approval request; dependency findings in `environment/README.md`.
- **pip dry run:** resolves; `wrapt 2.6.0.dev1` (pre-release) via formulaic; `nvidia-nccl-cu13` 206.6 MB via xgboost. Nothing installed; pins unchanged.
- **Tests:** see the CHANGELOG and the final report.

## Follow-up (EXEC-SCAFFOLD-4, same day)
- **Harness:**
  - threshold-scale defect corrected (the D-cal threshold is no longer applied to uncalibrated out-of-fold predictions);
  - calibrated internal estimate added;
  - `_summarise` hardened;
  - `calibrator_order_preserving` recorded.
- **Mutation check:** reverting the harness line makes `test_threshold_only_used_on_its_own_probability_scale` fail (1/25 in that file); restored, 0 failing.
- **Protocol v1.0 candidate:** §9 review, R1–R9.
- **Manuscript:** 01, 03 and 05 added; 02 §2.4 corrected.
- **D-064 export probe:** `<scratchpad>/probe_d064_exports.py` (not in the repository).

  | Case | Outcome |
  |---|---|
  | E1, no year rule | `partially_verified` ("crossref lacks year") |
  | E1, test-only year rule | `verified` |
  | E1b, paper not in the pilot list | build refused |
  | E2, publisher transcription, spot-check passed | `verified`, but enters as query `Q-TEST-PUB` |
  | E2, spot-check not done | `partially_verified` (independence undetermined) |

- **CDC re-check (HEAD only), 07:18:41Z:**
  - 32/32 files reachable; Content-Length equals the recorded bytes;
  - the old-style `DEMO_J.XPT` path returns an HTML page;
  - Crossref and E-utilities: CONNECT 403.

### Critical path to 2026-11-27 (assessment, not a decision)
Order (D-108, then D-019):
1. **Your decisions:** A1 + A2 (custodian), A3, A4, A5, A6, Q-098 and Q-099.
2. Record D-114 to D-121; commit; Stage 0 (same day).
3. Pilot draw (D-077 (6)) → the custodian's commitment C → the blinded pilot, both screeners (about 1 day each, depending on the custodian) → κ and the pass rule. A failed pilot means a second pilot (Q-083), about +5 days.
4. Title/abstract screening of the 1,470 in-scope records → the researcher audit (25 + 25) → full texts in tier order, RQ5 first → the RQ5 closest-prior-art check → D-016 (contribution wording).
5. **Gates C/D (D-042)** → D-017, D-018, D-019 freeze (v1.0 candidate + R3/R9 + Q-054) → install (A3) → synthetic verification (A4) → download authorisation (hashes re-checked) → build → experiments: 5 seeds × 7 methods × 3 groups, plus sensitivity analyses.
6. Citations: Crossref exports + an authorised rebuild + a new fixed-inventory entry → results, discussion → submission package.

Today is Day 30, so 15 days remain. Steps 3–5 are strictly sequential, and steps 1 and 3 depend on people.

### Reduced-scope plan if the full breadth becomes infeasible
Declared before any result, and applied only by your decision at the D-019 freeze.

**Never reduced:**
- the primary research question;
- Q1–Q3;
- temporal validation (applied once, frozen);
- equal tuning budgets;
- in-fold preprocessing;
- the real-data guard;
- reporting of null results.

**Reduction tiers, in this order:**
- **R-1:**
  - drop S-09b;
  - drop the secondary weighted analyses at the internal level (keep them at temporal validation);
  - limit explanation stability to 20 bootstrap refits instead of 50 (stated);
  - read full texts for Tier 1 and RQ5 only, and record the rest as limitations.
- **R-2:**
  - run the six baselines in group B only (Q2);
  - Q1 keeps groups A, B and C for the framework and BL-1;
  - drop S-10a and S-13 (stated as future work);
  - use 3 seeds instead of 5. This is a stated precision loss, not a validity loss.
- **R-3 (last resort):**
  - submit the literature review and the prediction study as separate manuscripts;
  - complete one, with the other declared ongoing.

  This changes timing, not rigour.

## Follow-up (EXEC-SCAFFOLD-5, same day)
**Scratchpad scripts** (not in the repository):
- `probe_q098_year.py`: the edge-case table;
- `assemble_v1.py`: 24 replacements, each asserted to match once; source `63d275d1…`, candidate `df3d35e7…`;
- `q100_illustration.py`: simulated scores only.

**Results:**
- Flow-diagram generator on the real repository: refused, exit 2 (no `screening/decisions.csv`).
- Data-protection check of the planned output paths:
  - ignored: `data/raw`, `data/derived`, `results/predictions`, `research/literature/raw_exports`;
  - tracked (intended, aggregate only): `results/runs`;
  - researcher Crossref exports must be placed in `raw_exports/`.
- Critical-path schedule and reduction tiers: decision sheet, final section.

## Follow-up (EXEC-SCAFFOLD-6, same day)
- Scratch copy `<scratchpad>/dry/repo`, deleted after use, with the drafted D-114 to D-122 rows ("SCRATCH DRY RUN — NOT APPROVED"):
  - `stage0.py` dry run → 7 rows;
  - `pilot_sample.py --frame-only` → 1,463 records;
  - `verify_run_authorisation` D-122 → accepted.
- **Q-098:** the first patch (null-as-absent) broke the committed fail-closed test. Revised to a constant-only patch with pinned no-rule tests: 379 OK.
- **Withdrawn downloader:** kept at `<scratchpad>/withdrawn/` (not in the repository).
- **NLM pages:** web-fetch failed (DNS).

## Follow-up (EXEC-SCAFFOLD-7, same day; the session worker restarted once mid-task)
- **Scratch scripts:**
  - `<scratchpad>/readiness_check.sh`: reproduces Stage 0, the frame and the authorisations on a disposable copy;
  - the download-loop URL check (echo + HEAD): 32/32 HTTP 200.
- **Git scope:** recounted at 58 paths.

## Follow-up (EXEC-SCAFFOLD-8, same day)
- **PubMed connector calls:**
  - `convert_article_ids` (6 DOIs);
  - `lookup_article_by_citation` (CR-05, CR-07; the response swapped its key and PMID fields, so identity was confirmed by metadata);
  - `get_article_metadata` (12 PMIDs);
  - `get_full_text_article` PMC12690183 (empty);
  - 5 searches (TRIPOD+AI, TreeSHAP, decision curves, the Hutchison published version, errata).
- **alphaXiv:** summaries of 1705.07874, 1603.02754, 2107.07511.
- None of these calls was registered; none changes the inventory.

## Follow-up (EXEC-SCAFFOLD-9, same day)
- **Full-text reads** via alphaXiv `answer_pdf_queries` (arXiv PDFs; PMC pages saved to tool-results and searched with grep): CR-01, CR-05, CR-06, CR-12b, CR-12c, CR-12d, CR-12e, CR-13.
- **CR-03:** PMC page states the full text is not archived (licence).
- **PubMed metadata:** CR-02, CR-04, CR-13, the Riley Part II erratum, 3 conformal records.
- **Exploratory searches (not registered):** 2.

## Follow-up (EXEC-SCAFFOLD-10, same day)
- **PubMed metadata:** 22 stability hits.
- **alphaXiv full-text queries:** PMC12524205, PMC13665122, arXiv 1806.08049, arXiv 1201.0490.
- **Failed fetches:** PMC12690183 (ADA), medRxiv, CR-02 DOI.
- **Platt and Holm titles:** not indexed in alphaXiv.
- **CDC variance tutorial:** fetched with curl into `<scratchpad>/web` (public page).
- **Synthetic ICI span check:** run inline.

## Follow-up (EXEC-SCAFFOLD-11, same day)
- **alphaXiv:** arXiv 2202.01602 full-text query.
- **Consensus searches** (metadata and abstracts): Efron 1979, Holm 1979, Platt (the first Holm/Platt attempt was rate-limited, then succeeded).
- **R15 edge-case scratch run (inline):** E1–E5.
- **No code changed.**

## EXEC-SCAFFOLD-12 (same day)
- **Fetched:** the CDC variance page; the R `lowess`/`loess` R/C/Rd sources from the `wch/r-source` mirror (svn.r-project.org blocked).
- **PubMed:** Hanley & McNeil (PMID 7063747), CR-02/CR-03 records.
- **Platt primary hosts:** unreachable.
- **Scratch (deleted):**
  - R15 tests fail on the current code; patched, 73 OK;
  - Q-052 ratio-formula match 1.3e-15; JKn 0.01%.
- **Output:** the corrections/evidence document and the unapplied patch.
- **No code changed.**

## EXEC-SCAFFOLD-13 (same day, 12:33 UTC)
- Wrote `research/reviews/2026-11-12_FOCUSED-DECISION-READINESS.md`.
- Compared the A5 §3 list with `git status`: 61 = 61; 2 extra paths.
- R15 before/after edge-case table: scratch copies, deleted.
- Patched scratch suite: 73 OK. One unrelated failure was a scratch artefact (missing `.gitignore`), re-run OK.
- No code, frozen, governance or decision file changed; no Git operation.

## EXEC-SCAFFOLD-14 (same day)
- Appended the pre-A5 reconciliation addendum to `research/reviews/2026-11-12_FOCUSED-DECISION-READINESS.md` (keeps the scope at 64 paths).
- Log-reference and "59" scans done.
- No code, decision sheet, frozen or governance change; no Git operation.

## EXEC-SCAFFOLD-15 (same day)
- Appended Addendum 2 (A5 authorisation package) to `research/reviews/2026-11-12_FOCUSED-DECISION-READINESS.md`.
- Content scan of the three review files.
- Read `pubrecords.check_ledger_matches_head`.
- No Git operation; no code or decision-sheet change.

## EXEC-SCAFFOLD-16 (A5 execution, researcher-approved)
- Verified tree == approved 64 paths (diff empty; 0 staged; HEAD = origin = `a0af2ad`).
- Applied C-1 to C-5 (each replacement asserted to match once).
- Ran checks, then performed the four A5 operations. Results are recorded in the follow-up commit.

## EXEC-SCAFFOLD-17 (A1 preparation; nothing recorded)
- Wrote `research/reviews/2026-11-12_A1-PREPARATION.md`. It records the researcher confirmations R-a, R-b and R-c.
- Verified: remote = `2246ca7`; IDs D-114 to D-122 unused; hashes; raw exports.
- Stage-0 dry run in a disposable copy with the drafted rows: in_scope 1470, E5 5, E7 2, new_rows 7. The real repository correctly refuses without D-121.
- No decision-log change, no repository Stage-0 run, no Git operation.

## EXEC-SCAFFOLD-18 (A1 recording and Stage 0, researcher-approved)
- Inserted D-114 to D-121 after D-113 (each edit asserted to match once; IDs confirmed unused) and 8 status-history rows. Q-063 answered with wording A.
- `verify_run_authorisation` accepted D-121.
- **STOPPED before the A1 commit.** `run_checks.sh`: literature 3 FAIL (389 of 392 pass). The failures are the pre-activation guard tests in `tests/literature/test_phase1_screening_tools.py`:
  - `test_real_decision_log_holds_no_run_authorisation` (line 638);
  - `test_real_decision_log_holds_no_complete_authorisation` (line 1091; it also asserts that no ledger exists);
  - `test_real_decision_log_has_no_cell_beginning_with_a_marker` (line 955).
- They assert that the real decision log contains no run authorisation, so recording D-121 necessarily fails them.
- No commit, push, Stage-0 dry run or write was performed. The recorded rows remain uncommitted, awaiting the researcher's decision.

## EXEC-SCAFFOLD-19 (researcher approved Option 1)
- Applied the activation-state test patch; the file equals the proposal version (`cmp`). Only the four approved tests were removed; 22 added.
- A1 commit `dea6042`.
- Stage-0 dry run exact match; write OK; dedicated commit `6079ced`.
- **D-099 (5): ledger SHA-256 after the run = `6842e24493145a504fa00bd45f34e5a4c79cf5ac36d441265cf067f448f3a650`**; `decisions.csv` SHA-256 `3550838b237c43bcb175e1d38b36acb8e048f7df6f66324ec63b3ed3afbaad7b`.
- Post-ledger checks: 2 literature failures (live-state tests in `test_flow_diagram.py` and `test_rq5_review.py`); push withheld; reported.

## EXEC-SCAFFOLD-20 (researcher approved the fixture-based fix)
- Tests-only correction in the two files (see CHANGELOG).
- A draft real-repository RQ5 test of mine contained a conditional that would have hidden the completeness-gate problem. It was removed, not committed, and the problem was recorded as Q-101.
- All suites pass (411/10/39/71; query table PASS).
