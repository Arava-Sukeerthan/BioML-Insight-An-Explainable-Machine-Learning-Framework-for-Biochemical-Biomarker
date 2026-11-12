# Closest-prior-art and methods evidence for the protocol (2026-11-12)

> **Status: assistant evidence record. No decision is made here.** D-016 (contribution), D-019 (protocol) and every other decision listed remain the researcher's.
>
> **Sources, retrieved 2026-11-12:**
> - PubMed connector (metadata and abstracts);
> - alphaXiv connector (raw PDF or article-page text; long outputs saved in the session tool-results folder and searched with grep);
> - one public CDC page fetched with curl.
>
> **Evidence levels:**
> - **FT** — full text read for the stated items;
> - **FT-p** — full text searched for the stated items only;
> - **AB** — abstract only.
>
> **The searches here are exploratory and unregistered.** They are not part of the review's search record (`search_queries.csv`), and absence of a match is **not** evidence of a gap (CLAUDE.md rule 14). Formal evidence for D-016 comes from the registered, screened RQ5 strand. No abstract text is reproduced; content is paraphrased.

## Access limitations (checked 2026-11-12)
The container's proxy refused (HTTP 000) every one of these hosts:
- `pmc.ncbi.nlm.nih.gov` and `www.ncbi.nlm.nih.gov` from the container (the alphaXiv service reached PMC pages for other articles, but **not** PMC12690183);
- `diabetesjournals.org`, `www.medrxiv.org`, `www.sciencedirect.com`;
- `stat.ethz.ch` and `search.r-project.org` (R documentation).

`wwwn.cdc.gov` was reachable.

Consequences:
- **CR-02 (Elsevier), CR-03 (medRxiv; not archived in PMC by licence) and ADA 2026 could not be read in full.**
- The R `loess`/`lowess` defaults could not be verified.

## 1. Closest-prior-art evidence table

Components of the candidate framework (protocol v1.0 candidate):
- **B** — biochemical predictors;
- **Cal** — probability calibration;
- **CP** — conformal uncertainty;
- **XS** — explanation, and explanation stability;
- **TV** — temporal or independent validation.

