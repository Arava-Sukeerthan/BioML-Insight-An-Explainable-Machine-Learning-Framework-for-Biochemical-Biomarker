# Decision and execution sheet (2026-11-12, Day 30; deadline 2026-11-27)

> **Nothing here is approved or recorded.** An item takes effect only when you state it; anything you do not name stays unapproved.
> Labels:
> - **IMPLEMENTATION** — the assistant's technical choice, made and tested;
> - **RESEARCHER** — reserved for you;
> - **VERIFIED** — checked by a command on 2026-11-12.
>
> Full texts of D-114 to D-121: `2026-11-12_CONSOLIDATED-APPROVAL-REQUEST.md`, Appendix A. Evidence for Q-098 to Q-100 and Q-054: `2026-11-12_Q-098_Q-099_Q-100_Q-054_analysis.md`.

## 0. Approval response template (copy, delete what you do not approve, fill the `<…>`)

**Part 1 — can be decided now** (unblocks Stage 0, the pilot and the parallel lanes)

```
A1. Q-063: answered — preservation status 'off-device backup designated; integrity and privacy
researcher-reported; not independently verified' (not PRESERVED). Archive integrity is verified in
the container; the WhatsApp approval date, wording and approver are not available; conditions are
not recorded. I confirm that I cannot supply those WhatsApp details. I accept this as sufficient to
record the fixed-inventory entry, with the limitation stated. I accept 'met at decision level' for
condition rows 1, 2 and 4. I approve D-114 to D-121 as drafted, and authorise recording them, one
Stage-0 run under D-121, and the related commits and push.

A2. I approve the R1-min revision of D-102 as drafted (execution pack §2) and the D-096 extension
allowing the custodian to receive the private sheet. I appoint <full name or role> as independent
custodian, who has confirmed C1–C6 in writing on <date>. For sharing abstracts I choose <S1 | S2>,
having <read the applicable PubMed/publisher terms myself | other basis: …>. I authorise implementing
and testing `pilot_commitment.py` with synthetic tests, with commit and push. I approve D-122 as
drafted (pilot draw), to be recorded after the Stage-0 commit.

A3. I approve D-002 with the pins in `environment/requirements-proposed.txt`, amended to
`xgboost-cpu==3.4.1` (Q-048: XGBoost, CPU build) and with `wrapt==2.5.2`; I authorise running
`environment/install_and_verify.sh --q048 xgboost-cpu --authorisation <ID> --install` and committing
the generated lock file.

A4. Under D-040 I extend Rule S to synthetic verification of the BL-1–BL-6 and F2 experiment harness
(scope extension; D-040 otherwise unchanged). I approve the test plan in
`tests/synthetic_harness/test_rule_s_harness.py`: (1) exactly 40 configurations per method; (2)
seed-identical reruns identical; (3) validation labels never change development results; (4) a
negative control with labels independent of features gives AUROC within 0.5 ± 0.05 at n = 3,000. I
authorise up to three runs before 2026-11-27, logged in logs/SYNTHETIC_VERIFICATION_LOG.md.

A5. I authorise the four Git operations listed in §3 of the 2026-11-12 decision sheet, on exactly
the 64 paths listed in Addendum 2 of 2026-11-12_FOCUSED-DECISION-READINESS.md.

A6-a. For the 2026-11-27 deadline the frozen protocol keeps Q1–Q3; all six baselines with 5 seeds;
groups A, B and C for the framework and BL-1; sensitivity analyses S-01, S-08 (reference), S-10a and
S-13, with S-09b only if Q-046 is decided; ablations ABL-1 and ABL-2. All other prespecified analyses
are declared now, before any result, as future work.

A6-b. Citation route (a): I will download the Crossref /works JSON for each record to be cited and
each candidate reference needed for AB-7, using the documented curl command and provenance file. I
authorise (1) a registered, targeted PubMed-connector lookup by PMID adding the candidate
references not yet in the inventory, as identified in 2026-11-12_AB-7_reference_preverification.md:
CR-01 (PMID 33951067), CR-05 (19949143), CR-06 (31842878), CR-07 (32188600), CR-08 (41358893),
CR-11 (38626948), CR-12a (32607472), CR-12e (17099194), and an alphaXiv transcription of CR-12b
(arXiv 1705.07874), CR-12c (1603.02754) and CR-12d (2107.07511) (new query rows; D-044 scope
unaffected; CR-03 is already P3005, and CR-09 and CR-10 are unresolved and not included); (2) running crossref_export_check.py and register_crossref_exports.py on my
exports; (3) after the pilot draw, one authorised rebuild with the Q-098 rule, followed by a new
fixed-inventory entry.

Q-098. Crossref year = first present of published-print, published-online; issued is not used;
empty or null dates remain malformed (rejected at intake). I authorise applying
2026-11-12_Q-098_proposed.patch after the pilot draw, with the literature tests re-run, as part of the
authorised rebuild.

Q-099. A Crossref /works response downloaded by me counts as recorded retrieval under D-064 (10)
when it passes crossref_export_check.py and is registered by register_crossref_exports.py with its
researcher-export provenance; D-064 itself is unchanged.

Q-054. Option (b) — no formal non-inferiority claim; ΔAUROC reported with its paired-bootstrap 95% CI;
M10 descriptive only; the research question's 'comparable discrimination' is read descriptively.

Q-100. The Q3 internal reference is the calibrated out-of-fold estimate; the uncalibrated estimate is
reported alongside.

Q-061. <I supply the ADA Standards of Care 2026 Section 2 PDF (doi:10.2337/dc26-S002) by <date> |
I accept the fallback: the outcome is described numerically as a laboratory-defined rule, with no
claim of guideline correspondence, and this is stated as a limitation>.
```

