# Technical corrections and decision evidence (2026-11-12, from 12:14 UTC)

> **Status:** preparation for researcher review.
> - **No researcher decision is made.**
> - **No implementation was modified.** The R15 correction is a proposed patch (`2026-11-12_R15_proposed.patch`), validated only in a disposable scratch copy that has been deleted.
> - No Git operation was performed.
>
> **Repository at start:**
> - branch `claude/eloquent-mccarthy-bqtxr3-part1`;
> - HEAD `a0af2ad` = origin;
> - 6 modified + 55 new paths (the unapproved 61-path A5 list); 0 staged.
>
> This file and the patch file are **new paths outside the 61-path A5 list**. The A5 list itself was not changed.
>
> Labels:
> - **[V]** full text or source code read;
> - **[AB]** abstract;
> - **[MD]** metadata only;
> - **[UV]** unverified;
> - **[RD]** researcher decision;
> - **[TR]** technical recommendation.

## 1. R15 — defect analysis and proposed patch
**Source [V]:** CDC/NCHS NHANES tutorial "Variance Estimation" (`wwwn.cdc.gov/nchs/nhanes/tutorials/varianceestimation.aspx`, read 2026-11-12). Exact passage:
> "your statistical software requires all observations with a non-zero value for your weight variable, as well as an indicator for which records are in your subpopulation of interest."

The same page treats first-stage sampling as "with replacement", and gives design degrees of freedom = number of PSUs − number of strata ("Most two-year public data releases … have 15 degrees of freedom").

**Current code:** `scripts/models/survey.py::weighted_mean_taylor(x, w, strata, psu, domain=None)`.

| Input-validation path (current) | Behaviour |
|---|---|
| Shapes / empty | Raises |
| `domain` length | Raises |
| `w < 0` | Raises |
| NaN `x` in the domain | Raises |
| NaN `x` outside the domain | Allowed (legitimate: not used) |
| Domain weight sum ≤ 0 | Raises |
| **NaN or inf weight (in or out of the domain)** | **Not checked (D1)** |
| **Zero weight** | **Kept in the design (D2)** |
| Single-PSU stratum | Raises |
| NaN strata / PSU codes | Not checked (outside D1/D2; noted, no change proposed) |

**D1 — missing or infinite weights:**
- *Mechanism:* `(w < 0)` is False for NaN. The domain weight sum becomes NaN, `NaN <= 0` is False, so the function returns `estimate = NaN, se = NaN`.
- *Outside the domain:* NaN weights are silently zeroed by `np.where(d, w, 0)`.
- *Classification:* a missing **weight** is invalid design input. It is **not** a legitimate missing **observation**, because NaN `x` outside the domain remains allowed.

**D2 — zero-weight records:**
- *Mechanism:* they stay in the design. A PSU made up only of zero-weight records is counted in n_h, which changes n_h/(n_h − 1) and the PSU-total mean.
- *Demonstrated:* SE 0.0446 → 0.0444 when a zero-weight-only PSU is added.
- *The reverse case:* a stratum whose second PSU has only zero weights is treated as a two-PSU stratum instead of the single-PSU (unestimable) stratum it really is.

**Proposed minimal diff** (unapplied; `git apply --check` passes; SHA-256 prefix `3db1a415`). It replaces the combined check with:
1. reject non-finite weights anywhere;
2. reject negative weights;
3. **drop w = 0 records from the design**, keeping the domain indicator for the remaining records;
4. the existing complete-in-domain and positive-domain-sum checks.

**No domain filtering is introduced.** Domain members and non-members with positive weight stay in the design, and non-members contribute 0 to the linearised variable.

**Effect on design and variance:**
- the point estimate is unchanged (zero weights contribute nothing);
- the SE changes only when a PSU consists entirely of zero-weight records;
- a stratum whose PSUs are all zero-weight except one now raises (single PSU) instead of returning a mis-specified variance.

| Situation | Before | After |
|---|---|---|
| NaN or inf weight (any record) | NaN result, or the record silently dropped | `ValueError` ("must be finite") |
| Zero-weight-only PSU | Counted in n_h; SE altered | Not part of the design; SE as without those records |
| Stratum left with one positive-weight PSU | Variance computed with a phantom PSU | `ValueError` (single PSU) |
| NaN `x` outside the domain | Allowed | Allowed (unchanged) |
| All existing tests | Pass | Pass |

