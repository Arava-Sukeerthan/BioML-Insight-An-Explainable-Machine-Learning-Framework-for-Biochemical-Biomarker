# Evidence and decision-readiness review (2026-11-12, 12:04 UTC onwards)

> **Controlled review. No researcher decision is made, and no protected operation was performed.**
>
> **Repository state checked at start:**
> - branch `claude/eloquent-mccarthy-bqtxr3-part1`;
> - HEAD `a0af2ad` = `origin/claude/eloquent-mccarthy-bqtxr3-part1`;
> - working tree: 6 modified + 54 untracked paths; 0 staged.
>
> Labels used throughout:
> - **[V]** verified: full text read for the stated point;
> - **[AB]** abstract-level evidence;
> - **[UV]** unverified;
> - **[RD]** researcher decision required;
> - **[TR]** technical recommendation.
>
> Earlier evidence records:
> - `2026-11-12_AB-7_reference_preverification.md`;
> - `2026-11-12_PRIOR-ART_AND_METHODS_EVIDENCE.md` (study numbers 1–11 below refer to its table).
>
> All literature searches cited here are **exploratory and unregistered**. A missing match is not evidence of a gap.

## 1. Contribution-option comparison (input to D-016; not a decision)

| Criterion | A — calibrated, uncertainty-aware biomarker modelling | B — integrated prediction + calibration + conformal + explanation stability under temporal validation | C — incremental value of biochemistry over a non-laboratory comparator under temporal validation |
|---|---|---|---|
| 1. Closest prior studies | Studies 2, 3, 5, 6, 7 (biochemical + calibration) [AB, FT-p for 5 and 6]; 8–10 (conformal elsewhere) [AB] | 1 (same outcome, NHANES 2021–2023) [AB]; 6 (SHAP refit stability) [V, partial]; 8 (Mondrian CP) [AB]; 11 (cross-population importance consistency) [AB] | 1 (CR-02: non-laboratory model, same outcome, temporal + external validation) [AB]; 5 (laboratory increment over FINDRISC) [V, partial] |
| 2. Already established | Biochemical ML for dysglycaemia/diabetes with calibration assessment is common | Every component exists separately. Temporal validation for **this outcome** exists (CR-02). Conformal classification exists in a diabetes context (genetic predictors) | A strong non-laboratory model for this outcome exists (CR-02). In one primary-care cohort, adding laboratory variables to a risk score added little (study 5, internal only) |
| 3. Genuinely uncertain | Whether anything beyond application is added | Whether any study combines all components, and especially **conformal coverage and explanation-rank stability measured across a period shift** in this setting | **Whether routine biochemistry adds discrimination or calibration over clinical measures for this outcome in NHANES, under temporal validation** |
| 4. Evidence for the gap | Weak: only absence in a non-exhaustive search | Absence in exploratory searches only (not evidence) | **Positive design evidence:** CR-02 used no laboratory predictors, so their value for this outcome is not addressed by it [AB]. Study 5 asked the question in a different setting with internal validation only [V, partial] |
| 5. Evidence against the gap | High overlap (studies 2, 3, 5–7) | CR-02 already does temporal + external validation with calibration and interpretability. Study 6 already examines refit stability. Mondrian CP is published | CR-02's abstract says the development used "multimodal data" before selecting non-laboratory predictors; its full text may report laboratory comparisons (**unknown until read**). Study 5 suggests a small increment |
| 6. Testable with planned data | Yes (Q2) | Yes (Q2, Q3, F4, F5), but the F5 metric needs a source decision (section 3) | **Yes**: this is protocol Q1 as drafted (B vs C, A vs C; framework and BL-1; internal and temporal) |
| 7. Feasible by 2026-11-27 | Yes, if the critical path holds (section 9) | Tight: every component must be run and reported, and F5 and CP under shift add analyses | **Most feasible:** Q1 is a subset of the planned runs |
| 8. Literature still needed | RQ1/RQ3 screen | RQ5 complete; RQ2/RQ3 strands; a methods source for refit/period stability | **CR-02 full text** (essential); the RQ1/RQ5 screen for direct NHANES incremental-value studies |
| 9. Risk of an application-only contribution | **High** | Medium (an "integration" claim is vulnerable to the RQ5 findings) | **Lower**: a substantive, testable question with a clear comparator |
| 10. Valid null result possible | Yes (no improvement over baselines) | Yes (e.g. coverage loss under shift; unstable explanations) | **Yes, and informative:** "biochemistry adds no meaningful value over clinical measures" is publishable if prespecified and reported with CIs |

