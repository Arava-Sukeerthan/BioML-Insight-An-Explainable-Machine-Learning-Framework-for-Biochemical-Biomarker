# AB-7 candidate references — pre-verification record (2026-11-12, second pass)

> **What this is:** a bibliographic and content **pre-verification** of the protocol's candidate references (v0.1 Appendix D, CR-01 to CR-12) and of references found to be missing. Sources, all retrieved 2026-11-12:
> - the PubMed connector (NCBI metadata, ID conversion, PMC full-text attempt);
> - the alphaXiv connector, which returns raw PDF pages for arXiv papers and readable page text for PMC article pages; long outputs were saved to the session's tool-results folder and searched.
>
> **What this is not:**
> - **Not D-064 verification:** a record becomes `verified` only in an authorised inventory build with an eligible independent second source. **No reference here is `verified` and none is citable** (`research_plan.md` §6). The inventory holds 0 `verified` records.
> - **Not search provenance:** none of these look-ups was registered, and nothing was added to the inventory, manifest or decision log.
>
> No abstract or article text is reproduced beyond short identifying phrases; claims are paraphrased (D-010, D-089).

## Verification levels used
| Level | Meaning |
|---|---|
| **FT** | Full text read for the specific claim (raw article or PDF text) |
| **AB** | Abstract read; it supports the claim. Full text not read for it |
| **MD** | Bibliographic metadata only (identity confirmed; claim not checked) |
| **UV** | Not located, or the claim is not supported by what could be read |

Correction checks for every PubMed record:
- **Publication types:** none carries "Retracted Publication".
- **Errata searches by author and journal:** no *Published Erratum* or *Expression of Concern* found for the cited items. **Limit:** errata are often indexed without authors, and the connector does not expose PubMed's correction links, so "none found" is not proof of absence.

One related erratum was found and is listed under CR-07.

## 1. Verification table

