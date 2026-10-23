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