**Technical recommendation [TR]:**
- **C as the primary contribution**, with calibration, conformal sets and explanation stability reported as prespecified secondary evaluations (B-type elements). A is not recommended as a stand-alone contribution.
- This rests on abstract-level evidence for CR-02 and must be re-checked once its full text is read.
- **D-016 stays with the researcher [RD].**

## 2. CR-02 / CR-03 evidence matrix
**Evidence status: abstract only for both [AB].** The full texts are inaccessible from this environment (sections 2 and 7 of the earlier evidence file). "Not stated" means **not stated in the abstract**; it is never read as "not done".

| Item | CR-02 (Yoo, Maggiore, Jolliet, *J Clin Epidemiol* 2026;195:112266; PMID 41950976) | CR-03 (Hutchison, Rinella, Mirmira, Parker, *medRxiv* 2025; PMID 39990568; preprint) |
|---|---|---|
| Research objective | Develop and externally validate an ML self-assessment system for prevalent prediabetes/diabetes from accessible parameters | Test whether easily obtained clinical data improve diagnosis of prediabetes/diabetes over HbA1c alone |
| Population | NHANES 1988–2018 (N = 17,458) | NHANES 2005–2016 participants with HbA1c, OGTT and sample weight (N = 13,800) |
| Outcome | FPG ≥ 100 mg/dL or HbA1c ≥ 5.7% | OGTT 2-h glucose 140–199 (pre); ≥ 200 mg/dL (diabetes) |
| Predictor groups | "Multimodal data" at development; final 7-parameter self-assessment set | A 20-feature model |
| Laboratory variables | Not stated in the final model (non-invasive set); development set not stated | FPG, insulin, triglycerides, iron, cholesterol, GGT, creatinine, platelets, neutrophil %, urine albumin, urine creatinine |
| Non-laboratory variables | Age, waist, SBP, gender, upper-leg length, arm circumference, BMI | Age, height, weight, waist, BP, pulse; poverty ratio |
| Development data | NHANES 1988–2018 | NHANES 2005–2016 |
| Validation data | NHANES 2021–2023 (N = 3,043); KNHANES 2023 (N = 5,492) | Not stated |
| Temporal validation | Yes (NHANES 2021–2023) | Not stated |
| External validation | Yes (KNHANES) | Not stated |
| Model families | "Multiple ML models"; neural network best; Boruta selection | Gradient-boosted decision trees (for 2-h glucose) |
| Calibration | "Calibration" (method not stated) | "Calibration" (method not stated) |
| Explainability | "Interpretability analysis" (method not stated) | Main features listed (method not stated) |
| Conformal / other uncertainty | Not stated (95% CIs for ROC-AUC) | Not stated |
| Explanation stability | Not stated | Not stated |
| Missing-data handling | Not stated | Exclusion of participants without HbA1c, OGTT or weights; otherwise not stated |
| Statistical comparison | Against established screening guidelines (decision curves) | AUROC vs HbA1c and FPG alone; PPV; net benefit |
| Limitations | Not stated in the abstract (beyond "not a diagnosis") | Not stated; it is a preprint |
| Evidence location | PubMed record PMID 41950976 (abstract), retrieved 2026-11-12 | PubMed record PMID 39990568 and the PMC landing page PMC11844569 (abstract only; the licence does not permit PMC archiving) |
| Status | **Abstract** | **Abstract** |

**Legitimate access routes** (no restriction is bypassed):
- **CR-03:** medRxiv is a public preprint server. The researcher can download the PDF from `medrxiv.org` in a browser and supply it.
- **CR-02:** institutional (library) subscription to *J Clin Epidemiol*; interlibrary loan; the publisher's article page; or a request to the corresponding author named in the PubMed record.

Unauthorised copies are not used. **If a PDF is supplied, this matrix will be updated from it.**

## 3. Explanation-stability methodology

**Types of stability:**

