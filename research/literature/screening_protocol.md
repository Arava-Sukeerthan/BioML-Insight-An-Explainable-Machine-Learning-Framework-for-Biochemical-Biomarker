# Title/Abstract Screening Protocol (pilot and main screening)

| Field | Value |
|---|---|
| Task | LIT-004-PREPARATION (2026-10-23) |
| Version | 0.1 — **DRAFT, PROPOSED, not approved** (D-025, D-026). §1 and §8 status updated in LIT-004-WORKFLOW-FIXES (B-1, B-3, B-4 implemented, pending approval as D-027); no rule changed |
| Relationship to existing documents | Operational protocol for `screening_criteria.md` v1.0 (LIT-001, draft) and `search_strategy.md` §6. It **does not replace** them. Where it proposes changes, they are listed in §9 as *proposed amendments*. `screening_criteria.md` was **not** edited |
| Status of screening | **Not started.** No record has been screened, labelled or selected |
| Scope of claims | The protocol does not assume that the BioML-Insight framework is new or better. Screening exists to describe the existing evidence; whether a defensible research gap exists is decided later (Stage D) from verified, screened evidence |

---

## 1. Input set and fields

**Records:** 2,979 publications (`paper_inventory.csv`, `records/publications.jsonl`), built in LIT-003.
`fulltext_review_candidates.csv` (234) is a mechanical work-ordering list. It is **not** a screened
or validated shortlist and has no role in eligibility decisions.

| Field needed for title/abstract screening | Where it is | Note |
|---|---|---|
| `paper_id` | inventory, index, jsonl | Stable for all 2,979 records since LIT-004-WORKFLOW-FIXES (B-1 fixed by a fallback registry key; P2980–P2988 kept their IDs, `records/id_migration_LIT-004.csv`) |
| title | inventory | |
| abstract | `records/publications.jsonl` only (git-ignored, container) | Not in any committed file (D-010). Can be rebuilt from the preserved archive (`preservation/preservation_status.md`). 119 records have no abstract: all 113 arXiv/web records, plus 6 PubMed records whose abstract field is empty or the "[Abstract not available]" placeholder |
| publication types | inventory `source_publication_types` | Drives Stage 0 (§3) |
| language | jsonl (`language`) | 2,857 `eng`; 7 `chi`, 2 `ger`; 113 missing (arXiv/web) |
| year, venue, DOI/PMID/PMCID/arXiv ID | inventory | |
| query IDs and retrieval themes | inventory | **Context only**: retrieval by a theme's query is not evidence that the paper addresses that theme |
| duplicate status, possible duplicates | inventory / `records/dedup_review.csv` | §4 |
| retracted flag | inventory `scope_flags`, index `retracted` | §3 |
| MeSH terms, keywords | raw originals only (`source_records.jsonl`, git-ignored) | Optional aid; not required |

## 2. Screening labels

**Decision (one per record and stage)**, matching the `publication_record` schema enum:

| Label | Use |
|---|---|
| `include` | Clearly meets the criteria of ≥ 1 RQ strand (`screening_criteria.md` §3) |
| `exclude` | Clearly fails all strands; **one** primary reason code (§5) and a one-line justification |
| `uncertain` | Title/abstract do not allow a decision; goes to full text or adjudication. **Never** dropped silently |
| `abstract_only` | Full-text stage only (`screening_criteria.md` §4) |

**Descriptors recorded for every `include` or `uncertain`.** These are separate fields and are not decisions:

| Descriptor | Values | Meaning |
|---|---|---|
| `rq_tags` | RQ1…RQ6 | Strands the record could inform |
| `dim_explainability` | `yes` / `no` / `unclear` | Title/abstract **states** that an explanation/attribution method is used or studied |
| `dim_uncertainty` | `yes` / `no` / `unclear` | States that predictive uncertainty is estimated (e.g., conformal sets, ensembles, Bayesian, selective prediction) |
| `dim_calibration` | `yes` / `no` / `unclear` | States that probability calibration is assessed or corrected (e.g., calibration plot/slope, Brier score, recalibration) |
| `dim_independent_validation` | `external` / `temporal` / `internal_only` / `unclear` | Validation design as stated |
| `record_type` | `original` / `methodological` / `software` / `guideline` / `review_lead` / `preprint` / `notice` | |
| `scope_flags` | e.g. `scope_pending`, `lr_only`, `prognostic`, `non_metabolic_method_exemplar` | From `screening_criteria.md` |

