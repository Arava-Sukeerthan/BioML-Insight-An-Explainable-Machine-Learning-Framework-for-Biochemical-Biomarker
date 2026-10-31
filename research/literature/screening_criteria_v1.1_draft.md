# Screening Criteria — version 1.1 (DRAFT)

| Field | Value |
|---|---|
| Task | SCREENING-PREREQ-DECISIONS-2 (2026-10-30; assistant draft) |
| Version | **1.1 — DRAFT for researcher review. NOT frozen. Not in force.** |
| Replaces | `screening_criteria.md` v1.0 (2026-10-14, draft) **only when** the researcher approves and freezes this text as the pilot's `criteria_version` (D-035 record §6, condition 5). v1.0 is kept unchanged for traceability |
| Companion | `screening_protocol_v0.2_draft.md` (operational rules, pilot, audit trail) |
| Screening status | **INACTIVE.** No record has been screened, labelled or sampled |
| Governing decisions | D-008, D-009, D-012/D-023, D-024, D-025, D-027 (limited), D-028, D-029, D-031–D-038, D-043, D-044, D-055–D-062. Every change from v1.0 is traced in §9 |
| Wording rule | Only approved decisions are written as rules. Items still open are marked **[OPEN]** and listed in §10 |

Records are screened against the criteria of **the RQ strand(s) they could inform**. A record is included if it satisfies the criteria of at least one RQ. Its RQ tags are recorded.

---

## 0. Records to which these criteria apply
The **1,470** publication records defined by D-044 (records retrieved by G-1…G-7, Q-PM-01, Q-PM-02, Q-PM-03, Q-PM-11, Q-PM-12; `paper_inventory.json` SHA-256 `a509538d…f4a3`). All 743 Q-PM-02 records are screened (D-009). The remaining inventory records are outside the approved screening scope; they are neither screened nor excluded, and the review reports the reduced scope (D-044).

## 1. Common criteria (all RQs)

### Inclusion (all must hold) — unchanged from v1.0
| Code | Criterion |
|---|---|
| I-C1 | Peer-reviewed journal article, peer-reviewed full conference paper, or preprint (preprints flagged; published version preferred when it exists) |
| I-C2 | Full text or an abstract sufficient for the extraction fields of the relevant RQ |
| I-C3 | English language |
| I-C4 | Original research, methodological/statistical paper, software/framework paper, reporting guideline or consensus statement. **Reviews** are included only as *lead sources* (`record_type=review_lead`) |

### Exclusion (first applicable code in numerical order is the primary reason)
Codes E1–E12 are unchanged in number and meaning; the clarifications approved in D-059 (A-2, as modified) are added.

| Code | Reason | Clarification (D-059, A-2) |
|---|---|---|
| E1 | Not human data (animal, cell-line, plant, environmental) — RQ1, RQ2b, RQ4-applications | — |
| E2 | No supervised predictive model or classifier developed, validated or evaluated | — |
| E3 | Input data are not biochemical biomarkers (§2.2) | Includes imaging-only and genetics-only inputs for RQ1/RQ2b/RQ4a |
| E4 | Target condition outside the metabolic-disorder scope (§2.1) | **Not applied** when the record is retained as `non_metabolic_method_exemplar` for RQ2–RQ5, **or** is a non-metabolic framework with three or more possible RQ5 components, which is flagged `non_metabolic_rq5_candidate` instead (D-055; name D-061). The flag never decides inclusion or exclusion by itself; other E-codes still apply |
| E5 | Editorial, commentary, news, letter without original data, conference abstract only, study protocol without results, thesis, book chapter | Explicitly includes errata/correction notices, patents and dataset-only descriptors |
| E6 | Not English | Only when the record itself is non-English (`language` ≠ `eng` and no English full text). Missing language is **not** E6 |
| E7 | Retracted | — |
| E8 | Duplicate | Only after a recorded dedup/version decision. A-4 (secondary version → E8) is **deferred** until D-030 is decided; until then both records of a possible-duplicate pair are screened |
| E9 | Full text unavailable **and** abstract insufficient for extraction | — |
| E10 | Outside the query's date window (citation chasing / supplementary sources only) | — |
| E11 | Prediction target continuous only, no classification or risk-probability output — RQ1 | — |
| E12 | Not relevant to any RQ (catch-all) | Justification mandatory; audited at 100 % in the pilot |