| Type | Meaning |
|---|---|
| Feature-selection stability | Whether the same predictors are *selected* across resamples (e.g. LASSO/Boruta under bootstrap) |
| Refit stability of attributions / global importance | Whether global SHAP importance (or its ranking) is similar across models refitted on resamples |
| Explanation stability across periods | Whether the global importance ranking from a frozen model differs between the development and validation periods. This reflects **data shift**, not refitting |
| Stability of individual-level explanations | Whether one person's attribution vector is stable under refitting or small input perturbation |
| Stability of global rankings | Rank-based comparison of global importance vectors. Our F5 targets this |

**The four dysglycaemia-related papers among the 22 hits:**

| Study | What is assessed | Level |
|---|---|---|
| Türkoğlu Genç & Yildiz 2026 (study 5) | SHAP used for selection and interpretation; stability not stated in the parts read | [V, partial] |
| Yang 2025 (study 6) | **Refit stability of global SHAP importance**: distributions over 20 repeated train/test cycles, shown as boxplots and described qualitatively. Performance stability over 10 runs | [V, partial] |
| Ghaderzadeh 2025 (study 7) | SHAP + Morris sensitivity; stability not stated | [AB] |
| He 2026 (study 11) | "Feature importance patterns … evaluated for consistency" between NHANES and CHARLS: **cross-population consistency of global importance**; method not stated | [AB] |

None of these defines a quantitative stability metric in the parts read.

**Candidate metrics.** Notation: v, u are global-importance vectors over p features; R(·) their ranks.

| Metric | Definition | Interpretation | Inputs | Advantages | Limitations | Source | Suitable here? |
|---|---|---|---|---|---|---|---|
| Spearman ρ | Pearson correlation of R(v) and R(u) (ties: mid-ranks) | +1 = identical ranking | Two importance vectors (all p features) | Uses all features; already implemented (`explain.spearman`, `rank_stability`) | Weights all rank positions equally, so ordering changes among unimportant features count as much as among top features | **[V]** Krishna et al., *TMLR* 2024 (arXiv:2202.01602v6): "rank correlation" = Spearman between feature rankings of two explanations. **Their use compares different explanation methods for the same model, not refits or periods.** The original Spearman source is not located [UV] | **Yes, as primary** for refit and between-period ranking stability, with the adaptation stated |
| Kendall τ | (concordant − discordant pairs) / total pairs | +1 = all pairs ordered alike | As above | Robust; interpretable as pairwise agreement | Largely redundant with ρ | **[V]** Krishna et al. define **pairwise rank agreement** = the fraction of feature pairs with the same relative order. Without ties, τ = 2·PRA − 1: a mathematical identity derived here, not stated by the source. Kendall's original source not located [UV] | Optional. Not recommended in addition to ρ (redundant) |
| Top-k feature overlap | \|top-k(v) ∩ top-k(u)\| / k | Share of the k most important features kept | Vectors; a prespecified k | Directly answers "are the leading biomarkers the same?"; implemented (`explain.top_k_overlap`) | Depends on k; ignores order within the top k | **[V]** Krishna et al. "feature agreement" (identical definition) | **Yes, as secondary**, with k fixed before results (e.g. 5) [RD] |
| Rank displacement | e.g. mean \|R(v)_f − R(u)_f\| over features, or Krishna's "weighted rank agreement" = (1/k) Σ over the top-k intersection of (1 − \|R_a − R_b\| / k) | Average positional shift | Vectors | Interpretable in rank units | Several variants; no standard | **[V]** for the Krishna weighted-rank-agreement variant (appendix D.2.1). The plain mean-displacement variant has no located source [UV] | Not recommended unless a reviewer requests it |
| Bootstrap uncertainty of a stability estimate | Percentile interval of the statistic over resamples | Sampling variability of the stability measure | Resampled refits or a resampled validation set | Quantifies precision | **The pairwise correlations among B refits are not independent** (each refit enters B − 1 pairs), so a naive CI over pairs is wrong. Use per-refit or per-resample summaries | **[AB]** Efron 1979 (*Ann Stat*, bootstrap) via Consensus metadata; the full text was not reviewed | Report the **distribution** (median, 2.5th–97.5th percentiles) of pairwise ρ across refits **descriptively**. For between-period ρ, a percentile bootstrap over validation participants is defensible |

