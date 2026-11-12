# Session log — 2026-11-01 — WORKSTREAM-C

**Objective** (researcher prompt 2026-11-01, after review of the DECISION-PREPARATION report). Approved:
1. one local commit of the verified 17-file change set;
2. Workstream C (validator update for D-068 (5) Option A, D-069 and D-070);
3. rejection of repeated `scope_flags` tokens, recorded as an implementation decision;
4. the two D-077 wording fixes in protocol v0.2;
5. evidence-based preparation of the six-record classification;
6. a T2 review report.

**Not approved**: fetch, pull, push, merge, rebase, force-push, branch switch; PR #17 changes; executing T2; pilot draw, freeze or screening; real-data training; unrelated scientific decisions or question-status changes.

**Date**: the verified container clock read 2026-11-01 (08:39 UTC at the start).

## A. Preservation commit [EVIDENCE]
- **Pre-checks:**
  - branch `claude/eloquent-mccarthy-bqtxr3-part1`, HEAD `93dd16dbfa8ed5cd6764070309eb6695787f27d1`; nothing staged; no stashes;
  - 7 modified and 10 untracked files, identical by SHA-256 to the set audited in DECISION-PREPARATION.
- **Checks** (08:39:42–08:40:59 UTC, all exit 0): literature 212 OK; data protection (strict) 10 OK; NHANES 29 OK; query table PASS (168 rows); `sh -n scripts/run_checks.sh` OK; `git diff --check` OK; 470 pre-existing warning lines.
- **Staging:** only the 17 confirmed paths, by name. Staged diff: 17 files, +2,771/−109; no ignored or data path; `git diff --cached --check` OK; deletions only in the four code and test files.
- **Commit:** `ad02333b1ae8df8e58f4f11588d20960ef8fc2ba` (parent `93dd16d`). Not pushed, not fetched.

## B. Workstream C (uncommitted)
### Changes
- **`scripts/literature/pubrecords.py`:**
  - `SCOPE_FLAG_TOKENS` is the D-069 (E) vocabulary: `scope_pending_disorder`, `scope_pending_proteomics`, `non_metabolic_method_exemplar`, `non_metabolic_rq5_candidate`, `lr_only`;
  - `scope_flag_errors` rejects a repeated token (D-078);
  - new `STAGE0_RULE_REASON_CODES` and `is_stage0_rule_row()` (D-068 (5));
  - the D-060 (6) check in `load_screening_decisions` exempts only Stage-0 rule rows, i.e. no include/uncertain row is exempt (Option A);
  - Option B is not implemented;
  - comments updated.
- **`research/literature/schemas/screening_decision.schema.json`:** `scope_flags` pattern (approved vocabulary, no repeated token via a negative lookahead); `scope_flags` description; the header description of the Stage-0 exemption.
- **`research/literature/schemas/paper_inventory.schema.json`:** the build's `scope_flags` pattern (`retracted` plus the approved vocabulary, no repeats) and description.
- **`publication_record.schema.json`:** `scope_flags` has no pattern there, so nothing to change.
- **`make_literature_reports.py`:** it joins the build-derived `retracted` with the screening value, so it needed no change.
- **`tests/literature/test_t1a_schema_validation.py`:**
  - `test_scope_flag_patterns_match_code` rewritten;
  - new `test_repeated_token_message`;
  - `test_stage0_rule_rows_exempt` replaced by `test_stage0_rule_rows_e5_e7_accepted`, `test_stage0_screener_no_longer_exempts_include_or_uncertain`, `test_option_b_not_adopted` and `test_unrelated_exclusions_unaffected`;
  - `test_scope_flags` extended (accepted and rejected values, empty value);
  - new `test_co_occurring_tags_reach_the_inventory_and_pass_its_schema`;
  - module docstring updated.
- **`tests/literature/test_screening_and_ids.py`:** `needs_d060` no longer treats `rule:stage0` include/uncertain rows as exempt.

