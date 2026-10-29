# Experimental Protocol — NHANES laboratory-defined dysglycaemia (draft v0.1)

| Field | Value |
|---|---|
| Task | PROTOCOL-DRAFT-001 (2026-10-24, Day 11) |
| Version | **0.1, draft revision 4 (Q-069-RESOLUTION, 2026-10-29) — DRAFT for researcher review. Not approved, not frozen, not active.** Revisions 1–4 make only owner-authorized draft edits (change history) |
| Decision it informs | D-019 (freeze the experimental protocol, **PENDING**). It also informs D-013, D-014, D-015, D-016, D-017 and D-018, which are all **PENDING**. This draft does not change any decision status |
| Governing documents | `GOVERNANCE.md`, `CLAUDE.md`, `research/methodology/research_integrity.md` (draft v1.0, pending, Q-018), `logs/DECISION_LOG.md` |
| Data evidence | Local, read-only verification of the official NHANES files on 2026-10-24 (§3, Appendix A). The files are in the git-ignored `data/raw/nhanes/`. Nothing participant-level is committed |
| What this document is not | Not an approval record, not a result and not a novelty claim. No model has been trained or evaluated |

**Labels** (GOVERNANCE.md §1):
- `[EVIDENCE]`: verified source. Two kinds are used here:
  - *CDC documentation* — an official CDC codebook page, opened and read on 2026-10-24.
  - *local descriptive check* — an aggregate count computed from the verified raw files, with no modelling.
- `[HYPOTHESIS]`: an expectation that has not been tested.
- `[RECOMMENDATION]`: an assistant proposal, pending approval.
- `[OPEN]`: an unresolved question, also listed in `research/reviews/unresolved_questions.md`.

**Status codes** used in the decision table (§24):

| Code | Meaning |
|---|---|
| **CUP** | Confirmed user preference: the researcher's stated research direction. Not a formal approval |
| **PMC** | Provisional methodological choice: an assistant proposal |
| **FA** | Requires formal approval in `DECISION_LOG.md` |
| **UTQ** | Unresolved technical question |
| **AB** | Activation blocker |

> **Citation rule.** Under `research_plan.md` §6, only `verified` inventory records may be cited. None of the references this protocol needs is a `verified` inventory record (Appendix D). Every literature statement here is therefore marked *candidate reference, not yet citable*. The method choices are justified provisionally by the data characteristics, and their literature justification is an activation blocker (AB-7).

---

## 1. Objective and research question

**Primary prediction task** `[RECOMMENDATION]`, built from CUP-2 to CUP-6:
- **Population:** US adults (≥20 years) in the NHANES fasting subsample without previously diagnosed diabetes.
- **Task:** estimate the probability of **laboratory-defined dysglycaemia** (HbA1c ≥ 5.7% or fasting plasma glucose ≥ 100 mg/dL) at a single examination.
- **Model:** fitted on NHANES 2017–March 2020 and evaluated once, frozen, on NHANES August 2021–August 2023 (temporal validation).

**Research question** (narrowed from `research_plan.md` §1, provisional, Q-016):
> For this task, do biochemical biomarkers add predictive information beyond simple clinical measurements? And can one prespecified framework give calibrated probabilities, valid uncertainty statements and stable explanations, with discrimination comparable to established baseline methods — on the development period and on a later NHANES period?

**Not claimed:**
- clinical diagnosis (one examination, no confirmatory test);
- incident (future) risk, since the data are cross-sectional;
- causal effects of biomarkers;
- external validation (§16);
- clinical utility;
- novelty (D-016, §11.3).

## 2. Confirmed user preferences (CUP)

These are the researcher's stated provisional direction (owner prompt, 2026-10-24). They fix the scope of this draft. **They are not entries in `DECISION_LOG.md`, and they do not approve D-013–D-020.**

| ID | Preference |
|---|---|
| CUP-1 | Empirical machine-learning research |
| CUP-2 | Initial task: laboratory-based dysglycaemia classification in adults using NHANES |
| CUP-3 | Development period: NHANES 2017–March 2020 (pre-pandemic) |
| CUP-4 | Temporal validation period: NHANES August 2021–August 2023 |
| CUP-5 | Candidate primary outcome: HbA1c ≥ 5.7% OR FPG ≥ 100 mg/dL. **Owner instruction, 2026-10-24 (PROTOCOL-DRAFT-002):** keep FA-2 as the *preferred proposed* primary outcome. This is a preference, not a formal approval. FA-2 remains pending formal approval (D-019/D-014, GOVERNANCE.md §2) and primary-source verification of the ADA criteria (§5.1) |
| CUP-12 | Owner instruction, 2026-10-24 (PROTOCOL-DRAFT-002): exclude hs-CRP from the primary predictor set until the cross-period conversion discrepancy is resolved. No unverified equation may be applied (§6.4) |
| CUP-6 | Three predictor groups: A biochemical-only, B biochemical + clinical, C clinical-only |
| CUP-7 | Participants previously told they have prediabetes stay in the primary sample; diabetes-awareness questionnaire variables are excluded from the predictors; a sensitivity analysis excludes participants told they have prediabetes |
| CUP-8 | Five or six literature-supported baselines against one proposed framework, with the choices justified by the literature and the data |
| CUP-9 | About 8–10 prespecified metrics, covering discrimination, calibration and uncertainty; any decision-utility metric must be justified |
| CUP-10 | Genuine, reproducible research: no manufactured results, no forcing performance into a range, no invented citations, no novelty claim without a defensible review |
| CUP-11 | Target: a defensible manuscript by 2026-11-24 |

## 3. Data sources

### 3.1 Files
32 official public-use XPT files: 16 components × 2 periods.
- **Component names:** DEMO, DIQ, GHB, GLU, FASTQX, INS, TCHOL, HDL, TRIGLY, BIOPRO, CBC, HSCRP, ALB_CR, BMX, BPXO, RXQ_RX.
- **File names:** `P_` prefix for 2017–March 2020, `_L` suffix for 2021–2023.
- **Source:** `https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{2017|2021}/DataFiles/<FILE>.xpt`. The documentation pages are the same path with `.htm`.

`[EVIDENCE: CDC documentation; local descriptive check]`:
- All 32 files returned HTTP 200 and are valid SAS transport files.
- All read with pandas.
- Every codebook data variable is present.
- `SEQN` is unique in every file except `P_RXQ_RX`, which has one row per medicine.
- SHA-256 hashes and sizes are in Appendix A. On 2026-10-24, all 32 re-hashed to the local manifest.

### 3.2 Terms of use
NHANES public-use files are federal public-domain data, released under NCHS conditions: statistical analysis only, no linkage to identify individuals, and no re-identification attempts. These terms come from search results; the NHANES-specific page has not been opened `[OPEN: Q-055]`. The repository is public, so raw and participant-level files are never committed (§22).

### 3.3 Unit of analysis
The unit is the participant (`SEQN`). NHANES is cross-sectional, so each participant appears once per period. `[EVIDENCE: local descriptive check]` No `SEQN` appears in both periods; the build will check this (§22).

## 4. Eligibility and exclusions

The rules are prespecified and applied identically in both periods. Codes are from the official codebooks `[EVIDENCE: CDC documentation]`.

| Step | Rule | 2017–Mar 2020 | 2021–2023 |
|---|---|---|---|
| E0 | All participants (`DEMO`) | 15,560 | 11,933 |
| E1 | Examined in the MEC (`RIDSTATR` = 2) | 14,300 | 8,860 |
| E2 | Age ≥ 20 at screening (`RIDAGEYR`) | 8,544 | 6,064 |
| E3 | In the fasting-glucose subsample file (`P_GLU` / `GLU_L`; all were in the morning session) | 4,252 | 3,425 |
| E4 | Fasting subsample weight > 0 (`WTSAFPRP` / `WTSAF2YR`): blood drawn **and** fasted 8 to <24 h | 3,801 | 2,958 |
| E5 | Valid FPG (`LBXGLU`) and valid HbA1c (`LBXGH`) | 3,791 | 2,956 |
| E6 | Exclude pregnancy at exam (`RIDEXPRG` = 1) | 3,759 | 2,938 |
| E7 | Exclude diagnosed diabetes: keep only `DIQ010` ∈ {2 No, 3 Borderline}. Drops `DIQ010` = 1, and 7, 9 or missing | 3,137 | 2,529 |
| E8 | Exclude current diabetes pills (`DIQ070` = 1) | **3,088** | **2,485** |

`[EVIDENCE: local descriptive check, 2026-10-24]` These are aggregate feasibility counts computed before any modelling. The analysis code must reproduce them exactly (§22), or the difference must be explained.

**Notes on the rules:**
- **E2, minimum age 20** `[RECOMMENDATION]`. It matches the adult-only variables (`DMDEDUC2`, `RIDEXPRG` 20–44). Age ≥ 18 would give 8,965 and 6,337 at step E2 (alternative; FA-1).
- **E4, zero-weight participants.** CDC notes that participants with glucose values but an invalid fast (268 and 311) would need reweighting to be included. They are excluded and their counts reported.
- **E7, borderline answers kept** (CUP-7). `DIQ010` = 3 records "borderline", not diagnosed diabetes. 90 participants per period are retained this way.
- **E8, pill question routing** `[EVIDENCE: CDC documentation]`. `DIQ070` is asked only if `DIQ010` = 1, `DIQ010` = 3, or `DIQ160` = 1 (check item DIQ065), identically in both periods. E8 therefore removes borderline or told-prediabetes participants who take glucose-lowering pills. Their measured glycaemia is treatment-affected. Excluding them is `[RECOMMENDATION]`; FA-3.
- **`DIQ050` (insulin)** is asked only if `DIQ010` = 1, so E7 already covers it.
- **Prescription data** are not used for eligibility in the primary analysis. 2021–2023 has no drug names (`RXQ_RX_L` holds only `RXQ033` and `RXQ050`), so a name-based rule could not be applied in both periods. A development-only check is sensitivity analysis S-07.
- **No other exclusions.** Valid observations are not removed for being outliers (`research_integrity.md` §3).
- **Flow diagram.** Each excluded count is reported in a participant-flow diagram for each period.

## 5. Outcome

### 5.1 Primary outcome (CUP-5)
**Status:** the owner's **preferred proposed** primary outcome (owner instruction 2026-10-24, PROTOCOL-DRAFT-002). It is **not approved**: FA-2 is still pending formal approval (outcome definition is reserved for the researcher, GOVERNANCE.md §2; D-019, D-014), and the ADA source has not been verified (see the evidence-status bullet below).
```
y = 1  if LBXGH >= 5.7  or  LBXGLU >= 100      (both measured; HbA1c in %, FPG in mg/dL)
y = 0  if LBXGH <  5.7  and LBXGLU <  100
```
- **Both measurements are required (E5).** The outcome is never imputed. If only one test is present, positives can be confirmed but negatives can't, so imputing would bias the label.
- **What the outcome identifies:** participants who meet **either** laboratory criterion (HbA1c ≥ 5.7% or FPG ≥ 100 mg/dL) at a single examination. It is a laboratory classification and **must not be described as a clinical diagnosis** of prediabetes or diabetes.
- **Thresholds are fixed.** They will not be changed after any model result is seen.
- **Evidence status `[OPEN]`.** The thresholds are *intended* to match the prediabetes lower limits in ADA Standards of Care 2026, Section 2 (candidate reference CR-08). That correspondence, and the statement that each test is an independent criterion, are **provisional**:
  - The PubMed record exists (PMID 41358893).
  - The full text returned empty on 2026-10-24, so the criteria have not been read in the primary source.
  - CR-08 is not a `verified` inventory record.