**Scientific consequences if the defects remain:**
- **D1:** a data-handling error (a missing fasting weight) would produce NaN in Table 2 or silently drop records, rather than stopping the analysis.
- **D2:** design-based SEs and CIs could deviate from NCHS practice whenever zero-weight records are passed (for example, a full-file domain analysis that includes participants outside the fasting subsample).

**Approval request [RD]:**
> "I authorise applying `2026-11-12_R15_proposed.patch` (D1, D2) with its two regression tests."

The R15 wording for the protocol stays a D-019 item.

## 2. R15 — regression-test plan
Both tests are in the patch and were added to the scratch copy **before** the code change:

| Test | Asserts | On current code | On patched code |
|---|---|---|---|
| `test_r15_d1_nonfinite_weights_rejected` | NaN and inf weight, in and out of the domain → `ValueError`; NaN `x` outside the domain still allowed | FAIL | PASS |
| `test_r15_d2_zero_weight_records_are_not_part_of_the_design` | A zero-weight-only PSU leaves estimate and SE unchanged; a stratum reduced to one positive-weight PSU raises | FAIL | PASS |
| Existing model suite | No regression | 71 OK | 73 OK (71 + 2) |

## 3. Q-052 — variance-validation report
| Aspect | Implementation | Guidance / check |
|---|---|---|
| Variance formula | Σ_h n_h/(n_h−1) Σ_i (z_hi − z̄_h)², z = d·w·(x − r̂)/Σd·w (with-replacement Taylor linearisation of the ratio mean) | CDC: Taylor linearisation, with replacement [V]. The formula itself is not printed on the page read |
| PSU handling | PSU totals of z within strata | Consistent |
| Strata | Sum over strata; single-PSU strata raise (no collapsing) | Consistent; no collapsing rule is chosen |
| Degrees of freedom | **Not returned** | CDC: df = #PSUs − #strata [V]. **[TR]:** return or document df for CIs (t-quantile) at a later approved change; not in the R15 patch |
| Domain estimation | Indicator over all non-zero-weight records (after the patch) | CDC instruction [V] |

**Independent cross-checks** (scratch, synthetic; 15 strata × 2 PSUs; n = 6,000; patched code):
- the classical ratio-estimator variance from PSU totals, [V(Ŷ) − 2R̂·C(Ŷ, X̂) + R̂²·V(X̂)] / X̂², agrees to **relative difference 1.3×10⁻¹⁵**;
- the delete-one-PSU jackknife (JKn) agrees within **0.01%** (expected to be close, not identical);
- design df = 15.

**Limitation:** **no authoritative reference implementation** (R `survey`, SAS `SURVEYMEANS`, Stata `svy`, SUDAAN) is available, and installing one is not permitted. **Q-052 remains open** for a reference comparison after A3 (for example, a verified Python survey package, or R if an environment is approved) [RD].

## 4. Option C — incremental-value study design (proposal; D-016 not approved)
**Question:** does adding biochemical biomarkers to non-laboratory predictors give measurable incremental predictive value under temporal validation for laboratory-defined dysglycaemia?

All elements are existing protocol (v1.0 candidate) elements. No CR-02 predictors and no new variables or designs.

| Element | Specification |
|---|---|
| Groups | C (6 non-laboratory: age, sex, BMI, waist, SBP, DBP); A (21 analytes); B = A + C (27) |
| Primary contrast | **B − C** (increment of biochemistry over the non-laboratory set). Secondary: A − C (biochemistry alone vs clinical) |
| Models | Framework (F2 + F3) and BL-1, as protocol Q1 states |
| Participants | Identical eligible samples (N = 3,088 dev / 2,485 val). In-fold imputation keeps N constant across groups. S-10a complete-case on the intersection of the groups as sensitivity |
| Split and seeds | Identical D-train/D-cal splits, folds and 5 seeds across groups; the same temporal split; frozen models applied once |
| Leakage | In-fold preprocessing; validation isolation (tested); serum glucose and awareness items excluded |
| Harmonisation | S-08 reference; S-09b only if Q-046 is decided. *Asymmetry:* only groups A and B carry inter-period measurement changes. This can depress their temporal performance and must be reported as a limitation, not adjusted after results |
| Missing data | Median/mode + indicators above 5% (group A has more missingness than C). The complete-case sensitivity analysis guards against imputation-driven differences |
| Paired comparisons | All on the **same participants**: paired bootstrap (2,000) of ΔAUROC, Δlog loss, ΔBrier and ΔICI on **calibrated** probabilities; internal (calibrated OOF; Q-100) and temporal |
| Calibration differences | ΔICI, Δslope, Δintercept |
| Decision curves | **Only if M10 is retained** (Q-054); otherwise omitted |
| Reporting of C | Group C's own performance is always reported, so the increment is interpretable |