### Test coverage
| Case | Test |
|---|---|
| Each approved token alone; both co-occurring tokens in both orders; all five together (both orders) | `test_scope_flag_patterns_match_code` (code and both schema patterns); `test_scope_flags` (build) |
| `prognostic` (alone and with a valid token); manual `retracted` | Both tests (rejected; "derived by the build") |
| Misspellings (`scope_pending`, `scope_pending_disorders`, `LR_ONLY`, `lr-only`, `non_metabolic_exemplar`) | Both tests |
| Whitespace and malformed separators (`;;`, leading or trailing `;`, padded tokens, `; `, `,`) | Both tests |
| Repeated tokens (adjacent, separated, after all five) | Both tests; `test_repeated_token_message`; built pattern rejects `retracted;retracted` |
| Empty flags | Accepted; stored as null |
| Stage-0 include and uncertain at title/abstract, descriptors missing, one missing, or complete | `test_stage0_screener_no_longer_exempts_include_or_uncertain` |
| Stage-0 `exclude` E5 and E7 | `test_stage0_rule_rows_e5_e7_accepted` |
| Unrelated valid exclusions (`assistant` E3; hand-entered E5) | `test_unrelated_exclusions_unaffected` |
| Option B not adopted (`rule:stage0` on `exclude` E1 and on full text accepted) | `test_option_b_not_adopted` |
| Schema consistency | Code tokens equal the D-069 (E) list; every token in both schema descriptions; same accept/reject results for code and patterns; full jsonschema validation of an inventory with `retracted` plus co-occurring tags |
| Build failure behaviour | Every rejection goes through `assert_rejected`: the build raises and `publications.jsonl` and `build_report.json` are byte-identical |

### Mutation check (scratch copies, then deleted)
All 10 reintroduced defects were caught by `test_t1a_schema_validation.py`:
- `lr_only` dropped;
- `prognostic` accepted;
- repeats accepted in code;
- manual `retracted` accepted;
- the exemption restored for any `rule:stage0` row;
- rule row ignoring the reason code;
- Option B added;
- repeats allowed in the decision-schema pattern;
- repeats allowed in the inventory pattern;
- `lr_only` missing from the pattern.

### Preservation of metadata, provenance, IDs and deduplication
- **Method:** build and reports run on two scratch copies of `research/literature` outside the repository, one with the HEAD code (`ad02333`) and one with the Workstream C code (08:49–08:54 UTC). This is a regression comparison, **not T2**; the repository inventory was not touched.
- **Result:** 284 of 284 files identical; `build_report.json` differs only in `built_at`.
- No changed line touches metadata, provenance, ID or deduplication code.

## C. Protocol v0.2: D-077 wording (uncommitted)
- **Line 10:** "…D-063, D-068**, D-077**. Traced in §11".
- **Line 83:** "`screening/pilot_sample.csv` (IDs, stratum, seed**, inventory SHA-256 and the sampling script; D-063, D-077**), …".
- No other change. Protocol v0.2 remains **"DRAFT for researcher review. NOT frozen. Not in force."** and still awaits formal review and freeze.

## D. Six in-scope records without an abstract: evidence (classification not made)
**Rule** (D-068 (8)):
- "No abstract" means empty, absent or a source placeholder.
- *Not retrieved*: an abstract may exist but was not obtained (retrieval failed, metadata incomplete, or the transcription omits the field).
- *Unavailable*: the source indicates that no abstract exists.
- A retrieval failure is not proof of unavailability.
- Enforcement is human (D-068 (10)).

| Paper ID | PMID / DOI | Stored PubMed record (raw `META` file) | Source types | Stage 0 under D-074 | Assessment |
|---|---|---|---|---|---|
| P0522 | 37042260 / 10.1161/jaha.122.027736 | Retrieved; abstract field = "[Abstract not available]" (`META_2026-10-23_033.json`) | Letter; Research Support, N.I.H., Extramural | No (Letter) | PubMed explicitly records no abstract; consistent with a letter. Supports *unavailable* if the PubMed placeholder counts as "the source indicates" |
| P0559 | 35639990 / 10.1210/clinem/dgac334 | Placeholder (`META_2026-10-23_024.json`) | Journal Article; Comment | No (D-074 (c)) | Placeholder present, but a comment published as a journal article may carry a publisher abstract. **Ambiguous**: a publisher check (network) would settle it |
| P0624 | 31711877 / 10.1016/j.metabol.2019.154010 | Placeholder (`META_2026-10-23_009.json`) | Editorial | **Yes, E5 (D-074 (b))**; outside the 1,463 pilot frame | Placeholder consistent with an editorial. Its Stage-0 exclusion governs it (D-068 (2)(a), (4)); classification needed only for completeness |
| P0938 | 36645222 / 10.1097/hep.0000000000000209 | Placeholder (`META_2026-10-23_030.json`) | Research Support, Non-U.S. Gov't; Letter; Comment | No (D-074 (c)) | Placeholder; "Letter to the editor" title. Supports *unavailable* on the same basis as P0522 |
| P1154 | 28071176 / 10.1177/0004563216663083 | Placeholder (`META_2026-10-23_006.json`) | Journal Article | No | Placeholder for a journal article. **Ambiguous**: a publisher abstract may exist; publisher check needed |
| P3061 | 40348673 / 10.1016/j.bja.2025.03.029 | Placeholder (`META_2026-10-28_003.json`) | Letter | No | Placeholder; consistent with a letter. Supports *unavailable* on the same basis |

