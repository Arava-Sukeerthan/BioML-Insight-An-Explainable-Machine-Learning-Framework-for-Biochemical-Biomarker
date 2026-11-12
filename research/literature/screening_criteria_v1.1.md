# Screening Criteria — version 1.1 (DRAFT)

| Field | Value |
|---|---|
| Task | SCREENING-PREREQ-DECISIONS-2 (2026-10-30; assistant draft) |
| Version | **FROZEN** — approved 2026-11-11; effective 2026-11-11; freeze entry D-110. Screening also requires the D-035 §6 records and run authorisations. |
| `criteria_version` | `criteria_v1.1+protocol_v0.2` (D-103). It takes effect only through the freeze entry and the criteria registry (§11 steps 9 and 9a); until then it is not an effective version |
| Replaces | `screening_criteria.md` v1.0 (2026-10-14, draft) **only when** the researcher approves and freezes this text as the pilot's `criteria_version` (D-035 record §6, condition 5). v1.0 is kept unchanged for traceability |
| Companion | `screening_protocol_v0.2.md` (operational rules, pilot, audit trail) |
| Screening status | **INACTIVE.** No record has been screened, labelled or sampled |
| Governing decisions | D-008, D-009, D-012/D-023, D-024, D-025, D-027 (limited), D-028, D-029, D-031–D-038, D-043, D-044, D-055–D-062, D-068, D-069, D-070–D-076, D-077, D-078, D-079, D-080–D-084; Phase 1 tools and run authorisation D-085–D-088; Stage B preparation, approvals and audit decisions D-089–D-107 and D-109 (2026-11-11; D-108 is a proposal only). Every change from v1.0 is traced in §9 |
| Wording rule | Only approved decisions are written as rules. Items still open are marked **[OPEN]** where they affect a rule; §10 lists the pre-freeze items, and the freeze entry lists every open question and open proposal referred to in this text or protocol v0.2 (§11 step 5) |

Records are screened against the criteria of **the RQ strand(s) they could inform**. A record is included if it satisfies the criteria of at least one RQ. Its RQ tags are recorded.

---

## 0. Records to which these criteria apply
The **1,470** publication records defined by D-044 (records retrieved by G-1…G-7, Q-PM-01, Q-PM-02, Q-PM-03, Q-PM-11, Q-PM-12). **Inventory basis:** D-044 defined and counted this scope on `paper_inventory.json` SHA-256 `a509538d…f4a3` (commit `ffee9ec`, 2026-10-29); that historical basis is unchanged. The inventory was rebuilt later (commit `b81c4e7`, SHA-256 `e20ce77e…341f`; T2 rebuild, commit `bf0c579`, SHA-256 `b668dbde…d054`). The T2 log records identical `paper_id`s and order between `e20ce77e…` and `b668dbde…`; a read-only comparison of the committed inventories at `ffee9ec`, `b81c4e7` and `bf0c579` (2026-11-01; recorded in `logs/CHANGELOG.md`, PRE-FREEZE-CORRECTIONS, 2026-11-01) found the same 1,470 in-scope `paper_id`s in the same order in all three. The comparison covers record IDs and their order only and authorises no pilot draw. The three hashes differ because other fields changed, so they are **not interchangeable**: a hash identifies one file version only. The inventory is to be fixed in a separate decision-log entry before D-035 record §6 condition 6 is recorded (D-107, approved in principle, subject to verification; the exact order is the proposal D-108), and the pilot records its SHA-256 again at the draw (D-077 (5); protocol v0.2 §7). All 743 Q-PM-02 records are screened (D-009). The remaining inventory records are outside the approved screening scope; they are neither screened nor excluded, and the review reports the reduced scope (D-044).

## 1. Common criteria (all RQs)

