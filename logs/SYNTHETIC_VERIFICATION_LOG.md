# Synthetic Verification Log

Log of **synthetic-only software verification** under Rule S (`logs/DECISION_LOG.md`, D-040).
Created in GOV-D040-RULE-S (2026-10-24) as a header only.

**No synthetic verification has been run.** No test plan, test code or test environment exists.

## Scope and limits (summary of D-040; the decision log is authoritative)
- Checks only whether F-A software meets its stated specification: clinical-anchor offset handling
  throughout boosting, prediction consistency, validation offsets and early stopping, sample-weight
  handling, model persistence and reload, reproducibility, and attribution behaviour.
- Entirely artificial data from documented code with fixed, recorded seeds. NHANES and any other
  participant-level data, and values or parameters estimated from them, are prohibited.
- Entries here are **software verification, not experiments and not biomedical evidence**. They are
  never reported as evidence of biomedical validity, clinical utility, empirical model performance,
  superiority over baselines or methodological novelty. Empirical experiments are logged in
  `logs/EXPERIMENT_LOG.md`.
- Criteria, reference computations and negative controls are fixed in an approved test plan before
  execution and are not weakened after results are observed. Failures are kept.
- Each step needs separate researcher authorisation (test plan; test code and supporting files;
  environment specification; environment creation and package installation; each run). No run before
  2026-11-03. T10 (anchor-mismatch simulation) is outside Rule S.
- Generated model artifacts are stored in temporary directories outside the repository.
- D-040 status at creation: **APPROVED — CONDITIONAL (inactive)** until activation conditions K1–K4
  are satisfied; all existing restrictions remain in force until the exemption is active.

## Entry fields (one entry per authorised run)
Run ID · date · task/prompt ID · run authorisation (owner prompt reference) · Git commit of the test code ·
test-plan version · test IDs run · environment lock file path and hash · Python version and platform
(OS, glibc, CPU model and count) · package versions (installed inventory) · thread settings · random
seeds · command · result per test (pass/fail against the pre-specified criterion) · negative-control
outcomes · failures, errors and deviations from the plan · location of retained outputs (no model
artifacts in the repository) · researcher acceptance decision and date (acceptance does not approve
Q-048, D-017, D-019, the empirical protocol or any research claim).

## Entries

None.