**Part 2 — can be decided now, but needed only for the data step** (edit as needed):

```
Q-016. The provisional research question (protocol v0.1 §1) is approved as the working question.
D-013. Primary disorder: laboratory-defined dysglycaemia (HbA1c ≥ 5.7% or FPG ≥ 100 mg/dL) in adults
       without diagnosed diabetes.
D-014. Primary development dataset: NHANES 2017–March 2020 (CDC public files, SHA-256 per protocol
       Appendix A).
D-015. No independent external dataset within the deadline; temporal validation on NHANES
       August 2021–August 2023, reported as temporal, not external, validation.
Q-018. I approve research/methodology/research_integrity.md (draft v1.0) as binding for Stages F–J.
Q-044 / Q-046 / Q-060 (AB-8). Accept the documented fallback: S-08 (unadjusted 2021–2023 values) is
       the reference; S-09b is not run unless Q-046 and Q-060 are decided; the mg/dL reading of the
       TRIGLY_L equation is accepted with the §8.1 check as supporting evidence only.
DOWNLOAD. Run authorisation: one download of the 32 NHANES files of protocol Appendix A by the
       commands in §1 step 9 of the 2026-11-12 decision sheet into git-ignored data/raw/nhanes/,
       verified by descriptive_counts.verify_inputs(); then build_dataset.py for both periods
       (must reproduce the §4 counts, AB-12).
```

**Part 3 — cannot be decided until research evidence exists:**

| Item | Waits for |
|---|---|
| Expansion approval (protocol v0.2 §8), batch seed and audit rule (`expansion.py`), Q-084 audit timing | A passed pilot |
| D-016 contribution | The RQ5 review (`rq5_review.py` output; Stage D gate) |
| D-017, D-018 | The Stage C and D gates, and AB-7 |
| D-019 freeze | All of the above; the assembled v1.0 candidate plus your edits |
| R-1, R-2, R-3 | Only if their trigger dates are missed (§6) |

## 1. Execution runbook: commands and expected outputs

**VERIFIED twice on 2026-11-12** (scratch copy with the drafts inserted; deleted afterwards; the real repository untouched):
- the Stage-0 dry run;
- the frame check;
- the authorisation checks for D-121 and D-122.

The values below are the reproduced outputs.