### Inclusion (all must hold) — unchanged from v1.0
| Code | Criterion |
|---|---|
| I-C1 | Peer-reviewed journal article, peer-reviewed full conference paper, or preprint (preprints flagged; published version preferred when it exists) |
| I-C2 | Full text or an abstract sufficient for the extraction fields of the relevant RQ |
| I-C3 | English language |
| I-C4 | Original research, methodological/statistical paper, software/framework paper, reporting guideline or consensus statement. **Reviews** are included only as *lead sources* (`record_type=review_lead`). This includes systematic and scoping reviews that inform RQ6: they are coded `record_type=review_lead` and may carry the `rq_tags` value RQ6 |

### Exclusion (first applicable code in numerical order is the primary reason, D-080; Stage-0 rows with both E7 and E5 take E7, §4 and D-074 (d))
Codes E1–E12 are unchanged in number and meaning; the clarifications approved in D-059 (A-2, as modified) are added, and E1 is clarified by D-073 (its reason is unchanged).

| Code | Reason | Clarification (D-059, A-2; E1: D-073; E4 at full text: D-075; E5 and E7 for retraction notices: D-076) |
|---|---|---|
| E1 | Not human data (animal, cell-line, plant, environmental) — RQ1 and the RQ1-dependent strands RQ2b, RQ3b, RQ4a | Excludes a record only if it also fails RQ2a, RQ3a, RQ4b, RQ5 and RQ6 (§4: exclusion requires failing all RQs); applies to title-only decisions under D-068 (2)(b) with the same limits |
| E2 | No supervised predictive model or classifier developed, validated or evaluated | Applies to RQ1 and the RQ1-dependent strands (RQ2b, RQ3b, RQ4a); excludes a record only if it also fails every other RQ (§4: exclusion requires failing all RQs) |
| E3 | Input data are not biochemical biomarkers (§2.2) | Includes imaging-only and genetics-only inputs for RQ1/RQ2b/RQ4a. As for E1 and E2, excludes a record only if it also fails every other RQ (§4: exclusion requires failing all RQs) |
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

**Primary code (D-080; Q-081).** When several exclusion codes apply to a record, the first applicable code in numerical order is the primary reason. Exception (D-074 (d)): a Stage-0 row that qualifies for both E7 and E5 takes E7. The general rule was stated in v1.0 §1 and protocol v0.1 §5 without an approved decision (D-074 status) until D-080 adopted it (researcher approval, 2026-11-01).

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
| RQ6 | Systematic/scoping reviews, meta-research, reporting guidelines, risk-of-bias tools, or empirical studies of methodological pitfalls relevant to biomarker/omics/clinical ML | Narrative reviews without methodological content → `review_lead` only. Systematic and scoping reviews are also coded `review_lead` (I-C4) and may be tagged RQ6 |

---

## 4. Decision procedure

