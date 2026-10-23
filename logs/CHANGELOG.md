# Changelog

## P001 — 2026-10-14 — Project workspace and governance setup

**Created**
- `README.md`, `GOVERNANCE.md`, `.gitignore`
- `research/setup/environment_assessment.md`
- `research/literature/paper_inventory.csv` (header only), `research/literature/paper_inventory.json` (empty list + schema note), `research/literature/paper_inventory.schema.json`
- `research/methodology/design_decisions.md`
- `research/reviews/daily_review_log.md`, `research/reviews/unresolved_questions.md`
- `logs/CHANGELOG.md`, `logs/PROMPT_LOG.md`, `logs/DECISION_LOG.md`, `logs/EXPERIMENT_LOG.md`
- `logs/session_logs/2026-10-14_P001.md`

**Modified / deleted**: none (repository was empty).

**Not created yet (by design, created progressively)**: `search_strategy.md`, `literature_review.md`,
`research_gap_matrix.md`, `research_questions.md`, `hypotheses.md`, `proposed_framework.md`,
`experimental_protocol.md`.

**Validation**: see session log; JSON files parse, CSV header matches schema fields.

**Commit**: `6bf10d9`

## LIT-001 — 2026-10-14 — Literature-search strategy (Stage A)

**Created**
- `research/literature/search_strategy.md` — review type, capability assessment, concept blocks, per-source queries, collection/dedup/screening/verification/analysis procedures, limitations (v1.0 draft)
- `research/literature/search_queries.csv` — 98 rows: 12 capability probes, 30 count-only PubMed pilots, 56 planned queries (15 PubMed, 6 Europe PMC, 5 Semantic Scholar, 3 Crossref, 4 Google Scholar, 10 Consensus, 5 arXiv, 5 publisher-site, 3 repository)
- `research/literature/screening_criteria.md` — common and RQ-specific eligibility criteria, exclusion codes, decision procedure, tiers (v1.0 draft)
- `scripts/literature/validate_search_queries.py` — CSV integrity and PubMed-connector-limit checks

**Modified**
- `research/reviews/unresolved_questions.md` — Q-001/Q-002/Q-003 updated; Q-006–Q-010 added
- `research/literature/paper_inventory.schema.json` — `source_db` enum extended; `query_id` → `query_ids`; added `pmcid`, `publication_type`, `rq_tags`, `tier`, `scope_flags` (schema still PROPOSED; inventory empty)
- `research/literature/paper_inventory.csv` — header regenerated (32 fields)
- `logs/DECISION_LOG.md` — D-003 marked SUPERSEDED (was only proposed); D-005–D-009 proposed
- `logs/PROMPT_LOG.md`, `logs/CHANGELOG.md`, `research/reviews/daily_review_log.md`, `README.md`

**Deleted**: none.

**Validation**
- `python3 -I scripts/literature/validate_search_queries.py research/literature/search_queries.csv` → PASS (98 rows; all 15 planned PubMed queries ≤ 20 operators and ≤ 5 wildcards; each matches its pilot except the date clause)
- Inventory schema check (jsonschema) → PASS; empty JSON validates; CSV header matches 32 fields
- `[edat]` snapshot syntax accepted by the PubMed connector (PILOT-E01, PILOT-E02)

**Not done (by instruction)**: no records collected; no framework proposed.

**Commit**: `5621dc9`

## LIT-002 — 2026-10-14 — Publication collection and verification workflow