| # | Study (level) | Dataset; N | Outcome | Predictors | Models | Calibration | Uncertainty | Explainability | Validation | Metrics | Limitations (as reported or visible) | Overlap with BioML-Insight |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Yoo, Maggiore, Jolliet. *J Clin Epidemiol* 2026;195:112266 (CR-02; P0303) — **AB; FT inaccessible** | NHANES 1988–2018, N = 17,458; validation NHANES 2021–2023 (N = 3,043) and KNHANES 2023 (N = 5,492) | **FPG ≥ 100 mg/dL or HbA1c ≥ 5.7%** (prevalent pre/diabetes) | Multimodal at development; final 7 **non-laboratory** (age, waist, SBP, gender, upper-leg length, arm circumference, BMI) | Multiple ML; Boruta selection; neural network best | Assessed; method not stated in the abstract | Not stated (CIs for ROC-AUC) | "Interpretability analysis" (method not stated) | **Temporal** (NHANES 2021–2023) + **external** (KNHANES) | ROC-AUC, calibration, decision curves | Self-assessment predictors only; no laboratory data | **Same outcome; NHANES; same temporal validation period**; Cal; XS (unspecified). Not B, not CP |
| 2 | Hutchison, Rinella, Mirmira, Parker. *medRxiv* 2025 (CR-03; P3005) — **AB; FT inaccessible**; preprint, not peer-reviewed | NHANES 2005–2016, N = 13,800 | OGTT 2-h glucose: 140–199 (pre), ≥ 200 mg/dL (diabetes) | 20 features: vitals; FPG, insulin, TG, iron, cholesterol, GGT, creatinine, platelets, neutrophil %, urine albumin and creatinine; poverty ratio | Gradient-boosted trees; compared with HbA1c and FPG alone | Assessed; method not stated | Not stated | Feature contributions (method not stated) | Not stated in the abstract | AUROC, calibration, PPV, decision curves | Preprint; different outcome (OGTT); no LR comparator stated | **B**; Cal; gradient boosting. Not CP; TV unknown |
| 3 | Cai Z et al. *Diabetes Metab Res Rev* 2026;42:e70193 (CR-04; P0256) — **AB** | NHANES 2003–2018, HBV-positive adults, N = 14,287 | Diabetes | 11 inflammation/immune composite indices + demographic + biochemical | LASSO; 7 algorithms; ANN best | Calibration curve | Not stated | **SHAP** | Internal 7:3 split | AUC, accuracy, calibration, decision curves | Subgroup population; internal only | **B**; Cal; SHAP. Not CP, not TV |
| 4 | De Silva K et al. *PLoS One* 2021;16:e0250832 (CR-01) — **FT** | NHANES 2007–2016, N = 16,429; 2013–2016 held out (n = 6,673) | Undiagnosed type 2 diabetes | 114 nutritional + behavioural + socioeconomic | LR, ANN, RF; resampling | **None** in the text | None | Odds ratios / variable importance | Later-cycle hold-out of the same survey (called "external") | AUROC; benchmark against the ADA risk test | Diabetes, not prediabetes; no calibration | NHANES; LR comparator; temporal-type hold-out |
| 5 | Türkoğlu Genç F, Yildiz M. *Healthcare (Basel)* 2026;14(19):3214, doi:10.3390/healthcare14193214 — **FT-p** (outcome definition, calibration) | Primary care (Türkiye), N = 2,033 | Previously unrecognised dysglycaemia (authors cite ADA 2026: FPG 100–125 / HbA1c 5.7–6.4%, and the diabetes range) | FINDRISC + demographic, clinical, **laboratory** variables (FPG and HbA1c not used as predictors) | CatBoost (3 feature sets); raw FINDRISC benchmark | **Brier, calibration intercept and slope** | Paired-bootstrap CI for ΔAUC | **SHAP** (selection, interpretation) | Single internal split + 5-fold CV | AUC, Brier, intercept/slope, paired bootstrap | Single centre; internal only. Adding routine laboratory variables to FINDRISC gave a non-significant ΔAUC (reported 0.005, CI −0.012 to 0.022) | **Q1-type question** (incremental value of laboratory data); outcome close to ours; Cal; SHAP; paired bootstrap. Not CP, not TV |
| 6 | Yang CC et al. *Diagnostics (Basel)* 2025;15(19):2507, doi:10.3390/diagnostics15192507 — **FT-p** (stability, calibration, validation) | MJ cohort, Taiwanese men 18–35, N = 6,247; mean follow-up 5.9 y | Δ-FPG; future prediabetes | Body fat, WBC, age, TSH, TG, LDL-C and others | RF, SGB, XGBoost, elastic net vs linear regression; XGBoost classifier with SMOTE-Tomek | Brier; decision curves; no recalibration terms found | CIs over repeated runs | SHAP; **SHAP-importance distributions over 20 repeated train/test cycles** (boxplots) | Internal repeated splits only | SMAPE, RMSE, AUC, PR-AUC, Brier | Men only; internal | **B**; Cal (assessment); **explanation stability over refits** (qualitative). Not CP; no TV |
| 7 | Ghaderzadeh M et al. *BMC Med Inform Decis Mak* 2025;26:36, doi:10.1186/s12911-025-03333-9 — **AB** | PERSIAN Dena cohort, N = 3,203 | Type 2 diabetes (early detection) | 79 → 15 incl. biochemical (FBS, TG) | ExtraTrees | **Isotonic** post-hoc (made it worse: AUC fell, under-confident) | Not stated | SHAP + Morris sensitivity | 10-fold CV + 80/20 hold-out | AUC, F1, Brier, slope/intercept | Modest discrimination | B; post-hoc Cal; SHAP. Not CP, not TV |
| 8 | Kodji E et al. *PLoS Comput Biol* 2026;22(8):e1014670, doi:10.1371/journal.pcbi.1014670 — **AB** | ADVANCE (n = 4,098) → UK Biobank (17,574 White British; 1,145 South Asian; 749 African) | Nephropathy, stroke, MI in type 2 diabetes | Multi-polygenic risk score | LR + **Mondrian cross-conformal prediction** | Not stated | **Mondrian CP** (confidence, credibility, prediction sets) | Not stated | **Cross-cohort, cross-ancestry** (external) | Discrimination; set validity | Genetic predictors | **CP (Mondrian, classification)**; external transfer. Not B, not XS |
| 9 | Olshvang D et al. *medRxiv* 2026, doi:10.64898/2026.08.04.26359704 — **AB**; preprint | ACCORD (secondary analysis; N as stated in the abstract, partly garbled in the record) | 48-month eGFR decline (continuous) | Baseline clinical (creatinine and urine biomarkers excluded) | RF, GB, penalised linear, XGBoost | — | **Split and locally adaptive conformal intervals** | — | Fixed train / calibration / test | R², MAE, coverage, width | Regression | CP (regression), calibration partition |
| 10 | Harris C et al. *Diabetes Metab Syndr* 2024;18(8):103113, doi:10.1016/j.dsx.2024.103113 — **AB** | NHANES + Look AHEAD | Waist circumference (regression) | — | ML with conformal prediction | — | **Conformal intervals** | — | External (Look AHEAD) | Coverage | Regression | CP + NHANES + external |
| 11 | He L et al. *Acta Diabetol* 2026;63(8):1411–20, doi:10.1007/s00592-026-02717-1 — **AB** | NHANES (19,931) + CHARLS (96,628) | Functional decline (diabetes–sarcopenia) | CRP, HDL, TG, albumin, BMI and others | LR, LASSO, XGBoost | Calibration | — | SHAP | **Independent population (CHARLS)** | AUC, calibration, decision curves | Different outcome | B; Cal; SHAP; independent validation. Not CP |