- **Undiagnosed-diabetes range.** Participants with HbA1c ≥ 6.5% or FPG ≥ 126 mg/dL are in the positive class. They are reported as a descriptive subgroup (201 and 136).
- **Name.** The outcome is "laboratory-defined dysglycaemia at a single examination", not a clinical diagnosis. A single survey examination provides no repeat or confirmatory testing. `[OPEN]` ADA guidance is understood to require confirmation for a clinical diagnosis of diabetes. That understanding comes from secondary summaries; the primary text (CR-08) has not been read, so the statement is **provisional**.
- **Laboratory category vs clinical diagnosis** (revision 3). The outcome assigns a *laboratory-defined glycaemic category* from one HbA1c and one FPG measurement at one survey visit. It is **not a clinical diagnosis**: there is no repeat or confirmatory test, no clinical assessment and no symptom information. Reports must use "meets laboratory criteria" or "laboratory-defined dysglycaemia", never "has prediabetes" or "has diabetes".
- **The OR rule includes the diabetes range** (revision 3). y = 1 covers participants whose values fall in the prediabetes range **and** those in the diabetes range (HbA1c ≥ 6.5% or FPG ≥ 126 mg/dL; 201 and 136 participants, §5.2).
  - The population excludes self-reported diagnosed diabetes (E7) and current diabetes pills (E8), so diabetes-range participants are *undiagnosed* and *unconfirmed*.
  - The outcome is therefore "any laboratory dysglycaemia" (prediabetes range or diabetes range), not "prediabetes". Separating the two is only the exploratory three-class analysis S-05.
- **Internal consistency of population and outcome** (revision 3 check; no definition changed):
  1. E7/E8 remove people who report diagnosed diabetes or pill use, consistent with an outcome for *previously undetected* dysglycaemia.
  2. Insulin use (`DIQ050`) is asked only of `DIQ010` = 1, so it is already covered by E7.
  3. Borderline (`DIQ010` = 3) and told-prediabetes (`DIQ160` = 1) participants are retained by design (CUP-7). Their awareness questions are not predictors, and S-04 removes them.
  4. There is no upper exclusion: the diabetes range stays in the positive class (above).
  5. Both measurements are required (E5), so no participant is labelled from one test.
  6. Known gap, unchanged: undisclosed glucose-lowering treatment without a diagnosis cannot be identified in 2021–2023 (no drug names), and only in 2017–2020 by S-07.

  The target population and outcome are **unchanged** in revision 3.
- **ADA source verification attempt** (2026-10-24, PROTOCOL-EVIDENCE-001): **not completed.** None of the official article page (`diabetesjournals.org`), `doi.org`, PubMed Central or Europe PMC could be reached from the environment (no connection, ENOTFOUND), and the PubMed full-text tool returned an empty text. The ADA criteria, the "each test independent" statement and the confirmation guidance therefore remain **unverified** (§5.1 evidence status; CR-08). No ADA table or section number is recorded as verified.
- **Lab values.** No cross-period adjustment is applied to `LBXGH` or `LBXGLU` (§8).

### 5.2 Observed outcome distribution
`[EVIDENCE: local descriptive check]`:

| | 2017–Mar 2020 (N = 3,088) | 2021–2023 (N = 2,485) |
|---|---|---|
| y = 1, unweighted | 2,007 (65.0%) | 1,462 (58.8%) |
| y = 1, fasting-weighted | 62.6% | 54.3% |
| HbA1c only / FPG only / both / neither | 240 / 914 / 853 / 1,081 | 210 / 713 / 539 / 1,023 |

- **Majority class.** The primary outcome is the majority class in both periods, and most positives come from FPG 100–125 mg/dL alone.
- **Lower 2021–2023 prevalence.** Median FPG in the analytic samples is 101 vs 100 mg/dL, even though CDC reports no change in glucose method or equipment.
  - *Correction (revision 2):* v0.1 stated "103 vs 101 mg/dL". Those are the medians of a broader reference population (adults ≥ 18 in the fasting subsample with valid FPG and HbA1c, not pregnant, diagnosed diabetes **not** excluded), not of the analytic samples.
  - Both pairs are reproduced by `scripts/nhanes/descriptive_counts.py`.
- **These are outcome-distribution findings, not model-performance results.** Whether the CUP-5 definition stays primary is the researcher's decision (FA-2). It must be made **before** freeze and must not be revisited after results are seen.
- **Development vs temporal-validation differences** `[EVIDENCE: local descriptive check]`. Fasting-weighted prevalence of the primary outcome is 62.6% in 2017–March 2020 and 54.3% in 2021–2023, a difference of 8.3 points. Under the HbA1c-only definition (S-01) it is nearly stable (27.2% vs 26.0%). So the between-period difference sits mainly in the FPG component.
  - This is a property of the outcome distribution in two separately sampled periods. It is **not** evidence about any model.
  - Its cause (population change, design change, fasting or pre-analytical factors) is not established `[OPEN]`.
  - It is reported in the shift diagnostics (§16) and kept separate from internal (development-period) results.

### 5.3 Outcome-related sensitivity analyses
All prespecified; not chosen by performance.

| ID | Variation | Purpose |
|---|---|---|
| S-01 | HbA1c-only: y = 1 if HbA1c ≥ 5.7%; y = 0 if HbA1c < 5.7%. Same fasting analytic sample as the primary analysis (FPG ignored) | Raised average glycaemia over about 2–3 months, detectable without fasting. Note that red-cell indices in group A (Hb, MCV, RDW) can relate to HbA1c measurement validity, not only to glycaemia (§17) |
| S-02 | FPG-only outcome (≥ 100 mg/dL) | Isolates the dominant contributor |
| S-03 | y = 1 if HbA1c ≥ 5.7% **or** FPG ≥ 110 mg/dL; y = 0 if HbA1c < 5.7% **and** FPG < 110 mg/dL. Participants with FPG 100–109 and HbA1c < 5.7% become negative (664 and 547) | Same either-test question with the stricter FPG limit used for impaired fasting glucose outside the ADA. The WHO source (candidate reference CR-09) is **not located or verified**, so this justification is provisional |
| S-15a | Both tests, discordant = negative: y = 1 if HbA1c ≥ 5.7% **and** FPG ≥ 100 mg/dL; y = 0 otherwise. **Discordant participants (one test above threshold, the other below) are kept and labelled negative.** Same population as the primary analysis | Concordant dysglycaemia, the most specific laboratory phenotype |
| S-15b | **Exploratory.** Both tests, discordant excluded: as S-15a, but **discordant participants are removed** (leaves 1,934 and 1,562) | Separation between concordant-positive and concordant-negative participants. **Excluding discordant participants removes the hardest-to-classify cases, so apparent discrimination may be inflated.** The analysed population also differs from the primary analysis. Not used for any comparison with the primary results |
| S-04 | Exclude participants told they have prediabetes (`DIQ160` = 1) **and** borderline participants (`DIQ010` = 3) (CUP-7). Leaves 2,630 and 2,054 | Detection among people with no prior awareness, so that awareness-driven behaviour cannot inflate associations |
| S-05 | Exploratory three-class outcome: normoglycaemia / prediabetes range / undiagnosed-diabetes range | Labelled exploratory. The diabetes class is small (201 and 136) |

**Label distributions** `[EVIDENCE: local descriptive check, 2026-10-24]`. These are outcome-distribution findings, **not model results**.

| Definition | 2017–Mar 2020 (N = 3,088): positive, unweighted / fasting-weighted | 2021–2023 (N = 2,485): positive, unweighted / fasting-weighted |
|---|---|---|
| Primary | 2,007 (65.0%) / 62.6% | 1,462 (58.8%) / 54.3% |
| S-01 | 1,093 (35.4%) / 27.2% | 749 (30.1%) / 26.0% |
| S-03 | 1,343 (43.5%) / 36.7% | 915 (36.8%) / 32.0% |
| S-15a | 853 (27.6%) / 21.7% | 539 (21.7%) / 18.4% |
| S-15b (exploratory) | 853 of 1,934 (44.1%) | 539 of 1,562 (34.5%) |

None of these definitions may be promoted to primary because of model performance (§5.2).

## 6. Predictors

### 6.1 Candidate feature lists
Conventional-unit variables are used, and the SI duplicates are not.
- **Variable names and units:** `[EVIDENCE: CDC documentation]`.
- **Choice of variables:** `[RECOMMENDATION]` (FA-4).

**Group A — biochemical-only (21 variables; hs-CRP removed in revision 1, §6.4)**

| Domain | Variables (unit) | Source |
|---|---|---|
| Liver | ALT `LBXSATSI` (IU/L), AST `LBXSASSI` (IU/L), GGT `LBXSGTSI` (IU/L), ALP `LBXSAPSI` (IU/L), total bilirubin `LBXSTB` (mg/dL), albumin `LBXSAL` (g/dL), total protein `LBXSTP` (g/dL) | BIOPRO |
| Kidney and urate | creatinine `LBXSCR` (mg/dL), BUN `LBXSBU` (mg/dL), uric acid `LBXSUA` (mg/dL), urine albumin-to-creatinine ratio `URDACT` (mg/g) | BIOPRO, ALB_CR |
| Lipids | total cholesterol `LBXTC` (mg/dL), HDL-C `LBDHDD` (mg/dL), triglycerides, reference method (2017–20 `LBXTR`, 2021–23 `LBXTLG`, mg/dL, harmonised per §8) | TCHOL, HDL, TRIGLY |
| Blood count | WBC `LBXWBCSI`, neutrophil count `LBDNENO`, lymphocyte count `LBDLYMNO` (1000 cells/µL), haemoglobin `LBXHGB` (g/dL), MCV `LBXMCVSI` (fL), RDW `LBXRDW` (%), platelets `LBXPLTSI` (1000 cells/µL) | CBC |

**Group C — clinical-only (6 variables):** age `RIDAGEYR`, sex `RIAGENDR`, BMI `BMXBMI`, waist `BMXWAIST`, and systolic and diastolic blood pressure (mean of the available oscillometric readings `BPXOSY1–3` and `BPXODI1–3`).

**Group B — A + C (27 variables).**

**Clarifications on group A:**
- **Strictly biochemical** `[RECOMMENDATION]`: no age or sex. A variant **A′ = A + age + sex** is a design alternative (FA-4, Q-050). A′ separates "biochemistry" from "biochemistry plus demographic context".
- **eGFR is not used**, because the CKD-EPI equation includes age and sex, which would bring demographics into group A. Creatinine is used instead.