| # | After | Command (repository root) | Expected output / stop condition |
|---|---|---|---|
| 1 | A1, A5 | Check that D-114 to D-122 are unused; insert D-114 to D-121; `sh scripts/run_checks.sh` | All suites pass |
| 2 | A5 | The four Git operations (§3) | 64 paths staged; push accepted |
| 3 | A1 | `python3 -I scripts/literature/stage0.py --lit-dir research/literature --authorization D-121 --expected-inventory-sha256 b668dbde42473baa49ac1f02f89f900e94e39159c82efb8175ba125fef06d054 --criteria-version criteria_v1.1+protocol_v0.2` (dry run) | `in_scope 1470, E5 5, E7 2, new_rows 7, written false`; anything else stops |
| 4 | A1 | The same with `--write` | `written true`; ledger "started" then "completed" |
| 5 | A1 | Commit and push the ledger and `screening/decisions.csv` in one dedicated commit (D-099 (1)) | — |
| 6 | A2 | Implement `pilot_commitment.py` (`make`, `verify`; C = SHA-256("bioml-insight pilot commitment v1\n" ‖ S ‖ "\n" ‖ F)); 5 synthetic tests; commit | Tests pass |
| 7 | A2 | Record D-122; `python3 -I scripts/literature/pilot_sample.py --lit-dir research/literature --expected-inventory-sha256 b668…d054 --authorization D-122 --write`; commit and push the sample, sidecar and ledger | 60 records; frame 1,463; strata F 120, D 13, C 93, E 68, A 365, Q 8, B 623, untagged 173; sidecar hashes equal D-114 (D-113 stops otherwise) |
| 8 | A2 + custodian | `pilot_sheet.py --lit-dir research/literature --authorization D-122` → private sheet to the custodian; custodian returns C → commit; you screen the 60; the custodian returns F and S → `pilot_commitment.py verify`; `pilot_agreement.py report --lit-dir … --assistant … --researcher … --sample …` | Pass rule (κ ≥ 0.60, no unresolved include/exclude conflict, < 3 disagreements on any code) |
| 9 | DOWNLOAD | `for k in $(python3 -I -c "import sys; sys.path.insert(0,'scripts/nhanes'); from descriptive_counts import EXPECTED_SHA256 as E; print(' '.join(E))"); do p=${k%%/*}; f=${k##*/}; y=${p%%-*}; [ "$y" = 2017 ] \|\| y=2021; mkdir -p data/raw/nhanes/$p; curl -sSfR -o data/raw/nhanes/$k.xpt "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/$y/DataFiles/$f.xpt"; done` then `python3 -I -c "import sys; sys.path.insert(0,'scripts/nhanes'); import descriptive_counts as d; d.verify_inputs(); print('32/32 SHA-256 OK')"` | `32/32 SHA-256 OK`. Any mismatch stops; nothing is substituted. `data/raw/` is Git-ignored |
| 10 | A3 | `bash environment/install_and_verify.sh --q048 xgboost-cpu --authorisation <ID> --install` | Today's dry run: 28 packages, no pre-release, no GPU library. With `--install`: lock file written, imports OK, all suites pass |
| 11 | A3 + A4 | `RULE_S_AUTHORISATION=<ID> environment/.venv/bin/python -I -m unittest discover -s tests/synthetic_harness -v` | 4 tests pass; per-method seconds and null AUROC appended to `logs/SYNTHETIC_VERIFICATION_LOG.md`. Today the tests skip (no authorisation, no packages) |
| 12 | A6-b, Q-098, Q-099 | You: `curl -sS -D CRX_<date>_<n>.headers.txt -o CRX_<date>_<n>.json "https://api.crossref.org/works/<doi>"` into `research/literature/raw_exports/` + `provenance.csv`; assistant: `crossref_export_check.py research/literature/raw_exports --inventory research/literature/paper_inventory.json`, then (after the draw and the patch) `register_crossref_exports.py --lit-dir research/literature --package research/literature/raw_exports --authorization <ID> --write`, then the authorised rebuild | Checker `accepted`; manifest rows `VERIFY-CR-<paper_id>`; rebuild marks `verified` only where all fields agree |
| 13 | Passed pilot + expansion approval | `expansion.py batches --lit-dir … --expected-inventory-sha256 b668…d054 --pilot-sample research/literature/screening/pilot_sample.csv --seed <decided> --authorization <ID> --out research/literature/screening/expansion_batches.csv` | 1,403 records in 5 batches of 280 or 281 |
| 14 | Batches 1–2 screened (Q-084) | `expansion.py audit --lit-dir … --batches-file … --batches 1 2 --seed <decided> --out research/literature/screening/audit_sample.csv` | 50 IDs (25 include + 25 exclude), no decisions shown |
| 15 | Full texts | `flow_diagram.py`; `rq5_review.py` | Reconciled flow counts; RQ5 matrix, D-038 subgroups, verification queue |