**Result categories** (all permitted, all reported):

| Outcome | Rule (CI = paired-bootstrap 95% CI of B − C) |
|---|---|
| Positive increment | CI entirely > 0 **and** above the practical threshold, if one is set |
| Negligible increment | CI includes 0, or lies entirely within ± the practical threshold, if one is set. *Without a threshold, "negligible" cannot be claimed; report "no demonstrated increment"* |
| Negative increment | CI entirely < 0 (possible under temporal shift affecting the laboratory analytes) |
| Uncertain | A wide CI spanning clinically different conclusions; reported as inconclusive |

**Ways to define a meaningful-improvement threshold [RD] (none chosen):**

| Option | How | Consequence |
|---|---|---|
| (i) None | Report differences and CIs only | Safest; no "negligible" or "meaningful" verdict is possible |
| (ii) ΔAUROC threshold from verified literature | Requires a verified source (none found) | A defensible verdict if sourced; otherwise arbitrary |
| (iii) Net-benefit-based | ΔNB over a justified threshold range | Requires M10 and a justified range (Q-054); no source yet |
| (iv) A researcher-set threshold, fixed before results | e.g. a stated ΔAUROC | Allowed only if fixed and recorded before any result; must be reported as a judgement |

**Overstatement guards:** no non-inferiority or equivalence claim without a margin (Q-054); temporal ≠ external validation; no clinical-utility claim; multiplicity for Q1 as drafted.

## 5. CR-02 / CR-03 — access and evidence status
| | CR-02 | CR-03 |
|---|---|---|
| Official record | Yoo D, Maggiore U, Jolliet O. Enhancing prediabetes and diabetes detection through a machine learning-enabled self-assessment approach. *J Clin Epidemiol* 2026;195:112266. doi:10.1016/j.jclinepi.2026.112266; PMID 41950976 [MD] | Hutchison AL, Rinella ME, Mirmira RG, Parker WF. Development and validation of a multivariable prediction model for pre-diabetes and diabetes using easily obtainable clinical data. *medRxiv* 2025-02-12 (version 1). doi:10.1101/2025.02.10.25321897; PMID 39990568; PMC11844569 (abstract only) [MD] |
| Corresponding author | Daniel Yoo, Section for Quantitative Sustainability Assessment, Technical University of Denmark (electronic address given in the PubMed affiliation record; not copied into this public repository) | — |
| Legitimate route | (1) Your institutional library (subscription or ScienceDirect access); (2) interlibrary loan; (3) an author request (draft below) | The public medRxiv record at `https://doi.org/10.1101/2025.02.10.25321897`. Open the "Full Text" / PDF tab in a browser (the PMC page states the full text is available from the preprint server) |
| Evidence status | **Abstract** (unchanged) | **Abstract** (unchanged) |

**Author-contact draft** (for you to send if you choose):
> "Dear Dr Yoo, I am conducting a prediction-modelling study on laboratory-defined dysglycaemia in NHANES and would like to read your article 'Enhancing prediabetes and diabetes detection through a machine learning-enabled self-assessment approach' (J Clin Epidemiol 2026;195:112266) in full, in particular the candidate predictors considered during development, the calibration and interpretability methods, and the handling of NHANES 2021–2023. Would you be able to share the accepted manuscript or a PDF for personal research use? Thank you."

The evidence matrix in `2026-11-12_EVIDENCE-AND-DECISION-READINESS_REVIEW.md` §2 is unchanged, because no new evidence was obtained.

