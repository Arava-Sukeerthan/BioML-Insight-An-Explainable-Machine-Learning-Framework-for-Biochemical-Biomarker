# Limitations stated in advance (manuscript draft section)

> **Draft, 2026-11-12.** These limitations are declared **before** any screening result or model result exists, from protocol v0.1 §20, the v1.0 candidate (§9), the literature methods (§2.6) and recorded investigations. The Discussion adds result-dependent limitations later; nothing listed here is removed after results are seen. **[pending: …]** marks items that a decision may change. No citations (`research_plan.md` §6).

## Prediction study
1. **Design and outcome:**
   - cross-sectional data, with a single-visit laboratory outcome and no confirmatory test;
   - the outcome is a laboratory classification, not a clinical diagnosis;
   - in the development period, most positives come from fasting glucose 100–125 mg/dL alone [v0.1 §5.2].
2. **Exclusions:** diagnosis and medication are self-reported. Undiagnosed people taking glucose-lowering drugs cannot be identified in 2021–2023, which has no drug names.
3. **Measurement across periods:**
   - The HbA1c instrument and the chemistry analyser changed **within** 2021–2023, at dates that are not published.
   - The triglyceride method changed between periods.
   - The reference analysis uses unadjusted values (S-08). Residual bias near the 5.7% HbA1c threshold is possible [pending: Q-044, Q-046, Q-060].
4. **Validation type:** temporal validation in a later, separately sampled period of the same survey is **not** external validation in another population or setting. 2021–2023 also had lower response rates and design changes.
5. **Prevalence shift:** the outcome prevalence differs between periods (fasting-weighted 62.6% vs 54.3%), mostly in the glucose component. Its cause is not established [v0.1 §5.2].
6. **Analysis choices:**
   - survey weights are used only in secondary analyses [pending: FA-7];
   - subgroup samples are modest;
   - several prespecified sensitivity analyses are deferred as future work, declared before any result [pending: A6].
7. **Comparisons:**
   - no formal non-inferiority claim is made for AUROC, because no verified source supports a margin [pending: Q-054];
   - Q1 and Q3 comparisons are reported without multiplicity adjustment, and this is stated.
8. **Explanations:** SHAP attributions describe the fitted model, not causal effects of biomarkers.
9. **Prior aggregate access:** aggregate counts on the validation period were computed before any model was fitted (disclosed in the Methods).

## Literature review
10. **Screener:** a single primary screener (the assistant) is used outside the 60-record pilot and the 50-record audit.
11. **Coverage:** several bibliographic databases and second-source hosts were unreachable. Explainability and calibration/uncertainty evidence (RQ2, RQ3) is incidental, and external validation and limitations (RQ4, RQ6) are covered only partly [manuscript §2.4].
12. **Depth:** Tier-3 records are included on abstract-level evidence.
13. **Citation verification:** this relies on researcher-exported Crossref records where script retrieval was blocked [pending: Q-099].
14. **Preservation:** the off-device backup of the raw search exports is researcher-reported and not independently verified [pending: A1, Q-063 wording].