The three dimensions are recorded **independently**. A record that reports calibration but no
uncertainty estimate is `dim_calibration=yes`, `dim_uncertainty=no`. "Interpretable" in a title
without a stated method is `dim_explainability=unclear`, not `yes`. These descriptors say what the
abstract *claims*, not how well it was done; quality is appraised at full text
(`search_strategy.md` §8.2).

### 2a. RQ5 component evidence (approved with conditions, **INACTIVE**; D-031–D-036)
Not applied until the activation conditions in `research/reviews/Q-041_decision_record_D035.md` §6 are met. For RQ5 component statuses, this subsection replaces the "states/claims" meaning above. The descriptors' other uses stay as written (D-026 and D-029, proposed).
- **Five components:** feature selection (`dim_feature_selection`), classification (`dim_classification`, D-036; whether `lr_only` studies can be `yes` is open, Q-042), explainability (`dim_explainability`), probability calibration (`dim_calibration`), uncertainty estimation (`dim_uncertainty`).
- **`yes`** = a qualifying procedure applied to the study's data or model, with a documented output (definitions: D-032; D-035 §2). **`no`** = the absence is stated or the fully described design excludes it. **`unclear`** = assessed but unresolved. **Empty** = not assessed, never `no`.
- **Preliminary vs confirmed:** title/abstract statuses are preliminary (triage only). Statuses are **confirmed** only on a `full_text` row, never on an `abstract_only` decision. A full-text RQ5 assessment records all five statuses.
- **Researcher verification** of `qualified`/`near_rq5` records: a new `full_text` row with `screener=researcher` restating all statuses, justification "verified: …". Earlier rows are kept (D-035 §4).
- **Build safeguards (implemented):** a later row of the same stage cannot blank a recorded component; incomplete full-text component rows are rejected; both checks cover all five component columns (D-036).
- **Coverage group (derived, D-034/D-036):** the build sets `rq5_coverage_group` (`qualified` ≥ 4 `yes`, `near_rq5` = 3, `below_threshold` 0–2) and `rq5_coverage_provisional` (any `unclear`) from **confirmed** statuses only; null when not assessed. Screeners never assign it. It describes component coverage, not study quality.
- **Precedence:** for RQ5 component statuses, D-035 applies where it differs from §2 above (D-026) or R5 (D-029); both stay PROPOSED.

## 3. Decision rules for the distinctions requested

| Distinction | Rule (applies at title/abstract; doubt → `uncertain`) | Existing basis |
|---|---|---|
| Metabolic-disorder classification vs broader biomedical prediction | RQ1 requires a target within `screening_criteria.md` §2.1 (classification, screening, diagnosis, subtyping or risk probability). A model for cancer, psychiatric, cardiovascular-event, infectious or imaging diagnosis is `exclude E4` for RQ1. It may be **retained only** for RQ2/RQ3/RQ4/RQ5 as a methodological exemplar if it develops or evaluates explainability, uncertainty, calibration, validation/shift or integrated-framework methods applicable to tabular/omics/clinical-laboratory data (`scope_flags=non_metabolic_method_exemplar`). Complications as targets (e.g., retinopathy) → E4 | §2.1, §3 |
| Biochemical biomarkers vs imaging-only / genetics-only | RQ1/RQ2b/RQ4a require biochemical inputs (§2.2: metabolomics/lipidomics, newborn-screening MS/MS, routine clinical chemistry, or mixed sets where biochemical markers are substantive). Imaging-only, genomics/transcriptomics/methylation-only, microbiome-only, wearable/CGM-only or questionnaire-only → `exclude E3` for those strands. Multi-omics with metabolomics as one substantive layer → eligible (`uncertain` if the abstract does not make clear whether metabolites enter the model) | §2.2 |
| Original research vs reviews, corrections, retractions, duplicates | Reviews: `include` only as `record_type=review_lead` (RQ6 / citation chasing), never as primary evidence. Errata/corrections (PubMed type *Published Erratum*): Stage 0 → `exclude E5` (notice, not a study), linked to the corrected article. Retractions: Stage 0 → `exclude E7`. Duplicates/versions: §4 → `exclude E8` only after a recorded dedup decision. Editorials, comments, protocols without results, patents, dataset descriptors without a model → E5 (or E2) | §1 (I-C4, E5, E7, E8) |
| Explainability, uncertainty and calibration as separate dimensions | Recorded as three independent descriptors (§2). For RQ3 eligibility either uncertainty or calibration suffices (unchanged). For RQ5 counting see proposed amendment A-3 (§9) | §3 RQ2/RQ3/RQ5 |

