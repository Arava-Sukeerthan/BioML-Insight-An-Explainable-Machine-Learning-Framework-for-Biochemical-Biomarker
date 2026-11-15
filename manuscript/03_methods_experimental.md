# 3. Methods — prediction study (manuscript draft section)

> **Draft, 2026-11-12. Planned methods, not results.**
> - Written from the experimental protocol draft v0.1 revision 5 and the v1.0 freeze candidate. **Neither is approved.** The text becomes final only after the researcher's protocol freeze (D-019) and the data decisions D-013 to D-015. Every element marked **[pending: …]** may change at that freeze.
> - Counts are aggregate eligibility and outcome counts computed on 2026-10-24, before any modelling (protocol v0.1 §4, §5.2). They are data descriptions, not results of the study. No model has been trained.
> - **No citations** (`research_plan.md` §6). Placeholders `[REF: …]` follow the rule in §1.
> - Sources in square brackets are removed before submission.

## 3.1 Data source and design
- **Data:** the US National Health and Nutrition Examination Survey (NHANES) [pending: D-014]:
  - **development:** 2017–March 2020 (pre-pandemic) data;
  - **temporal validation:** August 2021–August 2023 data.
- **Design:** cross-sectional; each participant is analysed at a single examination.
- **Files:** 32 public data files, downloaded from the CDC website and checked against SHA-256 checksums [v0.1 Appendix A]. The 2021–2023 documentation advises caution before combining the period with earlier cycles, so the periods are not combined [v0.1 §10].
- **Validation-period access disclosure:** on 2026-10-24, before any model was fitted, aggregate counts (eligibility, outcome prevalence, missingness, medians, unit checks) were computed on the 2021–2023 files. No predictor–outcome relationship was examined [freeze candidate §7].

## 3.2 Participants
Adults aged ≥ 20 years were included if they:
- were examined in the mobile examination centre;
- were in the fasting subsample with a positive fasting weight (fasted 8 to < 24 h);
- had valid FPG and HbA1c values.

Exclusions:
- pregnancy at the examination;
- diagnosed diabetes (keeping only "no" or "borderline" answers);
- current use of diabetes pills.

The eligible samples are N = 3,088 (2017–March 2020) and N = 2,485 (2021–2023) [v0.1 §4; pending: FA-1, minimum age].

## 3.3 Outcome
**Laboratory-defined dysglycaemia** [pending: D-015, FA-2]:
- y = 1 if HbA1c ≥ 5.7% or FPG ≥ 100 mg/dL;
- y = 0 otherwise.

Prevalence:

| | Unweighted | Fasting-weighted |
|---|---|---|
| 2017–March 2020 | 65.0% | 62.6% |
| 2021–2023 | 58.8% | 54.3% |

[v0.1 §5.2]. That the thresholds match a named guideline is recorded as open [REF: candidate CR-08, status OPEN].

The outcome is a single-examination laboratory classification, not a clinical diagnosis.

## 3.4 Predictors
Three predictor groups [pending: FA-4, Q-050]:
- **A, biochemical (21):** liver enzymes and proteins; kidney markers and urate; urine albumin-to-creatinine ratio; reference-method lipids; blood-count indices.
- **C, clinical (6):** age, sex, body-mass index, waist circumference, systolic and diastolic blood pressure.
- **B:** A + C (27).

Exclusions from the predictors:
- serum glucose (direct leakage);
- diabetes-awareness questionnaire items;
- duplicate panel lipids;
- fasting insulin, which is used only in a sensitivity analysis.

Race/ethnicity and income are used only for subgroup reporting.

**Harmonisation between periods:** the reference analysis uses unadjusted 2021–2023 values (S-08). Applying CDC's published backward equations at cycle level is sensitivity analysis S-09b [pending: Q-046, FA-5]. The change of triglyceride method between periods and the change of HbA1c instrument within 2021–2023 are stated limitations.

## 3.5 Preprocessing
Preprocessing is fitted inside each training fold only:
- **missing values:** median or mode imputation, with missingness indicators for variables above 5% missing;
- **transformation:** log(x + 1) for triglycerides, the urine albumin-to-creatinine ratio, ALT, AST and GGT;
- **scaling:** standardisation for the scale-sensitive methods.

## 3.6 Models
**Baselines** [pending: D-018, FA-8, Q-048, Q-049]:
- BL-1: elastic-net logistic regression;
- BL-2: random forest;
- BL-3: gradient-boosted trees;
- BL-4: RBF support-vector machine;
- BL-5: multilayer perceptron;
- BL-6: k-nearest neighbours.