**The other 18 of the 22 explanation-stability hits.** Four of the 22 are in the table above: study 5 (PMID 42881653), study 6 (41095726), study 7 (41469992) and study 11 (42329276). The remaining 18 (abstract level) concern targets outside dysglycaemia detection:
- PMIDs 42997291, 42942319, 42903227, 42901554, 42767595, 42421984, 42293742, 42121627, 42042873, 41883473, 41869674, 41788702, 41659805, 41419964, 41353539, 41081817, 41072899, 37171784.

They use SHAP with calibration curves or Brier and often decision curves. Where they use "stability", it refers to **feature-selection or performance** stability under bootstrap, not explanation stability. None reports conformal prediction.

### What the evidence establishes and what it does not
| Component | Established in prior work (level) | Not established by this evidence |
|---|---|---|
| B (biochemical predictors for dysglycaemia/diabetes) | Yes: studies 2, 3, 5, 6, 7 | — |
| **Incremental value of laboratory data over clinical/risk-score data** | Study 5 (FT-p): a small, non-significant gain over FINDRISC in one primary-care cohort, internal only. Study 1 achieved its performance **without** laboratory data | Whether laboratory data add value **for this outcome in NHANES under temporal validation**. That is our Q1, and it is unanswered by these studies |
| Cal | Yes: 1, 2, 3, 5, 6, 7, 11 (assessment); 7 (post-hoc isotonic) | Platt-calibrated comparison of all baselines on equal footing (not seen) |
| CP | Yes in neighbouring settings: 8 (Mondrian classification, genetic predictors), 9 and 10 (regression intervals) | CP for dysglycaemia classification from routine biochemistry, or **CP coverage under temporal shift** in this setting (not seen in this non-exhaustive search) |
| XS | SHAP common; **refit-stability of SHAP importance** exists qualitatively (6) | Quantified rank stability across refits **and across periods** (not seen in this search) |
| TV | **Yes for the same outcome** (1: NHANES 2021–2023); later-cycle hold-out (4); independent population (11) | — (temporal validation is **not** a novelty for this outcome) |
| All five together | Not observed in the items read | **Cannot be claimed**: absence in an exploratory search is not evidence |

