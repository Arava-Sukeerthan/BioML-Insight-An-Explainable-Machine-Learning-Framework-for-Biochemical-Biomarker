# Screening Criteria

| Field | Value |
|---|---|
| Task | LIT-001 (Stage A) |
| Version | 1.0 — **DRAFT, pending researcher approval** |
| Prepared | 2026-10-14 |
| Applies to | All records from `search_queries.csv`, citation chasing, and seed lookups |
| Provisional elements | Disorder scope (Q-001) and biomarker scope (Q-002) are marked **[PROVISIONAL]** |

Records are screened against the criteria of **the RQ strand(s) they could inform**. A record is
included if it satisfies the criteria of at least one RQ. Its RQ tags are recorded.

---

## 1. Common criteria (all RQs)

### Inclusion (all must hold)
| Code | Criterion |
|---|---|
| I-C1 | Peer-reviewed journal article, peer-reviewed full conference paper, or preprint (preprints flagged; published version preferred when it exists) |
| I-C2 | Full text or an abstract sufficient for the extraction fields of the relevant RQ |
| I-C3 | English language |
| I-C4 | Original research, methodological/statistical paper, software/framework paper, reporting guideline or consensus statement. **Reviews** are included only as *lead sources* (tag `review_lead`) |

### Exclusion (first applicable code is recorded as the primary reason)
| Code | Reason |
|---|---|
| E1 | Not human data (animal, cell-line, plant, environmental) — applies to RQ1, RQ2b, RQ4-applications |
| E2 | No supervised predictive model or classifier developed, validated, or evaluated (e.g., purely univariate association or descriptive biomarker studies) |
| E3 | Input data are not biochemical biomarkers (see §2) |
| E4 | Target condition outside the metabolic-disorder scope (see §2) |
| E5 | Publication type: editorial, commentary, news, letter without original data, conference abstract only, study protocol without results, thesis, book chapter (books allowed only as verified foundational methods sources) |
| E6 | Not English |
| E7 | Retracted |
| E8 | Duplicate (handled by deduplication; recorded for the flow diagram) |
| E9 | Full text unavailable **and** abstract insufficient for extraction |
| E10 | Outside the query's date window (only possible for records from citation chasing or supplementary sources in RQ1/RQ2/RQ6 application strands) |
| E11 | Prediction target is continuous only (regression) with no classification or risk-probability output — applies to RQ1 |
| E12 | Not relevant to any RQ (catch-all; justification required) |

Sample size, journal, country and model type are **not** exclusion criteria. They are extracted
and coded.

---

## 2. Scope definitions

### 2.1 Metabolic-disorder scope [PROVISIONAL — Q-001]
**In scope:** type 1, type 2 and gestational diabetes; prediabetes / impaired glucose
regulation; insulin resistance; metabolic syndrome; NAFLD/MASLD/NASH/MASH; dyslipidaemias;
hyperuricaemia and gout; inborn errors of metabolism (incl. newborn-screening targets).

**Pending researcher decision (included at screening, tagged `scope_pending`):** obesity
(as a classification target), thyroid dysfunction, polycystic ovary syndrome. These records are
kept so that the decision does not require re-searching.

**Out of scope (E4):**
* complications of metabolic disease when the classification target is the complication itself
  (e.g., diabetic retinopathy, nephropathy, foot ulcer);
* cardiovascular events, cancer, and infectious disease, *unless* the record is retained for
  RQ2–RQ4 as a methodological exemplar (see §3).

### 2.2 Biochemical-biomarker scope [PROVISIONAL — Q-002]
**In scope:**
* **Metabolomics / lipidomics:** targeted or untargeted; MS- or NMR-based; any biofluid or tissue.
* **Newborn-screening profiles:** MS/MS amino acids and acylcarnitines.
* **Routine clinical-chemistry and laboratory values:** e.g., glucose, HbA1c, lipid panel, liver
  enzymes, renal markers, insulin/C-peptide, uric acid. Also complete blood count when
  combined with chemistry.
* **Mixed feature sets:** demographic, anthropometric or clinical variables combined with
  biochemical markers, provided the biochemical markers are a substantive part of the model
  input (stated, or ≥ 1 biochemical marker among the final predictors).

**Out of scope (E3):** imaging-only; genomics, transcriptomics or methylation-only;
microbiome-only; free text-only; continuous-glucose-monitoring or wearable time series only;
questionnaire-only.