**Conclusion:**
- A defensible F5 specification: **Spearman ρ of global mean-|SHAP| importance**
  - (i) across refits: distribution of pairwise ρ, plus top-k overlap with a prespecified k;
  - (ii) between periods: ρ between development and validation-period importance from the same frozen model, with a percentile bootstrap over validation participants.
- The metric definitions are supported by Krishna et al. [V], but **no verified source applies them to refit or temporal stability**. That adaptation must be stated as the study's own operationalisation.
- **Alvarez-Melis & Jaakkola (2018) [V] address input-perturbation (local Lipschitz) robustness only**, and are cited as motivation, not as the metric source.
- The implementation is **not changed**. The existing `rank_stability` reports the mean and minimum pairwise ρ; the descriptive percentile summary would be a later change after D-019 [RD].

## 4. R14 — ICI decision packet
| Criterion | (a) Keep span 0.75 (prespecified) | (b) Verified R `lowess` default span | (c) Paper's local-quadratic `loess` |
|---|---|---|---|
| Fidelity to Austin & Steyerberg 2019 | Same smoother family as their `lowess(iter = 0)` variant; span not tied to the paper | **Closest to their `lowess` variant**, once the default is verified (R documentation unreachable today) | Closest to their **primary** `loess` variant, once its defaults are verified |
| Reproducibility | High (fixed, documented, tested) | High once verified | Depends on matching R's `loess` internals (degree, family, surface interpolation): harder to reproduce exactly in numpy |
| Implementation complexity | None | One constant | New local-quadratic code plus tests; risk of subtle mismatch |
| Compatibility with existing code | Full | Full | New function; `metrics.ici` interface can stay |
| Sensitivity analysis | Span 0.5 and 0.9 on the same predictions (cheap) | Same | Same; plus the local-linear variant |
| Absolute ICI values | Study-specific; not comparable with other studies | Comparable only with studies using the same R `lowess` defaults | Comparable only with studies using R `loess` defaults |
| Between-model comparisons | **Meaningful:** same smoother for all models | Same | Same |

**What the existing synthetic check establishes:**
- In **one** simulated setting (n = 2,485; two simulated probability vectors; no model fitted), the between-model ICI difference changed little for spans 0.5–0.9 (+0.060 to +0.062).
- A small span (0.3) inflated the level for the well-calibrated model.

**What it does not establish:**
- robustness for other prevalences, sample sizes, calibration shapes or real data;
- equivalence to R's `loess`/`lowess`;
- which span is "correct".

**[TR]:** (a) or (b) plus the prespecified span sensitivity analysis. Report that absolute ICI depends on the smoother. **[RD]:** choose at D-019.

The code is unchanged and R14 is not resolved.

## 5. R15 — CDC survey-domain implementation assessment
**Guidance** (CDC/NCHS NHANES variance-estimation tutorial, read 2026-11-12) [V]:
- Taylor series linearisation;
- first-stage PSUs treated as sampled with replacement within strata (`sdmvstra`, `sdmvpsu`);
- for subpopulations, **all records with a non-zero weight plus a subpopulation indicator**.

**Code inspected:** `scripts/models/survey.py::weighted_mean_taylor(x, w, strata, psu, domain=None)` and its tests.

| Check | Finding |
|---|---|
| Retains design records | **Partly.** All passed records are kept, including **zero-weight** records (see D2) |
| Indicator, not filtering | **Yes:** domain members contribute; non-members contribute 0 to the linearised variable but keep their stratum/PSU [V by test] |
| Non-domain behaviour unchanged | **Yes:** `domain=None` and `domain=all ones` give identical results (test) |
| Point estimate | Equals the weighted domain mean (test) |
| Variance formula | Σ_h n_h/(n_h − 1) Σ_i (z_hi − z̄_h)², with z = d·w·(x − r̂)/Σ d·w: the standard with-replacement linearisation for a ratio mean. **Not yet compared with a reference implementation (Q-052 open)** |
| Edge case: NaN x outside the domain | Ignored, as intended |
| Edge case: single-PSU stratum | Raises (no silent collapsing) |

