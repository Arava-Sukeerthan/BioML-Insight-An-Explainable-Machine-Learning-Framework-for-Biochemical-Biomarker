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

## LIT-003-PRESERVATION-CONFIRMATION — 2026-10-23 — Record researcher-side checksum verification

**Prompt objective**: record that the researcher downloaded the LIT-003 archive and verified its SHA-256 on Windows. Durable storage must not be marked complete without a confirmed second backup.

**Completed**: `preservation_status.md` now says **downloaded and checksum-verified; durable storage not yet confirmed**. It records the command and hash as reported by the researcher, states that checksum verification shows identity and integrity but not durable backup or retention, and keeps Q-011 open for a second private backup or durable location. No storage credentials or locations were requested or recorded.

**Modified**: `research/literature/preservation/preservation_status.md`, `research/literature/raw_exports/README.md`, `research/reviews/unresolved_questions.md` (Q-011 note), `logs/PROMPT_LOG.md`, this file.
**Created**: `logs/session_logs/2026-10-23_LIT-003-PRESERVATION-CONFIRMATION.md`.
**Deleted**: none. Raw exports and archive not modified and not committed.

**Validation (actually performed)**: see the session report; container archive `sha256sum -c` against the `.sha256` file; `pubrecords.py verify`; unit tests; query-table check; `git status` and staged-file check for raw or archive files.

## LIT-003-PRESERVATION-CONFIRMATION (second update) — 2026-10-23 — Second local copy

**Prompt objective**: record the verified download and a second, checksum-verified local copy, without claiming an off-device backup.

**Completed**: `preservation_status.md` now says **archive integrity verified; local redundancy established (both copies on the same computer); off-device backup / disaster recovery outstanding**. A "Second local copy" section records both copies as researcher-reported (outputs not observed). A status-history table keeps the earlier status values. The earlier entry is marked as superseded rather than deleted. No credentials recorded; the backup path is a generic `%USERPROFILE%` path supplied by the researcher. No conflict with existing records was found.

**Modified**: `research/literature/preservation/preservation_status.md`, `research/literature/raw_exports/README.md`, `research/reviews/unresolved_questions.md` (Q-011: remaining item is the off-device backup), `research/reviews/daily_review_log.md`, `logs/PROMPT_LOG.md`, `logs/session_logs/2026-10-23_LIT-003-PRESERVATION-CONFIRMATION.md`, this file.
**Deleted**: none. Raw exports and archive not modified and not committed.

**Validation**: container archive `sha256sum -c`; `pubrecords.py verify`; unit tests; query-table check; staged-file check (results in the session report).

## LIT-004-PREPARATION — 2026-10-23 — Screening protocol review (no screening)

**Prompt objective**: prepare a reproducible pilot title/abstract screening protocol without screening, selecting papers or drawing novelty conclusions.

**Completed**
- Draft `research/literature/screening_protocol.md` v0.1 (PROPOSED). It is an operational layer over `screening_criteria.md` v1.0, which was **not edited**. Contents: input fields; labels and independent descriptors for explainability, uncertainty, calibration and validation; decision rules for the four requested distinctions; Stage-0 handling; the 15 dedup pairs (descriptive categories only); codes E1–E12 unchanged with clarifications; ambiguity/adjudication process; pilot design; blockers B-1…B-6; proposed amendments A-1…A-6.
- Findings recorded as blockers: unstable IDs for 9 web-only records (B-1); no version linking (B-2); conflicting screening-file specifications (B-3); inventory status enum / report script (B-4); abstracts only in the container (B-5); open scope decisions (B-6).
- Preservation: the explicit statement that no off-device backup is available (no external drive) was added to `preservation_status.md` and Q-011.

**Created**: `research/literature/screening_protocol.md`, `logs/session_logs/2026-10-23_LIT-004-PREPARATION.md`.
**Modified**: `logs/DECISION_LOG.md` (D-025, D-026 PROPOSED), `research/reviews/unresolved_questions.md` (Q-011 note; Q-026–Q-030), `research/reviews/daily_review_log.md`, `research/literature/preservation/preservation_status.md`, `logs/PROMPT_LOG.md`, this file.
**Not modified**: paper inventory, screening criteria, search strategy, code, raw exports, archive.
**Deleted**: none.

**Validation**: unit tests, query-table check, raw-export checksum check, inventory unchanged (`git diff`), no raw/archive files staged (results in the completion report).

## LIT-004-WORKFLOW-FIXES — 2026-10-23 — Stable IDs, one screening format, status persistence (no screening)

**Prompt objective**: resolve blockers B-1, B-3 and B-4 (`screening_protocol.md` §8) before any screening.

**Completed**
- **B-1 (IDs).** `record_keys()` now gives a record with no persistent identifier and no year the registry key `source_record:<source_record_id>` (raw-file stem + rank; raw files are immutable and checksummed). New command `pubrecords.py migrate-fallback-keys` appended these keys for the 9 affected records, mapped to the IDs they already had: **P2980–P2988 unchanged** (`records/id_migration_LIT-004.csv`, before = after). Registry 10,776 → 10,785 rows, append-only. Two rebuilds: `publications_index.csv` and the registry byte-identical; paper-ID → source-record mapping identical to the pre-fix build (2,979 publications); `publications_without_stable_registry_key` = 0.
- **B-3 (format).** One file `screening/decisions.csv`; required and optional columns, types and enums in the new `schemas/screening_decision.schema.json`, mirrored by constants in `pubrecords.py`. The build validates every row (decision, stage, reason code E1–E12 only on exclude, `abstract_only` only at full text, justification for exclude/uncertain, date format, screener, RQ tags, descriptor enums) and **rejects unknown columns**. Implementation notes added to `screening_criteria.md` §6 and `search_strategy.md` §6.2 (their text unchanged); `collection_workflow.md` §1 tables updated.
- **B-4 (status).** Inventory `screening_status` enum is now `not_screened / include / exclude / uncertain / abstract_only` (the LIT-001 values `included`, `excluded_title_abstract`, `excluded_full_text` were carried by no record). `make_literature_reports.py` copies decision, stage, reason, descriptors, screener, date and justification from the build instead of writing `not_screened`; no row = `not_screened`, distinct from `uncertain`.
- **No silent loss.** The build stops (writing nothing) if a screening, override, full-text or dedup input names a paper ID that is not in the build. The report script carries manual extraction values (`EXTRACTION_FIELDS`, `extraction_status`, `publication_type`) forward across rebuilds, stops if such a value belongs to a missing paper ID, and validates the inventory before writing it.
- Tests: new `tests/literature/test_screening_and_ids.py` (21 tests, synthetic fixtures) for stable IDs over repeated builds and new data, same-title no-year collision, migration (and its collision refusal), every status, invalid values, orphans, schema/code consistency, manual-field persistence.
- D-027 (PROPOSED) records the format and key scheme, with the URL key and the document wording as alternatives. Q-027 and Q-030 annotated as implemented, still open for approval; Q-031 (`publication_type` vs `record_type` vocabularies) and Q-032 (enforce descriptors?) added.

**Created**: `research/literature/schemas/screening_decision.schema.json`, `research/literature/records/id_migration_LIT-004.csv`, `tests/literature/test_screening_and_ids.py`, `logs/session_logs/2026-10-23_LIT-004-WORKFLOW-FIXES.md`.
**Modified**: `scripts/literature/pubrecords.py`, `scripts/literature/make_literature_reports.py`, `schemas/paper_inventory.schema.json`, `schemas/publication_record.schema.json`, `paper_inventory.csv/.json` (9 new empty columns only; every existing value unchanged, checked against `HEAD`), `records/paper_id_registry.csv` (+9 rows), `records/build_report.json`, `records/collection_stats.json` (new counters), `screening_protocol.md` (§1, §8 status), `screening_criteria.md`, `search_strategy.md` (notes only), `collection_workflow.md`, `logs/DECISION_LOG.md`, `research/reviews/unresolved_questions.md`, `research/reviews/daily_review_log.md`, `logs/PROMPT_LOG.md`, this file.
**Not modified**: search strategy content, queries, criteria, scope, dedup decisions (none made), raw exports, archive.
**Deleted**: none.

**Validation (performed)**: `python3 -I -m unittest discover -s tests/literature` → 43 tests OK; `validate_search_queries.py` → PASS 158 rows; `pubrecords.py verify` → OK; archive `sha256sum -c` → OK; all four schemas pass `check_schema`; no raw export, archive or `.jsonl` staged.
**Not done**: no screening, no pilot sample, no duplicate resolution, no novelty conclusion.


## LIT-004-REVIEW-AND-DECISIONS — 2026-10-23 — Decisions prepared for approval; version linking and scope briefs (no screening)

**Prompt objective**: prepare the researcher's decisions for explicit approval, investigate version linking (B-2), brief the open scope questions, and validate data integrity before pilot screening.

**Completed**
- Decisions prepared, all **PROPOSED** (none approved): D-027 confirmation text; D-028 (Q-031) and D-029 (Q-032) with the conflicts found (`publication_type` is a judgement enum, and source types already sit in `source_publication_types`; `dim_independent_validation` uses a four-value enum under D-026) and options; D-030 version linking. Exact texts in `research/reviews/approval_request_LIT-004.md`.
- B-2 investigated: the 15 pairs categorised from metadata only (8 preprint/journal, 1 unclear version, 2 web = PubMed article, 1 web preprint, 1 arXiv/journal, 1 erratum, 1 distinct patents); no shared URLs in the build. Reversible link representation and counting rules (reports vs studies) proposed in `research/literature/version_linking_proposal.md`. No pair resolved.
- Scope brief `research/methodology/scope_decision_brief.md`: disorders, biomarkers/modalities (gap: proteomics, Q-033), broader biomedical ML, Q-PM-02 (743 records, 626 unique; 83 also retrieved by C/D/E queries, a proxy only), approvals for the executed search.
- Integrity: `make_literature_reports.py` now (1) stops if `paper_inventory.csv` was edited after generation and disagrees with the JSON (checksum recorded in `collection_stats.json`), and (2) carries manual `notes` forward. Previously both could be overwritten on rebuild.
- 7 tests added (`TestIntegrity`): registry append-only, decisions attached after rebuilds with new and merging data, manual note kept, invalid screening input keeps annotations, invalid manual value writes nothing, CSV-only edit not overwritten, `not_screened` ≠ `uncertain` in inventory and index.

**Created**: `research/reviews/approval_request_LIT-004.md`, `research/literature/version_linking_proposal.md`, `research/methodology/scope_decision_brief.md`, `logs/session_logs/2026-10-23_LIT-004-REVIEW-AND-DECISIONS.md`.
**Modified**: `scripts/literature/make_literature_reports.py`, `tests/literature/test_screening_and_ids.py`, `research/literature/records/collection_stats.json` (CSV checksum), `research/literature/screening_protocol.md` (B-2 status), `research/literature/collection_workflow.md`, `logs/DECISION_LOG.md` (D-028–D-030, note on D-027), `research/reviews/unresolved_questions.md` (notes; Q-033, Q-034), `research/reviews/daily_review_log.md`, `logs/PROMPT_LOG.md`, this file.
**Not modified**: inventory contents, registry, criteria, strategy, scope, dedup decisions, raw exports, archive.
**Deleted**: none.

**Validation (performed)**: unit tests 50/50 OK; `validate_search_queries.py` PASS (158 rows); `pubrecords.py verify` OK; archive `sha256sum -c` OK; registry: every committed version is a prefix of the next (10,776 → 10,785 data rows, 0 duplicate keys, 2,979 IDs); report script re-run on real data: inventory unchanged.
**Not done**: no screening, no pilot sample, no pair resolved, no decision approved, D-028–D-030 not implemented.

## LIT-004-DECISION-RECONCILIATION — 2026-10-23 — Reconcile decisions before the pilot (review only)

**Prompt objective**: reconcile the owner's recommended choices with existing governance and decision texts; consolidated decision table; D-026/D-029, D-028, D-030, scope, Q-PM-02 and search-approval reviews. No production changes.

**Completed**
- `research/reviews/decision_reconciliation_LIT-004.md`: consolidated table (D-027–D-030, Q-001, Q-002, Q-033, Q-007/D-009, Q-022, D-012/D-023, D-010, D-008, D-025, A-1…A-6); D-028 roles, mapping and precedence (checked against the 34 source types present); D-026/D-029 conflicts C-1…C-6 and revised wording; version-linking ambiguities V-1…V-9; verbatim scope definitions; Q-PM-02 query review; executed-vs-proposed search comparison (26 of 56 planned searches run); 9 contradictions; 15 approval items; implementation order.
- New open questions Q-035 (biomarker strand field) and Q-036 (arXiv/web transcription spot-check not done).

**Created**: `research/reviews/decision_reconciliation_LIT-004.md`, `logs/session_logs/2026-10-23_LIT-004-DECISION-RECONCILIATION.md`.
**Modified**: `research/reviews/unresolved_questions.md` (Q-035, Q-036 added), `research/reviews/daily_review_log.md`, `logs/PROMPT_LOG.md`, this file.
**Not modified**: `logs/DECISION_LOG.md` (no status or text change), schemas, code, screening criteria, protocol, search strategy, scope, inventory, registry, raw exports, archive.
**Deleted**: none.

**Validation (performed)**: see the completion report: unit tests, query table, raw checksums, archive checksum, `git diff` limited to review/log files.
**Not done**: no approval recorded, no implementation, no pilot, no screening, no pair resolved.

## LIT-004-OWNER-BALLOT — 2026-10-24 — Owner-review ballot for the outstanding LIT-004 decisions (documentation only)

**Prompt objective**: one owner-review document with a ballot entry (issue, options, recommendation, justification, consequences, dependencies, evidence needed, APPROVE/REJECT/MODIFY/DEFER field, comments) for every outstanding LIT-004 decision.

**Completed**
- `research/reviews/owner_review_ballot_LIT-004.md`: 17 items covering D-027, D-028 (2a–2d), D-029 (+D-026), D-030, Q-024/Q-029, Q-001, Q-002/Q-035, Q-033, Q-007/D-009, Q-022 (D-005–D-007), D-012/D-023/Q-036, D-010/Q-011, D-008/Q-008, D-025/Q-026, A-1…A-6, A-3/Q-028, D-024.
- D-028 mapping checked against `source_records.jsonl`: 34 distinct source types, all covered; 7 table entries have no current record; resulting counts per type recorded. Retracted article vs retraction notice, corrections, expressions of concern, protocols, datasets, guidelines/consensus separated. arXiv source rule and URL/DOI rules put to the owner as separate choices.
- D-030 wording conflicts resolved in the proposal text (primary selection, withdrawal by `link_id`, screening decisions after withdrawal, retractions, group rules) with a record/report/study counting specification.
- 15 pairs reconciled with `records/dedup_review.csv`: 15 rows, 30 distinct IDs, 30 flagged publications, no count mismatch; one presentational difference between protocol §4 and the version-linking proposal noted.

**Created**: `research/reviews/owner_review_ballot_LIT-004.md`, `logs/session_logs/2026-10-24_LIT-004-OWNER-BALLOT.md`.
**Modified**: `research/reviews/daily_review_log.md`, `logs/PROMPT_LOG.md`, this file.
**Not modified**: `logs/DECISION_LOG.md`, `unresolved_questions.md`, schemas, code, tests, criteria, protocol, strategy, scope, inventory, registry, screening data (none exists), raw exports, archive.
**Deleted**: none.

**Validation (performed)**: `git diff` against the previous commit limited to the four documentation/log files plus this ballot; unit tests 50/50 OK; query table PASS; raw-export checksums OK; archive checksum OK (results in the completion report).
**Not done**: no approval recorded, no implementation, no pilot, no screening, no pair resolved.

## LIT-004-PROPOSED-RESPONSES — 2026-10-24 — Proposed owner-response set for the LIT-004 ballot (not recorded)

**Prompt objective**: prepare the owner's proposed responses to the 17 ballot items for confirmation, without recording approvals or implementing anything.

**Completed**
- `research/reviews/proposed_owner_responses_LIT-004.md` (v1, PROPOSED): one response per ballot item with the conditions and dependencies that remain open; D-030 MODIFY with an evidence-based retraction procedure (only the retracted record gets E7; related versions never excluded automatically; decided from the notice's stated reason, with human review); Item 16 options reproduced verbatim with neutral consequences and no recommendation (the ballot's "more cautious" phrase is noted and not adopted); D-024/Q-034 ambiguity flagged; pilot-blocking items listed; confirmation line for the owner.
- Checked `[EVIDENCE]`: the 3 retracted articles (P0931, P0939, P1443) are in no flagged pair; no retraction notice is present.

**Created**: `research/reviews/proposed_owner_responses_LIT-004.md`, `logs/session_logs/2026-10-24_LIT-004-PROPOSED-RESPONSES.md`.
**Modified**: `research/reviews/daily_review_log.md`, `logs/PROMPT_LOG.md`, this file.
**Not modified**: `logs/DECISION_LOG.md` (no status change), the ballot, `unresolved_questions.md`, schemas, code, tests, criteria, protocol, strategy, inventory, registry, raw exports, archive.
**Deleted**: none.

**Validation (performed)**: production diff empty; unit tests, query table, raw and archive checksums (results in the completion report).
**Not done**: no response recorded, no spot-check run, no implementation, no pilot, no screening, no pair resolved.

## LIT-004-CLARIFICATION-ADDENDUM — 2026-10-24 — Clarifications for owner review (documentation only)

**Prompt objective**: clarify D-024/Q-034, A-3/Q-028 and the pilot, the D-030 retraction procedure and the D-029 definitions, with response fields; no recording, no implementation.

**Completed**
- `research/reviews/clarification_addendum_LIT-004.md`: D-024 separated from Q-034 (options: 3 or 4 `extraction_status` values; how ineligible, pending, incomplete and completed states are distinguished via screening status and sentinels; proposed consistency checks); Q-028 options verbatim with consequences, comparison of deciding before the pilot vs provisional RQ5 labels (with representation, exclusion from eligibility, later adjudication and statistics safeguards), recommendation of deciding before the pilot without choosing; D-030 retraction procedure distinguishing the six record kinds, E7/E12 conditions and evidence, human review on insufficient evidence, sensitivity analysis and proposed register; full D-029 definitions with RQ5 handling; response fields R1–R6.
- Findings `[EVIDENCE]`: Stage 0 (`search_strategy.md` §6.1) does not cover retraction notices, corrections or expressions of concern, so the procedure needs a Stage-0 amendment; no feature-selection descriptor exists for mechanical RQ5 derivation; 141 theme-F publications, 6 in the pilot's F stratum; all 2,979 inventory rows `not_extracted`.

**Created**: `research/reviews/clarification_addendum_LIT-004.md`, `logs/session_logs/2026-10-24_LIT-004-CLARIFICATION-ADDENDUM.md`.
**Modified**: `research/reviews/daily_review_log.md`, `logs/PROMPT_LOG.md`, this file.
**Not modified**: `logs/DECISION_LOG.md`, ballot, proposed response set, schemas, code, tests, criteria, protocol, strategy, data.
**Deleted**: none.

**Validation (performed)**: production diff empty; unit tests, query table, raw and archive checksums (results in the completion report).
**Not done**: no recording, implementation, spot-check, pilot, screening or pair decision.

## LIT-004-FINAL-CONFIRMATION-SHEET — 2026-10-24 — Final confirmation sheet for the owner (documentation only)

**Prompt objective**: one confirmation sheet with explicit response fields (R1–R6 plus the remaining v1 items) before anything is recorded or implemented.

**Completed**
- `research/reviews/final_confirmation_sheet_LIT-004.md`:
  - response semantics, with conditional approvals recorded as `APPROVED — CONDITIONAL` and never converted;
  - R1 (D-024) separate from R2 (Q-034, option (b) recommended);
  - R3 with the Q-028 options, components and hypothetical examples copied verbatim, the reasons to decide before the pilot, and all dependent criteria and workflow items;
  - R4, the D-030 retraction procedure, conditional on sub-items R4a–R4e;
  - R5, the complete D-029 definitions plus their implementation dependencies;
  - the v1 items summary;
  - R6 recording choice;
  - the pilot-blocking list.
- Quoted text was copied programmatically from the addendum and the v1 set. One cross-reference was adjusted.

**Created**: `research/reviews/final_confirmation_sheet_LIT-004.md`, `logs/session_logs/2026-10-24_LIT-004-FINAL-CONFIRMATION-SHEET.md`.
**Modified**: `research/reviews/daily_review_log.md`, `logs/PROMPT_LOG.md`, this file.
**Not modified**: `logs/DECISION_LOG.md`, the ballot, the proposed response set, the addendum, schemas, code, tests, criteria, protocol, strategy, data.
**Deleted**: none.

**Validation (performed)**: production diff empty; unit tests, query table, raw and archive checksums (results in the completion report).
**Not done**: no recording, implementation, spot-check, pilot, screening or pair decision.

## LIT-004-Q028-DECISION — 2026-10-24 — Record the owner's Q-028 response (conditional)

**Prompt objective**: record the owner's response to Q-028 (option (c), ≥ 4 of 5 separate components) after verifying the components, effects, defensibility and dependencies; no other decision.

**Completed**
- Verified the five components against `screening_criteria.md` §3 and the ballot. Found that feature selection has no operational screening definition, "covering a component" is undefined, and explainability/calibration/uncertainty depend on unapproved D-029 definitions (R5).
- `research/reviews/Q-028_owner_decision_record.md`:
  - the six qualifying combinations and the effect on RQ5 eligibility and the closest-prior-art table;
  - the defensibility assessment, which does not consider which novelty conclusion either threshold would favour;
  - conditions C1–C4;
  - the dependent documents.
- `logs/DECISION_LOG.md`: new **D-031, APPROVED — CONDITIONAL** (researcher/owner, 2026-10-24), plus a status-history row and a note that D-026 and A-3 stay partly open. No other entry was changed.
- `unresolved_questions.md`: Q-028 marked answered (→ D-031, conditional); Q-037 (feature-selection and "covering" definitions) and Q-038 (handling of 3-of-5 frameworks) added.
- `final_confirmation_sheet_LIT-004.md`: R3 option (c) marked with the owner's words. All other lines remain unanswered.

**Created**: `research/reviews/Q-028_owner_decision_record.md`, `logs/session_logs/2026-10-24_LIT-004-Q028-DECISION.md`.
**Modified**: `logs/DECISION_LOG.md`, `research/reviews/unresolved_questions.md`, `research/reviews/final_confirmation_sheet_LIT-004.md`, `research/reviews/daily_review_log.md`, `logs/PROMPT_LOG.md`, this file.
**Not modified**: screening criteria, protocol, search strategy, research plan, schemas, code, tests, data, and every other decision entry.
**Deleted**: none.

**Validation (performed)**: production diff empty; unit tests, query table, raw and archive checksums (results in the completion report).
**Not done**: criteria v1.1 and dependent document updates (await C1–C4), implementation, pilot, screening, pair decisions.

## CORRECTION — 2026-10-24 — PR #2 status (recorded in LIT-004-Q028-DECISION)

**Finding `[EVIDENCE]`** (GitHub API, checked 2026-10-24): PR #2 was **merged** by the owner on 2026-10-23 at 17:51 UTC, at head `7b61e83`, as merge commit `7ffdcd2` on `claude/happy-hawking-rxptfv`.

Ten later commits on `claude/sweet-brahmagupta-urw7l1` are **not part of any pull request**: `f8fac8d`, `8056054`, `441d00e`, `6a2d017`, `56910a8`, `d14a002`, `95407fb`, `22f11ea`, `8504899`, `cb5c941`. They run from the second local archive copy through LIT-004-Q028-DECISION.

The CHANGELOG and PROMPT_LOG entries for those tasks state "PR #2 (existing, updated); not merged". **That statement is incorrect** and is corrected here. The earlier entries are left unchanged as the historical record.

The status was not checked after the merge, and the reports repeated the earlier state.

**Remaining step:** the owner decides how these 10 commits are reviewed, e.g. a new PR from the same branch into `claude/happy-hawking-rxptfv`. No rebase or force-push is needed, because `7b61e83` is already in the base. No PR was created, because the owner's instructions in these tasks excluded creating another PR.

## LIT-004-PR — 2026-10-24 — New pull request for the post-PR #2 commits

**Prompt objective**: open a new PR for the commits pushed after PR #2 was merged, without rewriting history.

**Completed**
- Verified with git and the GitHub API:
  - PR #1 (head `7352cee`) and PR #2 (head `7b61e83`, merge commit `7ffdcd2`, 2026-10-23 17:51 UTC) are both merged into `claude/happy-hawking-rxptfv` (the default branch).
  - No open PR existed.
  - 11 commits, `7b61e83..8f258a8`, were in no PR.
- Opened **PR #3**: https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/3. Base `claude/happy-hawking-rxptfv`, head `claude/sweet-brahmagupta-urw7l1`; not merged.

**Created**: `logs/session_logs/2026-10-24_LIT-004-PR.md`. **Modified**: `logs/PROMPT_LOG.md`, this file.
**Not modified**: decisions, criteria, schemas, code, data.

**Validation (performed)**:
- Unit tests: 50 OK.
- Query table: PASS, 158 rows.
- Raw-export checksums: OK. Archive checksum: OK.
- Schemas and inventory: valid.
- Registry: 2,979 IDs, 0 duplicate keys.
- `git merge-tree`: clean.
- No raw, archive, `.jsonl` or git-ignored files in the diff.

## Q-037a — 2026-10-24 — Proposal: feature/biomarker-selection component for RQ5 (not approved)

**Prompt objective**: an evidence-based proposal defining the selection component (D-031 condition C2), without screening or implementation.

**Completed**
- `research/reviews/Q-037a_feature_selection_proposal.md`:
  - options A (broad), B (data-driven subset selection; recommended), C (narrow), plus a sub-choice on knowledge-based panels;
  - a comparison of 8 candidate kinds of procedure: qualifies or not, evidence needed, how ambiguity is labelled, likely screener disagreements;
  - the operational definition, evidence and uncertainty rules, and human-review triggers;
  - 2 positive, 3 negative and 5 borderline hypothetical examples;
  - a design for an optional `dim_feature_selection` descriptor (no data migration; IDs unaffected);
  - risks, dependencies, and owner-response fields left unanswered.
- Sources verified through PubMed (PMIDs 17720704, 9044528, 11983868). Only statements in the PubMed records are attributed. Unverified points (category names, PCA statement, VIP) are marked as not cited.
- DECISION_LOG: D-032 PROPOSED. `unresolved_questions.md`: Q-037 annotated; still Open.

**Created**: the proposal and `logs/session_logs/2026-10-24_Q-037a.md`. **Modified**: `logs/DECISION_LOG.md`, `research/reviews/unresolved_questions.md`, `research/reviews/daily_review_log.md`, `logs/PROMPT_LOG.md`, this file.
**Not modified**: criteria, protocol, strategy, schemas, code, tests, data, other decisions.
**Branch note**: committed on a **local** branch `q037a-feature-selection` (from `9497a3a`). It was **not pushed**: the session's designated branch is PR #3's head, which this task must not modify. Awaiting the owner's choice of branch strategy.

**Validation (performed)**: see the completion report.

**Q-037a PR (2026-10-24)**: following the owner's approval of the stacked-PR workflow, branch `q037a-feature-selection` was pushed and **PR #4** opened: https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/4. Base `claude/sweet-brahmagupta-urw7l1` (PR #3 head, unchanged at `9497a3a`); head `q037a-feature-selection`. Diff before this log commit: `9497a3a..0e976db`, 7 files. Not merged. D-032 remains PROPOSED.

## RQ5-DECISIONS — 2026-10-24 — Record the owner's Q-037a, Q-037b and Q-038 decisions; implement `dim_feature_selection` (inactive)

**Prompt objective**: record and reconcile 15 owner decisions (Q-037a ×5, Q-037b ×5, Q-038 ×5), keep the dependent definitions inactive, and implement only what the schema safely supports.

**Owner-approved (conditional, inactive)**
- D-032 (Q-037a): PROPOSED → APPROVED — CONDITIONAL. Recorded as a status-history row; the original row is kept.
- D-033 (Q-037b): new entry, APPROVED — CONDITIONAL.
- D-034 (Q-038): new entry, APPROVED — CONDITIONAL.
- D-031 not revised. Its conditions C2–C4 are answered at decision level; C1 (R5) is open.

**Implemented (inactive for screening)**
- Optional column `dim_feature_selection` (`""/yes/no/unclear`):
  - `pubrecords.py`: `SCREENING_OPTIONAL`, `SCREENING_ENUMS`;
  - `schemas/screening_decision.schema.json`;
  - `schemas/publication_record.schema.json` (`screening_details`);
  - `schemas/paper_inventory.schema.json`;
  - `make_literature_reports.py`;
  - one new test.
- Real data rebuilt:
  - paper-ID → source-record mapping identical;
  - registry identical;
  - every existing inventory value unchanged;
  - the new column is null for all 2,979 records (no value filled).

**Proposed / specified only**
- `rq5_coverage_group` derivation, with a companion `rq5_coverage_provisional` flag; `pending_review` not proposed. Implementation **blocked** (Q-039, Q-041, R5, D-027).
- `scope_flags` tokens `published_panel_reused` (documented convention) and `proposed_only:<component>` (proposal).
- Component-specific evidence criteria (owner minimums only; no added requirements).

**Conflicts and open dependencies**
- New Q-039: no classification status field.
- New Q-040: non-metabolic 3-of-5 frameworks are excluded with E4 at screening, so the near-RQ5 group may be incomplete.
- New Q-041: R5 "stated" vs D-033 "applied", and the meaning of "confirmed".
- Option letters for Q-037a and the Q-037b/Q-038 options are not in the repository; the choices are recorded by content.

**Created**: `research/reviews/RQ5_component_decisions_D032-D034.md`, `logs/session_logs/2026-10-24_RQ5-DECISIONS.md`.
**Modified**:
- `logs/DECISION_LOG.md` (append-only)
- `research/reviews/unresolved_questions.md` (Q-037 and Q-038 status; Q-039–Q-041 added)
- `research/reviews/Q-037a_feature_selection_proposal.md` (status line; §10 owner responses)
- the schemas, code and test above
- `research/literature/paper_inventory.csv/.json` (new null column)
- `records/build_report.json` (`built_at`)
- `records/collection_stats.json` (CSV checksum)
- `research/reviews/daily_review_log.md`, `logs/PROMPT_LOG.md`, this file

**Not modified**: screening criteria, protocol, search strategy, research plan, other decisions, raw exports, archive.