## 6. R14 — ICI decision packet
**Sources:**
- Austin & Steyerberg 2019 [V, partial: they used R `loess(Y∼P)` and `lowess(Y∼P, iter = 0)`];
- **R source code [V]** via the GitHub mirror `wch/r-source` (trunk, fetched 2026-11-12; the official `svn.r-project.org` is blocked);
- the R version the paper used is not stated in the text read, so default stability over time is **[UV]**.

| | (a) Existing | (b) R `lowess` default | (c) R `loess` default |
|---|---|---|---|
| Smoothing method | Local-linear, tricube, nearest-neighbour bandwidth, no robustness iterations, evaluated at each point | Local-linear, tricube; `iter` default 3 (**the paper set `iter = 0`**); interpolation within `delta = 0.01·range(x)` | **Local quadratic** (`degree = 2`), tricube, Gaussian family; `loess.control(surface = "interpolate")` default (approximate evaluation) |
| Span | 0.75; neighbourhood ⌈0.75·n⌉ (min 3) | `f = 2/3`; neighbourhood ⌊f·n + 1e-7⌋ (min 2) (`lowess.c`) | `span = 0.75` |
| Fidelity to the paper | Same family as their `lowess(iter = 0)`; span differs | **Closest to their `lowess(iter = 0)` variant**, except `delta` interpolation and the floor/ceiling neighbourhood rule | Closest to their **primary** `loess`, but exact reproduction of `surface = "interpolate"` is hard |
| Reproducibility | High | High (one constant) | Medium (KD-tree interpolation; `surface = "direct"` reproducible but not the default) |
| Compatibility | Full | Full | New function; interface unchanged |
| Effort | None | One constant + test | New local-quadratic code + tests; the R comparison itself needs R |
| Absolute ICI sensitivity | Smoother-specific | Smoother-specific | Smoother-specific; Austin & Steyerberg found `lowess` gave the lowest metric values and RCS the highest |
| Between-model ΔICI sensitivity | One synthetic setting: stable for spans 0.5–0.9 (+0.060 to +0.062). **Not established in general** | Expected similar; untested | Untested |

**Sensitivity-analysis specification** (proposed [TR]; prespecified, computed on the **same** frozen predictions, no refitting, no reselection after results):

| Setting | Smoother | Span |
|---|---|---|
| S0 | Local-linear, no robustness iterations | 0.75 (current) |
| S1 | Local-linear, no robustness iterations | 2/3 (approximates R `lowess(iter = 0)`, without `delta` interpolation) |
| S2 | Local-quadratic, direct evaluation | 0.75 (approximates R `loess` with `surface = "direct"`); only if (c) or S2 is approved, since it needs new code |
| S3 | Local-linear | 0.5 and 0.9 (span bracket) |

- **Report:** absolute ICI per model, and Q2 ΔICI with paired-bootstrap CIs under each setting.
- **The primary setting is the one chosen in R14.** The others are reported in a supplement.
- **Conclusion rule:** state whether the sign and CI-overlap of ΔICI agree across settings. No setting is chosen after seeing results.

**[RD]:** R14 = (a), (b) or (c), and approval of the sensitivity specification. The ICI code is not changed.