## 2. Custodian and source terms

**Minimum requirements for a genuine independent custodian** (all needed; a second session or account under your control **never** qualifies):

| # | Requirement |
|---|---|
| C1 | A different natural person: not you, and with no stake in whether the pilot passes |
| C2 | Their own account and computing environment, to which you have no access |
| C3 | Able to run an assistant session and Python 3 at a recorded commit |
| C4 | Receives the private sheet by a private channel; never publishes or commits it; deletes it after disclosure |
| C5 | Returns C before you start screening, and F and S after you finish (target 11-14 to 11-16) |
| C6 | Does not discuss any pilot decision with you before disclosure |

**What I need from you:** the name or role; their written confirmation of C1–C6; the channel; the dates. **VERIFIED:** no custodian is named, and none is assumed.

**Sharing abstracts — what is unknown:**
- **Known:** D-010 records that "Abstracts may be under publisher copyright" and keeps them out of the public repository.
- **Unknown:**
  - the applicable PubMed, NLM and publisher terms: the NLM and NCBI pages could not be read from this environment on 2026-11-12 (DNS failure), and nothing is quoted or assumed;
  - whether a private, one-person, purpose-limited copy (S1) is permitted for every source in the 60-record sample;
  - whether, under S2, the PubMed text the custodian sees equals the inventory text (version drift).
- **Neither S1 nor S2 is shown to be compliant.** The choice and its basis are yours; the template asks you to state the basis.

## 3. A5 — exact Git scope (verified by `git status --untracked-files=all` on 2026-11-12)

**Six modified paths:**
- `logs/CHANGELOG.md`
- `logs/PROMPT_LOG.md`
- `research/reviews/daily_review_log.md`
- `research/reviews/unresolved_questions.md`
- `research/setup/environment_assessment.md`
- `scripts/run_checks.sh`

**Fifty-eight new paths** (55 + the three 2026-11-12 review files added under A5, correction C-4):
- **Environment:** `environment/README.md`, `environment/install_and_verify.sh`, `environment/requirements-proposed.txt`
- **Session log:** `logs/session_logs/2026-11-12_EXEC-SCAFFOLD.md`
- **Manuscript:** `manuscript/01_introduction.md`, `manuscript/02_methods_literature_review.md`, `manuscript/03_methods_experimental.md`, `manuscript/04_limitations_prespecified.md`, `manuscript/05_reproducibility_and_availability.md`, `manuscript/A_appendix_analysis_plan.md`, `manuscript/templates/tables_and_figures.md`
- **Protocol candidates:** `research/methodology/experimental_protocol_v1.0_candidate_full.md`, `research/methodology/experimental_protocol_v1.0_freeze_candidate.md`
- **Reviews:** `research/reviews/2026-11-12_AB-7_reference_preverification.md`, `research/reviews/2026-11-12_CONSOLIDATED-APPROVAL-REQUEST.md`, `research/reviews/2026-11-12_DECISION-SHEET_A1-A6.md`, `research/reviews/2026-11-12_EVIDENCE-AND-DECISION-READINESS_REVIEW.md`, `research/reviews/2026-11-12_PRIOR-ART_AND_METHODS_EVIDENCE.md`, `research/reviews/2026-11-12_Q-098_Q-099_Q-100_Q-054_analysis.md`, `research/reviews/2026-11-12_Q-098_proposed.patch`, `research/reviews/2026-11-12_CORRECTIONS-AND-DECISION-EVIDENCE.md`, `research/reviews/2026-11-12_FOCUSED-DECISION-READINESS.md`, `research/reviews/2026-11-12_R15_proposed.patch`
- **Literature scripts:** `scripts/literature/crossref_export_check.py`, `scripts/literature/expansion.py`, `scripts/literature/flow_diagram.py`, `scripts/literature/register_crossref_exports.py`, `scripts/literature/rq5_review.py`
- **Experiment code:** `scripts/models/README.md`, `scripts/models/calibration.py`, `scripts/models/compare.py`, `scripts/models/conformal.py`, `scripts/models/experiment_config_draft.json`, `scripts/models/explain.py`, `scripts/models/glm.py`, `scripts/models/harness.py`, `scripts/models/metrics.py`, `scripts/models/models.py`, `scripts/models/preprocess.py`, `scripts/models/report.py`, `scripts/models/reproducibility.py`, `scripts/models/splits.py`, `scripts/models/stats.py`, `scripts/models/survey.py`, `scripts/models/synthetic.py`, `scripts/models/tuning.py`
- **Dataset build:** `scripts/nhanes/build_dataset.py`
- **Literature tests:** `tests/literature/test_crossref_export_check.py`, `tests/literature/test_expansion.py`, `tests/literature/test_flow_diagram.py`, `tests/literature/test_register_crossref_exports.py`, `tests/literature/test_rq5_review.py`
- **Model tests:** `tests/models/test_explain_survey_compare.py`, `tests/models/test_metrics_calibration_conformal.py`, `tests/models/test_pipeline_scaffolding.py`, `tests/models/test_report_and_cli.py`
- **Other tests:** `tests/nhanes/test_build_dataset.py`, `tests/synthetic_harness/test_rule_s_harness.py`