```
Record (within the D-044 scope)
 ├─ Stage 0 (automatic, rule-based, counted; screener = rule:stage0):
 │     PubMed type Editorial, Comment, News, Published Erratum → E5; Retracted Publication → E7
 ├─ Stage 1 (title/abstract):
 │    ├─ clearly meets ≥ 1 RQ → INCLUDE (RQ tags, tier, required descriptors §6)
 │    ├─ clearly fails all RQs → EXCLUDE (first applicable code in numerical order, D-080 + one-line paraphrased justification, D-089)
 │    └─ insufficient information → UNCERTAIN → full text (required descriptors §6)
 └─ Stage 2 (full text): INCLUDE / EXCLUDE (code) / ABSTRACT_ONLY (full text unavailable but abstract supports extraction)
```
* **Stage 0 scope** (protocol v0.1 §3 through D-025; D-068 (5)). **List status:** approved conditionally through protocol v0.1 §3 (D-025, whose approval cell does not enumerate the types) and accepted provisionally by D-068 (5); confirmed by the researcher on 2026-11-01 against protocol v0.1 §3 (D-082). Because D-068 (5) requires the confirmation at the v1.1 freeze, it is restated in the freeze entry (§11). Letters are not auto-excluded; a letter is excluded only at manual screening, as E5 when it has no original data (§1). *Retraction of Publication* notices are not Stage-0 types (D-072): they are screened manually and, if excluded, coded E5 (§1; D-076); a record that also carries *Retracted Publication* is a Stage-0 E7 exclusion under D-074 (a). **Records with several source publication types** (D-074): (1) if the types include *Retracted Publication*, the record is a Stage-0 E7 exclusion whatever its other types, and E7 is its primary code even when an E5 type is also present (for Stage-0 rows only; D-074 (d), an exception to the §1 numerical-order rule, D-080); (2) otherwise it is a Stage-0 E5 exclusion only if every type is a Stage-0 E5 type or a type the D-028 2a mapping keeps but does not use for the class (*Research Support…*, *Validation Study*, *Multicenter Study*, *Comparative Study*, *Observational Study*, *Randomized Controlled Trial*, *Clinical Trial* and its phases, *Evaluation Study*, *English Abstract*, *Historical Article*, *Video-Audio Media*); (3) any other combination (for example with *Journal Article*, *Letter* or an unrecognised type) is not excluded at Stage 0 and is screened normally.
* **When in doubt, do not exclude at Stage 1: record `uncertain`, which sends the record to full text.** Exclusion requires a positive reason stated in the title/abstract.
* **Silence is never `no`** (D-060 (2)): absence of mention is not evidence that a method is absent.
* **Missing abstract** (title/abstract stage only; 6 records in the D-044 scope, classified as *unavailable — PubMed* under D-079 (R1: PubMed's "[Abstract not available]" placeholder; this does not establish that no abstract exists in any other source); D-060 (2) as amended by D-068; D-059 A-6): `uncertain` → full text, unless a Stage-0 rule exclusion (E5/E7, from source publication types) applies or the title alone clearly meets E1 as worded in the frozen §1, including its RQ limitations. **E4 is not applied because an abstract is missing.** Method descriptors and `validation_design` = `unclear`; `biomarker_class` = `unclear` unless explicitly supported by the title. All five preliminary component statuses are `unclear` with justification "no abstract". `rq_tags` (RQs the record could inform) and `record_type` are provisional and are confirmed or corrected at full text. No RQ5-based tier (§5; D-068 (7)). Missing information never gives `yes`, `include` or a confirmed classification. A record whose abstract was *not retrieved* is not treated as having an *unavailable* abstract; retrieval comes first where feasible (D-068 (8), (9)). Enforced by the screener with researcher review of every such decision (D-068 (10)).
* **RQ5 routing** (D-060 (4)): at title/abstract, descriptors are triage only and never count toward D-031/D-034 (D-035 G2). A record goes to full text (`uncertain`, `needs_human=yes`) if counting its `unclear` components as `yes` would give **three or more** of the five components, including records retained under D-055. Coverage groups use full-text-confirmed statuses only.
* **Human-review triggers** (`needs_human=yes`, D-060 (3)): (1) a term with two possible meanings not settled by the abstract ("calibration", "ensemble", "interpretable", "validation cohort"); (2) an otherwise RQ4-eligible record with `validation_design=unclear`; (3) any record routed under the RQ5 rule above; (4) a record without an abstract retained as `uncertain`; (5) any descriptor disagreement between the two pilot screeners.
* Uncertain records go forward to full text; they are never silently dropped. A full-text `uncertain` row is listed in the adjudication queue and resolved through adjudication, recorded as a new row (protocol v0.2 §5 items 3 and 4).
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
| `paper_id`, `stage`, `decision`, `reason_code`, `screener`, `date`, `justification` | Always | `decision` = `include/exclude/uncertain/abstract_only` (`abstract_only` at full text only); `reason_code` = E1–E12 for `exclude`; `justification` = one line that paraphrases the decisive information, never a quotation from the abstract or other source text (decision files are committed to the public repository; D-089) | D-027 (approved, limited); D-089 |
| `rq_tags` | `include`, `uncertain` | RQ1–RQ6 | D-060 (6) |
| `record_type` | `include`, `uncertain` | `original / methodological / software / guideline / review_lead / other` | D-028 2d; D-060 (6) |
| `biomarker_class` | `include`, `uncertain` | §2.2 | D-058; D-060 (6) |
| `dim_explainability`, `dim_uncertainty`, `dim_calibration` | `include`, `uncertain` | `yes / no / unclear` (triage meaning at title/abstract) | D-029; D-060 (5), (6) |
| `validation_design` | `include`, `uncertain` | `external / temporal / internal_only / none / not_applicable / unclear`; strongest stated | D-029; D-060 (1) |
| `dim_feature_selection`, `dim_classification` | Full-text RQ5 assessment: all five component columns; at title/abstract whenever the RQ5 routing rule is applied (preliminary, triage only) | D-032, D-035 §2, D-036 | D-035 G5; D-062 |
| `scope_flags` | When applicable | `scope_pending_disorder` (D-056 conditions), `scope_pending_proteomics`, `non_metabolic_method_exemplar` (descriptive retention tag; may co-occur with `non_metabolic_rq5_candidate`, D-070; a record with both tags is counted once per count), `non_metabolic_rq5_candidate` (set at title/abstract, D-061; reassessed at full text: recorded on a `full_text` row, including verification and adjudication rows, only when `yes` + `unclear` ≥ 3, otherwise omitted with a justification; the title/abstract row is unchanged, D-075), `lr_only` (descriptive; Q-042 open). Each token at most once per value (D-078). `prognostic`: deferred, not accepted; does not block the freeze (D-071) | D-056; D-057; D-059 (A-2); D-061; D-069; D-070; D-071; D-075; D-078 |
| `tier`, `needs_human`, `criteria_version` | `tier` for `include`; `needs_human` per §4 triggers; `criteria_version` always once frozen (enforced from the freeze: the validator then requires every row to carry a version listed in `research/literature/criteria_registry.json`, which is created only at the freeze and cross-checked against the freeze entry; until then rows are validated as before; the schema keeps a format-only pattern; D-085 B2–B4, commit `7f5b608`) | — | D-060 (3) |

Exemption (D-060 (6) as clarified by D-068 (5)): the descriptor requirement does not apply to Stage-0 rule rows, which are `exclude` rows with reason code E5 or E7 and `screener=rule:stage0`; these need only the always-required columns. The exemption covers only such rows: an `include` or `uncertain` row at title/abstract always needs the descriptors, whatever its screener. This rule sets the exemption's scope only; it does not restrict which rows may carry `screener=rule:stage0` (Option A, as implemented by the validator; researcher direction 2026-11-01). `exclude` rows may leave descriptors empty. `publication_type` is derived by the build from source metadata via the D-028 mapping table (never hand-edited; arXiv → `preprint`; no URL/DOI-prefix rules). Screening rows use `validation_design` (D-029 as specified in D-060 (1)); `dim_independent_validation` is a retired screening column that is rejected and never converted. In the generated inventory the screening value appears as `screening_validation_design`; the former inventory column `dim_independent_validation` was removed from generated outputs and schemas in the T2 rebuild (2026-11-01, commit `bf0c579`).

## 7. Pilot and audit
* **Pilot:** `screening_protocol_v0.2.md` §7 (D-025, A-1). The v1.0 §7 pilot (first 30 PMIDs of Q-PM-01 and Q-PM-09) is **replaced** once this version is frozen and A-1's conditions are met.
* **Audit (D-008):** after the first expansion batches (exact timing [OPEN; Q-084]: D-008 sets none; protocol v0.1 §7 "Expansion" row says after the first two batches; see protocol v0.2 §8), the researcher blind-audits 25 `include` + 25 `exclude` decisions; κ < 0.60 or a wrongful exclusion triggers clarification and re-screening of affected records.

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
| Header | Proposed `criteria_version` identifier (not in force) | Proposed by the assistant at the researcher's request (2026-11-01) | Proposed (status when this row was written; the identifier was later approved as D-103, see the B1–B6 row below) |
| §1 note and heading; §4; §6; §7; §10; §11 | Pre-freeze reconciliation (2026-11-01): rules without an approved decision marked [OPEN] (general code precedence; audit timing); D-076 (8), Stage-0 timing and D-030 listed as open; Stage-0 list status stated; `criteria_version` enforcement gap stated; §10 heading corrected; file-name reference to D-035 §6 condition 5 explained. No approved rule changed; the general code-precedence rule, which no approved decision adopts, is now presented as a proposed convention | D-008; D-030; D-035 record §6; D-059; D-068 (5); D-074; D-076 | As stated per row |
| Header; §1 heading and note; §4; §7; §10; §11 | Pre-freeze decisions (2026-11-01): general primary-code rule adopted with the D-074 (d) exception; Stage-0 list confirmed; final file names; Q-082 to Q-084 kept open at the freeze; freeze procedure amended (approved in principle, to be reviewed before execution) | D-080; D-081; D-082; D-083; D-084 | D-080, D-082: APPROVED — CONDITIONAL (inactive for screening); D-081, D-083: APPROVED; D-084: APPROVED IN PRINCIPLE — amended procedure requires researcher review and approval before execution |
| Header; §4; §6; §10; §11 | Stage B preparation (2026-11-11): Phase 1 tools reflected (`criteria_version` enforced through the registry from the freeze; Stage-0 generator); justifications paraphrased only; Stage-0 timing settled (before the pilot draw); superseded notes on v1.0 and v0.1 at the freeze; D-035 §6 recording form and condition-6 scope referenced. **No inclusion or exclusion rule, RQ criterion, scope definition or threshold changed** | D-085; D-089; D-090; D-091; D-092; D-093; D-095 | D-089, D-093: APPROVED — CONDITIONAL (inactive for screening); D-090, D-091, D-092: APPROVED; D-085, D-095: APPROVED — implementation decision |
| §10; §11 | Pre-commit audit corrections (2026-11-11): §11 step 1 lists the later approved decisions and excludes assistant proposals; STAGE0-T notes the sampler's Stage-0 row check. No rule changed | D-093; D-095 | D-093: APPROVED — CONDITIONAL (inactive for screening); D-095: APPROVED — implementation |
| Header; §11 | Governance reconciliation (2026-11-11): D-090 timing confirmed; §11 step 1 distinguishes provisional decisions and proposals. No rule changed | D-090; D-097–D-102 | D-090: APPROVED; D-097–D-099: APPROVED — PROVISIONAL; D-100: APPROVED; D-101: APPROVED — CONDITIONAL; D-102: PROPOSED (statuses when this row was written; later, 2026-11-11: D-097 and D-099 final, D-098 final and conditional, D-102 APPROVED — CONDITIONAL with its revision pending; current statuses in `logs/DECISION_LOG.md`) |
| Header; §11 | Researcher approvals B1–B6 (2026-11-11): identifier (D-103); freeze-commit status wording and superseded notes (D-104, answering Q-088); §11 reviewed: registry step 9a added, freeze-commit contents (step 6), reserved freeze-entry ID (step 8) and open questions at the freeze (step 5) made explicit. No rule changed | D-103; D-104; D-084 | APPROVED (documentation decisions); D-084: APPROVED IN PRINCIPLE, final amended text submitted for approval |
| §4 | "When in doubt" rule restored to the approved operational rule: record `uncertain`, which sends the record to full text (protocol v0.1 §5 item 1, approved through D-025; protocol v0.2 §5 item 1); the v1.0 wording "include at Stage 1" is replaced. No other change | D-025; D-105 | APPROVED |
| §11 step 5 | Open questions and the open proposal to be listed in the freeze entry: Q-021, Q-042, Q-063, Q-064, Q-085, Q-092 (c), Q-096 and D-030, besides Q-082 to Q-084 | D-083; D-106 | APPROVED |
| §0; §11 step 5 | Governance-review corrections (2026-11-11): §0 states that the inventory is fixed before condition 6 (D-107) and recorded again at the draw; the freeze open-items list adds the proposal D-108 and the pending D-102 revision. No rule changed | D-106; D-107 | D-106: APPROVED; D-107: APPROVED IN PRINCIPLE |
| Header; §11 steps 1, 5, 10 | FINAL-PRE-FREEZE-AUDIT (2026-11-11): governing-decision range and §11 step 1 extended to the approved D-105–D-107 and D-109 (D-108 named as a proposal); wording rule describes where open items are listed; step 5 wording covers open proposals and pending items; step 10 restates the D-107 requirement for condition 6 (d). No rule changed | D-105; D-106; D-107; D-109 | As recorded |
| §11 step 5 | D1 (2026-11-11): Q-097 added to the open items listed in the freeze entry. No rule changed | D-106 | APPROVED |
| §0; §11 steps 1, 10 | PRE-FREEZE-GOVERNANCE-REVIEW (2026-11-11): D-107 described as approved in principle, subject to verification, wherever its requirement is stated; the exact order named as the proposal D-108. No rule changed | D-107; D-108 (proposed) | D-107: APPROVED IN PRINCIPLE; D-108: PROPOSED |
| §9 (two earlier rows) | FINAL-PRE-FREEZE-ISSUE-RESOLUTION (2026-11-11): the status cells of the `criteria_version` proposal row and the governance-reconciliation row marked as the statuses when those rows were written, with a pointer to the later statuses; the original text kept. No rule changed | D-097–D-099; D-102; D-103 | As recorded in `logs/DECISION_LOG.md` |
| §4; §11 | COMPLETION-BATCH-E (2026-11-11; researcher-approved mechanical corrections): §4 states that a full-text `uncertain` is resolved through adjudication (as protocol v0.2 §5 already provides); §11 states the execution order of its steps. No rule, code, threshold or RQ changed | D-084 (in principle); D-025 | As recorded |
| §1 I-C4, E2, E3; §3 RQ6 | Researcher decisions R7 (option (a)) and R8 (2026-11-11; researcher prompt "We are proceeding toward the documentation freeze." (2026-11-11)): systematic and scoping reviews informing RQ6 are coded `review_lead` and may be tagged RQ6; E2 and E3 carry the E1-style note that a record is excluded only if it also fails every other RQ (§4). Clarifications of existing rules: no rule, code, threshold or RQ changed. R1 and R5 recorded as limitations only, not in this text | I-C4 (unchanged); D-073 (E1 pattern); §4 | Content approval pending |
| §1 I-C1–I-C4, E2, E7, E9–E11, RQ2–RQ4, RQ6 | Unchanged | — | — |

## 10. Pre-freeze items: settled by decisions, and still open
A row marked *Settled* cites the approved decision that settles it (all are conditional and inactive for screening, as stated). A row marked **[OPEN]** is unresolved. Neither kind approves or freezes this draft.

| ID | Item | Resolution and status |
|---|---|---|
| OPEN-1 | Name of the D-055 flag | Settled: D-061 (`non_metabolic_rq5_candidate`), effective at freeze |
| OPEN-2 | Tier for records routed only as possible `near_rq5` | Settled: D-062 (Tier 2 rule), effective at freeze |
| Q-073 | Pilot stratification inside the D-044 scope | Settled: D-063 (near-equal allocation), conditional and inactive |
| Q-074 | Missing-abstract rule and its enforcement | Settled: D-068 (amends D-060 (2) and the application of D-062), conditional and inactive. G1: Stage-0 type list compared with protocol v0.1 §3 on 2026-10-31 (read-only V11-FREEZE-READINESS report): identical; re-verified 2026-11-01 (FREEZE-DRAFT-CORRECTIONS): the same five types and E5/E7 codes in protocol v0.1 §3, D-068 (5) and both drafts. Protocol v0.1 §3 is the approved source through D-025 ("Stage-0 handling", APPROVED — CONDITIONAL, inactive), whose approval cell does not enumerate the list. The researcher confirmed the list on 2026-11-01 (D-082); because D-068 (5) requires the confirmation at the v1.1 freeze, it is restated in the freeze entry (§11). G2: settled by D-073 (E1 clarified, §1) |
| Q-075 | `scope_flags` vocabulary | Settled: D-069 (`scope_pending_disorder`, `non_metabolic_method_exemplar`, `lr_only`); D-070 (the two non-metabolic tags may co-occur; counted once per count); D-071 (`prognostic` deferred, not in the vocabulary, does not block the freeze); conditional and inactive |
| Q-078 | Full-text handling of `non_metabolic_rq5_candidate` when fewer than three possible components remain | Settled: D-075, conditional and inactive; rule in §1 E4, §3 RQ5 and §6 |
| Q-079 | Code for retraction notices at manual screening (not Stage 0, D-072) | Settled: D-076, conditional and inactive; rule in §1 E5/E7 and §4. Notice-to-article linking stays with D-030 (PROPOSED) |
| Q-080 | Stage-0 handling of records with several source publication types (H4; recording stopped because of a conflict with D-028 2a) | Settled: D-074 (approved with the E7-precedence clarification), conditional and inactive; rule in §4 |
| PREC | Primary code when several codes apply | Settled: D-080 (first applicable code in numerical order; Q-081), with the D-074 (d) Stage-0 E7-over-E5 exception; conditional and inactive; rule in the §1 note |
| D-076 (8) | Manual coding of retracted **articles** that lack the PubMed *Retracted Publication* type | **[OPEN — researcher decision; Q-082]** (D-076 (8): "Not resolved"). Stage-0 E7 is triggered only by the source type *Retracted Publication* (D-074 (a)); a retraction **notice** (`retraction_notice`) is a different record, screened manually and coded E5 if excluded (D-076 (1)–(2)). Whether and how E7 is applied at manual screening to a retracted article without that source type is not decided; no automatic rule exists. Kept open at the v1.1 freeze (D-083); needed "Before such a record is screened (may stay open at the freeze if recorded as open)" (Q-082) |
| STAGE0-T | When Stage-0 rows are written after activation, and the tool that writes them | Settled: D-093 (Q-089): Stage-0 rows are written **before the pilot draw**, after D-035 record §6 is recorded and under a separate D-074 (f) authorisation in the D-088 form; tool `scripts/literature/stage0.py` (D-085 A1–A5), not yet run on the real inventory; the pilot sampler refuses to draw unless these rows exist with the approved codes; conditional and inactive (protocol v0.2 §3) |
| AUDIT-T | Timing of the D-008 audit | **[OPEN — researcher confirmation; Q-084]**: §7; protocol v0.2 §8. Kept open at the v1.1 freeze (D-083); needed "Before expansion screening" (Q-084) |
| D-030 | Duplicates and versions (E8; A-4; notice-to-article linking) | **[OPEN]**: D-030 PROPOSED; A-4 DEFERRED (D-059); until decided, both records of a pair are screened (§1 E8) |

## 11. Freeze procedure (amended under D-084; approved in principle; final amended text submitted for the researcher's approval before execution; not executed)
The researcher reviews and approves this amended procedure before it is executed (D-084). The identifier is `criteria_v1.1+protocol_v0.2` (D-103). It becomes effective only through the freeze entry (step 9) and the criteria registry (step 9a); until then this text and protocol v0.2 are drafts and not in force.

**Execution order.** The step numbers below are not chronological. The steps are carried out in this order: 1 (approved decisions written in) → 3 (the researcher's content approval) → 8 (freeze-entry ID and dates reserved) → 6 with 2 (freeze commit with the status wording and the superseded notes) → 7 (hashes from that commit) → 9 with 9a (freeze entry and criteria registry in one commit). Steps 4 and 5 state what the freeze entry contains; steps 10 and 11 state what the freeze does not do.
1. The approved decisions written into the texts (D-080 to D-107 and D-109, as recorded in `logs/DECISION_LOG.md`; D-107 is approved in principle only, subject to verification; D-108 is a proposal and is not written in as a rule) are written into both texts before final content approval. A decision that is still open is marked **[OPEN]** and does not block the freeze only if this procedure says so (step 5).
2. The final file names are `research/literature/screening_criteria_v1.1.md` and `research/literature/screening_protocol_v0.2.md` (D-081), reached by a rename commit that is separate from the freeze commit. D-035 record §6 condition 5 names "`screening_criteria.md` v1.1"; the freeze entry states that this refers to `screening_criteria_v1.1.md`. **Status wording (D-104):** in the freeze commit, the Version row of both texts reads "**FROZEN** — approved <date>; effective <date>; freeze entry D-nnn. Screening also requires the D-035 §6 records and run authorisations." **Superseded notes (D-090; D-104):** `screening_criteria.md` (v1.0) and `screening_protocol.md` (v0.1) keep their content unchanged and, in the freeze commit, receive the note "**SUPERSEDED** by `screening_criteria_v1.1.md` / `screening_protocol_v0.2.md` (frozen <date>, D-nnn); kept unchanged for traceability."
3. The researcher reviews the complete final text of this document and of protocol v0.2 (including its §7a, D-100) and explicitly approves it.
4. The freeze entry restates the researcher's Stage-0 confirmation (D-082; D-068 (5)).
5. The freeze entry lists the questions that remain open, with their restrictions as recorded in `research/reviews/unresolved_questions.md` ("Needed by"): Q-082, Q-083 and Q-084 (kept open at the freeze, D-083), and the other open questions, open proposals and pending items referred to in either text, each with its recorded restriction: Q-021, Q-042, Q-063, Q-064, Q-085, Q-092 (c), Q-096, Q-097, the proposals D-030 and D-108, and the pending revision of D-102 (D-106).
6. A dedicated freeze commit contains only: the final contents of both texts with the status wording of step 2 filled in, and the superseded notes on v1.0 and v0.1. No other file changes in that commit.
7. The SHA-256 of each of the two texts is computed from its exact committed contents at the freeze commit (`git show <commit>:<path>`).
8. Neither text contains its own final hash or commit; the freeze entry holds them, which avoids a self-referential hash. The freeze-entry ID (D-nnn) and the dates written in step 2 are fixed before the freeze commit.
9. A separate `logs/DECISION_LOG.md` freeze entry, with the reserved ID, records the identifier, both final paths, the freeze commit, both SHA-256 values, the researcher's explicit approval and the actual effective date, which the researcher sets when the freeze is executed. It adds status-history rows for the decisions that take effect at the freeze.

9a. In the same commit as the freeze entry, `research/literature/criteria_registry.json` is created with one entry copied from the freeze entry (identifier, freeze-entry ID, both paths, freeze commit, both SHA-256 values, effective date; D-085 B2). From then on the validator requires this frozen version on every screening row (D-085 B3).

10. The freeze is separate from recording the D-035 record §6 conditions (one decision row per condition, D-092, in the D-097 form; condition 6 = the closed list of D-091, scope of item (a) open under Q-096, and its item (d) requires the separate fixed-inventory entry recorded before the condition-6 row, D-107, approved in principle; condition 3 awaits Q-085) and from the run authorisations (D-074 (f) for Stage 0; D-077 (6) for the pilot draw and sheet; both in the D-088/D-097 form); each remains a later, separate decision.
11. Freezing the documents does not itself authorise screening, sampling, extraction, pilot work or training.
