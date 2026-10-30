# Daily Review Log

One entry per researcher review session (~1 h/day).

## Day 1 — 2026-10-14
- Items for review: `GOVERNANCE.md` (schedule), `research/setup/environment_assessment.md`, `logs/DECISION_LOG.md` (D-001 to D-004), `research/reviews/unresolved_questions.md`.
- Researcher decisions: _pending_

## Day 1 (cont.) — 2026-10-14 — LIT-001
- Items for review (priority order): `research/literature/search_strategy.md` §1.3, §2, §4.1, §6; `screening_criteria.md` §2; `logs/DECISION_LOG.md` D-005–D-009; `unresolved_questions.md` Q-001, Q-002, Q-006, Q-007, Q-010.
- Researcher decisions: _pending_

## Day 1 (cont.) — 2026-10-14 — LIT-002
- Items for review: `research/literature/collection_workflow.md` §2.1, §3, §4.2–4.3, §6, §7, §8; `logs/DECISION_LOG.md` D-010–D-012; `unresolved_questions.md` Q-003 (eutils host), Q-011, Q-012.
- Researcher decisions: _pending_

## Day 10 — 2026-10-23 — BIO-001
- **Task ID:** BIO-001 (establish research governance and project logbook)
- **Work completed:** inspected the repository; existing governance and literature-design work (P001, LIT-001, LIT-002) was preserved. Expanded `CLAUDE.md` with the BIO-001 rules. Rewrote `README.md` (title, objective, provisional RQ, stages, integrity, layout, status). Added pending research decisions D-013–D-020 (cross-referenced to BIO-001 prompt items BIO-001/D001–D008) and process decisions D-021, D-022. Created `research/literature/research_plan.md` (themes A–F overview) and `research/methodology/research_integrity.md`. Updated the logs.
- **Important findings:** `[EVIDENCE]` The repository was not empty: 3 prior tasks and 6 commits, all from 2026-10-14, with nothing since. `[EVIDENCE]` The project is behind the proposed schedule: Day 10, and the Stage-B search has not been run (Q-013). `[EVIDENCE]` The bibliographic APIs are still blocked (re-checked with `curl`, HTTP 000). No literature findings: no search was run (by instruction).
- **Decisions requiring review:** D-013–D-020 (all PENDING); D-021 (PR workflow), D-022 (CLAUDE.md scope); still-open earlier proposals D-001, D-002, D-005–D-010, D-012.
- **Outstanding problems:** schedule slip (Q-013); decision numbering (Q-014); default branch is a `claude/` branch, not `main` (Q-015); network access (Q-003); scope questions Q-001, Q-002.
- **Recommended next step:** researcher review of the pending approvals needed to start Stage B (D-005–D-007, D-010, Q-001, Q-002, Q-013). Then LIT-003: run the PubMed snapshot queries, register raw exports, deduplicate and verify.
- **Researcher decisions:** _pending_