**Concrete defects (reported, NOT fixed; demonstrated by a scratch run on 2026-11-12):**
- **D1 — NaN weight in the domain is not rejected.** The function returns `estimate = NaN, se = NaN` silently, instead of raising.
  - *Consequence:* a data error would propagate into Table 2 as NaN rather than stopping the analysis (it violates the fail-closed design).
  - *Proposed fix:* reject non-finite weights (in-domain and out-of-domain).
- **D2 — zero-weight records are retained in the design.** A PSU containing only zero-weight records is counted in n_h and alters the SE: in the demo, 0.0446 became 0.0444.
  - *Consequence:* deviation from the CDC instruction to use records with **non-zero** weight. In NHANES's masked 2-PSU design this case is unlikely, but possible with subsample weights.
  - *Proposed fix:* drop w = 0 records before the variance computation, or refuse inputs containing them.

**Minor:** a NaN weight **outside** the domain is silently ignored (E4). The D1 fix would cover it.

**[RD]:** whether to authorise fixing D1 and D2 now (code scaffolding) and the R15 wording at D-019. R15 is **not** approved.

## 6. Q-061 — outcome-definition decision packet
**Facts requiring the primary source** (*Diabetes Care* 2026;49(Suppl 1):S27–S49, doi:10.2337/dc26-S002, Section 2):
- HbA1c ≥ 5.7% and FPG ≥ 100 mg/dL as the prediabetes lower limits;
- HbA1c ≥ 6.5% and FPG ≥ 126 mg/dL as diabetes thresholds;
- the confirmatory-testing guidance;
- whether either test alone satisfies the criterion.

**Status [UV]:** four access attempts failed. Secondary papers (study 5; CR-02) **are not equivalent** to the primary source.

| | Route 1: primary ADA source obtained and verified | Route 2: primary source unavailable |
|---|---|---|
| What is done | Record exact wording and table reference; CR-08 threshold claim → [V] | Use the numerical laboratory rule; **no claim** that it reproduces the ADA definition |
| Scientific consequence | The outcome is anchored to a named guideline; the "either test" and confirmation statements are sourced | Same outcome and data; the link to a clinical definition is not asserted, so the clinical framing is weaker |
| Manuscript consequence | Methods: "consistent with ADA Standards of Care 2026, Section 2 (lower limits of the prediabetes range)" + citation; the "not a diagnosis" statement is sourced | Methods state the numbers only. Introduction §1.1 guideline sentence removed. Limitation added. Wording draft in the earlier evidence file §5 (its "commonly used" phrase also needs a source or is deleted) |
| Effect on thresholds | None | None |

**[RD]:** Route 1 or 2 (Q-061; FA-2 / D-015). Not selected here.

## 7. Option C — study-design proposal (if C is chosen; NOT approved)
Built only from elements already in the v1.0 candidate. No new outcome, dataset, predictor group or validation design is introduced.

| Element | Proposal (existing protocol element) |
|---|---|
| Non-laboratory group | **Group C** (age, sex, BMI, waist, SBP, DBP; 6 variables). *Note:* not identical to CR-02's 7 self-assessment variables. Reproducing CR-02's set would add new predictors (e.g. leg length, arm circumference; their NHANES availability is unchecked) and would need your approval |
| Biochemical group | **Group A** (21 analytes) |
| Combined group | **Group B** = A + C (27), already in the protocol |
| Comparison | B vs C (added value of biochemistry over clinical measures) and A vs C, for the framework (F2 + F3) and BL-1, as protocol Q1 states |
| Populations | The **same participants** in every group comparison: identical eligible samples (N = 3,088 / 2,485), identical seeds, splits and folds; in-fold imputation keeps N constant. S-10a (complete case on the intersection of groups) as sensitivity |
| Temporal split | Identical 2017–Mar 2020 → 2021–2023, frozen models applied once |
| Leakage prevention | Existing: in-fold preprocessing; validation isolated (tested); serum glucose and awareness items excluded; harness guard |
| Missingness / harmonisation | Group A carries harmonisation issues (TG method, analyser changes; S-08 reference, S-09b conditional) that group C does not. **Such differences can favour or penalise group A under temporal validation; this is a design limitation to state** |
| Discrimination | ΔAUROC (B − C, A − C) with a paired bootstrap 95% CI, internal and temporal |
| Calibration | ΔICI, Δcalibration slope, ΔBrier, on calibrated probabilities (Q-100 reference for transfer) |
| Decision curves | Only if M10 is retained (Q-054). Otherwise omitted |
| Uncertainty statements | CIs only. No non-inferiority or equivalence claim without a justified margin (Q-054 (b)) |
| Null result | If the CI for ΔAUROC includes 0, or the improvement is below a practically meaningful size, it is reported as "no demonstrated added value". **A practical-importance threshold is not in the protocol**; defining one before the results is your decision [RD]. Otherwise the result is reported descriptively, without a "meaningful" verdict |
| Overstatement guards | Report group C's own performance alongside the increment; no claim of clinical utility; temporal ≠ external validation; the multiplicity statement for Q1 stays as drafted |