**Excluded from the primary feature sets, with reasons:**
- serum glucose `LBXSGL` (direct leakage, §7);
- biochemistry-panel cholesterol `LBXSCH` and triglycerides `LBXSTR` (duplicates of the reference-method lipids; CDC recommends the reference variables);
- calculated LDL-C (derived from TC, HDL and TG; Friedewald and Martin-Hopkins are invalid at TG > 400);
- electrolytes, osmolality, CPK, LDH, iron, phosphorus, calcium, globulin, magnesium. Reasons: no prespecified hypothesis linking them to the outcome; magnesium exists only in 2021–23; and the bridging is weaker for several (r = 0.645 sodium, 0.846 calcium, 0.891 chloride, 0.922 potassium) `[EVIDENCE: CDC documentation, BIOPRO_L]`. An extended panel is sensitivity analysis S-11.

**Race/ethnicity and income** (`RIDRETH3`, `INDFMPIR`) are **not predictors** in the primary analysis. They are used for subgroup reporting of calibration and error rates (§14) `[RECOMMENDATION]`; FA-4. Note that 2021–2023 has no oversampling by race/ethnicity or income `[EVIDENCE: CDC documentation, DEMO_L]`, so subgroup precision is lower.

### 6.2 Complete cases per group
`[EVIDENCE: local descriptive check]`:

| | A (21) | C (6) | B (27) |
|---|---|---|---|
| 2017–Mar 2020 (N = 3,088) | 2,970 | 2,758 | 2,674 |
| 2021–2023 (N = 2,485) | 2,305 | 2,354 | 2,194 |

Revision 1 recomputed these counts without hs-CRP. With hs-CRP, the v0.1 counts were A (22) 2,963 / 2,305 and B (28) 2,669 / 2,194.

Per-variable missingness is ≤ 5.3%. The exception is blood pressure in 2017–2020, at 8.6% for the first reading; the averaged value may be lower.

### 6.3 Fasting insulin
`LBXIN` is **excluded from the primary feature sets**. It enters only in sensitivity analysis S-06 (A + insulin, B + insulin). Reasons:
1. It is closely tied to glucose regulation, so its inclusion moves the model towards a HOMA-like index (§7).
2. It is not a routine clinical test.
3. No official cross-period equation was found (`INS_L` and `P_INS` give none) `[EVIDENCE: CDC documentation]`, so comparability between periods is not established (Q-047).

Until Q-047 is resolved, any temporal-validation result involving insulin is labelled **exploratory**.

### 6.4 hs-CRP: excluded from the primary predictor set
**Owner instruction, 2026-10-24 (CUP-12).** hs-CRP (`LBXHSCRP`, mg/L) is **removed from groups A and B** until the cross-period conversion discrepancy (Q-045) is resolved. **No unverified conversion equation may be applied.**

**The unresolved issue** `[EVIDENCE: CDC documentation, read 2026-10-24]`. On `HSCRP_L.htm`:
- the bridging passage describes "the HSCRP results (mg/dL)";
- its equations are written in instrument terms ("Cobas 8000", "Cobas 6000"), not in variable names.

Every other official statement found uses mg/L:
- the variable `LBXHSCRP` is "(mg/L)";
- the 2021–2023 method manual (HSCRP-L-MET) reports mg/L (analytical range 0.15–20 mg/L; reportable range 0.15–600 mg/L);
- the 2017–2018 and 2019–2020 method manuals (HSCRP-J-MET, HSCRP-K-MET) also report mg/L.

Two further gaps:
- The stated "14.28% higher" average cannot be reproduced without the bridging data, which are not published.
- No applicable concentration range is stated. The earlier 2017–2018 bridging in `HSCRP_J` limited its equations to ≤ 20 mg/L.

Numeric plausibility is **not** used to decide the units. Status: **unresolved**.

**Second unresolved point** `[OPEN]`. `HSCRP_L` says the Cobas 6000 "was upgraded to the Cobas 8000 … during the cycle". The 2021–2023 values may therefore come from both instruments, and the public file has no per-participant instrument indicator. Even with confirmed units, which 2021–2023 values a conversion should apply to is unclear.

**Conditional sensitivity analyses** (§19):
- **S-16a, development period only:** hs-CRP is added to groups A and B for **internal validation within 2017–March 2020 only**.
  - Both 2017–2020 method manuals (HSCRP-J-MET, HSCRP-K-MET) name the Roche Cobas 6000, so no cross-period conversion is involved.
  - Its results are not compared with temporal-validation results.
- **S-16b, temporal validation with hs-CRP:** **conditional on resolving Q-045** (units, applicable range and the instrument-change timing). If unresolved at freeze, S-16b is **not run**. It is never run with an assumed equation.

## 7. Leakage audit of variables

| Category | Variables | Rule |
|---|---|---|
| Direct outcome variables | `LBXGH`; `LBXGLU`, `LBDGLUSI` | Never predictors |
| Other glucose measurements | `LBXSGL`, `LBDSGLSI` (serum glucose, biochemistry panel); OGTT (not collected after 2015–16) | Never predictors |
| Derived glycaemic indices | HOMA-IR/β, QUICKI, TyG, TyG-BMI/WC, METS-IR, CTI, eGDR (uses HbA1c), SPISE, glucose/insulin ratios | Never predictors (all contain glucose, HbA1c or insulin) |
| Diabetes-awareness questionnaire | All `DIQ*` / `DID*` items, including `DIQ010`, `DIQ160`, `DIQ180`, `DIQ050`, `DIQ070`, `DID040` | Never predictors (CUP-7). Used only for eligibility (E7, E8) and S-04 |
| Medication | `RXQ*` / `RXD*` | Never predictors. Used only in S-07 |
| Survey and processing variables | `SEQN`, weights, `SDMVSTRA`, `SDMVPSU`, `RIDEXMON`, fasting duration, session, comment codes (`*LC`) | Never predictors. Fasting duration and session are eligibility only |

**Build-time check** `[RECOMMENDATION]`: an automated test fails if any variable from this table appears in a feature matrix.

## 8. Cross-period measurement harmonisation

**Principle** `[RECOMMENDATION]` (FA-5): the model is fitted on the 2017–2020 measurement scale. Before temporal validation, the 2021–2023 values are mapped back to that scale using **CDC's published backward equations**. Both are applied by script, never by hand. Two sensitivity analyses check the effect:
- **S-08:** apply the unadjusted 2021–2023 values;
- **S-09:** apply the forward equations to the 2017–2020 values and refit.

| Variable | 2021–23 change | CDC recommendation | Backward equation (2021–23 → 2017–20 scale) | Unit status |
|---|---|---|---|---|
| HbA1c `LBXGH` (outcome) | Tosoh G8 → Bio-Rad D-100 during cycle; bridging n = 201, r = 0.999, Tosoh 2.3% higher | **No adjustment** | — | n/a. Residual bias near the 5.7% cut-off is a limitation |
| FPG `LBXGLU` (outcome) | None (Cobas C311 2017–2023) | **No adjustment** | — | n/a |
| Triglycerides | Glycerol-blanked → non-blanked method; Cobas 6000 → 8000; bridging n = 89, r = 0.999 | Equations provided "for analytic use" | `LBXTR = −12.19 + 0.9785 × LBXTLG` | **Provisional.** The equation is written in the variable names `LBXTLG`/`LBXTR`, which the codebooks define in mg/dL, and the 2021–2023 method manual reports mg/dL (9–885 mg/dL). One prose label says "(mg/L)", so a written contradiction remains. Not applied until Q-044 is decided (FA-5) |
| hs-CRP `LBXHSCRP` | Cobas 6000 → 8000 "during the cycle"; bridging n = 150; Cobas 6000 stated 14.28% higher | Equations provided | **None applied.** CDC's equation is not used | **Unresolved** (Q-045): the prose says "(mg/dL)", but the variable and all method manuals use mg/L; no applicable range; instrument-change timing unknown. hs-CRP is **excluded from the primary predictor set** (§6.4) |
| Urine albumin `URXUMA`/`URXUMS` | Fluorescein immunoassay → LC-MS/MS; bridging n = 195; new method 6.20% higher | Equations provided | `Old = −1.643 + 1.189 × New` (mg/L) | Stated in mg/L, consistent with `URXUMS`. `URDACT` is recomputed from adjusted albumin and urine creatinine. Q-046 (recomputation formula) |
| Urine creatinine | Cobas 6000 → 8000, r = 0.999 | **No adjustment** | — | n/a |
| ALT `LBXSATSI` | Cobas 6000 → 8000 | **Adjust** | `Y6000 = −1.529 + 1.035 × X8000` | Per-variable unit IU/L in CDC table |
| ALP `LBXSAPSI` | same | **Adjust** | `Y6000 = 0.6098 + 0.9041 × X8000` | IU/L |
| GGT `LBXSGTSI` | same | **Adjust** | `Y6000 = 0.9735 + 0.9444 × X8000` | IU/L |
| BUN `LBXSBU` | same | **Adjust** | `Y6000 = 0.09386 + 1.021 × X8000` | mg/dL |
| Total bilirubin `LBXSTB` | same | **Adjust** | `Y6000 = 0.01793 + 1.012 × X8000` | mg/dL |
| AST, albumin, total protein, creatinine, uric acid | same | **Adjustment not recommended** | — | — |
| Total cholesterol, HDL | Cobas 6000 → 8000; r = 0.998 / 0.997 | **No adjustment** | — | — |
| CBC | None (DxH 800) | None | — | — |
| Fasting insulin | No equation published | Not established | — | Q-047 (S-06 exploratory) |
| BMI, waist, blood pressure | Same protocol and device (oscillometric Omron HEM-907XL) in both periods per the codebooks | None | — | — |

Equation text was transcribed from the official pages `BIOPRO_L.htm`, `TRIGLY_L.htm`, `HSCRP_L.htm` and `ALB_CR_L.htm`, retrieved 2026-10-24 (Appendix B). Before freeze, each equation must be re-checked character by character against the page (AB-9).

### 8.1 Unit-consistency checks
`[EVIDENCE: local descriptive check, 2026-10-24]`. These are aggregate numbers only, and they don't replace confirmation from NCHS.
- **Triglycerides.** The within-person difference between reference-method and biochemistry-panel triglycerides is −14.0 mg/dL (median) in 2017–2020.
  - In 2021–2023, after mapping the panel value to the Cobas 6000 scale with its own equation, the difference is +0.9 mg/dL.
  - After applying the backward equation **read in mg/dL**, it becomes −13.3 mg/dL, reproducing the 2017–2020 relation.
  - Read in mg/L (intercept −1.219), it becomes −2.4 mg/dL.
  - Conclusion: consistent with the mg/dL reading. This numeric check is **supporting only**; the units question rests on the documentary evidence in the §8 table. Status: provisional, not confirmed (Q-044).