Sample size, journal, country and model type are **not** exclusion criteria.

---

## 2. Scope definitions

### 2.1 Metabolic-disorder scope (D-056; Q-001 answered)
**In scope:** type 1, type 2 and gestational diabetes; prediabetes / impaired glucose regulation; insulin resistance; metabolic syndrome; NAFLD/MASLD/NASH/MASH; dyslipidaemias; hyperuricaemia and gout; inborn errors of metabolism (incl. newborn-screening targets).

**Pending (included at screening, flagged `scope_pending`):** obesity (as a classification target), thyroid dysfunction, polycystic ovary syndrome. Decided later without re-screening. (The ballot's proposed rename to `scope_pending_disorder` is not decided; v1.0's flag name is kept.)

**Out of scope (E4), subject to the §1 E4 clarification:** complications of metabolic disease when the classification target is the complication itself (e.g., diabetic retinopathy, nephropathy, foot ulcer); cardiovascular events, cancer and infectious disease.

This defines the literature-screening scope only. It does not decide the primary disorder (D-013) or any experimental scope.

### 2.2 Biochemical-biomarker scope (D-043, D-057, D-058)
**In scope (two distinct strands, D-043):**
* **Metabolomics / lipidomics:** targeted or untargeted; MS- or NMR-based; any biofluid or tissue. **Newborn-screening MS/MS** profiles (amino acids, acylcarnitines) are reported with this strand (D-058).
* **Routine clinical chemistry and laboratory values:** e.g., glucose, HbA1c, lipid panel, liver enzymes, renal markers, insulin/C-peptide, uric acid; complete blood count when combined with chemistry.
* **Mixed feature sets:** clinical variables combined with biochemical markers, provided the biochemical markers are a substantive part of the model input (stated, or ≥ 1 biochemical marker among the final predictors).

**Pending (included at screening, flagged `scope_pending_proteomics`, D-057):** proteomics and other protein-biomarker panels (e.g., cytokines). Multi-omics studies with a substantive metabolomics layer stay eligible whatever is decided.

**Out of scope (E3):** imaging-only; genomics, transcriptomics or methylation-only; microbiome-only; free text-only; CGM/wearable time series only; questionnaire-only.

**Content field (D-058):** every `include`/`uncertain` record gets `biomarker_class` = `metabolomics_lipidomics` / `newborn_screening_msms` / `routine_chemistry` / `mixed_both` / `other` / `unclear`, from what the study used, never from the retrieving query. Reporting: `mixed_both` appears in both strand tables and as its own row; overall totals count each record once.

### 2.3 Machine-learning scope — unchanged from v1.0
Supervised classification or risk-probability models: regularised regression; PLS-DA/OPLS-DA used as classifiers; tree ensembles, SVM, k-NN, naive Bayes, neural networks, AutoML, tabular foundation models. Classical logistic-regression-only studies are included only for RQ3/RQ4 methodological relevance or as comparators (`lr_only`).

---

## 3. RQ-specific criteria