## 8. Missing-method-reference verification table
| Method (where used) | Reference | Identifier | Status | Full text reviewed? | Supports the intended statement? |
|---|---|---|---|---|---|
| Platt scaling (F3; `calibration.PlattCalibrator`) | Platt JC. Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods (1999 per the Consensus record; cited as a book chapter in Smola et al. (eds.), *Advances in Large Margin Classifiers*, MIT Press, 2000 by Lin et al. 2007) | No DOI found | **[AB]** (Consensus metadata/abstract); **year and venue inconsistent between records** | No | Partly: a sigmoid mapping of classifier scores to probabilities. *Note:* our implementation fits a logistic model on logit scores by IRLS; whether Platt's target-smoothing variant is used must be stated, and is not checked against the text |
| Platt algorithm note | Lin H-T, Lin C-J, Weng RC. A note on Platt's probabilistic outputs for support vector machines. *Machine Learning* 2007 | DOI not returned | **[AB]** | No | Context only |
| Holm procedure (Q2; `stats.holm`) | Holm S. A simple sequentially rejective multiple test procedure. *Scand J Stat* 1979 | DOI not returned | **[AB]** | No | Yes, at abstract level: a sequentially rejective procedure controlling type I error for any combination of true hypotheses |
| Bootstrap (CIs; `stats.py`) | Efron B. Bootstrap methods: another look at the jackknife. *Ann Stat* 1979 | DOI not returned | **[AB]** | No | General bootstrap principle only. **Percentile-interval and paired-comparison specifics need a further source [UV]** |
| Baseline learners (implementations) | Pedregosa F et al. Scikit-learn. *JMLR* 2011;12:2825–30 (arXiv:1201.0490) | arXiv:1201.0490 | **[V]** | Yes | Software reference (SVC via LIBSVM, elastic net, k-NN named). Original algorithm papers [UV], not added |
| XGBoost (F2, BL-3) | Chen & Guestrin, KDD '16 (arXiv:1603.02754) | arXiv | **[V]** | Yes | Yes |
| Explanation-stability metrics | Krishna S et al. The disagreement problem in explainable machine learning: a practitioner's perspective. *TMLR* (06/2024); arXiv:2202.01602v6 | arXiv:2202.01602 | **[V]** | Yes | Metric **definitions** yes; **application to refit/temporal stability no** (adaptation) |
| Explanation robustness (motivation) | Alvarez-Melis D, Jaakkola TS. On the robustness of interpretability methods. WHI 2018; arXiv:1806.08049 | arXiv | **[V]** | Yes | Input-perturbation robustness only |
| NHANES variance | CDC/NCHS NHANES tutorial "Variance Estimation" | URL | **[V]** | Yes | Yes (Taylor; with replacement; domain estimation) |
| ICI | Austin & Steyerberg, *Stat Med* 2019 (PMID 31270850) | doi:10.1002/sim.8281 | **[V, partial]** | Searched | Definition yes; span not specified (R14) |
| Conformal (F4) | Angelopoulos & Bates, arXiv:2107.07511 | arXiv | **[V]** | Yes | Yes (tutorial) |
| SHAP / TreeSHAP | Lundberg & Lee 2017 [V]; Lundberg et al. 2020 [AB] | arXiv / doi | as stated | — | Yes |
| Decision curves (M10) | Vickers & Elkin 2006 | doi:10.1177/0272989X06295361 | **[V]** | Yes | Yes |
| Other methods in the code | lowess smoother (Cleveland); PAVA isotonic regression; Wilson score interval (`report.py`); AUROC with ties (Mann–Whitney equivalence); IRLS logistic regression; elastic net, random forest, SVM, MLP, k-NN originals | — | **[UV]: not located** | No | Needed only where the manuscript makes a methodological statement about them |