- **hs-CRP.** Applied to the 2017–2020 distribution with values taken as stored in mg/L, the forward equation gives no non-positive predictions; the mean implied difference is 33.8% and the median 10.9%.
  - Read in mg/dL, it would give non-positive predicted values for 39.1% of participants, which is implausible.
  - The stated mean of 14.28% is not reproduced exactly; the bridging-sample distribution is not published.
  - Revision 1: these numbers are **not** used to decide the units, and the equation is not applied (§6.4). Q-045 remains unresolved.
- **Urine albumin.** The implied mean difference is 8.5% (median −1.1%) against the stated 6.20%. This is roughly consistent with the stated mg/L units.

### 8.2 Within-cycle instrument changes in 2021–2023 (revision 3)
`[EVIDENCE: CDC documentation, read 2026-10-24]`, from the official 2021–2023 codebook pages and method manuals.

**What the sources state:**

| Analyte | Exact statement on the 2021–2023 codebook page | CDC adjustment advice |
|---|---|---|
| HbA1c (`GHB_L`, outcome) | "During the cycle, the laboratory instrument changed from the Tosoh G8 to the Bio-Rad D-100." | None needed (bridging: Tosoh 2.3% higher) |
| hs-CRP (`HSCRP_L`) | "During the cycle, the laboratory equipment changed from the Cobas 6000 Analyzer to the Cobas 8000." | Equations given; units unresolved (§6.4) |
| Total cholesterol (`TCHOL_L`), HDL (`HDL_L`) | "the lab equipment used changed from the Cobas 6000 Analyzer to the Cobas 8000 during the cycle" | None needed |
| Triglycerides (`TRIGLY_L`) | "There was a change in the lab method … The glycerol blanked assay used in previous cycles were phased out by the manufacturer. In addition, the lab equipment used for the measurement was updated from the Cobas 6000 Analyzer to Cobas 8000"; bridging "from an instrument change in the August 2021 – August 2023 cycle" | Equations given (§8) |
| Biochemistry panel (`BIOPRO_L`) | "the lab equipment used for the measurements was updated from the Cobas 6000 Analyzer to Cobas 8000"; bridging "from an instrument change in the August 2021-August 2023 cycle" | Per analyte (§8) |

**Manuals.**
- The 2021–2023 manuals (`TRIGLY-L-MET`, `HSCRP-L-MET`) describe only the Cobas 8000. The triglyceride manual names only the non-blanked TRIGL reagent.
- The 2017–2018 and 2019–2020 manuals (`-J-MET`, `-K-MET`) describe the Cobas 6000; the triglyceride manuals also name the glycerol-blanked Trig/GB reagent.
- No document gives the date of the change, or which 2021–2023 specimens were measured before it.

**What remains unknown:**
- Which 2021–2023 records were measured on which instrument (and, for triglycerides, with which method).
- Whether the released 2021–2023 values are all on the new scale, or mixed.
- **Participant timing cannot be reconstructed:** the only exam-timing variable, `RIDEXMON`, gives a six-month season (November–April or May–October) without a year. Instrument timing is **not** inferred from the cycle label (Q-060).

**Impact on the study:**
- (a) **hs-CRP:** already excluded from the primary sets (§6.4).
- (b) **No-adjustment analytes** (HbA1c, total cholesterol, HDL, AST, albumin, total protein, creatinine, uric acid): timing does not change the analysis, because CDC advises no adjustment. The HbA1c instrument mix inside the validation period is a residual outcome-measurement limitation near the 5.7% threshold (§20).
- (c) **Analytes where CDC recommends or provides an equation** (triglycerides, ALT, ALP, GGT, BUN, total bilirubin): CDC describes the backward equations as a way to "ensure comparability between the August 2021-August 2023 cycle and previous years", i.e. a cycle-level analytic use. Whether applying them to **every** 2021–2023 record is correct depends on the unknown timing. Records measured before the change would be over-corrected.

**Recommendation** `[RECOMMENDATION]`, for researcher decision (FA-5; no status changed):
- Do not apply any cross-period equation by default until Q-060 is answered (NCHS enquiry: date of each change and whether the released values are mixed).
- Pending that, temporal validation is run on **unadjusted** 2021–2023 values. This promotes S-08 to the reference analysis.
  - **Unadjusted values are not established as comparable** with 2017–March 2020, or within the 2021–2023 cycle. The documented instrument/method transition (dates unknown), the triglyceride unit discrepancy (Q-044) and the unresolved participant-level timing (Q-060) remain limitations of the reference analysis, and must be reported as such.
- Applying CDC's backward equations at cycle level, as CDC describes, becomes a **sensitivity analysis** (S-09b), labelled "assumes all 2021–2023 values are on the new instrument/method".
- This changes no outcome or population; it changes the harmonisation proposal (FA-5), which needs researcher approval.

## 9. Preprocessing and missing data

All steps are fitted on training data only, inside one pipeline object per model (`research_integrity.md` §5) `[RECOMMENDATION]` (FA-6).
1. **Harmonisation** (§8) is applied to the 2021–2023 raw values before anything else. It is a fixed published transformation and is not fitted to data.
2. **Derived inputs:** the mean of the available blood-pressure readings (1–3). `URDACT` is recomputed only where albumin is adjusted (Q-046).
3. **Below-detection values:** the CDC fill value (LLOD/√2) is kept as documented. Comment codes are not predictors.
4. **Transformations:** prespecified log transforms (natural log of x + 1) for right-skewed analytes: triglycerides, urine albumin-to-creatinine ratio, ALT, AST, GGT, insulin in S-06, and hs-CRP in S-16a/S-16b only. They are used for scale-sensitive models (LR, SVM, MLP); tree models are invariant to them. Standardisation is fitted in-fold.
5. **Missing predictors (primary):** in-fold median imputation for continuous variables and mode for sex, plus binary missingness indicators for any variable with > 5% missing in the training data. Missingness is low (§6.2), so simple imputation is proportionate.
6. **Missing data sensitivity analyses:**
   - **S-10a:** complete-case analysis per predictor group (counts in §6.2).
   - **S-10b:** in-fold iterative (chained-equations) imputation.
7. **Outliers:** none removed. Values are used as reported.
8. **Class imbalance:** no resampling and no class weights in the primary analysis.
   - The positive class is the majority (§5.2), not a rare event.
   - Resampling or reweighting distorts predicted probabilities, which would interfere with the calibration aims.
   - A class-weighted ablation is AB-3 in §15.

## 10. Survey design and weighting

`[EVIDENCE: CDC documentation]` NHANES is a complex, multistage probability sample.
- **Fasting subsample:** the fasting weights (`WTSAFPRP`, `WTSAF2YR`) are the documented weights for analyses involving fasting glucose.
- **Variance estimation:** uses `SDMVSTRA` and `SDMVPSU`.
- **Combining cycles:** the `DEMO_L` documentation notes the 15-month gap after 2017–March 2020 and states that "Data users are urged to proceed with caution before combining August 2021-August 2023 with previous cycles to calculate cross sectional health estimates or conducting trend analysis" (read 2026-10-24). The plan does not combine the periods; it keeps them separate (development vs temporal validation).

**Proposal** `[RECOMMENDATION]` (FA-7):
- **Model fitting: unweighted.** The estimand is a prediction rule for individuals, and ML learners generally fit unweighted. A weighted-fitting sensitivity analysis (S-12, using normalised fasting weights as sample weights) checks whether this choice matters.
- **Primary performance: unweighted**, describing the analytic sample.
- **Secondary performance: fasting-weighted**, approximating the US non-institutionalised adult population without diagnosed diabetes. Weighted AUROC, Brier score and calibration measures use normalised weights.
- **Confidence intervals:**
  - Primary: participant-level bootstrap.
  - Secondary design-aware sensitivity analysis: a bootstrap that resamples PSUs within strata.
- **Descriptive population estimates** (prevalence, Table 1): fasting-weighted, with design-based standard errors from Taylor linearisation. The software implementation is to be verified (Q-052).
- **Clustering.** Participants in the same PSU share a location, and random splits ignore this.
  - Sensitivity analysis **S-13:** internal validation with folds grouped by stratum × PSU.
  - `[EVIDENCE: local descriptive check]` 2017–2020 has 49 such clusters in the analytic sample (minimum 28 participants, median 64), so grouped 5-fold splitting is feasible.
  - Household clustering cannot be identified from the public files.

## 11. Models

### 11.1 Baseline methods
Six baselines, each trained on groups A, B and C `[RECOMMENDATION]` (FA-8; D-018):

| # | Method | Why it is in the set (data characteristics) | Literature status |
|---|---|---|---|
| BL-1 | Penalised logistic regression (elastic net) | Reference model required by D-018; interpretable; usually well calibrated | Candidate references CR-01 to CR-04 report LR comparators (from abstracts; not yet citable) |
| BL-2 | Random forest | Nonlinear tabular baseline robust to scale and outliers | same |
| BL-3 | Gradient-boosted trees (XGBoost or LightGBM; Q-048) | Usually strong on tabular data; handles nonlinearity and interactions | same |
| BL-4 | Support vector machine (RBF kernel) with Platt scaling | Margin-based learner; widely used in the applied literature | same |
| BL-5 | Multilayer perceptron (one or two hidden layers) | Neural baseline at a scale suitable for n ≈ 3,000 | same |
| BL-6 | One of: k-nearest neighbours, or an inherently interpretable model such as an explainable boosting machine (Q-049) | k-NN is common in applied comparisons; an interpretable model is a fair comparator for the explainability aim | Not yet assessed |

**Activation blocker AB-7.** D-018 requires the baselines to be "methods most used in the included RQ1 studies". RQ1 screening has not started, and the screening workflow is inactive (§23). Until the candidate references are verified into the inventory, this baseline set is justified only provisionally, by the data characteristics.

### 11.2 Proposed framework
`[RECOMMENDATION]` (FA-9; D-017). A **calibrated, uncertainty-aware, explained classification pipeline**. It is defined before any results and is not modified after them.

| Component | Specification | Hypothesis `[HYPOTHESIS]` |
|---|---|---|
| F1 Preprocessing | §9, fitted in-fold | Prevents optimistic bias compared with whole-data preprocessing |
| F2 Classifier | Gradient-boosted trees (same family as BL-3), tuned with the same budget as the baselines (§12) | Discrimination comparable to the best baseline, not necessarily higher |
| F3 Post-hoc calibration | Platt (sigmoid) calibration fitted on the calibration split D-cal (§12). Isotonic regression is sensitivity analysis S-14 | Lower calibration error and a calibration slope closer to 1 than the uncalibrated classifier, with unchanged AUROC (monotone map) |
| F4 Uncertainty | Class-conditional (Mondrian) split conformal prediction on D-cal, target miscoverage α = 0.10 (Q-051), reporting prediction sets {0}, {1}, {0,1} | Coverage ≥ 0.90 in each class on the development data. On temporal validation, coverage may degrade under shift; how much is measured, not assumed |
| F5 Explanation | TreeSHAP attributions on the uncalibrated F2 margin. Global importance, direction, and **stability** (Spearman rank correlation of global importance across 50 bootstrap refits, and between periods) | The top-ranked biomarkers are stable across refits and periods. Explanations describe the model, not causation (`research_integrity.md` §12) |

