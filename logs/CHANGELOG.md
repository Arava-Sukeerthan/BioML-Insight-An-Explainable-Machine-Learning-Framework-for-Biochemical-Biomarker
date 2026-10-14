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

**Commit**: see `logs/session_logs/2026-10-14_LIT-002.md`.
