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

## BIO-001-REVIEW — 2026-10-23 — Review and correction of the BIO-001 pull request (#1)

**Prompt objective**: review PR #1 without merging it. Check whether superseding D-004/D-011 was
justified and restore their status if not; keep the eight BIO-001 decisions traceable without
ambiguous IDs; check that the README stage status and the review log match the repository; log
every correction; validate; update the existing PR.

**Finding on D-004 / D-011**: **not justified.** The decision log allowed marking "a proposal replaced before approval"
as SUPERSEDED, and LIT-001 had done so for D-003. In BIO-001, however:
(a) D-004 and D-011 were awaiting explicit researcher answers (Q-005, Q-012);
(b) their replacements D-021/D-022 were themselves only PROPOSED;
(c) the change therefore settled a choice between two open proposals without the researcher.
CLAUDE.md rule 7 says an assistant recommendation is not approval, and GOVERNANCE.md §1.9 forbids silent changes to decisions. The BIO-001 changelog
entry recorded the change, so it was not hidden, but it still pre-empted the researcher.

**Changes and reasons**
| File | Change | Reason |
|---|---|---|
| `logs/DECISION_LOG.md` | D-004 and D-011 rows restored verbatim from `330d3fd` (status PROPOSED) | Restore the status the researcher had not yet decided on |
| `logs/DECISION_LOG.md` | D-021/D-022 reworded from "Supersedes …" to "**Alternative to** D-004/D-011 … superseded only if approved" | Both options stay open until the researcher chooses |
| `logs/DECISION_LOG.md` | New "Status history" table (D-003 in LIT-001; D-004/D-011 changed in BIO-001; restored in BIO-001-REVIEW) and a clarified rule: SUPERSEDED only after the replacement is approved or the proposal is withdrawn | Preserve the decision history, including the erroneous change, and prevent a repeat |
| `logs/DECISION_LOG.md` | Second column renamed "BIO-001 prompt item (cross-reference only)"; values `D001`→`BIO-001/D001` … `D008`→`BIO-001/D008`; explicit mapping table including the existing D-001–D-008 that each must not be confused with | Bare `D001` could be read as `D-001`. Existing IDs D-001–D-022 kept unchanged; 22 unique IDs |
| `CLAUDE.md` | Rule 10 extended: do not change the status of an open proposal; record conflicting proposals as alternatives; cite decisions only by `D-0nn` | Make the corrected practice persistent |
| `README.md` | Status: "no literature search has been run" → "no search executed; only capability probes and count-only pilot queries (2026-10-14)" | Accuracy: 12 probes and 30 count-only pilots exist in `search_queries.csv` |
| `README.md` | Stage table rebuilt with the GOVERNANCE.md §3 day mapping (marked "D-001, not approved") and actual status per stage; Stage A "gate not passed"; Stage B "not started, tooling prepared (LIT-002)" | The BIO-001 table placed Stage F wholly after Day 20, which contradicts GOVERNANCE.md §3 (feasibility from Day 13, acquisition Days 17–20). It also did not state that the Stage-A gate has not been passed |
| `research/reviews/daily_review_log.md` | BIO-001 entry: "BIO-001 labels D001–D008" → "BIO-001/D001–D008" cross-reference wording; new BIO-001-REVIEW entry | Unambiguous references; record the review |
| `research/reviews/unresolved_questions.md` | Q-005, Q-012 updated (choose D-004 vs D-021, D-011 vs D-022); Q-014 wording; Q-019 added (dataset timing: D-001 vs BIO-001 prompt) | Expose the choices to the researcher instead of resolving them |
| `logs/CHANGELOG.md`, `logs/PROMPT_LOG.md`, `logs/session_logs/2026-10-23_BIO-001-REVIEW.md` | This entry, a prompt-log row and detail block, a session log | Logging requirement |

**Not changed (deliberately)**: the provisional research question (README and `research_plan.md`); D-013–D-020 content and status;
`GOVERNANCE.md`; search strategy, queries and criteria; scripts and tests. The earlier BIO-001 entries in this changelog, the prompt
log and the BIO-001 session log are kept as written (history), including the bare `D001–D008` wording, which appears there only in an
explicit "recorded as D-013–D-020" mapping. No literature collected, no models.

**Deleted**: none.