- **Feature selection** is **not** a framework component in the primary specification. An in-fold selection variant is ablation AB-5.
- **Equal treatment.** F3 and F4 are also applied to every baseline in the comparison (§13). Any advantage of the framework must therefore come from the combination, not from calibration or conformal prediction being unavailable to the baselines (`research_integrity.md` §7).

### 11.3 Contribution and novelty
**No novelty claim is made.** Two of the closest candidate studies combine NHANES, ML and calibration, or SHAP:
- CR-02: non-laboratory prediabetes/diabetes model, NHANES 1988–2018, validated on NHANES 2021–2023 and KNHANES;
- CR-04: SHAP and calibration in a hepatitis B subgroup.

Both are `partially_verified` and not citable. Whether the combination proposed here is distinct can be judged only after the RQ5 closest-prior-art review (D-016, D-031–D-038, inactive). The manuscript contribution must be worded as the review supports.

## 12. Data partitioning and tuning

`[RECOMMENDATION]` (FA-6)

1. **Development (2017–March 2020, N = 3,088):** one stratified split (by outcome) into:
   - **D-train** (80%), used for fitting and tuning;
   - **D-cal** (20%), used only for fitting F3 and F4 for every model.

   The seed is fixed in the frozen configuration before any data are split.
2. **Tuning:** stratified 5-fold cross-validation on D-train.
   - **Tuning criterion:** log loss, a proper scoring rule. AUROC is not used, so that probability quality is not traded for ranking.
   - **Budget:** the same for every method — the same number of randomly sampled configurations (proposed: 40) from search spaces prespecified in the configuration file. Penalised LR uses its own small grid of comparable size.
3. **Internal performance:** out-of-fold predictions from the tuned configuration on D-train, reported as internal validation.
   - Repeated over **5 seeds** for the split and the CV folds.
   - Mean, SD and range are reported. No favourable seed is picked.
   - The primary seed is fixed in advance.
4. **Final models:** refit on all of D-train with the chosen configuration, then calibrated and conformalised on D-cal, then **frozen** (configuration, fitted objects and hashes logged).
5. **Temporal validation (2021–2023, N = 2,485):** frozen models applied **once** (§16). No tuning, threshold selection, recalibration or feature selection uses these data.
6. **Decision threshold for threshold-based metrics:** chosen on D-cal as the smallest probability threshold giving sensitivity ≥ 0.80 (Q-053, FA-10), then applied unchanged. A clinically justified threshold, if the literature supports one, would replace this before freeze.

## 13. Comparisons

Prespecified comparisons `[RECOMMENDATION]` (FA-11):
- **Q1, value of biochemistry:** B vs C, and A vs C, for the framework and for BL-1. This is the primary scientific comparison: does biochemistry add information?
- **Q2, framework vs baselines:** within group B, the framework vs each baseline after the baseline also receives F3 calibration ("calibrated baselines"). Uncalibrated baselines are also reported.
- **Q3, temporal transfer:** the change in each metric from internal to temporal validation, per model.

**Primary metric per question:**
- **Q1:** AUROC difference.
- **Q2:** the integrated calibration index (ICI) and the Brier score, with AUROC used for non-inferiority. The margin is a researcher decision (FA-11, Q-054) and must be fixed before freeze.

All other comparisons are secondary.

## 14. Evaluation metrics

Ten prespecified metrics `[RECOMMENDATION]` (FA-10). Each is computed on internal out-of-fold predictions and on the temporal-validation set, unweighted (primary) and fasting-weighted (secondary).

| # | Metric | Dimension | Justification |
|---|---|---|---|
| M1 | AUROC | Discrimination | Threshold-free ranking quality |
| M2 | AUPRC, with the prevalence shown as its baseline | Discrimination | Complements AUROC. Interpret with care at 59–65% prevalence |
| M3 | Brier score (and scaled Brier) | Overall probabilistic accuracy | Proper scoring rule; combines calibration and discrimination |
| M4 | Calibration intercept (calibration-in-the-large) | Calibration | Detects systematic over- or under-prediction; key under prevalence shift |
| M5 | Calibration slope | Calibration | Detects overfitting (too extreme) or underfitting |
| M6 | Integrated calibration index (ICI), with a binned ECE as secondary | Calibration | Summary of the smoothed calibration curve; less bin-dependent than ECE. Calibration curves shown graphically |
| M7 | Sensitivity and specificity at the D-cal threshold (§12.6) | Classification at a fixed threshold | Interpretable error rates. The threshold is fixed before validation |
| M8 | Conformal coverage: marginal and per class | Uncertainty validity | Tests whether nominal 90% coverage holds, especially under temporal shift |
| M9 | Conformal efficiency: mean set size, and the share of ambiguous {0,1} and empty sets | Uncertainty informativeness | Coverage alone can be met with uninformative sets |
| M10 | Net benefit over a threshold range (decision curve) | Decision utility | **Secondary.** Reported only over a range justified before freeze (Q-054). Without a justified range for this screening context, it is descriptive and not used for conclusions |

**Supporting, non-headline measures:**
- **Explanation:** SHAP global-importance stability (F5) and the agreement between SHAP direction and LR coefficient signs.
- **Subgroups:** M4–M7 by sex, age band (20–39, 40–59, ≥60) and race/ethnicity, labelled descriptive (small cells).

## 15. Statistical analysis

- **Temporal validation:** 95% CIs by participant bootstrap (2,000 resamples). Differences between models use paired bootstrap of the difference on the same resamples.
- **Multiplicity:** Holm adjustment within Q2 (framework vs 6 calibrated baselines) for each primary metric. Q1 and Q3 comparisons are few and prespecified; unadjusted CIs are reported with that stated.
- **Internal CV:** mean ± SD over folds and seeds. No naive t-tests on overlapping folds. If a test is needed, a corrected resampled test is used (candidate reference CR-10, not yet citable).
- **Ablations** (framework, group B, development internal and temporal):

  | ID | Ablation |
  |---|---|
  | AB-1 | Without F3 |
  | AB-2 | Without F4 (point predictions only) |
  | AB-3 | Class-weighted training |
  | AB-4 | F2 replaced by penalised LR, keeping F3–F5 |
  | AB-5 | In-fold feature selection added (L1 or stability selection) |

- **Sensitivity analyses** S-01 to S-14 are listed in §19. None changes the primary analysis after results are seen.
- **Sample size.** `[EVIDENCE: local descriptive check]` Development has 2,007 events and 1,081 non-events for up to 27 candidate predictors in the primary sets, about 40 per predictor in the smaller class. A formal minimum-sample-size calculation (candidate reference CR-07, not yet citable) is part of freeze (Q-056).
- **Logging.** Every run, including failed and discarded runs, is logged in `logs/EXPERIMENT_LOG.md` (`research_integrity.md` §6).

## 16. Temporal validation

- **What it is:** a later, separately sampled NHANES period, the same survey programme and protocol, 15 months later, after pandemic-era design changes. The models, preprocessing, calibration, conformal sets and threshold are frozen on 2017–2020.
- **What it is not:** independent external validation (`research_integrity.md` §11; D-015). It doesn't show generalisation to other countries, health systems, clinical populations or laboratory systems.
- **Known differences** `[EVIDENCE: CDC documentation; local descriptive check]`:
  - no oversampling by race/ethnicity or income in 2021–2023, and age oversampling added;
  - instrument and method changes (§8);
  - a new phlebotomy weight (`WTPH2YR`), not needed for the fasting analyses;
  - the session code changed (`PHDSESN` → `PHDSESNZ`; afternoon and evening merged);
  - outcome prevalence lower by 6.2 percentage points unweighted (8.3 fasting-weighted). This is an outcome-distribution finding, concentrated in the FPG component (§5.2).
- **Shift diagnostics, prespecified:**
  - standardised mean differences of every predictor;
  - outcome prevalence;
  - calibration-in-the-large;
  - conformal coverage by class.
- **Updated models are reported separately.** A model updated on validation data (intercept recalibration) is exploratory and labelled "updated, not validation".
- **Fair comparison:** identical inputs, harmonisation and evaluation for every model. Conclusions focus on relative behaviour and calibration drift, not only absolute AUROC.

## 17. Explainability evaluation
- **Methods:** TreeSHAP for tree models (F5, BL-2, BL-3), coefficients for BL-1, permutation importance as a model-agnostic cross-check.
- **Reported:** global importance with bootstrap intervals; rank stability across refits and between periods; dependence plots for the top features.
- **Interpretation:** explanations are model descriptions only. Associations with dysglycaemia are not interpreted causally, and biomarkers affected by treatment, such as statin effects on lipids, are noted.

## 18. Uncertainty evaluation
- **Development:** `[HYPOTHESIS]` Split conformal prediction is generally described as giving finite-sample coverage under exchangeability of calibration and test data. **The source and its exact assumptions are not yet verified** (CR-12; for class-conditional sets, the conditions per class also need checking). No validity guarantee is claimed in this protocol: coverage is **measured**, on internal out-of-fold data with a nested calibration split (Q-051).
- **Temporal validation:** exchangeability is not assumed. Observed coverage is an empirical finding.
- **Not part of this protocol:** weighted or shift-adaptive conformal variants. If explored, they are exploratory.

## 19. Sensitivity analyses (prespecified)

| ID | Analysis |
|---|---|
| S-01 | HbA1c-only outcome |
| S-02 | FPG-only outcome |
| S-03 | FPG ≥ 110 or HbA1c ≥ 5.7 outcome |
| S-04 | Exclude told-prediabetes and borderline participants (CUP-7) |
| S-05 | Exploratory three-class outcome |
| S-06 | Fasting insulin added to groups A and B (temporal part exploratory, §6.3) |
| S-07 | Development only: also exclude participants with a glucose-lowering drug name in `P_RXQ_RX`. 15 such participants found, metformin and liraglutide. The drug list is fixed before freeze (Q-057) |
| S-08 | Temporal validation with unadjusted 2021–2023 laboratory values |
| S-09 | Forward-equation harmonisation (2017–2020 → 2021–2023 scale) |
| S-09b | *Proposed in revision 3 (§8.2), pending FA-5:* CDC backward equations applied at cycle level to all 2021–2023 records of triglycerides, ALT, ALP, GGT, BUN and total bilirubin. Labelled "assumes all 2021–2023 values are on the new instrument/method" (Q-060). Never applied to hs-CRP while Q-045/Q-059 are open. **Not executed.** Any future execution requires FA-5 approval and further documented methodological justification (units: Q-044; record-level applicability: Q-060) |
| S-10a | Complete-case analysis |
| S-10b | Iterative imputation |
| S-11 | Extended biochemistry panel (§6.1 exclusions added back, except leakage variables and magnesium) |
| S-12 | Survey-weighted model fitting |
| S-13 | Internal validation grouped by stratum × PSU |
| S-14 | Isotonic instead of Platt calibration |
| S-15a | Both-tests outcome, discordant participants labelled negative (§5.3) |
| S-15b | **Exploratory.** Both-tests outcome, discordant participants excluded. Apparent separability may be inflated (§5.3) |
| S-16a | hs-CRP added to groups A and B, **development-period internal validation only**, with no conversion (§6.4) |
| S-16b | hs-CRP in temporal validation: **conditional on resolving Q-045**. Not run, and never run with an assumed equation, while Q-045 is unresolved (§6.4) |
| — | Age ≥ 18 instead of ≥ 20, if FA-1 keeps 20 |