## 2. CR-02 and CR-03 — verification status
| | CR-02 (Yoo 2026, *J Clin Epidemiol*) | CR-03 (Hutchison 2025, *medRxiv*) |
|---|---|---|
| Full text | **Not accessible:** Elsevier host blocked (HTTP 000); the alphaXiv fetch returned nothing. No PMC copy | **Not accessible:** PMC states the licence does not permit archiving; `www.medrxiv.org` blocked |
| Level reached | AB (PubMed) | AB (PubMed, and the PMC landing page with the abstract) |
| AI summaries used? | **No** | **No** |

**Component comparison** (AB level only; anything not in the abstract is "not stated", **not** "absent"):

| Component | CR-02 | CR-03 |
|---|---|---|
| Outcome | Same as ours | OGTT-based (different) |
| Predictors | Non-laboratory (differs from our B) | Laboratory + vitals (like our B) |
| Models | Several ML; NN best | Gradient-boosted trees |
| Calibration | Assessed; method not stated | Assessed; method not stated |
| Uncertainty | Not stated | Not stated |
| Explanation | Stated; method not stated | Feature list; method not stated |
| Validation | Temporal + external | Not stated |
| Baselines | Guideline screening rules | HbA1c and FPG alone |

**What is needed:** the full texts (your library access, or the PDFs). Until then, the manuscript can compare only at abstract level, and must say so.

## 3. Missing methodological references (Task 3)
| Claim in protocol / manuscript | Reference located and verified (level) | Precise support | Status |
|---|---|---|---|
| Taylor-linearised variance for NHANES; PSUs "with replacement" within strata; **domain (subpopulation) estimation using all non-zero-weight records** | CDC/NCHS, NHANES tutorials, "Variance Estimation", `wwwn.cdc.gov/nchs/nhanes/tutorials/varianceestimation.aspx` (read 2026-11-12) — **FT** | NCHS recommends Taylor series linearisation for all NHANES surveys; with-replacement first-stage approximation; subpopulation estimation requires all records with non-zero weight + a subpopulation indicator. The page cites Korn & Graubard, *Analysis of Health Surveys* (Wiley, 1999) as a text; that book was **not** read | Use the CDC page as the authoritative source. **Implementation consequence:** `survey.weighted_mean_taylor` had no domain option. A `domain` argument was added on 2026-11-12, with a test (previous behaviour unchanged) |
| Explanation stability as a concern | Alvarez-Melis D, Jaakkola TS. On the robustness of interpretability methods. 2018 ICML Workshop on Human Interpretability (WHI 2018); arXiv:1806.08049 — **FT** | Defines robustness as **local Lipschitz stability to small input perturbations**; shows SHAP and LIME explanations can vary strongly for non-linear models | Supports the **motivation**. It does **not** define our refit/period rank-stability metric (F5). The applied precedent for refit stability is study 6 above. A methodological source for **refit or bootstrap stability of global importance** is still missing (not located) |
| Baseline implementations (elastic net, SVM via LIBSVM, k-NN, random forest, MLP) | Pedregosa F et al. Scikit-learn: machine learning in Python. *JMLR* 2011;12:2825–30 (arXiv:1201.0490) — **FT** | A software reference for the implementations (the paper names the SVC via LIBSVM, elastic net and k-NN) | Cite as the **software** reference. Original algorithm papers (elastic net, random forest, SVM, k-NN, MLP) are **not located**; cite them only if a methodological claim needs them (not for count) |
| XGBoost (F2, BL-3) | Chen & Guestrin, KDD '16 (CR-12c) — FT | — | Done earlier |
| Platt scaling (F3, BL-4) | **Not located:** the 1999 book chapter is not indexed in PubMed or alphaXiv; no bibliographic details are asserted | — | **UV.** Needs your library copy or a Crossref export |
| Holm's procedure (Q2 multiplicity) | **Not located:** *Scand J Stat* 1979 is not indexed in alphaXiv or PubMed; no bibliographic details asserted | — | **UV**, as for Platt |
| Bootstrap percentile CIs | **Not searched or located** in this pass | — | **UV** |