**Validation (actually performed, 2026-10-23)**
| Check | Outcome |
|---|---|
| D-004, D-011 rows vs `330d3fd` (`diff`) | Identical; status PROPOSED |
| All rows D-001–D-012 vs `330d3fd` | Identical |
| Decision IDs unique (first column) | 22 rows, 0 duplicates |
| Mapping | 8/8 mapping-table rows; 8/8 D-013–D-020 rows carry `BIO-001/D00n` and status PENDING |
| APPROVED in any status cell | 0 |
| Bare `D00n` outside `BIO-001/` form | Only in the historical BIO-001 changelog, prompt-log and session-log text, each in an explicit mapping statement |
| README facts | 0 tracked `records/` or `screening/` files; inventory 0 records; 0 `executed` query rows (12 probes, 30 pilots, 56 planned); no `data/` or `src/`; experiment log empty → "not started" for Stages B–J and "no search executed" confirmed. Stage days match GOVERNANCE.md §3 |
| Research question unchanged | `git diff` on the RQ block since `da3aa35`: no change. Strategy, criteria, queries and GOVERNANCE.md: 0 diff lines since `330d3fd` |
| Unit tests | `python3 -I -m unittest discover -s tests/literature` → Ran 19 tests, OK |
| Query table | `validate_search_queries.py` → PASS: 98 rows |
| Deletions | none |

**Errors / warnings**: none from the commands.

**Commit / PR**: corrections commit `c9f1374` (hash added in a follow-up commit); pushed to the existing PR #1
(https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/1). No new PR; not merged.

## LIT-003 — 2026-10-23 — Execute verified scholarly literature searches

**Prompt objective**: run the stored search strategy on the accessible sources; preserve
provenance; collect, deduplicate and verify records; build the evidence table and reports.
No screening, gap analysis, novelty claim or models.

**Governance**: the queries were executed unchanged (only `{RUN_DATE}` = 2026/10/23 was substituted)
under the researcher's LIT-003 instruction. D-005/D-006/D-007/D-010 remain PROPOSED, and approval is
requested (Q-022). No approved decision was changed. The branch was restarted from the default branch
after PR #1 had been merged.

**Completed**
- Access testing: 19 probes (`access_report.md`, `search_queries.csv` LIT003-PROBE-01…19).
- PubMed Q-PM-01…15 executed in full: 3,413 hits, 2,866 unique PMIDs, all complete. PMID transcription checked by an independent re-fetch: 15/15 identical. Metadata for all PMIDs (144 verbatim connector responses).
- arXiv (alphaXiv) Q-AX-01…05: 76 records. Web Q-WS-01…05 + Q-RP-03: 54 records.
- Not run: Consensus (quota), Europe PMC, Crossref, Semantic Scholar, repository APIs (blocked), Google Scholar (manual).
- Build: 3,543 source records → 564 exact identifier duplicates removed → **2,979 publications**. 15 pairs (30 records) flagged for manual dedup review. 3 retracted records flagged.
- Verification: 14 verified, 2,928 partially verified, 36 unverified, 1 needs review.
- Evidence table (`paper_inventory`), 2,979 rows: all extraction fields `REQUIRES FULL-TEXT REVIEW`. 234 mechanical full-text candidates.

**Created**
- `research/literature/access_report.md`, `collection_summary.md`, `search_execution_register.md` (generated), `verification_report.md` (generated), `fulltext_review_candidates.csv` (generated)
- `research/literature/raw_exports/MANIFEST.csv` (205 rows; the raw files themselves are git-ignored)
- `research/literature/records/`: `build_report.json`, `collection_stats.json`, `dedup_review.csv`, `paper_id_registry.csv`, `publications_index.csv` (git-ignored, not committed: `source_records.jsonl`, `publications.jsonl`)
- `scripts/literature/make_literature_reports.py`
- `logs/session_logs/2026-10-23_LIT-003.md`

