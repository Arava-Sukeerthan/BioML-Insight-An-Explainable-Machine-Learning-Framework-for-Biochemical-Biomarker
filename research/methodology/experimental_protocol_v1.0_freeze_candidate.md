# Experimental protocol v1.0 — freeze candidate (change set against v0.1 revision 5)

| Field | Value |
|---|---|
| Status | **Assistant draft, 2026-11-12. NOT approved, NOT frozen, NOT in force.** It becomes v1.0 only through the researcher's D-019 decision; until then `experimental_protocol_v0.1_draft.md` revision 5 is the current draft |
| Form | A change set. v1.0 = v0.1 revision 5 with the changes below applied. At the freeze the complete text is assembled, hashed and recorded, like the screening freeze (D-110) |
| Basis | v0.1 revision 5; preparation pack corrections C1–C6 (2026-11-12); approval item A6 (proposed, not approved); the implementation in `scripts/models/` and `scripts/nhanes/build_dataset.py` |
| Gates | D-042: the Stage C and Stage D gates (D-016) must pass before D-017, D-018 and D-019 are approved and before any model is trained on real data. This candidate passes no gate |
| Not claimed | No result, performance level, novelty or clinical validity. "Comparable discrimination" is assessed only as defined in §5 below |

## 1. Corrections (no change of meaning)
| # | v0.1 section | Change |
|---|---|---|
| C1 | §8 "Principle" | Replace the claim that backward equations are primary with: "The reference analysis uses unadjusted 2021–2023 values (S-08); CDC backward equations at cycle level are sensitivity analysis S-09b (see §8.2 and FA-5 below)." |
| C2 | §26 "Before literature screening" | Replace with: "Screening activation follows D-108 (fixed-inventory entry → six D-035 §6 rows → D-074 (f) → Stage 0 → D-077 (6) → draw)." |
| C3 | §23 milestones | Replace with the 2026-11-27 schedule in the current task report |
| C4 | §26 blocker AB-1 | Mark the date condition (≥ 2026-11-03) as met: necessary, not sufficient |
| C5 | Appendix B vs §8 | State that calcium, panel cholesterol and phosphorus ("Adjustment Not Recommended") are not candidate predictors, so they are not listed in §8 |
| C6 | Environment | Network access to `wwwn.cdc.gov` is re-checked at the download authorisation and the result recorded |

## 2. Threshold rule (resolves the wording problem in §12 item 6, FA-10, Q-053)
v0.1 says "the smallest probability threshold giving sensitivity ≥ 0.80". Read literally, this always selects the lowest score. **Proposed wording:**
> The decision threshold t is the **largest** value such that the rule "positive if p ≥ t" has sensitivity ≥ 0.80 among the D-cal participants with y = 1, computed on calibrated probabilities. It is fixed before temporal validation and applied unchanged.

Implemented as `metrics.threshold_for_sensitivity`. Tests: a hand-computed case, and agreement with an exhaustive search over 200 random cases with tied scores.

Consequences, made explicit (review 2026-11-12, §9):
- With tied scores (e.g., isotonic in S-14), sensitivity on D-cal can exceed 0.80. Ties never make it fall below 0.80.
- M7 is not reported for D-cal itself: sensitivity there is ≥ 0.80 by construction. M7 is reported at temporal validation, and internally only on calibrated out-of-fold predictions (§9 R2).
- With an order-preserving calibrator (Platt, slope > 0), a threshold on calibrated probabilities is equivalent to a threshold on raw scores.

## 3. Harmonisation (FA-5; Q-044, Q-046, Q-060)
- **Reference analysis:** S-08, unadjusted values in both periods.
- **S-09b** (backward equations for TRIG, ALT, ALP, GGT, BUN and total bilirubin) runs only if Q-046 is decided. Q-044's mg/dL reading is accepted for S-09b, with the §8.1 check stated as supporting evidence only.
- **Limitations stated in the paper:** the triglyceride method differs between periods, and HbA1c changed instrument within 2021–2023.
- **AB-9:** the equations are to be re-checked character by character against the CDC pages before S-09b is run.