**Created**
- `scripts/literature/pubrecords.py` — raw-export registration (sha256 manifest), parsers (PubMed connector JSON, E-utilities efetch XML, structured transcriptions), source records with verbatim originals, deduplication (identifiers → title rules → fuzzy flags; identifier conflicts never merged), conflict-preserving merge, stable paper IDs (append-only registry), automatic verification status, transcription spot-check, abstract-free index, build report; CLI `register | build | verify | spot-check | set-check`
- `scripts/literature/fetch_pubmed_eutils.py` — official NCBI E-utilities client (rate-limited, `tool` param, optional `NCBI_EMAIL`/`NCBI_API_KEY` from environment, raw saving + registration, no overwrite)
- `research/literature/schemas/source_record.schema.json`, `research/literature/schemas/publication_record.schema.json`
- `research/literature/collection_workflow.md` — routes, access conditions, transcription controls, record fields, rules, alternatives for unavailable databases, Git policy, test coverage
- `research/literature/raw_exports/README.md`
- `tests/literature/test_pubrecords.py` — 19 unit tests (synthetic fixtures, clearly labelled)
- `CLAUDE.md` — pointer to GOVERNANCE.md (proposed, D-011)
- `logs/session_logs/2026-10-14_LIT-002.md`

**Moved**
- `research/literature/paper_inventory.schema.json` → `research/literature/schemas/paper_inventory.schema.json` (content unchanged)

**Modified**
- `.gitignore` — raw literature exports and abstract-bearing record files excluded (public repository; D-010)
- `research/literature/search_strategy.md` — v1.0.1: schema path, pointer to workflow doc, §9 task labels (queries and criteria unchanged)
- `research/reviews/unresolved_questions.md` — Q-003 (eutils priority), deadlines re-labelled; Q-011, Q-012 added
- `logs/DECISION_LOG.md` — D-010, D-011, D-012 proposed
- `logs/PROMPT_LOG.md`, `logs/CHANGELOG.md`, `research/reviews/daily_review_log.md`, `README.md`

**Deleted**: none.

**Validation**
- `python3 -I -W error::ResourceWarning -m unittest discover -s tests/literature -v` → 19 tests, OK
- `python3 -I scripts/literature/validate_search_queries.py research/literature/search_queries.csv` → PASS (98 rows)
- Schema meta-validation of the three schemas → OK
- Dedup benchmark (3,405 synthetic records, not committed) → 1.6 s, 5/5 planted near-duplicates flagged
- Two defects found by testing and fixed before commit: (1) the ID registry could give an unmerged identifier-conflict record the same paper ID (silent re-merge); (2) fuzzy matching was quadratic in large author blocks (~40 s for 400 records) → pre-filters added

**Not done**: no real search run; no publications collected; no live API test (hosts blocked).

**Commit**: `eee92c1`

## BIO-001 — 2026-10-23 — Establish research governance and project logbook

**Prompt objective**: prepare the existing repository for rigorous, reproducible research.
Inspect the repository, establish or update the governance files, change/prompt/decision logs
and review logs, and prepare the literature research plan and research integrity protocol.
No models, no literature search, no novelty assumption.

**Initial state**: clean tree; 29 tracked files from P001, LIT-001 and LIT-002 (all from
2026-10-14); no PRs; single remote branch `claude/happy-hawking-rxptfv`. Details in
`logs/session_logs/2026-10-23_BIO-001.md`.

**Completed**
- `CLAUDE.md` expanded from a pointer into persistent instructions with all rules listed in the BIO-001 prompt
- `README.md` rewritten: working title, objective, provisional research question (`[OPEN]`), stage table with actual status, integrity principles, repository layout, workflow. It states explicitly that the gap and methodology are not finalised and that no performance is claimed
- Decision log: `PENDING` status added; research-scope decisions D-013–D-020 (prompt labels D001–D008), all PENDING with evidence required, rationale and approval status; process decisions D-021 (PR per task, no auto-merge) and D-022 (CLAUDE.md scope), both PROPOSED
- `research/literature/research_plan.md`: overview of themes A–F mapped to RQ1–RQ6; databases with **tested** access status; concepts; preliminary criteria; verification; extraction; gap-assessment strategy; deliverables; limitations. No references cited
- `research/methodology/research_integrity.md`: 13-section protocol (datasets, provenance, raw-data preservation, leakage, in-fold preprocessing, run logging, negative results, statistics, traceability, exploratory vs final, external-validation claims, clinical-validity claims, compliance check)
- Review log entry for Day 10; unresolved questions Q-013–Q-018

