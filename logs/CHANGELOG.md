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