## 20. Limitations, stated in advance
- Cross-sectional data; a single-visit laboratory outcome with no confirmatory testing.
- The outcome is dominated by fasting glucose 100–125 mg/dL alone.
- Self-reported diagnosis and medication; undiagnosed people taking metformin can't be identified in 2021–2023.
- Residual instrument differences (HbA1c +2.3%) near the threshold. The HbA1c and chemistry-analyzer changes happened *within* the 2021–2023 cycle, at unknown dates (§8.2).
- Equation units not fully confirmed (Q-044, Q-045).
- Temporal validation is not external validation.
- Lower response rates and design changes in 2021–2023.
- Modest sample sizes for subgroups and for the undiagnosed-diabetes range.
- Survey weights used only in secondary analyses.
- Literature justification incomplete at the time of drafting (AB-7).

## 21. Reporting
- **Planned guideline:** TRIPOD+AI for prediction-model reporting (candidate reference CR-11, to be verified).
- **Claims register:** each number traceable along `claim → table → script + commit → output file → run ID → data hash` (`research_integrity.md` §9).

## 22. Reproducibility and data management

`[RECOMMENDATION]`. Creating the planned files needs separate authorization; none are created in this task.

- **Raw data:** `data/raw/nhanes/{2017-2020,2021-2023}/`, git-ignored, never committed. Provenance comes from the local manifest (URL, HTTP status, bytes, SHA-256, server last-modified date, access time).
- **Committed manifest (planned):** `data/manifest/nhanes_files.csv` with the same fields as Appendix A. It contains no participant data.
- **Acquisition script (planned):** a download script with the URL list from the official CDC listing pages. It verifies the SAS-transport header and SHA-256, and fails on any HTML response or hash mismatch.
- **Analytic-dataset build (planned):** a script that reads only raw files plus the frozen configuration (`configs/protocol_v1.0.yaml`) and writes to git-ignored `data/processed/`. It must reproduce the §4 cascade counts and record output hashes.
- **Participant-level outputs:** predictions, SHAP values and conformal sets must also stay out of Git.
  - `[EVIDENCE: repository inspection]` At v0.1, `.gitignore` covered only `data/raw/`, `data/interim/`, `data/processed/`, `*.xpt` and `outputs/tmp/`.
  - **Revision 1** (owner-authorized safeguards, PROTOCOL-DRAFT-002):
    - Rules appended to `.gitignore`:
      - XPT, SAS, Stata and RDS files in any letter case;
      - `/data/derived/`, `/outputs/participant_level/`, `/outputs/models/`, `/models/`;
      - parquet, feather, npy, npz, h5, hdf5, pkl, pickle and joblib files in any letter case.
    - Aggregate publication tables go in `outputs/aggregate/`, which is not ignored (`outputs/README.md`).
    - Checks in `tests/data_protection/test_data_protection.py`:
      - ignore rules for representative sensitive paths and legitimate paths;
      - sensitive formats;
      - participant-level directories;
      - SAS-transport content under any filename;
      - `SEQN` in CSV/TSV headers and JSON/JSONL keys.
    - The test docstring lists what the checks cannot detect.
  - The safeguards are in place but are part of this unapproved draft. AB-10 stays open until reviewed.
  - **Revision 2** (PROTOCOL-DRAFT-003):
    - More `.gitignore` rules:
      - SPSS `.sav` in any case;
      - ONNX, PyTorch (`.pt`, `.pth`), safetensors, CatBoost (`.cbm`) and UBJSON model files;
      - archives and spreadsheets under `/data/`; archives under `/outputs/`.
    - JSON is not ignored globally. JSON models are protected only inside the model and participant-level directories.
    - The tests gained content-signature checks (SAS transport, Parquet, NumPy, HDF5), a validated identifier allowlist (`tests/data_protection/identifier_allowlist.txt`), strict Git handling, and detector self-tests.
    - `sh scripts/run_checks.sh` runs all project checks.
- **Descriptive counts:** `scripts/nhanes/descriptive_counts.py` (revision 2) reproduces the aggregate counts in §4–§6, §8.1, §10 and S-07 from the hash-verified raw files. It prints aggregates only and trains or evaluates nothing (`scripts/nhanes/README.md`).
- **Environment:** Python 3.13 (D-002, proposed) with a pinned lock file. scikit-learn, SciPy and the gradient-boosting, SHAP and conformal packages are **not installed** `[EVIDENCE: local check]` and must be pinned before training (AB-11).
- **Seeds:** all prespecified in the configuration.
- **Clean-environment re-run:** before submission (Stage J).
- **Tests:** leakage tests (forbidden variables, fit-on-train-only), cascade-count tests, and harmonisation-equation tests. Synthetic fixtures may be used, clearly labelled as test data (`research_integrity.md` §1).

## 23. Milestones to 2026-11-24

`[RECOMMENDATION]` (relates to D-001, proposed; stage order follows D-042, proposed, Q-069). Dates are
targets, not gates: no gate is treated as passed because its date has arrived. The 2026-11-24 target
is under review (D-001, Q-013, Q-058); no research requirement is weakened to meet it.

| Order | Work | Gate or prerequisite | Target |
|---|---|---|---|
| 1 | Researcher decisions for screening activation (`research/reviews/screening_activation_decision_brief_D035.md` §8) | D-035 record §6 conditions 2–6 recorded | Q-065 by 11-01; others not fixed |
| 2 | Screening pilot (D-025, proposed), then screening of the agreed scope (Q-065) and full-text review | Screening activated by the researcher | Not fixed |
| 3 | Stage C: critical comparison of existing methods | **Stage C gate: comparison reviewed by researcher** | Not fixed |
| 4 | Stage D: closest-prior-art review, gap matrix, contribution | **Stage D gate: gap + main contribution approved (D-016)** | Not fixed |
| F | D-013, D-014 and the outcome definition (Stage F gate) | Researcher decisions; D-042 does not fix their timing. Needed before D-017 (its evidence requirement) and before training (AB-3) | Not fixed |
| P | In parallel with 1–4, preparatory only: protocol v0.2 draft; dataset feasibility documentation (evidence for D-013–D-015); environment setup proposal (D-002); leakage-test design; code scaffolding without fitting a model to real data; Rule S test planning (D-040; execution not before 2026-11-03 and only under an approved test plan, D-040 (7)) | No gate is passed; each edit is authorised as usual | Ongoing |
| 5 | D-017 (framework) and D-018 (baselines), then D-019 (protocol v1.0 frozen) | Stage C and Stage D gates passed (D-042); D-014 approved (D-017 evidence requirement); researcher approvals | After steps 4 and F |
| 6 | Stage G: baselines under the frozen protocol | §26 AB-1 to AB-13 met (AB-1: date ≥ 2026-11-03) | After step 5 |
| 7 | Stages H–J and the manuscript | Gates as in `GOVERNANCE.md` §2 | Under review |

**Risks:**
- About 1 hour a day of researcher time against roughly 15 decisions.
- No verified literature yet (AB-7).
- The RQ5 review is inactive, so the contribution wording must stay limited.
- Model training cannot start before steps 3–5 are complete. A manuscript with model results by 2026-11-24 is therefore at risk `[HYPOTHESIS]`, not measured.

**Fallback.** If the Stage C and Stage D gates have not passed in time for the 2026-11-24 target, the
researcher decides the deliverable (D-001). A possible interim deliverable is the protocol draft, the
literature review to date and a descriptive data-feasibility section, without model results. The
protocol is not frozen and no gate is passed to produce it.

## 24. Decision table

| ID | Choice | Status | Rationale | Approval needed |
|---|---|---|---|---|
| FA-1 | Minimum age 20 (alternative 18) | PMC | Adult-only variables; diagnostic thresholds are adult-based | Researcher, in D-014/D-019 |
| FA-2 | Primary outcome HbA1c ≥ 5.7 OR FPG ≥ 100, both measures required, no outcome imputation; S-01, S-03, S-15a and S-15b (exploratory) as outcome sensitivity analyses | CUP; **owner-preferred proposed outcome (2026-10-24)**. Still FA: **not approved**; ADA source not verified | Reserved decision; prevalence 59–65% and FPG-dominated (§5.2) | Researcher (outcome definition, GOVERNANCE.md §2) |
| FA-3 | Exclude `DIQ070` = 1 (pills) among non-diagnosed participants | PMC | Treated glycaemia; the question routing is identical in both periods | Researcher |
| FA-4 | Feature lists A (21), B (27), C (6); hs-CRP excluded from the primary sets (CUP-12); group A without age or sex (A′ alternative); race and income not predictors | CUP (groups, hs-CRP exclusion) + PMC (lists) | Leakage and comparability audit (§6–§8) | Researcher, in D-019 |
| FA-5 | Backward harmonisation of 2021–2023 lab values using CDC equations; S-08 and S-09 as sensitivity analyses. *Revision 3 recommendation (§8.2): unadjusted values as reference until Q-060 is resolved; cycle-level CDC equations as sensitivity S-09b* | PMC | Model frozen on the development scale; equations are official | Researcher, after Q-044 to Q-046 |
| FA-6 | In-fold preprocessing, median imputation plus indicators, 80/20 D-train/D-cal, log-loss tuning, equal budget, 5 seeds | PMC | `research_integrity.md` §4–§6 | Researcher, in D-019 |
| FA-7 | Unweighted fitting and primary metrics; weighted secondary; PSU-bootstrap and grouped-CV sensitivity analyses | PMC | Prediction estimand vs population inference (§10) | Researcher, in D-019 |
| FA-8 | Baselines BL-1 to BL-6 (BL-3 library: Q-048; BL-6: Q-049) | CUP (5–6 baselines) + PMC | Data characteristics; literature pending (AB-7) | Researcher, D-018 |
| FA-9 | Framework F1–F5 (gradient boosting + Platt + Mondrian conformal + TreeSHAP stability) | PMC | Covers classification, calibration, uncertainty and explanation | Researcher, D-017; contribution D-016 |
| FA-10 | Metrics M1–M10; threshold rule (sensitivity ≥ 0.80 on D-cal) | CUP (8–10) + PMC | §14 | Researcher, in D-019 |
| FA-11 | Comparisons Q1–Q3, primary metrics, non-inferiority margin, Holm correction | PMC | Prevents post-hoc selection | Researcher, in D-019 |
| FA-12 | Temporal validation as the only test of the frozen models; not called external | CUP + PMC | D-015; `research_integrity.md` §11 | Researcher, D-015 |
| FA-13 | Data handling and Git rules (§22), including `.gitignore` and the guard test | PMC | Public repository | Researcher (authorization to change `.gitignore`) |
| — | Primary disorder: dysglycaemia (T2D/prediabetes spectrum) | CUP | — | Researcher, D-013 |
| — | Primary dataset: NHANES 2017–March 2020 | CUP | Verified files (§3) | Researcher, D-014 |
| — | Target journal | Not addressed | — | D-020 |

