# Decision Reconciliation before Pilot Screening

| Field | Value |
|---|---|
| Task | LIT-004-DECISION-RECONCILIATION (2026-10-23) |
| Status | **Review document. Nothing in it is approved or implemented.** No decision status, schema, criteria, scope or strategy text was changed. The owner's recommended choices (LIT-004-DECISION-RECONCILIATION prompt) are recorded here as *recommendations to be approved*, per GOVERNANCE.md (approval = a DECISION_LOG entry approved by the researcher) |
| Read for this review | `approval_request_LIT-004.md`, `research_plan.md`, `logs/DECISION_LOG.md`, `unresolved_questions.md`, `screening_criteria.md`, `screening_protocol.md`, `search_strategy.md`, `version_linking_proposal.md`, `scope_decision_brief.md`, `search_queries.csv`, `raw_exports/MANIFEST.csv`, `access_report.md`, `paper_inventory.json` |

Labels: `[EVIDENCE]` from project files or counts; `[HYPOTHESIS]` not verified; `[RECOMMENDATION]`; `[OPEN]`.

---

## 1. Consolidated decision table

"Approve first?" = must the owner explicitly approve before anything is implemented.

| ID | Proposed wording (exact; revised wording in §§2–5 where marked) | Recommended option (owner's preference) | Consequences | Dependencies | Evidence still needed | Approve first? |
|---|---|---|---|---|---|---|
| **D-027** | "`screening/decisions.csv` is the canonical screening-decision file (columns and values as in `schemas/screening_decision.schema.json`). Records without a persistent bibliographic identifier and without a year receive the deterministic registry key `source_record:<source_record_id>`. The URL-key alternative is rejected." (`approval_request_LIT-004.md` §1) | Approve as worded | **Schema/code:** already implemented on the PR branch (LIT-004-WORKFLOW-FIXES). **Workflow:** `screening_criteria.md` §6 and `search_strategy.md` §6.2 text amended to match (now notes only). **Manuscript:** methods state that IDs are stable and screening records are validated | The column list includes `dim_independent_validation`, whose definition changes under D-029. Approving D-027 "as in the schema" would freeze the old enum. **Approve D-027 for the file, the key scheme and the required columns; the descriptor columns follow D-029** (§3) | None | Yes (approval only; code exists) |
| **D-028** | Revised wording in §2 (the prepared option-a text is incomplete) | Option A, as revised in §2 | **Schema:** `publication_type` enum replaced (all values are currently empty, nothing lost); `record_type` enum loses `preprint` and `notice` (proposal; §2.4). **Code:** deterministic mapping + `unmapped_publication_types` in the build report; `publication_type` removed from the manual fields. **Workflow:** Stage 0 reads `publication_type`. **Manuscript:** counts by publication type are reproducible from the mapping table | D-024 (schema, proposed); protocol §2 (`record_type`, D-025); Stage-0 rule (`search_strategy.md` §6.1) | Mapping table checked against all 34 source types present (§2.3) | **Yes** |
| **D-029** (revises D-026) | Revised wording in §3 | Option A as the owner restated it: three method descriptors `yes/no/unclear` plus a separate `validation_design` | **Schema:** `dim_independent_validation` replaced by `validation_design` (no screening rows exist, nothing lost); required for `include`/`uncertain`. **Code:** enforcement in `load_screening_decisions`; tests. **Workflow:** assignment rules (§3.3) and human-review triggers (§3.4) go into the protocol. **Manuscript:** title/abstract descriptors are reported as "stated in the abstract", never as prevalence of absence | D-026 (proposed, to be revised); A-3/Q-028 (RQ5 counting); D-027 column list | Pilot agreement on descriptors (D-025 measures it) | **Yes** |
| **D-030** (alternative to A-4) | `version_linking_proposal.md` §3, with the ambiguities in §4 below resolved first | Owner prefers reversible, provenance-preserving links without automatic merging = D-030 | **Schema:** new columns in `records/dedup_decisions.csv`; derived fields `version_group`, `version_role`, … in the publication record and inventory. **Code:** link validation, group derivation, counting. **Workflow:** pair decisions entered from the papers. **Manuscript:** PRISMA 2020 flow with records, reports and studies | Q-024 (who decides); §4 issues V-1 … V-9; D-027 (decisions attach to paper IDs) | A written counting specification (§4, V-8) | **Yes**, after the wording is revised |
| **Q-001** | Keep the §2.1 list (§5.1) as provisional; obesity, thyroid dysfunction and PCOS stay `scope_pending` | Owner: keep the three `scope_pending` until the exact list is reviewed | **Criteria:** none now. **Workflow:** the tag `scope_pending` is used at screening. **Manuscript:** scope stated as provisional until approved | D-013 (primary disorder, later) | Owner's review of the exact list (§5.1) | Yes, to confirm the main list (the pending tags need no change) |
| **Q-002** | Both strands retained as **distinct** strands | Owner: retain both as distinct | **Schema/workflow:** "distinct" needs a recorded strand per record; retrieval theme is not the record's content (protocol §1). Proposed new descriptor `biomarker_class` (§5.3, new Q-035). **Manuscript:** results reported per strand | Q-035; Q-033 | None | Yes (and Q-035) |
| **Q-033** | Proteomics and other protein-biomarker panels `scope_pending` | Owner: keep `scope_pending` | **Workflow:** a defined flag value is needed (§5.3); multi-omics with a substantive metabolomics layer stays eligible regardless | Q-002 | None | Yes (flag wording) |
| **Q-007 / D-009** (Q-PM-02) | Option A: screen all 743 at title/abstract, full text by tier | Owner: provisionally Option A, if the query matches the approved scope | **Workflow:** stratum B of the pilot drawn from all records. **Manuscript:** query limitations reported (§6) | Q-001, Q-002 approved; the condition "query matches approved scope" cannot be met literally (§6) | None for the decision; MeSH-tree verification for the limitations text | Yes |
| **Q-022** (D-005, D-006, D-007) | "D-005, D-006 and D-007 are approved **as executed** on 2026-10-23, with the deviations listed in `decision_reconciliation_LIT-004.md` §7 recorded as limitations" | `[RECOMMENDATION]` approve as executed with limitations | **Manuscript:** "structured review with systematic elements"; PubMed-centred; 30 of 56 planned searches not run, listed as not searched. **No comprehensive-search claim** | D-010, D-012/D-023 | §7: arXiv/web transcription spot-check not done (new Q-036) | Yes |
| **D-012 / D-023** | Transcription controls as proposed | `[RECOMMENDATION]` approve, after the arXiv spot-check (Q-036) or with the gap stated | Verification statuses unchanged (arXiv capped at `partially_verified`, web `unverified`) | Q-022 | Q-036 | Yes |
| **D-010 / Q-011** | Storage rule; off-device backup unavailable | Owner decision | Limitation in the reproducibility statement | — | — | Yes (not pilot-blocking) |
| **D-008 / Q-008** | Researcher audit 25 + 25, κ < 0.60 rule | Owner decision | Quality control of single screening | D-025 | Owner's availability | Yes |
| **D-025 / Q-026** | Pilot design (60 records, seed 4004) vs `screening_criteria.md` §7 pilot | Owner decision | Pilot files | All of the above | — | Yes |
| **A-1 … A-6, Q-028** | `screening_protocol.md` §9 | Owner decision | New criteria version (v1.1) before the pilot | D-029 (A-3), D-030 (A-4) | — | Yes |

## 2. D-028: roles of the three type fields

### 2.1 Definitions (proposed revised wording)
| Field | Role | Who fills it | Values |
|---|---|---|---|
| `source_publication_types` | **Verbatim** source-provided types, never edited, never normalised. Publication level = the list from the field-priority source (as recorded in `field_provenance`); every source's own list stays in `source_records.jsonl` | Build (copied) | Free strings as given (34 distinct PubMed values in the current build) |
| `publication_type` | **Normalised bibliographic type derived only from source metadata** by a versioned mapping table. Not a judgement about the content | Build (mapping; never by hand) | See §2.2 |
| `record_type` | **Screening classification** of what the paper *is for the review*, made by the screener from title/abstract (or full text) | Screener | `original`, `methodological`, `software`, `guideline`, `review_lead`, `other` (§2.4) |

### 2.2 Mapping and precedence (deterministic; first match wins)
| Order | `publication_type` | Source evidence |
|---|---|---|
| 1 | `retraction_notice` | PubMed *Retraction of Publication* |
| 2 | `expression_of_concern` | *Expression of Concern* |
| 3 | `erratum_or_correction` | *Published Erratum*, *Correction* |
| 4 | `study_protocol` | *Clinical Trial Protocol* |
| 5 | `dataset` | *Dataset* |
| 6 | `preprint` | *Preprint*; or source database = arXiv |
| 7 | `review` | *Review*, *Systematic Review*, *Scoping Review*, *Meta-Analysis*, *Evidence Synthesis* |
| 8 | `guideline_or_consensus` | *Guideline*, *Practice Guideline*, *Consensus Statement* |
| 9 | `editorial_comment_letter` | *Editorial*, *Comment*, *Letter*, *News* |
| 10 | `conference_paper` | *Conference Proceedings*, *Congress* |
| 11 | `journal_article` | *Journal Article* (only if nothing above matched) |
| — | `unknown` | No source type at all (113 records: 76 arXiv are caught by row 6; 37 web) |
| — | `other` | Only unrecognised types present |

- **Retracted articles:** *Retracted Publication* marks an article that **was retracted**. It is not a notice. It does not change `publication_type` (for example, it stays `journal_article`). It sets the existing `retracted` flag (Stage 0, E7). The prepared option-a text omitted this distinction.
- **Ignored for the class, kept verbatim:** *Research Support…*, *Validation Study*, *Multicenter Study*, *Comparative Study*, *Observational Study*, *Randomized Controlled Trial*, *Clinical Trial* (and phases), *Evaluation Study*, *English Abstract*, *Historical Article*, *Video-Audio Media*.
- **Unrecognised types:** any type that appears in neither the mapping nor the ignore list gives `other`. It is also listed in the build report as `unmapped_publication_types`, and the run does not fail. The table is then extended by a logged change, never silently. No source type is ever dropped.
- **Missing types:** `unknown`. It is never inferred from a URL or a title, so web results stay `unknown`.
  - Example: the USPTO records would need an approved URL rule to be called patents.
  - `[OPEN]` Should a URL or DOI-prefix rule (USPTO → `patent`; `10.1101` → `preprint`) be allowed? It is source metadata, but its interpretation would be a heuristic. Not proposed by default.
- **Several types present:** the mapping takes the highest-precedence one. All types remain in `source_publication_types`.

### 2.3 Check against the current data `[EVIDENCE]`
- The 34 distinct source types (counted from `paper_inventory.json`) are all covered by §2.2 or by the ignore list.
- Records most affected:
  - *Journal Article*: 2,848
  - *Review*: 339
  - *Preprint*: 39 (PubMed) + 76 arXiv
  - *Clinical Trial Protocol*: 3
  - *Retracted Publication*: 3
  - *Dataset*: 2
  - *Published Erratum*: 2
- The prepared enum would have had no category for protocols, datasets, guidelines/consensus statements or expressions of concern. This is a contradiction in the prepared text, corrected above.

### 2.4 `record_type` overlap `[OPEN]`
The protocol's list (D-025) contains `preprint` and `notice`. Both are **bibliographic** facts, which `publication_type` now carries. If they are kept in `record_type`, the two fields can disagree.

Proposed: remove them from `record_type`, so that preprint status comes from `publication_type`. `record_type` then describes content only. A preprint that is original research is `record_type=original`, `publication_type=preprint`. This revises the protocol's §2 list and needs approval.

## 3. D-026 vs D-029: the four screening dimensions

### 3.1 Incompatibilities found
| # | D-026 / protocol §2 (proposed) | D-029 as prepared (option a) | Owner's restatement (this prompt) | Conflict |
|---|---|---|---|---|
| C-1 | `dim_independent_validation`: `external / temporal / internal_only / unclear` | Four descriptors, all `yes/no/unclear`, plus `validation_design` | **Three** `yes/no/unclear` descriptors; validation design separate | Is there still a `yes/no/unclear` validation descriptor? **Resolution proposed:** no. The four required items are `dim_explainability`, `dim_uncertainty`, `dim_calibration` and `validation_design`. A yes/no would duplicate the design value (external/temporal ⇒ yes) and could contradict it |
| C-2 | "`yes` = the abstract **states** that …" | `no` only if absence is stated or implied by the design | — | Compatible. D-026 does not define `no`; D-029 does |
| C-3 | `dim_uncertainty` examples include "ensembles" | — | — | A random forest is an ensemble, but that is not an uncertainty estimate. The example needs the qualifier "ensembles **used to estimate** predictive uncertainty" |
| C-4 | `dim_calibration` examples include "Brier score" | — | — | The Brier score mixes discrimination and calibration. Proposed: Brier score alone → `unclear`; calibration plot/slope/intercept, ECE, Hosmer–Lemeshow or recalibration → `yes` |
| C-5 | `dim_explainability`: "explanation/attribution method used or studied"; "interpretable" without a method → `unclear` | — | — | Not settled: built-in feature importance and inherently interpretable models (coefficients of a logistic model) — `yes` or `unclear`? Criteria RQ2 treats importance without a stated method as insufficient. Proposed: `yes` only if the abstract names the method (SHAP, LIME, permutation importance, attention analysis, coefficient interpretation reported as explanation); otherwise `unclear` |
| C-6 | Analytical-chemistry "calibration" (instrument calibration curves) | — | — | Known term problem (`search_strategy.md` §3.1). Proposed: analytical calibration alone → `dim_calibration=no`, with a justification |

### 3.2 Proposed revised D-029 wording
> For every `include` or `uncertain` row, four fields are required: `dim_explainability`,
> `dim_uncertainty`, `dim_calibration` (each `yes`, `no`, `unclear`) and `validation_design`
> (`external`, `temporal`, `internal_only`, `none`, `not_applicable`, `unclear`). The column
> `dim_independent_validation` is replaced by `validation_design`. Values describe what the title
> and abstract **state**; missing information is never read as `yes`. D-026 is revised accordingly
> (C-1 to C-6).

### 3.3 Assignment from title/abstract
| Value | Rule |
|---|---|
| `yes` | The title or abstract names the method or result (examples in C-3 to C-5) |
| `no` | The abstract explicitly states its absence, **or** it fully describes the analysis and the element is clearly outside it. Example: analytical calibration only (C-6). Silence alone is **not** `no` |
| `unclear` | Not mentioned; vague wording ("interpretable", "robust"); no abstract (119 records); or conflicting statements |
| `validation_design` | Strongest design stated, in the order `external` (different cohort, site or dataset) > `temporal` (same source, later period) > `internal_only` (CV, bootstrap, random hold-out from the same cohort) > `none` (apparent performance only). `not_applicable` = no predictive model evaluated (reviews, pure methods without empirical evaluation). `unclear` = not stated, or "independent test set" without saying whether it is from the same cohort |

### 3.4 When human review is needed (`needs_human=yes`)
- Any C-3 to C-6 term problem that the screener cannot settle from the abstract.
- `validation_design` = `unclear` when the record is otherwise `include` for RQ4.
- Any record where the descriptors decide RQ5 status (≥ 3 components). These feed the closest-prior-art table, so all are human-checked.
- Every descriptor disagreement in the pilot.
- Records without an abstract that are retained as `uncertain`. Their descriptors are all `unclear`, and they are filled at full text.

**Consequence for synthesis:** title/abstract descriptors measure *what abstracts report*. A low share of `yes` is not evidence that the methods are absent. Prevalence claims need full-text extraction.

## 4. Version-linking proposal: ambiguities (no pair resolved)

| # | Topic | Ambiguity in `version_linking_proposal.md` | Proposed clarification |
|---|---|---|---|
| V-1 | Primary selection | "Primary = peer-reviewed version" conflicts with the source-priority rule (`search_strategy.md` §5.3: PubMed > … > web) when the peer-reviewed version exists only as an unverified web record. Example: P2870 (arXiv) / P2982 (ScienceDirect page, no year) | Primary = peer-reviewed version. Before the record is screened or cited, its metadata must be verified (`verified` or `partially_verified`); until then the group is screened from the best-verified member, and `needs_human` is set |
| V-2 | Primary selection | No rule for two peer-reviewed versions (conference paper + extended journal paper) or for a version with new data | Same data and results → `version_of`, journal version primary. New data or analyses → `different` (separate studies), with a note |
| V-3 | Groups | Links are pairwise, but a work can have > 2 records (preprint, web copy, journal article). "No chains" is stated but group semantics are not | Group = connected component of `version_of` / `duplicate_of` links. Exactly one primary per component; conflicting primaries stop the build |
| V-4 | Withdrawn links | Two mechanisms: "`withdrawn` cancels the latest earlier decision for the pair" vs "`link_id` lets a later row withdraw a specific decision" | One mechanism: a `withdrawn` row must name the `link_id`. The latest active row per pair applies |
| V-5 | Withdrawn links and screening | Unspecified effect on decisions already made. A secondary that "followed" its primary has no decision of its own; if the primary changes, the new primary may be unscreened | Decisions stay attached to paper IDs (D-027). After a withdrawal or a change of primary, every record without its own decision shows `not_screened`, and the build report lists them for screening. Nothing is inherited silently |
| V-6 | Correction notices | The notice is excluded at Stage 0 (E5) **and** shown as linked. It is unclear whether PRISMA counts it as an excluded record or as a linked report | Count it once, as excluded at Stage 0 (E5, "correction notice"). The link exists only so the correction is read at extraction |
| V-7 | Retractions | Not covered. Open cases: a retraction notice and its article; a preprint of a retracted article; a group whose primary is retracted | Add `retraction_of` (notice → article; notice E5, article E7 as now). If the primary of a group is retracted, the whole group is excluded under E7 at the study level, and other versions are not used as evidence; owner to confirm |
| V-8 | Duplicate reports and PRISMA | The proposal mixes levels: "records identified" is counted at the publication level, but PRISMA counts records per source **before** deduplication. The status of `duplicate_of` records is not defined (E8 row or derived status?). Redundant publication of one study in two journals is not covered | Fixed counting chain: source records identified (3,543; check re-fetches excluded) → automatic identifier duplicates removed (564) → `duplicate_of` removed (derived status `duplicate_removed`, no row in `decisions.csv`, counted as E8 in the flow) → records screened (primaries + unlinked records) → reports linked to included studies → studies included (one per group). Redundant publication = `version_of` |
| V-9 | Existing `same` | `same` stays allowed. It is silently ignored for identifier-conflict pairs | If D-030 is approved: a `same` on an identifier-conflict pair stops the build. Recommend not using `same` for the 15 pairs |

## 5. Scope: existing definitions (verbatim) and consequences

### 5.1 Disorders — `screening_criteria.md` §2.1 [PROVISIONAL — Q-001]
> **In scope:** type 1, type 2 and gestational diabetes; prediabetes / impaired glucose
> regulation; insulin resistance; metabolic syndrome; NAFLD/MASLD/NASH/MASH; dyslipidaemias;
> hyperuricaemia and gout; inborn errors of metabolism (incl. newborn-screening targets).
>
> **Pending researcher decision (included at screening, tagged `scope_pending`):** obesity
> (as a classification target), thyroid dysfunction, polycystic ovary syndrome.
>
> **Out of scope (E4):** complications of metabolic disease when the classification target is the
> complication itself (e.g., diabetic retinopathy, nephropathy, foot ulcer); cardiovascular events,
> cancer, and infectious disease, *unless* the record is retained for RQ2–RQ4 as a methodological
> exemplar.

Owner's choice (keep the three pending) = the current text, so no change is needed. The main list itself is still unapproved.

### 5.2 Biomarkers — `screening_criteria.md` §2.2 [PROVISIONAL — Q-002]
> **In scope:** Metabolomics / lipidomics (targeted or untargeted; MS- or NMR-based; any biofluid
> or tissue). Newborn-screening profiles (MS/MS amino acids and acylcarnitines). Routine
> clinical-chemistry and laboratory values (e.g., glucose, HbA1c, lipid panel, liver enzymes, renal
> markers, insulin/C-peptide, uric acid; also complete blood count when combined with chemistry).
> Mixed feature sets (demographic, anthropometric or clinical variables combined with biochemical
> markers, provided the biochemical markers are a substantive part of the model input — stated, or
> ≥ 1 biochemical marker among the final predictors).
>
> **Out of scope (E3):** imaging-only; genomics, transcriptomics or methylation-only;
> microbiome-only; free text-only; continuous-glucose-monitoring or wearable time series only;
> questionnaire-only.

### 5.3 Consequences of the owner's scope choices
- **Q-002 "distinct strands":** the inventory records only the *retrieval* theme (A or B), which is not evidence of content. A content field is needed. Proposed new Q-035: screening descriptor `biomarker_class` with values `metabolomics_lipidomics`, `newborn_screening_msms`, `routine_chemistry`, `mixed_both`, `other`, `unclear`. The newborn-screening and mixed categories must be assigned to a strand explicitly; proposed: NBS MS/MS reported with metabolomics, and `mixed_both` in both strands.
- **Q-033 proteomics `scope_pending`:** proposed flag `scope_pending_proteomics`, kept separate from the disorder flag `scope_pending` so the two pending questions can be resolved independently.
- **Disorder `scope_pending`:** proposed to become `scope_pending_disorder` for the same reason. This is a wording change to the criteria and needs approval.

## 6. Q-PM-02 against the documented scope

Query `[EVIDENCE]` (`search_queries.csv`):
`("Metabolic Diseases"[Mesh] OR "metabolic syndrome"[tiab] OR diabetes[tiab] OR "fatty liver"[tiab] OR NAFLD[tiab] OR MASLD[tiab] OR dyslipidemia[tiab]) AND ("laboratory test*"[tiab] OR "biochemical marker*"[tiab] OR "biochemical parameter*"[tiab] OR "clinical chemistry"[tiab] OR "blood test*"[tiab] OR "routine laboratory"[tiab] OR "Clinical Laboratory Techniques"[Mesh]) AND ("Machine Learning"[Mesh] OR "machine learning"[tiab] OR "deep learning"[tiab]) AND 2015/01/01:{RUN_DATE}[edat]`

| Aspect | Finding | Label |
|---|---|---|
| Broader than scope | `diabetes[tiab]` also matches diabetes insipidus. `"Metabolic Diseases"[Mesh]` is a wide MeSH branch; it is expected to include conditions outside §2.1 (e.g., electrolyte, iron or bone metabolism disorders) | `[EVIDENCE]` for the text match; `[HYPOTHESIS]` for the MeSH tree contents (not verified; the MeSH browser is not reachable) |
| Narrower than scope | No free-text terms for prediabetes, insulin resistance, hyperuricaemia/gout, inborn errors or NASH/MASH; these are reached only through MeSH. Recent citations not yet MeSH-indexed (the run includes 2026 entries) would be missed unless the free text says "diabetes" etc. | `[EVIDENCE]` for the query text; `[HYPOTHESIS]` for the size of the effect |
| Biomarker block | Matches *mentions* of laboratory tests. A paper using labs as a reference standard, or "blood test" in passing, is retrieved. A paper that uses HbA1c, lipids etc. without these phrases is missed. `"Clinical Laboratory Techniques"[Mesh]` may cover non-chemistry techniques | `[HYPOTHESIS]` |
| ML block | Lacks "artificial intelligence", which Q-PM-01 has | `[EVIDENCE]` |
| Size | 743 records, 626 retrieved by no other query, 34 also by the metabolomics strand | `[EVIDENCE]` |

**Is screening all 743 appropriate?** `[RECOMMENDATION]` Yes, under conditions.
- The query is the executed, stored strategy for RQ1 strand B. Restricting it now (Option B) would be a post-search filter that has to be reported as such.
- Records outside the scope are excluded at screening with E3/E4 and counted, so over-retrieval costs effort but not validity.
- The owner's condition "if the query is confirmed to match the approved scope" **cannot be met literally**: the query is both broader and narrower than §2.1/§2.2, and the scope is not approved yet.
- Proposed wording instead: "Option A: all 743 Q-PM-02 records are screened against the approved criteria. Out-of-scope records are excluded with E3/E4 and counted. The query's recall limits (above) are reported as limitations. No claim is made that the strand is complete."
- Not before Q-001/Q-002 are approved.

## 7. Search-strategy approvals vs. what was executed

| Decision | As proposed | As executed `[EVIDENCE]` | Consequence for approval |
|---|---|---|---|
| D-005 | Structured review with systematic elements, no completeness claim | Consistent | Can be approved as written |
| D-006 | PubMed primary; Consensus, arXiv, publisher web supplementary; Europe PMC, Crossref, Semantic Scholar if enabled; Google Scholar manual | 26 of 56 planned searches run: PubMed 15/15, arXiv 5/5, publisher web 5/5, repository fallback Q-RP-03 1/3. Not run: Consensus 0/10 (quota), Europe PMC 0/6, Semantic Scholar 0/5, Crossref 0/3, repository APIs 0/2 (blocked), Google Scholar 0/4 (manual, not done). Web domain filter not honoured | Approval "as executed" must list the 30 unexecuted searches as **not searched**. No comprehensive search may be claimed. Re-running when access exists remains an option (D-006 unchanged) |
| D-007 | Application strands from 2015 (`[edat]`), methods unrestricted, run-date cap | PubMed as designed (cap 2026-10-23). arXiv/web: no date limit (relevance-ranked tools) | Consistent for PubMed. arXiv/web are not reproducible snapshots |
| D-012 / D-023 | ≥ 10 % re-fetch spot-check of transcribed output; check-search for PubMed pages | PubMed: 25/25 search pages passed (re-fetch, 15/15 queries identical). **arXiv: 5 transcribed files, check `not_done`. Web: 6 files, `not_done`** | The spot-check was not met for arXiv and web. Either run it before approval (alphaXiv is reachable; new Q-036) or approve with the gap stated. arXiv stays `partially_verified` and web `unverified` either way |
| D-010 | Raw exports git-ignored | Done; archive verified; two copies on one computer; no off-device backup | Limitation, not pilot-blocking |
| Timing | Day 3 | Day 10 | Reported |

## 8. Contradictions found (summary)

1. **D-028 option a** has no categories for protocols, datasets, guidelines/consensus statements or expressions of concern, and does not separate *Retracted Publication* (a status) from a retraction notice (§2).
2. **D-028 vs `record_type`:** `preprint` and `notice` in `record_type` duplicate bibliographic facts (§2.4).
3. **D-029 as prepared vs the owner's restatement:** four yes/no/unclear descriptors vs three plus `validation_design` (C-1).
4. **D-026 definitions:** "ensembles", "Brier score", built-in feature importance, analytical calibration (C-3 to C-6).
5. **D-027 "as in the schema"** would freeze the descriptor enum that D-029 changes.
6. **D-030:** primary selection vs source priority (V-1); two withdrawal mechanisms (V-4); retractions missing (V-7); PRISMA levels mixed (V-8).
7. **Q-PM-02 condition:** "matches the approved scope" cannot be confirmed (§6).
8. **D-012 spot-check** not met for arXiv and web output (§7).
9. **Q-002 "distinct strands"** has no content field to support it (§5.3).

## 9. Exact choices that require the owner's explicit approval

| # | Choice | Options to answer |
|---|---|---|
| 1 | D-027 for the file, key scheme and required columns, with the descriptor columns governed by D-029 | approve / amend |
| 2 | D-028 revised (§2.1–2.2): roles, mapping, precedence, `unknown`/`other` handling | approve / amend |
| 3 | URL or DOI-prefix rules for `publication_type` (§2.2) | none (default) / allow named rules |
| 4 | Remove `preprint` and `notice` from `record_type` (§2.4) | remove / keep |
| 5 | D-029 revised (§3.2) replacing D-026's validation enum; definitions C-3 to C-6; assignment rules §3.3; human-review triggers §3.4 | approve / amend each |
| 6 | D-030 with clarifications V-1 to V-9 (incl. new `retraction_of`; E7 for a group whose primary is retracted) | approve / amend; or A-4 instead |
| 7 | Q-024: who decides the 15 pairs | researcher / assistant with audit |
| 8 | Q-001: the §5.1 main list (pending three unchanged) | confirm / amend |
| 9 | Q-002 with Q-035 (`biomarker_class` descriptor; NBS and mixed-set strand rules) | approve / amend |
| 10 | Q-033 flag `scope_pending_proteomics`; disorder flag renamed `scope_pending_disorder` | approve / amend |
| 11 | Q-007 / D-009: Option A with the wording in §6 | approve / Option B |
| 12 | Q-022: D-005, D-006, D-007 as executed with §7 limitations | approve / request re-runs |
| 13 | D-012 / D-023, and Q-036 (run the arXiv/web spot-check first, or accept the gap) | spot-check first / accept gap |
| 14 | D-008 / Q-008 audit; D-025 / Q-026 pilot design | approve / alternative |
| 15 | Criteria amendments A-1, A-2, A-5, A-6; A-3 / Q-028 RQ5 counting | approve each |

## 10. Recommended order of implementation (after the approvals concerned)

1. **Record the approvals** in `DECISION_LOG.md` (status changes only in that step, with date and "researcher").
2. **Close the search record:** run the arXiv/web spot-check if chosen (Q-036). Then record the approval of Q-022 / D-012 / D-023 with the limitations.
3. **Schema and code, in one task, with tests and a rebuild:**
   - D-028 (mapping, `unmapped_publication_types`);
   - D-029 (`validation_design`, required descriptors);
   - Q-035 / Q-033 flags;
   - D-030 (links, group validation, counting chain);
   - each step verified to change no paper ID and no existing inventory value.
4. **Documents:**
   - `screening_criteria.md` v1.1 with the approved scope wording and amendments;
   - protocol v0.2 (descriptor rules, human-review triggers, `record_type` list);
   - `search_strategy.md` change-history entry;
   - all three frozen as the pilot's `criteria_version`.
5. **Pair decisions (optional before the pilot):** the 15 pairs decided from the papers by the person named in Q-024. Otherwise both records stay in screening.
6. **Pilot:** generate the 60-record sample (D-025), then the blinded assistant and researcher screening and the agreement report. Expansion only after the pass criteria are met and approved.