| RQ | Include when | Specific exclusions |
|---|---|---|
| RQ1 | Meets §2.1 + §2.2 + §2.3; diagnosis/screening/classification/subtyping or risk prediction of a metabolic disorder (prognostic models flagged `prognostic`) | E1–E4, E11 |
| RQ2 | (a) Methodological work on explanation methods for tabular or omics classifiers (any biomedical domain), incl. stability, faithfulness or agreement of attributions; **or** (b) RQ1-eligible study that reports and interprets an explanation method | "Feature importance" without stating how it was computed → E12 unless otherwise RQ1-eligible |
| RQ3 | (a) Methodological work on calibration, recalibration, conformal prediction or other uncertainty quantification for classification/risk models, preferably tabular biomedical data; **or** (b) RQ1-eligible study reporting calibration or uncertainty | Image-only or NLP-only UQ papers excluded unless directly applicable to tabular classifiers (judgement recorded) |
| RQ4 | (a) RQ1-eligible study with external, temporal or cross-cohort validation; **or** (b) methodological work on external validation, transportability, dataset shift, batch/site effects | Internal validation only → not RQ4 (may remain RQ1) |
| RQ5 | Proposes or evaluates an integrated pipeline/framework covering **at least 4 of 5** separate components — (1) biomarker/feature selection; (2) classification; (3) explainability; (4) probability calibration; (5) uncertainty estimation — for biomarker/omics/clinical tabular data (D-031). A component counts only when applied or evaluated with a documented output (D-033, D-035 §2), confirmed at full text (D-035 G3). Coverage groups `qualified` (≥ 4), `near_rq5` (exactly 3), `below_threshold` (0–2) are derived, never assigned (D-034, D-036, D-037, D-038). `qualified`/`near_rq5` records are verified by the researcher (D-035 G4) | — Any domain is retained as closest prior art, tagged with domain; non-metabolic frameworks with ≥ 3 possible components are retained under D-055 |
| RQ6 | Systematic/scoping reviews, meta-research, reporting guidelines, risk-of-bias tools, or empirical studies of methodological pitfalls relevant to biomarker/omics/clinical ML | Narrative reviews without methodological content → `review_lead` only |

---

## 4. Decision procedure

```
Record (within the D-044 scope)
 ├─ Stage 0 (automatic, rule-based, counted; screener = rule:stage0):
 │     PubMed type Editorial, Comment, News, Published Erratum → E5; Retracted Publication → E7
 ├─ Stage 1 (title/abstract):
 │    ├─ clearly meets ≥ 1 RQ → INCLUDE (RQ tags, tier, required descriptors §6)
 │    ├─ clearly fails all RQs → EXCLUDE (first applicable code + one-line justification)
 │    └─ insufficient information → UNCERTAIN → full text (required descriptors §6)
 └─ Stage 2 (full text): INCLUDE / EXCLUDE (code) / ABSTRACT_ONLY (full text unavailable but abstract supports extraction)
```
* **When in doubt, include at Stage 1.** Exclusion requires a positive reason stated in the title/abstract.
* **Silence is never `no`** (D-060 (2)): absence of mention is not evidence that a method is absent.
* **Missing abstract** (title/abstract stage only; 6 records in the D-044 scope; D-060 (2) as amended by D-068; D-059 A-6): `uncertain` → full text, unless a Stage-0 rule exclusion (E5/E7, from source publication types) applies or the title alone clearly meets E1 as worded in the frozen §1, including its RQ limitations. **E4 is not applied because an abstract is missing.** Method descriptors and `validation_design` = `unclear`; `biomarker_class` = `unclear` unless explicitly supported by the title. All five preliminary component statuses are `unclear` with justification "no abstract". `rq_tags` (RQs the record could inform) and `record_type` are provisional and are confirmed or corrected at full text. No RQ5-based tier (§5; D-068 (7)). Missing information never gives `yes`, `include` or a confirmed classification. A record whose abstract was *not retrieved* is not treated as having an *unavailable* abstract; retrieval comes first where feasible (D-068 (8), (9)). Enforced by the screener with researcher review of every such decision (D-068 (10)).
* **RQ5 routing** (D-060 (4)): at title/abstract, descriptors are triage only and never count toward D-031/D-034 (D-035 G2). A record goes to full text (`uncertain`, `needs_human=yes`) if counting its `unclear` components as `yes` would give **three or more** of the five components, including records retained under D-055. Coverage groups use full-text-confirmed statuses only.
* **Human-review triggers** (`needs_human=yes`, D-060 (3)): (1) a term with two possible meanings not settled by the abstract ("calibration", "ensemble", "interpretable", "validation cohort"); (2) an otherwise RQ4-eligible record with `validation_design=unclear`; (3) any record routed under the RQ5 rule above; (4) a record without an abstract retained as `uncertain`; (5) any descriptor disagreement between the two pilot screeners.
* Uncertain records go forward to full text; they are never silently dropped.
* Any change to these criteria after screening starts is logged in `logs/DECISION_LOG.md` as a new criteria version, and affected records are re-screened.