**Created**
- `research/literature/research_plan.md`
- `research/methodology/research_integrity.md`
- `logs/session_logs/2026-10-23_BIO-001.md`

**Modified**
- `CLAUDE.md`, `README.md` — reasons above
- `logs/DECISION_LOG.md` — new entries added. Only the status cells of the unapproved proposals D-004 and D-011 were changed (to SUPERSEDED), following the D-003 precedent
- `research/methodology/design_decisions.md` — outdated sentence ("D-001 to D-004 … only") corrected; pointer to D-013–D-020 and the integrity protocol
- `research/reviews/daily_review_log.md`, `research/reviews/unresolved_questions.md` — entries appended
- `logs/CHANGELOG.md`, `logs/PROMPT_LOG.md` — this entry

**Deleted**: none. **Not modified (deliberately)**: `GOVERNANCE.md` (changes need an approved decision); all literature-design files, scripts and tests.

**Reasons for important changes**
- Decision IDs D001–D008 from the prompt would clash with the existing D-001–D-008 → numbered D-013–D-020, with a mapping column (Q-014).
- Branch: the suggested `research/bio-001-project-governance` was not used. The session may only push to `claude/sweet-brahmagupta-urw7l1`.
- `research_plan.md` is an overview, not a second strategy, to avoid conflicting duplicates of `search_strategy.md`.

**Validation (actually performed, 2026-10-23)**
| Check | Command / method | Outcome |
|---|---|---|
| Required files exist | `test -e` for the 9 files + `logs/session_logs/` | All present |
| Duplicate/conflicting governance docs | `find` for *claude*, *readme*, *changelog*, *prompt_log*, *decision*, *integrity*, *plan* | One of each. `raw_exports/README.md` and `design_decisions.md` are distinct, non-conflicting files |
| Existing work preserved | `git status --short`; `git diff --diff-filter=D` | 6 modified, 3 new, 0 deleted. Previous log entries retained (appended only, apart from the two superseded status cells) |
| README unsupported claims | `grep -iE 'outperform\|superior\|state-of-the-art\|novel\|accuracy\|auc\|achiev\|validated\|clinical'` | Only disclaimer and principle sentences matched. One wording changed from "Data leakage is prevented" to "must be prevented", so it no longer reads as an achieved fact |
| Fabricated references in plan/protocol/README/CLAUDE | `grep -E 'et al\|10.NNNN/\|doi.org\|PMID\|(19xx\|(20xx'` | No reference patterns; only task dates matched |
| Pending decisions marked | `grep` D-013–D-020 rows with `\| PENDING \|`; `grep APPROVED` | 8/8 PENDING, 8 "Not approved"; no decision has APPROVED status |
| Unit tests | `python3 -I -m unittest discover -s tests/literature` | Ran 19 tests, OK (same as baseline) |
| Query table | `validate_search_queries.py research/literature/search_queries.csv` | PASS: 98 rows (unchanged) |
| Network | `curl` to 5 bibliographic APIs | All blocked (HTTP 000) |
| Final diff inspected | `git diff --stat`, `git diff` | Reviewed before commit |
| Completed vs planned | Manual review of this entry | Planned items appear only under research_plan §9, the decision log and unresolved questions, never as completed |

Not performed: Markdown rendering check on GitHub; no literature search (by instruction).

**Errors / warnings**: none from the commands. Warning: the project is behind the proposed schedule (Q-013).

**Unresolved questions**: Q-013–Q-018 added; Q-001–Q-012 remain open.

**Commit**: `fc0c79b` (work); this line added in a follow-up commit.

**Pull request**: #1 — https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/1 (base `claude/happy-hawking-rxptfv`, head `claude/sweet-brahmagupta-urw7l1`; open, not merged)