## 9. Critical-path and deadline assessment (2026-11-12, about 12:10 UTC, Day 30)
- **Completed (working tree, uncommitted):**
  - Stage-0 and pilot tooling, verified by dry runs;
  - the experiment harness and tests;
  - evidence records (AB-7, prior art, this review);
  - protocol v1.0 candidate with R1–R15;
  - manuscript drafts.
- **Pending approvals:** A1–A6, the custodian, Q-098, Q-099, Q-054, Q-100, Q-061; the Part 2 data decisions; R14/R15 and D-019 later.
- **None has been received.**

**Critical path:** approvals + custodian → Stage 0 → pilot → screening → Stage C/D gates → D-016 → D-017/D-018 → D-019 → experiments → manuscript.

**In parallel after approval:** installation and synthetic verification; download and build; the reference look-up and rebuild (AB-7).

| Milestone | Latest feasible date |
|---|---|
| Approvals + custodian | **11-13** (zero slack) |
| Stage 0 | 11-14 |
| Pilot complete | 11-16 |
| Title/abstract screening | 11-20 |
| AB-7 | 11-21 |
| Gates and D-019 | 11-22 |
| Experiments | 11-25 |
| Manuscript | 11-27 |

- **R-1: approaching, not triggered.** It is triggered if screening cannot finish by 11-19, which happens if approvals or the custodian slip past 11-13.
- **R-2, R-3: not triggered.**
- **Is the existing scope feasible?** Only if the approvals and the custodian arrive by 11-13 and the pilot passes. Otherwise, the governed route is R-1 first (your decision), then R-2.
- None is applied automatically. Validation and safeguards are never reduced.

## 10. Researcher decision sheet (only decisions that genuinely need you)
**Now:**

| # | Decision |
|---|---|
| 1 | **A1** (Q-063 alternative wording) and **A5** (Git, 61 paths: see the decision sheet §3, updated) |
| 2 | **A2:** name an independent custodian who meets C1–C6; S1 or S2, stating your basis |
| 3 | **Q-061:** supply the ADA 2026 Section 2 PDF (Route 1) or accept Route 2 |
| 4 | Supply or authorise access routes for the **CR-02 and CR-03 full texts** (section 2) |
| 5 | **R15 defects D1/D2:** authorise the fix now, or defer to D-019 |
| 6 | A3, A4, A6, Q-098, Q-099, Q-054, Q-100 (already prepared in the decision sheet) |

**Later (needs evidence first):**

| # | Decision |
|---|---|
| 7 | **D-016:** contribution option A, B or C, after CR-02's full text and the RQ5 review. Recommendation C, with B elements as secondary |
| 8 | **D-019:** R14 option, F5 metric (Spearman primary, top-k with a fixed k), practical-importance threshold for Option C (or descriptive only), R13/R15 wording |

---
Consensus metadata records used in section 8 (retrieved 2026-11-12):
- [1] [A Simple Sequentially Rejective Multiple Test Procedure](https://consensus.app/papers/details/w:a5bf6b92-b3b9-42ee-bedc-e723ea4c5bee/?utm_source=claude_desktop) (Holm, 1979, *Scandinavian Journal of Statistics*);
- [2] [Probabilistic Outputs for Support vector Machines and Comparisons to Regularized Likelihood Methods](https://consensus.app/papers/details/w:adfc3387-2c45-490d-93b0-ad5c0a1f2135/?utm_source=claude_desktop) (Platt, 1999);
- [3] [A note on Platt's probabilistic outputs for support vector machines](https://consensus.app/papers/details/w:28002646-1a40-4bbc-b56b-79dd536f1b29/?utm_source=claude_desktop) (Lin et al., 2007, *Machine Learning*);
- [4] [Bootstrap Methods: Another Look at the Jackknife](https://consensus.app/papers/details/w:279de8c0-20cd-46ab-8c73-65e707f20252/?utm_source=claude_desktop) (Efron, 1979, *The Annals of Statistics*).