| CR | Record (identity confirmed against PubMed or the paper's own first page) | Level | What the source actually supports | Recommendation |
|---|---|---|---|---|
| CR-01 | De Silva K, Lim S, Mousa A, Teede H, Forbes A, Demmer RT, Jönsson D, Enticott J. *PLoS One* 2021;16(5):e0250832. PMID 33951067; doi:10.1371/journal.pone.0250832; PMC8099133 | **FT** | Undiagnosed **type 2 diabetes** (not prediabetes) from NHANES 2007–2016. Compares logistic regression, an ANN and random forests. NHANES **2013–2016 held out** as an "external" validation set: a later-cycle hold-out of the same survey, closer to temporal validation. **No calibration assessment** in the text (no match for calibration, Brier or Hosmer–Lemeshow), and no SHAP or conformal methods | Keep as **context** for "LR among compared methods" and NHANES ML practice. Do not present it as same-target evidence |
| CR-02 | Yoo D, Maggiore U, Jolliet O. *J Clin Epidemiol* 2026;195:112266. PMID 41950976; doi:10.1016/j.jclinepi.2026.112266 (inventory P0303) | **AB** | **Same composite outcome** (FPG ≥ 100 mg/dL or HbA1c ≥ 5.7%). NHANES 1988–2018 development; multiple ML models with Boruta selection; calibration; interpretability analysis; decision curves. Validation on **NHANES 2021–2023** and **KNHANES 2023**. **Non-laboratory** predictors (self-assessment) | **Closest prior art.** It must be cited and compared, and it constrains the contribution (section 4) |
| CR-03 | Hutchison AL, Rinella ME, Mirmira RG, Parker WF. *medRxiv* preprint v1, 2025-02-12. PMID 39990568; doi:10.1101/2025.02.10.25321897 (inventory **P3005**, inside the D-044 scope) | **AB** (PMC states the licence does not permit PMC archiving; full text only on medRxiv, not reached) | NHANES 2005–2016; OGTT-defined prediabetes and diabetes; a gradient-boosted model compared with HbA1c and FPG alone; calibration, PPV and decision curves. **No LR comparator in the abstract. Not peer-reviewed;** no published version found | **Remove** from the "reports LR comparators" claim (§11.1). Keep as closest-context evidence, labelled as a preprint |
| CR-04 | Cai Z et al. (11 authors). *Diabetes Metab Res Rev* 2026;42(5):e70193. PMID 42423124; doi:10.1002/dmrr.70193 (inventory P0256) | **AB** | HBV-positive adults, NHANES 2003–2018; diabetes; inflammatory/immune and biochemical indicators; LASSO and 7 algorithms; calibration curve and decision curves; SHAP; **internal 7:3 split only** | Keep as closest context (biochemical inputs + calibration + SHAP) |
| CR-05 | Bang H, Edwards AM, Bomback AS, Ballantyne CM, Brillon D, Callahan MA, Teutsch SM, Mushlin AI, Kern LM. *Ann Intern Med* 2009;151(11):775–83. PMID 19949143; doi:10.7326/0003-4819-151-11-200912010-00005 | **FT** (PMC3633111 is an NIH **author manuscript**) | Logistic regression; NHANES 1999–2004 development; validation on NHANES 2005–2006 and ARIC/CHS; target is **undiagnosed diabetes** (FPG ≥ 126 mg/dL). *Version note:* the author manuscript reports a different selection percentage (30%) from the published abstract (35%); cite the **published** version | Keep as context (an NHANES risk score; LR) |
| CR-06 | Van Calster B, McLernon DJ, van Smeden M, Wynants L, Steyerberg EW, [sixth author entry empty in PubMed]. *BMC Med* 2019;17(1):230. PMID 31842878; doi:10.1186/s12916-019-1466-7; PMC6912996 | **FT** | Calibration hierarchy (mean / weak / moderate / strong); weak calibration via calibration intercept and slope; moderate via a flexible calibration curve | Keep for M5/M6 and F3. Complete the author list from the full text |
| CR-07 | Riley RD, Ensor J, Snell KIE, Harrell FE, Martin GP, Reitsma JB, Moons KGM, Collins G, van Smeden M. *BMJ* 2020;368:m441. PMID 32188600; doi:10.1136/bmj.m441 | **MD** (no abstract in PubMed; no PMC copy; publisher full text not reached) | Title only: minimum sample size for developing a clinical prediction model | Keep only if Q-056 (formal sample-size calculation) is retained; needs full text. *Related:* the companion *Stat Med* Part II paper has a published correction (PMID 31793031; doi:10.1002/sim.8409); if Part II's formulas are used, the correction must be applied |
| CR-08 | ADA Professional Practice Committee. 2. Diagnosis and Classification of Diabetes: Standards of Care in Diabetes—2026. *Diabetes Care* 2026;49(Suppl 1):S27–S49. PMID 41358893; doi:10.2337/dc26-S002 | **MD**; threshold claim **UV** | Identity only. The abstract does not state any threshold. The PMC copy (PMC12690183) returned no text on three attempts | **Required, not replaceable** by a secondary source for the outcome definition. See section 3 |
| CR-09 | WHO definition of impaired fasting glucose | **UV** (not located; not in PubMed or arXiv) | — | **Remove** if A6-a defers S-03 (its only use) |
| CR-10 | Corrected resampled t-test | **UV** (not located) | — | **Remove**: the v1.0 candidate summarises over seeds and runs no fold-level tests (§9 R11) |
| CR-11 | Collins GS, Moons KGM, Dhiman P, Riley RD, Beam AL, Van Calster B, et al. *BMJ* 2024;385:e078378. PMID 38626948; doi:10.1136/bmj-2023-078378; PMC11019967 | **AB** | TRIPOD+AI supersedes TRIPOD 2015 for regression and ML prediction models; 27-item checklist | Keep (reporting guideline, Q-055). Read in full before writing to its checklist |
| CR-12a | Lundberg SM, Erion G, Chen H, DeGrave A, Prutkin JM, Nair B, Katz R, Himmelfarb J, Bansal N, Lee SI. *Nat Mach Intell* 2020;2(1):56–67. PMID 32607472; doi:10.1038/s42256-019-0138-9; PMC7326367 | **AB** | Polynomial-time exact Shapley explanations for tree models (TreeSHAP) | Keep (F5) |
| CR-12b | Lundberg SM, Lee SI. A unified approach to interpreting model predictions. *NIPS 2017* (31st Conference on Neural Information Processing Systems, per the paper's first page); arXiv:1705.07874 | **FT** | Additive feature attribution; Theorem 1: uniqueness under local accuracy, missingness and consistency (Shapley values) | Keep (F5) |
| CR-12c | Chen T, Guestrin C. XGBoost: a scalable tree boosting system. *KDD '16* (per the paper's first page); arXiv:1603.02754 | **FT** | Regularised objective (Eq. 2); sparsity-aware split finding with learned default directions for missing values | Keep (F2, BL-3) |
| CR-12d | Angelopoulos AN, Bates S. A gentle introduction to conformal prediction and distribution-free uncertainty quantification. arXiv:2107.07511 (v6, 2022) | **FT** | Split-conformal coverage ≥ 1 − α under i.i.d. data, and under exchangeability per the Theorem D.1 remark; quantile level ⌈(n+1)(1−α)⌉/n, with q̂ = ∞ when α < 1/(n+1); class-conditional procedure with class-balanced coverage (Proposition 2, credited to Vovk). **Matches `scripts/models/conformal.py`** | Keep, as a tutorial. A primary source for class-conditional (Mondrian) validity (Vovk's work, cited in the tutorial) is **not yet located**; a primary source would be preferable |
| CR-12e | Vickers AJ, Elkin EB. *Med Decis Making* 2006;26(6):565–74. PMID 17099194; doi:10.1177/0272989X06295361; PMC2577036 | **FT** | Net benefit = TP/n − FP/n × pt/(1 − pt). **Matches `metrics.net_benefit`** | Keep only if M10 is retained (Q-054) |
| **CR-13 (new)** | Austin PC, Steyerberg EW. The Integrated Calibration Index (ICI) and related metrics for quantifying the calibration of logistic regression models. *Stat Med* 2019;38(21):4051–65. PMID 31270850; doi:10.1002/sim.8281; PMC6771733 | **FT** | ICI = the density-weighted mean absolute difference between predicted probability and a smoothed observed rate. The smoothed curve came from R `loess(Y∼P)` and `lowess(Y∼P, iter = 0)` | **Add.** The primary metric ICI (M6, Q2) currently has no source. **Implementation mismatch:** our `metrics.ici` uses local-linear smoothing with span 0.75, which the paper does not state to be equal to either R function. The smoother must be fixed at the freeze to a cited specification, and the R defaults confirmed from the R documentation (not checked here) |

## 2. Status summary and AB-7
| Level | Items |
|---|---|
| FT | CR-01, CR-05, CR-06, CR-12b, CR-12c, CR-12d, CR-12e, CR-13 |
| AB | CR-02, CR-03, CR-04, CR-11, CR-12a |
| MD | CR-07; CR-08 (threshold claim UV) |
| UV | CR-09, CR-10 (both recommended for removal) |

**AB-7 is NOT complete:**
- (a) **no reference is D-064 `verified`**: each needs the registered look-up, a Crossref second source and the authorised rebuild (A6-b, Q-098, Q-099);
- (b) the **CR-08 thresholds are unverified** (section 3);
- (c) **sources still missing** for: Platt scaling (F3), the elastic-net, random-forest, RBF-SVM, MLP and k-NN baselines (BL-1 to BL-6), Holm's procedure, the paired bootstrap, Taylor-linearisation variance for NHANES, and a **methodological source on explanation stability**. None was searched for in this pass, and none is asserted.

### Manuscript claims lacking adequate evidence (2026-11-12)
| Location | Claim | Status |
|---|---|---|
| `01_introduction.md` §1.1 | Thresholds of the outcome correspond to a guideline | **Unsupported** until CR-08 is read (section 3) |
| `01_introduction.md` §1.1 | "Routine panels are measured far more often than glycaemic tests" | **No source found. Remove** unless one is verified |
| `01_introduction.md` §1.2 | What prediction studies usually report | **Hypothesis**; waits for screening results (RQ1–RQ4) |
| `01_introduction.md` §1.3 | Calibration; conformal coverage; explanation stability; validation types | CR-06 (FT) and CR-12d (FT) support the first two. **Explanation stability: no source.** Validation types: CR-11 (AB), to be read in full |
| `03_methods_experimental.md` §3.3 | Outcome thresholds | **Unsupported** (CR-08) |
| `03_methods_experimental.md` §3.8 | ICI with local-linear smoothing, span 0.75 | **Source now identified (CR-13); specification mismatch**, decide at the freeze |
| `03_methods_experimental.md` §3.6 | Baseline set justified by the included studies | Waits for RQ1 screening (D-018, AB-7) |

## 3. CR-08 / Q-061 — source requirements note

**What must be verified:**

| Threshold the protocol uses | Where it is used | What must be confirmed from the primary text |
|---|---|---|
| HbA1c ≥ 5.7% (39 mmol/mol) | Primary outcome (§5.1), lower limit of the "prediabetes" range | That ADA 2026 defines this as the lower limit of increased risk / prediabetes by HbA1c, and its exact wording (the inclusive bound) |
| FPG ≥ 100 mg/dL (5.6 mmol/L) | Primary outcome (§5.1) | That ADA 2026 uses this as the lower limit of impaired fasting glucose, and its exact wording |
| HbA1c ≥ 6.5%; FPG ≥ 126 mg/dL | Descriptive "diabetes-range" subgroup (§5.1, S-05) | The diabetes cut-points and the statement on **confirmatory testing** (the protocol states that a single examination is not a diagnosis) |
| "Either test independently" | The OR rule (§5.1) | Whether ADA treats each test as a criterion on its own |

**The source and section needed:** American Diabetes Association Professional Practice Committee, *Diabetes Care* 2026;49(Suppl 1):S27–S49, doi:10.2337/dc26-S002, Section 2 "Diagnosis and Classification of Diabetes". This means the criteria table for diabetes and for prediabetes / increased risk, plus the surrounding text on confirmation. The table numbers are **not** asserted here, because the text has not been read.

**Is the public bibliographic record sufficient?** **No.** The PubMed record confirms identity only; its abstract states no threshold. Secondary sources, including CR-02, which uses the same composite outcome, show that the definition is used in the literature, but they **cannot** verify the guideline content.

**What the researcher can supply:**
- the PDF of the article (publisher or PMC download), or
- access to `diabetesjournals.org` / PMC full text from the environment (a network setting).

On receipt, the assistant records the exact wording and table reference, and the threshold claim moves to FT.

**If the PDF cannot be obtained:**
- The outcome **may still be used**, because it is a prespecified, reproducible laboratory definition. **But:**
  - (1) the manuscript must not state that it equals the ADA definition. It is described as a laboratory-defined dysglycaemia rule with the thresholds stated numerically;
  - (2) the guideline-correspondence sentence in §5.1 and §1.1 is removed or marked unverified;
  - (3) this is listed as a limitation.
- Under CLAUDE.md rule 11, the outcome definition remains the researcher's decision (D-015 / FA-2). This fallback is an option for that decision, not a default.
- **No threshold is changed** in either case.

## 4. Closest-prior-art evidence (input to D-016; not a decision)

**Tool readiness:**
- `rq5_review.py` counts only confirmed full-text assessments.
- It marks every record that is not D-064 `verified` as "not citable".
- It prints "Review complete: NO — no contribution or novelty wording is supported yet" while any RQ5-routed record is unassessed or awaiting verification (tests).
- No screening has run, so it refuses on the real repository.

**Evidence base:**
- the candidates above;
- two **exploratory, unregistered** PubMed searches (2026-11-12):
  - (i) `conformal prediction` with diabetes, prediabetes, glycaemic or NHANES: **3 records**;
  - (ii) SHAP with stability, consistency or bootstrap, plus diabetes or prediabetes, plus calibration: **22 records, not screened**.

These are **not** part of the review's search record and cannot support a claim that something is absent.

**Conformal records from (i)** (abstract level):

| Study | Setting | What it shows |
|---|---|---|
| Kodji et al., *PLoS Comput Biol* 2026;22(8):e1014670 (doi:10.1371/journal.pcbi.1014670) | **Mondrian cross-conformal prediction** with logistic regression | Classification of type 2 diabetes complications from polygenic risk scores, evaluated across ancestries |
| Olshvang et al., *medRxiv* 2026 (doi:10.64898/2026.08.04.26359704) | Split and adaptive conformal **intervals** | eGFR decline in type 2 diabetes |
| Harris et al., *Diabetes Metab Syndr* 2024;18(8):103113 (doi:10.1016/j.dsx.2024.103113) | Conformal **intervals** | Waist circumference, NHANES and Look AHEAD |

| Capability | Established in the closest work (abstract or full text, as stated) | Implication for the contribution |
|---|---|---|
| Biochemical-biomarker classification of dysglycaemia or diabetes | Yes: CR-03 (labs + vitals, NHANES; preprint), CR-04 (biochemical + inflammatory indicators; diabetes in HBV). CR-02 deliberately uses **non-laboratory** predictors | The **added value of biochemistry over clinical measures** (Q1) is not shown to be established for this outcome, because CR-02 used no laboratory data. It is a candidate gap to be confirmed by screening |
| Probability calibration | Yes: CR-02, CR-03 and CR-04 report calibration | Not a contribution in itself |
| Conformal uncertainty | Yes in diabetes contexts: Mondrian conformal classification (Kodji 2026), conformal regression intervals (Olshvang 2026, Harris 2024). **None found for dysglycaemia detection in NHANES** in this exploratory search, which is **not evidence of absence** | At most a candidate gap |
| Explanation stability | SHAP is used (CR-04). Stability of explanations was not assessed in what was read. The 22 hits are unscreened | Unknown. Needs the RQ2 strand |
| Temporal / independent validation | **Yes, for the same outcome:** CR-02 validated on NHANES 2021–2023 (temporal) and KNHANES (external). CR-01 used later NHANES cycles | **Temporal validation on 2021–2023 is not new** for this outcome. The protocol's temporal design is sound but **not a novelty** |
| Combination of all five | Not observed in the items read | Cannot be claimed without the completed RQ5 review (D-034 / D-038 groups) |

**Evidence required before D-016:**
- (1) the RQ5 strand screened, assessed at full text and verified (`rq5_review.py` "Review complete: yes");
- (2) CR-02 and CR-03 read in full and compared component by component;
- (3) the 22 explanation-stability hits and the RQ2/RQ3 strands at least title-screened, or the limitation stated;
- (4) all cited records D-064 `verified`.

**Defensible framing options for the researcher** (no choice made here):
- (a) a methods-integration and evaluation study whose contribution is the **prespecified, temporally validated comparison** of biochemical vs clinical predictors with calibrated, uncertainty-aware outputs, positioned explicitly against CR-02;
- (b) a narrower claim limited to Q1, the value of biochemistry;
- (c) further options after the review.

Each must avoid "first" or "novel" unless the completed review supports it (CLAUDE.md rule 14).