**Stage 0 (automatic, rule-based, counted):** PubMed types *Editorial*, *Comment*, *News*,
*Published Erratum* → E5; *Retracted Publication* → E7. This is the existing
rule (`search_strategy.md` §6.1). Letters are not auto-excluded. Each Stage-0 exclusion is written with
`screener=rule:stage0`, so it is visible and reversible. All Stage-0 decisions are listed in the pilot
report for the researcher to see (§7).

Current inventory (counts from `source_publication_types`; not yet applied): 3 *Retracted Publication*
(P0931, P0939, P1443), 2 *Published Erratum* (P0028, P0113), 6 *Editorial*, 4 *Comment*, 8 *Letter* (not auto-excluded).

## 4. Possible duplicates and related versions (15 pairs, 30 records)

Expected handling in the existing workflow (`collection_workflow.md` §1, §4.2): a person records
`same` or `different` in `records/dedup_decisions.csv`; `same` merges on the next build;
`different` suppresses the flag. **No decision has been made, and none is made here.**

Observed categories (descriptive only; from metadata, not from reading the papers):

| Category | Pairs | Observation | Workflow limitation |
|---|---|---|---|
| Preprint vs journal version (both PubMed) | P0010/P1368, P1213/P1320, P1360/P1442, P1466/P1479, P2128/P2148, P2488/P2535, P2562/P2565, P2140/P2149 | One record has PubMed type *Preprint*; titles identical or near-identical | Three pairs have different PMIDs/DOIs (`identifier_conflict`), and the code **never merges** those, even after `same`. The workflow has no "version-of" link, although `search_strategy.md` §5.3 asks for preprints to be linked to the published version, with the published one primary (blocker B-2) |
| Possible version, titles differ | P1421/P1488 ("Lipid Ratios…" vs "Lipidomics…", 2025 vs 2023 preprint) | Same-work status unclear from the title | Needs a human decision (`uncertain`) |
| Web result vs PubMed record | P0098/P2988, P1343/P2987, P0450/P2978 | Web record has title/URL only; P2978 URL is a medRxiv DOI while P0450 is the eLife article | As above; P2978 is a preprint version |
| Web vs arXiv/web version | P2870/P2982 | arXiv record vs ScienceDirect page title | As above |
| Erratum vs article | P0113/P0153 | P0113 is a *Published Erratum* whose abstract cites the DOI of P0153 | Stage 0 excludes P0113 (E5); pair still needs `different` + link note |
| Two web results with same title | P2980/P2981 | Two USPTO documents with different numbers in the URL | Probably different documents; both would be E5 (patent) at screening |

**Proposed procedure (A-4, pending):** before Stage 1, the researcher (or the assistant with a
researcher audit, Q-024) records for each pair `same`, `different`, or `version` (new, proposed),
with a note `version_of:Pxxxx`. Only the primary version is screened. The other gets
`exclude E8` with the note. Until the decisions exist, **both** records are screened normally,
and the pair is listed in the pilot report.

## 5. Exclusion reason codes

The existing E1–E12 (`screening_criteria.md` §1) are used unchanged, so they still match the schema pattern
`^E(1[0-2]|[1-9])$`. The first applicable code in numerical order is the primary reason.
Clarifications proposed (A-2):