**Git**: committed locally on `q037a-feature-selection` (PR #4's head branch). **Not pushed**: pushing would add this commit to PR #4 and needs the owner's authorization.

**Validation (performed)**: see the session log and completion report.

**RQ5-DECISIONS PR (2026-10-24)**: following the owner's choice of a separate stacked PR, branch `rq5-decisions-d032-d034` was created at `ed432a9`. That commit was unpushed and its parent is PR #4's head `b3f1ab2`, so no history was rewritten. The local `q037a-feature-selection` ref was reset to its unchanged remote (`b3f1ab2`); the remote PR #4 branch was not touched. The new branch was pushed and **PR #5** opened: https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/5. Base `q037a-feature-selection` (PR #4 head) ← head `rq5-decisions-d032-d034`. Not merged. D-032–D-034 remain APPROVED — CONDITIONAL and inactive.

## Q-041-DECISIONS — 2026-10-24 — Record D-035 (RQ5 evidence standard); stage-separated component evidence (inactive)

**Prompt objective**: record the owner's Q-041 choices (G1–G6), update the RQ5 documentation consistently, and implement only what resolved dependencies permit; no screening.

**Owner-approved (conditional, inactive)**
- D-035, new: G1 A, G2 A, G3 I, G4 B, G5 A, G6 approve.
- Status-history notes:
  - D-031: C1 met at decision level; still conditional.
  - D-034: "confirmed" defined; groups unchanged.
  - D-029 and D-026: stay PROPOSED; their component wording is governed by D-035 for RQ5.
- No approved decision was changed.

**Implemented**
- `pubrecords.py`:
  - `rq5_component_evidence()`: per paper, `preliminary` (latest title/abstract row) and `confirmed` (latest full-text row, not `abstract_only`), with full-text history, `researcher_verified` and `changed_by_verification`;
  - a later same-stage row blanking a recorded component stops the build;
  - a full-text row with only some component statuses stops the build;
  - `derive_rq5_coverage_group()`: D-034 on confirmed statuses, with `null` for not assessed and a provisional flag. **Not wired** (Q-039).
- Publication-record schema: new `rq5_components` (null for all records).
- 9 new tests; one existing test moved to title/abstract rows (G5 completeness).
- Screening-file columns, inventory and IDs unchanged.

**Documentation (INACTIVE notes; draft text unchanged)**
- `screening_criteria.md` (RQ5, Tier 1);
- `screening_protocol.md` new §2a;
- `search_strategy.md` §1.2, §8.3 and change history;
- `research_plan.md` §2, §8 and change history;
- the R5 note in `final_confirmation_sheet_LIT-004.md`;
- §8 addendum in `RQ5_component_decisions_D032-D034.md`;
- Q-041 answered.

**Created**: `research/reviews/Q-041_decision_record_D035.md`, `logs/session_logs/2026-10-24_Q-041-DECISIONS.md`.
**Not modified**: screening data (none exists), inventory values, registry, raw exports, archive, PR branches.
**Git**: working tree on new local branch `q041-rq5-evidence-standard` (from PR #5 head `b7c2e51`). **Not committed and not pushed** (awaiting owner authorization).

**Validation**: see the session log.

## CORRECTION — 2026-10-24 — Q-041/D-035 git status and PR #4–#8 history (GOV-LOG-CORRECTION, findings M1/M2)

**Scope**: log corrections only. No change to methodology, decisions or decision statuses, criteria, schemas, code, tests or data. Earlier entries are left unchanged as the historical record; this entry supersedes the statements listed below.

**M1 — stale statements** `[EVIDENCE: git, GitHub API, checked 2026-10-24]`

| Location | Earlier statement (true when written) | Corrected status |
|---|---|---|
| This file, Q-041-DECISIONS entry ("**Git**" line) | Local branch `q041-rq5-evidence-standard`; "Not committed and not pushed" | Committed as `0eae10a` (parent `b7c2e51`) and pushed to `q041-rq5-evidence-standard`. PR #7 was opened from it and merged into the **intermediate** branch `q037a-feature-selection` (merge commit `f5b03e3`), **not** the default branch. PR #8 was opened from the same head into the default branch to bring the same reviewed changes there; it is open and subject to owner review |
| `PROMPT_LOG.md`, Q-041-DECISIONS rows "Branch" / "Pull request" | "local; uncommitted"; "None" | As above (PR #7 merged into an intermediate branch; PR #8 open) |
| `session_logs/2026-10-24_Q-041-DECISIONS.md`, "Branch" row | "uncommitted" | As above (a correction row is appended to that log) |
| `PROMPT_LOG.md`, Q-037a and RQ5-DECISIONS "Pull request" rows; this file, Q-037a and RQ5-DECISIONS PR notes | PR #4 / PR #5 "open; not merged" | Both merged on 2026-10-24 into intermediate branches (table below); their content reached the default branch through PR #6 |
| `PROMPT_LOG.md`, LIT-004-PR; this file, LIT-004-PR | PR #3 "open; not merged" | Merged into the default branch (table below) |

**M2 — verified PR history** (times UTC, 2026-10-24; SHAs abbreviated). "Reached default" was checked with `git merge-base --is-ancestor` against `origin/claude/happy-hawking-rxptfv` (head `c69b162`).

| PR | Purpose | Head (SHA) | Base | Status | Merge commit (parents) | Reached default branch? |
|---|---|---|---|---|---|---|
| [#3](https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/3) | LIT-004 post-PR #2 commits (context) | `claude/sweet-brahmagupta-urw7l1` (`9497a3a`) | `claude/happy-hawking-rxptfv` (default) | Merged 04:48:22 | `7c667bf` (`7ffdcd2`, `9497a3a`) | Yes, directly |
| [#4](https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/4) | Q-037a proposal (D-032 PROPOSED) | `q037a-feature-selection` (`b3f1ab2`) | `claude/sweet-brahmagupta-urw7l1` (**intermediate**) | Merged 04:48:36 | `ea0889e` (`9497a3a`, `b3f1ab2`) | Merge commit `ea0889e`: **no**. Content (`b3f1ab2`): yes, via PR #6 |
| [#5](https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/5) | D-032–D-034, inactive `dim_feature_selection` | `rq5-decisions-d032-d034` (`b7c2e51`) | `q037a-feature-selection` (**intermediate**) | Merged 04:48:50 | `88badf6` (`b3f1ab2`, `b7c2e51`) | Yes, via PR #6 (`88badf6` is PR #6's head) |
| [#6](https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/6) | Bring PR #4/#5 work (D-032–D-034) to default | `q037a-feature-selection` (`88badf6`) | `claude/happy-hawking-rxptfv` (default, `7c667bf`) | Merged 05:00:19 | `c69b162` (`7c667bf`, `88badf6`) | Yes, directly |
| [#7](https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/7) | Q-041/D-035 | `q041-rq5-evidence-standard` (`0eae10a`) | `q037a-feature-selection` (**intermediate**, `88badf6`) | Merged 05:00:28 | `f5b03e3` (`88badf6`, `0eae10a`) | **No** (`f5b03e3` and `0eae10a` are not on default) |
| [#8](https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/8) | Replacement PR: same reviewed Q-041/D-035 changes to default | `q041-rq5-evidence-standard` (`0eae10a` before this log commit) | `claude/happy-hawking-rxptfv` (default, `c69b162`) | **Open**, created 05:03:34; subject to owner review | — | Not yet |

**Unknown / not recorded**: the GitHub account that performed each merge (the API query used did not return `merged_by`); the merge method is inferred to be a merge commit, because each merge SHA has two parents. Creation times of PRs #3–#7 are 03:31:49, 03:45:38, 04:19:29, 04:55:04 and 04:55:46 respectively.

**Cause**: the stacked PRs (#4, #5, #7) were merged without being retargeted to the default branch after their parent PRs merged, and the logs were not updated after the commit, push and merges.

**Decision statuses (unchanged)**: D-026 and D-029 PROPOSED; D-031–D-034 APPROVED — CONDITIONAL; D-035 APPROVED — CONDITIONAL and inactive. Screening and the pilot are not started.

**Modified**: this file; `logs/PROMPT_LOG.md`; `logs/session_logs/2026-10-24_Q-041-DECISIONS.md` (appended correction row); `research/reviews/daily_review_log.md`. **Created**: `logs/session_logs/2026-10-24_GOV-LOG-CORRECTION.md`. **Not modified**: `DECISION_LOG.md`, code, tests, schemas, research documents, data.

**Validation**: see the session log. No CI is configured, so none ran.

## CORRECTION — 2026-10-24 — PR #8 merged (GOV-PR8-MERGE-RECORD)

**Scope**: log-only. This supersedes the "PR #8 open / subject to owner review / not yet on default" statements in the CORRECTION entry above (GOV-LOG-CORRECTION) and in `PROMPT_LOG.md`. Those statements were correct when written and are left unchanged.

**Verified `[EVIDENCE: GitHub API and git, checked 2026-10-24]`**

| Item | Value |
|---|---|
| PR | [#8](https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/8): **merged** (no longer open) |
| Merged at | 2026-10-24 05:20:14 UTC |
| Merged by | `Arava-Sukeerthan` (GitHub `merged_by` for PR #8). The merge accounts for PRs #3–#7 remain **not verified** |
| Merge commit | `18f4b09`, parents `c69b162` (base before merge) and `4835d3b` (head before merge) |
| Default branch | `claude/happy-hawking-rxptfv` at `18f4b09`; `0eae10a` (Q-041/D-035) and `4835d3b` (log corrections) are ancestors |
| Merge content | The merge-commit tree is identical to `4835d3b`. The diff `c69b162..18f4b09` is identical to the PR #8 diff (17 files, +620/−6). `DECISION_LOG.md` is append-only (+10/−0) |

**Post-merge validation** (run on a checkout whose tree equals `18f4b09`):
- unit tests: 60, OK;
- query table: PASS, 158 rows;
- raw-export verify: OK, all match `MANIFEST.csv`;
- archive checksum: OK;
- decision IDs: 35 unique (D-001–D-035), no gaps or duplicates.

No CI is configured.

**Statuses confirmed unchanged**: D-026 and D-029 PROPOSED; D-035 APPROVED — CONDITIONAL, inactive for screening. Screening and pilot not started (no `screening/decisions.csv` or pilot file exists).

**Modified**: this file; `logs/PROMPT_LOG.md`; `research/reviews/daily_review_log.md`. **Created**: `logs/session_logs/2026-10-24_GOV-PR8-MERGE-RECORD.md`. **Not modified**: `DECISION_LOG.md`, code, tests, schemas, criteria, protocol, data, branches other than the new `gov-pr8-merge-record`.

**GOV-PR8-MERGE-RECORD PR (2026-10-24)**: following the owner's request, **PR #9** "docs: record PR #8 merge in governance logs" was opened: https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/9. Base `claude/happy-hawking-rxptfv` (`18f4b09`) ← head `gov-pr8-merge-record` (`bf36297` when opened; this log-only commit is added on top). Status: **open**, awaiting owner review; not merged. Recorded per CLAUDE.md §3.5; the PROMPT_LOG "Pull request" row for this task is corrected in the same way.

## Q-039-DECISION — 2026-10-24 — Record D-036 (classification status); `dim_classification` and build-derived RQ5 coverage group (inactive)

**Prompt objective**: record the researcher's Q-039 choices (Choice 1 Option A, Choice 2 Option A) as a formal decision and implement them in one reviewable PR, without activating screening.

**Decision**: **D-036 — APPROVED — CONDITIONAL (inactive for screening)**, approved by the researcher (owner) on 2026-10-24 through the explicit choices in the prompt (`research/reviews/Q-039_decision_record_D036.md`). Q-039 is answered. New open question **Q-042** asks whether `lr_only` studies can receive classification `yes`; it is not decided. No other decision changes status. D-026, D-027 and D-029 stay PROPOSED.

**Implemented**
- `pubrecords.py`:
  - `dim_classification` (`""/yes/no/unclear`) added to `SCREENING_OPTIONAL` and `SCREENING_ENUMS`;
  - `RQ5_COMPONENT_FIELDS["classification"] = "dim_classification"`, so the erasure check, the full-text completeness check and preliminary/confirmed detection now cover all five components;
  - `build()` sets `rq5_coverage_group` and `rq5_coverage_provisional` from `derive_rq5_coverage_group()` on **confirmed** statuses only.
- Schemas:
  - screening decision: property and column order;
  - publication record: `screening_details.dim_classification`, `rq5_coverage_group`, `rq5_coverage_provisional`;
  - inventory: `dim_classification`.
- `make_literature_reports.py`: inventory column `dim_classification`.
- Tests: `TestRQ5ComponentEvidence` rewritten for five components (16 tests). The test that encoded the four-component limitation was replaced. `TestSchemaConsistency` gained a publication-schema test.
- Real-data outputs regenerated with the repository's tools:
  - `paper_inventory.csv` and `.json` gain an empty `dim_classification` column for all 2,979 records;
  - `collection_stats.json`: inventory hash only;
  - `build_report.json` differed only in `built_at` and was restored.

**Documentation**
- Protocol §2a (INACTIVE): describes the five columns and the derived group.
- Dated addenda: D-035 record §8 and `RQ5_component_decisions_D032-D034.md` §9.
- `unresolved_questions.md`: Q-039 answered; Q-042 added.
- DECISION_LOG: D-036 section and three status-history rows.

**Not modified**: `screening_criteria.md`, raw exports, archive, registry, paper IDs, `GOVERNANCE.md`. No screening decision, pilot or model training.

**Validation**: see `logs/session_logs/2026-10-24_Q-039-DECISION.md`. No CI is configured.

**Q-039-DECISION PR (2026-10-24)**: **PR #10**, "Q-039: D-036 dim_classification and build-derived RQ5 coverage group (conditional, inactive)": https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/10. Base `claude/happy-hawking-rxptfv` (`17b0866`) ← head `q039-dim-classification` (work commit `b122e10`, plus this log-only commit). Status: **open**, awaiting owner review; not merged.

## PR10-AUDIT-DECISIONS — 2026-10-24 — Record D-037 (owner decisions A1 and B1 after the PR #10 audit); provisional-flag rule

**Prompt objective**: implement the researcher's Decision A1 (`rq5_coverage_provisional` only when resolving `unclear` statuses could change the group) and record Decision B1 (Q-042 is not a new activation blocker), as a follow-up to PR #10. Screening stays inactive.

**Decision**: **D-037 — APPROVED — CONDITIONAL (inactive for screening)**, approved by the researcher (owner) on 2026-10-24 (`research/reviews/PR10_audit_decisions_D037.md`). It revises part of D-036 by a new entry; D-036 keeps its status and text.

**Implemented**
- `pubrecords.py`: `derive_rq5_coverage_group()` now sets the provisional flag by enumerating every `yes`/`no` resolution of the `unclear` statuses; true only if one gives a different group. New helper `_rq5_group_for()` holds the unchanged thresholds. Null behaviour for missing statuses unchanged.
- `publication_record.schema.json`: `rq5_coverage_provisional` description.
- Tests (`test_screening_and_ids.py`): two new tests (the A1 examples in every component order; all 3,125 status combinations against an independent form of the rule). Expectations changed in three existing tests: 4 `yes` + 1 `unclear` is now `qualified`, not provisional.

**Documentation**
- New decision record `research/reviews/PR10_audit_decisions_D037.md`.
- Dated addenda: D-036 record §8, `RQ5_component_decisions_D032-D034.md` §10, D-035 record §9. Original text unchanged.
- `screening_protocol.md` §2a (INACTIVE): coverage-group line.
- `unresolved_questions.md`: Q-042 "Needed by" corrected (no longer an activation condition; status **Open**). New **Q-043**: whether D-034(4)'s "flag kept" needs a separate marker for qualified records with an `unclear` component.
- DECISION_LOG: D-037 section and three status-history rows (+9/−0).

**Not modified**: raw exports, archive, registry, paper IDs, inventory CSV/JSON, `collection_stats.json`, `screening_criteria.md`, `GOVERNANCE.md`, `CLAUDE.md`, D-035 §6 activation conditions. No screening decision, pilot or model training. No `lr_only` rule.

**Validation**: see `logs/session_logs/2026-10-24_PR10-AUDIT-DECISIONS.md`. No CI is configured.

**PR10-AUDIT-DECISIONS PR (2026-10-24)**: **PR #11**, stacked on PR #10: https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/11. Base `q039-dim-classification` (`f106fdc`) ← head `claude/eloquent-mccarthy-bqtxr3` (work commit `29523ea`, plus this log-only commit). Status: **open**, awaiting owner review; not merged. PR #10 not changed.

## CORRECTION — 2026-10-24 — PRs #10, #11 and #12 merged; D-037 reached the default branch through PR #12 (GOV-PR10-12-MERGE-RECORD)

**Scope**: log-only. This supersedes the "open / awaiting owner review / not merged" statements for PR #10 (Q-039-DECISION entry) and PR #11 (PR10-AUDIT-DECISIONS entry) above and in `PROMPT_LOG.md`. Those statements were correct when written and are left unchanged. It also records **PR #12**, which was not previously entered in this file (CLAUDE.md §3.5).

**Verified `[EVIDENCE: GitHub API and git, checked 2026-10-24]`**

| PR | Merged into | Merged at (GitHub `merged_at`, UTC) | Merged by | Merge commit and parents | Merge-commit tree |
|---|---|---|---|---|---|
| [#10](https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/10) (Q-039 / D-036) | `claude/happy-hawking-rxptfv` (default) | 2026-10-24 06:50:19 | `Arava-Sukeerthan` | `ad650f9`: `17b0866` (base), `f106fdc` (head) | identical to `f106fdc` |
| [#11](https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/11) (D-037: A1, B1; Q-043 opened) | `q039-dim-classification` (its stacked base, **not** the default branch) | 2026-10-24 06:50:31 | `Arava-Sukeerthan` | `bd0c8ee`: `f106fdc` (base), `e8bf189` (head) | identical to `e8bf189` |
| [#12](https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/12) (recovery: PR #11's head into the default branch) | `claude/happy-hawking-rxptfv` (default) | 2026-10-24 06:59:56 | `Arava-Sukeerthan` | `6f57b6f`: `ad650f9` (base), `e8bf189` (head) | identical to `e8bf189` |

- **Sequence.** PR #10 brought D-036 into the default branch. Twelve seconds later, PR #11 was merged into `q039-dim-classification`, so the default branch did **not** receive D-037. PR #12 (opened with owner authorization; head `claude/eloquent-mccarthy-bqtxr3` @ `e8bf189`, 2 commits `29523ea` and `e8bf189`, 14 files, +228/−12, identical to PR #11's diff) then brought D-037 into the default branch without the merge commit `bd0c8ee`.
- **Result.** The default branch `claude/happy-hawking-rxptfv` is at `6f57b6f`. Its tree equals `e8bf189` (PR #11's reviewed head): D-036 and D-037 are both present. `bd0c8ee` is **not** an ancestor of the default branch; it remains only on `q039-dim-classification`, whose content is identical. No branch was deleted.
- **Merge-commit times** (git committer date, GitHub): `ad650f9` 06:50:18, `bd0c8ee` 06:50:30, `6f57b6f` 06:59:56 UTC. They differ from `merged_at` by at most one second.

**Post-merge validation** (run on this branch, whose code, tests and data equal `6f57b6f`): see `logs/session_logs/2026-10-24_GOV-PR10-12-MERGE-RECORD.md`. Real-data rebuild, raw-export verify and archive checksum **not run** (raw exports and git-ignored build files are not in the container). No CI is configured.

**Statuses confirmed unchanged**: D-036 and D-037 APPROVED — CONDITIONAL (inactive for screening). D-038 is in open PR #13, not on the default branch. Screening and pilot not started (no `screening/decisions.csv` or pilot file exists). Q-042 Open.

**Modified**: this file; `logs/PROMPT_LOG.md`; `research/reviews/daily_review_log.md`. **Created**: `logs/session_logs/2026-10-24_GOV-PR10-12-MERGE-RECORD.md`. **Not modified**: `DECISION_LOG.md`, decision records, code, tests, schemas, criteria, protocol, data. Branch: local `gov-pr10-12-merge-record` from `6f57b6f`; not pushed, no PR.

## Q-043-DECISION — 2026-10-24 — Record D-038 (reporting of qualified records with an unresolved component; no marker)

**Prompt objective**: record the owner's approved Q-043 resolution as a new append-only decision; update PR #10's description (B1 wording); prepare the PR #10/#11 merge sequence and the Option A proposal for `abstract_only` without implementing either.

**Decision**: **D-038 — APPROVED — CONDITIONAL (inactive for screening)**, approved by the researcher (owner) on 2026-10-24 (`research/reviews/Q-043_decision_record_D038.md`). ID checked as the next free one on every branch. Q-043 answered.

**Changed**
- New decision record `research/reviews/Q-043_decision_record_D038.md`.
- DECISION_LOG: D-038 section and two status-history rows (+8/−0).
- `unresolved_questions.md`: Q-043 status cell → Answered.
- Dated addenda: `RQ5_component_decisions_D032-D034.md` §11, `PR10_audit_decisions_D037.md` §6.
- `screening_protocol.md` §2a (INACTIVE): one reporting bullet.
- PR #10 description (GitHub, not a repository file): Q-042 removed from the remaining activation conditions, with a statement that Q-042 remains open and no `lr_only` rule is decided; follow-up note on PR #11. Title, base, head and state unchanged.

**Not modified**: code, schemas, tests, inventory, raw exports, `screening_criteria.md`, `GOVERNANCE.md`, `CLAUDE.md`. No screening decision, pilot or model training. No PR merged, retargeted, approved or closed.

**Validation**: see `logs/session_logs/2026-10-24_Q-043-DECISION.md`. No CI is configured.

**Q-043-DECISION follow-up (2026-10-24, owner instructions after the pre-merge review)**:
- D-038 record (not yet pushed): status line reads **APPROVED — CONDITIONAL (inactive)**, stating that the reporting rule is approved in principle and screening stays inactive until the applicable activation conditions are met; the §4 "must be carried into criteria v1.1 / protocol v0.2" sentence is replaced by `[RECOMMENDATION] Carry D-038-2 into criteria v1.1 / protocol v0.2 when drafted (owner to confirm).` The DECISION_LOG entry is not edited.
- PR #11 description (GitHub, owner-authorized): the stale sentence "PR #10's description still lists Q-042 under 'Remaining blockers'. It was not edited and is left for the owner." is replaced by "PR #10's description was updated on 2026-10-24 (owner Decision 2) to remove Q-042 from its activation conditions." Nothing else in PR #11 changed (head `e8bf189`, base, title and state unchanged). The D-037 record (§3, "Not edited: the PR #10 description …") is kept as written; it was accurate when written.


**Q-043-DECISION rebase (2026-10-24, log-only)**: branch `q043-reporting-rule` was rebased onto default-branch commit `6f57b6f` (merge of PR #12; D-037 now on the default branch), from its earlier base `e8bf189`. No conflicts; the D-038 diff is byte-identical before and after. Rebased work commits: `1547cf0` → `995166c`, `ef3bfa6` → `83b4951`. The earlier branch notes in PROMPT_LOG and the Q-043-DECISION session log ("from `e8bf189`") were accurate when written and are kept as written. This note's own commit ID is recorded in the PR description.

**Q-043-DECISION PR (2026-10-24)**: **PR #13**, "Q-043: D-038 reporting rule for qualified records with an unresolved component (no marker; inactive)": https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/13. Base `claude/happy-hawking-rxptfv` (`6f57b6f`) ← head `q043-reporting-rule` (work commits `995166c`, `83b4951`, rebase note `07087d3`, plus this log-only commit). Status: **open**, awaiting owner review; not merged.

## CORRECTION — 2026-10-24 — PRs #14 and #13 merged; D-038 on the default branch (GOV-PR13-14-MERGE-RECORD)

**Scope**: log-only. This supersedes the "open / not merged" statements for PR #13 (Q-043-DECISION PR paragraph above, and `PROMPT_LOG.md`), the "not pushed, no PR" statements for the GOV-PR10-12-MERGE-RECORD branch, and that record's dated statement "D-038 is in open PR #13, not on the default branch". Those statements were correct when written and are left unchanged. It also records **PR #14** by number for the first time (CLAUDE.md §3.5).

**Verified `[EVIDENCE: GitHub API and git, checked 2026-10-24]`**

| PR | Merged into | Merged at (GitHub `merged_at`, UTC) | Merged by | Merge commit and parents | Merge-commit tree |
|---|---|---|---|---|---|
| [#14](https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/14) (GOV-PR10-12-MERGE-RECORD, log-only) | `claude/happy-hawking-rxptfv` | 2026-10-24 07:36:47 | `Arava-Sukeerthan` | `f7f6bb7`: `6f57b6f` (base), `30905f4` (head) | — |
| [#13](https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/13) (Q-043 / D-038) | `claude/happy-hawking-rxptfv` | 2026-10-24 07:48:00 | `Arava-Sukeerthan` | `694b389`: `f7f6bb7` (base), `6776eba` (head) | identical to `6776eba` |

- **Conflict resolution before the merge.** After PR #14 merged, PR #13 conflicted in `logs/CHANGELOG.md`, `logs/PROMPT_LOG.md` and `research/reviews/daily_review_log.md`: both sides had appended at the end of each file. With owner authorization, `f7f6bb7` was merged into `q043-reporting-rule` (`6776eba`, parents `fde915a`, `f7f6bb7`; `--no-ff`, no rebase, normal push). Each file keeps the default-branch text byte for byte, followed by the PR #13 block.
- **Result.** The default branch is at `694b389`. `f7f6bb7..694b389` is identical to the reviewed PR #13 diff (10 files, +119/−1). D-036, D-037 and D-038 are all on the default branch.

**Post-merge validation** (run on a copy of `694b389`): unit tests 69, OK; query table PASS, 158 rows; decision log 38 unique IDs (D-001–D-038), no duplicates, D-038 once. Real-data rebuild, raw-export verify and archive checksum **not run** (raw exports and git-ignored build files are not in the container). No CI is configured.

**Statuses confirmed unchanged**: D-036, D-037 and D-038 APPROVED — CONDITIONAL (inactive). Q-042 Open; Q-043 Answered (D-038). Screening and pilot not started (no `screening/decisions.csv` or pilot file exists). No model training.

**Modified**: this file; `logs/PROMPT_LOG.md`; `research/reviews/daily_review_log.md`. **Created**: `logs/session_logs/2026-10-24_GOV-PR13-14-MERGE-RECORD.md`. **Not modified**: `DECISION_LOG.md`, decision records, code, tests, schemas, criteria, protocol, data.

## CORRECTION — 2026-10-24 — PR #15 published and merged (GOV-PR15-MERGE-RECORD)

**Scope**: log-only. This supersedes the "local, not pushed" and "Pull request: None" statements in the GOV-PR13-14-MERGE-RECORD entries above, in `PROMPT_LOG.md` and in that task's session log. Those statements were correct when written and are left unchanged. It records **PR #15** by number for the first time (CLAUDE.md §3.5).

**Verified `[EVIDENCE: GitHub API and git, checked 2026-10-24]`**

| Item | Value |
|---|---|
| PR | [#15](https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/15), "docs: record merges of PR #14 and PR #13 in governance logs (log-only)": **merged** |
| Source → target | `gov-pr13-14-merge-record` @ `4af0acb` (one commit, parent `694b389`) → `claude/happy-hawking-rxptfv` (base `694b389`) |
| Merged at / by | 2026-10-24 08:03:26 UTC (GitHub `merged_at`), `Arava-Sukeerthan` |
| Merge commit | `5c7d455`, parents `694b389` (base) and `4af0acb` (head); tree identical to `4af0acb` |
| Default branch | `claude/happy-hawking-rxptfv` at `5c7d455` |
| Merged content | `694b389..5c7d455` is identical to the reviewed PR #15 diff: `logs/CHANGELOG.md` (+20), `logs/PROMPT_LOG.md` (+12), `logs/session_logs/2026-10-24_GOV-PR13-14-MERGE-RECORD.md` (new, +14), `research/reviews/daily_review_log.md` (+7); 4 files, +53/−0, each appended after the last line of its file |

**Post-merge validation** (run on a copy of `5c7d455`): unit tests 69, OK; query table PASS, 158 rows; decision log 38 unique IDs (D-001–D-038), no duplicates, D-038 once. Real-data rebuild, raw-export verify and archive checksum **not run** (raw exports and git-ignored build files are not in the container). No CI is configured.

**Statuses confirmed unchanged**: D-036, D-037 and D-038 APPROVED — CONDITIONAL (inactive). Q-042 Open. Screening and pilot not started (no `screening/decisions.csv` or pilot file exists). No model training. D-039 not started.

**Final correction for this sequence**: this record closes the merge-history sequence for PRs #13–#15. Its own statements that it was prepared locally with no PR are accurate when written and will not be corrected by a further record created solely for that purpose; any publication of this record is shown by the git history and GitHub. Later governance records may still be needed for other work.

**Modified**: this file; `logs/PROMPT_LOG.md`; `research/reviews/daily_review_log.md`. **Created**: `logs/session_logs/2026-10-24_GOV-PR15-MERGE-RECORD.md`. **Not modified**: `DECISION_LOG.md`, decision records, code, tests, schemas, criteria, protocol, data.

## 2026-10-24 — PROTOCOL-DRAFT-001 (experimental protocol draft v0.1; nothing approved)

**Objective**: prepare a draft experimental protocol for review for the provisional NHANES laboratory-defined dysglycaemia study (owner prompt 2026-10-24). No training, evaluation, screening or pilot.

**Created**: `research/methodology/experimental_protocol_v0.1_draft.md` (draft v0.1; informs D-019 and D-013–D-018; changes no decision status).
**Modified**: `research/reviews/unresolved_questions.md` (Q-044–Q-058 appended, +15/−0); this file; `logs/PROMPT_LOG.md`; `research/reviews/daily_review_log.md`. **Created**: `logs/session_logs/2026-10-24_PROTOCOL-DRAFT-001.md`.
**Not modified**: `logs/DECISION_LOG.md` (no entry added or changed; the protocol's proposals are listed as FA-1–FA-13 inside the draft, for the researcher to record if wanted); `GOVERNANCE.md`; `CLAUDE.md`; `.gitignore`; `research_integrity.md`; code, tests, schemas; screening files.

**Evidence used** (all re-checkable):
- Official CDC codebook pages for the 32 required files (opened 2026-10-24 in the NHANES-VERIFY task, whose report was delivered in conversation and is not committed).
- The verified local raw files in git-ignored `data/raw/nhanes/`. All 32 were re-hashed against the local manifest in this task: 0 mismatches. No new download.
- Aggregate descriptive checks, with no modelling:
  - eligibility cascade: 3,088 and 2,485;
  - outcome prevalence 65.0% / 58.8% unweighted;
  - complete cases per predictor group;
  - 49 and 30 stratum × PSU clusters;
  - unit-consistency checks for the triglyceride, hs-CRP and urine-albumin equations.
- Inventory status of the candidate references: none is `verified`; two are `partially_verified` (P0303, P0256), so none is citable.

**Main findings recorded in the draft**:
- The primary candidate outcome is the majority class and dominated by FPG 100–125 mg/dL alone.
- The triglyceride equation is supported in mg/dL, not the "mg/L" stated in the text (Q-044).
- The hs-CRP equation is plausible only in mg/L; CDC's mean difference is not reproduced (Q-045).
- Insulin has no published cross-period equation (Q-047).
- `.gitignore` has no rule for participant-level model outputs (AB-10; not changed).

**Validation (actual outcomes)**:
- `python3 -I -m unittest discover -s tests/literature`: 69 tests, OK.
- `validate_search_queries.py`: PASS, 158 rows.
- `DECISION_LOG.md`: no diff; 38 unique IDs, no duplicates.
- `git ls-files`: no `.xpt` or `data/` path tracked.

**Not done**: no model training, evaluation, screening or pilot. No commit, push or PR (the owner prompt forbids pushing and PR actions; the work is uncommitted on local branch `claude/eloquent-mccarthy-bqtxr3`, based on default `eb79996`). The equations were transcribed but not yet re-checked character by character (AB-9).

## 2026-10-24 — PROTOCOL-DRAFT-002 (owner-authorized draft edits and data-protection safeguards; nothing approved)

**Authorization** (owner prompt, 2026-10-24), limited to three actions:
1. Retain FA-2 (HbA1c ≥ 5.7% OR FPG ≥ 100 mg/dL) as the **preferred proposed** primary outcome.
2. Exclude hs-CRP from the primary predictor set until the cross-period conversion discrepancy is resolved; apply no unverified equation.
3. Make draft-only protocol edits, add data-protection safeguards and tests, and update the permitted task logs.

**Preferred candidate vs approved decision.** The owner's preference is recorded inside the draft (CUP-5, CUP-12). **FA-2 is not approved.** It remains pending formal approval (D-019, D-014; GOVERNANCE.md §2) and verification of the ADA primary source (PMID 41358893 found; full text not read). No DECISION_LOG entry was added or changed.

**Modified**:
- `research/methodology/experimental_protocol_v0.1_draft.md` → v0.1 rev. 1:
  - FA-2 recorded as preferred, still pending; "either laboratory criterion, not a clinical diagnosis" made explicit;
  - S-15a (both tests, discordant negative) and S-15b (exploratory; discordant excluded, may inflate separability) added;
  - hs-CRP removed from groups A and B (A 21, B 27; complete-case counts recomputed: A 2,970 / 2,305, B 2,674 / 2,194);
  - unresolved conversion documented, with conditional S-16a (development period only, no conversion) and S-16b (temporal; only if Q-045 is resolved);
  - period prevalence differences labelled outcome-distribution findings;
  - verbatim CDC equation strings;
  - safeguards recorded; AB-10 left open.
- `.gitignore`: rules appended for raw/statistical-package files (XPT, sas7bdat, dta, rds; any case), participant-level directories (`/data/derived/`, `/outputs/participant_level/`, `/outputs/models/`, `/models/`), and columnar tables, arrays and serialized objects (any case). Existing rules unchanged.
- `research/reviews/unresolved_questions.md`: Q-059 appended (hs-CRP instrument timing within 2021–2023). No status changed.
- This file; `logs/PROMPT_LOG.md`; `research/reviews/daily_review_log.md`.

**Created**:
- `tests/data_protection/test_data_protection.py`: 6 checks, with limitations stated in its docstring.
- `outputs/README.md`: designates `outputs/aggregate/` as the only committed output location.
- `logs/session_logs/2026-10-24_PROTOCOL-DRAFT-002.md`.

**Evidence gathered in this task**: official CDC files fetched 2026-10-24 — `TRIGLY_L.htm`, `HSCRP_L.htm`, `HSCRP_J.htm`, and the method manuals TRIGLY-L-MET, HSCRP-J-MET, HSCRP-K-MET and HSCRP-L-MET.
- `[EVIDENCE: CDC documentation]` The hs-CRP bridging passage says "(mg/dL)", but the variable and all three method manuals use mg/L; the 2021–2023 instrument change happened "during the cycle".
- **Unresolved hs-CRP issue:** units (Q-045) and instrument timing (Q-059). No conversion applied.
- **Triglycerides (Q-044):** provisional documentary evidence for mg/dL; still open.
- **References:** none newly verified. The container could not reach any second bibliographic source.

**Validation (actual outcomes)**:
- `python3 -I -m unittest discover -s tests/literature`: 69 tests, OK.
- `python3 -I -m unittest discover -s tests/data_protection -v`: 6 tests, OK, none skipped.
- Negative control on a scratchpad copy of the working tree with synthetic bad files: the identifier, SAS-transport and format checks each failed as expected. The run also exposed case-sensitive extension rules, which were then made case-insensitive and retested (OK). The copy was deleted.
- `validate_search_queries.py`: PASS, 158 rows.
- `git ls-files -ci --exclude-standard`: 0 tracked files conflict with the new rules.
- `DECISION_LOG.md`, `GOVERNANCE.md`, `CLAUDE.md` and `research_integrity.md` unchanged.

**Not done / limitations**: no model training, evaluation, pilot, screening or protocol activation. No commit, push or PR: the work is uncommitted on local `claude/eloquent-mccarthy-bqtxr3`, together with the uncommitted PROTOCOL-DRAFT-001 files. The new test directory is not run by the `CLAUDE.md` test command (`tests/literature` only); it must be run separately until `CLAUDE.md` is updated through the proper route. The checks cannot detect participant data under unusual names or formats, renamed identifiers, or anything in Git history.

## 2026-10-24 — PROTOCOL-DRAFT-003 (Option A: corrections, reproducibility, data protection; commit and push authorized)

**Authorization** (owner prompt, 2026-10-24, "Option A"):
- make the specified protocol corrections;
- add reproducible aggregate-count scripts;
- strengthen the data-protection rules and tests;
- run the checks;
- commit and push the reviewed changes to the intended project branch.

No approval of FA-2, the protocol or any decision is implied.

**Modified**:
- `research/methodology/experimental_protocol_v0.1_draft.md` → v0.1 rev. 2. Scientific wording:
  - §5.1: the ADA confirmation-rule statement is now provisional (primary text not read);
  - §10: the CDC combining-periods wording now quotes `DEMO_L` ("urged to proceed with caution before combining"), replacing "advises against";
  - §18: the conformal "guarantee" is removed; it is stated as an unverified hypothesis, with coverage measured.

  Correction found by the reproduction check (§5.2): "median FPG 103 vs 101 mg/dL" was the median of a broader reference population (adults ≥ 18, diagnosed diabetes not excluded). The analytic-sample medians are 101 vs 100 mg/dL. The correction is recorded in the change history.

  Also: revision-2 safeguards recorded in §22. FA-2 stays preferred and unapproved; hs-CRP stays out of the primary sets; S-15a/b and S-16a/b unchanged.
- `.gitignore` (block appended; earlier rules untouched): SPSS any case; `.onnx`, `.pt`, `.pth`, `.safetensors`, `.cbm` and `.ubj` any case; archives and spreadsheets under `/data/`; archives under `/outputs/`. JSON is deliberately **not** ignored globally.
- `tests/data_protection/test_data_protection.py` (untracked file, rewritten): 10 tests.
  - Strict/skip Git handling; a `check-ignore` error is now a failure.
  - Content signatures for SAS transport, Parquet, NumPy and HDF5.
  - Validated identifier allowlist; detector self-tests on synthetic bytes.
  - More representative paths; limitations listed in the docstring.
- This file; `logs/PROMPT_LOG.md`; `research/reviews/daily_review_log.md`.

**Created**:
- `scripts/nhanes/descriptive_counts.py`: consolidates the scratchpad scripts; verifies the 32 input SHA-256 hashes; aggregate output only; no modelling.
- `scripts/nhanes/README.md`.
- `scripts/run_checks.sh`: literature tests, strict data-protection checks and the query-table check.
- `tests/data_protection/identifier_allowlist.txt` (no entries).
- `logs/session_logs/2026-10-24_PROTOCOL-DRAFT-003.md`.

**Verification (actual)**:
- `descriptive_counts.py` vs the draft: 85 values compared, 84 identical. The one difference is the median-FPG population labelling above, corrected rather than silently changed.
- Negative control (synthetic files in a scratchpad copy) found one test flaw: an invalid allowlist entry still exempted its file. It was fixed and re-checked: every planted problem detected; the documented limitations (`.txt` rows, JSON-format model) not detected, as stated.
- Missing-git simulation: default mode skipped; strict mode failed.
- The `check-ignore` error path itself was not exercised.
- Test results are in the session log.

**References**: none newly verified; reference status unchanged.
**Not done**: no training, evaluation, pilot, screening or activation. `CLAUDE.md`'s test command not changed (protected): the project-wide command is `sh scripts/run_checks.sh`.

## 2026-10-24 — PROTOCOL-EVIDENCE-001 (primary-source review: ADA criteria, NHANES laboratory comparability)

**Objective**: verify the ADA outcome criteria from the official article, and review the official CDC documentation for 2017–March 2020 and 2021–2023 hs-CRP and triglycerides (codebooks, method manuals, bridging text). No commit or push, per the prompt.

**Start state**: branch `claude/eloquent-mccarthy-bqtxr3` at `a4a2955`, clean, tracking `origin/claude/eloquent-mccarthy-bqtxr3`.

**ADA: blocked, not verified.**
- The official page (`diabetesjournals.org`), `doi.org`, PubMed Central and Europe PMC all failed from the container (HTTP 000).
- WebFetch: ENOTFOUND.
- PubMed full text for PMC12690183: empty.
- No ADA criterion, table or section is recorded as verified. New Q-061 asks for access.

**CDC evidence** `[EVIDENCE: CDC documentation, fetched 2026-10-24]`:
- Pages fetched: `HSCRP_L`, `P_HSCRP`, `TRIGLY_L`, `P_TRIGLY`, `BIOPRO_L`, `TCHOL_L`, `HDL_L`, `GHB_L`.
- Method manuals: HSCRP-J/K/L-MET and TRIGLY-J/K/L-MET.
- Cycle pages: lab methods, release notes and lab overview for 2021–2023.
- The hs-CRP/TG pages and manuals are byte-identical to the 2026-10-24 earlier reads.

**New finding.**
- The within-cycle change is not specific to hs-CRP:
  - HbA1c ("During the cycle … Tosoh G8 to the Bio-Rad D-100");
  - total cholesterol and HDL ("Cobas 6000 … to the Cobas 8000 during the cycle");
  - triglycerides and the biochemistry panel ("instrument change in the … cycle"; triglyceride method also changed).
- No date or participant indicator is published; `RIDEXMON` gives only a six-month season with no year.
- Applying the backward equations to every 2021–2023 record is therefore not established (Q-060).
- Units and other points are unchanged: hs-CRP stays unresolved (Q-045); triglycerides stay provisional mg/dL (Q-044).

**Modified**:
- `research/methodology/experimental_protocol_v0.1_draft.md` → rev. 3:
  - §5.1: laboratory category vs diagnosis; OR rule includes the diabetes range; population/outcome consistency check (no definition changed); ADA attempt recorded.
  - New §8.2 (CDC statements, unknowns, impact, recommendation).
  - S-09b proposed; limitation note; FA-5 note (recommendation only).
  - Q-059–Q-061 in §25; AB-8 note; CR-08 note; change history.
- `research/reviews/unresolved_questions.md`: Q-060 and Q-061 appended (Open).
- This file; `logs/PROMPT_LOG.md`; `research/reviews/daily_review_log.md`.

**Created**: `logs/session_logs/2026-10-24_PROTOCOL-EVIDENCE-001.md`.

**Not changed**: FA-2 (preferred, not approved); the target population and outcome; hs-CRP exclusion; DECISION_LOG and every status. No training, evaluation, activation, commit, push or merge. References other than the CDC documents are not newly verified.

### 2026-10-24 — PROTOCOL-COMMIT-001 (owner-authorized commit and push of PROTOCOL-EVIDENCE-001)
- **Authorization:** keep S-09b as a proposed, conditional sensitivity analysis; commit and push to `origin/claude/eloquent-mccarthy-bqtxr3` only.
- **Pre-commit wording clarification** in `experimental_protocol_v0.1_draft.md`, so the text states the owner's boundaries explicitly:
  - §8.2: unadjusted 2021–2023 values are **not** established as comparable, and the transition, unit discrepancy and timing remain limitations;
  - S-09b: "**Not executed**"; any future execution requires FA-5 approval and further documented methodological justification.
- No definition, outcome, population or status changed. FA-2 remains preferred and unapproved; the ADA evidence (Q-061) and Q-060 remain open.
- S-09b was not run, and no equation was applied.
- The commit hash is recorded in Git history and the task report, not in this file.

## 2026-10-24 — GOV-D040-RULE-S (record D-040: Rule S and Synthetic Verification Exemption; local edits only)

**Objective**: record the owner-approved Rule S and Synthetic Verification Exemption as D-040, add the approved cross-references (activation conditions K1–K4), create the header of the separate synthetic verification log, and update the task logs. **Local working-tree edits only; no commit, push, PR or remote contact** (owner authorization, 2026-10-24).

**Start state**: branch `claude/eloquent-mccarthy-bqtxr3` at `6deaac5`, clean, tracking `origin/claude/eloquent-mccarthy-bqtxr3`. Pre-edit checks: working tree clean; target sections unchanged; `D-040`, `Q-062`, `GOV-D040` and `logs/SYNTHETIC_VERIFICATION_LOG.md` absent.

**Owner approvals recorded** (owner prompts 2026-10-24): the governance-review C1 wording with the approved activation adjustment; K1–K4 as mandatory activation conditions; status APPROVED — CONDITIONAL (inactive); D-040 used, D-039 kept reserved; decision date 2026-10-24; `logs/SYNTHETIC_VERIFICATION_LOG.md`; the C2–C4 wording; scope A1, Rule S A2, date A3, protocol relationship A4 option (c), location A5, T10 excluded A6.

**Modified**:
- `logs/DECISION_LOG.md`: new section "Owner decision on synthetic software verification (added GOV-D040-RULE-S, 2026-10-24)" with D-040 (K1); new Status history row. No existing row changed.
- `CLAUDE.md` rule 13: the approved exception sentence referencing D-040 (K2).
- `GOVERNANCE.md` §2: the approved one-sentence cross-reference after the "No predictive model training" paragraph, added after K1 (K3).
- `logs/EXPERIMENT_LOG.md` header: the approved pointer to the synthetic verification log (K4).
- `research/reviews/unresolved_questions.md`: Q-062 appended (Open).
- This file; `logs/PROMPT_LOG.md`; `research/reviews/daily_review_log.md`.

**Created**: `logs/SYNTHETIC_VERIFICATION_LOG.md` (header only; no entries); `logs/session_logs/2026-10-24_GOV-D040-RULE-S.md`.

**Activation status**: the K1–K4 edits exist in the working tree but are **uncommitted**. D-040 stays **APPROVED — CONDITIONAL (inactive)**; no activation row was recorded. Whether the conditions count as satisfied while uncommitted is for the owner to decide (Q-062). All existing restrictions remain in force.

**Context**: the preceding read-only reviews in this session (F-A literature and full-text reviews, F-A specification, synthetic-test preparation, governance and environment proposals) changed no files and were not logged separately; they are summarised in the session log.

**Not changed**: the experimental protocol draft; every other decision and status (D-002 stays PROPOSED; D-017, D-019 PENDING; D-039 reserved and unused); `scripts/run_checks.sh`; tests. No test code, test plan, environment, package installation, test run, data access, model training or experiment. No commit, push, PR or remote Git operation.

**Validation**: see the session log. Local, read-only checks only (`git status`, `git diff`, ID uniqueness and table-structure checks). The existing test suites (`scripts/run_checks.sh`) were **not run**, because the authorization for this task excluded executing tests.

## 2026-10-24 — GOV-D040-ACTIVATION (Q-062 Option 1: commit, D-040 activation record, Q-062 closed; local edits only)

**Objective**: resolve Q-062 under the owner's Option 1, and record D-040's activation. **One owner-authorized local commit; no push, PR or remote contact** (owner prompts, 2026-10-24).

**Commit** (owner-authorized, local only): `c84323016c77b78b0cfb7ce6378a4adf91d515bb` on `claude/eloquent-mccarthy-bqtxr3` (parent `6deaac5`). It contains exactly the 10 GOV-D040-RULE-S files: `CLAUDE.md`, `GOVERNANCE.md`, `logs/CHANGELOG.md`, `logs/DECISION_LOG.md`, `logs/EXPERIMENT_LOG.md`, `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, `research/reviews/unresolved_questions.md`, `logs/SYNTHETIC_VERIFICATION_LOG.md` (new) and `logs/session_logs/2026-10-24_GOV-D040-RULE-S.md` (new). Pre-commit checks: nothing staged; no other change; diffs as recorded in GOV-D040-RULE-S. The GOV-D040-RULE-S entries above say "uncommitted"; that was true when written, and those changes are now in `c843230`. Not pushed: the branch is 1 commit ahead of `origin/claude/eloquent-mccarthy-bqtxr3`.

**K1–K4**: each present once, with the approved wording, in the committed files (`git show c843230:<path>`) and in the working tree.

**Modified (uncommitted; a further commit needs separate authorization)**:
- `logs/DECISION_LOG.md`: new Status history row (GOV-D040-ACTIVATION): D-040 `APPROVED — CONDITIONAL (inactive)` → **`APPROVED — CONDITIONAL (active; K1–K4 met in commit c843230)`**. Owner-approved label (Option (a)), following the existing conditional-approval and transition conventions. The D-040 decision row is unchanged (verified identical to `c843230`).
- `research/reviews/unresolved_questions.md`: Q-062 → **Closed**, quoting the owner's decision and the commit hash. Note: the file header lists "Open / Answered / Superseded"; "Closed" was used as explicitly authorized by the owner, and the header was not changed.
- This file; `logs/PROMPT_LOG.md`; `research/reviews/daily_review_log.md`.

**Created**: `logs/session_logs/2026-10-24_GOV-D040-ACTIVATION.md`.

**Not changed**: the D-040 decision text and its conditions; `logs/SYNTHETIC_VERIFICATION_LOG.md` (its rule is one entry per authorized run; none has occurred); every other decision and status. **D-040 activation does not authorize synthetic verification**: the test plan, test code, environment, installation and each run still need separate owner authorization, and no run is permitted before 2026-11-03. No test code, environment, package installation, test run, research-data access, model training or experiment. No push, PR, branch change or remote contact.

**Validation**: local, read-only checks only (`git status`, `git diff`, `git show`, K1–K4 string checks, table-column and ID checks). The test suites were not run (excluded by the authorization).

**Correction (2026-10-24, owner instruction)**: Q-062's status label changed from "Closed" to **"Answered"**, the documented status value (file header: Open / Answered / Superseded). The question, the owner's quoted decision and the commit reference are unchanged. The "Closed" statements above are kept as written. No other change.

**Correction (2026-10-24, owner-approved wording)**: Q-062's answer text now reads: "K1–K4 satisfied in the documentation committed in `c84323016c77b78b0cfb7ce6378a4adf91d515bb`. The activation entry (DECISION_LOG Status history, GOV-D040-ACTIVATION: APPROVED — CONDITIONAL (active; K1–K4 met in commit c843230)) was recorded afterwards, outside that commit." It replaces "Committed in `c84323016c77b78b0cfb7ce6378a4adf91d515bb`; activation recorded in the DECISION_LOG Status history (GOV-D040-ACTIVATION) as APPROVED — CONDITIONAL (active; K1–K4 met in commit c843230).", which could be read as saying the activation entry was committed in `c843230`. D-040's conditions and activation status are unchanged. These GOV-D040-ACTIVATION records and corrections are then committed in one owner-authorized local commit (hash in Git history and the task report); not pushed.

## LIT-005 — 2026-10-28 — Focused gap searches, transcript-derived notes and evidence review (no screening)

**Prompt objective**: researcher-authorised named searches (PubMed G-1…G-8, one alphaXiv search, Consensus G-5 if the quota permits); bibliographic verification where possible; document the 2026-10-24 conversation review as transcript-derived historical notes; thematic synthesis, gap matrix and contribution recommendation. No screening, no inclusion/exclusion decisions, no protocol, governance or decision changes, no participant-level data, no commit/push/PR.

**Governance**: searches executed under the researcher's LIT-005 instruction; D-005/D-006/D-007 remain PROPOSED. Screening stays blocked (D-035 record §6 conditions 2–6 unmet). Q-021 unchanged; PMC not treated as a second source.

**Completed**
- 8 PubMed searches, each recorded in `search_queries.csv` before execution and re-fetched with `sort=pub_date`; `pubrecords.py check-search` passed for all 8 (44, 27, 33, 68, 1, 21, 2, 244 hits).
- alphaXiv search: 15 ranked listings (structured transcription).
- Consensus G-5: **not executed** — monthly quota exhausted (resets 2026-11-01).
- PubMed metadata for the 395 PMIDs not in the inventory: 20 harness-saved responses copied unchanged; 394 returned, PMID 31314250 missing (Q-067).
- Second-source check: Crossref, doi.org and Europe PMC refused by the network policy (403). **No reference newly verified.**
- 24 new or re-found records read at abstract level; 2026-10-24 findings documented as transcript-derived notes with limitations.

**Created**
- `research/literature/reviews/LIT-005_evidence_review.md`
- `logs/session_logs/2026-10-28_LIT-005.md`
- 39 raw files in `research/literature/raw_exports/` (git-ignored, not committed): 18 PubMed search pages (9 original + 9 `CHECK-`), 20 metadata files, 1 alphaXiv file

**Modified (append only)**
- `research/literature/search_queries.csv` — 10 rows (G1–G8, AX-G9, CN-G5); existing rows unchanged
- `research/literature/raw_exports/MANIFEST.csv` — 39 rows; existing rows unchanged. `retrieved_at` of the new rows corrected the same day to transcript tool-result times (search pages) and harness file times (metadata); the provenance blocks inside the 19 transcribed raw files keep approximate placeholder times written by the session helper, as noted in each manifest row
- `research/reviews/unresolved_questions.md` — Q-063…Q-067
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file

**Not changed**: all generated literature artifacts (`paper_inventory.*`, `records/*`, `verification_report.md`, `search_execution_register.md`, `fulltext_review_candidates.csv`). Reason: `pubrecords.py build` stops in `verify_manifest` because the 205 LIT-003 raw exports are missing in this workspace (Q-063); hand-editing generated files was not done. Inventory remains 2,979 records. Protocol, decision log, governance files and `screening/` untouched.

**Validation (actually performed)**
| Check | Outcome |
|---|---|
| `validate_search_queries.py` | PASS, 168 rows |
| `pubrecords.py check-search` Q-PM-G1…G8 | passed ×8 |
| `pubrecords.py verify` | 39 new files match their checksums; 205 LIT-003 files reported missing (pre-existing) |
| `git diff` on CSVs | only appended lines; no historical line changed |
| Unit tests | not run (not required for documentation and registration changes; no code changed) |
| Rebuild | **not possible** (see above) |

**Errors / warnings**: one PubMed rate-limit error (retried once, succeeded); Consensus quota; network-policy blocks; PMID 31314250 not returned.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3`, base `53e419a`; changes uncommitted; no PR (not authorised).

**Correction (2026-10-28, LIT-005 pre-commit review; researcher-authorised C1–C10)**: the statements above are kept; these corrections apply.
| ID | Correction | Where |
|---|---|---|
| C1 | Screening-pilot blocker list (D-035 record §6, condition 6) replaced by the documented list in `final_confirmation_sheet_LIT-004.md` ("Pilot-blocking items after confirmation") plus `screening_protocol.md` B-6. Q-024 pair decisions and D-030 are no longer listed as blockers (the sheet says they are not pilot-blocking for the current pilot); the Q-036 arXiv spot-check, implementation of D-028/D-029/`biomarker_class`/scope flags, and Q-001/Q-002 are added | evidence review §8 |
| C2 | 2026-10-24 leads re-found: 7, not 3 (adds MacNell 2023, Kim 2026, Si 2025, Morrison 2024 from G-6) | evidence review §1.1 |
| C3 | Q-PM-11/12: 120 unique inventory records, not 121 (one record retrieved by both) | evidence review §6, §8 |
| C4 | Pre-task check 12:01Z; second-source check 12:13Z | session log (appended correction) |
| C5 | arXiv listings: "not checked against the inventory" (wrong cross-reference to §6 removed) | evidence review §1.1 |
| C6 | "New to the inventory" = not matched by PMID only; PMID-less inventory records not compared by DOI; rebuild duplicate check still needed. Applies also to "395 PMIDs not in the inventory" in this entry | evidence review §1, §1.1, §7; session log and daily review log (appended corrections) |
| C7 | The D-012 ≥ 10 % spot-check was not performed for the hand-copied file `Q-AX-G9_2026-10-28.json` | evidence review §1, §11; session log |
| C8 | 2026-10-24 notes "summarised from", not "quoted from", that report (the separately marked quotation is unchanged) | evidence review §3 |
| C9 | Q-065's feasibility statement marked as an assistant estimate `[HYPOTHESIS]` | `unresolved_questions.md` (correction note in the Q-065 row) |
| C10 | Review header: "prepared on base `53e419a`" | evidence review header |

No decision, question status, raw export, manifest row or search row was changed. No test, script, rebuild, search or network call was run for these corrections.

## LIT-005-PRESERVATION — 2026-10-28 — Archive of the 39 LIT-005 raw exports (no data, inventory or decision change)

**Prompt objective**: create a verifiable, deterministic archive of the 39 LIT-005 raw export files so the researcher can keep a copy outside the ephemeral container; record its status after the researcher's own checksum check.

**Preceding step (same day, researcher-authorised)**: the LIT-005 commit `db8493706affc5d556e284c13026190e206a1338` was pushed to `origin/claude/eloquent-mccarthy-bqtxr3` (fast-forward from `53e419a`).

**Completed**
- File list taken from the 39 `MANIFEST.csv` rows dated 2026-10-28 (all LIT-005); 39/39 present as regular files and matching their manifest SHA-256; no `data/` or NHANES path involved.
- Archive `research/literature/preservation/archive/LIT-005_raw_exports_2026-10-28.tar.gz` (479,473 bytes, SHA-256 `7b7d4674426c7581839b970cad37e21251ade0bf22d295814ac542bd7ec96ea1`): GNU tar with sorted names, fixed mtime, owner/group 0, fixed mode, file entries only; `gzip -n -9`; built twice, byte-identical.
- Companion files: `.tar.gz.sha256`, `LIT-005_SHA256SUMS.txt`, `LIT-005_archive_manifest.csv` (all git-ignored).
- Delivered to the researcher as attachments (twice; the second time the original archive was re-sent, not rebuilt).
- **Researcher-reported** (not observed by the assistant): the copy at `%USERPROFILE%\Downloads\LIT-005_raw_exports_2026-10-28.tar.gz` has the expected SHA-256.
- `research/literature/preservation/preservation_status.md`: LIT-005 section appended (+54 lines; LIT-003 content unchanged).

**Not changed**: raw exports, `MANIFEST.csv`, generated literature artifacts, inventory, protocol, screening criteria, decisions. The LIT-003 archive was not restored.

**Validation (actually performed, container side)**
| Check | Outcome |
|---|---|
| Archive entries vs the 39 manifest paths | identical; 39 regular files, no other entries |
| Extraction to a fresh temporary directory + `sha256sum -c LIT-005_SHA256SUMS.txt` | 39/39 OK |
| Two builds | byte-identical |
| `sha256sum -c` on the archive checksum file (before the second delivery) | OK |
| Archive git-ignored | yes (`research/literature/preservation/archive/`) |
| Tests, rebuild, searches, network calls | none |

**Status**: archive integrity verified (container and researcher-reported). **Off-device backup / disaster recovery remains outstanding**: one copy outside the container, on one laptop.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3`; documentation committed locally in one researcher-authorised commit (hash in Git history); not pushed; no PR.

**Status clarification (2026-10-29, documentation-only reconciliation; appended, the line above is kept as written)**: the line above was true when it was written. The local commit is `9bbd847d7256f1932f5c30f4f285f5189950a77d` (2026-10-28 12:56:35 UTC; subject "docs: record LIT-005 archive preservation status"; the 5 files named in the LIT-005-PRESERVATION section of `logs/session_logs/2026-10-28_LIT-005.md`). It is now on `origin/claude/eloquent-mccarthy-bqtxr3` (evidence: see the reconciliation entry at the end of this file). When it was pushed, and on whose authorisation, is not recorded. No PR.

## LIT-003-RESTORE — 2026-10-28 — Verification and restoration of the LIT-003 raw exports (no rebuild)

**Prompt objective**: verify the researcher-uploaded LIT-003 archive, then (separately authorised) restore its 205 raw JSON files into empty destinations in `research/literature/raw_exports/` and run `pubrecords.py verify`. No inventory rebuild, no Git operation during the restore.

**Completed (tool output)**
- Uploaded archive `/root/.claude/uploads/e89f2544-52ab-549f-965c-1d5f571bc462/e9f8022d-LIT-003_raw_exports_2026-10-23.tar.gz`: 3,647,967 bytes, SHA-256 `69e690f06834758aea76bca99ec4699c2abb2dac9aa776798aecf0366bd60c0e` (exact match, checked twice). A first upload was a 0-byte unrelated CSV and was not used.
- Listing: 211 entries (209 files + 2 directories); no unsafe paths or entry types.
- Extraction to a fresh scratch directory: `sha256sum -c SHA256SUMS.txt` 208/208 OK; `SHA256SUMS.txt` byte-identical to the committed `archive_contents_SHA256SUMS.txt`; the 205 raw JSON files match `MANIFEST.csv` and `raw_exports_inventory.csv` (0 hash or size mismatches).
- Restore: 205 files copied byte-for-byte with exclusive create; 0 destination conflicts; each copy re-hashed against the manifest. Archived `MANIFEST.csv`, `README.md` and inventory not used.
- `pubrecords.py verify`: `OK: all raw exports match MANIFEST.csv` for all 244 manifest files.
- **Researcher-reported** (not observed): the uploaded copy came from `%USERPROFILE%\Documents\BioML-Insight-Backup\`.

**Modified (documentation, append only)**: `research/literature/preservation/preservation_status.md` (status-history row + restoration section), `logs/PROMPT_LOG.md`, `logs/session_logs/2026-10-28_LIT-005.md`, `research/reviews/daily_review_log.md`, this file.

**Not changed**: raw exports already present, `MANIFEST.csv`, inventory, registry, generated artifacts, protocol, screening criteria, decisions, `unresolved_questions.md`. **Inventory not rebuilt.** Restored files are git-ignored and not committed.

**Status**: all 244 raw exports present and verified in this (ephemeral) workspace; rebuild precondition met. Q-063 remains **Open** (restore done for this workspace; rebuild pending). Off-device backup of both archives remains **outstanding**.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3` at `9bbd847`; documentation uncommitted; no PR.

**Status clarification (2026-10-29, documentation-only reconciliation; appended, the line above is kept as written)**: the line above was true when it was written. This documentation was later committed as `4acfce00f84d225f5c3be5480e282524f153598d` (2026-10-29 04:13:08 UTC; subject "docs: record LIT-003 raw-export restoration and verification"). `logs/session_logs/2026-10-29_LIT-005-REBUILD.md` records that commit as researcher-authorised. It is now on `origin/claude/eloquent-mccarthy-bqtxr3` (evidence: see the reconciliation entry at the end of this file). When it was pushed, and on whose authorisation, is not recorded. No PR.

## LIT-005-REBUILD — 2026-10-29 — Literature inventory rebuild with the LIT-005 records (no screening)

**Prompt objective**: researcher-authorised real rebuild (`pubrecords.py build`, then `make_literature_reports.py`) after a copy-based dry run and a preflight; compare with the dry run; stop and roll back on any change to existing paper IDs, merges of existing records, registry-prefix failure, or unexpected metadata or verification-status change. Theme mapping unchanged (researcher choice).

**Pre-checks**: clean tree at `4acfce0`; `pubrecords.py verify` OK (244 raw exports); `validate_search_queries.py` PASS (168 rows); unit tests OK (69 at the 2026-10-29 run); inventory checksum guard passed. Committed baseline exported (`git archive`) to the session scratchpad for comparison.

**Run**: 2026-10-29T05:44:51Z – 05:47:30Z; both scripts exit 0; nothing on stderr.

**Results (tool output)**
| Item | Result |
|---|---|
| Publications / inventory | 2,979 → 3,386; new paper IDs P2989–P3395 (407: 395 PubMed, 12 arXiv) |
| Registry | 10,785 → 12,268 rows; old rows an unchanged prefix (0 lines removed); 0 old keys re-mapped; new rows dated 2026-10-29 |
| Existing records | 0 IDs missing or re-mapped; 0 identifier, substantive-field or verification-status changes; no merge of existing records; registry conflicts unchanged (3 known pairs); duplicate-review pairs 15 → 15 |
| Expected changes to existing records | 43 gained query IDs (40 PMIDs re-found by G1/G2/G4/G8; 3 arXiv records by Q-AX-G9), none removed; 29 of them `unique` → `merged_duplicates` (their own new LIT-005 hit for the same identifier) |
| New records | 406 `partially_verified`, 1 `unverified` (P3383 = PMID 31314250, no metadata; Q-067); all `not_screened`; `retrieval_themes` empty (G queries not in `THEMES`; mapping unchanged by choice) |
| Search completeness | G1–G8 complete; no incomplete query |
| Comparison with the dry run | identical on every compared item |
| Validation | inventory valid against `paper_inventory.schema.json` (`collection_stats.json`: `valid`); CSV columns identical to the baseline; 0 duplicate PMID/DOI/PMCID/arXiv ID; no abstract column; `verify` OK after the run |

**Modified (generated, uncommitted)**: `paper_inventory.csv`, `paper_inventory.json`, `records/build_report.json`, `records/collection_stats.json`, `records/paper_id_registry.csv` (append only), `records/publications_index.csv`, `search_execution_register.md`, `verification_report.md`. `records/dedup_review.csv` and `fulltext_review_candidates.csv` were rewritten with identical content (no Git change). Created (git-ignored, contain abstracts): `records/source_records.jsonl`, `records/publications.jsonl`.

**Not changed**: raw exports, `MANIFEST.csv`, `search_queries.csv`, code, tests, theme mapping, protocol, screening criteria, decisions, question statuses. No screening; nothing becomes citable (Q-021, Q-064, D-035 §6 still open).

**Logging note**: `research/literature/collection_workflow.md` §5 says to log each build in `logs/EXPERIMENT_LOG.md`; that log's header limits it to experiments, and earlier builds were logged here and in session logs. This build is logged in this file and `logs/session_logs/2026-10-29_LIT-005-REBUILD.md`, as the researcher chose; the discrepancy is unresolved.

**Correction to the preflight report**: it first named 9 generated files; `records/dedup_review.csv` is also written by the build (10 tracked files in total).

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3` at `4acfce0`; rebuild and log changes uncommitted for researcher review; not pushed; no PR.

**Correction (2026-10-29, LIT-005-REBUILD; researcher-authorised C2 and C1)**: the statements above are kept; these corrections and notes apply.
- **C2 — blocked Consensus search recorded as executed.** `research/literature/search_queries.csv` row `Q-CN-G5@2026-10-28` (added in LIT-005, commit `db84937`) had `row_type = executed`, although the search never ran: the Consensus connector refused it for quota at 2026-10-28T12:09:07Z (status `blocked_quota`, no result, no export, no manifest row; LIT-005 evidence review §1 and session log). The generated `search_execution_register.md` therefore listed it under "Exact query strings as executed". Corrected: only that row's `row_type` changed to `capability_probe`, matching the 2026-10-23 precedent `LIT003-PROBE-17` (Consensus, `blocked_quota`); query text, date, status, identifiers and all other fields unchanged. `make_literature_reports.py` re-run (no rebuild; `row_type` is read only by the register section): `search_execution_register.md` no longer lists `Q-CN-G5`; the other 12 generated files (inventory CSV/JSON, index, registry, build report, collection stats, dedup review, full-text candidates, verification report, both `.jsonl` files) are byte-identical to before the correction. `validate_search_queries.py`: PASS, 168 rows.
- **C1 — known display limitation (not fixed).** The dated PubMed rows `Q-PM-G1…G8@2026-10-28` contain the date restriction in their stored query strings (`AND 2015/01/01:2026/10/28[edat]`; `date_limit` = "2015-01-01 to run date (entry date)"). The generated register shows an empty "Date restriction" column and "Filters: none" for these searches because `make_literature_reports.py` looks rows up by the base ID (`Q-PM-G1`), and only the dated `@2026-10-28` rows exist for LIT-005 (the LIT-003 queries also have base-ID planned rows). The report code and query schema were not changed; the register still displays the gap.

**Status clarification (2026-10-29, documentation-only reconciliation; appended, the "Branch / commit / PR" line above is kept as written)**: that line was true when it was written. The rebuild, the C1/C2 corrections and their log entries were later committed as `ffee9ec55ff346b55136a3d3c532b8dbae70b209` (2026-10-29 06:31:01 UTC; subject "data: rebuild literature inventory with LIT-005 records; correct Q-CN-G5 row type"; 11 files: the 8 generated files, `search_queries.csv`, this file and the session log). The repository does not record who authorised this commit. It is the head of `origin/claude/eloquent-mccarthy-bqtxr3` (evidence: see the next entry). When it was pushed, and on whose authorisation, is not recorded. No PR. `logs/PROMPT_LOG.md` and `research/reviews/daily_review_log.md` had no LIT-005-REBUILD entry; both were added in the next entry's task.

## Documentation-only reconciliation — 2026-10-29 — Record the commit and push state of LIT-003-RESTORE, LIT-005-PRESERVATION and LIT-005-REBUILD; record the branch recovery and post-recovery audit (log-only)

**Prompt objective** (researcher, 2026-10-29, "Task: Documentation-Only Reconciliation"; no task ID was assigned, and the label above is taken from the prompt title): carry out the documentation-only reconciliation that the post-recovery governance audit recommended. Documentation edits and non-destructive validation only: no commit, push, branch change, merge, PR, rebuild, restore, screening, experiment, decision change or question-status change.

**Preceding prompts in the same session (2026-10-29), recorded here because each needs a log entry**
- *Branch recovery*: the researcher authorised switching the session from `claude/gracious-hopper-rx64za` (`eb79996`, the default-branch head) to the existing `claude/eloquent-mccarthy-bqtxr3` if the remote branch pointed to `ffee9ec55ff346b55136a3d3c532b8dbae70b209` and the tree was clean. Both held. The single branch was fetched and a local tracking branch created; no reset, merge, commit or push. Checks: query table PASS (168 rows); unit tests 69, OK; `pubrecords.py verify` exit 1, all 244 raw exports missing and nothing else reported. No files changed.
- *Post-recovery governance audit* (read-only): it found the D-039 gap intentional (reserved by the researcher on 2026-10-24 for a screening-related proposal whose text is not in the repository). It also found the logging gaps corrected here, that `claude/eloquent-mccarthy-bqtxr3` is 8 commits ahead of the default branch `claude/happy-hawking-rxptfv` with no PR for them, and that D-035 record §6 conditions 2–6 are unmet. Inventory: 3,386 records, CSV SHA-256 matching `collection_stats.json`. No files changed; the only side effect was a `git fetch` of the default branch, which updated a remote-tracking ref inside `.git`.

**Evidence for the commit and push state (observed in this session)**
- `git log`: `9bbd847` (2026-10-28 12:56:35 UTC), `4acfce0` (2026-10-29 04:13:08 UTC) and `ffee9ec` (2026-10-29 06:31:01 UTC) are consecutive commits on `claude/eloquent-mccarthy-bqtxr3`.
- `git ls-remote origin refs/heads/claude/eloquent-mccarthy-bqtxr3`: `ffee9ec55ff346b55136a3d3c532b8dbae70b209`. This was observed at the start of the branch recovery and again in this task's preflight. `git merge-base --is-ancestor`: `9bbd847`, `4acfce0` and `db84937` are ancestors of the remote head.
- The repository does not record when these commits were pushed, by whom, or under which authorisation. The local reflog starts with this session's checkout. The push time is therefore not stated anywhere.
- GitHub PR listing (read-only, during the audit): the most recent PR is #16 (2026-10-24); no PR has `claude/eloquent-mccarthy-bqtxr3` at these commits as its head.

**Modified (append-only; no existing line changed or removed)**
- `logs/CHANGELOG.md`: status clarifications after the LIT-005-PRESERVATION, LIT-003-RESTORE and LIT-005-REBUILD entries; this entry.
- `logs/PROMPT_LOG.md`: detailed entries for LIT-005-REBUILD, the branch recovery, the post-recovery audit and this task. Each includes a note on the earlier entries whose Git status changed.
- `research/reviews/daily_review_log.md`: Day 16 entries for LIT-005-REBUILD and for the recovery, audit and reconciliation.

**Created**: `logs/session_logs/2026-10-29_DOCUMENTATION-ONLY-RECONCILIATION.md`.

**Not changed**: `logs/DECISION_LOG.md`, `research/reviews/unresolved_questions.md`, `research/literature/preservation/preservation_status.md`, `CLAUDE.md`, `GOVERNANCE.md`, generated inventory files, git-ignored files, code, tests, protocol, criteria. No D-039 entry. No question closed (Q-063 and Q-067 remain Open).

**Validation**: see the session log; the results are recorded there.

**Unresolved**: (1) who authorised the `ffee9ec` commit and the pushes of `9bbd847`, `4acfce0` and `ffee9ec`, and when the pushes happened; (2) `collection_workflow.md` §5 versus the `logs/EXPERIMENT_LOG.md` header on where builds are logged (unchanged); (3) Q-063's question text predates the restore and rebuild, and the raw exports are absent from the current container; its status is the researcher's decision; (4) the content of reserved D-039.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3` at `ffee9ec` (unchanged); changes uncommitted, awaiting the researcher's diff review; not pushed; no PR.

## SECOND-SOURCE-ACCESS-RECHECK — 2026-10-29 — Stage B: re-check of second-source verification access (Q-021, Q-064); no search, no verification change

**Prompt objective** (researcher, 2026-10-29: resume Stage B literature research and source verification; perform one bounded, non-screening task under existing approvals). No task ID was assigned; the label is the assistant's. The selected task was a dated re-check of access to independent bibliographic sources, plus a read-only count of which records each route could reach. Its purpose is to give the researcher current evidence for Q-021 and Q-064.

**Why this task was permitted**: it is non-screening, needs no raw exports and no participant-level data, executes no literature search, and changes no decision, question status or inventory. Not chosen: Q-036 spot-check (needs the absent raw exports and the researcher's answer), Q-067 re-request (an open question awaiting the researcher), any verification lookup (depends on Q-021/Q-064), screening (D-035 record §6 conditions 2–6 unmet).

**Completed (tool output)**
- Proxy status read (`$HTTPS_PROXY/__agentproxy/status`): enabled, not selective.
- One `curl` request each to 10 hosts (Crossref, doi.org, Europe PMC REST, E-utilities, PubMed web, PMC web, OpenAlex, Semantic Scholar, arXiv API, diabetesjournals.org), 14:50:09–14:50:11Z. All returned `CONNECT tunnel failed, response 403` (network policy). No response body was saved.
- Read-only counts from `paper_inventory.json`: 3,334 `partially_verified`; of these, 2,282 PubMed records with a PMCID, 964 PubMed records without one (including A2, `P0303`), 88 arXiv records awaiting the transcription spot-check.
- Found an inconsistency between the verification rule in `search_strategy.md` §7 / `research_plan.md` §6 and the second-source basis of the 14 `verified` records (web-search URL agreement on title and identifier only; `verification_report.md`). Recorded as Q-068; not resolved.

**Modified (append-only)**: `research/setup/environment_assessment.md` (2026-10-29 addendum); `research/reviews/unresolved_questions.md` (new row Q-068, Open); `logs/PROMPT_LOG.md`; `research/reviews/daily_review_log.md`; this file.
**Created**: `logs/session_logs/2026-10-29_SECOND-SOURCE-ACCESS-RECHECK.md`.

**Not changed**: decisions; existing question statuses (Q-021, Q-036, Q-063–Q-067 Open); `search_queries.csv` (no search executed, so no row); inventory and generated files; raw exports and manifest; code; tests; protocol; criteria; `CLAUDE.md` (its network note "re-checked 2026-10-23" is left as written; the 2026-10-29 result is in `environment_assessment.md`).

**Validation**: see the session log.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3` at `a280e01`; changes uncommitted, awaiting researcher review; not pushed; no PR.

## RESEARCH-AMBITION-D041 — 2026-10-29 — Research ambition and quality standard in `CLAUDE.md` and `README.md`; D-041 PROPOSED (documentation only)

**Prompt objective** (researcher, 2026-10-29): reflect the ambition of an original, rigorous, reproducible contribution suitable for a reputable journal of an established publisher. Add the proposed wording to `CLAUDE.md` and `README.md`, record D-041 as PROPOSED, and log the change. No task ID was assigned; the label is the assistant's. No staging, commit, push, branch change or PR.

**Conflicts reported before editing (none blocking)**: (1) the proposed rule 15 cited "(D-018)", which would imply D-018 already requires strong, recent baselines; it does not (D-018, PENDING: most-used RQ1 methods, a simple reference model, equal tuning budgets). It was reworded to "input to D-018, which is PENDING". (2) D-011 and D-022 (both PROPOSED) concern rules in `CLAUDE.md`; D-041 is recorded alongside them without changing their status (`CLAUDE.md` rule 10). (3) As with D-022, rules 14–17 are followed as researcher instructions while D-041 is PROPOSED. (4) Rules 14–17 sit in §1a, before §2 (rules 8–13); numbers are kept so existing references stay valid. (5) The tension between the 2026-11-24 manuscript target (protocol CUP-11, D-001 PROPOSED) and the ambition is unresolved and not decided here.

**Modified**
- `CLAUDE.md`: new section §1a (ambition statement, journal-selection criteria for D-020, rules 14–17), inserted before §2; no existing line changed.
- `README.md`: "Ambition" paragraph appended to "Research objective"; no existing line changed. The README status block (dated 2026-10-23) was left as it is.
- `logs/DECISION_LOG.md`: Status-history row for D-041; new section with the D-041 row (PROPOSED, "Not approved").
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file: task entries.

**Created**: `logs/session_logs/2026-10-29_RESEARCH-AMBITION-D041.md`.

**Not changed**: `GOVERNANCE.md`; D-001–D-040 (including D-011, D-013–D-020, D-022); question statuses; research question; dataset; protocol; method; baseline set; screening status; inventory; code; tests. The six uncommitted SECOND-SOURCE-ACCESS-RECHECK files are preserved (their existing content is unchanged; three logs were appended to).

**Validation**: see the session log.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3` at `a280e01`; uncommitted together with the SECOND-SOURCE-ACCESS-RECHECK changes; not staged, not pushed; no PR.

## SCREENING-ACTIVATION-BRIEF — 2026-10-29 — Decision brief for the unmet D-035 record §6 conditions (documentation only; screening stays inactive)

**Prompt objective** (researcher, 2026-10-29): verify that both uncommitted tasks are intact, then prepare a documentation-only screening-activation decision brief: the five unmet D-035 §6 conditions, the evidence each needs, blockers by kind, Q-065 (due 2026-11-01), the Q-068 verification conflict, the 2026-11-24 target, and next actions in dependency order. No task ID was assigned; the label is the assistant's. No search, screening, verification, training, decision change, staging, commit or push.

**Preflight**: branch `claude/eloquent-mccarthy-bqtxr3` at `a280e01`; nothing staged; no stashes. Both uncommitted tasks (SECOND-SOURCE-ACCESS-RECHECK, RESEARCH-AMBITION-D041) present; checksums and sizes recorded before editing.

**Created**: `research/reviews/screening_activation_decision_brief_D035.md`. No existing brief covered D-035 §6; the file sits with the other decision records in `research/reviews/`.
**Modified (append-only)**: `research/reviews/unresolved_questions.md` (Q-069, Open: gate order of protocol §23 vs `GOVERNANCE.md` §2); `logs/PROMPT_LOG.md`; `research/reviews/daily_review_log.md`; this file.
**Created (log)**: `logs/session_logs/2026-10-29_SCREENING-ACTIVATION-BRIEF.md`.

**Findings** (from the records): condition 1 met (D-036); conditions 2–6 unmet. D-031 C1 (R5/D-029) is the only open D-031 condition. No condition needs a network change. The rebuild in pilot-blocking item 8 and the arXiv spot-check in item 6 need the raw exports restored (Q-063). Criteria v1.1 and protocol v0.2 do not exist. Correction to the post-recovery audit report (conversation only, not in the repository): it listed D-032 among PROPOSED decisions. The Status history records D-032 as APPROVED — CONDITIONAL (inactive); its row keeps the original text by convention.

**Not changed**: decision statuses (including D-011, D-013–D-020, D-022, D-041); existing question statuses; `GOVERNANCE.md`; criteria; screening and experimental protocols; schemas; code; tests; inventory; raw exports. **Screening remains inactive.**

**Validation**: see the session log.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3` at `a280e01`; uncommitted together with the two earlier tasks; not staged, not pushed; no PR.

## Q-069-RESOLUTION — 2026-10-29 — D-042 PROPOSED (stage order before D-017–D-019 and training); protocol draft revision 4 (documentation only)

**Prompt objective** (researcher, 2026-10-29): after a read-only analysis of Q-069 and a reviewed proposal, record the researcher's in-principle resolution as D-042 (PROPOSED — awaiting explicit approval), keep Q-069 Open with a linking note, and revise the experimental protocol draft (§23, §26) to match. No task ID was assigned; the label is the assistant's. No screening, training, experiment, protocol freeze, decision approval, staging, commit or push.

**Contradictions found in the reviewed proposal and corrected before editing** (reported to the researcher):
1. §23 row P listed Rule S synthetic verification as "Ongoing". D-040 (7) says "No execution before 2026-11-03" and requires an approved test plan. Row P now covers Rule S test **planning** only and refers to D-040 (7).
2. §23 step 5 placed D-014 and the outcome definition (Stage F gate) after the Stage D gate. D-042 orders only D-017, D-018 and D-019. D-014/outcome now has its own row ("F"), with timing not fixed by D-042, but needed before D-017 (its evidence requirement) and before training (AB-3).

**Modified**
- `research/methodology/experimental_protocol_v0.1_draft.md`: header "Version" → draft revision 4; §23 replaced (dependency-ordered table; dates are targets, not gates; new risk line; new fallback that does not assume a frozen protocol); §26: new block "Before D-017, D-018 or D-019 is approved", AB-13, sentence "A blocker is not met because its date has arrived", AB-7 last sentence replaced (old sentence quoted in place), "Not blocking training" line replaced (old line quoted in place); change-history row "0.1 rev. 4" (Approved: **No**).
- `logs/DECISION_LOG.md`: Status-history row for D-042; new section with the D-042 row (PROPOSED — awaiting explicit approval; "Not approved").
- `research/reviews/unresolved_questions.md`: Q-069 status cell "Open" → "Open — researcher's in-principle answer (2026-10-29) prepared as D-042 (PROPOSED); awaiting explicit approval." (precedent: Q-032 and D-029). Status value unchanged.
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file: task entries.

**Created**: `logs/session_logs/2026-10-29_Q-069-RESOLUTION.md`.

**Not changed**: `GOVERNANCE.md`; `CLAUDE.md`; decision statuses other than the new D-042 (D-001, D-016–D-019 and all others unchanged); every other question; screening files; inventory; code; tests; data. Protocol not frozen or activated. **Screening remains inactive.**

**Validation**: see the session log.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3` at `eca5116`; uncommitted; not staged, not pushed; no PR.

## D-042-APPROVAL — 2026-10-29 — Researcher approval of D-042 recorded; Q-069 Answered; protocol references synchronised (documentation only)

**Prompt objective** (researcher, 2026-10-29): "I explicitly approve D-042 exactly as currently written in `logs/DECISION_LOG.md`." Record the approval following the governance and audit-log conventions; mark Q-069 Answered and link it to D-042; update only references made factually stale by the approval. No task ID was assigned; the label is the assistant's. No staging, commit or push.

**Convention note**: precedent for approving a PROPOSED entry is mixed. D-032's approval (2026-10-24) is recorded only in the Status history, with "Original D-032 row kept unchanged"; other PROPOSED rows had their status cell changed in place (e.g., D-003). As instructed, D-042's row had only its status cell (→ **APPROVED**) and "Approved by" cell (→ "Researcher (owner), 2026-10-29 — explicit approval of the text as written") updated; the decision text and rationale are byte-identical; the earlier status stays in the Status history.

**Modified**
- `logs/DECISION_LOG.md`: D-042 status and "Approved by" cells; Status-history row (PROPOSED — awaiting explicit approval → **APPROVED**); note under the D-042 table.
- `research/reviews/unresolved_questions.md`: Q-069 status → "**Answered 2026-10-29 by the owner** → D-042 (APPROVED): …", with the earlier status quoted (convention of Q-037, Q-039, Q-041). Question text and other columns unchanged.
- `research/methodology/experimental_protocol_v0.1_draft.md`: header → draft revision 5; five references "D-042, proposed" → "D-042, approved 2026-10-29" (§23 intro; §26 block heading, AB-7, AB-13, submission line); change-history row "0.1 rev. 5" (Approved: **No**). The revision 4 row keeps its wording.
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file: task entries.

**Created**: `logs/session_logs/2026-10-29_D-042-APPROVAL.md`.

**Not changed (historical, accurate when written)**: earlier CHANGELOG, PROMPT_LOG, daily-review and session-log entries that describe D-042 as PROPOSED; `research/reviews/screening_activation_decision_brief_D035.md` (it records Q-069 as opened). **Not changed (protected or out of scope)**: `GOVERNANCE.md`; `CLAUDE.md`; D-001, D-016–D-019 and every other decision status; every other question status.

**What the approval does not do**: it passes no gate (the Stage C and Stage D gates are not passed); it does not activate screening, authorise real-data training or experiments, approve D-016–D-019, freeze the protocol, or relax the Stage B verification requirement. **Screening remains inactive.**

**Validation**: see the session log.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3` at `9aefe42`; uncommitted; not staged, not pushed; no PR.

## Q-065-DECISION-PACKAGE — 2026-10-29 — Q-065 scope and schedule decision package; audit-trail reconciliation of commits and pushes (documentation only)

**Prompt objective** (researcher, 2026-10-29): prepare a researcher-reviewable decision package for Q-065 with the schedule analysis (D-001, Q-013, Q-058, CUP-11 under D-042); compute the priority-strand counts from committed metadata only, with an independent check; reconcile the audit trail for commits `24f5dfd`, `27c86c0`, `eca5116`, `9aefe42`, `5d92d94`. No task ID was assigned; the label is the assistant's. No screening, labelling, searches, downloads, training, decision change, staging, commit or push.

**Preceding request (same session, not executed)**: a request to commit the 11 LIT-005-REBUILD files was interrupted by the researcher. That commit already exists as `ffee9ec` and is on `origin`; nothing was staged or committed.

**Created**: `research/reviews/Q-065_decision_package.md`; `logs/session_logs/2026-10-29_Q-065-DECISION-PACKAGE.md`.
**Modified (append-only)**: `logs/PROMPT_LOG.md`; `research/reviews/daily_review_log.md`; this file.

**Results (computed from `paper_inventory.json`, SHA-256 `a509538d…f4a3`, metadata fields only)**: G-1…G-7 194; Q-PM-02 743; Q-PM-11/12 120; overlaps 10 (G ∩ Q-PM-02), 0 (G ∩ Q-PM-11/12), 3 (Q-PM-02 ∩ Q-PM-11/12), 0 (all three); union **1,044**. Confirmed independently on `paper_inventory.csv` (membership-pattern counting) and with `jq`. Alternative scope sizes: priority + remaining RQ1 strands (Q-PM-01, Q-PM-03) 1,470; entire inventory 3,386. No title or abstract was read; no record was sampled or labelled.

**Audit-trail reconciliation (verified from Git; earlier entries kept as written)**
The CHANGELOG and PROMPT_LOG entries for SECOND-SOURCE-ACCESS-RECHECK, RESEARCH-AMBITION-D041, SCREENING-ACTIVATION-BRIEF, Q-069-RESOLUTION and D-042-APPROVAL say "uncommitted" and "not pushed". That was true when each was written. Their later state:

| Commit | Commit time (UTC) | Subject | Pushed (remote-tracking reflog, "update by push") |
|---|---|---|---|
| `24f5dfd6ef1c526acc67fc585864f22faa7d8766` | 2026-10-29 15:12:36 | docs: record literature access re-check | with `eca5116`, 2026-10-29 15:13:15 (`a280e01..eca5116`) |
| `27c86c0469c5d615c038d0e10b1283b27a5c44f5` | 2026-10-29 15:12:50 | docs: document research ambition and D-041 proposal | with `eca5116`, 2026-10-29 15:13:15 |
| `eca5116319dc5af3f0968c1195a7c3e99469f704` | 2026-10-29 15:13:07 | docs: add screening activation decision brief | 2026-10-29 15:13:15 |
| `9aefe42aca800769d2c089ad5de60aa82be00991` | 2026-10-29 15:28:07 | docs: record Q-069 resolution proposal | 2026-10-29 15:29:25 (`eca5116..9aefe42`) |
| `5d92d94286a0a8257222a662241b016c545618d5` | 2026-10-29 15:36:38 | docs: record D-042 approval | 2026-10-29 15:40:56 (`9aefe42..5d92d94`) |

Additional, same pattern: `a280e01` (DOCUMENTATION-ONLY-RECONCILIATION; its entry says "not pushed") was pushed at 2026-10-29 14:47:14 (`ffee9ec..a280e01`). Evidence: `git log`; `git reflog show --date=iso origin/claude/eloquent-mccarthy-bqtxr3`; `git merge-base --is-ancestor` (all six on `origin/claude/eloquent-mccarthy-bqtxr3`); `git ls-remote` → `5d92d94`. Commits and pushes were made in this session on the researcher's explicit authorisation (three commits + push; then commit, push; then commit, push). No PR exists for these commits.

**Not changed**: Q-065 (Open); every decision status; every question status; `GOVERNANCE.md`; `CLAUDE.md`; the protocol (draft revision 5, not approved); inventory and generated files; code; tests. **Screening remains inactive.**

**Validation**: see the session log.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3` at `5d92d94`; uncommitted; not staged, not pushed; no PR.

## SCOPE-SCHEDULE-DECISIONS — 2026-10-29 — Owner decisions on Q-002 (D-043), Q-065 (D-044) and the schedule (D-045) recorded (documentation only)

**Prompt objective** (researcher, 2026-10-29): record the researcher's explicit decisions on Q-002 (biomarker scope), Q-065 (screening scope, Option 3) and the project schedule, after verifying the Q-065 count; no screening activation, no experiment authorisation, no change to unrelated decisions. No task ID was assigned; the label is the assistant's. No staging, commit or push.

**Pre-checks**: branch `claude/eloquent-mccarthy-bqtxr3` at `5d92d94`, in sync with `origin`; uncommitted Q-065-DECISION-PACKAGE work (5 files) present and snapshotted (checksums and sizes) before editing. D-043–D-045 unused (D-039 reserved).

**Count verification (before recording)** — `paper_inventory.json` SHA-256 `a509538d…f4a3` and `paper_inventory.csv` `8fc5bea9…6846`, both equal to HEAD. RQ1 = Q-PM-01, Q-PM-02, Q-PM-03 (`search_queries.csv`, column `rq`). Method 1: `jq` set union on the JSON → G 194, Q-PM-02 743, Q-PM-11/12 120, Q-PM-01 434, Q-PM-03 52; priority 1,044; Option 3 **1,470**. Method 2: Python `csv` on the CSV, five-set membership patterns and inclusion–exclusion → **1,470**. Decomposition: 1,044 + 399 (Q-PM-01 outside the priority strand) + 44 (Q-PM-03 outside) − 17 (in both) = 1,470. The package states 399 and 44 but not the 17 overlap; no discrepancy in the total. Metadata of the 1,470: all `not_screened`; 1,460 `partially_verified`, 10 `verified`; 6 `abstract_available = False`; 2 retraction publication types; 0 duplicate PMID/DOI/PMCID; 4 pending dedup pairs touch the set, 1 with both members inside (caveat recorded in D-044). Metadata only; no title or abstract read.

**Modified**
- `logs/DECISION_LOG.md`: three Status-history rows; new section with D-043 (APPROVED), D-044 (APPROVED — CONDITIONAL, inactive for screening until D-035 record §6 is met), D-045 (APPROVED); attribution "Researcher (owner), 2026-10-29".
- `research/reviews/unresolved_questions.md`: Q-002 → Answered → D-043; Q-065 → Answered → D-044; Q-013 and Q-058 stay **Open** with notes referring to D-045 (D-001 revision pending pilot evidence).
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file: task entries.

**Created**: `logs/session_logs/2026-10-29_SCOPE-SCHEDULE-DECISIONS.md`.

**Not changed**: D-001 (PROPOSED), D-005, D-009, D-013–D-020, D-025, D-035, D-042 and every other decision; Q-001, Q-007, Q-033, Q-035 and every other question; `GOVERNANCE.md`; `CLAUDE.md`; `screening_criteria.md` (v1.0 draft; D-043 enters only via v1.1); the experimental protocol (draft revision 5; CUP-11 and §23 wording not updated, see open items); the Q-065 decision package; the inventory and all record fields. **Screening remains inactive**; no training, experiment or dataset work authorised.

**Open items**: protocol CUP-11 ("Target: a defensible manuscript by 2026-11-24") and §23 ("The 2026-11-24 target is under review") predate D-045 and need an owner-authorised protocol revision; `screening_criteria.md` §2.2 still reads "[PROVISIONAL — Q-002]" until v1.1; D-001 revision after the pilot.

**Validation**: see the session log.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3` at `5d92d94`; uncommitted together with the Q-065-DECISION-PACKAGE work; not staged, not pushed; no PR.

## D-051-GOVERNANCE-APPROVAL — 2026-10-30 — Owner approval of the `GOVERNANCE.md` §2 Rule S sentence recorded as D-051 (documentation only)

**Context**: the PR #17 merge-readiness review (2026-10-30) found that the D-040 records do not settle whether the conditional approval of D-040 satisfies the `GOVERNANCE.md` rule "It must not be changed without a DECISION_LOG entry approved by the researcher". The researcher asked for a separate entry on the PR-1 branch before PR #17 is merged (Option A of the review) and approved the exact sentence on 2026-10-30.

**Modified**
- `logs/DECISION_LOG.md`: one Status-history row; new section with D-051 (APPROVED; Researcher (owner), 2026-10-30), quoting the approved sentence and the researcher's scope statement verbatim. D-040 and every other entry unchanged.
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file: task entries.

**Created**: `logs/session_logs/2026-10-30_D-051-GOVERNANCE-APPROVAL.md`.

**Not changed**: `GOVERNANCE.md` (the approved sentence is unchanged); `CLAUDE.md`; D-040 and all other decisions; all questions; the protocol (draft revision 5, not approved, not frozen, not active); schemas; inventory; scripts; tests. **Screening remains inactive.** No test planning, test code, environment specification or creation, package installation, synthetic verification, experiment or model training; NHANES data not accessed.

**Not recorded (proposals only, not approved)**: D-040 scope after the merge; a definition of "F-A software" before any Rule S test plan; the restriction on NHANES-derived values in synthetic work.

**Validation**: see the session log.

**Branch / commit / PR**: prepared for `claude/eloquent-mccarthy-bqtxr3-part1` on top of `0c85634` (PR #17); uncommitted when written; not pushed.

## LIT-PRESERVATION-V1-V5 — 2026-10-30 — LIT-003 and LIT-005 archives verified and restored; LIT-005 per-file evidence prepared in this change set (documentation and evidence only)

**Context**: the preservation audits of 2026-10-30 concluded "Preservation evidence partially established; closure pending". The researcher uploaded both archives and authorised V1 (archive checksums), V2 (LIT-005 listing and safety checks), V3 (LIT-005 temporary extraction and per-file check), V4 (restoration of both and full `verify`) and V5 (this documentation and the LIT-005 listing), each separately.

**Created**
- `research/literature/preservation/LIT-005_archive_contents_SHA256SUMS.txt`: 39 per-file SHA-256 lines (archive entry paths), sorted.
- `research/literature/preservation/LIT-005_raw_exports_inventory.csv`: 39 rows, same columns as the LIT-003 `raw_exports_inventory.csv`.
- `logs/session_logs/2026-10-30_LIT-PRESERVATION-V1-V5.md`.

**Modified**
- `research/literature/preservation/preservation_status.md`: one status-history row each for LIT-003 and LIT-005; new final section with the V1–V4 results, the new evidence files, and the researcher-reported Google Drive check (not observed).
- `research/reviews/unresolved_questions.md`: Q-063 status cell only ("Open — partly addressed", with what remains); question text and status unchanged in substance (still Open).
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file: task entries.

**Results (tool output)**: LIT-003 3,647,967 bytes, SHA-256 `69e690f0…0c0e`, 205/205 raw files match `MANIFEST.csv`, 4 companion files match committed records (not restored); LIT-005 479,473 bytes, SHA-256 `7b7d4674…6ea1`, safety checks passed, 39/39 match; 244/244 restored with exclusive create; `pubrecords.py verify` exit 0, `OK: all raw exports match MANIFEST.csv`; `MANIFEST.csv` and `README.md` unchanged; archives unchanged.

**Not changed**: `MANIFEST.csv`, `README.md`, `archive_contents_SHA256SUMS.txt`, `raw_exports_inventory.csv`, the inventory and all generated records (no build), decisions, protocol, screening status (inactive). The 244 restored raw files are git-ignored and exist only in this workspace.

**Open**: backup on a separate physical device; Google Drive approval as project storage; Q-063 closure (researcher).

**Validation**: see the session log.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `ec52627`; uncommitted when written; not pushed.

## LIT-PRESERVATION-GDRIVE — 2026-10-30 — Google Drive approval recorded as researcher-reported (documentation only)

**Context**: the researcher reported on 2026-10-30 that explicit approval has been obtained from "the project owner or supervisor" to use their personal Google Drive for research archives, and that both archives are in a private folder in the researcher's personal Google Drive. Neither the approval details nor the Drive copies were verified by the assistant.

**Modified**
- `research/literature/preservation/preservation_status.md`: one status-history row each for LIT-003 and LIT-005; new final section "Google Drive copies: approval reported (2026-10-30)" with four parts: researcher-reported approval; approval details not yet recorded or verified; archive integrity verification (assistant-observed vs researcher-reported); the unresolved backup-requirement decision.
- `research/reviews/unresolved_questions.md`: Q-063 status cell only (Google Drive clause); status still Open.
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file: task entries. `logs/session_logs/2026-10-30_LIT-PRESERVATION-GDRIVE.md`: new.

**Not changed**: earlier preservation entries; `MANIFEST.csv`, `README.md`, the restored raw files and the archives; decisions (no DECISION_LOG entry: approver, date, scope and conditions not recorded); protocol; screening status (inactive). Google Drive not accessed. Preservation not marked complete; backup on a separate physical device outstanding.

**Validation**: see the session log.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `78e4269`; uncommitted when written; not pushed.

## Q-011-OPTION-B and SCREENING-READINESS-RECHECK — 2026-10-30 — off-device backup designated; screening readiness re-checked (documentation only)

**Context**: the researcher selected Q-011 option (b) (private Google Drive folder as the off-device backup), reported the project owner's approval via WhatsApp (date and wording not provided) and supplied the SHA-256 values of the Drive copies; and asked whether screening can start before a 2026-11-02 interim deliverable.

**Modified**
- `research/literature/preservation/preservation_status.md`: one status-history row each for LIT-003 and LIT-005; new final section "Off-device backup designated (Q-011 option (b), 2026-10-30)". Status not changed to PRESERVED.
- `research/reviews/unresolved_questions.md`: Q-011 and Q-063 status cells (update notes); both still Open.
- `research/reviews/screening_activation_decision_brief_D035.md`: new §11 (dated status update; §1–§10 unchanged).
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file: task entries. `logs/session_logs/2026-10-30_Q-011-OPTION-B_SCREENING-READINESS.md`: new.

**Not changed**: `DECISION_LOG.md` (D-010 stays PROPOSED pending a one-line confirmation that option (b) approves it as written); screening status (INACTIVE; D-035 §6 conditions 2–6 unmet); protocol, criteria, scope, inventory, raw exports. No screening, sampling, labelling, experiment or training. Google Drive and the approval message not accessed.

**Validation**: see the session log.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `f60a23b`; uncommitted when written; not pushed.

## D-010-APPROVAL — 2026-10-30 — D-010 approved under Q-011 option (b) (decision record)

**Context**: explicit researcher approval (2026-10-30): "I explicitly approve D-010 under Q-011 Option B, designating my private personal Google Drive folder as the off-device backup location for the literature exports, subject to the applicable governance requirements and outstanding preservation checks."

**Modified**
- `logs/DECISION_LOG.md`: D-010 row Status and "Approved by" cells (PROPOSED → **APPROVED**, as for D-042); one Status history row (D-010-APPROVAL); one note line after the first table. Decision text and rationale unchanged.
- `research/reviews/unresolved_questions.md`: Q-011 → **Answered** (D-010); Q-011 and Q-063 update notes adjusted; Q-063 still Open.
- `research/literature/preservation/preservation_status.md`: Q-011-OPTION-B rows annotated; part 5 added to the final section. Not PRESERVED.
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file; session log `2026-10-30_Q-011-OPTION-B_SCREENING-READINESS.md` (addendum).

**Not changed**: other decisions; screening (INACTIVE); protocol; inventory; raw exports.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `f60a23b`; uncommitted when written; not pushed.

## SCREENING-PREREQ-DECISIONS — 2026-10-30 — researcher selections recorded; recommendations and approval request for the remaining screening prerequisites

**Context**: the researcher's prompt of 2026-10-30 stated selections on Q-040, Q-001, Q-033, D-027, Q-036 and D-008 (Q-011/D-010 were recorded earlier the same day) and asked for evidence-based recommendations on the remaining choices.

**Created**
- `research/reviews/screening_prerequisites_decision_package.md`: recorded selections; recommendations on Q-035, D-028, D-029/R5/Q-032, D-024, Q-007, D-025, A-1–A-6; D-035 §6 activation table; critical path; approval request.
- `logs/session_logs/2026-10-30_SCREENING-PREREQ-DECISIONS.md`.

**Modified**
- `logs/DECISION_LOG.md`: new section with D-055 (Q-040), D-056 (Q-001), D-057 (Q-033), all APPROVED — CONDITIONAL (inactive for screening); D-027 → APPROVED (limited) and D-008 → APPROVED — CONDITIONAL, Status and "Approved by" cells updated in place; Status history rows, including D-012/D-023 unchanged (PROPOSED until the arXiv spot-check passes).
- `research/reviews/unresolved_questions.md`: Q-001, Q-008, Q-033, Q-036, Q-040 → Answered.
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file: task entries.

**Not changed**: screening (INACTIVE; D-035 §6 conditions 3–6 unmet); protocol, criteria, scope (D-044), inventory; D-013–D-020; Q-063. No spot-check, screening, experiment or training.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `f60a23b`; uncommitted when written; not pushed.

## SCREENING-PREREQ-DECISIONS-2 — 2026-10-30 — remaining screening decisions recorded; arXiv spot-check passed; criteria v1.1 and protocol v0.2 drafted

**Context**: the researcher delegated the selection of the recommended options (`screening_prerequisites_decision_package.md` §2), authorised their recording, and asked for the Q-036 arXiv spot-check and drafts of criteria v1.1 and protocol v0.2.

**Created**
- `research/literature/reviews/arxiv_transcription_spot_check_2026-10-30.md` and `.csv`: 25/25 sampled records match in 5/5 files (seeded sample, ≥ 10 %, min 5 per file).
- `research/literature/screening_criteria_v1.1_draft.md`, `research/literature/screening_protocol_v0.2_draft.md`: drafts, not frozen; v1.0 and v0.1 unchanged.
- `logs/session_logs/2026-10-30_SCREENING-PREREQ-DECISIONS-2.md`.

**Modified**
- `logs/DECISION_LOG.md`: new D-058 (Q-035), D-059 (A-1–A-6), D-060 (R5, Q-032); D-009, D-024, D-025, D-028, D-029 approved (conditional/not implemented as stated); D-012, D-023 approved (spot-check passed); D-026 revised by D-029; Status history rows; D-030 unchanged.
- `research/reviews/unresolved_questions.md`: Q-007, Q-026, Q-032, Q-035 answered; Q-034 proposed resolution noted (Open); new Q-073 (pilot strata in the D-044 scope).
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file: task entries.

**Not changed**: `MANIFEST.csv` (spot-check outcome not yet recorded there), raw exports, inventory, schemas, code, `screening_criteria.md` v1.0, `screening_protocol.md` v0.1, scope (D-044), protocol, D-013–D-020. Screening INACTIVE; no sample.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `f60a23b`; uncommitted when written; not pushed.

## SCREENING-PREREQ-DECISIONS-3 — 2026-10-30 — OPEN-1/OPEN-2 settled; Q-073 recommendation; arXiv spot-check recorded in MANIFEST.csv

**Modified**
- `logs/DECISION_LOG.md`: new D-061 (flag `non_metabolic_rq5_candidate`) and D-062 (RQ5 tier rule), both APPROVED — CONDITIONAL (effective at the v1.1 freeze); Status history rows (D-025 unchanged pending Q-073; D-012 spot-check recorded).
- `research/literature/raw_exports/MANIFEST.csv`: `transcription_check=passed` and a note for Q-AX-01…05 only (`pubrecords.py set-check`; dry run on a copy first; `verify` OK).
- `research/reviews/unresolved_questions.md`: Q-073 recommendation (near-equal allocation), still Open.
- `research/literature/screening_criteria_v1.1_draft.md`, `screening_protocol_v0.2_draft.md`: OPEN-1/OPEN-2 resolved, Q-073 recommendation, spot-check status; still DRAFT.
- `research/literature/reviews/arxiv_transcription_spot_check_2026-10-30.md`: recording status.
- `research/reviews/screening_prerequisites_decision_package.md`: §6 review summary and implementation readiness.
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file; session log `2026-10-30_SCREENING-PREREQ-DECISIONS-3.md` (new).

**Not done**: implementation and rebuild (reasons in the package §6.3); no build run; no freeze; screening INACTIVE.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `f60a23b`; uncommitted when written; not pushed.

## Q-073-DECISION — 2026-10-30 — D-063 pilot allocation approved (conditional, inactive)

Explicit researcher approval of the near-equal allocation (B 8, A 8, untagged 8, F 8, C 7, E 7, D 7, Q 7; seed 4004; fixed stratum order; deterministic draw; inventory hash). Recorded as D-063 (APPROVED — CONDITIONAL, inactive) revising D-025's allocation; Q-073 Answered; protocol v0.2 §7, §10, §11 and criteria v1.1 §9, §10 updated (still DRAFT). No sample generated; screening INACTIVE. Committed in the preservation commit of the same day (17 files).

## Q-068-DECISION — 2026-10-30 — D-064 recorded (Step A: decision and documentation only)

**Context**: explicit researcher approval: "Approve D-064 with A5 = needs_review and A6 = report-level only. Authorize Step A only."

**Modified**
- `logs/DECISION_LOG.md`: new section with D-064 (APPROVED; takes effect at the next authorised build) and one Status history row.
- `research/reviews/unresolved_questions.md`: Q-068 → Answered (D-064); question text unchanged.
- `research/literature/collection_workflow.md` §4.3: new §4.3.1 (approved D-064 policy, implementation pending); existing table kept as §4.3.2 (rules of the current build).
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file: task entries; `logs/session_logs/2026-10-30_Q-068-DECISION.md` (new).

**Not changed**: code (`pubrecords.py`, `make_literature_reports.py`), tests, schemas, inventory and generated reports (incl. `verification_report.md`), verification statuses, D-044 scope and snapshot, criteria and protocol drafts, screening status (INACTIVE). Steps B, C, D not authorised.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `ee0d7de`; uncommitted when written; not pushed.

## D-064-STEP-B — 2026-10-30 — D-064 implemented in code and tests (no build)

**Context**: researcher authorisation of Step B with decisions D2 (first-author rules), D3 (modify `test_spot_check_upgrades_verification`; add a negative Consensus test) and D4 (no "arXiv" venue).

**Modified**
- `scripts/literature/pubrecords.py`: new `normalize_venue`, `compare_first_author`, `compare_identifiers`, `compare_required_fields`, `source_provider`, `source_independence`, `evaluate_second_sources`; `auto_verification` applies D-064 after the unchanged existing checks; `build()` writes report-level `verification_second_sources` and `verification_status_changes` into `build_report.json`. `merge_cluster`, `deduplicate`, `normalize_journal` and the schemas are unchanged; publication records gain no field.
- `scripts/literature/make_literature_reports.py`: D-064 rule text replaces the old web-second-source sentence; new sections "Second-source evaluation (D-064; report-level only)" and "Verification status changes since the previous build".
- `tests/literature/test_pubrecords.py`: `test_spot_check_upgrades_verification` now uses a synthetic, checked Crossref source; new `test_consensus_without_underlying_source_does_not_verify`; new classes `TestD064Helpers` (6 tests) and `TestD064Build` (11 tests). All fixtures synthetic.
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file; session log `2026-10-30_D-064-STEP-B.md` (new).

**Not changed**: inventory, generated reports, `records/`, verification statuses, raw exports and manifest, schemas, D-044 snapshot, criteria/protocol drafts, screening (INACTIVE). No build run.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `5cd9fc3`; uncommitted when written; not pushed.

## T0-GOVERNANCE-DECISIONS — 2026-10-31 — D-065, D-066, D-067 recorded; Q-022 answered; GOVERNANCE.md Stage B row amended

**Context**: researcher approval (2026-10-31) of the final T0 wording and authorisation to record it. Commit and push are not authorised by this task.

**Modified**
- `logs/DECISION_LOG.md`: new section with D-065 (Q-022: 35 recorded search executions approved as executed with limitations; 30 planned searches not searched), D-066 (Stage B interpretation) and D-067 (Stage B governance amendment), all APPROVED; D-005, D-006, D-007 status and "Approved by" cells → APPROVED as executed with documented limitations (texts unchanged); four Status history rows.
- `GOVERNANCE.md` §2: Stage B row only (D-067).
- `research/reviews/unresolved_questions.md`: Q-022 → Answered (D-065).
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file; new `logs/session_logs/2026-10-31_T0-GOVERNANCE-DECISIONS.md`.

**Not changed**: Q-020, Q-021, Q-063, Q-064; other decisions; search inventory and register; code, tests, schemas, inventory and generated outputs; criteria and protocol drafts; screening (INACTIVE).

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `b81c4e7`; uncommitted when written; not pushed.

## T1-A — 2026-10-31 — Approved screening-schema and validation changes implemented in code, schemas and tests (no build)

**Context**: researcher task T1-A (2026-10-31) with owner directions 1–12: inventory field `screening_validation_design` for the screening descriptor; extraction field `validation_design` unchanged; `dim_independent_validation` retired from screening input without value mapping (removal from generated outputs and their schemas deferred to T2); manual `scope_flags` tokens limited to `scope_pending_proteomics` and `non_metabolic_rq5_candidate`; `retracted` stays build-derived; no software enforcement of the D-060 (2) missing-abstract rule; descriptor requirement only for title/abstract `include`/`uncertain` rows, Stage-0 rows exempt. Governing decisions: D-028 (2a–2d), D-029 as specified in D-060, D-057, D-058, D-061.

**Modified**
- `scripts/literature/pubrecords.py`: screening columns and enums (`record_type` per D-028 2d; `validation_design` per D-060 (1); `biomarker_class` per D-058); `RETIRED_SCREENING_COLUMNS` (clear error, no conversion); D-060 (6) required-descriptor check for title/abstract `include`/`uncertain` rows with the `rule:stage0` exemption; controlled `scope_flags` validator (`scope_flag_errors`, checked on the value as written); D-028 mapping (`PUBLICATION_TYPE_MAP`, `PUBLICATION_TYPES_IGNORED`, `derive_publication_type`, `unmapped_publication_types`); `publication_type` written to publication records and `unmapped_publication_types` to the build report.
- `scripts/literature/make_literature_reports.py`: inventory columns `biomarker_class` and `screening_validation_design`; `publication_type` taken from the build and removed from the manual fields; `dim_independent_validation` written as null until T2.
- `research/literature/schemas/screening_decision.schema.json`, `paper_inventory.schema.json`, `publication_record.schema.json`: aligned with the code (enums, column order, controlled `scope_flags` pattern, 13-value `publication_type`, `screening_details` keys); `scope_flags` description no longer lists `abstract_only` or `expression_of_concern`; extraction field `validation_design` unchanged.
- `tests/literature/test_screening_and_ids.py`: fixtures completed with SYNTHETIC D-060 (6) descriptors where the test subject is not the descriptors; RQ5 tests that leave method descriptors blank at title/abstract now use `exclude` rows (their assertions are unchanged); `test_optional_descriptor_columns` uses `validation_design`/`screening_validation_design`; manual-value tests use extraction fields instead of `publication_type`; new `test_publication_type_is_derived_not_manual`; publication-schema test allows the retired key until T2.
- `tests/literature/test_t1a_schema_validation.py` (new, 22 tests, synthetic fixtures only).
- `research/reviews/unresolved_questions.md`: Q-074, Q-075, Q-076 added (Open).
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file; new `logs/session_logs/2026-10-31_T1-A.md`.

**Validation**: `python3 -I -m unittest discover -s tests/literature` (run with `-B`, `PYTHONDONTWRITEBYTECODE=1`): 113 tests, OK (baseline before T1-A: 90, OK). Protected files (306: all of `research/` except `schemas/`, incl. ignored raw exports, plus `DECISION_LOG.md`, `GOVERNANCE.md`, `CLAUDE.md`) hashed before and after the code/test work: identical. Committed inventory (3,386 rows) and `publications.jsonl` (3,386) validate against the new schemas (read-only check). `git -c core.whitespace=cr-at-eol diff --check`: exit 0.

**Not changed**: inventory, `records/`, `build_report.json`, generated reports, raw exports and `MANIFEST.csv`, registry, D-044 snapshot, criteria/protocol drafts, decision statuses. No build, screening, pilot, freeze or experiment.

**T2 (requires separate authorisation)**: rebuild under the Step C safeguards; then remove `dim_independent_validation` from `INV_COLS`, the inventory schema and the publication schema `screening_details` (with `RETIRED_SCREENING_COLUMNS` kept for input rejection) and list `publication_type` as required in the publication schema.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `1478089`; uncommitted when written; not pushed.

> **Update (2026-10-31, T1-A-PR-REFERENCE).** The line above was accurate when written. This work, together with T1-A-FOLLOW-UP, was committed as `d1aaceb` ("Implement literature T1-A validation safeguards"), pushed to `claude/eloquent-mccarthy-bqtxr3-part1`, and is included in **PR #17** — https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17 — open, not merged. This note records the PR reference only; it does not indicate approval.

## T1-A-FOLLOW-UP — 2026-10-31 — Q-076(a)–(d) owner directions implemented (no build)

**Context**: researcher prompt 2026-10-31 with owner directions on Q-076: (a) all-ignored source types → `unknown`; (b) arXiv rule on the primary source database; (c) reject non-null hand-edited `publication_type` values that differ from the derived value, include the field in the CSV-versus-JSON check, allow nulls from earlier inventories; (d) exclude retracted records from the full-text candidate list by token membership; recognised types take precedence over unrecognised ones. Q-074 and Q-075 stay open. No DECISION_LOG entry or status change.

**Modified**
- `scripts/literature/make_literature_reports.py`: `DERIVED_GUARDED` (`publication_type`) added to the CSV-versus-JSON comparison in `manual_values`; new check in `manual_values` (runs before any output is written) that stops with nothing written when a non-null `publication_type` differs from `pr.derive_publication_type` on the same row's `source_publication_types`/`source_db`; candidate filter uses `"retracted" in (scope_flags or "").split(";")`.
- `tests/literature/test_screening_and_ids.py`: `test_publication_type_is_derived_not_manual` now expects rejection with outputs unchanged (it previously expected the edit to be overwritten).
- `tests/literature/test_t1a_schema_validation.py`: new classes `TestFollowUpQ076` (3), `TestFollowUpPublicationTypeEdits` (4), `TestFollowUpRetractedCandidates` (2); synthetic fixtures only.
- `research/reviews/unresolved_questions.md`: Q-076 status cell (owner directions; implemented; no decision entry); new Q-077 (guard versus a future mapping-table extension).
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file; `logs/session_logs/2026-10-31_T1-A.md` (follow-up section).

**Validation**: `PYTHONDONTWRITEBYTECODE=1 python3 -I -B -m unittest discover -s tests/literature`: 122 tests, OK (113 before the follow-up). Mutation checks on a scratchpad copy: restoring the old exact-equality filter fails `test_retracted_with_other_flag_excluded_and_theme_record_kept`; disabling the guard fails 3 tests. Protected files unchanged (see session log). `git -c core.whitespace=cr-at-eol diff --check`: exit 0.

**Not changed**: inventory, `records/`, generated reports, raw exports, MANIFEST, registry, D-044 snapshot, criteria/protocol drafts, decision statuses, the 13-value mapping. No build, screening, pilot, freeze or experiment.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `1478089`; uncommitted (together with T1-A); not pushed.

> **Update (2026-10-31, T1-A-PR-REFERENCE).** The line above was accurate when written. This work, together with T1-A, was committed as `d1aaceb` ("Implement literature T1-A validation safeguards"), pushed to `claude/eloquent-mccarthy-bqtxr3-part1`, and is included in **PR #17** — https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17 — open, not merged. This note records the PR reference only; it does not indicate approval.

## Q-074-DECISION — 2026-10-31 — D-068 recorded (missing-abstract rule); Q-074 answered (documentation only)

**Context**: researcher agreement to the Q-074 decision brief and consolidated proposal (incl. G1–G3) and explicit authorisation, 2026-10-31, to record D-068 and apply the agreed documentation-only changes. Commit and push are not authorised by this task.

**Modified**
- `logs/DECISION_LOG.md`: new section with D-068 (APPROVED — CONDITIONAL, inactive for screening; amends D-060 (2) "Stage-0/E1/E4" → "Stage-0/E1" and the application of D-062; clarifies D-059 A-6, D-060 (4) and the D-060 (6) Stage-0 exemption); four Status history rows. The D-059, D-060 and D-062 rows are unchanged.
- `research/reviews/unresolved_questions.md`: Q-074 status cell → Answered (D-068); question text unchanged.
- `research/literature/screening_criteria_v1.1_draft.md` (still DRAFT, not frozen): §4 missing-abstract bullet, §5 tier note, §6 Stage-0 exception, §9 traceability rows (§4, §5), §10 Q-074 row.
- `research/literature/screening_protocol_v0.2_draft.md` (still DRAFT, not frozen): governing-decision list, §1 "Without abstract" row, §3 missing-abstract row and Stage-0 paragraph, §7 missing-abstract review row, §8 expansion review.
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file; new `logs/session_logs/2026-10-31_Q-074-DECISION.md`.

**Not changed**: code, scripts, tests, schemas, configuration, inventory, registry, manifest, generated reports; D-008, D-025, D-029, D-035, D-058, D-059, D-060, D-061, D-062 statuses; Q-075, Q-076, Q-077. No screening activation, freeze, T2, retrieval or data acquisition. The current code does **not** enforce the D-068 (5) Stage-0 restriction (see session log).

**Validation**: diff inspected; `git -c core.whitespace=cr-at-eol diff --check`; no tests run (no executable change).

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `753a1bc`; uncommitted when written; not pushed. The branch is the head of PR #17.

**Follow-up correction (2026-10-31, Option (i), researcher-selected after the independent review)**: D-068 (6), the missing-abstract bullet of `screening_criteria_v1.1_draft.md` and the missing-abstract row of `screening_protocol_v0.2_draft.md` were aligned so that, for records without an abstract: method descriptors and `validation_design` remain `unclear`; `biomarker_class` may take a value only when explicitly supported by the title; all five preliminary component statuses remain `unclear`, justified by "no abstract"; no RQ5-based tier applies; `rq_tags` and `record_type` remain provisional until full-text assessment. This resolves the inconsistency between D-068 (6), which had allowed title-supported values for the method descriptors, and D-068 (7), which sets all five component statuses (three of which are those descriptors) to `unclear`. No other policy changed; both drafts stay unfrozen and screening stays inactive. Checks performed: diff of the three files inspected; text search confirming the title exception now appears only for `biomarker_class`; D-025, D-029, D-035, D-058, D-059, D-060, D-061 and D-062 rows compared with HEAD (unchanged); `git diff --check` exit 0. Uncommitted; not pushed.

## Q-075-DECISION — 2026-10-31 — D-069 recorded (`scope_flags` vocabulary); Q-075 partly addressed (documentation only)

**Context**: researcher approval of Decisions A–D (researcher prompt 2026-10-31); exemplar-tag co-occurrence deferred by the researcher; recording authorised in the researcher prompt of 2026-10-31 using the corrected wording of the final audit. Commit and push are not authorised by this task.

**Modified**
- `logs/DECISION_LOG.md`: new section with D-069 (APPROVED — CONDITIONAL, inactive for screening): `scope_pending_disorder` for the D-056 pending conditions; `non_metabolic_method_exemplar` as a descriptive retention tag (D-059 A-2); `lr_only` descriptive only (Q-042 open); `prognostic` deferred; co-occurrence of `non_metabolic_method_exemplar` and `non_metabolic_rq5_candidate` not decided. Three Status history rows (D-069; D-056 and D-059 A-2 with no status change). The D-056, D-059 and D-061 rows are unchanged.
- `research/reviews/unresolved_questions.md`: Q-075 status cell → "Open — partly addressed" (D-069); question text unchanged.
- `research/literature/screening_criteria_v1.1_draft.md` (still DRAFT, not frozen): header governing-decision list (+D-069); §2.1 tag name; §2.3 heading and `lr_only` note; §3 RQ1 row (`prognostic` deferred, **[OPEN]**); §6 `scope_flags` row (vocabulary, **[OPEN]** markers, governing decisions); §9 rows (§2.1, §6, new §2.3/§3 RQ1 row, "Unchanged" row narrowed to RQ2–RQ4); §10 Q-075 row.
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file; new `logs/session_logs/2026-10-31_Q-075-DECISION.md`.

**Not changed**: screening protocol v0.2, validator, schemas, tests, data and generated outputs; Q-042, Q-076, Q-077. The validator still rejects `scope_pending_disorder`, `non_metabolic_method_exemplar` and `lr_only` until a separately authorised implementation. The pre-existing omission of D-068 from the criteria header is not addressed here.

**Validation**: see the session log (during editing: exact-match edit assertions, per-file line counts, historical decision rows and other questions compared with HEAD, SHA-256 baseline of `research/`, `scripts/` and `tests/`, whitespace checks; full diff reviewed afterwards in the independent audit). No tests run (no executable change).

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `e64ce8f` (1 commit ahead of `origin`, unpushed); uncommitted when written; not pushed. The branch is the head of PR #17; the PR is not changed by this task.

## PR17-DESCRIPTION-UPDATE — 2026-10-31 — PR #17 description updated for commits 28–29 (D-068, D-069); task recorded (documentation only)

**Context**: researcher authorisation, 2026-10-31, to update the description of PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) with the reviewed proposal (default and base branch verified as `claude/happy-hawking-rxptfv`; the only change to the earlier proposal was naming that branch in the first summary sentence); then a separate authorisation, 2026-10-31, to record that completed update in the audit logs. Commit and push of this record are not authorised by this task.

**Done on GitHub (PR description only)**
- PR #17 description replaced with the approved text. It now covers 29 commits (head `81875c3`), adds commit rows 28 (`e64ce8f`, D-068) and 29 (`81875c3`, D-069), the updated size (82 files, +38,364/−3,958), D-068 and D-069 sections, and the updated governance status, checks and reviewer items (Q-042, Q-075 remainder, Q-076, Q-077 and the unfixed discrepancies kept open; screening INACTIVE; criteria v1.1 not frozen; T2 and the D-069 validator change not authorised).
- Read-back: the published body was fetched from the GitHub API and compared programmatically with the approved text: identical except for the final trailing newline, which GitHub does not store (24,302 vs 24,303 characters). GitHub `updated_at` after the update: 2026-10-31T08:55:37Z.
- State after the update: title unchanged; open; not draft; not merged; mergeable state `clean`; head `81875c301fcddd0afc36959b45eb65c4a2af8aed`; base `claude/happy-hawking-rxptfv` at `eb79996`; 29 commits.

**Modified (this record)**
- `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md`, this file; new `logs/session_logs/2026-10-31_PR17-DESCRIPTION-UPDATE.md`.

**Not changed**: PR title, state, base, reviewers, labels, assignees, milestone, comments and reviews; no approval or merge; no branch, commit or push during the description update; `DECISION_LOG.md`, `unresolved_questions.md`, criteria and protocol drafts, code, schemas, tests, data, inventory and generated reports. No PR-2, T2, screening, retrieval, build, experiment or test run. This entry records only the description update of 2026-10-31 (08:55 UTC); it does not reconstruct earlier description updates.

**Validation**: see the session log, sections "Preflight" and "Verification (read-back)" (approved-text diff against the previously published body; programmatic read-back comparison; `git status` clean at `81875c3` after the update). No tests run (no executable change).

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `81875c3` (= `origin`); this record uncommitted when written; not pushed. The branch is the head of PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17), open, not merged.

## PR17-DESCRIPTION-UPDATE-2 — 2026-10-31 — PR #17 description updated for commits 30–31 (documentation only)

**Context**: researcher prompts 2026-10-31: read-only audit and reconciliation proposal for the PR #17 description after `dcaa741` and `e0dd690` were pushed; one researcher-specified wording change; authorisation to publish the reviewed text (`body_v4.md`); then preparation of this audit record for review. Applying, committing and pushing this record each need separate authorisation.

**Previously completed on GitHub (PR description body only)**
- PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) description body updated for commits `dcaa741` and `e0dd690`: commit rows 30 and 31, head, size totals and Checks. Governance sections, decision statuses and open questions unchanged: screening INACTIVE; screening criteria v1.1 and protocol v0.2 remain drafts, not frozen.
- Read-back: the published body was fetched from the public GitHub API and compared programmatically with `body_v4.md`: matched except the final newline, which GitHub does not store.
- At the last verification: title and other PR fields unchanged; open; not merged; head `e0dd690`; base `claude/happy-hawking-rxptfv` at `eb79996`; 31 commits; 83 files; +38,426/−3,958.
- No tests, builds, screening, retrieval or experiments were run for the PR-description update.

**Proposed audit-log changes (drafted for review; not applied to repository files when drafted)**: append-only entries in this file, `logs/PROMPT_LOG.md` and `research/reviews/daily_review_log.md`; new `logs/session_logs/2026-10-31_PR17-DESCRIPTION-UPDATE-2.md`.

**Not changed**: earlier audit entries; `DECISION_LOG.md`, `unresolved_questions.md`, criteria and protocol drafts, code, schemas, tests, data, inventory and generated reports. No approval, merge, PR-2 or T2.

**Branch / commit / PR**: branch at time of review `claude/eloquent-mccarthy-bqtxr3-part1` at `e0dd690` (= `origin`), working tree clean; this record drafted for review, uncommitted and not pushed when written. The branch is the head of PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17), open, not merged. Committing and pushing these audit entries would advance the branch beyond the 31-commit snapshot (HEAD `e0dd690`) currently described in PR #17, making the description's commit count and HEAD reference stale. This task does not update the PR description again.

## PRESERVATION-FIRST — 2026-10-31 — preservation commit of uncommitted decision, draft and safeguard work (no content change)

**Context**: researcher prompts 2026-10-31 ("Option A: Preservation First", then explicit decisions: governance-log entries authorised; the four previously protected files may be committed with their existing content; no fetch and no push). Preserves existing uncommitted work in one local commit before any defect correction. Excludes defect fixes, Workstream C, schema or token changes, new scientific decisions, screening, sampling, freeze, external access, model training and PR changes.

**Preserved without content change (written by earlier tasks on 2026-10-31, uncommitted until this commit)**:
- `logs/DECISION_LOG.md` (insertions only): D-070 to D-073 (H1-H8-DECISIONS); D-074 (Q-080-PROPOSAL, then approval); D-075 (Q-078-DECISION); D-076 (Q-079-DECISION); D-077 (PILOT-SAMPLING-DECISION); status-history rows, including the D-063 F1-PILOT-FRAME row.
- `research/reviews/unresolved_questions.md`: Q-075 answered; Q-078, Q-079 and Q-080 added and answered.
- `research/literature/screening_criteria_v1.1_draft.md` and `research/literature/screening_protocol_v0.2_draft.md`: revisions for D-070 to D-077. Both remain drafts, **not frozen**.
- Crossref second-source verification lookups (Workstream A, researcher prompt 2026-10-31):
  - modified: `scripts/literature/pubrecords.py`, `scripts/literature/make_literature_reports.py`, `research/literature/schemas/source_record.schema.json`;
  - new: `scripts/literature/fetch_crossref.py`, `tests/literature/test_crossref_verification.py`.
  - The fetcher has never contacted Crossref.
- NHANES leakage and eligibility safeguards (Workstream B, same prompt):
  - new: `scripts/nhanes/safeguards.py`, `tests/nhanes/test_safeguards.py`;
  - `scripts/run_checks.sh` now runs the NHANES tests.
  - Synthetic fixtures only; no data file read.
- The PR17-DESCRIPTION-UPDATE-2 entries in this file, `logs/PROMPT_LOG.md` and `research/reviews/daily_review_log.md`, and `logs/session_logs/2026-10-31_PR17-DESCRIPTION-UPDATE-2.md`. Byte-identical to the reviewed versions; their wording describes the state when they were drafted.

**Added by this task**: this entry; the PRESERVATION-FIRST entries in `logs/PROMPT_LOG.md` and `research/reviews/daily_review_log.md`; `logs/session_logs/2026-10-31_PRESERVATION-FIRST.md`.

**Validation**:
- Inspection: hash comparison of all 144 tracked files with the snapshot taken before Workstreams A and B showed that only the four Workstream A/B files had changed.
- The decision files, both drafts and the four log files match the hashes recorded earlier in the session.
- `logs/DECISION_LOG.md` diff: 71 insertions, 0 deletions.
- Checks: see the session log, section "Checks".

**Known unresolved (not fixed; out of scope)**, from the independent read-only audit of 2026-10-31:
- **Crossref:** saving the raw file and registering it in the manifest are not atomic; the parser accepts wrongly shaped `title`/`container-title` values; `VERIFY-CR-` query IDs are not restricted to the `crossref_works` route; title markup inside words can produce false title conflicts.
- **NHANES:** `eligibility_cascade` E3 treats a missing value or a text value as "in the file"; predictor checks go by column name only; fold checks go by row index only.
- **Integration:** the NHANES safeguards are not integrated into any pipeline.
- **Drafts:** protocol v0.2 line 10 does not list D-077, and line 83 does not name the inventory SHA-256 and the sampling script. Left unchanged by this task.

**Open decisions**: Crossref year field; pilot list and venue-mapping policy; the reading of D-068 (5) for the validator; authorisation of defect fixes, Workstream C and T2; the criteria v1.1 / protocol v0.2 freeze (D-035 record §6 conditions 5 and 6 unmet); Q-044, Q-046, Q-047, Q-050, Q-055, Q-060, Q-061 (open); D-013 to D-020 (pending).

**Not done**: no content of any preserved file changed; no decision status changed; no screening, sampling, freeze, external API call, data download, T2, model training or PR change; no fetch, no push.

**Logging gap (recorded, not backfilled)**: no CHANGELOG, PROMPT_LOG or daily-review entries exist for:
- the individual 2026-10-31 decision tasks (H1-H8-DECISIONS, Q-080-PROPOSAL, D-074 approval, Q-078-DECISION, Q-079-DECISION, F1-PILOT-FRAME, PILOT-SAMPLING-DECISION; the task IDs are as cited in `logs/DECISION_LOG.md`);
- the Workstream A/B implementation;
- the read-only analyses and the independent audit of 2026-10-31.

No session logs exist for them either. This entry records that the work exists and is preserved; it does not replace those records.

**Branch / commit / PR**:
- Branch `claude/eloquent-mccarthy-bqtxr3-part1`, parent commit `e0dd690`. This entry is part of the local preservation commit; its hash is reported to the researcher, because an entry cannot contain its own commit hash.
- Not pushed: no push authorisation. Not fetched: the local tracking ref (`e0dd690`) may not reflect the remote.
- This session's standing instructions name a different development branch (`claude/gracious-hopper-rx64za`). The researcher directed that the current branch be used; the discrepancy is left for a separate decision.
- The branch is the head of PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17), open, not merged, not changed by this task.

## DEFECT-CORRECTION-AB — 2026-10-31 / 2026-11-01 — corrections to the Crossref and NHANES safeguards (Workstreams A and B); synthetic tests only; uncommitted

**Context**:
- Researcher prompt 2026-10-31: correct the confirmed implementation defects found by the independent read-only audit of Workstreams A and B (2026-10-31), with targeted regression tests and documented limitations.
- Researcher prompt 2026-11-01: review the corrections, rerun the checks, and record this task with append-only logging (authorised for this task only).
- Not authorised: commit, push, fetch, merge, branch change, scientific decisions, screening freeze, external API calls and real-data experiments.
- The task label `DEFECT-CORRECTION-AB` was chosen by the assistant; no label was given in the prompts.

**Modified**:
- `scripts/literature/pubrecords.py`:
  - Crossref-only inline-markup removal (`strip_inline_markup`; e.g. `HbA<sub>1c</sub>` → `HbA1c`); ordinary parsing (`strip_markup`) unchanged;
  - shape validation of Crossref `title`, `container-title`, `author` and `DOI`, plus the (inactive) year fields;
  - `VERIFY-CR-` query IDs restricted to route `crossref_works`, in `register_raw` and again in `build_source_records`;
  - `register_raw` refuses a manifest whose last line is incomplete and appends each row in one write followed by `fsync`;
  - a non-object Crossref file stops the build instead of crashing;
  - the no-year behaviour is documented in `auto_verification` (unchanged).
- `scripts/literature/fetch_crossref.py`:
  - `.partial` write with `fsync` and SHA-256 read-back, then a hard link to the final name (never overwriting);
  - run refused before any request on a damaged manifest, a malformed run date or an existing lock file;
  - already-registered papers skipped, so a run can be resumed with the same date; new files take the next free number;
  - `http.client.HTTPException` retried as a transport error;
  - per-record handling of unexpected exceptions; a persistence failure stops the run with the report still returned;
  - unregistered `CR_*` files reported as orphans and never deleted;
  - exit status 1 for any outcome other than saved, already registered or dry run.
- `scripts/nhanes/safeguards.py`:
  - E3 flags must be real booleans (missing, text, numeric and NA values raise instead of being coerced to True);
  - `SEQN` must be unique and non-missing when present;
  - name aliases for the section 7 categories, matched as whole tokens; OGTT names `LBXGLT`/`LBDGLTSI` added;
  - derived-index names matched as whole tokens; the comment-code rule limited to NHANES-style names;
  - optional allow-list in `check_predictors`;
  - participant-aware fold checks with optional full coverage;
  - `check_partitions` (train/calibration/validation separation and coverage) and `check_unique_participants`; missing IDs rejected in `check_disjoint_participants`;
  - optional subcategory and per-step exclusion counts in `eligibility_cascade`.
- `tests/literature/test_crossref_verification.py`: two tests updated for intended behaviour changes (route refused at registration; existing files are never overwritten and the next number is used); helper `append_manifest_row`.

**Created**:
- `tests/literature/test_crossref_robustness.py` (25 tests, including failure injection on the save-and-register path);
- `tests/nhanes/test_safeguards_corrections.py` (17 tests);
- `logs/session_logs/2026-11-01_DEFECT-CORRECTION-AB.md`.

**Validation (actual outcomes)**:
- **2026-11-01 07:26:02–07:27:10 UTC** (`python3 -I -B`; all exit 0):
  - `tests/literature`: 177 tests, OK;
  - `DATA_PROTECTION_STRICT=1 … tests/data_protection -v`: 10, OK;
  - `tests/nhanes -v`: 27, OK;
  - `validate_search_queries.py`: PASS, 168 rows;
  - `sh -n scripts/run_checks.sh`: OK;
  - `git diff --check`: OK.
  - Literature tests emitted 470 warning lines (unclosed files and implicitly cleaned temporary directories, all in pre-existing code and tests; none from the new test files). The same counts were seen on 2026-10-31 at 18:01–18:02 UTC.
- **Mutation check (2026-10-31; scratch copies, then deleted):**
  - 26 deliberately reintroduced defects; 24 caught in the first run;
  - two tests were then tightened; 26 of 26 caught in the second run.
  - Only the second run's results are kept in the session scratchpad.
- **Regression (2026-10-31; scratch copies of `research/literature` outside the repository):**
  - build and reports with the code at `93dd16d` and with the corrected code;
  - 284 of 284 files identical, `build_report.json` differing only in `built_at`.
  - Separately, the generated files committed to the repository differ from both runs: `publication_type` in all 3,386 inventory records, `collection_stats`, `verification_report`. This is because they predate the T2 rebuild, which is not authorised; it is not caused by this task.
- `fetch_crossref.manifest_problems` and `orphans`, run read-only on the real `research/literature`, returned no problems; the `MANIFEST.csv` hash was unchanged.

**Scope of the evidence**:
- All new tests use synthetic fixtures and a fake transport, with `urlopen` patched to fail.
- No Crossref request was made and no NHANES file was read.
- The corrections are **not** validated against real Crossref responses or real NHANES data.
- Crash recovery is tested by injected failures. Atomicity is **not** guaranteed: it depends on POSIX hard links and `fsync`; a crash can leave an orphan file, a stale lock or an incomplete manifest line, all detected and repaired by hand.

**Known limitations and open items (review of 2026-11-01)**:
- **Crossref:**
  - `main()` exit status 1 for failed or malformed outcomes is not tested through `main()`;
  - no run report is produced if planning itself raises (for example an unreadable inventory) or on a keyboard interrupt;
  - the report goes to standard output only;
  - malformed response bodies are reported but not retained;
  - the manifest and directory `fsync` calls are not directly tested;
  - the tag list and the real Crossref response layout are unverified.
- **NHANES:**
  - the alias list is an assistant proposal, not approved and not complete by nature;
  - `LBXGLT`/`LBDGLTSI` were named from memory and not checked against a codebook;
  - the allow-list depends on Q-050;
  - a declared feature derived only from `LBXIN` is still flagged (S-06 undecided);
  - fold coverage checking is opt-in and stratification is not checked;
  - the `SEQN` check runs only when the column is present;
  - equivalence with `descriptive_counts.py` on the real files is unverified;
  - the safeguards are not integrated into any pipeline.
- **Observation for the researcher (not changed):** protocol draft §7 states that every listed derived index contains glucose, HbA1c or insulin; as recalled, SPISE uses HDL, triglycerides and BMI only. This is unverified.

**Not changed**: research decisions and their statuses; `DECISION_LOG.md`; `unresolved_questions.md`; screening drafts; the inventory and generated outputs in the repository; the preservation commit; the PRESERVATION-FIRST and PR17-DESCRIPTION-UPDATE-2 session logs.

**Branch / commit / PR**:
- `claude/eloquent-mccarthy-bqtxr3-part1` at `93dd16d` (preservation commit, unchanged). All changes of this task are uncommitted and unstaged; not pushed; not fetched.
- The local tracking ref (`e0dd690`) may not reflect the remote.
- PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed; open, not merged.

## SOFTWARE-GAP-CLOSURE — 2026-11-01 — failure-path tests and two report fixes for the Crossref fetcher; synthetic cascade-equivalence test; uncommitted

**Context**:
- Researcher prompt 2026-11-01 ("November 1 Software Gap Closure"): close, where safe, the software-testing gaps listed in the DEFECT-CORRECTION-AB review, using offline synthetic tests only.
- Not authorised: staging, commit, push, fetch, branch or PR changes, network, real NHANES records, screening sample or freeze, model training, and decision or question-status changes.
- The task label is taken from the prompt title.

**Modified**:
- `scripts/literature/fetch_crossref.py`:
  - a failed directory `fsync` (best effort) is now reported in `report["warnings"]` instead of being ignored silently; the key is omitted when empty, so ordinary reports are unchanged;
  - a `persistence_error` entry now records the state on disk (`file_saved`, `manifest_row_present`). A manifest `fsync` failure after the row is written leaves the row in place, and the report now says so.
- `scripts/literature/pubrecords.py`: comment only. It records that the inline-markup tag list is an implementation assumption: no project document describes Crossref markup, no real Crossref response has been inspected, and the only project evidence is that PubMed connector titles carried no markup. Tag list and behaviour unchanged.

**Created**:
- `tests/literature/test_crossref_failure_paths.py` (20 tests): manifest and directory `fsync` failures; command-line exit status for failed, exhausted-retry and malformed responses and for refused, saved and dry runs; one report for mixed per-record outcomes; planning failures and keyboard interrupts (actual behaviour: they raise and no report is produced; lock released; state resumable); recovery from a truncated `.partial`, an orphan file, an incomplete manifest line and a stale lock.
- `tests/nhanes/test_cascade_equivalence.py` (2 tests): `descriptive_counts.period_counts` (with `read` replaced by synthetic tables and `pandas.read_sas` patched to fail) and `safeguards.eligibility_cascade` give identical cascade counts on a synthetic fixture covering every E0–E8 rule and subcategory.
- `logs/session_logs/2026-11-01_SOFTWARE-GAP-CLOSURE.md`.

**Validation (2026-11-01, 07:35:52–07:37:07 UTC; `python3 -I -B`; all exit 0)**:
- `tests/literature`: 197 tests, OK;
- `DATA_PROTECTION_STRICT=1 … tests/data_protection -v`: 10, OK;
- `tests/nhanes -v`: 27 + 2 = 29, OK;
- `validate_search_queries.py`: PASS, 168 rows;
- `sh -n scripts/run_checks.sh`: OK;
- `git diff --check`: OK.
- **Warnings:** 470 warning lines in the literature run, the same count as before. They come from 5 `open()` calls without a context manager in `make_literature_reports.py` (lines 76, 78, 167, 239, 291, present since `eb79996`) and from temporary directories in `test_screening_and_ids.py`, `test_t1a_schema_validation.py` and `test_pubrecords.py`. Per module: 264, 138, 58 and 10 (the last via the existing report test in `test_crossref_verification.py`); 0 from `test_crossref_robustness.py` and `test_crossref_failure_paths.py`. Not suppressed and not fixed (out of scope).
- **Mutation check (scratch copies):** 10 of 11 reintroduced defects caught. The survivor (E6 written as `!= 1` instead of `~(== 1)`) is equivalent in pandas for missing values, so it is not a test gap.

**Evidence status**:
- Tested on synthetic data: every behaviour listed under Created.
- Inferred from code inspection only: behaviour after a real power loss or kernel crash; POSIX hard-link and `fsync` semantics on the target filesystem.
- Untested: a failure inside the orphan or report bookkeeping in `finally`; concurrent runs beyond the lock check.
- Outstanding: real Crossref response validation; real NHANES equivalence of the cascade (no local data or codebook in the repository).
- `LBXGLT`/`LBDGLTSI` remain unverified: the project contains no codebook or other authoritative evidence for these names.

**Not changed**: decisions, decision statuses and questions (`DECISION_LOG.md`, `unresolved_questions.md`); protocol draft and screening drafts; the NHANES alias list, Q-050, S-06 and insulin handling; `safeguards.py`; PubMed parsing; earlier log entries and session logs.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `93dd16d` (preservation commit, unchanged); all changes uncommitted and unstaged; not pushed; not fetched. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## FAILURE-REPORT-RELIABILITY — 2026-11-01 — incomplete-run reports for planning failures and KeyboardInterrupt in the Crossref fetcher; uncommitted

**Context**:
- Researcher prompt 2026-11-01 ("Failure Report Reliability Review"): investigate the two missing-report paths (planning failure; KeyboardInterrupt) and, if safe, implement the smallest fix.
- Not authorised: staging, commit, push, fetch, branch or PR changes; network; real data; screening; training; decision or protocol changes.
- The task label is taken from the prompt title.

**Root causes**:
1. **Planning failure:** `run()` reads the inventory and the manifest and plans before its `report` dict exists, and `main()` printed only a returned report, so an exception there left nothing to print.
2. **KeyboardInterrupt:** it is not an `Exception`, so it bypassed every per-record handler. `finally` released the lock and listed orphans in the local `report`, but the dict was lost when the exception left `run()`.

**Related weaknesses found**:
- An exception inside `finally` (orphan listing) could replace the propagating exception.
- A failure between creating the lock file and entering `try` (lock write, transport construction) left a stale lock.

**Modified** `scripts/literature/fetch_crossref.py`:
- `run(..., progress=None)` records the stage reached and the partial report.
- Every returned report has `status` set to `refused`, `aborted` or `finished` ("finished" means every planned paper was processed, not that every lookup succeeded).
- Lock creation moved inside `try`, with a `locked` flag, so `finally` removes only a lock this run created; a lock that appears from another run is never removed.
- The orphan listing in `finally` is guarded and reported as a warning.
- `main()` catches `BaseException`, prints a failure report (`status: incomplete`, `completed: false`, `failure_stage`, exception name and message, partial report) and re-raises the original exception unchanged.
- `emit_failure_report()` contains any error raised while writing the report (one line on standard error if possible), so it can never replace the original exception.
- Module docstring updated.
- No file is written for the failure report (standard output only). Persistence, manifest and resume behaviour are unchanged.

**Created**:
- `tests/literature/test_crossref_failure_report.py` (15 tests): missing pilot file, missing inventory and unreadable manifest; KeyboardInterrupt between papers and during a save (partial results, orphans, released lock, resume); a failure report that never claims completion; failure-report construction errors and broken standard output and error; identity and traceback of the re-raised exception; an orphan-listing failure in `finally`; lock write failure; another run's lock never removed; status of completed, refused and aborted runs; two child-process tests (report on standard output, original traceback on standard error, non-zero exit status).
- `logs/session_logs/2026-11-01_FAILURE-REPORT-RELIABILITY.md`.

**Validation (2026-11-01, 07:52:16–07:53:34 UTC; `python3 -I -B`; all exit 0)**:
- `tests/literature`: 212 tests, OK;
- `DATA_PROTECTION_STRICT=1 … tests/data_protection -v`: 10, OK;
- `tests/nhanes -v`: 29, OK;
- `validate_search_queries.py`: PASS, 168 rows;
- `sh -n scripts/run_checks.sh`: OK;
- `git diff --check`: OK.
- **Warnings:** 470 warning lines in the literature run, the same count and sources as before (`make_literature_reports.py` unclosed files and temporary directories in older tests); 0 from the new test file.
- **Mutation check (scratch copies):** 9 of 9 reintroduced defects caught.

**Remaining limitations**:
- No report on SIGTERM, SIGKILL or power loss.
- A second Ctrl-C while the first is being handled can stop the report or the lock release.
- A KeyboardInterrupt in the instant between the exclusive lock creation and setting `locked` can leave a stale lock (manual removal).
- An interrupt while the normal report is printing is not handled.
- The failure report goes to standard output only and is not saved.
- Crash recovery is tested by injected failures only; atomicity is not guaranteed.

**Not changed**: `DECISION_LOG.md`, `unresolved_questions.md`, protocol and screening drafts, publication metadata or provenance logic, earlier log entries and session logs.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `93dd16d` (unchanged); uncommitted and unstaged; not pushed; not fetched. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## READINESS-STABILIZATION — 2026-11-01 — verified state, software review, research-readiness assessment and plan to 2026-11-24 (audit and planning only)

**Context**: researcher prompt titled "BioML-Insight — November 2 Consolidated Research Readiness and Stabilization"; the container clock read 2026-11-01. Audit and planning only; no staging, commit, push, fetch, network, real data, screening, freeze, training or decision change.

**Created**: `logs/session_logs/2026-11-01_READINESS-STABILIZATION.md`, which holds the full assessment and the task plan. **Modified**: this file, `logs/PROMPT_LOG.md` and `research/reviews/daily_review_log.md` (append-only). No source code, test, decision, question status, protocol or screening file was changed.

**Validation (07:58:49–08:00:08 UTC; `python3 -I -B`; all exit 0)**:
- literature 212 tests, OK; data protection (strict) 10, OK; NHANES 29, OK;
- query table PASS (168 rows); `sh -n scripts/run_checks.sh` OK; `git diff --check` OK;
- 470 warning lines from existing code and tests, recorded as technical debt TD-1;
- the 15 uncommitted changes were unchanged (SHA-256 checked at start and end).

**Key findings**:
- **Inventory** [EVIDENCE]: 3,386 records (3,348 partially verified, 37 unverified, 1 needs review, 0 verified); all not screened and not extracted.
- **Gates:** D-035 §6 conditions 5 and 6 unmet; Stage C and Stage D gates not passed; D-013–D-020 pending; AB-2 to AB-13 unmet.
- **Data:** no NHANES files in the container.
- **Schedule:** [INFERENCE] real-data training before 2026-11-24 is unlikely. [RECOMMENDATION] use the D-045 fallback deliverable.
- **Governance:** D-064's status cell does not record the later implementation authorisations (question for the researcher).

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `93dd16d` (unchanged); uncommitted; not pushed; not fetched. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## DECISION-PREPARATION — 2026-11-01 — change-safety assessment, decision package, screening and Crossref readiness, conditional schedule (planning only)

**Context**: researcher prompt titled "BioML-Insight — November 2 Execution and Decision Preparation"; container clock 2026-11-01. No staging, commit, push, fetch, network, real data, screening, freeze, training or decision change.

**Created**: `logs/session_logs/2026-11-01_DECISION-PREPARATION.md`. **Modified**: this file, `logs/PROMPT_LOG.md` and `research/reviews/daily_review_log.md` (append-only). No code, test, decision, question status, protocol or screening file was changed.

**Findings**:
- State verified: 7 modified and 9 untracked files; the 12 non-log files unchanged since READINESS-STABILIZATION. No material defect found.
- The changes must be committed together (test imports; logs refer to the untracked session logs).
- The six in-scope records without an abstract (P0522, P0559, P0624, P0938, P1154, P3061) all carry PubMed's "[Abstract not available]" placeholder in the local raw metadata; their classification under D-068 (8) is left to the researcher.
- D-035 §6 conditions 5 and 6 remain unmet.

**Validation**: `git diff --check` exit 0. Test suites not re-run (no code or test changed since 07:58–08:00 UTC: 212/10/29 OK; query table PASS).

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `93dd16d` (unchanged); uncommitted; not pushed; not fetched. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## WORKSTREAM-C — 2026-11-01 — preservation commit `ad02333`; validator update (D-068 (5) Option A; D-069/D-070 vocabulary; repeated tokens rejected, D-078); D-077 wording in protocol v0.2; six-record evidence; T2 checklist

**Context**: researcher prompt 2026-11-01 approving the items below. Not approved: fetch, push, branch or PR changes, executing T2, pilot draw, freeze, screening, training, unrelated decisions.

**Commit**:
- `ad02333b1ae8df8e58f4f11588d20960ef8fc2ba` (parent `93dd16d`): the 17-file set verified in DECISION-PREPARATION, staged by explicit path.
- Pre-commit checks: literature 212, data protection 10, NHANES 29, all OK; query table PASS (168 rows); `sh -n` OK; `git diff --check` OK.
- Not pushed.

**Modified (uncommitted)**:
- `scripts/literature/pubrecords.py`:
  - D-069 (E) vocabulary;
  - repeated tokens rejected (D-078);
  - `is_stage0_rule_row()`: the D-060 (6) exemption is limited to `exclude` E5/E7 `rule:stage0` rows (D-068 (5), Option A; Option B not adopted).
- `research/literature/schemas/screening_decision.schema.json` and `paper_inventory.schema.json`: `scope_flags` patterns and descriptions.
- `tests/literature/test_t1a_schema_validation.py`: token, pattern, Stage-0, co-occurrence and inventory tests.
- `tests/literature/test_screening_and_ids.py`: `needs_d060` helper.
- `research/literature/screening_protocol_v0.2_draft.md`: two D-077 wording fixes only; still DRAFT, not frozen.
- `logs/DECISION_LOG.md`: D-078 (new) and three status-history rows; insertions only.

**Created**: `logs/session_logs/2026-11-01_WORKSTREAM-C.md`.

**Validation** (`python3 -I -B`, 09:00:58–09:02:32 UTC; all exit 0):
- **Tests:** literature 217, OK; data protection (strict) 10, OK; NHANES 29, OK.
- **Other checks:** query table PASS (168 rows); `sh -n scripts/run_checks.sh` OK; `git diff --check` OK.
- **Warnings:** 484 lines (470 before). The 14 extra lines come from existing code run by the new tests (`make_literature_reports.py` unclosed files and fixture temporary directories, TD-1); two unclosed files in the new test code were fixed.
- **Mutation check (scratch copies):** 10/10 caught.
- **Regression (scratch copies of `research/literature` outside the repository; not T2):** HEAD vs new code, 284/284 files identical (`build_report.json` differs only in `built_at`).

**Not done**: T2 not executed. D-035 §6 conditions 5 and 6 not recorded as met. Six records not classified (evidence in the session log). No push, fetch or PR change.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1`, HEAD `ad02333` (local, 1 ahead of `93dd16d`, 2 ahead of the last known remote `e0dd690`); this task's other changes are uncommitted. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## T2-REBUILD — 2026-11-01 — inventory rebuild: `publication_type` populated, two new columns, `dim_independent_validation` removed; integrity verified; CRLF convention accepted

**Context**: researcher prompts 2026-11-01:
- fetch and fast-forward push of `93dd16d`, `ad02333`, `2fcc7b9` (`e0dd690..2fcc7b9`, no force);
- T2 execution under stop conditions;
- acceptance of the CRLF line endings of `paper_inventory.csv`, T2 logs and one local commit.

Not authorised: push of the T2 commit, PR #17 changes, decision changes, six-record classification, freeze, D-035 §6 record, pilot, screening, training.

**Modified**:
- code and tests: `scripts/literature/make_literature_reports.py`; `research/literature/schemas/paper_inventory.schema.json`; `research/literature/schemas/publication_record.schema.json` (also `publication_type` required); `tests/literature/test_t1a_schema_validation.py`; `tests/literature/test_screening_and_ids.py`;
- regenerated: `research/literature/paper_inventory.json`, `paper_inventory.csv`, `records/build_report.json`, `records/collection_stats.json`, `verification_report.md` (and the git-ignored `records/publications.jsonl`).

**Created**: `logs/session_logs/2026-11-01_T2-REBUILD.md`.

**Preflight**: manifest verified (244 rows, 0 problems); 14 outputs hashed and backed up to the scratchpad, including the two git-ignored `.jsonl` files; backups verified.

**Result (actual)**:
- `publication_type` for 3,386 records: journal_article 2,698; review 483; preprint 135; unknown 38; editorial_comment_letter 22; study_protocol 3; erratum_or_correction 2; dataset 2; conference_paper 2; guideline_or_consensus 1.
- `unmapped_publication_types` `{}`; `biomarker_class` and `screening_validation_design` null for all.

**Integrity**:
- same 3,386 paper IDs in the same order;
- registry byte-identical, no new row;
- provenance and metadata identical;
- verification statuses unchanged (3,348 / 37 / 1 / 0; 0 changes);
- the 3 registry conflicts are pre-existing;
- pilot frame 1,463 with identical membership;
- dedup review, publications index, search register, full-text candidate list, `source_records.jsonl` and manifest byte-identical.

**Inventory SHA-256**: JSON `b668dbde42473baa49ac1f02f89f900e94e39159c82efb8175ba125fef06d054`; CSV `00062fed6d7aad189af86e4e489488db45d347f5426acf0f393695f406a194ef`.

**Whitespace**:
- ordinary `git diff --check` exits 2: 3,387 findings, all CRLF carriage returns in `paper_inventory.csv`;
- no genuine trailing spaces or tabs; uniform CRLF in the working and committed CSV;
- `git -c core.whitespace=cr-at-eol diff --check` exits 0, the accepted repository-specific check for this generated CSV (researcher, 2026-11-01);
- no git configuration changed; line endings not converted.

**Validation**: test and check results before commit are in the session log (§6).

**Not done**: six records without an abstract not classified; D-035 §6 conditions 5 and 6 not recorded as met; criteria v1.1 and protocol v0.2 still drafts; no pilot, screening, extraction or training.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1`; remote at `2fcc7b9` after the authorised push. This entry is part of one local T2 commit (parent `2fcc7b9`; hash reported to the researcher); not pushed. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## FREEZE-READINESS-REVIEW — 2026-11-01 — freeze-readiness review package for criteria v1.1 and protocol v0.2 (proposals only)

**Context**: researcher prompt 2026-11-01. Decision support only. No draft edits, freeze, classification, Option A/B choice, D-035 §6 record, pilot, screening, training, network access, commit or push.

**Created**:
- `research/reviews/freeze_readiness_review_v1.1_v0.2.md` (sections A–I: summary; outdated passages with proposed replacements; Stage-0 Option A vs B; Stage-0 type list; six records without an abstract; D-035 §6 evidence table; freeze checklist; downstream prerequisites; decision register);
- `logs/session_logs/2026-11-01_FREEZE-READINESS-REVIEW.md`.

**Key findings**:
- `[EVIDENCE]` protocol v0.2 §10 line 102 still lists the validator work and T2 as pending ("T2, not authorised"), and criteria v1.1 line 138 describes the column removal as future work. Both are done (`2fcc7b9`, `bf0c579`).
- `[EVIDENCE]` criteria v1.1 lists neither D-077 nor D-078 among its governing decisions (line 10) and does not state the D-078 repeat rule (line 135).
- `[OPEN]` protocol v0.2 line 55 states a usage restriction (Option B) while the validator implements Option A.
- `[EVIDENCE]` the Stage-0 type list is identical in all sources (no discrepancy); its explicit confirmation at the freeze is still required (D-068 (5)).
- The six records remain unclassified (R1/R2 open).
- No `criteria_version` identifier is defined yet.

**Validation**: all references checked against the repository; new files without trailing whitespace; the drafts, DECISION_LOG, unresolved questions and inventory are byte-identical before and after. Tests: the strict data-protection suite was run at the end of the task and reported OK (10-test suite); the literature and NHANES suites and the query-table check were not run (no code change). *(Corrected before commit on 2026-11-01: previously "No tests run".)*

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `bf0c579` (= `origin`); uncommitted; not pushed. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## FREEZE-DRAFT-CORRECTIONS — 2026-11-01 — draft corrections from the freeze-readiness review; D-079 (R1, six records); Option A retained; Stage-0 list re-verified (not a freeze)

**Context**: researcher prompt 2026-11-01:
- retain Option A;
- adopt R1 for all six records if compatible with D-068 (8);
- confirm the Stage-0 list only after comparison, documenting unresolved approval evidence;
- correct outdated passages; propose a `criteria_version`.

Not a freeze. No D-035 §6 record, pilot, screening, training, network, commit or push.

**Modified**:
- `research/literature/screening_criteria_v1.1_draft.md` and `research/literature/screening_protocol_v0.2_draft.md`: Option A exemption-scope wording; completed T2 and validator work no longer described as pending; D-077, D-078 and D-079 references; D-078 repeat rule; six records classified *unavailable — PubMed* (D-079); proposed `criteria_version` `criteria_v1.1+protocol_v0.2` (not in force); §10 refreshed without recording any condition as met; traceability rows.
- `logs/DECISION_LOG.md` (insertions only): D-079 and status-history rows for D-079 and D-068.

**Created**: `logs/session_logs/2026-11-01_FREEZE-DRAFT-CORRECTIONS.md`.

**Key points**:
- `[EVIDENCE]` R1 is compatible with D-068 (8) when limited to PubMed. It is not a finding that no abstract exists in any source.
- `[EVIDENCE]` the Stage-0 list is identical in protocol v0.1 §3, D-068 (5) and the drafts. D-025 approved v0.1's "Stage-0 handling" but does not enumerate the list. `[OPEN]` the explicit confirmation "at the v1.1 freeze" remains for the freeze record.
- No validator code changed: Option A matches D-068 (5).

**Validation** (10:26–10:27 UTC; all exit 0):
- literature 217, data protection (strict) 10, NHANES 29, all OK;
- query table PASS (168 rows); `sh -n` OK;
- `git diff --check` and the CRLF-aware check OK;
- every cited D-number exists; inventory and `unresolved_questions.md` unchanged; 484 pre-existing warning lines (TD-1).

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `bf0c579` (= remote-tracking ref); uncommitted, together with the FREEZE-READINESS-REVIEW changes; not pushed. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## FREEZE-DOCUMENTATION-CORRECTIONS — 2026-11-01 — four wording corrections from the final read-only review of the uncommitted freeze change set

**Context**: researcher prompts 2026-11-01 after the read-only final review (no critical or major issues; minor documentation corrections recommended). Wording only; no scientific decision, rule, status or classification changed. Not a freeze.

**Modified**:
- `logs/session_logs/2026-11-01_FREEZE-READINESS-REVIEW.md` and the FREEZE-READINESS-REVIEW entry above: test-run record corrected. The strict data-protection suite was run at the end of that review and reported OK (10-test suite); the literature and NHANES suites and the query-table check were not run. Both lines carry a dated "corrected before commit" note.
- `research/literature/screening_criteria_v1.1_draft.md` (header; §9 header row) and `research/literature/screening_protocol_v0.2_draft.md` (header): `criteria_v1.1+protocol_v0.2` now attributed as "proposed by the assistant at the researcher's request (2026-11-01)"; it remains a proposed identifier only, not frozen or effective.
- `logs/DECISION_LOG.md`: D-079 (4) "is listed" → "will be listed in the pilot report" (no pilot report exists). Status unchanged: APPROVED — CONDITIONAL (inactive for screening).
- `research/reviews/freeze_readiness_review_v1.1_v0.2.md`: one dated "Later note" header row; the original point-in-time analysis is unchanged.

**Created**: `logs/session_logs/2026-11-01_FREEZE-DOCUMENTATION-CORRECTIONS.md`.

**Validation**: edits compared with pre-edit copies; no unrelated file changed; no whitespace issue (`git diff --check` and the CRLF-aware check exit 0); no generated output, code, test, schema or inventory change. No tests or scripts run (wording-only change).

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `bf0c579`; uncommitted, together with the FREEZE-READINESS-REVIEW and FREEZE-DRAFT-CORRECTIONS changes; not pushed. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## PRE-FREEZE-CORRECTIONS — 2026-11-01 — pre-freeze documentation corrections to the drafts; three-inventory consistency check recorded (not a freeze)

**Context**: researcher prompts 2026-11-01:
- a read-only pre-freeze review of criteria v1.1 and protocol v0.2;
- documentation-only corrections to the two drafts;
- a read-only decision and evidence audit;
- authorisation to record the corrections and the inventory check and to make one local commit.

Not a content approval or a freeze. No D-035 §6 record, pilot draw, implementation, screening, network access or push.

**Modified (drafts; wording only, no E-code, inclusion rule, Stage-0 list, Option A wording or D-079 text changed)**:
- `research/literature/screening_criteria_v1.1_draft.md`:
  - header: the identifier takes effect only through an explicit, approved freeze decision;
  - §0: inventory basis distinguished (D-044 historical inventory, later inventories, inventory hashed at the draw);
  - new §11: proposed freeze procedure, **not executed**, with file names and status wording marked [OPEN].
- `research/literature/screening_protocol_v0.2_draft.md`:
  - header pointer to criteria §11;
  - §1: all three inventory hashes and commits;
  - §3: Stage-0 timing from approved decisions, with the timing and the generating tool marked [OPEN];
  - §7 "When": the separate draw authorisation of D-077 (6) added, no existing prerequisite removed;
  - §10: rows 1–4 reworded to "Assessed as met at decision level; not formally recorded", plus a status-terms note. **No condition 1–6 is formally recorded as met; conditions 5 and 6 remain Unmet.** How conditions 1–4 are recorded is [OPEN].

**Inventory consistency check `[EVIDENCE]`** (read-only, 2026-11-01; reproduced again at 14:11 UTC before this entry):
- **Method:** each inventory was read from Git objects (`git show <commit>:<path>`), never from the working tree. Two independent parsers: Python `json` on `paper_inventory.json` and Python `csv` on `paper_inventory.csv`.
- **Filter (D-044):** a record is in scope if any `;`-separated token of `query_ids` (whitespace-stripped, exact match) is one of `Q-PM-G1` … `Q-PM-G7`, `Q-PM-01`, `Q-PM-02`, `Q-PM-03`, `Q-PM-11`, `Q-PM-12`. The G-strand is `Q-PM-G1` … `Q-PM-G7`.

| Commit | Date | `paper_inventory.json` SHA-256 | `paper_inventory.csv` SHA-256 |
|---|---|---|---|
| `ffee9ec55ff346b55136a3d3c532b8dbae70b209` | 2026-10-29 | `a509538dc5e1cf41cd7a4e180ed17df86f6d4cd83a7d227abea073f1689af4a3` | `8fc5bea9c57f486ea1099f4f9f3902f2537144c0f22af36f1b556a44d4891846` |
| `b81c4e700e3c35c3a57c0c868a387e009d39d321` | 2026-10-30 | `e20ce77e9e3af3bafdd4d6ae38a36213df2d98eb2dc89b2ecfebb4178a84341f` | `a63e08ce35ec81911399a06427924f2e430e5b1ccf11dc01a234462f09b11699` |
| `bf0c579d7d2b6099232774e9d6388b19159b983d` | 2026-11-01 | `b668dbde42473baa49ac1f02f89f900e94e39159c82efb8175ba125fef06d054` | `00062fed6d7aad189af86e4e489488db45d347f5426acf0f393695f406a194ef` |

- **Results**, identical for all three commits:
  - 3,386 records, 3,386 unique `paper_id`s;
  - 1,470 in the D-044 scope (first P0001, last P3161);
  - 194 G-strand records;
  - JSON and CSV agree on all IDs, their order, the scope list and the G count.
- **Across commits:** the 1,470 in-scope IDs are identical and in identical order; all 3,386 IDs are identical and in identical order. The 1,470 and the 194 agree with the 2026-10-29 count (`logs/session_logs/2026-10-29_SCOPE-SCHEDULE-DECISIONS.md`, count verification).
- **Distinction kept:**
  - (1) D-044's historical basis remains `a509538d…`;
  - (2) `e20ce77e…` and `b668dbde…` are later versions of the same record set, but their hashes differ because other fields changed, so they are **not interchangeable**;
  - (3) the inventory actually used at a future pilot draw is hashed and recorded at that time (D-077 (5)).
- **Limitations:**
  - the mapping of D-044's "G-1…G-7" to the tokens `Q-PM-G1` … `Q-PM-G7` is an inference, supported by the matching G-strand count of 194;
  - the check compares IDs and order only, not other fields;
  - it authorises no pilot draw and makes no record eligible or ineligible.

**Not changed**: `logs/DECISION_LOG.md` (no decision made); inventories; records; schemas; code; tests; generated outputs.

**Open, pending your content approval and a later authorised freeze**:
- Stage-0 list confirmation;
- final file names and status wording;
- the formal D-035 §6 recording approach;
- Stage-0 row timing;
- authorisation and implementation of the Stage-0 generator, the frozen `criteria_version` check and the pilot-sampling tool;
- the pilot-draw authorisation.

**Researcher planning preferences (2026-11-01; preferences, not decisions)**:
- keep v1.0 (`screening_criteria.md`) unchanged;
- consider version-specific file names for the new versions;
- record conditions 1–4 separately from conditions 5–6;
- implement software only after content approval and the freeze.

**Validation**: `git diff --check` and the CRLF-aware check before commit; both drafts still read "DRAFT … NOT frozen. Not in force"; inventory check reproduced as above. No test suite run (documentation only).

**Note**: both drafts describe the inventory comparison as "not yet recorded in the logs". This entry now records it; that draft wording is left unchanged in this task (no further draft edits authorised) and can be updated in a later documentation correction.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1`, parent `9308a6a`. This entry is part of one local commit whose hash it cannot contain; the hash is reported to the researcher and can be recorded in a later entry. Not pushed. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## PRE-FREEZE-RECONCILIATION — 2026-11-01 — documentation reconciliation of review issues I-1 to I-12 in the two screening drafts; open questions Q-081 to Q-089 (documentation only; not a freeze)

**Context**: researcher prompts 2026-11-01:
- evidence-driven resolution pass for the 12 issues of the pre-freeze review packet;
- read-only audit of the resulting diff ("return for correction": two wording issues, corrected in three locations);
- the three wording corrections;
- authorisation to write the governance logs;
- later the same day, after a further read-only audit: the Q-088/Q-089 split, question-ID cross-references in both drafts, and log clarifications.

**Documentation only.** No rule, E-code, decision, status or identifier changed. No screening rule was approved or frozen.

**Modified (drafts)**:
- `research/literature/screening_criteria_v1.1_draft.md`:
  - §1 heading and a new §1 note: the general "first applicable code in numerical order" rule is presented as a proposed convention [OPEN], because no approved decision adopts it (D-074 status); D-074 (d), Stage-0 E7 over E5, is kept as the only approved precedence;
  - §4: the diagram and Stage-0 bullet are qualified accordingly, and the Stage-0 list status is stated (conditional through D-025, provisional under D-068 (5), not confirmed for the freeze);
  - §6: the `criteria_version` enforcement gap is stated;
  - §7: audit timing marked [OPEN] (D-008 sets none; protocol v0.1 §7 "Expansion" row says first two batches);
  - §10: heading and column corrected so that settled rows and [OPEN] rows are distinguished, and rows added: PREC, D-076 (8), STAGE0-T, AUDIT-T, D-030;
  - §11 step 3: the D-035 §6 condition 5 file-name reference is explained;
  - §9: one traceability row.
- `research/literature/screening_protocol_v0.2_draft.md`:
  - §5 item 2: `criteria_version` enforcement gap;
  - §6: precedence presented as in the criteria;
  - §7 "If not passed": the undefined retry details marked [OPEN];
  - §7 missing-abstract row: statuses aligned with D-068 (8) and D-079;
  - §8: audit timing [OPEN];
  - §10 rows 3 and 6: condition 3 sufficiency and condition 6 scope marked [OPEN];
  - §11: one traceability row.
- **Wording corrections after the audit:**
  - "No rule changed" (criteria §9, protocol §11) → "No approved rule changed; the general code-precedence rule, which no approved decision adopts, is now presented as a proposed convention";
  - protocol §7 "(protocol v0.1 §7, under D-025)" → "(protocol v0.1 §7; D-025 approved its "pass criteria and adjudication as written" but does not name the retry)".
- `research/reviews/unresolved_questions.md`: Q-081 to Q-089 added (Q-080 was the last ID; no Q-081 or higher existed). Q-089 (Stage-0 row timing) was split from an initial combined Q-088 before commit; Q-088 keeps file names, status wording and superseded notes. Duplicate handling is already open as Q-024 and Q-029, so no new entry.
- **Question-ID cross-references (added after the first logging pass):** Q-081 to Q-089 were added to the matching [OPEN] items in both drafts:
  - `research/literature/screening_criteria_v1.1_draft.md`: §1 note and §10 PREC (Q-081); §10 D-076 (8) (Q-082); §7 audit and §10 AUDIT-T (Q-084); §11 step 3 (Q-088); §10 STAGE0-T (Q-089);
  - `research/literature/screening_protocol_v0.2_draft.md`: §6 (Q-081); §7 "If not passed" (Q-083); §8 (Q-084); §10 row 3 (Q-085), row 6 (Q-086) and status terms (Q-087); §3 (Q-089).

  Only the IDs were added; no wording, rule or status changed.

**Created**: `logs/session_logs/2026-11-01_PRE-FREEZE-RECONCILIATION.md`.

**Issue status**:
- settled from approved evidence: I-4 (wording), I-9, I-10, I-11 (drafts already consistent);
- partly settled: I-3;
- your decision needed: I-1, I-2, I-5, I-6, I-7, I-8;
- missing software: I-6, I-12 (no Stage-0 generator, no pilot-sampling tool, no `criteria_version` check).

**Validation**: `git diff --check` and the CRLF-aware check exit 0; consistent table column counts; quotations checked against `screening_criteria.md` line 26, `screening_protocol.md` lines 116, 145 and 146, and the D-008, D-024, D-025, D-027, D-030, D-059, D-068 (8), D-074, D-076 and D-079 entries. **Not performed:** scientific validation of any screening rule; no test suite run (no code changed).

**Unchanged**: `logs/DECISION_LOG.md`; decision statuses; D-035 §6 conditions (none formally recorded as met; 5 and 6 unmet); both drafts "DRAFT … NOT frozen. Not in force"; code, schemas, tests, inventories, records.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `e70a038` (2 earlier commits not pushed); these changes uncommitted; not pushed. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## PRE-FREEZE-DECISIONS — 2026-11-01 — five researcher-approved pre-freeze decisions recorded (D-080 to D-084); drafts renamed; not a freeze

**Context**: the researcher approved five recommendations of the read-only pre-freeze decision sheet (2026-11-01) and four procedural choices (2026-11-01), and authorised their documentation-only implementation. Not a freeze; no content approval; no screening, sampling, extraction, pilot work or training; no commit or push in this task.

**Decision records**:
- `logs/DECISION_LOG.md`, new section:
  - D-080: primary exclusion code = first applicable code in numerical order, with the D-074 (d) E7-over-E5 Stage-0 exception; APPROVED — CONDITIONAL, inactive; effective at the freeze;
  - D-081: final file names; APPROVED;
  - D-082: Stage-0 list confirmed against protocol v0.1 §3; APPROVED — CONDITIONAL, inactive; to be restated in the freeze entry;
  - D-083: Q-082 to Q-084 kept open at the freeze, with their "Needed by" restrictions unchanged; APPROVED;
  - D-084: freeze procedure approved in principle, with the amended text to be reviewed before execution.
- Status-history rows: D-080 to D-084 new; D-074 (its "not part of an approved decision" note superseded by D-080; row text kept); D-068 ((5) confirmation given).
- `research/reviews/unresolved_questions.md`: Q-081 answered (D-080); Q-088 partly answered (D-081; status wording and superseded notes still open; step reference updated to §11 step 2); Q-082 to Q-084 annotated "kept open at the v1.1 freeze (D-083)", still Open.

**Drafts**:
- **Renamed** (plain move; not staged): `research/literature/screening_criteria_v1.1_draft.md` → `screening_criteria_v1.1.md`; `screening_protocol_v0.2_draft.md` → `screening_protocol_v0.2.md`. Both still read "DRAFT … NOT frozen. Not in force".
- **Criteria v1.1**:
  - §1 heading and note: D-080;
  - §4 diagram and Stage-0 bullet: D-080; list status confirmed (D-082);
  - §7 pilot reference and header Companion: new protocol name;
  - §10 rows PREC (settled, D-080), Q-074 (D-082), D-076 (8) and AUDIT-T (kept open, D-083);
  - §11 rewritten as the amended freeze procedure (D-084; not executed);
  - §9 traceability row; governing decisions list.
- **Protocol v0.2**:
  - header Replaces (new criteria name) and governing decisions;
  - §3 Stage-0 confirmation (D-082);
  - §6 rule (D-080);
  - §7 retry and §8 audit kept open (D-083);
  - §11 traceability row.
- **Unchanged:** `screening_criteria.md` (v1.0), `screening_protocol.md` (v0.1), historical logs and reviews (old names kept), code, schemas, tests, inventories.

**Deviation from the plan**: the plan's Q-083 restriction ("no second pilot until … recorded as a new criteria/protocol version") would have strengthened the register's "Needed by" ("Before a second pilot, if the first fails"); the register wording was used unchanged, as instructed.

**Validation**: see the session log (`git diff --check`, CRLF-aware check, register column and ID checks, reference checks, v1.0/v0.1 hashes). No tests run (no code change). Not performed: scientific validation.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `c036f47`; uncommitted; not pushed. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed. The researcher's choice of a separate rename commit applies when committing.

**Corrections after the read-only review (researcher-approved, 2026-11-01)**:
- (A) The header of both active documents now describes §11 as approved in principle only under D-084, requiring researcher review and approval before execution.
- (B) Criteria §9 now distinguishes the statuses of D-080 through D-084 and identifies D-084 as approved in principle.
- (C) The session log records the validation commands and their observed outcomes.
- (D) Q-082's full "Needed by" wording is preserved in D-083, criteria §10 row D-076 (8), and the session log.

These are documentation corrections only. No research decision, approval status, restriction, or research-execution authorization has changed. Q-082 remains open.

## PHASE1-SCREENING-TOOLS — 2026-11-01 and 2026-11-11 — Phase 1 screening tools, independent review and five corrections (synthetic fixtures only; not a freeze)

**Context**:
- 2026-11-01: the researcher approved the Phase 1 design defaults (D-085) and authorised Phase 1 implementation and testing with 12 restrictions (D-086);
- an independent read-only review then found five implementation weaknesses;
- 2026-11-11: the researcher authorised their correction, regression tests, the logs, and recording D-085 to D-087.

No real-data operation, freeze, commit or push.

**Created**:
- `scripts/literature/stage0.py`: Stage-0 generator (D-082, D-074, D-080; D-085 A1–A5);
- `scripts/literature/pilot_sample.py`: pilot sampler (C1 parameters of D-025, D-063 and D-077 unchanged; D-085 C2–C4);
- `scripts/literature/pilot_sheet.py`: blinded pilot sheet (D-085 D1–D3, D5; D-087);
- `tests/literature/test_phase1_screening_tools.py`: 64 tests;
- `logs/session_logs/2026-11-11_PHASE1-SCREENING-TOOLS.md`.

**Modified**:
- `scripts/literature/pubrecords.py`: frozen criteria-version registry (`load_criteria_registry`, cross-checked against `DECISION_LOG.md`); validator checks for `criteria_version` (format; registered frozen value once a registry exists; fail closed, B2–B4); run-authorisation check (`verify_run_authorisation`); `load_screening_decisions(lit_dir, path=None)` so a candidate file can be validated before it replaces the real one;
- `research/literature/schemas/screening_decision.schema.json`: `criteria_version` `pattern` only (a format guard; B1, the identifier, stays open).

**Corrections (2026-11-11)**:
1. Run authorisation verified against `DECISION_LOG.md`: a decision row with status starting "**APPROVED**" and the exact marker "Run authorisation under D-074 (f)" or "Run authorisation under D-077 (6)". Invented, malformed, conditional, in-principle, duplicated or wrong-clause references are refused. No current decision carries either marker, and the marker wording is open (Q-090).
2. Stage-0 writes are atomic: the original file plus the new rows are written to a temporary file, validated, then moved into place. A validation failure leaves the original unchanged.
3. The sampler builds its frame through the shared checked guards (`stage0.check_types`: A1 union guard, A2 variant stop).
4. The Stage-0 run report records the SHA-256 of `publications.jsonl` and `source_records.jsonl`; the sampler sidecar records them too.
5. Input validation:
   - `run_date` must be a real calendar date;
   - the type guards apply to D-044 in-scope records;
   - the pilot-sheet command line refuses unless the sample, its provenance sidecar, the current inventory and the authorisation agree.

**Decision records**: `logs/DECISION_LOG.md` D-085, D-086, D-087, with status-history rows; `research/reviews/unresolved_questions.md` Q-090 (run-authorisation marker convention).

**Validation (actual runs)**:
- 2026-11-01 17:48:22 UTC, initial implementation: literature 259 OK (42 new), data protection (strict) 10 OK, NHANES 29 OK, query table PASS (168 rows), whitespace checks OK.
- 2026-11-11 02:41:02–02:42:38 UTC, after the corrections: Phase 1 module 64 OK; literature 281 OK; data protection (strict) 10 OK; NHANES 29 OK; query table PASS (168 rows).
- Not performed: any run on the real inventory, including the check that the real frame equals 1,463 and the F1 stratum sizes; scientific validation.

**Unchanged**:
- approved decisions and statuses;
- criteria v1.1, protocol v0.2, v1.0 and v0.1;
- the inventory and records;
- `.gitignore`;
- PR #17.

No `screening/decisions.csv`, Stage-0 row, pilot sample, pilot sheet or criteria registry exists.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `4b56345`; uncommitted; not pushed. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## RUN-AUTH-Q090 — 2026-11-11 — run-authorisation marker anchored to the start of the Decision cell; Q-090 resolved (D-088); no run authorisation created

**Prompt**: researcher prompt "Fix Run Authorisation Validation and Resolve Q-090" (2026-11-11). Starting state verified: branch `claude/eloquent-mccarthy-bqtxr3-part1`, HEAD `7f5b608`, clean working tree.

**Code** (`scripts/literature/pubrecords.py`):
- `RUN_AUTHORISATION_MARKERS` are now the bold sentences approved in D-088, one per clause (D-074 (f), D-077 (6)).
- `verify_run_authorisation`: the old check `marker not in decision` (marker anywhere in the cell) is replaced by `decision.strip().startswith(marker)`. Only the cell's surrounding whitespace is ignored; a marker in the middle or at the end of the cell is refused.
- Unchanged: the D-ID format check, the decision-log existence check, the single-decision-row requirement, and the status-prefix check `**APPROVED**`, which refuses conditional, in-principle, proposed and pending decisions.

**Tests** (`tests/literature/test_phase1_screening_tools.py`):
- New class `RunAuthorisationMarkerAnchoring` (10 tests): marker at the start accepted; surrounding spaces and tabs ignored; marker in the middle or at the end refused; a Q-090-style description refused under three statuses and both clauses; near-miss markers refused (not bold, lower case, inner space, no full stop, leading `> `, leading character); wrong clause; conditional, in-principle, implementation-decision, proposed and pending statuses; duplicate decision rows; the real `DECISION_LOG.md` has no Decision cell beginning with a marker.
- Updated: three expected refusal messages ("does not state" → "does not begin with"); the fixture helper and one sheet fixture now put the marker at the start of the cell. No test was removed, skipped or weakened.

**Decision records**:
- `logs/DECISION_LOG.md`: D-088 (Q-090 convention; **APPROVED — implementation decision**), with a status-history row. D-088 was checked as unused first. Its Decision cell begins with "**Q-090: run-authorisation convention.**", not with a marker. No run-authorisation row was created.
- `research/reviews/unresolved_questions.md`: Q-090 answered → D-088.

**Validation (actual runs, 2026-11-11 03:21:30–03:23:08 UTC)**:
- focused run-authorisation tests 14 OK;
- Phase 1 module 74 OK;
- literature 291 OK;
- data protection (strict) 10 OK;
- NHANES 29 OK;
- query table PASS (168 rows);
- SHA-256 of `publications.jsonl`, `source_records.jsonl` and `paper_inventory.json` identical before and after;
- Decision cells beginning with a marker: 0.
- The whitespace checks after the log edits are reported in the task report.

**Not machine-checked yet**: the exact status text `**APPROVED** — run authorisation (single use)` (the code checks the `**APPROVED**` prefix), and the D-088 (4) bindings (`criteria_version`, `inventory_sha256`, freeze entry, D-035 §6 entry, single use).

**Unchanged**: data and inventory files; `.gitignore`; approved decisions; the drafts; PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17). No real-data run, screening output, registry, freeze or run authorisation.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `7f5b608`; uncommitted; not pushed.

## STAGE-B-PREPARATION — 2026-11-11 — Stage B preparation package: documentation refresh, frame-only and identity checks, hardened run authorisation, pilot follow-on tools, D4 ignore rules, decisions D-089 to D-096 (synthetic fixtures only; not a freeze)

**Prompt**: researcher prompt "Proceed with the approved BioML-Insight Stage B preparation work" (2026-11-11). Starting state: branch `claude/eloquent-mccarthy-bqtxr3-part1`, HEAD `8d9bd79`, clean working tree, in sync with the remote.

**Code**:
- `scripts/literature/pubrecords.py` (P16):
  - `verify_run_authorisation` now requires:
    - the exact status `**APPROVED** — run authorisation (single use)`;
    - the D-088 (4) bindings in the D-095 syntax (`criteria_version`, `inventory_sha256`, `freeze_entry`, six `d035_s6_records`, `single_use: yes`), each exactly once;
    - one approved decision row for the freeze entry, matching the registry entry of the bound version;
    - six distinct approved §6 rows, each beginning with "**D-035 §6 condition N recorded as met.**", covering 1–6;
    - when the tool passes them, equality with the run's inventory SHA-256 and `criteria_version`.
  - New single-use ledger `screening/run_authorisation_ledger.jsonl` (`check_authorisation_unused`, `record_authorisation_use`): one Stage-0 write per D-074 (f) authorisation; one draw and one sheet per D-077 (6) authorisation; fail closed on malformed content.
  - `load_criteria_registry_entries` added; `load_criteria_registry` is unchanged in behaviour.
- `stage0.py`, `pilot_sample.py`, `pilot_sheet.py`: pass the run's inputs to the check and use the ledger. Dry runs consume nothing.
- `pilot_sample.py`:
  - P17: `load_scope_snapshot` (recorded SHA-256 `a5d4851f…53ea`) and `verify_frame_identity` (frame = snapshot minus the seven F1 Stage-0 IDs; missing, additional and duplicated IDs refused), run before any draw.
  - P15: `--frame-only` validates count, strata and identity with no draw, no output and no authorisation.
- New `scripts/literature/pilot_agreement.py` (P18): Cohen's κ and agreement measures with the D-025 pass evaluation (thresholds unchanged); the researcher decision template (paper IDs only); the adjudication-queue builder.
- `.gitignore` (D4, D-096): ignores the blinded sheet, `*_sheet_*.csv` and `*.tmp` under `research/literature/screening/`. The audit-trail files stay trackable.

**Tests**:
- `tests/literature/test_phase1_screening_tools.py`: 33 new tests (P16 bindings and ledger 12, plus 1 Stage-0 binding test in an existing class; P17 identity 5; P15 frame-only and synthetic draw 5; P18 agreement, template and queue 10). Two existing tests were renamed (see below).
- Existing fixtures updated to write complete authorisations, because the checks are stricter.
- Three existing expectations changed:
  - a second Stage-0 `--write` is now refused (single use), where it was previously an idempotent rewrite; the dry-run idempotence is still tested;
  - a changed inventory is now refused by the inventory binding check, before the provenance check;
  - the default sheet path is now ignored (D4).
- The fixture freeze entry is D-999, so the "invented ID" case uses D-977.
- No test was skipped or removed.
- `tests/data_protection/test_data_protection.py`: the ignored and trackable screening paths were added.
- Mutation check: disabling the exact-status check, the ledger or the identity check makes 1, 4 and 3 tests fail respectively.

**Documents**:
- `screening_criteria_v1.1.md` and `screening_protocol_v0.2.md` (P1), still DRAFT:
  - the Phase 1 tools and the hardened checks are reflected;
  - stale "not yet enforced" and "no committed script" statements are corrected;
  - paraphrase-only justifications (D-089);
  - Stage-0 timing (D-093);
  - superseded notes at the freeze (D-090);
  - condition-6 list and recording form (D-091, D-092);
  - agreement computation and operational definitions (D-094; Q-091 open);
  - private sheet exchange (D-096).
  - **No inclusion or exclusion rule, research question, scope definition or threshold changed.**
- New `research/literature/pilot_procedure_assistant.md` (DRAFT, D-094).

**Decision records**:
- `logs/DECISION_LOG.md`: D-089 to D-096 with status-history rows (IDs checked as unused first).
- `research/reviews/unresolved_questions.md`:
  - Q-086, Q-087 and Q-089 answered;
  - Q-088 still partly open;
  - Q-091 and Q-092 added;
  - Q-085 unchanged (evidence in the session log; not decided).

**Validation (actual runs, 2026-11-11 04:28:22–04:30:04 UTC)**:
- Phase 1 module 107 OK;
- literature 324 OK;
- data protection (strict) 10 OK;
- NHANES 29 OK;
- query table PASS (168 rows);
- SHA-256 of `publications.jsonl`, `source_records.jsonl` and `paper_inventory.json` unchanged; inventory, records, scope and raw exports equal HEAD;
- no `screening/` directory and no `criteria_registry.json`.
- The whitespace checks after the log edits are reported in the task report.

**Not done**: no real-data run (the frame-only check included), Stage-0 run, pilot sample or sheet, screening output, run authorisation, freeze, or D-035 §6 record. No commit or push. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

**Branch / commit / PR**: `claude/eloquent-mccarthy-bqtxr3-part1` at `8d9bd79`; uncommitted.

## STAGE-B-AUDIT-CORRECTIONS — 2026-11-11 — corrections to the uncommitted Stage B preparation package after the pre-commit audit (PASS WITH ISSUES); proposals D-097 to D-100; Q-093 to Q-095 (synthetic fixtures only; not a freeze)

**Prompt**: researcher prompt "The final audit returned PASS WITH ISSUES. Implement the necessary corrections before the first commit" (2026-11-11). Starting state: branch `claude/eloquent-mccarthy-bqtxr3-part1`, HEAD `8d9bd79`, the 17 uncommitted files of STAGE-B-PREPARATION, nothing staged.

**Findings addressed**:
- **M2 (D-093 enforced):** `pilot_sample.verify_stage0_rows`. Before drawing, `decisions.csv` must hold exactly one `rule:stage0` title/abstract `exclude` row per approved Stage-0 record, with its F1 code (P0028, P0099, P0113, P0624, P0830 → E5; P0931, P0939 → E7), and no other `rule:stage0` row.
- **M5:** an include/exclude conflict is resolved only by a separate adjudication row for the same pilot paper, at `title_abstract`, with `screener=researcher` and a pilot decision. Any other adjudication row is refused. The latest row is the agreed decision.
- **L3:** the adjudication queue lists every pair in `dedup_review.csv`; a member without a decision is listed with an empty stage.
- **L5:**
  - an exclusive run lock (`screening/.run_lock.tmp`, created with `O_EXCL`; never removed automatically after a crash);
  - "started" and "completed" ledger events, with a consistency check;
  - an interrupted run consumes its authorisation (fail closed);
  - outputs are written without overwriting (temporary file, `fsync`, hard link). The sheet's temporary file must itself be ignored by Git;
  - the sheet requires a completed draw with the same authorisation;
  - a sheet path that is not ignored is refused before the authorisation is consumed.
- **M4:**
  - D-092, D-094 and D-095 no longer present assistant conventions as researcher decisions. The removed sentences are preserved verbatim in the session log, and status-history rows record the correction.
  - The conventions are recorded as **PROPOSED** D-097 (run-authorisation formats; Q-092) and D-098 (pass-rule operational definitions; Q-091).
- **H1:** procedure proposed as **PROPOSED** D-099, with Q-093 opened. Steps (1)–(5) are not implemented.
- **M1:** two options proposed as **PROPOSED** D-100, with Q-094 opened.
- **M3** is not decided; it is registered as Q-095, and procedure §4 is marked [OPEN].
- **L1:** the Q-088 status cell rewritten as one consistent statement.
- **L2:**
  - `stage0.py` and `pilot_sample.py` docstrings corrected;
  - criteria v1.1 §11 step 1 now lists D-085 to D-096 and excludes proposals;
  - protocol v0.2 §10 heading date corrected.

**Tests**:
- 19 new tests: Stage-0 rows 4; adjudication evidence 4; lock, interruption and ledger 6; no-overwrite and sheet 5.
- Existing fixtures and expectations were updated for the ledger events, the completed draw before a sheet, the Stage-0 rows before a draw, the adjudication rows, and all duplicate pairs in the queue. No test was skipped or removed.
- Mutation check: disabling the Stage-0 row check, the adjudication screener check, the lock's `O_EXCL`, or "an interrupted run consumes the authorisation" makes 2, 1, 3 and 1 tests fail respectively. The source was restored and compared byte for byte.

**Validation (actual runs, 2026-11-11 08:42:24–08:44:01 UTC)**:
- Phase 1 module 126 OK;
- literature 343 OK;
- data protection (strict) 10 OK;
- NHANES 29 OK;
- query table PASS (168 rows);
- SHA-256 of `publications.jsonl`, `source_records.jsonl` and `paper_inventory.json` unchanged; inventory, records, scope, raw exports, v1.0 and v0.1 equal HEAD;
- no `screening/` directory.
- The whitespace checks after the log edits are reported in the task report.

**Not done**: no real-data run, Stage-0 run, pilot sample or sheet, run authorisation, activation-condition record or freeze. Q-085, Q-088, Q-091 and Q-092 not decided; H1, M1 and M3 not decided. No commit, stage or push. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## GOVERNANCE-RECONCILIATION — 2026-11-11 — researcher preferences on D-090 and Q-091 to Q-095 recorded; provisional decisions marked as provisional; assistant procedure integrated into protocol v0.2 §7a; hash-first workflow proposed (not a freeze)

**Prompt**: researcher prompt "Prepare the final governance reconciliation" (2026-11-11). Starting state: branch `claude/eloquent-mccarthy-bqtxr3-part1`, HEAD `8d9bd79`, the 18 uncommitted files of the Stage B package, nothing staged.

**Decision records** (`logs/DECISION_LOG.md`; 10 status-history rows; replaced text preserved in the session log):
- **D-090:** the timing is now the researcher's confirmation (superseded notes at the formal freeze), not the assistant's reading.
- **D-091:** the approved list is unchanged; the scope of item (a) is stated as open (new Q-096).
- **D-097:** PROPOSED → **APPROVED — PROVISIONAL**, subject to final review.
- **D-098:** PROPOSED → **APPROVED — PROVISIONAL**, subject to consistency with D-025. Consistency check:
  - (a) is consistent;
  - (b) as proposed was broader than D-025 ("without adjudicated agreement on the exclusion") and is aligned: only an adjudicated `exclude` resolves an include/exclude conflict;
  - (c) is not covered by D-025; no pass is reported without κ ≥ 0.60.
- **D-099:** PROPOSED → **APPROVED — PROVISIONAL**, including the rule that an interrupted run consumes its authorisation. Steps (1)–(5) are not implemented.
- **D-100:** PROPOSED → **APPROVED**, Option A.
- **New D-101:** **APPROVED — CONDITIONAL (inactive)** — the assistant's pilot decisions are not exposed before the researcher's independent screening is complete.
- **New D-102:** **PROPOSED** — the hash-first workflow.
- Cross-references in D-092, D-094 and D-095 updated; a note added to the D-097–D-100 section introduction.
- No provisional row is marked as finally approved. None starts with the `**APPROVED**` prefix that the tools require for a freeze entry or a condition record.

**Register**:
- Q-088: D-090 timing confirmed; final status wording still open.
- Q-091, Q-092, Q-093: provisionally answered (not final).
- Q-094: answered (Option A).
- Q-095: partly answered (D-101), with the workflow proposed in D-102.
- New Q-096: scope of D-091 item (a).
- Q-085 unchanged.

**Documents**:
- Protocol v0.2:
  - new §7a, the assistant pilot procedure (Option A), with the D-101 requirement and the D-102 workflow marked PROPOSED;
  - the §7 "Pass" row restores the D-025 wording ("agreement on the exclusion"; "≥ 3 disagreements on one code"), which v0.2 had shortened;
  - D-097 to D-099 marked provisional; outputs, §10 and §11 updated.
- `pilot_procedure_assistant.md` reduced to a pointer to §7a.
- Criteria v1.1: header, the D-090 timing in §11 step 2, §11 step 1 (provisional decisions and proposals), §9.
- No exclusion rule, threshold, sample parameter or RQ changed.

**Code**:
- `pilot_agreement.py`: an include/exclude conflict is resolved only by an adjudicated `exclude` (D-025; D-098 (b)); docstrings and report text say provisional.
- `pubrecords.py`: comments only.

**Tests**:
- 1 new test (`test_only_agreement_on_the_exclusion_resolves`).
- 2 tests updated for the D-025 rule: an adjudicated `include` now leaves the conflict unresolved.

**Validation (actual runs, 2026-11-11 08:56:30–08:58:03 UTC)**:
- Phase 1 module 127 OK;
- literature 344 OK;
- data protection (strict) 10 OK;
- NHANES 29 OK;
- query table PASS (168 rows);
- ignored data-file hashes unchanged; inventory, records, scope, raw exports, v1.0 and v0.1 equal HEAD;
- `.gitignore` unchanged in this task; no `screening/` directory.
- The whitespace checks are reported in the task report.

**Not done**: Q-085 not decided; no freeze, activation-condition record, run authorisation, real-data processing, stage, commit or push. The D-102 ignore rule and tool support were not implemented. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## B1-B6-APPROVALS — 2026-11-11 — researcher approvals B1–B6 recorded; D-098 marker and undefined-κ rule implemented; final drafts of criteria v1.1 and protocol v0.2 prepared for content approval (not a freeze)

**Prompt**: researcher prompt "The researcher has approved B1–B6 according to the recommendations in the latest decision report" (2026-11-11). Baseline: commit `c6e1b14` (preparation package), clean working tree.

**Decision records** (`logs/DECISION_LOG.md`; 6 status-history rows; replaced text preserved in the session log):
- **D-097:** final (**APPROVED — implementation decision**).
- **D-098:** final (**APPROVED — CONDITIONAL**, inactive; effective at the freeze):
  - (a) exactly-one-screener code counting, include/exclude disagreements included;
  - (b) only an adjudicated `exclude` resolves a conflict, whatever its code;
  - (c) an undefined κ is not passed;
  - (d) pilot adjudication marker `screener=researcher:adjudication`.
- **D-099:** final (**APPROVED**). Steps (3) and (4) are authorised for implementation after the freeze and are required before the first authorised run.
- **D-102:** approved (**APPROVED — CONDITIONAL**, inactive): salt line, independent custodian (encrypted copy or custodian-held file). Custodian appointment is pending.
- **New D-103:** the identifier `criteria_v1.1+protocol_v0.2` (B1).
- **New D-104:** the freeze-commit status wording and superseded note (B2; answers Q-088).

**Register**:
- Q-088, Q-091, Q-093 and Q-095 answered.
- Q-092 partly answered; (c) open.
- Q-085 and Q-096 unchanged (open).

**Code**:
- `pilot_agreement.py`:
  - `ADJUDICATION_SCREENER = "researcher:adjudication"`; adjudication rows need it;
  - pilot files are checked for `screener=assistant` and `screener=researcher`;
  - an undefined κ gives `pass=False` and `kappa_undefined=True`, and the report reads "NOT PASSED (kappa undefined)".

**Tests**:
- 3 new: marker and pilot screeners; agreed exclusion with another code; include/exclude counting.
- Adjudication fixtures now use the marker; the undefined-κ expectation changed to "not passed".

**Documents** (final drafts for content approval; not frozen):
- Protocol v0.2:
  - `criteria_version` header row (D-103);
  - Version row stating the D-104 freeze wording;
  - §5 item 3 (the marker);
  - §7 rows with the final D-097, D-098, D-099 and D-102 text, Q-092 (c) marked open;
  - §7a final (salt, custodian, preconditions);
  - §10 row 6 (Q-096 open);
  - §11.
- Criteria v1.1:
  - header rows;
  - §9;
  - §11 reviewed under D-084: step 1 (decisions D-080 to D-104), step 2 (D-104 wording), step 5 (open questions at the freeze), step 6 (freeze-commit contents), step 8 (reserved ID), new step 9a (registry), step 10.
- No exclusion rule, threshold, sample parameter or RQ changed.

**Validation (actual runs, 2026-11-11 09:34:32–09:36:02 UTC)**:
- Phase 1 module 130 OK;
- literature 347 OK;
- data protection (strict) 10 OK;
- NHANES 29 OK;
- query table PASS (168 rows);
- ignored data-file hashes unchanged; data, scope, v1.0, v0.1 and `.gitignore` equal `c6e1b14`;
- 87 decision IDs, none accepted as a run authorisation, no condition row.

**Not done**: no freeze, activation record, run authorisation, Stage 0, sampling or real-data processing. Q-085, Q-092 (c) and Q-096 not decided. No stage, commit or push. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## AUDIT-DECISIONS — 2026-11-11 — researcher decisions on the final consistency audit applied (A1, B1 with Q-063, D-105 to D-109; D-108 kept PROPOSED; R1 selected for design)

**Prompts**:
- researcher prompt "I have reviewed the final consistency and governance audit dated 2026-11-11" (decisions);
- researcher prompt "Researcher instructions — BioML-Insight governance update (2026-11-11)" (application of `proposed_changes_v2.py` with `--with-q063`).

**Pre-checks**:
- every replacement target was found exactly once in the working tree;
- D-105 to D-109 were unused;
- the three target files were backed up outside the repository (SHA-256 recorded), with automatic restore on failure.

The script applied cleanly; no restore was needed. The uncommitted B1–B6 work was preserved.

**Changes**:
- `research/literature/screening_criteria_v1.1.md`:
  - §4 when-in-doubt rule restored (D-105);
  - §11 step 5 open-question list (D-106);
  - two §9 rows.
- `research/reviews/unresolved_questions.md`: Q-063 "Needed by" revised. It does not block the document freeze; the off-device backup comes before the fixed-inventory entry and the next rebuild; a verified restore comes first in any rebuild or provenance-check workspace. Q-063 stays **Open**.
- `logs/DECISION_LOG.md`:
  - D-105 (APPROVED); D-106 (APPROVED); D-107 (APPROVED IN PRINCIPLE, subject to verification; verified inventory hash vs observed ignored-file hashes with incomplete provenance); D-108 (**PROPOSED**); D-109 (APPROVED — design work only);
  - status-history rows: D-025, D-093, D-097 (B2 deferred), D-102, D-105 to D-109, D-106 (Q-063 wording applied), D-109 (R1 selected, R2 fallback), D-108 (kept PROPOSED).

**Not done**:
- no fixed-inventory entry, activation-condition row, registry, run authorisation, Stage 0, draw, sheet, real screening or freeze;
- no custodian appointed, no keys, no encryption, no blinding tools;
- the D-102 (R1) revision is prepared for review only (not in the repository);
- no stage, commit or push. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## GOVERNANCE-REVIEW-FIXES — 2026-11-11 — approved documentation corrections from the governance review (C1, C2 Option Y, C4, B-m1 to B-m4); documentation only

**Prompt**: researcher prompt "Apply the approved documentation corrections from the 2026-11-11 governance review, using Option Y for C2" (2026-11-11).

**Pre-checks**: every target matched exactly once; Q-097 unused; seven files backed up outside the repository, with automatic restore on failure. Applied cleanly; no restore was needed.

**Changes**:
- **Protocol v0.2:**
  - §10 row 6 (d): the fixed-inventory entry comes before condition 6. It records the verified inventory hash and the observed hashes and provenance status of the ignored files. The condition-6 row refers to it by ID; the authorisations bind the same hash. D-108 is named as proposed, not approved.
  - §1: the inventory is fixed before condition 6 (D-107) and recorded again at the draw (D-077 (5)).
  - §7a: governing note (D-102 revision pending); precondition reworded (obsolete custody form removed); step 5 replaced by "[OPEN: revision of D-102 pending …]. The pilot cannot start until the revision is approved."
  - §11: traceability row.
- **Criteria v1.1:**
  - §0: the inventory is fixed before condition 6 (D-107) and recorded again at the draw.
  - §11 step 5: adds the proposal D-108 and the pending D-102 revision.
  - §9: traceability row.
- **Register:**
  - Q-063 status note now covers rebuilds and provenance checks (still Open);
  - new Q-097 (provenance method for the ignored record files; needed before the fixed-inventory entry; Open).
- **Decision log:** status-history rows for D-107 (verification of `paper_inventory.json` completed; ignored-file provenance outstanding, Q-097), D-106 (list extended) and D-102 (revision pending in §7a; not revised). No status changed. D-108 remains PROPOSED.
- The freeze-readiness checklist (outside the repository) was updated.

**Not done**: no D-102 revision approved or implemented; no R1 or R2, custodian, keys, commitments or tools; no fixed-inventory entry, condition rows, registry, authorisations, Stage 0, draw or real-data screening; no data, raw-export, inventory or ignored-record change; no freeze, stage, commit or push. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## FINAL-PRE-FREEZE-AUDIT — 2026-11-11 — consolidated final consistency audit of criteria v1.1 and protocol v0.2; safe documentation corrections; approval package (documentation only; not a freeze)

**Prompt**: researcher prompt "We are moving BioML-Insight towards its document freeze…" (2026-11-11).

**Safe corrections** (wording fixed by approved decisions; target strings pre-checked; backups and automatic rollback):
- **Register:** Q-063 punctuation ("…decision. Update 2026-11-11 (D-106): …"); status, restrictions and meaning unchanged; still Open.
- **Criteria v1.1:**
  - header decision range (to D-107 and D-109; D-108 a proposal);
  - wording rule (where open items are listed);
  - §11 steps 1, 5 and 10 (approved decision range; open proposals and pending items; the D-107 condition-6 (d) requirement);
  - §9 row.
- **Protocol v0.2:**
  - header range;
  - §2 paraphrased justification (D-089);
  - §9 (Q-068 answered by D-064; no record verified after the authorised builds);
  - §10 rows 5 and 6 (a) brought up to date;
  - §11 (Q-022 answered by D-065; traceability row).

**New**: `research/reviews/final_pre_freeze_approval_package_2026-11-11.md` (reviews, cross-document results, decisions D1–D10, freeze readiness 9/14, freeze-entry structure, commit sequence, approval checklist).

**Not done**: no decision approved; no status cell changed; no freeze; no FROZEN status; no registry, fixed-inventory entry, condition rows or authorisations; no custodian, D-102, R1 or R2 implementation; no Stage 0, sampling or screening; no data change; no stage, commit or push. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## D1-D2-APPLIED — 2026-11-11 — D1 (Q-097 in protocol §10 and criteria §11 step 5) and D2 (protocol §7 D-102 details neutralised) applied; D3 left unchanged; approval package updated (documentation only; not a freeze)

**Prompt**: researcher prompt "We are approaching the document freeze for BioML-Insight" (2026-11-11). D1 YES, D2 YES, D3 LEAVE. This is not content approval, freeze approval or Git authorisation.

**Changes** (targets pre-checked; backups with automatic rollback):
- **Protocol v0.2:**
  - §10 row 6 (d) names Q-097;
  - §7 Screeners and Outputs rows say "form and timing set by the revision of D-102 pending in §7a step 5" instead of the D-102 workflow details; D-101 kept;
  - §11 row.
- **Criteria v1.1:** §11 step 5 adds Q-097; §9 row.
- **Decision log:** history rows on D-106 (Q-097 added to the list) and D-102 (§7 neutralised; revision pending). No status cell changed (D3).
- **Package:** `final_pre_freeze_approval_package_2026-11-11.md` rewritten with the D1/D2 evidence, freeze readiness 9/14, exact freeze-entry fields, exact commit sequence and the approval checklist.

**Not done**: no freeze, FROZEN status, freeze entry, registry, condition rows, authorisations or D-102 implementation; no data change; no stage, commit or push. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## PRE-FREEZE-GOVERNANCE-REVIEW — 2026-11-11 — comprehensive pre-freeze governance review; Q-063 wording corrected to D-010; D-107 described as approved in principle; approval package rewritten (documentation only; not a freeze)

**Prompt**: researcher prompt "We need to complete a comprehensive pre-freeze governance review of the BioML-Insight research repository" (2026-11-11).

**Baseline**: HEAD `c6e1b14`, 1 ahead of the remote, nothing staged; working-tree diff and file hashes captured before editing.

**Corrections** (targets pre-checked; backups with automatic rollback):
- **Q-063 register text:**
  - What was wrong: the D-106 wording said the off-device backup was "outstanding" and had to be "established". This contradicted D-010 and the Q-011-OPTION-B record (a private Google Drive folder designated; Drive-copy hashes reported by the researcher as matching).
  - Corrected to: the backup is designated, and its provenance (approval details; PRESERVED status; researcher-reported hashes) is what remains open, before the fixed-inventory entry and the next rebuild; a verified restore comes first in each new workspace.
  - Q-063 stays **Open — partly addressed**.
- **D-107:** described as "approved in principle, subject to verification" in criteria §0 and §11 steps 1 and 10, and in protocol §1 and §10 row 6; D-108 named as the proposed order.
- **Protocol §7a step 5:** R2 named as the fallback (D-109, design only).
- **Traceability:** criteria §9 and protocol §11 rows.
- **Decision log:** a D-106 history row recording the Q-063 correction. No status cell changed.
- **Package:** `final_pre_freeze_approval_package_2026-11-11.md` rewritten (sections A–H).

**Not done**: no freeze, freeze entry, registry, activation rows, fixed-inventory entry or run authorisations; no Stage 0, sampling or screening; no custodian or D-102 implementation; no raw-export, inventory or records change; no stage, commit, push or merge. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## FINAL-PRE-FREEZE-ISSUE-RESOLUTION — 2026-11-11 — issue-resolution audit (D-107 provenance, D-108 sequence, D-102, open questions, custodian readiness, cross-document consistency, §11 audit); mechanical corrections only (not a freeze)

**Prompt**: researcher prompt "BIO-ML INSIGHT: FINAL PRE-FREEZE ISSUE RESOLUTION AND GOVERNANCE AUDIT" (2026-11-11).

**Added**: `research/reviews/2026-11-11_FINAL-PRE-FREEZE-ISSUE-RESOLUTION.md` (Sections 1–12).

**Corrections** (each target matched exactly once):
- criteria v1.1 §9: two status cells marked as the statuses at the time the row was written, with a pointer to the later statuses; original text kept; new traceability row.
- Approval package §E: D-099 steps (3), (4) moved to "before step 4" (D-099: "required before the first authorised run"); follow-up note added at the top.
- Register Q-097: evidence pointer added; still **Open**.

**Findings**:
- `[EVIDENCE]` The current `source_records.jsonl` equals the T2 pre-build hash (scratch, uncommitted).
- `[EVIDENCE]` The current `publications.jsonl` equals the outputs of four earlier offline builds; no hash was recorded at T2.
- D-107 is assessed as partially verified.
- The Drive backup holds raw-export archives only.

**Proposed, not applied** (P1–P5):
- P1: a D-102 status-cell clarification;
- P2: D-108 additions;
- P3: protocol §10 row 6 (d), which depends on D-108;
- P4: the revised D-102 (R1) text;
- P5: a Q-097 answer.

**Validation**: actual results are in the report §10 (130, 347, 10 and 29 tests OK; query check PASS; raw-export verify OK; whitespace checks exit 0; data hashes unchanged).

**Not done**:
- no freeze, freeze entry, registry, fixed-inventory entry, condition rows or authorisations;
- no Stage 0, sample, sheet or screening;
- no custodian, keys or D-102 implementation;
- no rebuild; no record content read;
- no decision-status change; protocol v0.2 and the decision log not changed;
- no stage, commit, push or merge. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## COMPLETION-BATCH-E — 2026-11-11 — six researcher-approved mechanical corrections; final approval package prepared (not a freeze)

**Prompt**: researcher prompt "We are moving to the completion stage. I do not want another audit cycle." (2026-11-11).

**Applied** (one batch; each target matched exactly once; rollback copies kept outside the repository):
1. Protocol §1: abstracts recoverable by an authorised rebuild from the raw exports.
2. Criteria §4: a full-text `uncertain` is resolved through adjudication (protocol §5 items 3 and 4).
3. Criteria §11: execution-order paragraph.
4. Protocol §7a step 5: the independent-custodian requirement of D-102 (3); a D-096 extension needed under R1 (not decided); nothing implemented.
5. Package §E: D-099 (3)/(4) before step 5 at the latest.
6. Decision log: a D-102 history row; "(2026-11-11)" is the recorded approval date, not a freeze date.

Traceability rows were added to criteria §9 and protocol §11. Package sections H (confirmation sheet) and I (R1, R2, R5, R7, R8 prepared, not applied) were rewritten.

**Unchanged**:
- statuses: D-107 in principle; Q-097 Open; D-108 PROPOSED; D-102 pending; D-084 in principle;
- no rule, code, threshold or RQ changed.

**Not done**: no freeze, entry, registry, condition rows, authorisations, screening, sampling, rebuild or Git operation. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## R-DECISIONS-APPLIED — 2026-11-11 — researcher decisions R1, R2, R5, R7 (a), R8 applied in one batch (not a freeze)

**Prompt**: researcher prompt "We are proceeding toward the documentation freeze." (2026-11-11).

**Applied**:
- **R7 (a):** criteria I-C4 and §3 RQ6, and protocol §3: systematic and scoping reviews informing RQ6 are `review_lead` and may be tagged RQ6.
- **R8:** criteria E2 and E3 carry the E1-style note (excluded only if every other RQ also fails, §4).
- **R2:** `search_strategy.md` §1.2 RQ5 names probability calibration; the earlier wording is kept in the note; a change-history row added.
- **R1 and R5:** recorded as limitations only, in the approval package §I (not in the criteria or protocol).
- **Traceability:** rows added to criteria §9 and protocol §11.
- **Package F5:** proposed freeze-entry ID `D-110`; dates left to the researcher.

**Unchanged**: eligibility rules, codes, thresholds and RQ scope; D-107 in principle, Q-097 Open, D-108 PROPOSED, D-102 pending, D-084 in principle.

**Not done**: no freeze, entry, registry, activation, screening, sampling or Git operation. PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.

## F1-F5-APPROVALS — 2026-11-11 — researcher content approvals recorded (documentation approval only; not a freeze)

**Prompt**: researcher prompt "I confirm the following researcher approvals" (2026-11-11).

**Recorded**:
- package §J (F1–F5 as given);
- a D-084 status-history row (status cell unchanged).

**Left unfilled**: the approval date (researcher text "[ENTER ACTUAL APPROVAL DATE]"; not entered by the assistant); the effective date (set at the freeze).

**Verification**: the approved files are unchanged (SHA-256 `ff5ce20e…675d`, `836e26fd…7c30`).

**Not done**: no freeze, freeze entry, registry, Git operation, screening, sampling, activation or real-data operation.

## F1-F5-APPROVAL-DATE — 2026-11-11 — approval date recorded

**Prompt**: researcher prompt "I confirm that the F1–F5 approval date is 2026-11-11" (2026-11-11).

**Recorded**:
- the approval date 2026-11-11 in package §J;
- a new D-084 status-history row (status cell unchanged; the earlier F1-F5-APPROVALS row kept).

**Not done**: no freeze, registry, Git operation or screening.