## 25. Unresolved technical questions

Also recorded in `research/reviews/unresolved_questions.md`.

| ID | Question |
|---|---|
| Q-044 | Triglyceride bridging equation: CDC text states "(mg/L)" while `LBXTR`/`LBXTLG` are mg/dL. The local check supports mg/dL. Confirm with NCHS, or accept the mg/dL reading with the check documented? *Revision 1, still open:* provisional documentary evidence for mg/dL — the equation uses the variable names, and the method manual reports mg/dL (§8) |
| Q-045 | hs-CRP equation: text states "(mg/dL)", but `LBXHSCRP` is mg/L. Only the mg/L reading is plausible, but CDC's 14.28% mean difference is not reproduced (33.8% mean, 10.9% median). Confirm with NCHS; until then, is S-08 (unadjusted) the reference? *Revision 1, still open:* hs-CRP is excluded from the primary sets (CUP-12). Additional evidence needed: the instrument-change timing within 2021–2023 and the applicable range (§6.4) |
| Q-046 | Urine albumin harmonisation: which albumin variable (`URXUMA` µg/mL vs `URXUMS` mg/L, numerically equal) and what exact formula for recomputing `URDACT` after adjustment? |
| Q-047 | Fasting insulin cross-period comparability: no equation in `INS_L`/`P_INS`. Keep it exploratory (proposed), or search the NHANES methods documentation further? |
| Q-048 | BL-3 library: XGBoost vs LightGBM (or scikit-learn histogram GBM, fewer dependencies) |
| Q-049 | BL-6: k-NN vs an inherently interpretable model (e.g., an explainable boosting machine) |
| Q-050 | Group A strictly biochemical, or A′ = A + age + sex as the primary biochemical group? |
| Q-051 | Conformal settings: α = 0.10; class-conditional vs marginal; how internal coverage is checked without touching D-cal twice |
| Q-052 | Software for design-based (Taylor-linearised) standard errors in Python; to be verified and pinned |
| Q-053 | Decision threshold: the D-cal sensitivity ≥ 0.80 rule vs a literature-justified clinical threshold |
| Q-054 | AUROC non-inferiority margin for Q2, and the threshold range for net benefit (M10): which justification does the researcher accept? |
| Q-055 | Open and record the NHANES-specific data-use terms page (now reachable) |
| Q-056 | Formal minimum-sample-size calculation for the development set (method from a verified source) |
| Q-057 | Fixed glucose-lowering drug-name list for S-07 |
| Q-058 | Schedule: accept a 3-day compression of Stage J (11-24 vs 11-27 in D-001)? |
| Q-059 | hs-CRP instrument timing in 2021–2023 (no per-participant instrument indicator) |
| Q-060 | Within-cycle instrument/method timing for **all** Cobas-measured 2021–2023 analytes with CDC equations (triglycerides, ALT, ALP, GGT, BUN, total bilirubin; and hs-CRP), and for HbA1c: date of each change, and whether released values are mixed. Generalises Q-059. Needed to decide FA-5 (§8.2) |
| Q-061 | Access to the ADA 2026 Section 2 primary text (blocked from the environment): allow `diabetesjournals.org` (and `doi.org`), or the researcher supplies the PDF, to complete CR-08 verification |

## 26. Blocker checklist

**Before literature screening or a screening pilot.** These come from the existing records; this protocol does not change them.
- [ ] The remaining D-035 record §6 conditions: Q-040; D-027 and D-024; the remaining R5/D-029 items; screening criteria v1.1 and screening protocol v0.2 frozen as the pilot's `criteria_version`; "the other pilot-blocking items". Condition 1, Q-039, was met by D-036. Separately, the pilot design itself (D-025, Q-026) is still PROPOSED.
- [ ] D-031 to D-038 stay inactive until then.

**Before D-017, D-018 or D-019 is approved** (D-042, proposed; Q-069):
- [ ] Stage C gate passed: comparison of existing methods reviewed by the researcher.
- [ ] Stage D gate passed: gap and main contribution approved (D-016).

**Before model training** (AB = activation blocker):
- [ ] **AB-1** Date ≥ 2026-11-03 (Day 21; GOVERNANCE.md §2).
- [ ] **AB-2** D-019 approved by the researcher: protocol frozen and versioned (v1.0), including FA-1 to FA-13.
- [ ] **AB-3** D-014 (primary dataset) and the outcome definition approved (GOVERNANCE.md Stage F gate); D-013 approved.
- [ ] **AB-4** D-015 decided: temporal validation accepted, and the claims limited accordingly.
- [ ] **AB-5** D-017 and D-018 approved (framework and baselines).
- [ ] **AB-6** `research_integrity.md` approved (Q-018).
- [ ] **AB-7** Literature justification: the candidate references (Appendix D) verified into the inventory, and baseline, threshold and metric choices linked to verified records. A provisional, data-based justification does not replace the Stage C gate (D-042, proposed). *Revision 4 replaces the revision 3 sentence "Otherwise the researcher must explicitly accept the provisional, data-based justification."*
- [ ] **AB-8** Q-044 and Q-046 resolved, or the researcher accepts the documented fallback (S-08 as reference). For hs-CRP the fallback is exclusion from the primary sets (CUP-12). Resolving Q-045 is needed only for S-16b. *Revision 3:* Q-060 (within-cycle timing) must also be resolved, or the researcher must accept unadjusted values as the reference (§8.2), before any equation is applied.
- [ ] **AB-9** Equations re-checked character by character against the official pages.
- [ ] **AB-10** `.gitignore` rule for participant-level outputs and the `SEQN` guard test (authorization needed). *Revision 1:* implemented under owner authorization (§22). Left open pending researcher review, and because the checks are not exhaustive.
- [ ] **AB-11** Pinned environment (D-002) with the required packages installed and recorded.
- [ ] **AB-12** Build script reproduces the §4 cascade counts; leakage tests pass.
- [ ] **AB-13** Stage C and Stage D gates passed (D-042, proposed; Q-069).

A blocker is not met because its date has arrived: AB-1 is necessary, not sufficient.

**Needed before submission (not training blockers):** D-020 (journal); Q-055; Q-058. *Revision 4:* D-016 was removed from this line; under D-042 (proposed) it blocks D-017–D-019 and training (AB-13). The revision 3 text read "Not blocking training, but needed before submission: D-016 (contribution wording) after the RQ5 review; D-020 (journal); Q-055; Q-058."

## Appendix A. Verified raw files (local manifest, 2026-10-24)

The SHA-256 values below are the full hashes from `data/raw/nhanes/MANIFEST_local.csv` (git-ignored). All files returned HTTP 200 and have a SAS-transport header. `[EVIDENCE: local check]`

| File | Bytes | SHA-256 |
|---|---|---|
| P_DEMO | 3,614,720 | 2e46c6c26bf77cd8989f64011ace12cbf42c0f3e03414eb59acc5328c8f87913 |
| DEMO_L | 2,582,160 | ca4374a158b493b8b0163e1388da21d57a18d1b9cecff2aa4e2fa2bec494fe23 |
| P_DIQ | 3,361,520 | 79153f799fc2171792771c4aa250029c62807f14915f1f81405b03233b1e5ae3 |
| DIQ_L | 847,600 | 9535a023673ae869afae19d842d8679e06f6a464606ac15900686b41ef05090f |
| P_GHB | 167,600 | dac9e423f56041c2ec46486cb16be16d3347e0a81a575985882ffad5a60e1195 |
| GHB_L | 174,000 | 67aee0353160e2392dc0a33bece99b90764a630c76d82415ac4639105ad9dd03 |
| P_GLU | 164,160 | 91b83c46fb4707c431838159135e93693a0572bce54074f5a890f0ee104732b3 |
| GLU_L | 129,200 | 70f773ab37e3d8485341f32137e280e05b9279e5fe9b6f0362e4052d8fe9a201 |
| P_FASTQX | 2,096,800 | 2ff1a59eae3b7564373d61abecd585c4d7c39e1ad6826403775bd94def3ce6d1 |
| FASTQX_L | 1,330,000 | e687d7ed729e81b256dbf911c9737883d948c1441079b012741d8ea3b115be6b |
| P_INS | 205,040 | 00b2cebd564df7038451d297df1a1d11e8e69a9443eee16770c24cc2ce3471da |
| INS_L | 161,280 | cdbf53b644805e5e67725c81ee32048dad3c06687689435b042a7a144cb9ec65 |
| P_TCHOL | 294,000 | 759cd9c408b5d1b91f6cfb5d5e67920a301f7478c0e90ce7adf4bbd277a45ac8 |
| TCHOL_L | 259,520 | 5c3312e555bb0706fd97cbd63fcbc9e78f00bda8d2d149732d9dd368169b25d3 |
| P_HDL | 294,000 | 04a344f00fe34b3dc4202ee9e47cf61e67d1f985d7c9ece228e25caa85c7fbd7 |
| HDL_L | 259,520 | c1bb43df5ca366f470b411c043f4aee7ae6552a7f4bca1178bc87b24fb9a7300 |
| P_TRIGLY | 409,360 | d3eb2df386f24a559ae4db992f0ec9aaf3d2c0caec173aa1921e78100ee88b31 |
| TRIGLY_L | 321,840 | 77679864c33b98d9b6db528f3a0ac0a15ea34bde9731c04d23bc9801277975f4 |
| P_BIOPRO | 3,420,640 | f242cb9f9da5787f77d81ffb02822350e01cea4adf072d23bc96eb008182010c |
| BIOPRO_L | 2,425,520 | 912b345aad6b71d53a3bc299a7f3bb0d5530e9fa5b6e76d2d00103979861a476 |
| P_CBC | 2,427,760 | 8a910eacc0fad8d3b817bb01699c5d90761c60be3b2daaaf025396b58de96ef8 |
| CBC_L | 1,609,840 | 4405da2a5899dcd11e3ef4dbec0b4d2fca6d736a3efa7a85afee668baa95923f |
| P_HSCRP | 331,760 | e6954d17afa70755c26004bda6d4f0b256a5f30b0620cb70fdd6f520147218e1 |
| HSCRP_L | 280,560 | c56098d7c33509087a4645dfdf39936c14213d9123e1e718831a10d5bc4e3a1b |
| P_ALB_CR | 835,600 | c493f6b74cc0608bb7083b92e074fc3070b9e614fd5e1e34d0ce943e0f6116bf |
| ALB_CR_L | 545,440 | fc011a80d14419884559372a3196f0a268b494f4f2fa972d00be1f3a23ba3c41 |
| P_BMX | 2,520,640 | 7038d0da3169420a4a3cbaec09ac586a701b38e1c7b925431b60e13ac24fed66 |
| BMX_L | 1,563,200 | 44440c416d9ad709e8b1708a5975378ab4d5b18edc39eb5015c2ae7186500170 |
| P_BPXO | 1,039,840 | 5edbcb81e99fe8dad38deb8b642570278b200c525d88ffa29ae3ceb4dd38bde4 |
| BPXO_L | 696,720 | 189aa9bed689d2c69cf8d780b01de85073276fea5694dd52cdf696229f9054a6 |
| P_RXQ_RX | 16,154,000 | 0ee30345ccfee5ce0ff55e51fca4dec7389d3a8e985c59485d13400e9ec2ee2e |
| RXQ_RX_L | 287,600 | b801ca006aa8b505f597c4b28221e6f8c8b033781f214c16d45a114c5b564211 |