## 4. Scope for the 2026-11-27 deadline (approval item A6; proposed)
| Element | v1.0 candidate |
|---|---|
| Primary comparisons | Q1 (B vs C and A vs C; framework and BL-1), Q2 (framework vs the 6 calibrated baselines, group B), Q3 (temporal transfer) — unchanged |
| Baselines | BL-1 to BL-6. Q-048: XGBoost proposed (alternative: scikit-learn histogram gradient boosting, fewer dependencies; see the A3 findings). Q-049: k-NN proposed |
| Seeds and budget | 5 seeds; 40 configurations per method; search spaces in `scripts/models/experiment_config_draft.json`; BL-1 grid 8 × 5 |
| Sensitivity analyses kept | S-01, S-08 (reference), S-10a, S-13; S-09b only if Q-046 is decided |
| Sensitivity analyses deferred (declared now, before results, as future work) | S-02, S-03, S-04, S-05, S-06, S-07, S-09, S-10b, S-11, S-12, S-14, S-15a, S-15b, S-16a, S-16b |
| Ablations | Ablations AB-1 (no F3) and AB-2 (no F4) kept; ablations AB-3 to AB-5 deferred (labels: §9 R9) |
| Explanations | TreeSHAP stability over 50 bootstrap refits and between periods (F5); sign agreement with BL-1 |

## 5. Comparison rules (FA-11; Q-054 — researcher decision)
- **Q2 primary metrics:** ICI and Brier score; paired bootstrap (2,000 resamples); Holm adjustment within each metric family (`compare.py`).
- **AUROC: two options; I recommend (b).** v0.1 gives no margin value and cites no verified source for one.
  - (a) Non-inferiority with a margin of `<value>`. A justification must be stated before the freeze.
  - (b) **No formal non-inferiority claim.** The AUROC difference and its 95% CI are reported descriptively. This is the smallest defensible choice without a verified margin source.
- **M10 net benefit:** without a justified threshold range (Q-054), it is reported descriptively over 0.05–0.95 and not used for any conclusion, or it is dropped.

## 6. Settings fixed by the implementation (no scientific change; listed for completeness)
- **ICI:** local linear smoothing (tricube kernel, span 0.75).
- **ECE:** 10 equal-width bins (secondary).
- **Conformal:** class-conditional split conformal, α = 0.10; finite-sample rank ⌈(n_c + 1)(1 − α)⌉; +∞ if the rank exceeds n_c (Q-051).
- **Descriptive survey estimates:** Taylor linearisation, PSUs within strata, with replacement. A single-PSU stratum stops the computation rather than being collapsed silently (Q-052).
- **Preprocessing:** median or mode imputation with missingness indicators above 5%; log(x + 1) for TRIG, URDACT, ALT, AST and GGT; scaling only for BL-1, BL-4, BL-5 and BL-6.
- **Real-data guard:** the harness refuses REAL data without an authorisation reference and a non-draft protocol version.

## 7. Disclosure of prior aggregate access to the validation period
On 2026-10-24, before any model, aggregate counts were computed on the 2021–2023 files: the eligibility cascade, outcome prevalence, missingness, medians and unit checks (`scripts/nhanes/descriptive_counts.py`). No predictor–outcome relationship was examined and no model was fitted. The manuscript states this. All outcome, feature, harmonisation and analysis choices are fixed at this freeze, before any model is run.

## 8. What the researcher decides at the freeze (unchanged reservation)
- FA-1 to FA-13 (v0.1 §24), with the values proposed above, including the Q3 reference (§9 R3);
- Q-048, Q-049, Q-050, Q-051, Q-052, Q-053, Q-054, Q-056;
- Q-044, Q-046, Q-060 or the S-08 reference;
- D-013, D-014, D-015;
- the A6 scope.

