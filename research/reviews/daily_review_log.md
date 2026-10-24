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
