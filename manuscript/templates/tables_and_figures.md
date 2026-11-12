# Table and figure templates (shells only)

> **Templates, 2026-11-12. Every cell is empty ("·").** No value may be typed in by hand. Each table is filled by its named generator from logged run records or validated screening records, and the generator states the data label. SYNTHETIC output never fills a manuscript table: `report.results_table` refuses mixed labels and marks synthetic tables as "not evidence".
>
> Aggregate eligibility counts already recorded on 2026-10-24 (protocol v0.1 §4) may be shown in Table 2 only after the build reproduces them from the authorised download (AB-12).

## Literature review

**Figure 1. Screening flow.**
- **Generator:** `scripts/literature/flow_diagram.py` (Markdown table + Mermaid), run on validated `screening/decisions.csv` only. It currently refuses, because no screening exists.
- **Boxes:** source records identified → after deduplication → in scope (D-044) → Stage-0 exclusions by code → title/abstract screened → excluded by code → sought for full text → abstract only → full-text excluded by code → included.

**Table 1. Characteristics of included studies.** One row per included study; the counts come from the extraction file.

| Study (verified citation) | Disorder | Biomarker class | Model family | n | Validation design | Explainability | Calibration | Uncertainty |
|---|---|---|---|---|---|---|---|---|
| · | · | · | · | · | · | · | · | · |

The citation column takes `verified` records only (D-064; Q-098, Q-099).

## Prediction study

**Table 2. Participant characteristics by period.**

| Characteristic | 2017–Mar 2020: n (unweighted) | 2017–Mar 2020: weighted % / mean (SE) | 2021–2023: n (unweighted) | 2021–2023: weighted % / mean (SE) | SMD |
|---|---|---|---|---|---|
| · | · | · | · | · | · |

- **Generators:** `survey.weighted_mean_taylor` and `survey.shift_diagnostics`.

**Table 3. Q1 — value of biochemistry** (framework and BL-1).

| Model | Contrast | Internal ΔAUROC (mean ± SD over seeds) | Temporal ΔAUROC (95% CI) |
|---|---|---|---|
| · | B − C | · | · |
| · | A − C | · | · |

**Table 4. Q2 — framework vs calibrated baselines (group B).**

| Comparator | ΔICI (95% CI) | Holm p | ΔBrier (95% CI) | Holm p | ΔAUROC (95% CI) [Q-054] |
|---|---|---|---|---|---|
| · | · | · | · | · | · |

- **Generator:** `compare.compare_to_reference`, applied to `p_calibrated` (internal) and to the temporal-validation predictions.

**Table 5. Q3 — temporal transfer, per model.**

| Model | Metric | Internal reference [Q-100] | Temporal (95% CI) | Change |
|---|---|---|---|---|
| · | · | · | · | · |

- **Generator:** `report.results_table(internal=…)`. The internal estimate used is printed with the table.

**Table 6. Uncertainty and threshold metrics at temporal validation.**

| Model | Coverage y = 0 | Coverage y = 1 | Mean set size | Threshold (from D-cal) | Sensitivity | Specificity |
|---|---|---|---|---|---|---|
| · | · | · | · | · | · | · |

**Supplementary tables:**
- S1: all metrics per seed;
- S2: sensitivity analyses (kept set, A6);
- S3: ablations ABL-1 and ABL-2;
- S4: subgroup calibration (race/ethnicity, income), with small-cell protection;
- S5: deviations from the protocol.

## Figures (data generators exist; plotting needs the A3 installation of matplotlib)

| Figure | Content | Data source |
|---|---|---|
| 2 | Calibration curves, internal (b) and temporal, framework vs best calibrated baseline, Wilson 95% intervals | `report.calibration_curve` → `report.write_csv(min_cell=…)` |
| 3 | Class-conditional conformal coverage and set-size distribution, internal vs temporal | `metrics.conformal_summary` |
| 4 | SHAP global importance with rank stability (bootstrap refits; between periods) | `explain.global_importance`, `explain.rank_stability` |
| 5 | Decision curve (only if M10 is kept and its range is justified, Q-054) | `metrics.net_benefit` |
