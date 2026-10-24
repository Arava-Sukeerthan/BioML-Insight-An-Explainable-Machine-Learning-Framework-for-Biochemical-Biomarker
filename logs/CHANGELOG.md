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