| Code | Clarification |
|---|---|
| E3 | Also for "imaging-only"/"genetics-only" inputs in RQ1/RQ2b/RQ4a (as §2.2) |
| E4 | Non-metabolic targets, unless retained as `non_metabolic_method_exemplar` for RQ2–RQ5 |
| E5 | Explicitly includes errata/correction notices, patents and dataset-only descriptors |
| E6 | Applied only when the record itself is non-English (`language` ≠ `eng` **and** no English full text). 9 records (`chi`/`ger`) are candidates; 113 arXiv/web records with missing language are **not** E6 by default |
| E8 | Only after a recorded dedup/version decision (§4) |
| E12 | Catch-all; justification mandatory; audited at 100 % in the pilot |

## 6. Ambiguity handling and manual review

1. **When in doubt, `uncertain`** (`screening_criteria.md` §4). Exclusion needs a positive reason found in the title/abstract.
2. Each decision records `screener`, `date`, `justification` (≤ 1 sentence, quoting the decisive phrase where possible), `criteria_version`.
3. **Adjudication queue** (`screening/adjudication_queue.csv`, proposed): every `uncertain`, every E12, every record where the screener marks `needs_human=yes`, and all §4 pairs. The researcher decides. The decision is stored with `screener=researcher`, and the original decision is kept (append-only).
4. Criteria problems found during screening go to `research/reviews/unresolved_questions.md`. An accepted change is logged in `logs/DECISION_LOG.md` (new criteria version), and every record decided under the old wording with the affected code is re-screened.
5. Records with no abstract (119): `uncertain`, unless the title alone gives a clear Stage-0-type or E1/E4 reason. arXiv/web records are queued for metadata completion (authors/venue) before inclusion.

## 7. Pilot sample and consistency check (proposed, D-025)

| Item | Proposal |
|---|---|
| Size | **60 records** (about 2 % of 2,979). Researcher time about 60–75 min at 1–1.5 min per record |
| Sampling | Stratified random, seed **4004** (to be recorded in the pilot file). Strata by primary retrieval theme of the inventory: A, B, C, D, E, F, Q, plus `arxiv/web`. Allocation: 8 each for A–E and Q (48), 6 for F, 6 for arXiv/web. A record retrieved by several themes is assigned to its rarest theme, in the order F, D, C, E, A, Q, B, so that small themes are represented. Stratum sizes under this rule (current inventory): B 626, C 625, E 503, D 447, A 369, Q 176, F 120, arXiv/web 113. Records without abstracts are allowed (they test rule 6.5). Exclude Stage-0 records from the sample (they are rule-based) |
| Blinding | Assistant and researcher screen the same 60 **independently**. The researcher's sheet (`screening/pilot_sheet_researcher.csv`) has title, abstract, year, venue, types and no assistant decision |
| Agreement metrics | Percentage agreement and Cohen's κ on the 3-level decision (include/uncertain/exclude), plus κ on include-vs-not; agreement on the primary exclusion code; agreement per dimension descriptor (X/U/C) |
| Pass criteria | κ (3-level) ≥ 0.60 **and** no record excluded by one screener that the other judged `include` without adjudicated agreement on the exclusion **and** no systematic disagreement on any single code (≥ 3 disagreements on one code) |
| If not passed | Disagreements reviewed together; criteria clarified (logged as a new criteria version); a **second pilot of 40 new records** (same strata, next seed) before any expansion |
| Expansion | Only after pass and researcher approval: screening of the remaining records in batches of about 300, with the existing post-hoc audit (`search_strategy.md` §6.4: 25 included + 25 excluded, blinded) after the first two batches |
| Outputs | `screening/pilot_sample.csv` (IDs, stratum, seed), `pilot_decisions_assistant.csv`, `pilot_decisions_researcher.csv`, `pilot_report.md` (metrics computed by a script, not by hand) |

