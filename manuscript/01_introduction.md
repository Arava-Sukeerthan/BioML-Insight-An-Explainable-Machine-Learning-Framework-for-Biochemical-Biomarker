# 1. Introduction (manuscript draft section)

> **Draft, 2026-11-12. Structure and argument only.**
> - **No citations.** Every statement that needs literature support carries a placeholder `[REF: …]` naming the kind of evidence required. A placeholder may be filled only with an inventory record that is `verified` under D-064 (`research_plan.md` §6). If no verified record supports the statement, the statement is **removed or weakened**, not kept without support.
> - **No results, novelty claim or contribution wording.** The contribution paragraph (§1.4) stays a placeholder until D-016, which follows the RQ5 closest-prior-art review.
> - The empirical task described here is the **draft** protocol's proposal: the disorder, dataset and outcome decisions D-013, D-014 and D-015 are **pending**.

## 1.1 Problem
Dysglycaemia below the diabetes range, defined here by laboratory thresholds for glycated haemoglobin (HbA1c) or fasting plasma glucose (FPG), is the target of screening and prevention programmes [REF: guideline defining the thresholds; candidate CR-08, status OPEN]. Routine clinical-chemistry panels and blood counts are measured far more often than dedicated glycaemic tests [REF: evidence on test-ordering patterns; or remove]. Whether these routine biomarkers carry information about dysglycaemia beyond simple clinical measurements (age, sex, body size, blood pressure) is an empirical question. It can be studied directly in population survey data where both sets of measurements and the glycaemic reference tests are available.

## 1.2 What prediction studies of this kind usually report
Machine-learning studies that classify metabolic conditions from biochemical biomarkers commonly report discrimination [REF: RQ1 review findings, after screening]. They report probability calibration, uncertainty statements and the stability of explanations less often [REF: RQ2/RQ3 findings; note that coverage of these strands is incidental, manuscript §2.4]. They also often lack validation on data collected separately from the development data [REF: RQ4 findings]. These statements are hypotheses of the review until the screening and synthesis are complete (`[HYPOTHESIS]`), and they are rewritten to match what the review finds, including if it finds the opposite.

## 1.3 Why calibration, uncertainty, explanation and temporal validation together
- **Calibration.** A predicted probability is useful for decisions only if it matches observed frequencies [REF: methodological source on calibration in prediction models].
- **Uncertainty.** Conformal prediction gives prediction sets with a finite-sample coverage guarantee under exchangeability, and class-conditional variants give that guarantee per class [REF: methodological source on split and Mondrian conformal prediction].
- **Explanation stability.** Attributions such as SHAP values describe a fitted model. Their usefulness depends on whether they stay stable across refits and data periods [REF: methodological source on explanation stability].
- **Temporal validation.** Applying a frozen model once to a later, separately sampled period tests transfer under changes in population and measurement. It is not external validation in a different population or setting [REF: TRIPOD or a comparable reporting framework, on the definition of validation types].

## 1.4 Aim and contribution
**Aim** (research question, provisional, Q-016; protocol v0.1 §1):
> For laboratory-defined dysglycaemia in US adults without diagnosed diabetes, do biochemical biomarkers add predictive information beyond simple clinical measurements? And can one prespecified framework give calibrated probabilities, valid uncertainty statements and stable explanations, with discrimination comparable to established baseline methods, on the development period and on a later NHANES period?

**Contribution:** [PLACEHOLDER — reserved for the researcher (D-016), worded only as the RQ5 closest-prior-art review supports. Candidate closest studies CR-02 and CR-04 are not yet citable. No novelty claim is made.]

**Not claimed:** clinical diagnosis; incident risk; causal effects of biomarkers; external validation; clinical utility; novelty.