**Modified**
- `scripts/literature/pubrecords.py` — `CHECK-` exclusion, `check_search` / `check-search`, abstract-placeholder handling. Reason: transcription control for search pages; correct abstract availability
- `tests/literature/test_pubrecords.py` — 3 tests added
- `research/literature/search_queries.csv` — 41 `executed` rows + 19 LIT-003 probe rows appended (existing rows unchanged)
- `research/literature/schemas/paper_inventory.schema.json` — evidence fields, sentinels, `needs_review`; `calibration_or_uncertainty` split into `calibration_methods` / `uncertainty_methods`. Reason: the LIT-003 evidence items; the schema was PROPOSED and the inventory empty (D-024)
- `research/literature/paper_inventory.csv/.json` — populated (were empty)
- `research/literature/collection_workflow.md` (v1.1: status, §5 heading, new §9), `raw_exports/README.md`, `research_plan.md` (status row), `README.md` (status, Stage B)
- `logs/DECISION_LOG.md` (D-023, D-024 proposed; note on D-005–D-010), `research/reviews/unresolved_questions.md` (Q-011 marked urgent; Q-020–Q-025), `research/reviews/daily_review_log.md`, `logs/PROMPT_LOG.md`, this file

**Deleted**: none. `search_strategy.md` and `screening_criteria.md` were not changed.

**Validation (actually performed)**
| Check | Outcome |
|---|---|
| Evidence table against schema (jsonschema) | valid, 2,979 rows; CSV columns = schema properties |
| Required fields / types | 0 missing; types valid by schema |
| Identifier duplicates in final table (PMID, DOI, PMCID, arXiv) | 0 each |
| Title duplicates | 11 identical normalised titles shared by 2 records; all 11 are in `dedup_review.csv` (not merged) |
| Count reconciliation | 3,543 raw − 564 identifier duplicates − 0 title merges = 2,979 = publications = inventory rows; manifest hit rows 3,543 = source records; PubMed retrieved 3,413 = sum of reported totals |
| Source and search IDs | every record has `source_db` and valid `query_ids` (0 violations) |
| No fabricated metadata | every title/DOI/PMID/PMCID/arXiv ID/year in the inventory equals a value in its source records (0 violations); PubMed identifiers equal the raw response (0 mismatches); extraction fields only contain the sentinel |
| Abstracts not committed | no abstract column in committed tables |
| Raw-file checksums | `pubrecords.py verify` → OK |
| Search-page transcription | `check-search` 15/15 passed |
| Unit tests | 22 tests OK |
| Query table | PASS, 158 rows |
| Git diff inspected; earlier logs preserved | only appended rows in logs/queries, except the Q-011 cell; no file deleted |

**Errors / warnings**: 3 transient connector rate-limit errors (retried). The connector's silent 20-article limit was detected and handled. The web-search domain filter was not honoured. One PubMed metadata call came back inline (7 records) and was re-requested so that it was saved verbatim. No validation failures.

**Unresolved questions**: Q-011 (urgent), Q-020–Q-025, plus earlier open ones.

**Branch / commit / PR**: `claude/sweet-brahmagupta-urw7l1`; work commit `b48adde` (this line added in a follow-up commit); PR #2 — https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/2 (open, not merged)

## LIT-003-HOTFIX — 2026-10-23 — Preserve LIT-003 raw exports

**Prompt objective**: secure the 205 git-ignored raw exports of LIT-003 before the container is reclaimed. No screening or methodology changes.

**Completed**: inventory of 205/205 files (0 missing, 0 unexpected, 0 checksum mismatches vs `MANIFEST.csv`). Deterministic archive built and verified (extraction into a separate directory: 208/208 hashes OK, 205/205 match the manifest). Archive delivered to the researcher through the Claude app.
**Preservation status: PENDING.** The researcher must save the archive to private storage and confirm the SHA-256 `69e690f06834758aea76bca99ec4699c2abb2dac9aa776798aecf0366bd60c0e`.

**Created**: `research/literature/preservation/preservation_status.md`, `raw_exports_inventory.csv`, `archive_contents_SHA256SUMS.txt`, `logs/session_logs/2026-10-23_LIT-003-HOTFIX.md`. Archive `preservation/archive/LIT-003_raw_exports_2026-10-23.tar.gz` (3,647,967 bytes) **not committed**.
**Modified**: `.gitignore` (archive directory excluded; reason: it contains abstracts and the repository is public); `research/literature/raw_exports/README.md`, `collection_summary.md` (limitation 6), `research/reviews/unresolved_questions.md` (Q-011 status), `logs/PROMPT_LOG.md`, this file.
**Deleted**: none. Raw files not modified (`pubrecords.py verify` → OK).

**Validation**: as above; plus `git check-ignore` confirms the archive is ignored and `git status` shows no raw or archive file staged.
**Errors / warnings**: none. Google Drive not used (not approved; inline base64 upload impractical).
**PR**: existing PR #2 updated (no new PR).