### 2.3 Machine-learning scope
Supervised classification or risk-probability models, including:
* regularised regression (LASSO, elastic net);
* PLS-DA / OPLS-DA used as classifiers;
* tree ensembles, SVM, k-NN, naive Bayes, neural networks, AutoML, and tabular foundation models.

Classical logistic-regression-only studies are included **only** for RQ3/RQ4 methodological
relevance or as comparators. They are not part of the RQ1 ML-method landscape. They are coded
`lr_only`.

---

## 3. RQ-specific criteria

| RQ | Include when | Specific exclusions |
|---|---|---|
| RQ1 | Meets §2.1 + §2.2 + §2.3; task is diagnosis/screening/classification/subtyping or risk prediction of a metabolic disorder (prognostic incident-disease models tagged `prognostic`) | E1–E4, E11 |
| RQ2 | (a) Methodological work on explanation methods for tabular or omics classifiers (any biomedical domain), incl. evaluation of stability, faithfulness, or agreement of attributions; **or** (b) RQ1-eligible study that reports and interprets an explanation method | Studies that only mention "feature importance" without reporting how it was computed are excluded under E12 unless otherwise RQ1-eligible |
| RQ3 | (a) Methodological work on calibration, recalibration, conformal prediction, or other uncertainty quantification for classification/risk models, preferably tabular biomedical data; **or** (b) RQ1-eligible study reporting calibration or uncertainty | Image-only or NLP-only UQ papers excluded unless proposing a method directly applicable to tabular classifiers (judgement recorded) |
| RQ4 | (a) RQ1-eligible study with external, temporal, or cross-cohort validation; **or** (b) methodological work on external validation, transportability, dataset shift, batch/site effects for clinical or omics prediction models | Internal cross-validation only → not RQ4 (may remain RQ1) |
| RQ5 | Proposes or evaluates an integrated pipeline/framework covering **≥ 3** of: biomarker/feature selection; classification; explainability; calibration or uncertainty estimation — for biomarker/omics/clinical tabular data | — (any domain is retained here as closest prior art, tagged with domain) |
| RQ6 | Systematic/scoping reviews, meta-research, reporting guidelines, risk-of-bias tools, or empirical studies of methodological pitfalls (leakage, overfitting, reproducibility) relevant to biomarker/omics/clinical ML | Narrative reviews without methodological content → `review_lead` only |

---

## 4. Decision procedure

```
Record
 ├─ Stage 0: PubMed publication type ∈ {Editorial, Comment, News, Published Erratum,
 │           Retracted Publication} → exclude (E5/E7), automatic, counted
 ├─ Stage 1 (title/abstract):
 │    ├─ clearly meets ≥1 RQ → INCLUDE (tag RQs, tier)
 │    ├─ clearly fails all RQs → EXCLUDE (first applicable code + one-line justification)
 │    └─ insufficient information → UNCERTAIN → full text
 └─ Stage 2 (full text): INCLUDE / EXCLUDE (code) / ABSTRACT_ONLY (if full text unavailable
                          but abstract supports extraction)
```
* **When in doubt, include at Stage 1.** Exclusion requires a positive reason.
* Uncertain records go forward to full text. They are never silently dropped.
* Any change to these criteria after screening starts is logged in `logs/DECISION_LOG.md`, and the
  affected records are re-screened.

## 5. Tiering for full-text priority (from `search_strategy.md` §6.5)
| Tier | Definition |
|---|---|
| 1 | RQ1-eligible and addresses ≥ 2 of {explainability, calibration/uncertainty, external validation}; all RQ5; reporting guidelines/RoB tools |
| 2 | Methodological papers for RQ2–RQ4; RQ1-eligible studies addressing exactly one of the three aspects |
| 3 | Other RQ1-eligible studies. These are coded from the abstract; full text is read for a random sample only |

## 6. Screening record format
`research/literature/screening/title_abstract_decisions.csv` and `full_text_decisions.csv`:
`record_id, decision, reason_code, rq_tags, tier, scope_flags, justification, screener, date`.
The audit file (`audit_sample.csv`) contains the sampled records without the assistant's
decision, plus the random seed used.

## 7. Pilot calibration of the criteria
Before full screening, the criteria are applied to the first 30 records (in PMID order) of
`Q-PM-01` and `Q-PM-09`. Ambiguities found are resolved with the researcher and logged before
screening the rest. *(Planned for LIT-003.)*
