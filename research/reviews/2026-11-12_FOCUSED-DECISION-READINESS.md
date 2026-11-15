# Focused decision-readiness review (2026-11-12, 12:33 UTC; deadline 2026-11-27 unchanged)

> **Status**
> - Nothing is approved. **No decision is made** on your behalf.
> - **The R15 patch is not applied.** It was exercised only in throwaway scratch copies, which have been deleted.
> - No code, frozen file, governance file or decision record was changed.
> - No Git operation was performed.
>
> **State checked:** `claude/eloquent-mccarthy-bqtxr3-part1`, HEAD `a0af2ad` = origin; 63 uncommitted paths; 0 staged.
>
> **Sources:**
> - `2026-11-12_DECISION-SHEET_A1-A6.md` (§0, §2, §3, §6, §7);
> - `2026-11-12_CONSOLIDATED-APPROVAL-REQUEST.md` (A1, A2, evidence status);
> - `2026-11-12_CORRECTIONS-AND-DECISION-EVIDENCE.md`;
> - `logs/DECISION_LOG.md` (statuses read only).

## 1. A1 — what remains
| Item | Exactly what is needed from you |
|---|---|
| **Q-063 wording** | Choose one of the following. **(a) Alternative wording** (recommended in the consolidated request), replacing only the Q-063 clause: *"Q-063: answered — preservation status 'off-device backup designated; integrity and privacy researcher-reported; not independently verified' (not PRESERVED). Archive integrity is verified in the container; the WhatsApp approval date, wording and approver are not available; conditions are not recorded. I accept this as sufficient to record the fixed-inventory entry, with the limitation stated."* **(b) PRESERVED**, only with your dated written confirmation now that the Google Drive copies exist and are private |
| **WhatsApp details** | The approval date, the wording and the approver are **[U]** ("not provided"). Before using "not available" you must confirm that you genuinely cannot supply them. If you can, supply them instead |
| **Condition rows 1, 2, 4** | These rest on decisions whose status is **APPROVED — CONDITIONAL (inactive for screening)**: D-036 (Q-039, row 1), D-055 with flag D-061 (Q-040, row 2), and D-060 as amended by D-068 (R5, row 4). Recording rows 1, 2 and 4 as met needs your explicit acceptance of the reading "met at decision level", which D-111 and protocol §10 already use. Rows 3, 5 and 6 rest on D-111, D-110 and checked repository facts |
| **Other confirmations** | The Drive copies still exist and are private **[R]**; the D-114 hashes (re-observed on 11-12, 244/244 raw exports match **[V]**) |

**Consequences of accepting the alternative wording:**
1. Q-063 is closed permanently, with the limitation as stated. The word PRESERVED is never used, and the backup's integrity and privacy remain researcher-reported, which the manuscript must disclose.
2. The rest of A1 is unaffected: D-114 to D-121 can be recorded as drafted. The dry run accepted the corrected D-121 text **[V]**.
3. The fixed inventory is bound to `b668dbde…d054`. Any later change needs a new entry (D-108).
4. All six activation conditions are recorded as met, so screening becomes activatable, and one single-use Stage-0 run is authorised. Expected dry-run output: in_scope 1470, E5 5, E7 2, new_rows 7.
5. The ledger must be committed before any further run (D-099), so **A1 is not executable without A5**.

**A1 is not approved.**

## 2. A5 — Git scope reconciliation
**Verification:** the A5 §3 paths were extracted from the decision sheet and compared with `git status --porcelain -uall`. **The 61 listed paths match exactly**; the only differences are the two new files below.

**1. Original 61 paths** (as in decision sheet §3):
- **Modified (6):**
  - `logs/CHANGELOG.md`
  - `logs/PROMPT_LOG.md`
  - `research/reviews/daily_review_log.md`
  - `research/reviews/unresolved_questions.md`
  - `research/setup/environment_assessment.md`
  - `scripts/run_checks.sh`
- **New (55):**
  - **Environment:**
    - `environment/README.md`
    - `environment/install_and_verify.sh`
    - `environment/requirements-proposed.txt`
  - **Session log:**
    - `logs/session_logs/2026-11-12_EXEC-SCAFFOLD.md`
  - **Manuscript:**
    - `manuscript/01_introduction.md`
    - `manuscript/02_methods_literature_review.md`
    - `manuscript/03_methods_experimental.md`
    - `manuscript/04_limitations_prespecified.md`
    - `manuscript/05_reproducibility_and_availability.md`
    - `manuscript/A_appendix_analysis_plan.md`
    - `manuscript/templates/tables_and_figures.md`
  - **Protocol candidates:**
    - `research/methodology/experimental_protocol_v1.0_candidate_full.md`
    - `research/methodology/experimental_protocol_v1.0_freeze_candidate.md`
  - **Reviews:**
    - `research/reviews/2026-11-12_AB-7_reference_preverification.md`
    - `research/reviews/2026-11-12_CONSOLIDATED-APPROVAL-REQUEST.md`
    - `research/reviews/2026-11-12_DECISION-SHEET_A1-A6.md`
    - `research/reviews/2026-11-12_EVIDENCE-AND-DECISION-READINESS_REVIEW.md`
    - `research/reviews/2026-11-12_PRIOR-ART_AND_METHODS_EVIDENCE.md`
    - `research/reviews/2026-11-12_Q-098_Q-099_Q-100_Q-054_analysis.md`
    - `research/reviews/2026-11-12_Q-098_proposed.patch`
  - **Literature scripts:**
    - `scripts/literature/crossref_export_check.py`
    - `scripts/literature/expansion.py`
    - `scripts/literature/flow_diagram.py`
    - `scripts/literature/register_crossref_exports.py`
    - `scripts/literature/rq5_review.py`
  - **Experiment code:**
    - `scripts/models/README.md`
    - `scripts/models/calibration.py`
    - `scripts/models/compare.py`
    - `scripts/models/conformal.py`
    - `scripts/models/experiment_config_draft.json`
    - `scripts/models/explain.py`
    - `scripts/models/glm.py`
    - `scripts/models/harness.py`
    - `scripts/models/metrics.py`
    - `scripts/models/models.py`
    - `scripts/models/preprocess.py`
    - `scripts/models/report.py`
    - `scripts/models/reproducibility.py`
    - `scripts/models/splits.py`
    - `scripts/models/stats.py`
    - `scripts/models/survey.py`
    - `scripts/models/synthetic.py`
    - `scripts/models/tuning.py`
  - **Dataset build:**
    - `scripts/nhanes/build_dataset.py`
  - **Literature tests:**
    - `tests/literature/test_crossref_export_check.py`
    - `tests/literature/test_expansion.py`
    - `tests/literature/test_flow_diagram.py`
    - `tests/literature/test_register_crossref_exports.py`
    - `tests/literature/test_rq5_review.py`
  - **Model tests:**
    - `tests/models/test_explain_survey_compare.py`
    - `tests/models/test_metrics_calibration_conformal.py`
    - `tests/models/test_pipeline_scaffolding.py`
    - `tests/models/test_report_and_cli.py`
  - **Other tests:**
    - `tests/nhanes/test_build_dataset.py`
    - `tests/synthetic_harness/test_rule_s_harness.py`