## 7. Methodological-reference verification table
| Method (code location) | Reference | Identifier | Level | Exact claim supported | Supports the manuscript statement? |
|---|---|---|---|---|---|
| Holm (`stats.holm`) | Holm S. A simple sequentially rejective multiple test procedure. *Scand J Stat* 1979 (volume/pages not retrieved) | No DOI retrieved | **[AB]** (abstract text via a search-engine record; not a primary record) | Sequentially rejective procedure controlling type I error for any combination of true hypotheses | At abstract level only; primary record needed for volume/pages |
| Platt (`calibration.PlattCalibrator`) | Platt JC. Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods | — | **[MD], discrepancy unresolved:** one record gives 1999 (technical-report URL); Lin et al. (2007) cite it as a chapter in Smola et al. (eds.), *Advances in Large Margin Classifiers*, MIT Press, 2000. Primary bibliographic hosts (MIT Press, dblp, Springer) are blocked. **Not resolved; nothing fabricated** | Sigmoid mapping of scores to probabilities (abstract fragment) | Partly. Our IRLS logistic recalibration on logit scores is a Platt-type sigmoid; whether Platt's target adjustment is used is **not** verified against the text |
| Bootstrap (`stats.py`) | Efron B. Bootstrap methods: another look at the jackknife. *Ann Stat* 1979 | No DOI retrieved | **[AB]** | General bootstrap principle | Percentile-interval and paired-comparison specifics: source still needed [UV] |
| AUROC / Mann–Whitney (`metrics.auroc`, ties = ½) | Hanley JA, McNeil BJ. The meaning and use of the area under a receiver operating characteristic (ROC) curve. *Radiology* 1982;143(1):29–36. doi:10.1148/radiology.143.1.7063747; PMID 7063747 | doi | **[AB]** (PubMed) | The AUC equals the probability of correctly ranking a diseased above a non-diseased subject, the quantity estimated by the Wilcoxon statistic | Yes, for the equivalence. Tie handling is not covered by the abstract |
| Lowess (`metrics._lowess`) | Cleveland WS (1979, 1981) are **named as references in R's `lowess` help page** [V: help-page keys `R:Cleveland:1979`, `R:Cleveland:1981`] | — | **[MD-pointer]**: full bibliographic entries not retrieved | Algorithm as implemented in R `lowess.c` [V source] | Algorithm description yes (via R source); a citation needs the primary record |
| Isotonic / PAVA (`calibration.pava`) | — | — | **[UV] not located** | — | Only if isotonic (S-14) is reported; deferred under A6-a |
| Wilson interval (`report._wilson`) | — | — | **[UV] not located** | — | Needed for calibration-curve figure captions |
| Elastic net, RF, RBF-SVM, MLP, k-NN (originals) | — | — | **[UV] not located** | Software reference instead: Pedregosa et al., *JMLR* 2011 **[V]** | Cite the originals only where the manuscript describes an algorithm |
| Explanation-stability metrics | Krishna S et al., *TMLR* (06/2024); arXiv:2202.01602v6 | arXiv | **[V]** | Definitions of feature agreement (top-k), Spearman rank correlation, pairwise rank agreement, between explanation methods | Definitions yes; refit/period use is an adaptation (section 8) |
| NHANES variance | CDC/NCHS tutorial | URL | **[V]** | Taylor; with replacement; non-zero-weight records + indicator; df = PSUs − strata | Yes |

*Search-engine summaries were not used as substitutes for publications.* Where only such a record exists, the level is [AB] or [MD] and the item is not cited until a primary record is obtained.

## 8. Explanation-stability methodology note (D-019 not resolved; code unchanged)
- **Original use [V]:** Krishna et al. compare the explanations **of different explanation methods** (LIME, KernelSHAP, gradient methods) for the **same model and prediction**, mostly per data point and averaged over test points. Their metrics:
  - feature agreement = |top-k(Ea) ∩ top-k(Eb)| / k;
  - rank correlation = Spearman between feature rankings;
  - pairwise rank agreement = the fraction of feature pairs ordered alike.
- **Proposed adaptation to refits:** for B bootstrap refits of the same pipeline, compute global importance g_b (mean |SHAP| per feature) on a fixed evaluation set. Stability is the distribution of Spearman ρ(g_b, g_b′) over pairs, plus top-k overlap with a prespecified k.
- **Proposed adaptation to periods:** with the **frozen** primary model, compute g_dev (development) and g_val (2021–2023); ρ(g_dev, g_val) and top-k overlap. This measures how the model's reliance pattern **expresses itself on shifted data**, not model instability.
- **Why pairwise refit correlations are dependent:** each refit appears in B − 1 of the B(B − 1)/2 pairs, so the pairwise values are correlated. Treating them as independent overstates precision.
- **Why a naive CI is wrong:** a t- or normal-based CI over the B(B − 1)/2 pairwise values assumes independence and uses the wrong effective sample size.
- **Descriptive approach [TR]:** report the median and the 2.5th–97.5th percentiles of pairwise ρ (and of top-k overlap) as a **descriptive spread**, explicitly not a confidence interval. For the between-period ρ, a percentile bootstrap over validation participants (recomputing g_val) is a defensible interval for that single quantity.
- **Limitations:**
  - global importance can be stable while individual explanations are not;
  - mean |SHAP| ignores direction;
  - correlated predictors (e.g. waist/BMI, liver enzymes) can swap ranks without a substantive change;
  - rank metrics ignore the size of importance gaps;
  - explanations describe the model, not causation;
  - **no verified source applies these metrics to refit or temporal stability.** The adaptation is the study's own operationalisation and is labelled as such.