## 4. R14 — ICI decision record (for researcher review)
- **What the original method specifies** (CR-13, Austin & Steyerberg 2019, full text searched):
  - ICI = the weighted mean absolute difference between predicted probability and a smoothed observed rate, weighted by the empirical density of predictions.
  - The authors built calibration curves with R `loess(Y∼P)` and `lowess(Y∼P, iter = 0)`, plus a logistic-regression / restricted-cubic-spline alternative.
  - Their simulations found the smoother changes the metric's level: `lowess` lowest, the spline method highest.
  - **The defaults of R `loess`/`lowess` (span, degree) are not stated in the text read and could not be checked** (R documentation unreachable).
- **What our implementation computes** (`metrics._lowess`, `metrics.ici`):
  - local-linear regression of y on p;
  - tricube weights; nearest-neighbour bandwidth of ⌈0.75·n⌉ points; **no robustness iterations**;
  - evaluated at each observation, clipped to [0, 1];
  - optional observation weights.

  Structurally this is the `lowess(…, iter = 0)` variant. The only open parameter is the span, 0.75, whose equality to R's default is **unverified**.
- **Is span 0.75 justified?** Not by a cited source at present. It is a prespecified smoothing choice.
  - In a **synthetic** check (simulated probabilities; no model fitted; n = 2,485), ICI levels changed little for spans 0.5 to 0.9.
  - The between-model ICI difference was stable (+0.060 to +0.062).
  - A small span (0.3) inflated the level for the well-calibrated model (noise).
  - This is one setting, not proof of robustness.
- **Does the implementation need modification?** Not for validity of the within-study comparisons, because the same smoother is applied to every model. **The specification must be fixed and cited at the freeze.**
- **Options (RESEARCHER, at D-019):**

  | Option | What it means |
  |---|---|
  | (a) | Keep local-linear, span 0.75, stated as a prespecified choice with no claim of equality to R `lowess`; add a span sensitivity analysis |
  | (b) | Set the span to R `lowess`'s default once verified from R documentation, to match the paper's `lowess(iter = 0)` variant; add the sensitivity analysis |
  | (c) | Implement the paper's primary `loess` variant (local quadratic) after verifying its defaults; requires new code and tests |

- **Recommendation:**
  - (a) or (b) plus a **sensitivity analysis**: ICI recomputed at span 0.5 and 0.9 on the same predictions. It is cheap, needs no refitting, and is reported in a supplement.
  - (c) only if exact comparability with published ICI values is needed.
- **How to report the limitation:** "ICI depends on the smoothing method used to estimate the calibration curve; values are comparable across models within this study (same smoother) but not directly with ICI values from studies using other smoothers."
- **The implementation is not changed** pending this decision.

## 5. ADA outcome definition (Task 5)
- **Requirements to verify:** listed in `2026-11-12_AB-7_reference_preverification.md` §3:
  - the HbA1c ≥ 5.7% and FPG ≥ 100 mg/dL lower limits;
  - the 6.5% and 126 mg/dL diabetes cut-points;
  - the confirmatory-testing guidance;
  - whether each test is a criterion on its own.

  Source: *Diabetes Care* 2026;49(Suppl 1):S27–S49, doi:10.2337/dc26-S002, Section 2.
