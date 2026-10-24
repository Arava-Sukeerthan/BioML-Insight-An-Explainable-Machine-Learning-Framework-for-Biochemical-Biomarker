# Owner Review Ballot — outstanding LIT-004 decisions

| Field | Value |
|---|---|
| Task | LIT-004-OWNER-BALLOT (2026-10-24) |
| Status | **Ballot for the owner. Every item below is unapproved.** Recommendations are the assistant's (and, where stated, the owner's earlier *recommended choices*). They are not approvals (CLAUDE.md rule 7) |
| Governance | A decision is approved only by an owner response on this ballot that is then recorded in `logs/DECISION_LOG.md` (the decision log is in `logs/`, not `research/literature/`). No status, schema, code, criteria, strategy or screening data was changed in preparing this ballot |
| Sources | `decision_reconciliation_LIT-004.md` (§ numbers below refer to it), `approval_request_LIT-004.md`, `screening_protocol.md` v0.1, `version_linking_proposal.md`, `scope_decision_brief.md`, `unresolved_questions.md`, `logs/DECISION_LOG.md`, `records/dedup_review.csv`, `records/build_report.json`, `raw_exports/MANIFEST.csv`, `search_queries.csv`, `records/publications.jsonl` and `source_records.jsonl` (read-only) |
| Supersedes | Nothing. Earlier documents stay as the record of how the proposals developed. Where this ballot words a proposal differently, the ballot wording is the one put to the owner |

## How to answer

Each item has a response line. Mark exactly one option and add comments if needed, e.g. `Owner response: [x] APPROVE`.
- **APPROVE**: the recommended option, as worded.
- **MODIFY**: say what to change in the comments.
- **REJECT**: no change; the item stays as it is now, and where an alternative is named, say whether you want it instead.
- **DEFER**: decide later, with any reason in the comments.

Items can be answered one at a time. Section 1 shows which items block the pilot.

---

## 1. Summary of items

| # | ID | Topic | Blocks the pilot? | Evidence or manual review still needed |
|---|---|---|---|---|
| 1 | D-027 | Screening file and fallback ID keys | Yes | No |
| 2 | D-028 (a–d) | Publication-type fields | Yes (Stage 0 uses it) | No (mapping checked, §2 below) |
| 3 | D-029 (+ D-026) | Screening descriptors | Yes | Pilot measures agreement |
| 4 | D-030 | Version links and PRISMA counting | No, unless pairs are decided before the pilot | Pair decisions need the papers |
| 5 | Q-024 (+ Q-029) | Who decides the 15 pairs | No (as above) | Yes: manual review of the papers |
| 6 | Q-001 | Disorder scope | Yes | Your review of the exact list |
| 7 | Q-002 / Q-035 | Biomarker strands, `biomarker_class` | Yes | No |
| 8 | Q-033 | Proteomics | Yes | No |
| 9 | Q-007 / D-009 | Q-PM-02, 743 records | Yes | No (MeSH check only for the limitations text) |
| 10 | Q-022 (D-005, D-006, D-007) | Executed search | Yes | No |
| 11 | D-012 / D-023 / Q-036 | Transcription controls; arXiv/web spot-check | Yes (via Q-022) | Yes, if the spot-check is chosen |
| 12 | D-010 / Q-011 | Storage of raw exports | No | No |
| 13 | D-008 / Q-008 | Researcher audit | Yes | Your time |
| 14 | D-025 / Q-026 | Pilot design | Yes | No |
| 15 | A-1 … A-6 | Screening-criteria amendments | Yes | No |
| 16 | A-3 / Q-028 | RQ5 component counting | Yes, for theme F records | No |
| 17 | D-024 | Inventory schema (LIT-003) | No, but D-028/D-029 revise it | No |

---

## Item 1 — D-027: canonical screening file and fallback keys

- **Issue.** Screening decisions need one file format, and every record needs an ID that never changes. Nine web records (P2980–P2988) had no stable ID until LIT-004-WORKFLOW-FIXES.
- **Options.**
  - (a) Approve: file `screening/decisions.csv`; key `source_record:<source_record_id>` for records without an identifier and without a year.
  - (b) Use a normalised-URL key instead.
  - (c) Keep the draft wording in `screening_criteria.md` §6 (two files, `record_id`).
- **Recommended:** (a), limited to the file, the key scheme and the **required** columns (`paper_id, stage, decision, reason_code, screener, date, justification`). The optional descriptor columns follow Items 2, 3 and 7.
- **Justification.** A source-record key is unique by construction. A URL key can be shared by two unmerged records, and one of them would then change ID. Already implemented and tested: two rebuilds were byte-identical, and the 9 IDs were kept (`records/id_migration_LIT-004.csv`, before = after).
- **Consequences.**
  - Schema: none further.
  - Screening: the format is fixed.
  - Manuscript: methods describe validated decision records and stable IDs.
  - Workflow: `screening_criteria.md` §6 and `search_strategy.md` §6.2 are amended to match, in a later task.
  - Trade-off: if a later web re-run returns the same item, it gets a new ID and is flagged as a possible duplicate, not merged.