**2. The two additional paths** (not in A5):
- `research/reviews/2026-11-12_CORRECTIONS-AND-DECISION-EVIDENCE.md`
- `research/reviews/2026-11-12_R15_proposed.patch`

This review file is a third new path, also outside A5. The current count is therefore **64**.

**3. Contents:**
- **The CORRECTIONS file:** a review document containing:
  - the R15 analysis;
  - the Q-052 report;
  - the Option C design;
  - the CR-02/CR-03 access routes, including a draft request to the corresponding author (name only; the email address is not included);
  - the R14 packet;
  - the reference table;
  - the stability note;
  - Q-061;
  - the critical path;
  - the decision sheet.
- **The patch file:** a unified diff, SHA-256 prefix `3db1a415`. It covers `scripts/models/survey.py` (one validation block) and `tests/models/test_explain_survey_compare.py` (two tests). It is **not applied**.

**4. Material to keep out of the commit:**
- Neither file contains raw data, raw exports, abstract text, credentials or personal contact details. The CDC passage is a one-sentence quotation.
- **Two cautions:**
  - **(i)** If the patch file is committed, it is only a proposal. Committing it **does not** apply R15.
  - **(ii)** The log files in the 61-path list now contain EXEC-SCAFFOLD-12 entries (and will contain this review's entries) that **refer to the new files**. If A5 is executed on exactly 61 paths, the committed logs will reference uncommitted files.
- **Your choice:**
  - (a) extend A5 to 64 paths;
  - (b) commit 61 and accept the dangling references until a later commit.

**Inconsistency found:** decision sheet §7 (approval register) still says "A5: Git (59 paths, 4 operations)". §0 and §3 say 61, and 61 is what the working tree shows. The 59 is a stale value. It is noted here; the sheet was not edited.

**5. The four operations previously proposed** (decision sheet §3):
1. `git add -- <the 61 paths>` (explicit paths, never `-A`), then check `git diff --cached --name-only | wc -l` = 61.
2. `git commit` on `claude/eloquent-mccarthy-bqtxr3-part1`, with the attribution lines.
3. `git push -u origin claude/eloquent-mccarthy-bqtxr3-part1` (no force).
4. A follow-up commit recording the hash of commit 2 in `logs/CHANGELOG.md` and `logs/PROMPT_LOG.md`, pushed the same way.

**Not covered:** PR #17, merges, force-push, branch protection, data.

## 3. R15 patch — technical review (patch inspected; not applied)
**Exact change** in `weighted_mean_taylor`. The single combined check
`if (w < 0).any() or np.isnan(x[d]).any() or w[d].sum() <= 0: raise ValueError(...)`
is replaced by:
```python
if not np.isfinite(w).all():  raise ValueError("survey weights must be finite ...")
if (w < 0).any():              raise ValueError("survey weights must be non-negative")
keep = w > 0
x, w, strata, psu, d = x[keep], w[keep], strata[keep], psu[keep], d[keep]
if np.isnan(x[d]).any() or w[d].sum() <= 0:
    raise ValueError("x must be complete in the domain and the domain must have a positive weight sum")
```
The variance loop, the estimate formula and the function signature are unchanged. Two tests are added.

**Before vs after** (scratch run of both versions on the same inputs, 2026-11-12):

| Input | Before | After |
|---|---|---|
| NaN weight in the domain | estimate NaN, SE NaN (silent) | `ValueError` "finite" |
| NaN weight outside the domain | Silently ignored (est 2, SE 0.667) | `ValueError` "finite" |
| +inf weight | NaN, NaN (silent) | `ValueError` "finite" |
| −inf weight | `ValueError` (generic message) | `ValueError` "finite" |
| Negative finite weight | `ValueError` (generic) | `ValueError` "non-negative" |
| A zero-weight record in a PSU that still has positive weights | est 3, SE 0.667 | Identical |
| A PSU made up only of zero-weight records | SE 0.866 (phantom PSU counted) | SE 1.000 (= the design without those records) |
| A stratum left with one positive-weight PSU | Returns SE 0.943 (mis-specified) | `ValueError` "single PSU" |
| All-zero weights | `ValueError` | `ValueError` (new message) |
| Empty arrays | `ValueError` | `ValueError` (unchanged) |
| One observation | `ValueError` "single PSU" | Unchanged |
| One observation per PSU, two PSUs | est 2, SE 1 | Unchanged |
| Domain all False; domain members all zero-weight | `ValueError` | `ValueError` |
| NaN x in the domain, positive weight | `ValueError` | `ValueError` |
| **NaN x in the domain, zero weight** | `ValueError` | **Accepted** (the record leaves the design first) |
| Designs with all weights > 0 (15 strata × 2 PSUs, n = 600, full and domain) | — | Max \|before − after\| in estimate and SE = **0.0** |

**Comparison with the CDC/NCHS guidance [V, tutorial text collected earlier]:**
- "all observations with a non-zero value for your weight variable, as well as an indicator" for the subpopulation is what the patch implements: zero weights are dropped and the domain indicator is kept.
- No domain filtering is introduced.
- The with-replacement Taylor variance is unchanged.
- The guidance says nothing about NaN weights. Rejecting them is a **design choice** (fail closed), not a CDC requirement.

**Test evidence** (scratch copy of `scripts/` and `tests/` plus `.gitignore`; deleted):
- With only the test hunk applied (current code), the 2 new tests **fail**.
- With the full patch, `tests/models` gives **73 OK**.
- A first scratch run without `.gitignore` showed an unrelated failure in `test_git_ignore_check`, an environment artefact. It passed once `.gitignore` was copied.
- The repository's own suites still pass on the unpatched code: the 71 model tests are unchanged.

**Backward compatibility:**
- The only callers of `weighted_mean_taylor` are the tests (grep of `scripts/` and `tests/`).
- No pipeline code calls it yet.
- The other functions in `survey.py` (`standardised_mean_difference`, `shift_diagnostics`) are untouched.
- Results change only for inputs with non-finite weights or zero-weight-only PSUs.
- Error *messages* change for invalid inputs; only the tests match on them.
- **Unrelated functionality is not altered.**

**Remaining edge cases** (not addressed by the patch; listed, not fixed):
1. **inf x in the domain** returns est = inf, SE = NaN silently, before and after (`np.isnan` does not catch inf).
2. **NaN or None in `strata`/`psu`** is not validated.
3. **A non-boolean `domain`** containing NaN is cast to True.
4. **Zero-weight records with NaN x in the domain** are now accepted. This is consistent with the CDC rule, but it is a behaviour change you should be aware of.
5. **No degrees of freedom are returned** (Q-052 recommendation; separate change).
6. **Single-PSU strata** have no collapsing rule. This is by design; a collapsing rule would be a protocol decision.

**Independent validation:** this is algebraic agreement with the textbook ratio-estimator linearisation (1.3×10⁻¹⁵) and approximate agreement with the delete-one-PSU jackknife (JKn) (0.01%), on synthetic data only. **There is no comparison with R `survey`, SAS, Stata or SUDAAN** (Q-052 open).

## 4. A2 — custodian: information required (none assumed)
| Item | Required from you |
|---|---|
| Identity | Full name and role of an actual person; not you, and not a second account or session under your control |
| Independence (C1, C6) | A written statement of no stake in the pilot outcome and no discussion of pilot decisions with you before disclosure |
| Separate environment (C2, C3) | Their own account and computer, to which you have no access; able to run an assistant session and Python 3 at a recorded commit |
| Responsibilities | Written confirmation of C1–C6: run the assistant's pilot screening on the private sheet; send commitment C before your screening; send F and S after it |
| Handling and deletion (C4) | A private channel for the sheet; never published or committed; deleted after disclosure, with confirmation of deletion |
| Dates (C5) | Start (target 11-14, latest 11-15 for C) and completion (F and S by 11-16) |
| S1 / S2 | Your choice and its basis. The NLM, PubMed and publisher terms **could not be read** from this environment. **Neither S1 (private copy of the abstracts) nor S2 (custodian reads PubMed directly) is shown to comply**. S2 additionally risks version drift between PubMed and the inventory text |
| Also part of A2 | The R1-min revision of D-102; the D-096 extension; `pilot_commitment.py` authorisation; D-122 (after Stage 0) |

## 5. Option C and D-016 readiness (summary; nothing added)
- **Comparison:** group B (27 = 21 analytes + 6 non-laboratory predictors: age, sex, BMI, waist, SBP, DBP) against group C (the 6). The primary contrast is B − C; A − C is secondary. Framework (F2 + F3) and BL-1.
- **Participants:** the existing eligibility cascade E0–E8 (adults without diagnosed diabetes; FA-1 age ≥ 20 pending); N 3,088 development and 2,485 validation. Identical participants across groups (in-fold imputation); S-10a complete-case sensitivity.
- **Splits and seeds:** identical D-train/D-cal splits, folds and 5 seeds; temporal validation 2017–March 2020 → August 2021–August 2023, applied once to frozen models. Reported as temporal, not external.
- **Evaluation:** paired bootstrap (2,000) of ΔAUROC, Δlog loss, ΔBrier and ΔICI/slope/intercept on calibrated probabilities, internal and temporal. Decision curves only if M10 is retained (Q-054). Group C's own performance is always reported. The harmonisation asymmetry (only A and B carry inter-period assay changes) is reported as a limitation.
- **Result categories:** all four are preserved and all are reported:
  - positive (CI > 0, and above the threshold if one is set);
  - negligible (claimable only if a threshold is set; otherwise "no demonstrated increment");
  - negative (CI < 0);
  - uncertain (a wide CI).
- **Threshold:** not chosen; options (i)–(iv) are in §6.
- **Why CR-02 and CR-03 full texts are needed before D-016:**
  - Both are abstract-level only. Both develop prediabetes/diabetes models from easily obtained (non-laboratory) NHANES-type predictors.
  - Option C's contribution is the increment of biochemistry over exactly such predictors. Whether CR-02/CR-03 already measured that increment, with what predictors, validation design (temporal or not) and calibration reporting, **cannot be established from abstracts**. "Not stated in the abstract" ≠ "not done".
  - Rule 14 (finding no matching paper is not evidence of novelty) and Rule 5 (RQ5) require the closest prior work to be read before a contribution is claimed.
  - CR-02's predictor set also determines whether group C is a fair "non-laboratory comparator". Group C may not be changed without your approval.

## 6. D-019 decision table (no option selected)
| Item | Choices | Methodological consequence | Evidence gap |
|---|---|---|---|
| **R14 smoother** | (a) local-linear, span 0.75 (current); (b) R `lowess` defaults (f = 2/3; the paper used iter = 0); (c) R `loess` (span 0.75, degree 2) | (a) no code change; (b) one constant, closest to Austin & Steyerberg's `lowess(iter = 0)`; (c) closest to their primary `loess`, but needs new code and exact `surface = "interpolate"` is hard to reproduce. Absolute ICI is smoother-specific under every option | R defaults read from the GitHub mirror (the official svn is blocked); the R version used in the paper is unknown; ΔICI robustness checked only in one synthetic setting. Proposed sensitivity spec: S0–S3 |
| **Option C threshold** | (i) none (CIs only); (ii) from verified literature; (iii) net-benefit based; (iv) researcher-set before any result | (i) no "negligible" or "meaningful" verdict possible; (ii) defensible only if sourced; (iii) needs M10 and Q-054; (iv) must be recorded before any result and reported as a judgement | No verified source for a ΔAUROC threshold; no justified net-benefit range |
| **df reporting** | (a) report design df = #PSUs − #strata and use t-quantiles; (b) normal quantiles, state df; (c) not reported | (a) follows the CDC tutorial [V]; requires a small code change (not in R15) | None for the rule; the implementation is pending |
| **Q-061** | Route 1: supply the ADA 2026 Section 2 PDF; Route 2: numerical rule, no guideline-correspondence claim | Route 1 allows "consistent with ADA criteria"; Route 2 adds a limitation. **Thresholds are identical under both** | The primary ADA text is unavailable (4 failed attempts); secondary sources only |
| **Q-052 limitation** | (a) obtain a reference implementation after A3 (e.g. an approved package or an R environment); (b) accept algebraic + JKn agreement and state the limitation | (b) weakens the claim of validated design-based SEs to "internally cross-checked" | No R `survey` / SAS / Stata comparison possible today |

## 7. Critical-path check (12:33 UTC, 11-12; no approval received)
| Date | Milestone | Status | Depends on your decisions |
|---|---|---|---|
| 11-13 | Part 1 approvals (A1, A5, A2 with named custodian) + Stage 0 | **Feasible, zero slack** | A1, A5, A2 |
| 11-16 | Pilot complete (draw 11-14/15, C, both screenings, disclosure) | Feasible only if 11-13 holds and the custodian is available 11-14 to 11-16 | A2, custodian, your screening |
| 11-20 | Title/abstract screening latest (target 11-19); ADA PDF latest | Feasible only if the pilot passes on 11-16 | Your audit and missing-abstract review; Q-061 |
| 11-22 | Stage C/D gates, D-016, D-019 freeze | Feasible only on the above; also needs CR-02/CR-03 full texts, AB-7, A3/A4 | D-016, D-017, D-018, D-019 items (§6) |
| 11-25 | Experiments complete | Feasible only if the freeze is on 11-22 and the download/build (Part 2) is done by 11-21 | Part 2, DOWNLOAD, A3 |
| 11-27 | Manuscript | **Feasible only if every date above holds** | All |

- **R-1:** **not triggered** (its condition is title/abstract screening not finishing by 11-19). It is **approaching**: a one-day delay at 11-13 meets it.
- **R-2** (freeze past 11-22) and **R-3** (gates past 11-24 or a failed pilot) are **not met**.
- **No contingency condition has been met.** None is activated, and the deadline is not extended.

## Final summary
**1. Decisions required** (yours): A1 (Q-063 wording; WhatsApp confirmation; rows 1, 2, 4); A5 (61 vs 64 paths); A2 (custodian, S1/S2 basis); R15 (apply or defer); Q-061 route; CR-02/CR-03 access; then A3, A4, A6, Q-098, Q-099, Q-054, Q-100, Part 2, D-016, D-019 (§6).

**2. Evidence available:**
- **[V]:**
  - archive integrity; 244/244 raw exports;
  - the corrected D-121 dry run;
  - the CDC variance guidance;
  - the R `lowess`/`loess` source (mirror);
  - Krishna et al.;
  - R15 before/after behaviour and 73 OK in scratch;
  - Q-052 algebraic + JKn agreement;
  - A5 61-path reconciliation.
- **[AB]:** CR-02, CR-03, Hanley & McNeil, Holm, Efron, Platt.

**3. Evidence gaps:**
- the WhatsApp approval details;
- whether the Drive copies are private;
- a custodian;
- the PubMed/publisher terms;
- the ADA primary text;
- the CR-02/CR-03 full texts;
- a Q-052 reference implementation;
- the Platt year/venue;
- sources for Wilson, isotonic and the baseline learners;
- a refit/period stability methods source;
- an Option C threshold source.

**4. Technical risks:**
- R15 unapplied (silent NaN or a mis-specified SE if left);
- inf-x and strata/PSU NaN not validated;
- no df returned;
- absolute ICI depends on the smoother;
- harmonisation asymmetry in Option C;
- A5 at 61 leaves dangling log references;
- §7 "59" stale.

**5. Deadline implications:** all milestones are still feasible, but only with Part 1 decided on 11-13. Any slip moves everything day for day and meets R-1 (your decision, never automatic).

**6. Recommended order** [RECOMMENDATION, not a decision]:
1. A1 + A5 (including 61 vs 64) + A2 with a named custodian, by 11-13.
2. R15 apply/defer, and A3/A4 (parallel lanes).
3. Q-061 PDF and the CR-02/CR-03 full texts, by 11-20.
4. A6, Q-098, Q-099, Q-054, Q-100 and Part 2 (data step), 11-13 to 11-14.
5. D-016 after RQ5 and CR-02/CR-03.
6. The D-019 items (§6) by 11-22.

---

# Addendum — final pre-A5 reconciliation (2026-11-12, about 12:45 UTC; no Git operation authorised)
> **Why an addendum:** it is appended to this file, which is already in scope, so that **no 65th path is created**.
>
> **Not done:**
> - nothing staged, committed or pushed;
> - R15 not applied;
> - the decision sheet was not edited;
> - no frozen or governance file was changed.

## A. A5 — exact 64-path scope (`git status --porcelain -uall`, 2026-11-12)
**Composition:**
- the 61 original paths (decision sheet §3; identical to the working tree);
- **plus three additional review files**, marked ★ below:
  - #18 `2026-11-12_CORRECTIONS-AND-DECISION-EVIDENCE.md`;
  - #21 this file;
  - #25 `2026-11-12_R15_proposed.patch`.

**Status:** 6 modified, 58 new.

1. `environment/README.md`
2. `environment/install_and_verify.sh`
3. `environment/requirements-proposed.txt`
4. `logs/CHANGELOG.md`
5. `logs/PROMPT_LOG.md`
6. `logs/session_logs/2026-11-12_EXEC-SCAFFOLD.md`
7. `manuscript/01_introduction.md`
8. `manuscript/02_methods_literature_review.md`
9. `manuscript/03_methods_experimental.md`
10. `manuscript/04_limitations_prespecified.md`
11. `manuscript/05_reproducibility_and_availability.md`
12. `manuscript/A_appendix_analysis_plan.md`
13. `manuscript/templates/tables_and_figures.md`
14. `research/methodology/experimental_protocol_v1.0_candidate_full.md`
15. `research/methodology/experimental_protocol_v1.0_freeze_candidate.md`
16. `research/reviews/2026-11-12_AB-7_reference_preverification.md`
17. `research/reviews/2026-11-12_CONSOLIDATED-APPROVAL-REQUEST.md`
18. `research/reviews/2026-11-12_CORRECTIONS-AND-DECISION-EVIDENCE.md` ★
19. `research/reviews/2026-11-12_DECISION-SHEET_A1-A6.md`
20. `research/reviews/2026-11-12_EVIDENCE-AND-DECISION-READINESS_REVIEW.md`
21. `research/reviews/2026-11-12_FOCUSED-DECISION-READINESS.md` ★
22. `research/reviews/2026-11-12_PRIOR-ART_AND_METHODS_EVIDENCE.md`
23. `research/reviews/2026-11-12_Q-098_Q-099_Q-100_Q-054_analysis.md`
24. `research/reviews/2026-11-12_Q-098_proposed.patch`
25. `research/reviews/2026-11-12_R15_proposed.patch` ★
26. `research/reviews/daily_review_log.md`
27. `research/reviews/unresolved_questions.md`
28. `research/setup/environment_assessment.md`
29. `scripts/literature/crossref_export_check.py`
30. `scripts/literature/expansion.py`
31. `scripts/literature/flow_diagram.py`
32. `scripts/literature/register_crossref_exports.py`
33. `scripts/literature/rq5_review.py`
34. `scripts/models/README.md`
35. `scripts/models/calibration.py`
36. `scripts/models/compare.py`
37. `scripts/models/conformal.py`
38. `scripts/models/experiment_config_draft.json`
39. `scripts/models/explain.py`
40. `scripts/models/glm.py`
41. `scripts/models/harness.py`
42. `scripts/models/metrics.py`
43. `scripts/models/models.py`
44. `scripts/models/preprocess.py`
45. `scripts/models/report.py`
46. `scripts/models/reproducibility.py`
47. `scripts/models/splits.py`
48. `scripts/models/stats.py`
49. `scripts/models/survey.py`
50. `scripts/models/synthetic.py`
51. `scripts/models/tuning.py`
52. `scripts/nhanes/build_dataset.py`
53. `scripts/run_checks.sh`
54. `tests/literature/test_crossref_export_check.py`
55. `tests/literature/test_expansion.py`
56. `tests/literature/test_flow_diagram.py`
57. `tests/literature/test_register_crossref_exports.py`
58. `tests/literature/test_rq5_review.py`
59. `tests/models/test_explain_survey_compare.py`
60. `tests/models/test_metrics_calibration_conformal.py`
61. `tests/models/test_pipeline_scaffolding.py`
62. `tests/models/test_report_and_cli.py`
63. `tests/nhanes/test_build_dataset.py`
64. `tests/synthetic_harness/test_rule_s_harness.py`

**Log-reference check:**
- **Method:** every backticked file name in the added lines of the 5 modified logs and in the whole new session log (82 distinct names) was classified as:
  - in the 64-path scope;
  - already tracked at `a0af2ad`;
  - a short name of a scoped or tracked file;
  - outside.
- **Result:** all references resolve to scoped or tracked files, **except the 10 below**. These are deliberate mentions, not missing files.

| Reference | Why it is outside the scope | Action needed |
|---|---|---|
| `publications.jsonl`, `source_records.jsonl` | Git-ignored records (D-096/D-010); mentioned only by hash | None (must never be committed) |
| `data/raw/nhanes/MANIFEST_local.csv` | Proposed git-ignored data path; no file exists | None |
| `screening/decisions.csv` | Mentioned as **absent** (flow-diagram refusal); created only by Stage 0 | None |
| `scripts/nhanes/download.py` | Recorded as **withdrawn** (it violated the offline safeguard) | None |
| `assemble_v1.py`, `probe_q098_year.py`, `q100_illustration.py`, `readiness_check.sh` | Scratch scripts outside the repository, described as such | None (outside the repository by design) |
| `www.cdc.gov/nchs/nhanes/index.html` | A URL, not a file | None |

**Conclusion:**
- **With the 64-path scope, no log entry refers to an uncommitted repository file.**
- With the 61-path scope, the EXEC-SCAFFOLD-12 and -13 entries in `logs/CHANGELOG.md`, `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md` and the session log would refer to the three ★ files without including them.

## B. Stale "59 paths" figure
| Location | Text | Nature | Proposed correction (not applied) |
|---|---|---|---|
| `2026-11-12_DECISION-SHEET_A1-A6.md` line 252 (§7 approval register, A5 row) | "Git (59 paths, 4 operations)" | **Live and stale** (§0 and §3 say 61) | Change to **"Git (61 paths per §3, or 64 with the three 11-12 review files; 4 operations)"** — one cell |
| `logs/CHANGELOG.md` lines 3128, 3131, 3156 | "A5 scope now 59 paths", "= 59", "59 paths (6 modified, 53 new)" | Historical entries (EXEC-SCAFFOLD-8/9), correct when written; superseded by line 3222 (60) and line 3274 (61) | **None:** logs are append-only |
| `research/reviews/daily_review_log.md` line 1000 | "A5 reconciled at 59 paths" | Historical | **None** |
| This file, §2 and the final summary | Reports the inconsistency | Current | None |

**Consequential edits** (only if you approve 64 and the correction):
- **(i)** §3, operation 1: "must print 61" → "must print 64", and add the three ★ paths to the §3 list.
- **(ii)** §0 template A5: "on exactly the 61 listed paths" → "… 64 …".

The alternative to (ii) is to leave the sheet unchanged and state 64 in your approval text. **No edit is made until you authorise it.**

**Effect on scope:** editing the decision sheet does not change the path count; it is already in scope.

## C. R15 — final patch review (patch file unchanged, SHA-256 `3db1a415…`; `git apply --check` passes; not applied)
**Exact changed lines in `scripts/models/survey.py`:**
- Removed: current lines 32–33, `if (w < 0).any() or np.isnan(x[d]).any() or w[d].sum() <= 0:` and its `raise`.
- Added (14 lines, 4 of them comments):
  - `np.isfinite(w).all()` check → "must be finite";
  - `(w < 0).any()` check → "non-negative";
  - `keep = w > 0`, subsetting `x, w, strata, psu, d`;
  - then `np.isnan(x[d]).any() or w[d].sum() <= 0`.
- Variance code, estimator and signature: untouched.

**Tests:** +28 lines in `tests/models/test_explain_survey_compare.py` (2 tests). No existing test is changed.

| Question | Finding |
|---|---|
| **D1 addressed?** | Yes. NaN, +inf and −inf weights are rejected in and outside the domain (scratch evidence in §3). The new test covers NaN and +inf in and outside the domain; **−inf is not in the test** (it raises before and after, now with the "finite" message) |
| **D2 addressed?** | Yes. Zero-weight records leave the design before PSU counting. Tested: a zero-weight-only PSU leaves the estimate and SE unchanged; a stratum reduced to one positive-weight PSU raises "single PSU" |
| **Positive-weight behaviour preserved?** | Yes. When every weight is > 0, `keep` is all True and the code path is the original. Scratch comparison (15 strata × 2 PSUs, n = 600, full and domain): max \|difference\| = **0.0**. The existing survey tests (estimate, SE, domain using all PSUs, single-PSU error) pass unchanged |
| **Do the 73 tests cover the regressions?** | They cover D1 (NaN, +inf) and D2 (phantom PSU; single-PSU). **Not covered:** −inf (behaviour unchanged); all-zero weights (raises before and after); **NaN x with zero weight in the domain, newly accepted** (no test asserts this new behaviour). Optional additional tests are possible; not added |
| **Unrelated functionality** | Not altered. The only callers are the tests; `standardised_mean_difference` and `shift_diagnostics` are untouched |

**Remaining limitations** (unchanged by the patch):
1. **x values:**
   - `inf` in the domain gives estimate = inf and SE = NaN silently (`np.isnan` misses inf);
   - x outside the domain is unvalidated, which is intended.
2. **PSU/strata identifiers:**
   - NaN or None codes are not validated;
   - NaN strata form separate unique groups (each NaN is unequal to itself), which can produce spurious single-PSU errors or wrong grouping;
   - PSU codes are grouped within strata only, which is correct for NHANES (PSU codes repeat across strata);
   - there is no collapsing rule.
3. **Degrees of freedom:** not returned. CDC: df = #PSUs − #strata. A separate change is needed for t-based CIs.
4. **Validation:** algebraic agreement (1.3×10⁻¹⁵) and JKn agreement (0.01%) on synthetic data only; **no reference-software comparison** (Q-052 open).

## D. A1 and A2 — exactly what is needed (nothing assumed)
**A1 — your confirmations, in writing:**
1. **Q-063 wording:** the alternative wording (as in §1), **or** PRESERVED together with a dated confirmation that the Drive copies exist and are private.
2. **WhatsApp details:** that you **cannot** supply the approval date, wording and approver. If you can, supply them instead.
3. **Condition rows 1, 2, 4:** that "met at decision level" is accepted for:
   - row 1 — D-036;
   - row 2 — D-055 and D-061;
   - row 4 — D-060 as amended by D-068.

   All are APPROVED — CONDITIONAL (inactive for screening).
4. **Approval of D-114 to D-121** as drafted (Appendix A, corrected D-121), one Stage-0 run, and the related commit and push.

**Evidence already in place [V]:**
- archive hashes `69e690f0…` and `7b7d4674…`;
- 244/244 raw exports matching the manifest;
- inventory `b668dbde…d054`;
- D-121 dry run accepted.

**[R] only:** the Drive copies exist, are private and are intact.

**A2 — four separate items:**

| Item | Status | What is needed |
|---|---|---|
| **Appointment** | **None** | Name and role of an actual person other than you (not a second account or session of yours) |
| **C1–C6 written confirmation** | **None** | The custodian's own written confirmation of: C1 no stake; C2 own account and environment; C3 can run a session and Python at a recorded commit; C4 private channel, never published, deleted after disclosure; C5 C before your screening, F and S after (by 11-16); C6 no discussion before disclosure. Plus start and completion dates |
| **S1/S2 choice** | **None** | S1 (a private copy of the sheet with abstracts) or S2 (the custodian reads PubMed directly), with your stated basis |
| **Source-term uncertainty** | **Unresolved** | The NLM, PubMed and publisher terms could not be read from this environment. Neither S1 nor S2 is shown to comply. S2 adds version-drift risk. Only you can judge or obtain the terms |

## E. Final approval sheet (no option selected)
| Item | Decision required | Choices |
|---|---|---|
| **A1** | Items D.1–D.4 | Alternative wording / PRESERVED with confirmation |
| **A5** | Scope and the four operations: (1) `git add --` the explicit paths, never `-A`, then check `git diff --cached --name-only \| wc -l` = 61 or 64; (2) commit on `claude/eloquent-mccarthy-bqtxr3-part1` with the attribution lines; (3) `git push -u origin claude/eloquent-mccarthy-bqtxr3-part1`, no force; (4) a follow-up commit recording the hash in CHANGELOG and PROMPT_LOG, pushed the same way. Not covered: PR #17, merge, force-push, branch protection, data | **64 paths** (§A; no dangling references) / 61 paths (three dangling log references) / a subset. Optionally: authorise the §B one-cell correction (plus (i) and (ii) if 64) |
| **R15** | Apply or defer | Apply `2026-11-12_R15_proposed.patch` with its 2 tests (optionally request the extra tests in C) / defer (no design-based estimate until decided) |
| **A2** | Appointment, C1–C6, S1/S2 and your basis, plus R1-min, the D-096 extension, `pilot_commitment.py`, D-122 | — |
| **Q-061** | Route | Route 1: supply the ADA 2026 Section 2 PDF (latest 11-20) / Route 2: numerical rule, no guideline claim |
| **CR-02 / CR-03** | Obtain the full texts | **Both are still abstract-only.** CR-02: library / ILL / author request (draft in CORRECTIONS §5). CR-03: the medRxiv PDF via doi:10.1101/2025.02.10.25321897 in your browser |
| **D-016** | Contribution | After the RQ5 review and the CR-02/CR-03 full texts (latest 11-22) |
| **D-019** | R14 smoother; Option C threshold (i)–(iv); df reporting; Q-061 route; Q-052 limitation; plus Q-054, Q-100 and the F5 metric | By 11-22 (see §6) |

**Deadline:**
- the 11-13 decision on A1, A5 and A2 has zero slack;
- no contingency condition is met; R-1 is approaching, not triggered;
- the deadline of 2026-11-27 is unchanged.

**Awaiting your explicit approval. No Git operation will be performed before then.**

---

# Addendum 2 — A5 authorisation package (2026-11-12; **A5 NOT approved**; nothing executed)
> **Why an addendum:** it is appended here so the scope stays at 64 paths.
>
> **Not done:**
> - no staging, commit or push;
> - no R15 application;
> - no code, frozen, governance or decision-sheet change;
> - PR #17 untouched.

## 1. The exact 64 paths
**Modified (6):**
1. `logs/CHANGELOG.md`
2. `logs/PROMPT_LOG.md`
3. `research/reviews/daily_review_log.md`
4. `research/reviews/unresolved_questions.md`
5. `research/setup/environment_assessment.md`
6. `scripts/run_checks.sh`

**New (58)** (★ = the three additional review files):
1. `environment/README.md`
2. `environment/install_and_verify.sh`
3. `environment/requirements-proposed.txt`
4. `logs/session_logs/2026-11-12_EXEC-SCAFFOLD.md`
5. `manuscript/01_introduction.md`
6. `manuscript/02_methods_literature_review.md`
7. `manuscript/03_methods_experimental.md`
8. `manuscript/04_limitations_prespecified.md`
9. `manuscript/05_reproducibility_and_availability.md`
10. `manuscript/A_appendix_analysis_plan.md`
11. `manuscript/templates/tables_and_figures.md`
12. `research/methodology/experimental_protocol_v1.0_candidate_full.md`
13. `research/methodology/experimental_protocol_v1.0_freeze_candidate.md`
14. `research/reviews/2026-11-12_AB-7_reference_preverification.md`
15. `research/reviews/2026-11-12_CONSOLIDATED-APPROVAL-REQUEST.md`
16. `research/reviews/2026-11-12_CORRECTIONS-AND-DECISION-EVIDENCE.md` ★
17. `research/reviews/2026-11-12_DECISION-SHEET_A1-A6.md`
18. `research/reviews/2026-11-12_EVIDENCE-AND-DECISION-READINESS_REVIEW.md`
19. `research/reviews/2026-11-12_FOCUSED-DECISION-READINESS.md` ★
20. `research/reviews/2026-11-12_PRIOR-ART_AND_METHODS_EVIDENCE.md`
21. `research/reviews/2026-11-12_Q-098_Q-099_Q-100_Q-054_analysis.md`
22. `research/reviews/2026-11-12_Q-098_proposed.patch`
23. `research/reviews/2026-11-12_R15_proposed.patch` ★
24. `scripts/literature/crossref_export_check.py`
25. `scripts/literature/expansion.py`
26. `scripts/literature/flow_diagram.py`
27. `scripts/literature/register_crossref_exports.py`
28. `scripts/literature/rq5_review.py`
29. `scripts/models/README.md`
30. `scripts/models/calibration.py`
31. `scripts/models/compare.py`
32. `scripts/models/conformal.py`
33. `scripts/models/experiment_config_draft.json`
34. `scripts/models/explain.py`
35. `scripts/models/glm.py`
36. `scripts/models/harness.py`
37. `scripts/models/metrics.py`
38. `scripts/models/models.py`
39. `scripts/models/preprocess.py`
40. `scripts/models/report.py`
41. `scripts/models/reproducibility.py`
42. `scripts/models/splits.py`
43. `scripts/models/stats.py`
44. `scripts/models/survey.py`
45. `scripts/models/synthetic.py`
46. `scripts/models/tuning.py`
47. `scripts/nhanes/build_dataset.py`
48. `tests/literature/test_crossref_export_check.py`
49. `tests/literature/test_expansion.py`
50. `tests/literature/test_flow_diagram.py`
51. `tests/literature/test_register_crossref_exports.py`
52. `tests/literature/test_rq5_review.py`
53. `tests/models/test_explain_survey_compare.py`
54. `tests/models/test_metrics_calibration_conformal.py`
55. `tests/models/test_pipeline_scaffolding.py`
56. `tests/models/test_report_and_cli.py`
57. `tests/nhanes/test_build_dataset.py`
58. `tests/synthetic_harness/test_rule_s_harness.py`

## 2. The three additional review files — content check
**Method:**
- a scan for email addresses, phone numbers, credential patterns (key, token, password, secret, bearer, `ghp_`, `sk-`), URLs and the word "abstract";
- a check for the researcher's private email (0 hits);
- a manual reading of the hits.

| File | Contents | Raw data | Credentials | Private contact details | Abstract text |
|---|---|---|---|---|---|
| `2026-11-12_CORRECTIONS-AND-DECISION-EVIDENCE.md` | The 11 deliverables (R15, Q-052, Option C, CR-02/03 access, R14, references, stability, Q-061, critical path, decision sheet) | None (synthetic numerical results only) | None | **None.** Contains the published author names and the institutional affiliation of CR-02's corresponding author (public bibliographic data) and a draft letter, but **no email address** | **None copied.** Only bibliographic records and short paraphrased claims labelled [AB]. One public URL (`doi.org/10.1101/2025.02.10.25321897`). One one-sentence quotation from the public CDC tutorial |
| `2026-11-12_FOCUSED-DECISION-READINESS.md` | Readiness review, Addendum 1 (reconciliation) and this Addendum 2 | None | None | None | None ("abstract" appears only as a status word) |
| `2026-11-12_R15_proposed.patch` | Unified diff for `survey.py` + 2 tests; synthetic test values only | None | None | None | None |

**Note for your judgement:** CORRECTIONS §5 names CR-02's corresponding author in a draft request. This is public bibliographic information. If you prefer not to publish a draft letter in a public repository, exclude or edit that file before approving. This is your choice.

## 3. Proposed corrections to `2026-11-12_DECISION-SHEET_A1-A6.md` (not applied; the file is already in scope, so the count is unaffected)
| # | Location | Current text (exact) | Proposed text |
|---|---|---|---|
| C-1 | §7 line 252, A5 row, column 2 | `Git (59 paths, 4 operations)` | `Git (64 paths: the 61 in §3 plus the three 2026-11-12 review files; 4 operations)` |
| C-2 | §3 line 191, operation 1 | ``1. `git add -- <the 61 paths above>` (explicit paths; never `-A`), then `git diff --cached --name-only \| wc -l` must print 61.`` | ``1. `git add -- <the 64 paths above>` (explicit paths; never `-A`), then `git diff --cached --name-only \| wc -l` must print 64.`` |
| C-3 | §0 template, A5 line | `A5. I authorise the four Git operations listed in §3 of the 2026-11-12 decision sheet, on exactly` / `the 61 listed paths.` | `A5. I authorise the four Git operations listed in §3 of the 2026-11-12 decision sheet, on exactly` / `the 64 paths listed in Addendum 2 of 2026-11-12_FOCUSED-DECISION-READINESS.md.` |
| C-4 (consequential) | §3 path list | 6 modified + 55 new | Add under "Reviews": `2026-11-12_CORRECTIONS-AND-DECISION-EVIDENCE.md`, `2026-11-12_FOCUSED-DECISION-READINESS.md`, `2026-11-12_R15_proposed.patch` → 6 + 58 |
| C-5 (consequential) | §1 runbook, row 2 | `61 paths staged; push accepted` | `64 paths staged; push accepted` |

**Notes:**
- **Alternative:** leave the sheet unchanged and use the C-3 sentence directly in your approval. The sheet would then remain inconsistent until a later correction.
- **Order if authorised:** C-1 to C-5 are made **before** operation 1, so that the committed sheet already shows 64.
- The historical "59" entries in `logs/CHANGELOG.md` (lines 3128, 3131, 3156) and `daily_review_log.md` (line 1000) are append-only and are **not** changed.

## 4. Verification against the working tree
- **Check:** `git status --porcelain -uall` on 2026-11-12 gives 64 lines: **6 ` M` + 58 `??`**, 0 staged.
- **Result:** the §1 list is generated from that output and is identical to it.
- **Comparison with the original list:** §3 of the decision sheet gives 61, and the set difference with the tree is exactly the three ★ files.
- **Excluded and ignored:** raw exports, `records/*.jsonl` and `__pycache__`. These are not in `--porcelain` output because they are ignored.
- **Re-check required:** if any further file is created or modified before execution, the count changes and operation 1's check fails closed. The list must then be re-reconciled.

## 5. A1 ↔ A5 dependencies (no approval or prerequisite marked complete)
**A1 prerequisites** (all open):
- (a) the Q-063 wording choice;
- (b) your confirmation that the WhatsApp details cannot be supplied;
- (c) acceptance of "met at decision level" for condition rows 1, 2 and 4 (D-036; D-055/D-061; D-060 + D-068);
- (d) approval of D-114 to D-121 (Appendix A text, corrected D-121) and of one Stage-0 run plus its commits and push;
- (e) [R] the Drive copies exist and are private. **Required for PRESERVED**; under the alternative wording it is recorded as researcher-reported.

**Must A5 be executed before A1? A correction to my earlier wording:**
- My earlier review said "A1 is not executable without A5". That **overstates** it.
- **What the code requires:**
  - `stage0.py` and `pubrecords.check_ledger_matches_head` refuse only if the run-authorisation ledger differs from its version at HEAD. With no ledger yet, they accept.
  - **No clean-tree check applies to Stage 0.**
  - D-120 (a) refers to the literature tools at `a0af2ad`. The existing literature tools are unchanged; the 10 literature paths in scope are new files only.
- **So A5 is not a technical prerequisite of A1 or Stage 0.**
- **Why A5 first is still the recommended order:**
  1. D-099 (1) requires the ledger and run outputs to go into **one dedicated commit**. With 64 unrelated uncommitted paths in the tree, that commit is still possible with explicit paths, but separating them first removes the risk of mixing.
  2. Recording D-114 to D-121 modifies `logs/DECISION_LOG.md`, which is **not** in the 64. Doing A5 first keeps the A5 commit exactly as authorised and puts the decision-log change in A1's own commit.
  3. A5 preserves the work before any irreversible single-use authorisation is consumed.

**Recommended ordering:**

| Step | Requires | Action |
|---|---|---|
| 0 | Your A5 approval (+ C-1 to C-5 if authorised) | Apply C-1 to C-5 (if authorised); `sh scripts/run_checks.sh`; re-verify 64 paths |
| 1 | A5 | Operations 1–4 (§6) |
| 2 | A1 | Check D-114 to D-122 are unused; insert D-114 to D-121 into `DECISION_LOG.md`; `run_checks.sh`; commit and push the decision-log change (A1's "related commit and push") |
| 3 | A1 | Stage 0 dry run. Expected: `in_scope 1470, E5 5, E7 2, new_rows 7, written false`; anything else stops |
| 4 | A1 | Stage 0 `--write` (single use) |
| 5 | D-099 (1), (2), (5) | One dedicated commit of the ledger + `screening/decisions.csv`, pushed; a status-history row "D-121 used by stage0.py; ledger commit <hash>"; the ledger SHA-256 in the session log |
| 6 | A2 + custodian | Pilot steps (D-122 etc.) |

## 6. The four Git operations (exact; **not performed**)
Run from the repository root on `claude/eloquent-mccarthy-bqtxr3-part1`.

**Operation 1 — stage the approved paths only:**
```bash
git add -- <each of the 64 paths in §1, listed explicitly>   # never -A, never "."
git diff --cached --name-only | wc -l                        # must print 64; otherwise stop and unstage
git diff --cached --name-only | sort | diff - <(sort <the §1 list>)   # must print nothing
```

**Operation 2 — one commit on the authorised branch:**
```bash
git commit -m "<summary of the 2026-11-12 scaffold, review and proposal files (A5)>

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CgJ3gRgrYmk9tG8qm9hN8t"
```

**Operation 3 — normal push** (no `--force`, no `--force-with-lease`):
```bash
git push -u origin claude/eloquent-mccarthy-bqtxr3-part1
```
On a network error, retry up to 4 times with backoff. A rejected (non-fast-forward) push stops and is reported; it is never forced.

**Operation 4 — follow-up commit recording the hash** (only `logs/CHANGELOG.md` and `logs/PROMPT_LOG.md`):
```bash
H=$(git rev-parse --short HEAD)       # the operation-2 commit
# append one line to each log: "A5 commit <H> pushed to claude/eloquent-mccarthy-bqtxr3-part1"
git add -- logs/CHANGELOG.md logs/PROMPT_LOG.md
git diff --cached --name-only | wc -l  # must print 2
git commit -m "Record A5 commit hash <H> (A5)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CgJ3gRgrYmk9tG8qm9hN8t"
git push -u origin claude/eloquent-mccarthy-bqtxr3-part1
```

**Not covered by A5:**
- PR #17 (no description or base change);
- any merge, rebase, reset, branch switch, force-push or branch-protection change;
- `DECISION_LOG.md`;
- R15 application;
- any data.

## 7. Approval text options (for you to copy; nothing is assumed)
- **64 paths:**
  > "A5: I authorise corrections C-1 to C-5 to the decision sheet and the four Git operations of Addendum 2 §6 on exactly the 64 paths of Addendum 2 §1."
- **64 paths without the corrections:**
  > "A5: I authorise the four Git operations of Addendum 2 §6 on exactly the 64 paths of Addendum 2 §1; the decision sheet stays unchanged."
- **61 paths:**
  > "A5: I authorise the four Git operations on exactly the 61 paths of decision sheet §3." This leaves three dangling log references.
- **Subset:** list the paths to exclude.

**Deadline:** 2026-11-27 unchanged. The A1/A5/A2 decision date of 11-13 has zero slack. No contingency condition is met.

**Waiting for your explicit approval.**