## 5. Tiering for full-text priority
| Tier | Definition |
|---|---|
| 1 | RQ1-eligible and addresses ≥ 2 of {explainability, calibration/uncertainty, external validation}; records whose preliminary statuses could reach the D-031 threshold (≥ 4 components counting `unclear` as `yes`); reporting guidelines/RoB tools |
| 2 | Methodological papers for RQ2–RQ4; RQ1-eligible studies addressing exactly one of the three aspects |
| 3 | Other RQ1-eligible studies (coded from the abstract; full text read for a random sample only) |

**RQ5 tier rule (D-062, title/abstract only).** For records to which the D-060 (4) routing rule is applied, preliminary statuses are recorded for all five components (`dim_feature_selection`, `dim_classification` with written justification, and the three method descriptors). y = `yes` count, u = `unclear` count: y + u ≥ 4 → Tier 1; y + u = 3 → Tier 2 (full text guaranteed by D-060 (4)) unless another Tier 1 criterion applies; y + u ≤ 2 → no RQ5-based tier. The highest applicable tier is recorded. Tiers do not apply at full text. **Records without an abstract** receive no RQ5-based tier: their five preliminary statuses are `unclear` with justification "no abstract", and they are read at full text (D-068 (7)).

## 6. Screening record format (D-027 limited; D-059 A-5; D-028; D-029; D-058; D-060)
One file, `research/literature/screening/decisions.csv`, with `stage` = `title_abstract` / `full_text` (D-027).

| Column | Required? | Values / rule | Governing decision |
|---|---|---|---|
| `paper_id`, `stage`, `decision`, `reason_code`, `screener`, `date`, `justification` | Always | `decision` = `include/exclude/uncertain/abstract_only` (`abstract_only` at full text only); `reason_code` = E1–E12 for `exclude` | D-027 (approved, limited) |
| `rq_tags` | `include`, `uncertain` | RQ1–RQ6 | D-060 (6) |
| `record_type` | `include`, `uncertain` | `original / methodological / software / guideline / review_lead / other` | D-028 2d; D-060 (6) |
| `biomarker_class` | `include`, `uncertain` | §2.2 | D-058; D-060 (6) |
| `dim_explainability`, `dim_uncertainty`, `dim_calibration` | `include`, `uncertain` | `yes / no / unclear` (triage meaning at title/abstract) | D-029; D-060 (5), (6) |
| `validation_design` | `include`, `uncertain` | `external / temporal / internal_only / none / not_applicable / unclear`; strongest stated | D-029; D-060 (1) |
| `dim_feature_selection`, `dim_classification` | Full-text RQ5 assessment: all five component columns; at title/abstract whenever the RQ5 routing rule is applied (preliminary, triage only) | D-032, D-035 §2, D-036 | D-035 G5; D-062 |
| `scope_flags` | When applicable | `scope_pending`, `scope_pending_proteomics`, `lr_only`, `prognostic`, `non_metabolic_method_exemplar`, `non_metabolic_rq5_candidate` | D-055, D-056, D-057, D-061 |
| `tier`, `needs_human`, `criteria_version` | `tier` for `include`; `needs_human` per §4 triggers; `criteria_version` always once frozen | — | D-060 (3) |