- **Depends on:** Items 2, 3 and 7 for the optional columns.
- **Evidence/manual review:** none.

Owner response: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

---

## Item 2 — D-028: three fields for the type of a record

- **Issue.** "What kind of paper is this?" is currently held in fields that overlap:
  - `source_publication_types`: what PubMed says;
  - `publication_type`: an unused judgement list;
  - `record_type`: the screener's call.

  Your stated preference is to keep source metadata and our screening classification separate.

### 2a. Roles of the fields
| Field | Role | Filled by |
|---|---|---|
| `source_publication_types` | Types **exactly as the source gives them**. Never edited or dropped. Each source's own list stays in `source_records.jsonl` | Build (copied) |
| `publication_type` | **Normalised bibliographic type, derived only from source metadata** by the versioned table below. Not a judgement of content. Removed from the hand-edited fields | Build (mapping) |
| `record_type` | **Screening classification** of the paper's role in the review | Screener |

**Mapping (first match wins).** The final column was checked against `source_records.jsonl` and `publications.jsonl` on 2026-10-24.

| Order | `publication_type` | Source types (PubMed) | Publications in current data |
|---|---|---|---|
| 1 | `retraction_notice` | *Retraction of Publication* | 0 (type not present) |
| 2 | `expression_of_concern` | *Expression of Concern* | 0 (not present) |
| 3 | `erratum_or_correction` | *Published Erratum*, *Correction* | 2 |
| 4 | `study_protocol` | *Clinical Trial Protocol* | 3 |
| 5 | `dataset` | *Dataset* | 2 |
| 6 | `preprint` | *Preprint* | 39 |
| 7 | `review` | *Review*, *Systematic Review*, *Scoping Review*, *Meta-Analysis*, *Evidence Synthesis* | 434 |
| 8 | `guideline_or_consensus` | *Guideline*, *Practice Guideline*, *Consensus Statement* | 1 |
| 9 | `editorial_comment_letter` | *Editorial*, *Comment*, *Letter*, *News* | 15 |
| 10 | `conference_paper` | *Conference Proceedings*, *Congress* | 2 |
| 11 | `journal_article` | *Journal Article* (nothing above matched) | 2,368 |
| — | `unknown` | No source type (all arXiv and web records) | 113, or 37 if 2b is approved |
| — | `other` | Only unrecognised types | 0 |

- **Retracted article ≠ retraction notice.** *Retracted Publication* marks an article that **was retracted**. It sets the existing `retracted` flag (Stage 0, E7). It does **not** change `publication_type`; the 3 current cases stay `journal_article`. A *Retraction of Publication* record is the **notice** (row 1). The same applies to corrections: the notice is row 3, and the corrected article keeps its own type.
- **Types kept but not used for the class:** *Research Support…* (5 variants), *Validation Study*, *Multicenter Study*, *Comparative Study*, *Observational Study*, *Randomized Controlled Trial*, *Clinical Trial* (and Phases I–III), *Evaluation Study*, *English Abstract*, *Historical Article*, *Video-Audio Media*, *Retracted Publication* (as a flag only).
- **Coverage check `[EVIDENCE]`:**
  - 34 distinct source types are present (all PubMed; arXiv and web records carry none). Every one is covered by the table or by the kept-but-unused list, so 0 are unmapped.
  - Seven table entries match no current record (*Retraction of Publication*, *Correction*, *Expression of Concern*, *News*, *Congress*, *Guideline*, *Practice Guideline*). They are kept so future data are handled.
- **Unrecognised types** → `other`, listed in the build report as `unmapped_publication_types`; the build does not fail. The table is extended only by a logged change.
- **Missing types** → `unknown`. Never inferred from a title.

### 2b. arXiv source rule (separate choice)
- **Issue.** arXiv records carry no type, but the source itself is a preprint server. Rule: "source database = arXiv → `preprint`".
- **Recommendation:** approve. This is source metadata (which index returned the record), not a URL or DOI pattern.
- **If rejected:** the 76 arXiv records are `unknown`.

### 2c. URL or DOI-prefix rules (separate choice)
- **Issue.** Rules such as USPTO URL → `patent`, or DOI prefix `10.1101` → `preprint`, would interpret URLs and DOIs.
- **Recommendation: reject** (not used unless you approve a named rule). A heuristic is not source-provided type metadata. Affected records stay `unknown`.