**Excluded (Git-ignored, never staged):**
- 244 raw exports in `research/literature/raw_exports/`;
- `research/literature/records/publications.jsonl` and `source_records.jsonl`;
- 58 `__pycache__` files (count on 2026-11-12; it changes with every test run, and these files are never staged).

**The four operations:**
1. `git add -- <the 64 paths above>` (explicit paths; never `-A`), then `git diff --cached --name-only | wc -l` must print 64.
2. `git commit` on `claude/eloquent-mccarthy-bqtxr3-part1`, with the attribution lines.
3. `git push -u origin claude/eloquent-mccarthy-bqtxr3-part1` (no force).
4. A follow-up commit recording the hash of commit 2 in `logs/CHANGELOG.md` and `logs/PROMPT_LOG.md`, pushed the same way.

**Not covered:** PR #17's description, any merge, force-push, branch-protection change, or data.

## 4. Implementation status for each open question

| Question | IMPLEMENTATION (done, tested) | RESEARCHER |
|---|---|---|
| Q-098 | Patch prepared (379 literature tests OK in a scratch copy; applies cleanly; not applied). Empty dates stay fail-closed by design | The rule; when the patch is applied |
| Q-099 / D-064 | Checker (8 tests); registration step (3 tests); manifest provenance; `CRX_` naming | Whether researcher exports count as recorded retrieval |
| Q-100 | The harness records both internal estimates; wording in the v1.0 candidate §13 | The Q3 reference at D-019 |
| Q-054 | ΔAUROC paired-bootstrap CI implemented; the non-inferiority function is unused | (a) or (b) |
| Expansion | `expansion.py` (6 tests): seeded batches; blinded 25 + 25 audit sample | Batch seed, audit rule and timing (Q-084), expansion approval |
| RQ5 | `rq5_review.py` (4 tests): matrix from confirmed full-text statuses only; D-038 subgroups; verification queue | D-016 after the review |
| Environment | `install_and_verify.sh` (dry run: 28 packages, no pre-release, no GPU) | A3, Q-048 |
| Rule S | `tests/synthetic_harness/` (gated; skips without A4 and packages) | A4 route |
| Download | Command in §1 step 9 plus the existing hash check. No network code in `scripts/nhanes/`: the committed offline safeguard forbids it | DOWNLOAD authorisation |

## 5. Q-100 rationale (for D-019)
- The frozen model is calibrated, so temporal-validation metrics are on the calibrated scale.
- An uncalibrated internal reference mixes the calibration effect into the measured transfer. In the synthetic illustration, a calibration loss of +0.049 ICI appeared as −0.049.
- AUROC is unaffected.

## 6. Critical path and latest feasible dates (re-checked 2026-11-12, EXEC-SCAFFOLD-10; no approval received yet)

No approval has been received yet, so the 11-13 approval date now carries **zero slack**: every later step moves day for day.