The baseline set is justified provisionally by the data characteristics. D-018 requires it to reflect the methods most used in the included studies, so it is confirmed only after RQ1 screening.

**Framework** [pending: D-017, FA-9]:
- F1: in-fold preprocessing;
- F2: gradient-boosted trees;
- F3: Platt calibration on a held-out calibration split;
- F4: class-conditional (Mondrian) split conformal prediction, α = 0.10;
- F5: TreeSHAP global importance, direction and stability.

Calibration and conformal prediction are also applied to every baseline, so the framework is compared with calibrated baselines.

## 3.7 Partitioning, tuning and model freezing
For each of five seeds derived from a fixed master seed:
1. The development data are split, stratified, into D-train (80%) and D-cal (20%).
2. Every method is tuned with the **same budget** of 40 configurations, by mean log loss in stratified 5-fold cross-validation on D-train, with preprocessing refitted in every fold.
3. The selected configuration is refitted on D-train.
4. On D-cal only:
   - the calibrator and the conformal quantiles are fitted;
   - the decision threshold is fixed as the **largest** probability threshold whose sensitivity on calibrated D-cal probabilities is ≥ 0.80 [freeze candidate §2; pending: FA-10, Q-053].
5. The model is then frozen.

The temporal-validation data are never used for tuning, calibration, conformal fitting, threshold selection or feature choice. A software test checks this: changing the validation labels leaves every development result unchanged. Search spaces, seeds and the budget are fixed in a configuration file before any run [pending: FA-11; `scripts/models/experiment_config_draft.json`].

## 3.8 Evaluation
**Internal validation:**
- out-of-fold predictions on D-train;
- reported both uncalibrated and after the D-cal calibrator. The calibrated estimate is the like-for-like reference for temporal transfer [pending: freeze candidate §9 R3].

**Temporal validation:** the frozen primary-seed model is applied **once** to 2021–2023.

**Metrics:**
- discrimination: AUROC, AUPRC;
- overall accuracy: Brier score and scaled Brier score, log loss;
- calibration: calibration intercept and slope, the integrated calibration index (ICI; local linear smoothing, span 0.75), ECE (secondary);
- at the D-cal threshold: sensitivity and specificity;
- conformal: coverage per class, mean set size;
- net benefit: descriptive only, or omitted [pending: Q-054].

**Weighting** [pending: FA-7]:
- *primary:* unweighted;
- *secondary:* fasting-weighted.

## 3.9 Comparisons and statistical analysis
- **Q1, value of biochemistry:** B vs C and A vs C, for the framework and BL-1. The measure is the AUROC difference.
- **Q2, framework vs calibrated baselines:** within group B. The primary measures are ICI and Brier score, with a paired bootstrap (2,000 resamples) and Holm adjustment across the six comparisons within each metric. For AUROC, either:
  - (a) non-inferiority with a margin justified before the freeze; or
  - (b) a descriptive difference with a 95% CI and no non-inferiority claim [pending: Q-054; option (b) proposed].
- **Q3, temporal transfer:** the change in each metric from internal to temporal validation, per model.

Q1 and Q3 comparisons are few and prespecified, and are reported with unadjusted 95% CIs, which is stated. Survey-based descriptive estimates use Taylor linearisation with PSUs within strata [pending: Q-052].

## 3.10 Explanations and uncertainty
- **Explanations:** described as properties of the model, not causal effects. Their stability is measured as the Spearman correlation of global importance over 50 bootstrap refits and between periods, and as sign agreement with BL-1.
- **Conformal coverage at temporal validation** is measured, not assumed, because exchangeability between periods is not guaranteed.

## 3.11 Sensitivity analyses and scope
Kept for the 2026-11-27 deadline [pending: approval item A6]:
- S-01 (HbA1c-only outcome);
- S-08 (reference harmonisation);
- S-10a (complete-case analysis per predictor group);
- S-13 (folds grouped by stratum × PSU);
- S-09b, only if Q-046 is decided;
- ablations ABL-1 (without F3, no calibration) and ABL-2 (without F4, no conformal sets); labelled AB-1 and AB-2 in v0.1 §15, renamed in the v1.0 candidate to avoid a clash with the activation blockers.

The other prespecified sensitivity analyses and ablations are declared **now, before any result**, as deferred future work. They are not omitted after results are seen.

## 3.12 Reporting
- Reporting follows a prediction-model reporting guideline [REF: TRIPOD or TRIPOD+AI, once verified; pending: Q-055].
- Null, negative and failed results are reported (CLAUDE.md rule 16).
- No performance target was set.