### 2d. `record_type` values
- **Issue.** The protocol's `record_type` list includes `preprint` and `notice`, which are bibliographic facts that `publication_type` now holds.
- **Recommendation:** `record_type` = `original`, `methodological`, `software`, `guideline`, `review_lead`, `other`. Remove `preprint` and `notice`. For example, a preprint of original research is `record_type=original`, `publication_type=preprint`.

**Consequences.**
- Schema: the `publication_type` enum is replaced. No record has a value today, so nothing is lost. The `record_type` enum shrinks.
- Code: the mapping table, `unmapped_publication_types`, and tests.
- Screening: Stage 0 reads `publication_type` and the `retracted` flag.
- PRISMA/manuscript: counts by type are reproducible from the table.

**Depends on:** D-024 (schema), D-025 (protocol §2 list), Item 4 (notices in version links).
**Evidence/manual review:** none.

Owner response 2a (roles and mapping): [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner response 2b (arXiv source rule): [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner response 2c (no URL/DOI rules): [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner response 2d (record_type list): [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

---

## Item 3 — D-029 (revises D-026): screening descriptors

- **Issue.** For every `include` or `uncertain` record, the screener records what the title/abstract says about three methods, and the validation design separately. D-026 (proposed) used a different validation scale and had ambiguous examples (reconciliation §3, C-1 to C-6).
- **Proposed fields (required for `include` and `uncertain`, optional otherwise):**

| Field | Values |
|---|---|
| `dim_explainability` | `yes` / `no` / `unclear` |
| `dim_uncertainty` | `yes` / `no` / `unclear` |
| `dim_calibration` | `yes` / `no` / `unclear` |
| `validation_design` | `external` / `temporal` / `internal_only` / `none` / `not_applicable` / `unclear` |

`validation_design` replaces `dim_independent_validation`. No screening rows exist, so nothing is lost.

**Meaning of the values**
| Value | Rule |
|---|---|
| `yes` | The title or abstract **names** the method or result. Explainability: a named method (SHAP, LIME, permutation importance, attention analysis, or model coefficients presented as an explanation). Uncertainty: conformal sets or intervals, Bayesian predictive uncertainty, ensembles **used to estimate** uncertainty, selective prediction/abstention. Calibration: calibration plot, slope or intercept, ECE, Hosmer–Lemeshow, or recalibration (Platt, isotonic, temperature scaling) |
| `no` | The abstract **states** the element is absent, **or** fully describes the analysis and the element is clearly outside it. Example: "calibration" in the analytical-chemistry sense only (instrument calibration curves) → `dim_calibration=no`, with a justification |
| `unclear` | Not mentioned; vague wording ("interpretable", "explainable", "robust", "reliable"); Brier score alone; built-in feature importance without a named method; conflicting statements; **no abstract** |

**Why silence is not `no`.** Abstracts have word limits and report what the authors chose to highlight. A study may assess calibration and leave it out of the abstract. Reading silence as `no` would count missing reporting as missing methods. The resulting prevalence estimates would be biased toward absence, and the gap assessment (Stage D) would be built on that bias. Title/abstract descriptors therefore measure *what abstracts report*. Claims about how often a method is used need full-text extraction.

**`validation_design`**: the strongest design stated.
| Value | Meaning |
|---|---|
| `external` | A different cohort, site or dataset |
| `temporal` | Same source, later period |
| `internal_only` | Cross-validation, bootstrap, or a random hold-out from the same cohort |
| `none` | Apparent performance only |
| `not_applicable` | No predictive model is evaluated (reviews, purely theoretical methods) |
| `unclear` | Not stated, or "independent test set" without saying where it came from |

**Missing abstracts (119 records).** All three method descriptors `unclear`, `validation_design=unclear`. The decision is `uncertain` unless a title-level Stage-0, E1 or E4 reason applies (A-6). Descriptors are completed at full text.

**Human review (`needs_human=yes`) required when:**
1. a term could have two meanings and the abstract does not settle it (analytical vs probability calibration; "ensemble"; "interpretable");
2. a record that is otherwise `include` for RQ4 has `validation_design=unclear`;
3. the descriptors decide RQ5 status (≥ 3 components; Item 16). These feed the closest-prior-art table, so every such record is checked;
4. a record without an abstract is retained as `uncertain`;
5. the two screeners disagree on any descriptor during the pilot.

**Options.**
- (a) As above (your restated preference).
- (b) Keep D-026's validation scale `external / temporal / internal_only / unclear` as `dim_independent_validation`.
- (c) Four yes/no/unclear descriptors plus `validation_design`. Not recommended: the yes/no would duplicate the design and could contradict it.

**Recommended:** (a). These definitions are **not final** until you approve them, and the pilot may show they need clarifying (logged as a new criteria version).

**Consequences.**
- Schema: column renamed; enums.
- Code: enforcement in `load_screening_decisions`, plus tests.
- Screening: four more required fields per include/uncertain.
- Manuscript: descriptors reported as "stated in the abstract".

**Depends on:** D-026 (revised by this item), Item 16 (RQ5 counting), Item 1.
**Evidence/manual review:** pilot agreement per descriptor (Item 14).

Owner response: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

---

## Item 4 — D-030: reversible relationship links (alternative to A-4)

- **Issue.** Some of the 15 flagged pairs are probably two versions of one work, a web copy of an indexed article, or a correction notice and its article. The current tools can only merge (`same`, which hides one record and is ignored for identifier-conflict pairs) or separate (`different`). `search_strategy.md` §5.3 requires preprints to be linked to the published version, with the published one primary.
- **Proposal (wording conflicts V-1 to V-9 resolved):**

**4.1 Representation.** Rows are appended to the existing `records/dedup_decisions.csv`, which gains the columns `link_id` (L0001, …), `primary_paper_id` and `evidence`. Nothing is ever merged: each record keeps its paper ID, metadata and provenance, and the registry is untouched.

| Relation | Use | Primary |
|---|---|---|
| `version_of` | Preprint and peer-reviewed version of the same work; the same study published twice | The peer-reviewed version (V-1 rule below) |
| `duplicate_of` | The **same publication** retrieved again (a web page of an indexed article) | The indexed record |
| `correction_of` | Erratum/correction notice → article | The article |
| `retraction_of` | Retraction notice → article (new; V-7) | The article |
| `different` | Genuinely distinct records despite similar titles or URLs | — |
| `withdrawn` | Cancels one earlier link, named by its `link_id` | — |

**4.2 Rules**
- **Primary selection (V-1, V-2).** Primary = the peer-reviewed version. If that record is unverified (e.g., a web page without year or authors), its metadata must be verified before it is screened or cited. Until then the group is screened from its best-verified member, with `needs_human=yes`. Two peer-reviewed versions with the same data and results (conference + journal) → `version_of`, journal primary. New data or analyses → `different`, as separate studies.
- **Groups (V-3).** A group is every record connected by `version_of`/`duplicate_of` links. A group has exactly one primary; conflicting primaries, or a `same` on an identifier-conflict pair (V-9), stop the build.
- **Withdrawal (V-4).** One mechanism only: a `withdrawn` row naming the `link_id`. Rows are never edited or deleted, so the file is the audit trail. The latest active row per pair applies.
- **Screening decisions (V-5).** Decisions stay attached to **paper IDs** (D-027) and are never copied to another record.
  - A secondary version shows "linked to Pxxxx" and has no decision of its own.
  - When a link is withdrawn or the primary changes, every record without its own decision shows `not_screened`, and the build report lists it for screening. Nothing is inherited silently.
  - A decision on a former primary stays on that record.
- **Corrections (V-6).** The notice is excluded once at Stage 0 (E5) and counted there. The link exists so the correction is read at extraction; the correction is applied to the article's extracted data and cited.
- **Retractions (V-7).** The retracted article is E7 at Stage 0, as now. A retraction notice is E5 and linked with `retraction_of`. If the primary of a version group is retracted, the **whole group** is excluded under E7 at the study level, and its other versions (e.g., the preprint) are not used as evidence. → **Owner to confirm** this rule (comment field).

**4.3 Counting specification (PRISMA 2020: records, reports, studies)** (V-8)

| Step | Counted unit | Current numbers `[EVIDENCE]` | Rule |
|---|---|---|---|
| 1. Records identified | Source records per source, before deduplication (check re-fetches excluded) | PubMed 3,413; arXiv 76; web 54; total 3,543 | From `build_report.json` |
| 2. Removed: automatic identifier duplicates | Source records merged by shared PMID/DOI/PMCID/arXiv ID | 564 | As now |
| 3. Removed: `duplicate_of` | Publications linked as the same publication | 0 (no decisions yet) | Derived status `duplicate_removed`; no row in `decisions.csv`; reported as duplicates (E8 in the flow) |
| 4. Removed before screening: Stage 0 | Notices and retracted articles (E5/E7) | To be computed when Stage 0 runs | Rule-based, `screener=rule:stage0` |
| 5. Records screened (title/abstract) | Primaries + unlinked publications | 2,979 − step 3 − step 4 − secondaries | Secondaries of `version_of` groups are reported as "additional reports linked to a screened record", not screened separately |
| 6. Records excluded | By reason code | — | E1–E12 counts |
| 7. Reports sought / assessed at full text | Primaries (+ secondaries consulted for missing information) | — | |
| 8. Studies included | One per version group or unlinked record | — | |
| 9. Reports of included studies | Primary + linked secondary versions | — | Shown next to step 8 |

Until any pair is decided, both records of every flagged pair are screened as separate records. The pilot report lists the pairs.

- **Options.** (a) D-030 as above; (b) A-4 (secondary version → `exclude E8`); (c) no linking (only `same`/`different`).
- **Recommended:** (a). It is reversible, keeps every record, and does not count a report of an included study as an "excluded duplicate" (the problem with A-4).
- **Consequences.**
  - Schema: new columns; derived fields `version_group`, `version_role`, `linked_paper_ids`.
  - Code: link validation, group derivation, counting, tests.
  - PRISMA: per the table above.
  - Manuscript: flow diagram with records, reports and studies.
- **Depends on:** Item 5 (who decides), Item 1, Item 2 (notice types).
- **Evidence/manual review:** every pair decision needs the papers themselves. This item does **not** resolve any pair.

Owner response: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments (incl. confirmation of the group-level retraction rule):

---

## Item 5 — Q-024 (with Q-029): the 15 possible-duplicate pairs

**Reconciliation against `records/dedup_review.csv` `[EVIDENCE]`.**
- 15 rows, 30 distinct paper IDs. All 30 publications have `duplicate_status=possible_duplicate_review`.
- No flagged publication is outside the file, and every `possible_duplicates` entry corresponds to a row.
- By automatic reason: same title, year ±1: 3; same title, other differences: 5; fuzzy title: 4; identifier conflict: 3. This matches `collection_summary.md` ("12 title-based + 3 identifier-conflict = 15").
- **No count mismatch.**
- One presentational difference: `screening_protocol.md` §4 groups the three web-vs-PubMed pairs in one row, while `version_linking_proposal.md` §2 splits them into 2 + 1 (same article vs preprint). The total is 15 in both.
- The three identifier-conflict pairs also appear in `build_report.json` as registry conflicts (kept P1320/also P1213; P2148/P2128; P2535/P2488). Their IDs are stable.

| Pair | Automatic reason | Descriptive category (metadata only; **not a decision**) |
|---|---|---|
| P0010 / P1368 | same title, year ±1 | Preprint vs journal version |
| P1360 / P1442 | same title, year ±1 | Preprint vs journal version |
| P1466 / P1479 | same title, year ±1 | Preprint vs journal version |
| P1213 / P1320 | identifier conflict (pmid+doi+pmcid) | Preprint vs journal version |
| P2128 / P2148 | identifier conflict (pmid+doi+pmcid) | Preprint vs journal version |
| P2488 / P2535 | identifier conflict (pmid+pmcid) | Preprint vs journal version |
| P2562 / P2565 | same title, other differences | Preprint vs journal version |
| P2140 / P2149 | fuzzy title (0.958) | Preprint vs journal version |
| P1421 / P1488 | fuzzy title (0.938) | Unclear: titles differ ("Lipid Ratios…" vs "Lipidomics…") |
| P1343 / P2987 | same title, other differences | Web page vs PubMed record (URL contains P1343's DOI) |
| P0098 / P2988 | same title, other differences | Web page vs PubMed record (ACS page; DOI not in URL) |
| P0450 / P2978 | same title, other differences | Web preprint (medRxiv) vs PubMed article |
| P2870 / P2982 | fuzzy title (0.929) | arXiv record vs journal web page |
| P0113 / P0153 | fuzzy title (0.955) | Correction notice vs article |
| P2980 / P2981 | same title, other differences | Two web records with different patent numbers |

- **Issue.** Who decides the pairs, and when?
- **Options.** (a) The owner decides all 15 from the papers. (b) The assistant proposes decisions from the papers, and the owner audits all 15. (c) Defer; both records of each pair are screened, and the pairs are listed in the pilot report.
- **Recommended:** (c) for the pilot, then (b) once Item 4 is decided and implemented. With only 15 pairs, a full audit is cheap.
- **Q-029** (a `version` decision, "screen the primary only") is answered by Item 4 (D-030) or by A-4.
- **Consequences.** PRISMA counts are final only after the decisions.
- **Depends on:** Item 4.
- **Evidence/manual review:** yes, the papers.

Owner response: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

---

## Item 6 — Q-001: disorder scope (main list remains pending)

**Current text (`screening_criteria.md` §2.1, verbatim, PROVISIONAL):**
> **In scope:** type 1, type 2 and gestational diabetes; prediabetes / impaired glucose regulation;
> insulin resistance; metabolic syndrome; NAFLD/MASLD/NASH/MASH; dyslipidaemias; hyperuricaemia and
> gout; inborn errors of metabolism (incl. newborn-screening targets).
> **Pending researcher decision (included at screening, tagged `scope_pending`):** obesity (as a
> classification target), thyroid dysfunction, polycystic ovary syndrome.
> **Out of scope (E4):** complications of metabolic disease when the classification target is the
> complication itself (e.g., diabetic retinopathy, nephropathy, foot ulcer); cardiovascular events,
> cancer, and infectious disease, *unless* the record is retained for RQ2–RQ4 as a methodological exemplar.

- **Issue.** The main list has never been approved. Obesity, thyroid dysfunction and PCOS remain **PENDING** (your stated choice), included at screening and tagged.
- **Options.** (a) Approve the main list for screening, with the three conditions still pending. (b) Amend the main list (comments). (c) Defer; the pilot cannot run.
- **Recommended:** (a). The tag is renamed `scope_pending_disorder` so it cannot be confused with proteomics (Item 8).
- **Consequences.** E4 decisions in the pilot; the manuscript states the scope and the pending conditions.
- **Depends on:** D-013 (primary disorder, later), which is not affected.
- **Evidence/manual review:** your review of the list.

Owner response: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

---

## Item 7 — Q-002 / Q-035: biomarker strands and `biomarker_class`

**Current text (`screening_criteria.md` §2.2, summary of the verbatim definitions, in `decision_reconciliation_LIT-004.md` §5.2):**
- In scope: metabolomics/lipidomics (MS or NMR); newborn-screening MS/MS; routine clinical chemistry; mixed sets with substantive biochemical markers.
- Out of scope (E3): imaging-only, genomics/transcriptomics/methylation-only, microbiome-only, free text-only, CGM/wearable-only, questionnaire-only.

- **Issue.** You chose to keep routine chemistry and metabolomics/lipidomics as **distinct** strands. The inventory records only which query retrieved a paper, which is not evidence of its content. A content field is needed.
- **Proposal.** New screening descriptor `biomarker_class` = `metabolomics_lipidomics` / `newborn_screening_msms` / `routine_chemistry` / `mixed_both` / `other` / `unclear`.
  - Purpose: per-strand counts and synthesis based on what the study used, not on how it was found.
  - Reporting rule: NBS MS/MS is reported with metabolomics; `mixed_both` is reported in both strands.
- **Options.** (a) Approve both strands plus `biomarker_class`. (b) Both strands without the field (strand = retrieval theme; not recommended). (c) One strand only.
- **Recommended:** (a).
- **Consequences.** One more optional column in the screening schema, required for `include`/`uncertain` (as Item 3). The manuscript reports per strand.
- **Depends on:** Item 8, Item 3.
- **Evidence/manual review:** none.

Owner response: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

---

## Item 8 — Q-033: proteomics (remains pending)

- **Issue.** Proteomics and protein panels (e.g., cytokines) are defined neither in nor out of scope. Your stated choice: keep them **PENDING**.
- **Options.** (a) Pending, with flag `scope_pending_proteomics`: included at screening, decided later without re-screening. (b) In scope. (c) Out of scope (E3).
- **Recommended:** (a). Multi-omics studies with a substantive metabolomics layer stay eligible whatever is decided.
- **Consequences.** One flag value; reported as pending.
- **Depends on:** Item 7.
- **Evidence/manual review:** none.

Owner response: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

---

## Item 9 — Q-007 / D-009: the routine-biochemistry query Q-PM-02 (743 records)

- **Issue.** Q-PM-02 is the largest strand. 626 of its 743 records were found by no other query (21 % of 2,979).
- **Fit with the scope** (reconciliation §6). It is both broader and narrower than the provisional scope:
  - Broader: `diabetes[tiab]` also matches diabetes insipidus, and the wide "Metabolic Diseases" MeSH branch may reach conditions outside §2.1 (MeSH tree not verified).
  - Narrower: no free-text terms for prediabetes, insulin resistance, gout or inborn errors, so recent records not yet MeSH-indexed can be missed.
  - The laboratory-test terms match *mentions* of tests.
  - "artificial intelligence" is missing.
- Your condition "if the query matches the approved scope" therefore cannot be confirmed literally.
- **Options.**
  - (a) **Screen all 743** against the approved criteria. Out-of-scope records are excluded with E3/E4 and counted. Recall limits are reported. No completeness claim.
  - (b) Screen only records also matching explainability, calibration, uncertainty or validation terms, and characterise the rest by a sample. This is a post-search restriction, which the flow diagram must show.
- **Recommended:** (a).
  - The query is the executed, stored strategy for this strand, and restricting it now would be selective.
  - Over-retrieval costs screening time, not validity, because exclusions are counted by reason.
  - Routine chemistry matters most for dataset feasibility (Stage F).
- **Consequences.**
  - Screening: about 743 records in strand B.
  - PRISMA: E3/E4 counts.
  - Manuscript: the limitations listed above.
- **Depends on:** Items 6, 7 and 8.
- **Evidence/manual review:** none for the decision. The MeSH tree contents should be verified before the limitations are written.

Owner response: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

---

## Item 10 — Q-022: approve the executed search (D-005, D-006, D-007)

- **Issue.** The LIT-003 searches ran while the strategy decisions were still proposed. **26 of the 56 planned searches were executed. The search is not comprehensive and must not be described as such.**

| Source | Planned | Executed | Not executed (reason) |
|---|---|---|---|
| PubMed | 15 | 15 | 0 |
| arXiv (alphaXiv) | 5 | 5 | 0 |
| Publisher web search | 5 | 5 (domain filter not honoured) | 0 |
| Repository | 3 | 1 (Q-RP-03 fallback) | **2** (Q-RP-01, Q-RP-02: APIs blocked) |
| Consensus | 10 | 0 | **10** (quota exhausted) |
| Europe PMC | 6 | 0 | **6** (host blocked) |
| Semantic Scholar | 5 | 0 | **5** (host blocked) |
| Google Scholar | 4 | 0 | **4** (manual only, not done) |
| Crossref | 3 | 0 | **3** (host blocked) |
| **Total** | **56** | **26** | **30** |

Other deviations:
- The search ran on Day 10 instead of Day 3.
- arXiv and web records have no date limit and are not reproducible snapshots.
- arXiv records have no authors.

- **Options.**
  - (a) Approve D-005, D-006 and D-007 **as executed**, with the 30 unexecuted searches listed as *not searched* and the deviations as limitations.
  - (b) Approve, and require the blocked searches to be run when access exists, before Stage C.
  - (c) Reject and redesign.
- **Recommended:** (a), keeping (b) open. Most deviations are access limits that a re-run in this container would not remove.
- **Consequences.** The manuscript describes "a structured review with systematic elements, PubMed-centred, supplementary arXiv and web search; the following planned sources were not searched: …".
- **Depends on:** Items 11 and 12.
- **Evidence/manual review:** none for the decision.

Owner response: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

---

## Item 11 — D-012 / D-023 / Q-036: transcription controls and the outstanding spot-check

- **Issue.** Connector output that the assistant had to transcribe must pass a ≥ 10 % re-fetch spot-check (D-012).
  - PubMed: all 25 search pages passed an independent re-fetch, and 15/15 queries were identical (D-023).
  - **The 5 arXiv and 6 web raw files were never spot-checked** (`transcription_check=not_done` in `MANIFEST.csv`).
- **Options.**
  - (a) **Run the spot-check now** for arXiv (alphaXiv is reachable; web results are not reproducible, so a re-run checks only whether the same items are still returned), then approve D-012/D-023.
  - (b) Accept and document the gap as a limitation, then approve.
- **Recommended:** (a) for arXiv, (b) for web.
- **Consequences.** Verification statuses stay as they are either way: arXiv `partially_verified`, web `unverified`. Neither source can be cited before second-source verification.
- **Depends on:** Item 10.
- **Evidence/manual review:** the spot-check itself, if chosen.

Owner response (choose): [ ] APPROVE option (a)  [ ] APPROVE option (b)  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

---

## Item 12 — D-010 / Q-011: storage of raw exports

- **Issue.** Raw exports and abstracts are kept out of the public repository. A checksum-verified archive exists in two copies on one computer (owner-reported). **No off-device backup exists** (no external drive).
- **Options.** (a) Approve D-010 and accept the missing off-device backup as a documented limitation. (b) Approve D-010 and name another private storage location. (c) Make the repository private and commit the raw files.
- **Recommended:** (a) for now, with (b) when possible.
- **Consequences.** A reproducibility limitation.
- **Depends on:** none.
- **Evidence/manual review:** none.

Owner response: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

---

## Item 13 — D-008 / Q-008: researcher audit

- **Issue.** The assistant screens alone. D-008 proposes a blinded owner audit of 25 included + 25 excluded decisions after the first batches. If κ < 0.60 or a wrong exclusion is found, the criteria are clarified and the affected records re-screened. Owner time: about 60–75 min.
- **Options.** (a) Approve. (b) Smaller or larger audit (comments). (c) No audit; not recommended, as single-screener error would then be unmeasured.
- **Recommended:** (a).
- **Consequences.** Quality-control figures appear in the manuscript.
- **Depends on:** Item 14.
- **Evidence/manual review:** your time.

Owner response: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

---

## Item 14 — D-025 / Q-026: pilot design (no sample generated)

| Element | Proposal (`screening_protocol.md` §7) |
|---|---|
| Size | 60 records (about 2 % of 2,979) |
| Sampling | Stratified random, **seed 4004**, recorded in the pilot file |
| Strata | Primary retrieval theme: A, B, C, D, E, F, Q, plus arXiv/web. 8 each for A–E and Q (48), 6 for F, 6 for arXiv/web. A record retrieved by several themes goes to its rarest theme (order F, D, C, E, A, Q, B) |
| Inclusion in the sample | Stage-0 records excluded (rule-based); records without abstracts allowed |
| Screening | The assistant and the owner screen the same 60 **independently and blinded** (the owner's sheet shows no assistant decision) |
| Agreement reported | Percentage agreement; Cohen's κ on include/uncertain/exclude and on include vs not; agreement on the primary exclusion code; agreement per descriptor (Item 3) |
| Pass criteria | κ (3-level) ≥ 0.60 **and** no record excluded by one screener but included by the other without adjudicated agreement **and** fewer than 3 disagreements on any single code |
| If not passed | Criteria clarified (new version); a second pilot of 40 new records with the next seed |
| Expansion | Only after a pass and owner approval, in batches of about 300 |
| Outputs (later) | `screening/pilot_sample.csv`, both decision files, `pilot_report.md`. Metrics computed by script |

- **Options.** (a) Approve the design above. (b) The `screening_criteria.md` §7 pilot (first 30 PMIDs of Q-PM-01 and Q-PM-09). (c) Modify.
- **Recommended:** (a). (b) samples old records from two queries only and covers neither themes C, D or F nor arXiv/web.
- **Consequences.** Determines when screening can expand.
- **Depends on:** Items 1–3 and 6–10, 13 and 15.
- **Evidence/manual review:** your blinded screening of 60 records.

Owner response: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

---

## Item 15 — A-1 … A-6: screening-criteria amendments (`screening_protocol.md` §9)

Each line can be answered separately. Approved amendments go into `screening_criteria.md` v1.1 before the pilot.

| ID | Amendment | Recommended | Note |
|---|---|---|---|
| A-1 | Pilot design per protocol §7 instead of criteria §7 | Approve (= Item 14) | |
| A-2 | Code clarifications: E3 imaging/genetics-only; E4 non-metabolic unless method exemplar; E5 includes errata, patents, dataset-only descriptors; E6 only for non-English records (missing language ≠ E6); E8 only after a recorded dedup/version decision; E12 justification mandatory | Approve | Codes E1–E12 unchanged |
| A-3 | Separate descriptors (= Item 3) and the RQ5 counting rule (= Item 16) | See Items 3 and 16 | |
| A-4 | Secondary version → E8 | **Reject in favour of D-030** (Item 4) | Alternative kept open if Item 4 is rejected |
| A-5 | One screening file and columns (= Item 1) | Approve with Item 1 | |
| A-6 | No abstract → `uncertain` unless a title-level E-code applies | Approve | Consistent with Item 3 |

Owner response A-1: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner response A-2: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner response A-3: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner response A-4: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner response A-5: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner response A-6: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

---

## Item 16 — A-3 / Q-028: counting components for RQ5 (closest prior art)

- **Issue.** RQ5 counts a framework as closest prior art if it covers ≥ 3 components. The current criteria list four: feature selection, classification, explainability, and "calibration **or** uncertainty".
- **Options.** (a) Keep four components, with calibration or uncertainty counted as one. (b) Five components (uncertainty and calibration separate), still ≥ 3. (c) Five components, ≥ 4.
- **Recommended:** `[OPEN]`. No recommendation is given, because this choice directly changes which papers count as closest prior art and therefore any later novelty assessment.
  - Option (b) admits more papers as closest prior art. That is the more cautious choice before a novelty claim (RQ5 must be complete before any claim).
  - Option (a) keeps the current definition.
- **Consequences.** The theme F evidence table; the novelty assessment (Stage D).
- **Depends on:** Item 3.
- **Evidence/manual review:** none.

Owner response (choose): [ ] APPROVE (a)  [ ] APPROVE (b)  [ ] APPROVE (c)  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

---

## Item 17 — D-024: inventory schema revision (LIT-003)

- **Issue.** The LIT-003 evidence-table fields and sentinels ("REQUIRES FULL-TEXT REVIEW" etc.) are still proposed. Items 2 and 3 would revise two of its fields (`publication_type`; the descriptor columns). Q-034 adds an enum for `extraction_status`.
- **Options.** (a) Approve D-024 together with the revisions from Items 2 and 3 and the Q-034 enum. (b) Approve D-024 as it stands. (c) Defer.
- **Recommended:** (a).
- **Consequences.** A single schema version for the pilot.
- **Depends on:** Items 2 and 3.
- **Evidence/manual review:** none.

Owner response: [ ] APPROVE  [ ] REJECT  [ ] MODIFY  [ ] DEFER
Owner comments:

---

## 18. After the ballot (nothing below happens before the owner's responses)

1. Each response is recorded in `logs/DECISION_LOG.md` with the date and "researcher". MODIFY and DEFER responses are recorded as such, and the item is reworded or kept open.
2. Spot-check (Item 11a), if chosen.
3. One implementation task: Items 2, 3, 4, 7 and 8 in schema and code, with tests and a rebuild. Each step must be verified to change no paper ID and no existing value.
4. `screening_criteria.md` v1.1 and protocol v0.2 with the approved wording, frozen as the pilot's `criteria_version`.
5. Pilot sample and blinded screening (Item 14). Pair decisions (Item 5) when chosen.