| Milestone | Target | Latest | If missed (applied only by your decision) |
|---|---|---|---|
| Part 1 approvals + named custodian | 11-13 | **11-13** | Each day of delay moves pilot completion past 11-16 → **R-1** becomes likely |
| Stage 0 written and committed | 11-13 | **11-14** | — |
| Pilot draw; custodian's C | 11-14 | 11-15 | — |
| **Pilot complete** | 11-15 | **11-16** | Failed pilot → retry about +5 days (Q-083) → **R-3** |
| Title/abstract screening (about 1,403 records) + audit (you) + missing-abstract review (you) | 11-19 | **11-20** | Later than 11-19 → **R-1** |
| Full text Tier 1 + RQ5; RQ5 verification (you) | 11-21 | 11-21 | — |
| **ADA 2026 Section 2 PDF (Q-061)** | 11-14 | **11-20** | Outcome kept, but no guideline-correspondence claim (AB-7 §3 fallback, your decision) |
| **Stage C and D gates**; D-016 | 11-21 | **11-22** | Later than 11-24 → **R-3** |
| **Protocol freeze D-019** (after D-017, D-018; includes R13, R14, Q-100, Q-054) | 11-22 | **11-22** | Later than 11-22 → **R-2** |
| Parallel: A3 install → A4 synthetic runs (runtime measured) | 11-13 | 11-20 | Experiment window unverified |
| Parallel: Part 2 data decisions → download + build (AB-12) | 11-14 | 11-21 | — |
| Parallel: CR look-up + your Crossref exports + rebuild (after the draw) → AB-7 | 11-14 to 11-18 | **11-21** | AB-7 unmet → **no training** |
| **Experiments** | 11-23 to 11-24 | **11-25** | — |
| **Manuscript complete** | 11-26 | **11-27** | — |

**Trigger status:** **none is triggered.** R-1 is **approaching**: with zero slack, a one-day delay in Part 1 makes the 11-19 screening date infeasible. R-2 and R-3 are not yet approaching.

**Smallest acceptable reduction, if needed:** R-1 first. It narrows full-text reading to Tier 1 + RQ5 and uses 20 explanation refits. It reduces literature depth, not validation, and it keeps every safeguard. R-2 only if the freeze slips past 11-22.

Never reduced: Q1–Q3, temporal validation, equal budgets, safeguards, reporting of null results.

## 7. Approval register (none approved)

| Item | Decision required | Options | Scientific consequence | Evidence needed / available | Blocks |
|---|---|---|---|---|---|
| A1 | Q-063 status; D-114 to D-121; Stage 0 | Alternative wording (rec.) / PRESERVED with your written confirmation | A permanent, honest limitation on the backup; fixes the screening inventory | Available (dry runs reproduced twice). Missing: the WhatsApp details | **Stage 0, pilot, screening** |
| A2 | Custodian; R1-min; D-096 extension; S1/S2; D-122 | A named person meeting C1–C6; S1 or S2 | Pilot blinding (screening validity) | Missing: the custodian; your judgement on the source terms | **Pilot** |
| A3 | D-002 install; Q-048 | `xgboost-cpu` (rec.) / `xgboost` / scikit-learn histogram gradient boosting; `wrapt` 2.5.2 | Same learner either XGBoost way; HGB would change F2/BL-3 | Dry run: 28 packages, no pre-release, no GPU | Synthetic verification, experiments |
| A4 | Rule S route | (i) extend D-040 (rec.) / (ii) scaffolding | Audit trail for synthetic fitting | Test file ready (gated) | Synthetic verification |
| A5 | Git (64 paths: the 61 in §3 plus the three 2026-11-12 review files; 4 operations) | Approve / subset | Preserves the work; required before Stage 0 (D-099) | Scope reconciled (§3) | **Everything after Stage 0** |
| A6-a | Deadline scope | As proposed / modify | Less breadth; primary questions intact | v1.0 candidate §4, §9 | D-019 |
| A6-b | Citation route; registered look-up | (a) exports (rec.) / (b) amend D-064 / (c) defer | Citations become possible under D-064 | AB-7 record (FT/AB/MD levels) | **AB-7 → training; manuscript** |
| A6-c / Q-054 | Non-inferiority | (b) descriptive (rec.) / (a) a margin with its justification | Changes the wording of the research question | No source supports a margin | D-019 |
| Q-098 | Crossref year field | (c) print → online (rec.) / (a) / (b) | Avoids false conflicts for online-first articles | Patch tested (379 OK) | AB-7 |
| Q-099 | Researcher exports as recorded retrieval | Accept / script-only (needs network) | Weaker, but auditable, provenance | Checker and registration tested | AB-7 |
| Q-100 | Q3 internal reference | Calibrated (rec.) / uncalibrated | Avoids confounding calibration with transfer | Synthetic illustration | D-019 |
| Q-061 | ADA source for the thresholds | Supply the PDF / allow the host / accept the fallback | Guideline-correspondence claim or none | AB-7 §3 | D-019 wording |
| Part 2 | Q-016, D-013, D-014, D-015, Q-018, AB-8 fallback, download | As drafted in §0 / modify | Defines the target, data and validation design | Drafts in §0; CR-02 shows the same outcome in use | **Real-data processing** |
| Later | D-016, D-017, D-018, D-019 | After the gates | Contribution and frozen methods | Requires completed screening (AB-7 §4) | **Experiments** |