## Appendix B. CDC cross-period equations (transcribed 2026-10-24)

Source pages are the official `.htm` codebooks (§3.1); re-verification is required (AB-9).

- **TRIGLY_L:**
  - Forward: `LBXTLG = 12.45 + 1.022 × LBXTR`.
  - Backward: `LBXTR = −12.19 + 0.9785 × LBXTLG`.
  - Weighted Deming regression; n = 89; r = 0.999. CDC text: "serum triglyceride results (mg/L)".
- **HSCRP_L:**
  - Forward: `Cobas 8000 = −0.08653 + 0.9672 × Cobas 6000`.
  - Backward: `Cobas 6000 = 0.08946 + 1.034 × Cobas 8000`.
  - n = 150; r = 0.996; Cobas 6000 14.28% higher. CDC text: "HSCRP results (mg/dL)".
  - **Not applied** (§6.4, Q-045).

**Verbatim CDC strings** (revision 1; page text re-read 2026-10-24, with ASCII hyphens and asterisks as on the page; any implementation must use these):
- `TRIGLY_L.htm`, First Published September 2025:
  - "Forward: LBXTLG (New Instrument + New Triglyceride Method) = 12.45 + 1.022 LBXTR (Old Instrument); 95% CI of intercept (11.27 to 13.64) and slope (1.010 to 1.034)"
  - "Backward: LBXTR (Old Instrument) = -12.19 + 0.9785 LBXTLG (New Instrument + New Triglyceride Method); 95% CI of intercept (-13.46 to -10.91) and slope (0.9669 to 0.9900)"
  - The bracketed labels are subscripts on the page.
- `HSCRP_L.htm`, First Published September 2024:
  - "Forward: Cobas 8000 = -0.08653 + 0.9672 * (Cobas 6000); 95% CI of slope (0.9388 to 0.9956) and intercept (-0.1157 to -0.05737)."
  - "Backward: Cobas 6000 = 0.08946 + 1.034 * (Cobas 8000); 95% CI of slope (1.003 to 1.065) and intercept (0.06146 to 0.1175)."
- **Arithmetic check:** inverting each forward equation reproduces its backward equation to the stated precision (TG −12.182 + 0.97847x; CRP 0.08946 + 1.0339x). This confirms the direction of each equation, but **not** its units.
- **ALB_CR_L:**
  - Forward: `URXUMA New = 1.381 + 0.8407 × URXUMA Old`.
  - Backward: `URXUMA Old = −1.643 + 1.189 × URXUMA New`.
  - n = 195; r = 0.982; new method 6.20% higher; units mg/L.
- **BIOPRO_L adjustment table** (Cobas 6000 vs 8000), backward `Y6000` equations:
  - ALT `−1.529 + 1.035X`;
  - ALP `0.6098 + 0.9041X`;
  - GGT `0.9735 + 0.9444X`;
  - BUN `0.09386 + 1.021X`;
  - total bilirubin `0.01793 + 1.012X`.
  - "Adjustment Not Recommended" for albumin, AST, calcium, cholesterol, creatinine, phosphorus, total protein and uric acid.

## Appendix C. Codebook facts relied on

All `[EVIDENCE: CDC documentation]`, read 2026-10-24:
- **Eligible ages:** GHB, GLU, INS, BIOPRO, TRIGLY ≥ 12; TCHOL and HDL ≥ 6; ALB_CR ≥ 3; CBC and HSCRP ≥ 1; BPXO ≥ 8.
- **Morning session:** TRIGLY and the fasting measures are morning-session only.
- **Zero fasting weights:**
  - 2017–2020: 346 participants with no blood specimen and 268 with an invalid fast;
  - 2021–2023: 324 and 311.
- **Phlebotomy weight:** `WTPH2YR` is present in the 2021–2023 non-fasting lab files only.
- **Prescription variables:** `RXQ_RX_L` has only `RXQ033` and `RXQ050`; drug names, duration and reasons were not collected.
- **Routing check items:**
  - DIQ159: `DIQ010` = 1 → `DIQ050`; `DIQ010` = 3 and age ≥ 12 → `DIQ180`;
  - DIQ065: continue to `DIQ070` if `DIQ010` = 1, `DIQ010` = 3, or `DIQ160` = 1.

## Appendix D. Candidate references (none citable yet)

Identifiers come from PubMed connector metadata retrieved on 2026-10-24, where shown. Each must pass the `research_plan.md` §6 verification before citation.

| ID | Item | Identifier | Inventory status |
|---|---|---|---|
| CR-01 | De Silva et al., 2021, *PLoS One*; NHANES undiagnosed T2D ML | doi:10.1371/journal.pone.0250832 | Not in inventory |
| CR-02 | Yoo, Maggiore, Jolliet, 2026, *J Clin Epidemiol*; MEDWACS, NHANES 1988–2018, validated on NHANES 2021–2023 and KNHANES | doi:10.1016/j.jclinepi.2026.112266 | P0303, `partially_verified` |
| CR-03 | Hutchison et al., 2025, medRxiv preprint; OGTT-defined prediabetes/diabetes, NHANES 2005–2016 | doi:10.1101/2025.02.10.25321897 | Not in inventory |
| CR-04 | Cai et al., 2026, *Diabetes Metab Res Rev*; HBV subgroup, SHAP, calibration | doi:10.1002/dmrr.70193 | P0256, `partially_verified` |
| CR-05 | Bang et al., 2009, *Ann Intern Med*; diabetes self-assessment score (NHANES) | doi:10.7326/0003-4819-151-11-200912010-00005 | Not in inventory |
| CR-06 | Van Calster et al., 2019, *BMC Med*; calibration | doi:10.1186/s12916-019-1466-7 | Not in inventory |
| CR-07 | Riley et al., 2020, *BMJ*; sample size for prediction models | doi:10.1136/bmj.m441 | Not in inventory |
| CR-08 | ADA Standards of Care in Diabetes 2026, Section 2 (diagnosis criteria) | PMID 41358893; doi:10.2337/dc26-S002; *Diabetes Care* 49(Suppl 1):S27–S49 (PubMed record, 2026-10-24). Full text **not read**: the PMC full-text request returned empty. Second attempt 2026-10-24 (PROTOCOL-EVIDENCE-001): official page, doi.org, PMC and Europe PMC unreachable; PubMed full text empty again (Q-061) | Not in inventory; **claim not verified** |
| CR-09 | WHO definition of impaired fasting glucose | To locate | Not in inventory |
| CR-10 | Corrected resampled t-test for cross-validation | To locate | Not in inventory |
| CR-11 | TRIPOD+AI reporting guideline | To locate | Not in inventory |
| CR-12 | Foundational sources: split/Mondrian conformal prediction; SHAP/TreeSHAP; gradient boosting library; decision curve analysis | To locate | Search the existing inventory first (many conformal records are `partially_verified`, e.g. P2870) |

## Change history

| Version | Date | Change | Approved |
|---|---|---|---|
| 0.1 | 2026-10-24 | Initial draft (PROTOCOL-DRAFT-001) | **No.** Pending researcher review |
| 0.1 rev. 1 | 2026-10-24 | PROTOCOL-DRAFT-002, owner-authorized draft edits:<br>(1) FA-2 recorded as the owner's preferred proposed outcome, still pending approval and verification of the ADA source; "either laboratory criterion, not a clinical diagnosis" made explicit (§2, §5.1, §24);<br>(2) S-15a and S-15b (exploratory) added, with label counts (§5.3, §19);<br>(3) hs-CRP removed from groups A and B; unresolved conversion documented; conditional S-16a/S-16b (§6.4, §8, §25, Appendix B); counts recomputed (A 21, B 27);<br>(4) period prevalence differences labelled outcome-distribution findings (§5.2, §16);<br>(5) Q-044 documentary evidence and verbatim CDC strings (§8, Appendix B);<br>(6) data-protection safeguards recorded (§22, AB-10);<br>(7) CR-08 identifier recorded, claim still unverified (Appendix D) | **No.** Pending researcher review. No decision status changed |
| 0.1 rev. 2 | 2026-10-24 | PROTOCOL-DRAFT-003, owner-authorized corrections (Option A):<br>(1) ADA confirmation-rule statement qualified as provisional (§5.1);<br>(2) CDC wording on combining periods quoted from `DEMO_L` ("urged to proceed with caution"), replacing "advises against" (§10);<br>(3) conformal validity guarantee removed; stated as an unverified hypothesis, with coverage measured (§18);<br>(4) median-FPG sentence corrected: v0.1 gave the medians of a broader reference population (103 vs 101), while the analytic samples give 101 vs 100 (§5.2);<br>(5) reproduction script and further safeguards recorded (§22).<br>FA-2 stays a preferred proposed outcome; hs-CRP stays excluded; S-15a/b and S-16a/b unchanged | **No.** Pending researcher review. No decision status changed |
| 0.1 rev. 3 | 2026-10-24 | PROTOCOL-EVIDENCE-001, primary-source review:<br>(1) ADA verification attempted and **blocked** (source unreachable); the criteria remain unverified (§5.1, CR-08, Q-061);<br>(2) §5.1 makes explicit the laboratory-category vs diagnosis distinction, that the OR rule includes the diabetes range, and the population/outcome consistency check (no definition changed);<br>(3) §8.2 records the official CDC statements on within-cycle instrument/method changes; participant timing cannot be reconstructed (`RIDEXMON` is season only);<br>(4) FA-5 recommendation (unadjusted reference; cycle-level equations as S-09b) proposed for researcher decision; Q-059–Q-061 listed (§25); AB-8 note | **No.** Pending researcher review. No decision status changed |
| 0.1 rev. 4 | 2026-10-29 | Q-069-RESOLUTION, owner-authorized draft edits (documentation only):<br>(1) §23: the dated table (D-019 frozen 11-01 → 11-02, Stage G from 11-03) replaced by a dependency-ordered table; dates are targets, not gates; D-014/outcome listed separately (timing not fixed by D-042); Rule S limited to test planning before 2026-11-03 (D-040 (7)); the fallback no longer assumes a frozen protocol;<br>(2) §26: new block before D-017/D-018/D-019 approval; AB-13 added; the AB-7 provisional-justification fallback replaced; D-016 removed from "Not blocking training".<br>Follows the researcher's in-principle resolution of Q-069 (D-042, PROPOSED). Protocol not frozen; no decision status changed | **No.** Pending researcher review |