- **Alvarez-Melis & Jaakkola (2018) [V]** concern robustness to **input perturbations** (local Lipschitz estimates) and are cited only as motivation.

## 9. Q-061 — evidence status
- **Still missing** (primary source: ADA, *Diabetes Care* 2026;49(Suppl 1):S27–S49, doi:10.2337/dc26-S002, Section 2):
  - the exact wording for HbA1c ≥ 5.7% and FPG ≥ 100 mg/dL as prediabetes lower limits;
  - HbA1c ≥ 6.5% and FPG ≥ 126 mg/dL as diabetes thresholds;
  - the confirmatory-testing guidance;
  - whether each test alone satisfies the criterion;
  - the table or section reference.
- **Status:** **[UV]**, with four failed access attempts.
- **Secondary papers** (Türkoğlu Genç & Yildiz 2026; CR-02) are corroboration only and are not equivalent to the primary source.
- **Route 1** (primary source verified) and **Route 2** (numerical rule, no claim of ADA equivalence) are unchanged from the previous review §6.
- **Thresholds unchanged. No route selected [RD].**

## 10. Critical path (2026-11-12, about 12:30 UTC; no approval received)
| Question | Assessment |
|---|---|
| Is the 11-13 approval milestone still feasible? | Yes, if the Part 1 approvals **and** a named custodian arrive by the end of 11-13. There is no slack |
| R-1 status | **Approaching, not triggered.** Triggered (for your decision) if title/abstract screening cannot finish by 11-19 |
| If 11-13 is missed | Every downstream date moves day for day. Approvals on 11-14 → Stage 0 11-15 → pilot 11-17 → screening 11-21, which **meets the R-1 condition**. Each further day pushes the gates and freeze past 11-22, which **meets the R-2 condition** |
| Is the 11-19 screening date achievable? | Only with Stage 0 by 11-14 and a passed pilot by 11-16. It depends on you (audit, missing-abstract review) and the custodian |
| Is 11-27 feasible? | Feasible for the full scope only on the schedule above. With one day's delay, feasible with R-1 (if you approve it). With a failed pilot (about +5 days), only with R-3 (two manuscripts) |

- **Parallel lanes once approved:** A3 install → A4 synthetic runs; the download + build; the AB-7 look-up and rebuild.
- **Additional parallel items:** the R15 patch (if approved); the CR-02/CR-03/ADA PDFs.
- **R-1, R-2 and R-3 are never automatic. Validation and safeguards are never reduced.**

## 11. Concise researcher decision sheet
| # | Decision | Needed by |
|---|---|---|
| 1 | **A1, A5** (A5 = the existing 61-path list; this file and the R15 patch are **not** in it, and would need a separate scope update) | 11-13 |
| 2 | **A2:** a named independent custodian (C1–C6) + S1/S2 with your basis | 11-13 |
| 3 | **R15 patch:** approve applying `2026-11-12_R15_proposed.patch` (D1, D2 + tests), or defer | Before any design-based estimate |
| 4 | **Q-061:** supply the ADA PDF (Route 1) or accept Route 2 | Before D-019 (latest 11-20) |
| 5 | **CR-02 / CR-03 full texts:** library / ILL / author request (CR-02); medRxiv download (CR-03) | Before D-016 |
| 6 | A3, A4, A6, Q-098, Q-099, Q-054, Q-100 (prepared earlier) | 11-13 to 11-14 |
| 7 | **D-016:** contribution (recommendation C, with B elements secondary) | After the RQ5 review and CR-02 |
| 8 | **D-019:** R14 option + sensitivity spec; F5 metric (Spearman primary, top-k with k); the Option C threshold (one of i–iv); df reporting (Q-052); R13–R15 wording | 11-22 |