- **Status:** still **unverified**. A fourth attempt via the alphaXiv PMC route failed (2026-11-12).
- **Secondary corroboration (not verification):** two studies attribute the same cut-points to ADA 2026 or use them: study 5 (FT-p) and CR-02 (AB). Study 5 also avoids diagnostic terms because no confirmatory test was available, as our protocol does.
- **Alternative description if the PDF remains unavailable** (for your decision under FA-2 / D-015; no threshold is changed):
  > "The outcome was laboratory-defined dysglycaemia at a single examination: HbA1c ≥ 5.7% or fasting plasma glucose ≥ 100 mg/dL (both measured; outcome = 0 if both below these values). These numerical cut-points are commonly used to denote the lower limits of the prediabetes range; we do not claim correspondence with any specific edition of a clinical guideline. Because no repeat or confirmatory test was available, the outcome is not a clinical diagnosis of prediabetes or diabetes."

  The phrase "commonly used" would itself need a source. Without one, it is deleted, and the sentence states only the numbers.

## 6. Three candidate contribution formulations (Task 6; for D-016, not chosen)

### A — Biomarker-based predictive modelling with calibrated probabilities and uncertainty
- **Supporting studies:** 2, 3, 5, 6, 7 (biochemical prediction with calibration); 8–10 (conformal elsewhere).
- **Existing overlap:** high for biochemistry plus calibration; the conformal method itself is established.
- **Potential novelty:** limited. At most, class-conditional conformal sets for dysglycaemia from routine biochemistry, **if** the RQ5 review finds none.
- **Required experiments:** Q2 (framework vs calibrated baselines); conformal coverage internal and temporal.
- **Scientific risks:** it reads as an application of known methods. The discrimination gain over CR-02 may be small or absent.
- **Evidence still missing:** a completed RQ5/RQ3 screen; full texts of CR-02 and CR-03.

### B — Integrated explainability, calibration and uncertainty framework with temporal validation
- **Supporting studies:** 1 (temporal, same outcome); 6 (refit stability of SHAP); 8 (Mondrian CP).
- **Existing overlap:** temporal validation for this outcome exists (1). Each component exists separately.
- **Potential novelty:** the **combination**, including **conformal coverage and explanation-rank stability measured across the period shift**. Not seen in this search, but not established as absent.
- **Required experiments:** Q2, Q3 (with the Q-100 reference); F4 coverage under shift; F5 stability across refits and periods; ablations ABL-1 and ABL-2.
- **Scientific risks:**
  - an "integration" claim is vulnerable if the review finds a combined framework;
  - the stability metric lacks a methodological source;
  - temporal shift may reduce coverage (which must be reported).
- **Evidence still missing:** the RQ5 review complete; an explanation-stability methods source; CR-02 full text.

### C — Narrower contribution on the demonstrable gap (the incremental value of routine biochemistry, Q1)
- **Supporting studies:** 1 (strong non-laboratory model for the same outcome, so the comparison point exists); 5 (small, non-significant laboratory increment over FINDRISC, internal, different population).
- **Existing overlap:** the question has been asked in other settings (5). No NHANES temporally validated answer for this outcome was seen.
- **Potential novelty:**
  - a **prespecified, calibrated, temporally validated estimate** of the added value of biochemistry over clinical measures for this outcome in NHANES;
  - the paired comparison B vs C and A vs C (Q1), with calibration and uncertainty reported as secondary.

  A null result (no added value) is publishable and must be reported.
- **Required experiments:** Q1 (framework and BL-1 on groups A, B, C), internal and temporal; Q3 for transfer; S-01 (HbA1c-only) and S-13.
- **Scientific risks:**
  - the effect may be small;
  - the limited predictor set (21 analytes) may undersell biochemistry;
  - groups B and C differ in information, not only in type.
- **Evidence still missing:** the RQ1/RQ5 screen for direct NHANES incremental-value studies; CR-02 full text (its development may have tested laboratory data before selecting non-laboratory predictors: the abstract says "multimodal data").

**Common to all options:**
- no "first" or "novel" wording without the completed review;
- the contribution is decided by you (D-016) after the Stage D gate.
