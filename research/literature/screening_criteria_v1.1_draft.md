# Screening Criteria — version 1.1 (DRAFT)

| Field | Value |
|---|---|
| Task | SCREENING-PREREQ-DECISIONS-2 (2026-10-30; assistant draft) |
| Version | **1.1 — DRAFT for researcher review. NOT frozen. Not in force.** |
| Proposed `criteria_version` | `criteria_v1.1+protocol_v0.2` — **proposed identifier only, not a frozen or effective version** (proposed by the assistant at the researcher's request, 2026-11-01). It takes effect only through an explicit, approved freeze decision covering this text and protocol v0.2; the proposed procedure, which has not been executed, is in §11 |
| Replaces | `screening_criteria.md` v1.0 (2026-10-14, draft) **only when** the researcher approves and freezes this text as the pilot's `criteria_version` (D-035 record §6, condition 5). v1.0 is kept unchanged for traceability |
| Companion | `screening_protocol_v0.2_draft.md` (operational rules, pilot, audit trail) |
| Screening status | **INACTIVE.** No record has been screened, labelled or sampled |
| Governing decisions | D-008, D-009, D-012/D-023, D-024, D-025, D-027 (limited), D-028, D-029, D-031–D-038, D-043, D-044, D-055–D-062, D-068, D-069, D-070–D-076, D-077, D-078, D-079. Every change from v1.0 is traced in §9 |
| Wording rule | Only approved decisions are written as rules. Items still open are marked **[OPEN]** and listed in §10 |

Records are screened against the criteria of **the RQ strand(s) they could inform**. A record is included if it satisfies the criteria of at least one RQ. Its RQ tags are recorded.

---

## 0. Records to which these criteria apply
The **1,470** publication records defined by D-044 (records retrieved by G-1…G-7, Q-PM-01, Q-PM-02, Q-PM-03, Q-PM-11, Q-PM-12). **Inventory basis:** D-044 defined and counted this scope on `paper_inventory.json` SHA-256 `a509538d…f4a3` (commit `ffee9ec`, 2026-10-29); that historical basis is unchanged. The inventory was rebuilt later (commit `b81c4e7`, SHA-256 `e20ce77e…341f`; T2 rebuild, commit `bf0c579`, SHA-256 `b668dbde…d054`). The T2 log records identical `paper_id`s and order between `e20ce77e…` and `b668dbde…`; a read-only comparison of the committed inventories at `ffee9ec`, `b81c4e7` and `bf0c579` (2026-11-01; recorded in `logs/CHANGELOG.md`, PRE-FREEZE-CORRECTIONS, 2026-11-01) found the same 1,470 in-scope `paper_id`s in the same order in all three. The comparison covers record IDs and their order only and authorises no pilot draw. The three hashes differ because other fields changed, so they are **not interchangeable**: a hash identifies one file version only. The pilot records the SHA-256 of the inventory actually used at the draw (D-077 (5); protocol v0.2 §7). All 743 Q-PM-02 records are screened (D-009). The remaining inventory records are outside the approved screening scope; they are neither screened nor excluded, and the review reports the reduced scope (D-044).

## 1. Common criteria (all RQs)

### Inclusion (all must hold) — unchanged from v1.0
| Code | Criterion |
|---|---|
| I-C1 | Peer-reviewed journal article, peer-reviewed full conference paper, or preprint (preprints flagged; published version preferred when it exists) |
| I-C2 | Full text or an abstract sufficient for the extraction fields of the relevant RQ |
| I-C3 | English language |
| I-C4 | Original research, methodological/statistical paper, software/framework paper, reporting guideline or consensus statement. **Reviews** are included only as *lead sources* (`record_type=review_lead`) |

### Exclusion (first applicable code in numerical order is the primary reason; Stage-0 rows with both E7 and E5 take E7, §4 and D-074)
Codes E1–E12 are unchanged in number and meaning; the clarifications approved in D-059 (A-2, as modified) are added, and E1 is clarified by D-073 (its reason is unchanged).

| Code | Reason | Clarification (D-059, A-2; E1: D-073; E4 at full text: D-075; E5 and E7 for retraction notices: D-076) |
|---|---|---|
| E1 | Not human data (animal, cell-line, plant, environmental) — RQ1 and the RQ1-dependent strands RQ2b, RQ3b, RQ4a | Excludes a record only if it also fails RQ2a, RQ3a, RQ4b, RQ5 and RQ6 (§4: exclusion requires failing all RQs); applies to title-only decisions under D-068 (2)(b) with the same limits |
| E2 | No supervised predictive model or classifier developed, validated or evaluated | — |
| E3 | Input data are not biochemical biomarkers (§2.2) | Includes imaging-only and genetics-only inputs for RQ1/RQ2b/RQ4a |
| E4 | Target condition outside the metabolic-disorder scope (§2.1) | **Not applied** when the record is retained as `non_metabolic_method_exemplar` for RQ2–RQ5, **or** is a non-metabolic framework with three or more possible RQ5 components, which is flagged `non_metabolic_rq5_candidate` instead (D-055; name D-061). The flag never decides inclusion or exclusion by itself; other E-codes still apply. **At full text** the flag is reassessed (D-075): it applies only when `yes` + `unclear` ≥ 3 among the row's five component statuses; when it does not apply, this exception no longer applies on that basis, and E4 applies unless the record qualifies as `non_metabolic_method_exemplar` or meets another applicable RQ |
| E5 | Editorial, commentary, news, letter without original data, conference abstract only, study protocol without results, thesis, book chapter | Explicitly includes errata/correction notices, patents and dataset-only descriptors. Also retraction notices (`publication_type` = `retraction_notice`) excluded at manual screening; never at Stage 0 on the basis of the notice type; the justification names the retracted article's `paper_id` or states that the article is not in the inventory (D-076) |
| E6 | Not English | Only when the record itself is non-English (`language` ≠ `eng` and no English full text). Missing language is **not** E6 |
| E7 | Retracted | The retracted article itself (Stage 0 for *Retracted Publication*, D-074 (a)). Not applied to a retraction notice merely because it concerns a retracted article (D-076) |
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

**Pending (included at screening, flagged `scope_pending_disorder`, D-069):** obesity (as a classification target), thyroid dysfunction, polycystic ovary syndrome. Decided later without re-screening.

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

### 2.3 Machine-learning scope — unchanged from v1.0 except the `lr_only` tag note (D-069)
Supervised classification or risk-probability models: regularised regression; PLS-DA/OPLS-DA used as classifiers; tree ensembles, SVM, k-NN, naive Bayes, neural networks, AutoML, tabular foundation models. Classical logistic-regression-only studies are included only for RQ3/RQ4 methodological relevance or as comparators. They may be tagged `lr_only`, a descriptive tag only (D-069): it does not determine `dim_classification` or RQ5 counting; Q-042 remains open.

---

## 3. RQ-specific criteria

| RQ | Include when | Specific exclusions |
|---|---|---|
| RQ1 | Meets §2.1 + §2.2 + §2.3; diagnosis/screening/classification/subtyping or risk prediction of a metabolic disorder (`prognostic` tag deferred and outside the vocabulary, D-069; does not block the freeze, D-071; eligibility unchanged) | E1–E4, E11 |
| RQ2 | (a) Methodological work on explanation methods for tabular or omics classifiers (any biomedical domain), incl. stability, faithfulness or agreement of attributions; **or** (b) RQ1-eligible study that reports and interprets an explanation method | "Feature importance" without stating how it was computed → E12 unless otherwise RQ1-eligible |
| RQ3 | (a) Methodological work on calibration, recalibration, conformal prediction or other uncertainty quantification for classification/risk models, preferably tabular biomedical data; **or** (b) RQ1-eligible study reporting calibration or uncertainty | Image-only or NLP-only UQ papers excluded unless directly applicable to tabular classifiers (judgement recorded) |
| RQ4 | (a) RQ1-eligible study with external, temporal or cross-cohort validation; **or** (b) methodological work on external validation, transportability, dataset shift, batch/site effects | Internal validation only → not RQ4 (may remain RQ1) |
| RQ5 | Proposes or evaluates an integrated pipeline/framework covering **at least 4 of 5** separate components — (1) biomarker/feature selection; (2) classification; (3) explainability; (4) probability calibration; (5) uncertainty estimation — for biomarker/omics/clinical tabular data (D-031). A component counts only when applied or evaluated with a documented output (D-033, D-035 §2), confirmed at full text (D-035 G3). Coverage groups `qualified` (≥ 4), `near_rq5` (exactly 3), `below_threshold` (0–2) are derived, never assigned (D-034, D-036, D-037, D-038). `qualified`/`near_rq5` records are verified by the researcher (D-035 G4) | — Any domain is retained as closest prior art, tagged with domain; non-metabolic frameworks with ≥ 3 possible components are retained under D-055 (at full text: possible = status `yes` or `unclear`, `yes` + `unclear` ≥ 3 on the full-text row, D-075; this does not confirm three components, and coverage groups still use confirmed statuses only) |
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
* **Stage 0 scope** (protocol v0.1 §3 through D-025; D-068 (5)): letters are not auto-excluded; a letter is excluded only at manual screening, as E5 when it has no original data (§1). *Retraction of Publication* notices are not Stage-0 types (D-072): they are screened manually and, if excluded, coded E5 (§1; D-076); a record that also carries *Retracted Publication* is a Stage-0 E7 exclusion under D-074 (a). **Records with several source publication types** (D-074): (1) if the types include *Retracted Publication*, the record is a Stage-0 E7 exclusion whatever its other types, and E7 is its primary code even when an E5 type is also present (for Stage-0 rows only, an exception to the §1 numerical-order rule); (2) otherwise it is a Stage-0 E5 exclusion only if every type is a Stage-0 E5 type or a type the D-028 2a mapping keeps but does not use for the class (*Research Support…*, *Validation Study*, *Multicenter Study*, *Comparative Study*, *Observational Study*, *Randomized Controlled Trial*, *Clinical Trial* and its phases, *Evaluation Study*, *English Abstract*, *Historical Article*, *Video-Audio Media*); (3) any other combination (for example with *Journal Article*, *Letter* or an unrecognised type) is not excluded at Stage 0 and is screened normally.
* **When in doubt, include at Stage 1.** Exclusion requires a positive reason stated in the title/abstract.
* **Silence is never `no`** (D-060 (2)): absence of mention is not evidence that a method is absent.
* **Missing abstract** (title/abstract stage only; 6 records in the D-044 scope, classified as *unavailable — PubMed* under D-079 (R1: PubMed's "[Abstract not available]" placeholder; this does not establish that no abstract exists in any other source); D-060 (2) as amended by D-068; D-059 A-6): `uncertain` → full text, unless a Stage-0 rule exclusion (E5/E7, from source publication types) applies or the title alone clearly meets E1 as worded in the frozen §1, including its RQ limitations. **E4 is not applied because an abstract is missing.** Method descriptors and `validation_design` = `unclear`; `biomarker_class` = `unclear` unless explicitly supported by the title. All five preliminary component statuses are `unclear` with justification "no abstract". `rq_tags` (RQs the record could inform) and `record_type` are provisional and are confirmed or corrected at full text. No RQ5-based tier (§5; D-068 (7)). Missing information never gives `yes`, `include` or a confirmed classification. A record whose abstract was *not retrieved* is not treated as having an *unavailable* abstract; retrieval comes first where feasible (D-068 (8), (9)). Enforced by the screener with researcher review of every such decision (D-068 (10)).
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
| `scope_flags` | When applicable | `scope_pending_disorder` (D-056 conditions), `scope_pending_proteomics`, `non_metabolic_method_exemplar` (descriptive retention tag; may co-occur with `non_metabolic_rq5_candidate`, D-070; a record with both tags is counted once per count), `non_metabolic_rq5_candidate` (set at title/abstract, D-061; reassessed at full text: recorded on a `full_text` row, including verification and adjudication rows, only when `yes` + `unclear` ≥ 3, otherwise omitted with a justification; the title/abstract row is unchanged, D-075), `lr_only` (descriptive; Q-042 open). Each token at most once per value (D-078). `prognostic`: deferred, not accepted; does not block the freeze (D-071) | D-056; D-057; D-059 (A-2); D-061; D-069; D-070; D-071; D-075; D-078 |
| `tier`, `needs_human`, `criteria_version` | `tier` for `include`; `needs_human` per §4 triggers; `criteria_version` always once frozen | — | D-060 (3) |

Exemption (D-060 (6) as clarified by D-068 (5)): the descriptor requirement does not apply to Stage-0 rule rows, which are `exclude` rows with reason code E5 or E7 and `screener=rule:stage0`; these need only the always-required columns. The exemption covers only such rows: an `include` or `uncertain` row at title/abstract always needs the descriptors, whatever its screener. This rule sets the exemption's scope only; it does not restrict which rows may carry `screener=rule:stage0` (Option A, as implemented by the validator; researcher direction 2026-11-01). `exclude` rows may leave descriptors empty. `publication_type` is derived by the build from source metadata via the D-028 mapping table (never hand-edited; arXiv → `preprint`; no URL/DOI-prefix rules). Screening rows use `validation_design` (D-029 as specified in D-060 (1)); `dim_independent_validation` is a retired screening column that is rejected and never converted. In the generated inventory the screening value appears as `screening_validation_design`; the former inventory column `dim_independent_validation` was removed from generated outputs and schemas in the T2 rebuild (2026-11-01, commit `bf0c579`).

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
| §1 E1 | Clarification: RQ1-dependent strands named (RQ2b, RQ3b, RQ4a; "RQ4-applications" renamed RQ4a); excludes only when RQ2a, RQ3a, RQ4b, RQ5 and RQ6 also fail; same limits for title-only E1 under D-068 (2)(b) | D-073 | APPROVED — CONDITIONAL (inactive); effective at freeze |
| §1 E8 | Version handling deferred | D-059 (A-4 deferred); D-030 | DEFERRED / PROPOSED |
| §2.1 | Main list approved; pending conditions kept; tag renamed `scope_pending_disorder` | D-056; D-069 | APPROVED — CONDITIONAL (inactive) |
| §2.2 | Two strands; NBS MS/MS with metabolomics; proteomics pending; `biomarker_class` | D-043; D-057; D-058 | APPROVED; APPROVED — CONDITIONAL (inactive) |
| §3 RQ5 | ≥ 4 of 5 components; evidence standard; coverage groups; researcher verification; D-055 retention | D-031–D-038; D-055 | APPROVED — CONDITIONAL (inactive) |
| §4 | Stage-0 scope note: letters not auto-excluded; retraction notices not Stage-0 types | Protocol v0.1 §3 (D-025); D-068 (5); D-072 | APPROVED — CONDITIONAL (inactive) |
| §1 heading; §4 | Stage-0 handling of records with several source types; E7 primary over E5 for Stage-0 rows | D-074 | APPROVED — CONDITIONAL (inactive); effective at freeze |
| §1 E4; §3 RQ5; §6 | `non_metabolic_rq5_candidate` reassessed at full text (possible = `yes` or `unclear`; flag only when ≥ 3); E4 exception lapses on that basis otherwise | D-075 | APPROVED — CONDITIONAL (inactive); effective at freeze |
| §1 E5, E7; §4 | Retraction notices: manual screening, E5 if excluded, justification names the retracted article; E7 stays with the retracted article | D-076 | APPROVED — CONDITIONAL (inactive); effective at freeze |
| §4 | Silence ≠ `no`; missing abstracts; RQ5 routing; triggers | D-060 (2) as amended by D-068, (3), (4); D-059 (A-6); D-068; D-035 G2, G3 | APPROVED — CONDITIONAL (inactive) |
| §5 | RQ5 tier rule | D-031; D-060; D-062 (not applied without an abstract, D-068 (7)) | APPROVED — CONDITIONAL; D-062 and D-068 (7) effective at freeze |
| §6 | One file, required/optional columns, new fields, exemptions | D-027 (limited); D-059 (A-5); D-028; D-029; D-058; D-060 (6); D-069, D-070, D-071 (`scope_flags` vocabulary); D-078 | APPROVED / APPROVED — CONDITIONAL; implemented (commits `d1aaceb`, `2fcc7b9`; generated outputs rebuilt in T2, `bf0c579`) |
| §7 | Pilot replaced; audit; allocation | D-025; D-059 (A-1); D-063; D-008 | APPROVED — CONDITIONAL (inactive) |
| §2.3; §3 RQ1 | `lr_only` descriptive-tag note (§2.3); `prognostic` tag deferred, eligibility unchanged, does not block the freeze (§3 RQ1) | D-069; D-071 | APPROVED — CONDITIONAL (inactive) |
| §6 | Stage-0 exemption worded as its scope (Option A, matching the validator); T2 sentence updated; `scope_flags` tokens at most once per value | D-060 (6); D-068 (5); D-078 | APPROVED — CONDITIONAL (inactive); D-078 APPROVED (implementation decision) |
| §4 | Six records without an abstract classified *unavailable — PubMed* (R1) | D-079 | APPROVED — CONDITIONAL (inactive) |
| Header | Proposed `criteria_version` identifier (not in force) | Proposed by the assistant at the researcher's request (2026-11-01) | Proposed |
| §1 I-C1–I-C4, E2, E7, E9–E11, RQ2–RQ4, RQ6 | Unchanged | — | — |

## 10. Open items to settle before the freeze
| ID | Item | Proposed resolution (not approved) |
|---|---|---|
| OPEN-1 | Name of the D-055 flag | Settled: D-061 (`non_metabolic_rq5_candidate`), effective at freeze |
| OPEN-2 | Tier for records routed only as possible `near_rq5` | Settled: D-062 (Tier 2 rule), effective at freeze |
| Q-073 | Pilot stratification inside the D-044 scope | Settled: D-063 (near-equal allocation), conditional and inactive |
| Q-074 | Missing-abstract rule and its enforcement | Settled: D-068 (amends D-060 (2) and the application of D-062), conditional and inactive. G1: Stage-0 type list compared with protocol v0.1 §3 on 2026-10-31 (read-only V11-FREEZE-READINESS report): identical; re-verified 2026-11-01 (FREEZE-DRAFT-CORRECTIONS): the same five types and E5/E7 codes in protocol v0.1 §3, D-068 (5) and both drafts. Protocol v0.1 §3 is the approved source through D-025 ("Stage-0 handling", APPROVED — CONDITIONAL, inactive), whose approval cell does not enumerate the list. The researcher directed confirmation (2026-11-01); the explicit confirmation required at the v1.1 freeze (D-068 (5)) is completed only by the freeze record [OPEN]. G2: settled by D-073 (E1 clarified, §1) |
| Q-075 | `scope_flags` vocabulary | Settled: D-069 (`scope_pending_disorder`, `non_metabolic_method_exemplar`, `lr_only`); D-070 (the two non-metabolic tags may co-occur; counted once per count); D-071 (`prognostic` deferred, not in the vocabulary, does not block the freeze); conditional and inactive |
| Q-078 | Full-text handling of `non_metabolic_rq5_candidate` when fewer than three possible components remain | Settled: D-075, conditional and inactive; rule in §1 E4, §3 RQ5 and §6 |
| Q-079 | Code for retraction notices at manual screening (not Stage 0, D-072) | Settled: D-076, conditional and inactive; rule in §1 E5/E7 and §4. Notice-to-article linking stays with D-030 (PROPOSED) |
| Q-080 | Stage-0 handling of records with several source publication types (H4; recording stopped because of a conflict with D-028 2a) | Settled: D-074 (approved with the E7-precedence clarification), conditional and inactive; rule in §4 |

## 11. Proposed freeze procedure (not executed; nothing here is approved)
The identifier `criteria_v1.1+protocol_v0.2` is proposed only. It becomes effective only through step 6; until then this text and protocol v0.2 are drafts and not in force.
1. The researcher reviews the final content of this text and of protocol v0.2 and explicitly approves it.
2. The researcher explicitly confirms the Stage-0 type list and its E5/E7 codes against protocol v0.1 §3 (D-068 (5); §10 Q-074).
3. The final file names and status wording are settled **before** the freeze commit. **[OPEN — researcher decision]:** whether the files keep their `_draft` names or are renamed, the exact final status wording, and whether `screening_criteria.md` v1.0 and `screening_protocol.md` v0.1 receive a superseded note.
4. The final contents of both files are committed.
5. The SHA-256 of each file is computed from the exact contents at that commit.
6. A separate `logs/DECISION_LOG.md` entry records the identifier, both final paths, the commit, both SHA-256 values, the researcher's explicit approval and the effective date. Neither file contains its own final hash or commit; the decision-log entry holds them, which avoids a self-referential hash.
7. Only that approved entry makes the identifier effective. Recording D-035 record §6 conditions as met, authorising the pilot draw (D-077 (6)) and authorising screening remain separate later decisions.
