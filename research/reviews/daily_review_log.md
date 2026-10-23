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