Nothing in this candidate takes effect before that decision.

## 9. Internal-consistency review (2026-11-12; assistant review, not approval)
| # | Finding | Status |
|---|---|---|
| R1 | Threshold rule (§2): the "largest t" wording matches the implementation, including ties | **Consistent.** Verified by test |
| R2 | The harness applied the D-cal threshold, fixed on **calibrated** probabilities, to **uncalibrated** out-of-fold predictions when computing internal M7 (a scale mismatch) | **Corrected in the code.** Raw internal metrics now omit M7. A calibrated internal estimate (out-of-fold predictions passed through the D-cal calibrator) reports M7–M9. Tested; a mutation check confirms the test fails on the old code |
| R3 | v0.1 Q3 ("change from internal to temporal validation") compares uncalibrated internal metrics with calibrated temporal metrics. For calibration metrics (ICI, slope, Brier), the change would mix the effect of calibration with temporal transfer | **Researcher decision (FA-11).** Proposed: the Q3 reference is the calibrated internal estimate (`internal_calibrated_summary`), which is like for like with temporal validation. Both estimates are recorded. AUROC is identical under an increasing Platt fit |
| R4 | D-cal is used for both the calibrator and the conformal quantiles. Conformal validity needs the score order to be independent of the calibration data | **Consistent for Platt with slope > 0:** the sets are identical to those from raw scores, so the split-conformal guarantee holds. Isotonic can only add labels (conservative). Both are tested. Each run records `calibrator_order_preserving`; a `false` value is reported, not hidden |
| R5 | v0.1 §14: Holm within Q2 for each primary metric; Q1 and Q3 unadjusted with that stated. §5 here ("within each metric family") means the same | **Consistent** |
| R6 | v0.1 Q2 also reports uncalibrated baselines. That needs one extra run per baseline with `calibration: none` (same seeds and budget) | **Implementation note.** It adds 6 runs, which is within budget |
| R7 | Reduced scope for the deadline: Q1 needs groups A, B and C, but only for the framework and BL-1 | **Clarified.** A reduced scope may limit the six baselines to group B (Q2); it may not drop groups A or C for the framework and BL-1 (Q1). The 2026-11-12 report's phrase "predictor group B only" applies to the baselines only |
| R8 | Primary performance is unweighted and secondary is fasting-weighted (v0.1 FA-7). `apply_frozen` accepts weights; weighted internal estimates are not implemented | **Implementation note.** The secondary weighted analysis is applied at temporal validation; internally it is deferred unless FA-7 requires it |
| R9 | v0.1 uses the labels "AB-1" to "AB-13" for activation blockers (§26) **and** "AB-1" to "AB-5" for ablations (§15). C4 above and §4 use both meanings | **Proposed (editorial, no change of meaning):** rename the ablations ABL-1 to ABL-5 in v1.0. Until then, "ablation AB-n" and "blocker AB-n" are written out in full |
| R10 | Prediction-scale audit (2026-11-12, follow-up). Every metric path was checked: temporal validation — all metrics on calibrated p; threshold and conformal sets on calibrated p. Internal (a) raw — no M7/M8/M9. Internal (b) calibrated — M1–M9 on the threshold's scale. F5 explanations — on the uncalibrated F2 margin (scale-free ranking). Ablation AB-1 (without F3) — threshold and conformal set on raw p, consistently. **Defect found:** `run_experiment(return_predictions=True)` returned only the raw out-of-fold predictions, so a Q2 paired comparison built from them would have used the uncalibrated scale | **Corrected.** Both `p_raw` and `p_calibrated` are returned with explicit names; the docstring states that Q2 uses `p_calibrated`. A test ties each to its logged summary |
| R11 | v0.1 §15 says "mean ± SD over folds and seeds", but the harness pools the out-of-fold predictions per seed and summarises over seeds. Per-fold metrics on about 500 cases are noisier, and the calibration metrics (ICI) are unstable on small folds | **Proposed wording** (in the assembled text): pooled out-of-fold predictions per seed; mean ± SD and range over seeds |
| R12 | v0.1 §15 logs runs in `logs/EXPERIMENT_LOG.md` only. The harness writes `runs.jsonl`. The real-data guard did not bind the run to the frozen protocol text, and a dirty Git tree was recorded but not refused. The validation-data fingerprint was not recorded | **Implemented.** Real-data runs now need `protocol_path` + `protocol_sha256` (the file hash must match) and a clean, committed tree; the validation fingerprint is recorded. Tested via `_guard` only, with no REAL-labelled run on synthetic data. Logging wording updated in the assembled text |
| R13 | Candidate-reference pre-verification (2026-11-12, `research/reviews/2026-11-12_AB-7_reference_preverification.md`) found: (1) §11.1 "CR-01 to CR-04 report LR comparators" is not supported for CR-03 (its abstract has no LR comparator); (2) CR-01 and CR-05 concern undiagnosed **diabetes**, not prediabetes-range dysglycaemia; (3) Appendix D lists CR-03 as "Not in inventory", but it is P3005 (in the D-044 scope); (4) the CR-08 thresholds remain unverified (Q-061); (5) CR-10 may be unnecessary after R11 | **Researcher, at D-019.** Proposed: reword §11.1 to cite only references whose claim is confirmed at full text; describe CR-01 and CR-05 as context; correct Appendix D; drop the CR-10 sentence if R11 is accepted. Nothing is citable before D-064 verification (AB-7) |
| R14 | The primary calibration metric ICI (M6, Q2) has a primary source (Austin & Steyerberg, *Stat Med* 2019, PMID 31270850; CR-13, full text read). That paper builds its calibration curve with R `loess(Y∼P)` and `lowess(Y∼P, iter = 0)`. `metrics.ici` uses local-linear smoothing with span 0.75, which the paper does not state to be equal to either. CR-02 (closest prior art) uses the **same composite outcome** and validates on NHANES 2021–2023 | **Researcher, at D-019:** fix the ICI smoother to a cited specification (the implementation follows the decision; the R defaults are confirmed from the R documentation first). Position the contribution against CR-02: temporal validation on 2021–2023 is not a novelty for this outcome |
| R15 | NHANES design-based descriptive estimates (§10, Q-052). CDC/NCHS guidance (NHANES tutorial "Variance Estimation", read 2026-11-12): Taylor series linearisation, with-replacement PSUs within strata, and **subpopulation (domain) estimation using all records with non-zero weight plus a subpopulation indicator**. `survey.weighted_mean_taylor` had no domain option, so applying it to the analytic subsample alone could drop PSUs or fail on single-PSU strata | **Implemented 2026-11-12** (an optional `domain` argument; previous behaviour unchanged; tested). **Researcher, at D-019:** state that Table 2 and prevalence estimates use domain estimation over the full fasting-subsample file with the analytic sample as the domain. Q-052 (comparison with a reference implementation) stays open until A3 |

## 10. Assembled full text (2026-11-12)
`experimental_protocol_v1.0_candidate_full.md` is v0.1 revision 5 (SHA-256 `63d275d1…98ef7`, unchanged) with these 24 replacements applied by a script. Each replacement had to match exactly once, or the assembly stopped:
- H1–H2: title and status;
- C1–C6;
- §2 threshold wording (T);
- R2, R9 (ablation labels ABL-1 to ABL-5), R11, R12;
- Q3 and Q-054 marked **[DECISION PENDING]**;
- the A6 scope note at §19.

No content was removed except the replaced sentences and the superseded milestone table. That table is replaced by a pointer to the single critical-path schedule in the decision sheet. **This text is a candidate only.** At D-019 the researcher edits it, then the final text is hashed and recorded. The candidate's own hash (`df3d35e7…7668`) identifies this assembly, not a frozen version.

