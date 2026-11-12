# Appendix A. Statistical analysis plan (manuscript draft)

> **Draft, 2026-11-12. A plan, not results.** It restates the v1.0 candidate (`research/methodology/experimental_protocol_v1.0_candidate_full.md`), which is **not approved**. It becomes final only with the researcher's D-019 freeze, and every **[pending: …]** item may change there. No analysis described here has been run on real data, and no performance target is set (CLAUDE.md rule 16).

## A.1 Estimands
| Question | Estimand | Population / data | Primary measure |
|---|---|---|---|
| Q1, value of biochemistry | Difference in discrimination between predictor groups (B − C; A − C), for the framework and BL-1 | Development (internal) and 2021–2023 (temporal) | AUROC difference, 95% CI |
| Q2, framework vs calibrated baselines | Difference in calibration and overall accuracy (framework − baseline), group B | As above | ICI and Brier difference, paired bootstrap, Holm across the 6 baselines within each metric; AUROC per [pending: Q-054] |
| Q3, temporal transfer | Change from internal to temporal validation, per model and metric | Internal reference [pending: Q-100] vs temporal validation | Difference, with bootstrap 95% CI for the temporal value |

## A.2 Analysis sets
- **Development:** the eligible 2017–March 2020 sample (planned N = 3,088), split per seed into D-train (80%) and D-cal (20%), stratified by outcome.
- **Temporal validation:** the eligible 2021–2023 sample (planned N = 2,485), used once, with frozen models.
- **Complete-case variants (S-10a):** per predictor group.

## A.3 Order of operations (fixed; enforced in software)
1. Configuration fixed and hashed: search spaces, budget 40, 5 seeds from master seed 20261112, α = 0.10, sensitivity target 0.80.
2. Per seed:
   - split;
   - 5-fold cross-validated tuning by log loss (in-fold preprocessing);
   - refit on D-train;
   - on D-cal only: Platt calibration, conformal quantiles and the threshold;
   - freeze.
3. Internal estimates:
   - (a) raw out-of-fold;
   - (b) calibrated out-of-fold, on the threshold's scale.
4. Temporal validation: the frozen primary-seed model is applied once. Its data fingerprint is recorded.
5. Comparisons (A.1), then sensitivity analyses (A.6), then reporting. No step feeds back into an earlier one.

## A.4 Uncertainty of estimates
- **Temporal validation:** participant-level bootstrap, 2,000 resamples, percentile 95% CIs. Model differences use a paired bootstrap on the same resamples.
- **Internal:** mean ± SD and range over 5 seeds, on pooled out-of-fold predictions per seed. There are no t-tests on overlapping folds.
- **Design-aware secondary:** bootstrap resampling PSUs within strata [pending: FA-7].
- **Multiplicity:** Holm within Q2 for each primary metric. Q1 and Q3 are reported unadjusted, and this is stated.

## A.5 Calibration and uncertainty specifics
- **Calibration metrics:**
  - ICI: local linear smoothing, tricube kernel, span 0.75;
  - calibration intercept and slope from logistic recalibration;
  - ECE: 10 equal-width bins, secondary;
  - calibration curves: 10 bins (equal-width; equal-count as a check) with Wilson 95% intervals. Bins with fewer than [pending: minimum cell size] participants are not exported.
- **Conformal:** class-conditional coverage and mean set size at α = 0.10. With an order-preserving calibrator (Platt slope > 0, recorded per run) the sets equal those from raw scores, so the split-conformal guarantee is unaffected by fitting both on D-cal.
- **Threshold:** the largest t with D-cal sensitivity ≥ 0.80 on calibrated probabilities. Sensitivity and specificity are reported at temporal validation and on internal estimate (b).

## A.6 Sensitivity analyses and ablations
- **Kept** [pending: A6]:
  - S-01 (HbA1c-only outcome);
  - S-08 (unadjusted 2021–2023 values; reference);
  - S-10a (complete cases);
  - S-13 (folds grouped by stratum × PSU);
  - S-09b (CDC backward equations), only if Q-046 is decided;
  - ablations ABL-1 (without F3) and ABL-2 (without F4).
- **Deferred:** all others, declared before any result.

## A.7 Missing data and weighting
- **Missing values:** in-fold median or mode imputation, with missingness indicators above 5% missing.
- **Weighting:** primary performance unweighted; secondary fasting-weighted [pending: FA-7].
- **Descriptive population estimates:** Taylor linearisation. Single-PSU strata stop the computation [pending: Q-052].

## A.8 Explanations
- **Method:** TreeSHAP on the uncalibrated F2 margin.
- **Stability:** Spearman correlation of global importance across 50 bootstrap refits [R-1 reduction: 20, only if applied by decision] and between periods. Sign agreement with BL-1 coefficients.
- Explanations are described as model behaviour, not causation.

## A.9 Reproducibility controls
- Each run record contains:
  - the configuration hash and the protocol version and SHA-256;
  - the seeds;
  - the development and validation data fingerprints;
  - the Git commit and package versions;
  - all per-seed results.
- Real-data runs are refused unless:
  - an authorisation is referenced;
  - the protocol file matches its recorded SHA-256;
  - the Git working tree is clean.
- Participant-level predictions are held in memory or written only to Git-ignored locations.

## A.10 Reporting rules
- All prespecified analyses are reported, including null, negative and failed results.
- Deferred analyses are listed as future work.
- Any deviation from this plan is reported as a deviation with its reason.