**Facts [EVIDENCE]**:
- All six were retrieved successfully; none is a retrieval failure.
- PubMed's own placeholder "[Abstract not available]" is stored verbatim for each.
- The inventory records `abstract_available = false` for each.
- No other source was consulted (no network).

**For researcher review [OPEN]**:
1. Does the PubMed placeholder count as "the source indicates that no abstract exists" (D-068 (8))? If yes, P0522, P0624, P0938 and P3061 have a clear basis for *unavailable*.
2. For P0559 and P1154 (typed *Journal Article*), would you accept the PubMed-only evidence, or require a publisher check, which needs network access and authorisation?

No classification was recorded.

## E. T2 rebuild: review checklist (NOT executed)
Source: `logs/session_logs/2026-10-31_T1-A.md` ("Remaining for T2"); criteria v1.1 §6 (the `dim_independent_validation` sentence); D-066 (8); D-064 ("takes effect at the next authorised build").
1. **Authorisation:** explicit researcher authorisation for T2, given separately from this session. Start on a clean, committed tree (Workstream C committed).
2. **Before:**
   - record the HEAD hash and the SHA-256 of `paper_inventory.json` and `.csv`, `MANIFEST.csv`, the registry and the records outputs;
   - run all checks;
   - copy the current generated outputs to the scratchpad.
3. **Build** under the Step C safeguards: `pubrecords.build` then `make_literature_reports`, with no network and no new raw files.
4. **Expected changes:**
   - `publication_type` populated for all 3,386 records (currently null in the committed outputs);
   - the two T1-A inventory columns populated (`biomarker_class`, `screening_validation_design`; null while nothing is screened);
   - `unmapped_publication_types` in `build_report.json`.
5. **Then remove `dim_independent_validation`** from:
   - `INV_COLS` (`make_literature_reports.py:47`) and the null default (`:213`);
   - `paper_inventory.schema.json` (line 388);
   - `screening_details` in `publication_record.schema.json` (line 512);
   - also list `publication_type` as required in the publication schema;
   - update `test_t1a_schema_validation.py:82-83` and `test_screening_and_ids.py:260`.
6. **Integrity, before vs after:**
   - same 3,386 paper IDs; registry unchanged;
   - verification statuses unchanged (3,348 / 37 / 1 / 0), or every change listed and explained in `verification_status_changes`;
   - no change to titles, DOIs, PMIDs, `query_ids`, `retrieved_on`, `source_db` or provenance;
   - all diffs explained field by field.
7. **Record** the new inventory SHA-256 values; the pilot draw must record the hash at draw time (D-063, D-077).
8. **Re-check the 1,463-record pilot frame** (D-044 scope of 1,470 minus the 7 D-074 Stage-0 records: P0028, P0099, P0113, P0624, P0830, P0931, P0939). Recomputed today from the committed inventory and the D-074 rules: 1,463.
9. **Checks after:** all suites, query validation, `git diff --check`, the data-protection strict run, and logs.
10. **Unchanged by T2:** T2 does not activate screening, freeze anything, or draw the pilot.

## Remaining activation blockers (D-035 record §6)
- **Condition 5** (criteria v1.1 and protocol v0.2 frozen): **unmet**. Both are still drafts.
- **Condition 6:**
  - the validator items and their tests are **implemented but uncommitted**, pending your review;
  - **T2 is not authorised or executed**;
  - the **six-record classification is open** (see D).
- Conditions 5 and 6 are **not** recorded as met.

## Governance records
- **`DECISION_LOG.md`** (insertions only; 0 lines removed or changed):
  - three status-history rows (D-078 new; D-068 and D-069/D-070 "no status change, implemented");
  - a new section with D-078.
- **`unresolved_questions.md`:** unchanged.
- **Other:** no other decision changed.

## Checks after the changes
See the CHANGELOG entry for the final run (commands, counts, warnings).

## Git state
- HEAD `ad02333` (local commit of the 17-file set); not pushed, not fetched.
- The Workstream C, D-077, D-078 and logging changes are **uncommitted**.
- PR #17 (https://github.com/Arava-Sukeerthan/BioML-Insight-An-Explainable-Machine-Learning-Framework-for-Biochemical-Biomarker/pull/17) not changed.