Exceptions: Stage-0 rule rows (`screener=rule:stage0`; only `exclude` rows with E5 or E7, D-068 (5)) need only the always-required columns. `exclude` rows may leave descriptors empty. `publication_type` is derived by the build from source metadata via the D-028 mapping table (never hand-edited; arXiv → `preprint`; no URL/DOI-prefix rules). The schema currently names `dim_independent_validation`; it is replaced by `validation_design` when D-029 is implemented (implementation pending).

## 7. Pilot and audit
* **Pilot:** `screening_protocol_v0.2_draft.md` §7 (D-025, A-1). The v1.0 §7 pilot (first 30 PMIDs of Q-PM-01 and Q-PM-09) is **replaced** once this version is frozen and A-1's conditions are met.
* **Audit (D-008):** after the first expansion batches, the researcher blind-audits 25 `include` + 25 `exclude` decisions; κ < 0.60 or a wrongful exclusion triggers clarification and re-screening of affected records.

## 8. Not decided by these criteria
Primary disorder (D-013), primary dataset, outcome definition (D-014), evaluation protocol (D-019), research contribution (D-016), novelty: none is implied by any rule here. Inclusion in screening says nothing about study quality or novelty.

## 9. Traceability: changes from v1.0
| § | Change | Governing decision | Status of the decision |
|---|---|---|---|
| Header, §0 | Applies to the 1,470-record D-044 scope | D-044; D-009 | APPROVED — CONDITIONAL (inactive) |
| §1 E3, E5, E6, E8, E12 | Clarifications | D-059 (A-2) | APPROVED (as modified), inactive |
| §1 E4 | Exemplar and D-055 exceptions; flag name | D-059 (A-2 modified); D-055; D-061 | APPROVED, inactive; D-061 effective at freeze |
| §1 E8 | Version handling deferred | D-059 (A-4 deferred); D-030 | DEFERRED / PROPOSED |
| §2.1 | Main list approved; pending conditions kept | D-056 | APPROVED — CONDITIONAL (inactive) |
| §2.2 | Two strands; NBS MS/MS with metabolomics; proteomics pending; `biomarker_class` | D-043; D-057; D-058 | APPROVED; APPROVED — CONDITIONAL (inactive) |
| §3 RQ5 | ≥ 4 of 5 components; evidence standard; coverage groups; researcher verification; D-055 retention | D-031–D-038; D-055 | APPROVED — CONDITIONAL (inactive) |
| §4 | Silence ≠ `no`; missing abstracts; RQ5 routing; triggers | D-060 (2) as amended by D-068, (3), (4); D-059 (A-6); D-068; D-035 G2, G3 | APPROVED — CONDITIONAL (inactive) |
| §5 | RQ5 tier rule | D-031; D-060; D-062 (not applied without an abstract, D-068 (7)) | APPROVED — CONDITIONAL; D-062 and D-068 (7) effective at freeze |
| §6 | One file, required/optional columns, new fields, exemptions | D-027 (limited); D-059 (A-5); D-028; D-029; D-058; D-060 (6) | APPROVED / APPROVED — CONDITIONAL; implementation pending |
| §7 | Pilot replaced; audit; allocation | D-025; D-059 (A-1); D-063; D-008 | APPROVED — CONDITIONAL (inactive) |
| §1 I-C1–I-C4, E1, E2, E7, E9–E11, §2.3, RQ1–RQ4, RQ6 | Unchanged | — | — |

## 10. Open items to settle before the freeze
| ID | Item | Proposed resolution (not approved) |
|---|---|---|
| OPEN-1 | Name of the D-055 flag | Settled: D-061 (`non_metabolic_rq5_candidate`), effective at freeze |
| OPEN-2 | Tier for records routed only as possible `near_rq5` | Settled: D-062 (Tier 2 rule), effective at freeze |
| Q-073 | Pilot stratification inside the D-044 scope | Settled: D-063 (near-equal allocation), conditional and inactive |
| Q-074 | Missing-abstract rule and its enforcement | Settled: D-068 (amends D-060 (2) and the application of D-062), conditional and inactive. At the freeze: verify the Stage-0 type list against its approved source (G1) and fix the E1 wording (G2) |