This replaces the pilot in `screening_criteria.md` §7 ("first 30 records in PMID order of Q-PM-01 and Q-PM-09")
**only if approved**. That pilot is kept as the documented alternative (A-1). The reason for the proposal:
PMID order selects the oldest records, and two queries cover neither themes C/D/F nor arXiv/web.

## 8. Blockers and conflicts found (must be resolved before screening)

| ID | Finding | Evidence | Proposed resolution | Status (LIT-004-WORKFLOW-FIXES) |
|---|---|---|---|---|
| B-1 | **Unstable paper IDs** for 9 web-only records with no DOI/PMID/PMCID/arXiv ID and no year (P2980–P2988 in the current build; IDs change on every rebuild, e.g. P2977→P2988) | `record_keys()` in `pubrecords.py` needs title **and** year; these 9 have no registry key | Add a registry key from the source URL (or title alone when the year is missing). Small code change + test, then rebuild; record ID mapping. | **Implemented** with a different key: `source_record:<source_record_id>` (see D-027 for why, and the URL key as an alternative). The 9 IDs were kept (mapping before = after); approval pending (D-027) |
| B-2 | Workflow cannot record a **version** link and cannot merge identifier-conflict pairs | §4 | Add `version` decision and `version_of` note handling (A-4) | Open — representation proposed as D-030 (`version_linking_proposal.md`, LIT-004-REVIEW-AND-DECISIONS); not implemented, no pair resolved |
| B-3 | **Two screening file formats** in project documents: `collection_workflow.md`/`pubrecords.py` read `screening/decisions.csv` (`paper_id,stage,decision,reason_code,screener,date,justification`), while `screening_criteria.md` §6 and `search_strategy.md` §6.2 name `title_abstract_decisions.csv` with `record_id, decision, reason_code, rq_tags, tier, scope_flags, justification, screener, date` | file contents | Use `screening/decisions.csv` (the implemented one), with the extra columns of §2 appended (the reader ignores unknown columns); amend the two documents' wording (A-5) | **Implemented**, with one difference: the reader now **rejects** unknown columns instead of ignoring them, so a typo cannot drop a field silently. Schema `schemas/screening_decision.schema.json`; implementation notes added to the two documents, their text unchanged. Approval pending (D-027) |
| B-4 | Inventory enum `screening_status` (`not_screened, included, excluded_title_abstract, excluded_full_text`) has no `uncertain`/`abstract_only`, while the publication-record schema has them; `make_literature_reports.py` always writes `not_screened` | schemas, script line 133 | Map decisions from `publications.jsonl` into the inventory and extend the enum (D-024 revision) | **Implemented**: inventory enum now `not_screened/include/exclude/uncertain/abstract_only` (the old values were never used by any record); stage, reason, descriptors and screener carried into the inventory; manual extraction values carried forward on rebuild. Approval pending (D-027) |
| B-5 | Abstracts exist only in the container copy of `publications.jsonl` | D-010 | Screening must run where the build outputs exist, or after rebuilding from the preserved archive (requires uploading it back) | Open |
| B-6 | Scope decisions still open: Q-001 (disorders), Q-002 (biomarker class), D-009/Q-007 (Q-PM-02 strand), D-008/Q-008 (audit), Q-022 (strategy approval) | unresolved_questions.md | Researcher decisions before the pilot (or pilot run explicitly under the provisional scope) | Open |

## 9. Proposed amendments to `screening_criteria.md` (not applied)

| ID | Amendment |
|---|---|
| A-1 | Pilot design per §7 (alternative: the existing §7 design) |
| A-2 | Code clarifications per §5 |
| A-3 | Record explainability, uncertainty and calibration as separate descriptors (§2). For RQ5, count **uncertainty** and **calibration** as separate components (so 5 components; ≥ 3 required), *or* keep the current rule ("calibration or uncertainty" = one of 4). Researcher choice; this affects which papers count as closest prior art (Q-028) |
| A-4 | `version` decision for preprint/published pairs (§4) |
| A-5 | Unify the screening record file name and columns (B-3) |
| A-6 | Records without an abstract → `uncertain` unless a title-level E-code applies (§6.5) |