## 8. Experimental readiness — dependency table

| Component | Current state | Implementation (done/tested) | Must be approved before real-data experiments |
|---|---|---|---|
| Dataset selection | NHANES proposed | — | **D-014** |
| Dataset provenance | 32 files, URLs reachable, byte counts match | Download command + SHA-256 check | **Download authorisation** |
| Outcome definition | Lab OR rule (HbA1c ≥ 5.7 or FPG ≥ 100) | `build_dataset.outcome` | **D-015/FA-2**; Q-061 source (CR-08) |
| Inclusion/exclusion | E0–E8 cascade; counts recorded | `safeguards.eligibility_cascade`; build must reproduce the counts (AB-12) | FA-1 (age ≥ 20) |
| Preprocessing | In-fold; log transforms; scaling for some baselines | `preprocess.InFoldPreprocessor` (leakage-tested) | D-019 |
| Missing values | Median/mode + indicators above 5%; outcome never imputed | Same | D-019 (S-10a complete-case kept under A6-a) |
| Leakage prevention | Serum glucose and awareness items excluded; in-fold fitting; validation isolated | Tests: validation labels never change development results | D-019; Q-018 (integrity protocol) |
| Harmonisation | S-08 reference; S-09b conditional | `build_dataset.harmonise` (S-09b blocked by Q-046) | **AB-8 fallback** or Q-044/Q-046/Q-060 |
| Baseline selection | BL-1 to BL-6 | Registry; equal budget 40 | **D-018** (needs RQ1 screening, AB-7) |
| Proposed methodology | F1–F5 | Harness | **D-017** (needs Stage C/D gates) |
| Calibration | Platt on D-cal; ICI, intercept and slope | Implemented; ICI = local-linear, span 0.75 (R14 decision record in `2026-11-12_PRIOR-ART_AND_METHODS_EVIDENCE.md` §4) | **D-019:** R14 option (a)/(b)/(c) + span sensitivity analysis; Platt source (UV) |
| Uncertainty | Mondrian split conformal, α = 0.10 | Matches CR-12d (FT) | D-019 (Q-051) |
| Explainability | TreeSHAP; stability over refits and periods | `explain.py` | **D-019** (F5 metric); motivation source located (Alvarez-Melis & Jaakkola 2018, FT); a methods source for refit/period rank stability **still missing** |
| Independent validation | **Temporal** (2021–2023); no external dataset | Applied once; fingerprinted | **D-015** (stated as temporal, not external) |
| Statistical analysis | Paired bootstrap, Holm, descriptive ΔAUROC; Taylor-linearised descriptive estimates with **domain** option (R15) | `stats.py`, `compare.py`, `survey.py` | **D-019**; Q-054; Q-100; R15 wording; Holm and bootstrap sources (UV) |
| Reproducibility | Hash-bound protocol; clean-tree guard; seeds; environment record | Harness guard (tested) | A3 (lock file); A5 (commits) |

**Single next action:** send Part 1 of the template, with A1, A5 and a named custodian at minimum, **and** the ADA 2026 Section 2 PDF.