## Day 10 (cont.) — 2026-10-23 — BIO-001-REVIEW
- **Task ID:** BIO-001-REVIEW (review and correction of PR #1, not merged)
- **Work completed:** restored D-004 and D-011 to PROPOSED (original rows from `330d3fd`); recorded D-021/D-022 as alternatives; added a status-history table; made the BIO-001/D001–D008 → D-013–D-020 mapping explicit; corrected the README status and stage table; updated Q-005, Q-012 and Q-014; added Q-019.
- **Important findings:** `[EVIDENCE]` In BIO-001, the assistant marked D-004 and D-011 SUPERSEDED while they were awaiting the researcher (Q-005, Q-012) and their replacements were unapproved. The log's "replaced before approval" rule does not justify that, so the change was reversed. `[EVIDENCE]` The README stage table placed Stage F entirely after Day 20, contrary to GOVERNANCE.md §3. It also said "no literature search has been run" without mentioning the pilot queries. Both are corrected.
- **Decisions requiring review:** D-013–D-020 (PENDING); D-004 vs D-021; D-011 vs D-022; D-001, D-002, D-005–D-010, D-012 (PROPOSED).
- **Outstanding problems:** Q-013 (schedule slip), Q-014, Q-015, Q-019, plus earlier open questions.
- **Recommended next step:** unchanged. Researcher review of the decisions needed for Stage B, then LIT-003.
- **Researcher decisions:** _pending_

## Day 10 (cont.) — 2026-10-23 — LIT-003
- **Task ID:** LIT-003 (execute the stored literature searches; collection, deduplication, verification; no screening)
- **Work completed:** source access tested (19 probes); 15 PubMed queries executed in full (3,413 hits, 2,866 unique PMIDs) with an independent re-fetch check (15/15 identical); metadata retrieved for all 2,866 PMIDs; 5 arXiv and 6 web queries executed; build → 2,979 publications; register, access report, verification report, evidence table, full-text candidate list (234) and collection summary written.
- **Important findings:** `[EVIDENCE]` Only PubMed, alphaXiv and web search are reachable; Europe PMC, Crossref, OpenAlex, Semantic Scholar, E-utilities and repository APIs are blocked (CONNECT 403); the Consensus quota is exhausted. `[EVIDENCE]` 564 exact identifier duplicates removed; 15 pairs flagged for manual decision; 3 retracted records flagged. `[EVIDENCE]` 14 verified, 2,928 partially verified, 36 unverified, 1 needs review. `[OPEN]` No content-level findings: nothing has been screened or read.
- **Decisions requiring review:** Q-022 (approve the executed strategy: D-005–D-007, D-010); D-023, D-024 (proposed); Q-020, Q-021, Q-023, Q-024, Q-025; still Q-001/Q-002 (scope), D-009 (Q-PM-02 handling), D-008 (audit).
- **Outstanding problems:** raw exports exist only in the container (Q-011, urgent); second-source verification blocked (Q-021).
- **Recommended next step:** researcher decisions on Q-011 and Q-022 (plus Q-001/Q-002/Q-007), then LIT-004: title/abstract screening of the 2,979 records against `screening_criteria.md`, with the pilot calibration (§7) and the audit sample.
- **Researcher decisions:** _pending_

## Day 10 (cont.) — 2026-10-23 — LIT-003-PRESERVATION-CONFIRMATION
- **Work completed:** recorded the researcher's Windows SHA-256 verification of the downloaded LIT-003 archive (matches `69e690f0…0c0e`).
- **Important findings:** `[EVIDENCE]` (researcher-reported) the downloaded copy is identical to the verified container archive. `[OPEN]` No second private backup or durable storage confirmed yet.
- **Decisions requiring review:** Q-011 (confirm durable backup); earlier items unchanged (Q-022 etc.).
- **Recommended next step:** keep a second private copy (e.g. institutional or private cloud storage) and confirm here. Then LIT-004 after the pending approvals.
- **Researcher decisions:** _pending_

## Day 10 (cont.) — 2026-10-23 — LIT-003-PRESERVATION-CONFIRMATION (second update)
- **Work completed:** recorded a second checksum-verified copy of the LIT-003 archive on the researcher's computer.
- **Important findings:** `[EVIDENCE]` (researcher-reported) two verified copies exist, both on the same computer. `[OPEN]` No off-device backup.
- **Decisions requiring review:** Q-011 (off-device backup).
- **Recommended next step:** put one copy on separate private media or storage and confirm it.
- **Researcher decisions:** _pending_

## Day 10 (cont.) — 2026-10-23 — LIT-004-PREPARATION
- **Work completed:** draft screening protocol (`research/literature/screening_protocol.md`, v0.1, proposed); review of the 15 dedup pairs and 3 retraction flags (descriptive only, no decisions); blockers recorded.
- **Important findings:** `[EVIDENCE]` 9 web-only records have unstable paper IDs (B-1). `[EVIDENCE]` The workflow cannot link preprint/published versions; 3 version pairs can never be merged (B-2). `[EVIDENCE]` Two different screening-file formats are specified in project documents (B-3); the inventory status enum lacks `uncertain` (B-4). `[EVIDENCE]` No off-device backup is available (no external drive).
- **Decisions requiring review:** D-025, D-026; Q-026–Q-030; still Q-001, Q-002, Q-007/D-009, Q-008/D-008, Q-022, Q-024.
- **Recommended next step:** researcher review of the protocol and blockers; then fix B-1 (and B-3/B-4 if approved) before generating the pilot sample.
- **Researcher decisions:** _pending_

## Day 10 (cont.) — 2026-10-23 — LIT-004-WORKFLOW-FIXES
- **Work completed:** fixed blockers B-1 (stable IDs for 9 web-only records; IDs kept), B-3 (one validated screening file and schema), B-4 (screening status carried into the inventory; manual values survive rebuilds); 21 regression tests.
- **Important findings:** `[EVIDENCE]` two rebuilds are byte-identical and keep every paper ID. `[EVIDENCE]` The inventory's `publication_type` list and the protocol's `record_type` list differ (Q-031). `[OPEN]` The format and key scheme are implemented but not approved (D-027).
- **Decisions requiring review:** D-027 (with Q-027, Q-030); Q-031, Q-032; earlier items unchanged (D-025, D-026, Q-026, Q-028, Q-029, Q-001, Q-002, Q-007/D-009, Q-008/D-008, Q-022, Q-024).
- **Recommended next step:** `[RECOMMENDATION]` researcher review of D-027 and the remaining blockers B-2, B-5, B-6; then the pilot sample (D-025) once approved.
- **Researcher decisions:** _pending_


## Day 10 (cont.) — 2026-10-23 — LIT-004-REVIEW-AND-DECISIONS
- **Work completed:** decision texts for D-027–D-030 prepared; version-linking proposal; scope decision brief; two integrity gaps in the report script closed; 7 tests.
- **Important findings:** `[EVIDENCE]` the stated meanings for Q-031 and Q-032 conflict with the current schema/D-026 (options prepared). `[EVIDENCE]` `same` decisions cannot link versions and are ignored for identifier-conflict pairs. `[EVIDENCE]` Proteomics is undefined in the biomarker scope (Q-033).
- **Decisions requiring review:** D-027, D-028, D-029, D-030; scope items in `scope_decision_brief.md`; full list in `approval_request_LIT-004.md` §3.
- **Recommended next step:** `[RECOMMENDATION]` researcher approvals per `approval_request_LIT-004.md` §3, then implement D-028–D-030 and generate the pilot.
- **Researcher decisions:** _pending_

## Day 10 (cont.) — 2026-10-23 — LIT-004-DECISION-RECONCILIATION
- **Work completed:** consolidated decision table and reconciliation (`research/reviews/decision_reconciliation_LIT-004.md`); no production change.
- **Important findings:** `[EVIDENCE]` the prepared D-028 enum misses protocols, datasets, guidelines and expressions of concern; D-029 as prepared differs from the owner's restatement; D-030 is ambiguous on primaries, withdrawals, retractions and PRISMA levels; the D-012 spot-check was not done for arXiv/web; 30 of 56 planned searches were not run. `[HYPOTHESIS]` Q-PM-02 is both broader and narrower than the provisional scope (MeSH tree not verified).
- **Decisions requiring review:** 15 items in §9 of the reconciliation; Q-035, Q-036.
- **Recommended next step:** `[RECOMMENDATION]` owner answers §9; then the implementation order in §10.
- **Researcher decisions:** _pending_

## Day 11 — 2026-10-24 — LIT-004-OWNER-BALLOT
- **Work completed:** owner-review ballot `research/reviews/owner_review_ballot_LIT-004.md` (17 items, APPROVE/REJECT/MODIFY/DEFER fields).
- **Important findings:** `[EVIDENCE]` all 34 source publication types are covered by the D-028 mapping; the 15 dedup pairs reconcile exactly with `dedup_review.csv` (30 IDs, no mismatch); 26 of 56 planned searches were executed.
- **Decisions requiring review:** all 17 ballot items.
- **Recommended next step:** owner fills in the ballot; responses are then recorded in `logs/DECISION_LOG.md` before any implementation.
- **Researcher decisions:** _pending_

## Day 11 (cont.) — 2026-10-24 — LIT-004-PROPOSED-RESPONSES
- **Work completed:** proposed owner-response set v1 for the 17 ballot items (`research/reviews/proposed_owner_responses_LIT-004.md`); not recorded in the decision log.
- **Important findings:** `[EVIDENCE]` no current record is affected by the retraction procedure (the 3 retracted articles are unlinked; no retraction notices). `[OPEN]` D-024 vs Q-034 scope of the approval; A-3/Q-028 deferred affects theme F screening in the pilot.
- **Decisions requiring review:** owner confirmation of the response set (all or selected items); D-029 final definitions; D-030 retraction procedure.
- **Recommended next step:** owner confirmation; then record in `logs/DECISION_LOG.md`, then the arXiv spot-check.
- **Researcher decisions:** _pending_

## Day 11 (cont.) — 2026-10-24 — LIT-004-CLARIFICATION-ADDENDUM
- **Work completed:** clarification addendum (`research/reviews/clarification_addendum_LIT-004.md`) with response fields R1–R6.
- **Important findings:** `[EVIDENCE]` the retraction procedure needs a Stage-0 amendment (notices not covered); mechanical RQ5 derivation would need a feature-selection descriptor. `[RECOMMENDATION]` decide Q-028 before the pilot (owner's choice).
- **Decisions requiring review:** R1–R6.
- **Recommended next step:** owner answers R1–R6 and confirms what is to be recorded.
- **Researcher decisions:** _pending_

## Day 11 (cont.) — 2026-10-24 — LIT-004-FINAL-CONFIRMATION-SHEET
- **Work completed:** final confirmation sheet (`research/reviews/final_confirmation_sheet_LIT-004.md`).
- **Important findings:** `[EVIDENCE]` after confirmation, the pilot is still blocked by Q-028 (or the provisional alternative), the D-029 definitions, the recorded schema decisions, the arXiv spot-check, implementation and criteria v1.1/protocol v0.2.
- **Decisions requiring review:** R1–R6 and the v1 items.
- **Recommended next step:** owner completes the sheet; then recording per R6.
- **Researcher decisions:** _pending_

## Day 11 (cont.) — 2026-10-24 — LIT-004-Q028-DECISION
- **Work completed:** owner response to Q-028 verified and recorded as D-031 (APPROVED — CONDITIONAL).
- **Important findings:** `[EVIDENCE]` feature selection and "covering" have no operational screening definition; X/C/U definitions await R5. `[RECOMMENDATION]` report 3-of-5 frameworks so no novelty conclusion depends on the threshold (Q-038, owner decision).
- **Decisions requiring review:** Q-037, Q-038, R5; all other final-confirmation-sheet lines.
- **Recommended next step:** owner answers Q-037, Q-038 and R5 (and the remaining sheet lines); then criteria v1.1.
- **Researcher decisions:** Q-028 → option (c), 2026-10-24 (D-031, conditional).

## Day 11 (cont.) — 2026-10-24 — Q-037a
- **Work completed:** proposal for the RQ5 feature/biomarker-selection definition (D-032, PROPOSED).
- **Important findings:** `[EVIDENCE]` three PubMed-verified sources support the selection/embedded-selection/selection-bias points; no verified source for VIP thresholds. `[RECOMMENDATION]` option B (data-driven subset of original variables).
- **Decisions requiring review:** R-Q037a-1 to 5; branch strategy for this task.
- **Recommended next step:** owner answers the proposal and chooses the branch strategy.
- **Researcher decisions:** _pending_

## Day 11 (cont.) — 2026-10-24 — RQ5-DECISIONS
- **Work completed:** 15 owner decisions recorded (D-032 → APPROVED — CONDITIONAL; D-033, D-034 new, conditional); `dim_feature_selection` added (optional, inactive); `rq5_coverage_group` specified.
- **Important findings:** `[EVIDENCE]` no classification status field exists (Q-039); non-metabolic 3-of-5 frameworks are E4 under criteria v1.0 (Q-040); the R5 "stated" standard differs from D-033's "applied" (Q-041).
- **Decisions requiring review:** Q-039, Q-040, Q-041, R5; authorization to push this commit (it would extend PR #4).
- **Recommended next step:** owner decision on Q-041 together with R5 (the largest blocker).
- **Researcher decisions:** Q-037a (5), Q-037b (5), Q-038 (5), 2026-10-24.

## Day 11 (cont.) — 2026-10-24 — Q-041-DECISIONS
- **Work completed:** D-035 recorded (Q-041 G1–G6, APPROVED — CONDITIONAL, inactive); RQ5 component evidence separated by stage, with erasure and completeness safeguards and a verification audit trail; coverage-group function tested but not wired.
- **Important findings:** `[EVIDENCE]` the latest-row-wins build could erase title/abstract evidence with a later blank row (now prevented by stage separation and a same-stage check); classification still has no status column (Q-039), which blocks the coverage group and full five-status enforcement.
- **Decisions requiring review:** whether to mark D-029/D-026 component wording superseded; Q-039; Q-040; authorization to commit, push and open a PR.
- **Recommended next step:** owner decision on Q-039 (classification status column).
- **Researcher decisions:** Q-041 G1–G6, 2026-10-24.

## Day 11 (cont.) — 2026-10-24 — GOV-LOG-CORRECTION
- **Work completed:** log-only corrections. The Q-041/D-035 git status is updated (committed `0eae10a`, pushed; PR #7 merged into an intermediate branch; PR #8 open to the default branch). The verified PR #3–#8 history is recorded.
- **Important findings:** `[EVIDENCE]` PRs #4, #5 and #7 were merged into intermediate branches. #4/#5 content reached the default branch through PR #6. The Q-041/D-035 work is not on the default branch until PR #8 is merged.
- **Decisions requiring review:** PR #8 (owner review and merge).
- **Recommended next step:** owner reviews and merges PR #8; then Q-039.
- **Researcher decisions:** none in this task.

## Day 11 (cont.) — 2026-10-24 — GOV-PR8-MERGE-RECORD
- **Work completed:** log-only record of PR #8's merge (`18f4b09`, 05:20:14 UTC) and post-merge validation.
- **Important findings:** `[EVIDENCE]` the merge tree equals PR #8's head `4835d3b`, so the merge introduced no extra changes. D-026/D-029 are PROPOSED and D-035 is conditional and inactive.
- **Decisions requiring review:** whether to open a PR for this log-only branch.
- **Recommended next step:** owner review; then Q-039.
- **Researcher decisions:** none in this task.

## Day 11 (cont.) — 2026-10-24 — Q-039-DECISION
- **Work completed:** D-036 recorded (Q-039 Choice 1 A, Choice 2 A; APPROVED — CONDITIONAL, inactive). `dim_classification` was added. The RQ5 coverage group is now derived in the build from confirmed statuses (null for all records; no screening data).
- **Important findings:** `[EVIDENCE]` the five-status completeness rule (D-035 G5) is now enforced; the real-data rebuild changed no ID or value. `[OPEN]` whether `lr_only` studies can be classification `yes` (Q-042).
- **Decisions requiring review:** the PR for this task; Q-042; Q-040.
- **Recommended next step:** owner review of the PR; then Q-040 or Q-042.
- **Researcher decisions:** Q-039 Choice 1 Option A and Choice 2 Option A, 2026-10-24.

## Day 11 (cont.) — 2026-10-24 — PR10-AUDIT-DECISIONS
- **Work completed:** D-037 recorded (owner Decisions A1 and B1). `rq5_coverage_provisional` is now true only when resolving `unclear` statuses could change the group. Q-042 is no longer listed as an activation condition; it stays Open.
- **Important findings:** `[EVIDENCE]` under A1, `qualified` is never provisional (4 `yes` + 1 `unclear` included); this departs from the D-034 record §5.3 example, which is superseded by addendum. `[OPEN]` Q-043: whether D-034(4)'s "flag kept" needs a separate marker.
- **Decisions requiring review:** the follow-up PR for this task; Q-043; Q-042; Q-040.
- **Recommended next step:** owner review of this PR and PR #10.
- **Researcher decisions:** Decisions A1 and B1, 2026-10-24.

## Day 11 (cont.) — 2026-10-24 — GOV-PR10-12-MERGE-RECORD
- **Work completed:** log-only record of the merges of PRs #10, #11 and #12; PR #13's description synchronized to its head `fde915a`.
- **Important findings:** `[EVIDENCE]` PR #11 was merged into `q039-dim-classification`, not the default branch; PR #12 brought its content (`e8bf189`) into the default branch (`6f57b6f`). PR #12 had not been recorded in CHANGELOG/PROMPT_LOG until this record.
- **Decisions requiring review:** whether to publish this record (push and PR); PR #13; D-039 proposal.
- **Recommended next step:** owner review of this record and PR #13.
- **Researcher decisions:** none in this task.

## Day 11 (cont.) — 2026-10-24 — Q-043-DECISION
- **Work completed:** D-038 recorded (no marker; three-subgroup reporting rule for `qualified`). PR #10 description updated (Q-042 not an activation condition; still open). Merge sequence and the `abstract_only` Option A proposal prepared.
- **Important findings:** `[EVIDENCE]` D-037 is the highest decision ID on every branch; D-038 was free. `[OPEN]` the Option A policy for `abstract_only` after a full-text assessment awaits approval.
- **Decisions requiring review:** merge authorization for PR #10/#11; branch for the D-038 commit; Option A proposal.
- **Recommended next step:** owner merge authorization, then Option A.
- **Researcher decisions:** Q-043 resolution, PR #10 description, PR sequence in principle, Option A in principle (2026-10-24).

## Day 11 (cont.) — 2026-10-24 — GOV-PR13-14-MERGE-RECORD
- **Work completed:** log-only record of the merges of PR #14 (`f7f6bb7`) and PR #13 (`694b389`), and of the conflict-resolution merge `6776eba`.
- **Important findings:** `[EVIDENCE]` the PR #13 merge equals the reviewed head `6776eba`; D-038 is on the default branch. PR #14 had not been recorded by number until this record.
- **Decisions requiring review:** whether to publish this record; D-039 proposal.
- **Recommended next step:** owner review of this record; then D-039.
- **Researcher decisions:** none in this task.

## Day 11 (cont.) — 2026-10-24 — GOV-PR15-MERGE-RECORD
- **Work completed:** log-only record of the merge of PR #15 (`5c7d455`).
- **Important findings:** `[EVIDENCE]` the PR #15 merge equals the reviewed head `4af0acb`. PR #15 had not been recorded by number until this record.
- **Decisions requiring review:** whether to commit and publish this record; the remaining activation conditions in the D-035 record §6 (Q-040; D-027 and D-024; the remaining R5/D-029 items; criteria v1.1 and protocol v0.2, frozen as the pilot's `criteria_version`; the other pilot-blocking items). Separately, open question Q-042 (not an activation condition, D-037-B1).
- **Recommended next step:** owner review of this record; then resolve the outstanding D-035 record §6 activation conditions above before D-039 is considered. D-039 is not started.
- **Researcher decisions:** none in this task.

## Day 11 (cont.) — 2026-10-24 — PROTOCOL-DRAFT-001
- **Work completed:** experimental protocol draft v0.1 (`research/methodology/experimental_protocol_v0.1_draft.md`); open questions Q-044–Q-058.
- **Important findings:** `[EVIDENCE: local descriptive check]`
  - The analytic samples are 3,088 (2017–March 2020) and 2,485 (2021–2023).
  - The candidate outcome is 65.0% and 58.8% positive, mostly from FPG 100–125 mg/dL alone.
  - The triglyceride equation units are supported as mg/dL (Q-044). The hs-CRP equation units are unresolved (Q-045).
  - None of the needed references is citable yet (protocol Appendix D).
- **Decisions requiring review:** FA-1–FA-13 in protocol §24; D-013, D-014, D-015, D-017, D-018 and D-019 (all PENDING); Q-044–Q-058.
- **Recommended next step:** researcher review of the draft, starting with FA-2 (outcome) and Q-044/Q-045; then authorize verification of the candidate references into the inventory.
- **Researcher decisions:** none in this task. The confirmed preferences in the prompt are recorded as CUP-1–CUP-11 inside the draft, not as approvals.

## Day 11 (cont.) — 2026-10-24 — PROTOCOL-DRAFT-002
- **Work completed:** protocol draft v0.1 rev. 1 (owner-authorized draft edits); data-protection `.gitignore` rules, `outputs/README.md` and `tests/data_protection/` (6 checks).
- **Important findings:**
  - `[EVIDENCE: CDC documentation]` The hs-CRP equation passage states mg/dL, while the variable and all three method manuals use mg/L, and the 2021–2023 instrument change happened "during the cycle" (Q-045, new Q-059). No conversion applied; hs-CRP removed from the primary sets.
  - A development-period-only hs-CRP sensitivity analysis needs no conversion: both 2017–2020 method manuals name the Cobas 6000.
- **Decisions requiring review:** FA-2 (preferred by the owner, **not approved**); the safeguards (AB-10 left open); Q-044, Q-045, Q-059.
- **Recommended next step:** owner review of rev. 1, and authorization to commit (the work is uncommitted); NCHS enquiry on hs-CRP units and instrument timing.
- **Researcher decisions:** the owner expressed preferences (FA-2 preferred; hs-CRP excluded) and authorized draft edits. These are recorded as preferences, not approvals.

## Day 11 (cont.) — 2026-10-24 — PROTOCOL-DRAFT-003
- **Work completed:** protocol draft rev. 2 (three wording corrections and one traceability correction); reproducible aggregate-count script; extended data-protection rules and tests; `scripts/run_checks.sh`.
- **Important findings:**
  - `[EVIDENCE: local descriptive check]` 84 of 85 draft values reproduce exactly. The median-FPG sentence had used the broader reference population (corrected: analytic samples 101 vs 100 mg/dL).
  - The negative control found an allowlist-exemption flaw in the new test (fixed).
- **Decisions requiring review:** FA-2 (preferred, **not approved**); the safeguards (AB-10 open); Q-044, Q-045, Q-059; whether to add `sh scripts/run_checks.sh` to `CLAUDE.md` §4 (owner approval needed).
- **Recommended next step:** owner review of rev. 2 and of the pushed branch; NCHS enquiry (hs-CRP); a second bibliographic source for reference verification.
- **Researcher decisions:** Option A authorization (corrections, scripts, safeguards, commit and push). No decision approved.

## Day 11 (cont.) — 2026-10-24 — PROTOCOL-EVIDENCE-001
- **Work completed:** primary-source review; protocol draft rev. 3; Q-060 and Q-061.
- **Important findings:**
  - `[EVIDENCE: CDC documentation]` The 2021–2023 instrument changes for HbA1c and the chemistry analyzer (hs-CRP, TC, HDL, TG, BIOPRO) happened **within** the cycle, with no published date or participant indicator.
  - CDC backward equations cannot yet be shown to apply to every 2021–2023 record (Q-060).
  - The ADA text could not be reached (Q-061), so the criteria remain unverified.
- **Decisions requiring review:**
  - FA-5 recommendation: unadjusted values as reference; cycle-level equations as S-09b.
  - FA-2 (still preferred, not approved).
  - Network access or PDF for the ADA article.
- **Recommended next step:** allow `diabetesjournals.org` and `doi.org`, or supply the ADA PDF; send the NCHS enquiry for Q-044, Q-045, Q-059 and Q-060.
- **Researcher decisions:** none in this task.

## Day 11 (cont.) — 2026-10-24 — GOV-D040-RULE-S
- **Work completed:** D-040 recorded (Rule S and Synthetic Verification Exemption); approved cross-references added to `CLAUDE.md` rule 13, `GOVERNANCE.md` §2 and the `logs/EXPERIMENT_LOG.md` header; `logs/SYNTHETIC_VERIFICATION_LOG.md` created (header only); Q-062 opened. Local edits only, uncommitted.
- **Important findings:** D-040 was unused (working tree and local history); D-039 stays reserved for the screening-related proposal. The K1–K4 edits are in place but uncommitted, so activation is not recorded.
- **Decisions requiring review:** whether K1–K4 count as satisfied and D-040 may be recorded as active (Q-062); whether to commit/push these edits (Q-005 open); D-002 environment pins; the synthetic test plan (Gate 2).
- **Recommended next step:** owner review of the diff; decide Q-062 and the Git step; then the environment decision and the test plan. No test may run before 2026-11-03.
- **Researcher decisions:** Rule S and exemption wording (C1 with the activation adjustment), K1–K4 mandatory, APPROVED — CONDITIONAL (inactive), D-040 and date 2026-10-24, D-039 reserved, `logs/SYNTHETIC_VERIFICATION_LOG.md`, C2–C4 wording, authorization of local documentation edits only.

## Day 11 (cont.) — 2026-10-24 — GOV-D040-ACTIVATION
- **Work completed:** owner-authorized local commit `c843230` of the 10 GOV-D040-RULE-S files; D-040 activation recorded in the decision log Status history; Q-062 closed. Not pushed; the activation edits are uncommitted.
- **Important findings:** K1–K4 present with the approved wording in `c843230` and in the working tree. "ACTIVE" is not a decision-log status, so the owner chose the existing convention: APPROVED — CONDITIONAL (active; K1–K4 met in commit c843230). The questions file lists "Open / Answered / Superseded"; Q-062 uses "Closed" as the owner authorized.
- **Decisions requiring review:** whether to commit and push the activation edits (Q-005 open); whether to add "Closed" to the questions-file status list; D-002 environment pins; the synthetic test plan (Gate 2).
- **Recommended next step:** owner review; commit/push authorization; then the environment decision and test plan. D-040 activation authorizes no synthetic verification; no run before 2026-11-03.
- **Researcher decisions:** Q-062 Option 1; one local commit; activation label Option (a); Q-062 closure; local documentation edits only.
- **Correction (same day, owner instruction):** Q-062's status label changed from "Closed" to "Answered", the documented status value. This settles the "Closed" question above; the questions-file header is unchanged.
- **Correction (same day, owner-approved wording):** Q-062 now states that K1–K4 were satisfied in the documentation committed in `c843230`, and that the activation entry was recorded afterwards, outside that commit. The 6 GOV-D040-ACTIVATION files are then committed locally (owner-authorized); not pushed.

## Day 15 — 2026-10-28 — LIT-005
- **Work completed:** PubMed G-1…G-8 (435 unique PMIDs; 395 new to the inventory; all transcription checks passed), alphaXiv search (15 listings), metadata for 394 of 395 new PMIDs; 2026-10-24 review recovered as transcript-derived notes; `LIT-005_evidence_review.md` (synthesis, comparison matrix, gap matrix, contribution recommendation).
- **Important findings:** temporal validation across national-survey cycles is established (KNHANES, NHANES), so it is not a contribution; the closest NHANES designs are A2, Casacchia 2024 and Li 2026; glucose-free laboratory classification exists outside NHANES (Guo 2026, CBC only); PubMed G-5 found no tabular metabolic study combining explanation, calibration and uncertainty, which is absence of evidence only. No reference reached `verified` (Crossref, doi.org, Europe PMC blocked; Consensus quota).
- **Decisions requiring review:** Q-063 (restore raw exports), Q-064 (verification route), Q-065 (screening scope), Q-066 (A2 full text), D-035 §6 conditions 2–6, D-016 contribution wording.
- **Recommended next step:** restore the LIT-003 exports and rebuild; decide the verification route; clear the screening conditions by 11-01.
- **Researcher decisions:** authorisation of the LIT-005 searches and file updates (2026-10-28).
- **Correction (same day, LIT-005 pre-commit review, researcher-authorised):** "395 new to the inventory" means not matched **by PMID**; inventory records without a PMID were not compared by DOI, so the rebuild's duplicate check is still needed. The screening-pilot blocker list in `LIT-005_evidence_review.md` §8 now follows `final_confirmation_sheet_LIT-004.md` ("Pilot-blocking items after confirmation") and `screening_protocol.md` B-6. Other corrections: see `logs/CHANGELOG.md`.

## Day 15 (cont.) — 2026-10-28 — LIT-005-PRESERVATION
- **Work completed:** LIT-005 commit `db84937` pushed; deterministic archive of the 39 LIT-005 raw exports created, verified (39/39 after extraction) and delivered; `preservation_status.md` LIT-005 section added.
- **Important findings:** archive SHA-256 `7b7d4674426c7581839b970cad37e21251ade0bf22d295814ac542bd7ec96ea1`. The researcher reports that the Downloads copy matches (researcher statement; not observed by the assistant). Only one copy exists outside the container, so off-device backup is still outstanding.
- **Decisions requiring review:** off-device storage for both archives; Q-063 (restore the LIT-003 archive and rebuild); Q-064 (verification route).
- **Recommended next step:** store both archives on separate private media and verify them; then authorise the LIT-003 restore and rebuild.
- **Researcher decisions:** authorisation of the push, the archive task, the documentation update and one local commit (2026-10-28).

## Day 15 (cont.) — 2026-10-28 — LIT-003-RESTORE
- **Work completed:** uploaded LIT-003 archive verified (SHA-256 exact match; 208/208 internal checksums; 205 raw files match `MANIFEST.csv` and the committed inventory); 205 raw files restored into empty destinations; `pubrecords.py verify` OK for all 244 raw exports.
- **Important findings:** the archive's `SHA256SUMS.txt` is identical to the committed copy; its `MANIFEST.csv` is the pre-LIT-005 version and its README an earlier version, so neither was used. The rebuild precondition is now met in this workspace. Off-device backup remains outstanding, and the restored files exist only in the ephemeral container.
- **Decisions requiring review:** authorise the inventory rebuild; Q-063 status (still Open); off-device storage for both archives; Q-064; D-035 §6 conditions.
- **Recommended next step:** authorise the inventory rebuild while the restored files are present in this workspace.
- **Researcher decisions:** authorisation of the verification, the restore and this documentation update (2026-10-28).

## Day 16 — 2026-10-29 — LIT-005-REBUILD
*Added 2026-10-29 in the documentation-only reconciliation; this entry was missing. Source: `logs/session_logs/2026-10-29_LIT-005-REBUILD.md`, the CHANGELOG entry and Git history.*
- **Work completed:** literature inventory rebuilt with the LIT-005 records (2,979 → 3,386; P2989–P3395), identical to the dry run; correction C2 (`Q-CN-G5@2026-10-28` recorded as `capability_probe`, not `executed`); limitation C1 documented, not fixed. Committed as `ffee9ec`.
- **Important findings:** `[EVIDENCE]` 0 existing paper IDs changed or merged; 406 new records `partially_verified`, 1 `unverified` (P3383, PMID 31314250, Q-067); all records `not_screened`; new records have no theme labels. Nothing became citable.
- **Decisions requiring review:** Q-063 status; Q-021/Q-064 verification route; D-035 record §6 conditions; off-device backup of both archives.
- **Recommended next step (as recorded then):** researcher review and commit decision; push.
- **Researcher decisions:** authorisation of the rebuild and of corrections C2 and C1; the theme mapping kept unchanged (2026-10-29).

## Day 16 (cont.) — 2026-10-29 — Branch recovery, post-recovery audit, documentation-only reconciliation
- **Work completed:** the session was moved to `claude/eloquent-mccarthy-bqtxr3` at `ffee9ec` (verified against `origin`; tree clean). A read-only governance audit was carried out. Append-only log reconciliation was done (this entry, CHANGELOG, PROMPT_LOG, a session log). No commit, push or PR.
- **Important findings:** `[EVIDENCE]` `4acfce0`, `9bbd847` and `ffee9ec` are on `origin/claude/eloquent-mccarthy-bqtxr3`; their push times are not recorded. The branch is 8 commits ahead of the default branch with no PR. D-039 is reserved (2026-10-24) and its content is not in the repository. The raw exports and `data/raw/nhanes/` are absent from this container (`verify`: 244 missing). Inventory 3,386 records; validator PASS (168); tests 69 OK.
- **Decisions requiring review:** review of this diff and whether to commit and push it; a PR for the 8 commits; D-035 record §6 conditions 2–6 and Q-065 (due 2026-11-01); Q-021/Q-064; Q-063 status; the content of D-039.
- **Recommended next step:** researcher review of the reconciliation diff; then a PR for the unreviewed commits (separate authorisation).
- **Researcher decisions:** authorisation of the branch switch, the read-only audit and the documentation-only reconciliation (2026-10-29).

## Day 16 (cont.) — 2026-10-29 — SECOND-SOURCE-ACCESS-RECHECK
- **Work completed:** state verified at `a280e01` (clean, in sync with `origin`); second-source access re-checked for 10 hosts; read-only counts of the records each verification route could reach; `environment_assessment.md` addendum; Q-068 opened.
- **Important findings:** `[EVIDENCE]` Crossref, doi.org, Europe PMC, E-utilities, PubMed/PMC web, OpenAlex, Semantic Scholar, the arXiv API and diabetesjournals.org are all refused by the network policy (CONNECT 403, 14:50Z). 2,282 of 3,334 `partially_verified` records have a PMCID; 964 PubMed records, including A2 (`P0303`), do not. The 14 `verified` records rest on web-search URL agreement, which `search_strategy.md` §7 does not name as a second source (Q-068). `[OPEN]` No independent bibliographic index is reachable from this environment.
- **Decisions requiring review:** Q-021/Q-064 (verification route, including the network change); Q-068; Q-036; Q-065 (due 2026-11-01); D-035 record §6 conditions 2–6.
- **Recommended next step:** researcher decision on Q-021/Q-064/Q-068, or allow-listing `api.crossref.org` and `www.ebi.ac.uk`; then a scoped verification task for the citation-priority records (`LIT-005_evidence_review.md` §10).
- **Researcher decisions:** authorisation to resume Stage B with one bounded non-screening task (2026-10-29).

## Day 16 (cont.) — 2026-10-29 — RESEARCH-AMBITION-D041
- **Work completed:** existing governance inspected for the publication ambition; `CLAUDE.md` §1a (ambition, journal criteria, rules 14–17) and a README "Ambition" paragraph added; D-041 recorded as PROPOSED.
- **Important findings:** `[EVIDENCE]` most of the requested standards already exist (`GOVERNANCE.md` §1–2; `research_integrity.md` §1–11; D-016, D-018, D-020), but the journal-level ambition, the journal-selection criteria and the four rules were not explicit. `[OPEN]` The 2026-11-24 manuscript target (CUP-11) may conflict with the quality bar; `GOVERNANCE.md` §2 forbids skipping stages to meet the deadline.
- **Decisions requiring review:** D-041 (approve, amend or reject); D-011/D-022; the schedule (D-001) in view of the ambition; the six SECOND-SOURCE-ACCESS-RECHECK files and this change (commit decision).
- **Recommended next step:** screening-activation decision brief (D-035 record §6 conditions 2–6; Q-065, due 2026-11-01).
- **Researcher decisions:** instruction to state the ambition and record D-041 as PROPOSED (2026-10-29).

## Day 16 (cont.) — 2026-10-29 — SCREENING-ACTIVATION-BRIEF
- **Work completed:** decision brief for the D-035 record §6 conditions (`research/reviews/screening_activation_decision_brief_D035.md`); Q-069 opened.
- **Important findings:** `[EVIDENCE]` conditions 2–6 unmet: Q-040; D-024/D-027 approval; R5/D-029 items; criteria v1.1 and protocol v0.2 (not written); the other pilot-blocking items of `final_confirmation_sheet_LIT-004.md`. All need researcher decisions first; none needs a network change; the rebuild and arXiv spot-check need the raw exports restored (Q-063). `[HYPOTHESIS]` A complete, gate-compliant manuscript by 2026-11-24 is unlikely. `[OPEN]` Q-069 (gate order).
- **Decisions requiring review:** Q-065 (due 2026-11-01); D-001/Q-013/Q-058/Q-069 (schedule); R5 and D-029; Q-040; D-024, D-027, D-028, Q-035; v1 Items 6–9, 13–15; Q-036; Q-063 upload; Q-021/Q-064/Q-068 (citation route); commit decision for the three uncommitted tasks.
- **Recommended next step:** researcher decisions in the order of the brief's §8, starting with Q-065 and the schedule.
- **Researcher decisions:** instruction to prepare the brief, documentation only (2026-10-29).

## Day 16 (cont.) — 2026-10-29 — Q-069-RESOLUTION
- **Work completed:** read-only analysis of Q-069; D-042 recorded as PROPOSED; Q-069 note; protocol draft revision 4 (§23 dependency-ordered schedule and new fallback; §26 prerequisites for D-017–D-019, AB-13, AB-7 change, D-016 removed from "Not blocking training").
- **Important findings:** `[EVIDENCE]` no repository source explicitly permits or forbids parallel stages. The evidence required for D-017 (approved D-016) and D-018 (most-used methods in included RQ1 studies) already made training depend on Stages C and D; protocol revision 3's "D-016 not blocking training" line was inconsistent with that. Two contradictions in the proposal were corrected before editing (Rule S execution timing, D-040 (7); D-014 placement).
- **Decisions requiring review:** explicit approval, amendment or rejection of D-042 (then Q-069 can be marked Answered); protocol revision 4; D-001/CUP-11 (11-24 target); the commit decision.
- **Recommended next step:** researcher review of D-042 and protocol revision 4.
- **Researcher decisions:** in-principle approval of the Q-069 resolution; approval of the recording treatment and protocol edits for preparation (2026-10-29).

## Day 16 (cont.) — 2026-10-29 — D-042-APPROVAL
- **Work completed:** researcher approval of D-042 recorded; Q-069 marked Answered and linked to D-042; protocol draft revision 5 (references to D-042 updated from "proposed" to "approved").
- **Important findings:** `[EVIDENCE]` D-042 is the first approved rule on stage order: the Stage C and Stage D gates must both pass before D-017, D-018 and D-019 are approved and before any real-data training. Neither gate has passed. Precedent for recording approvals is mixed (D-032: history only; D-042: row cells updated at the owner's instruction, text unchanged).
- **Decisions requiring review:** this diff and the commit decision; D-001/CUP-11 (11-24 target); the screening-activation decisions (`screening_activation_decision_brief_D035.md` §8), starting with Q-065 (due 2026-11-01); Q-021/Q-064/Q-068.
- **Recommended next step:** researcher decisions on Q-065 and the schedule (D-001, Q-013, Q-058).
- **Researcher decisions:** explicit approval of D-042 as written (2026-10-29).

## Day 16 (cont.) — 2026-10-29 — Q-065-DECISION-PACKAGE
- **Work completed:** read-only audit; metadata-only priority-strand counts with an independent check; `research/reviews/Q-065_decision_package.md` (scope options, schedule options, recommendation); audit-trail reconciliation of the commits and pushes made on 2026-10-29.
- **Important findings:** `[EVIDENCE]` priority strand union 1,044 records (194 / 743 / 120; overlaps 10 / 0 / 3). D-018's documented evidence ("methods most used in the included RQ1 studies") covers Q-PM-01, Q-PM-02 and Q-PM-03, but the priority strand contains only Q-PM-02; priority + remaining RQ1 strands = 1,470. No screening rate has been measured; all durations are `[HYPOTHESIS]`. `[OPEN]` Q-065 (due 2026-11-01), Q-001, Q-002.
- **Decisions requiring review:** Q-065 scope (Options 1–3); Q-002 (biomarker scope), which decides whether Q-PM-01/Q-PM-03 are needed; schedule (D-001, Q-013, Q-058, CUP-11); the commit decision.
- **Recommended next step:** researcher decisions on Q-002 and Q-065 by 2026-11-01; schedule S1 + S2 (interim deliverable on 11-24; D-001 revised after the pilot).
- **Researcher decisions:** instruction to prepare the package, documentation only (2026-10-29).

## Day 16 (cont.) — 2026-10-29 — SCOPE-SCHEDULE-DECISIONS
- **Work completed:** owner decisions recorded: D-043 (Q-002: both metabolomics/lipidomics and routine clinical chemistry, as distinct categories, literature-review scope only); D-044 (Q-065: Option 3, 1,470 unique records, inactive until screening activation); D-045 (2026-11-24 kept as an interim deliverable without promised model results; schedule revised after the pilot).
- **Important findings:** `[EVIDENCE]` 1,470 reproduced independently (`jq`; CSV five-set inclusion–exclusion): 1,044 + 399 + 44 − 17. One pending dedup pair has both members in scope (count could become 1,469). Protocol CUP-11/§23 and `screening_criteria.md` §2.2 still carry pre-decision wording.
- **Decisions requiring review:** this diff and the commit decision (together with the Q-065 package); protocol revision for CUP-11/§23; remaining screening-activation items (D-035 record §6 conditions 2–6, including Q-001, Q-033, Q-035); Q-021/Q-064/Q-068.
- **Recommended next step:** researcher decisions on the remaining D-035 record §6 items (`screening_activation_decision_brief_D035.md` §8, steps 2–6).
- **Researcher decisions:** Q-002, Q-065 (Option 3) and the schedule decision (2026-10-29).

## Day 17 — 2026-10-30 — D-051-GOVERNANCE-APPROVAL
- **Work completed:** D-051 recorded: the owner's approval of the exact `GOVERNANCE.md` §2 Rule S sentence added in `c843230`; one Status-history row; task logs.
- **Important findings:** `[EVIDENCE]` the sentence is byte-identical at `c843230` and `0c85634`; D-051 was unused on every branch and in history before recording.
- **Decisions requiring review:** this change set and the commit decision; the push to the PR-1 branch; the PR #17 description update; the NHANES acknowledgement and D-040 comments; proposals on D-040 scope, "F-A software" and NHANES-derived values (not approved).
- **Recommended next step:** researcher review of this change set; if authorised, commit on the PR-1 branch (Option A); PR #17 to be merged with a merge commit, not a squash.
- **Researcher decisions:** approval of the exact `GOVERNANCE.md` §2 sentence (2026-10-30), limited to that sentence: "This approval applies only to that sentence. It does not amend D-040 or authorize test planning, test code, environment specification or creation, package installation, synthetic verification, experiments, or model training. Each such activity requires separate explicit authorization."

## Day 17 (cont.) — 2026-10-30 — LIT-PRESERVATION-V1-V5
- **Work completed:** both raw-export archives verified (archive checksums; LIT-005 listing and safety checks; per-file checks); all 244 raw files restored into `raw_exports/` with exclusive create; `pubrecords.py verify` OK; LIT-005 per-file listing and inventory created; preservation record and Q-063 status note updated.
- **Important findings:** `[EVIDENCE]` 205/205 LIT-003 and 39/39 LIT-005 files match `MANIFEST.csv`; first restoration from the LIT-005 archive succeeded; the LIT-003 archive's README and MANIFEST equal the `b48adde` versions. `[OPEN]` no backup on a separate physical device; Google Drive not approved as project storage; restored files exist only in this workspace.
- **Decisions requiring review:** this change set and the commit decision; Google Drive approval; a separate-device backup; Q-063 closure.
- **Recommended next step:** researcher review of the diff; then a commit if authorised.
- **Researcher decisions:** authorisation of phases V1, V2+V3, V4 and V5 (2026-10-30); Google Drive check reported by the researcher (not observed).

## Day 17 (cont.) — 2026-10-30 — LIT-PRESERVATION-GDRIVE
- **Work completed:** the researcher-reported Google Drive approval and the Drive folder recorded in `preservation_status.md` and the Q-063 status note.
- **Important findings:** `[EVIDENCE]` (researcher-reported) explicit approval of the researcher's personal Google Drive for research archives; both archives in a private Drive folder. `[OPEN]` approver ("project owner or supervisor"), date, scope and conditions not recorded; no backup on a separate physical device.
- **Decisions requiring review:** supply the missing approval details; whether a DECISION_LOG entry is wanted; whether the Drive copy meets the off-device requirement or a physical-device backup is still required; Q-063 closure.
- **Recommended next step:** researcher review of the diff; then a commit if authorised.
- **Researcher decisions:** Google Drive approval reported (2026-10-30); details pending.

## Day 17 (cont.) — 2026-10-30 — Q-011-OPTION-B and SCREENING-READINESS-RECHECK
- **Work completed:** Q-011 option (b) and the researcher-reported Drive-copy hashes recorded; screening readiness re-checked against D-035 §6 (brief §11).
- **Important findings:** `[EVIDENCE]` (researcher-reported) Drive copies' SHA-256 equal the recorded values. `[EVIDENCE]` D-035 §6 conditions 2–6 unmet; screening not authorised; 3,386 records `not_screened`. `[OPEN]` approval date and wording; D-010 confirmation; a 2026-11-02 interim deliverable is not recorded (D-045 retains 2026-11-24).
- **Decisions requiring review:** D-010 confirmation; R5/D-029 and Q-032; Q-040; D-024/D-027/D-028/Q-035; v1 Items 6–9, 13–15 and the pilot screener; Q-036; Q-021/Q-064/Q-068.
- **Recommended next step:** one researcher decision session on brief §11.3 steps 1–4.
- **Researcher decisions:** Q-011 option (b) selected (2026-10-30); D-010 confirmation pending.

## Day 17 (cont.) — 2026-10-30 — D-010-APPROVAL
- **Work completed:** D-010 recorded as APPROVED under Q-011 option (b); Q-011 Answered.
- **Important findings:** `[EVIDENCE]` explicit researcher approval of D-010 (2026-10-30). `[OPEN]` date and wording of the WhatsApp approval; who "the project owner" is; PRESERVED status (researcher decision); Q-063.
- **Decisions requiring review:** PRESERVED status; Q-063 closure; brief §11.3 steps 1–4.
- **Recommended next step:** researcher review of the change set; then a commit if authorised.
- **Researcher decisions:** D-010 approved (2026-10-30).

## Day 17 (cont.) — 2026-10-30 — SCREENING-PREREQ-DECISIONS
- **Work completed:** researcher selections recorded (D-055–D-057, D-027 limited, D-008; Q-036 answered); recommendations and approval request in `screening_prerequisites_decision_package.md`.
- **Important findings:** `[EVIDENCE]` D-035 §6 conditions 1–2 met; 3–6 unmet. `[RECOMMENDATION]` the R5 "RQ5 ambiguity" line needs a MODIFY to align with D-031, D-034, D-035 G2 and D-055 (route to full text at ≥ 3 of 5 counting `unclear`), and A-2's E4 clause needs a MODIFY for D-055.
- **Decisions requiring review:** the §5 approval request (Q-035, D-028, D-029/R5, Q-032, D-024, Q-007, D-025, A-1–A-6); commit and push.
- **Recommended next step:** owner answers to the §5 approval request; in parallel, the authorised arXiv spot-check.
- **Researcher decisions:** Q-040, Q-001, Q-033, D-027, Q-036 (a+b), D-008 (2026-10-30).

## Day 17 (cont.) — 2026-10-30 — SCREENING-PREREQ-DECISIONS-2
- **Work completed:** delegated decisions recorded (D-058–D-060 and status changes); arXiv spot-check run; criteria v1.1 and protocol v0.2 drafted.
- **Important findings:** `[EVIDENCE]` arXiv spot-check 25/25 match (5 files). `[EVIDENCE]` inside the D-044 scope the D-025 pilot allocation cannot be applied (no arXiv/web records; Q 8, D 13; 173 untagged) → Q-073. `[OPEN]` OPEN-1 flag name, OPEN-2 tier; implementation and rebuild; MANIFEST recording of the spot-check.
- **Decisions requiring review:** freeze of v1.1/v0.2 (with OPEN-1, OPEN-2, Q-073); authorisation for implementation, rebuild and `set-check`; Q-034; commit and push.
- **Recommended next step:** researcher review of the two drafts and Q-073.
- **Researcher decisions:** delegated selection of the recommended options (2026-10-30).

## Day 17 (cont.) — 2026-10-30 — SCREENING-PREREQ-DECISIONS-3
- **Work completed:** D-061 (flag name) and D-062 (tier rule) recorded; Q-073 recommendation; spot-check written to `MANIFEST.csv`; drafts updated and cross-checked.
- **Important findings:** `[EVIDENCE]` `set-check` changes only the target manifest row (dry run). `[EVIDENCE]` all cited decision IDs exist. `[OPEN]` Q-073; a rebuild will change the D-044 inventory hash; P2870/P2941 may become `verified` at the next build (Q-068).
- **Decisions requiring review:** Q-073; authorisation to commit, then to implement and rebuild; v1.1/v0.2 freeze.
- **Recommended next step:** approve Q-073 and authorise a commit.
- **Researcher decisions:** none new (delegated selection applied to OPEN-1/OPEN-2).

## Day 17 (cont.) — 2026-10-30 — Q-073-DECISION
- **Work completed:** D-063 recorded; 17-file preservation commit.
- **Important findings:** `[EVIDENCE]` allocation fits every stratum (Q 7 of 8 eligible; D 7 of 13).
- **Decisions requiring review:** implementation and rebuild authorisation; freeze of v1.1/v0.2.
- **Recommended next step:** authorise the implementation task (scope list first).
- **Researcher decisions:** D-063 approved (2026-10-30); commit and push authorised.
