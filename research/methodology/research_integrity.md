# Research Integrity Protocol

| Field | Value |
|---|---|
| Task | BIO-001 (2026-10-23) |
| Version | 1.0 — **DRAFT, pending researcher approval** |
| Applies to | All empirical work (Stages F–J) and every claim made in the manuscript |
| Related | `CLAUDE.md`, `GOVERNANCE.md` §1–§2, `logs/EXPERIMENT_LOG.md`, `logs/DECISION_LOG.md` (D-014, D-015, D-018, D-019) |

This protocol turns the principles in `GOVERNANCE.md` into concrete requirements. Requirements
marked **must** are mandatory. Implementation details (exact file names, tools) are
`[RECOMMENDATION]` and will be fixed in the experimental protocol (D-019). No dataset or experiment
exists yet. Nothing in this document reports a result.

---

## 1. Genuine, documented datasets
- Empirical evaluation **must** use genuine datasets with documented origin: a public repository record, a publication describing the cohort, or a data-use agreement.
- Synthetic or simulated data **must not** appear in any results table, figure or claim about biomedical performance. They are allowed only (a) as clearly labelled fixtures in `tests/` or (b) in a separate, labelled simulation study whose results are reported apart from the real-data results.
- A dataset whose provenance cannot be documented is not used.

## 2. Dataset provenance and access conditions
For every dataset, a provenance record (planned: `data/PROVENANCE.md` plus a machine-readable entry) **must** list:
- name, version or release, source URL or accession, and the citing publication (verified per `research_plan.md` §6);
- access route and date, who accessed it, licence/terms of use, and any restrictions on redistribution (the repository is **public**: restricted data are never committed);
- ethics/consent statement as documented by the data provider;
- population, setting, collection period, inclusion criteria and outcome/label definition, as documented by the provider;
- the SHA-256 checksum of every original file.

## 3. Preservation of original data and documented preprocessing
- Original files are kept unchanged in `data/raw/` (git-ignored). Checksums are committed.
- All transformations are done by versioned scripts that read raw files and write new files (`data/interim/`, `data/processed/`). There is no manual editing of data files.
- Every exclusion of observations or variables is recorded with its count and reason. Valid observations are not removed to improve results. Outlier handling rules are fixed in the protocol before modelling.
- Labels are taken from the documented outcome definition (approved under D-014/D-019) and are never relabelled to improve results.

## 4. Data-leakage prevention
- The unit of independence (e.g., participant, not sample or visit) is identified. All records from one unit are kept in the same partition.
- The hold-out/test partition is defined before any modelling and is not used for model selection, tuning, threshold choice, calibration fitting or feature selection.
- Information that would not be available at prediction time (post-diagnosis measurements, treatment variables, the outcome itself or proxies of it) is excluded. The check is documented per variable.
- Duplicate or near-duplicate records across partitions are checked.
- Batch/site/run-order structure is recorded. If it is confounded with the label, this is reported as a limitation, and it is not silently corrected using test data.

## 5. Preprocessing and feature selection inside training partitions
- Imputation, scaling, normalisation, batch correction, resampling for class imbalance, feature/biomarker selection, hyperparameter tuning and calibration-model fitting **must** be fitted on the training part of each split only. They are then applied unchanged to the corresponding validation/test part. In practice this means one pipeline object evaluated inside the resampling loop.
- With cross-validation, selection and tuning are nested (inner loop) so that the outer-loop estimate is not optimistically biased.
- Calibration maps and conformal/uncertainty calibration sets come from data disjoint from the data used to evaluate them.
- An automated test is planned that fails when a fitted transformer has seen test-partition indices (`[RECOMMENDATION]`).

## 6. Recording experiment configurations and outputs
Each run is logged in `logs/EXPERIMENT_LOG.md` with: run ID, date, task ID, Git commit, dataset version and checksum, protocol version, full configuration, random seeds, the exact command, an environment lock file, and the outputs path.
- Metrics are written to files by the code. Results tables are generated from those files, never typed by hand.
- **Every** run that informs a decision is kept, including failed and discarded runs, with the reason it was discarded. Selective reporting of the best run is not allowed.
- Seeds are fixed in advance. Variation over seeds/resamples is reported rather than picking a favourable seed.

## 7. Honest reporting of negative and inconclusive findings
- If the proposed method does not outperform the baselines, or differences are within statistical uncertainty, this is reported as such.
- Hypotheses are stated before testing (`[HYPOTHESIS]`) and are not rewritten after results are seen. Post-hoc analyses are labelled exploratory.
- Baselines receive the same data, preprocessing, tuning budget and evaluation as the proposed method (D-018).

## 8. Appropriate statistical comparison
- Point estimates are reported with uncertainty, for example confidence intervals from bootstrap or repeated resampling, as fixed in the protocol.
- Model comparisons use tests or intervals suited to the design: paired comparisons on the same splits, and corrected resampled tests where cross-validation folds overlap. The exact methods are chosen and justified in D-019 from verified methodological sources.
- Discrimination is not the only criterion. Calibration (e.g., calibration intercept/slope, reliability diagrams, Brier score) and uncertainty quality (e.g., coverage and set size of uncertainty estimates) are evaluated as separate outcomes, as specified in the protocol.
- Multiple comparisons are acknowledged and handled as specified in the protocol. Sample size and events per class are reported, and their limitations are discussed.

## 9. Traceability
Each number, table and figure in the manuscript **must** be traceable along the chain
`manuscript claim → table/figure → generating script + commit → output file → run ID → dataset checksum`.
A planned claims register (`manuscript/claims_register.csv`, `[RECOMMENDATION]`) lists each
quantitative or literature claim with its source. Literature claims cite only `verified`
inventory records (`research_plan.md` §6).

## 10. Exploratory analysis versus final evaluation
- Exploratory analysis (data inspection, pilot models on training data only, method development) is labelled exploratory. It is kept separate from the final evaluation and must not touch the final test partition.
- The final evaluation runs **once** under the frozen protocol (D-019). Any re-run after protocol changes is logged as a protocol revision, with the earlier result kept.

## 11. External validation claims
- "External" or "independent" validation is claimed **only** when the model, with all preprocessing, selection and calibration, was frozen on the development data and then evaluated on a genuinely separate dataset (different cohort, site or period) that was not used in any development step (D-015).
- A random split, cross-validation, or a split of one pooled dataset is reported as **internal** validation.
- If no independent dataset is feasible, the manuscript says so explicitly and limits its generalisation claims accordingly.

## 12. No clinical-validity claims from classification metrics
- Good discrimination or calibration on retrospective research datasets does **not** show clinical validity, clinical utility or readiness for deployment.
- Explanations (e.g., feature attributions) describe the model. They are not evidence of biological causation, and are reported as such.
- Any statement about clinical relevance is framed as a hypothesis requiring prospective evaluation, unless such evidence actually exists and is cited from verified sources.

## 13. Compliance checks
Before any results are reported (Stage I) and before submission (Stage J), the assistant prepares and the researcher reviews a checklist covering §1–§12, with evidence for each item (file paths, commits, test outputs). Items that are not met are reported as limitations. They are not hidden.

## Change history
| Version | Date | Change | Approved |
|---|---|---|---|
| 1.0 | 2026-10-23 | Initial draft (BIO-001) | Pending |
