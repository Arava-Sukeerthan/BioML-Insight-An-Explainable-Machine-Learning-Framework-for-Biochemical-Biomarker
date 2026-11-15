# scripts/models: experiment scaffolding (draft protocol sections 9-16)

**Status (2026-11-12): software scaffolding, tested on SYNTHETIC data only. No real data, no trained
classifier, no results.** The experimental protocol is a draft (D-019 PENDING); module defaults follow
`research/methodology/experimental_protocol_v0.1_draft.md` revision 5 and
`experiment_config_draft.json` (assistant proposal for the freeze).

| Module | Protocol | Content |
|---|---|---|
| `splits.py` | §12 | Seeded stratified D-train/D-cal split, stratified K-fold, grouped K-fold (S-13), seed derivation; validated by `scripts/nhanes/safeguards.py` |
| `preprocess.py` | §9 (F1) | In-fold leakage check, log(x+1), sex coding, >5% missingness indicators, median/mode imputation, optional scaling |
| `tuning.py` | §12.2 | Equal budget (40) for every method; seeded sampling; grid size check; selection by CV log loss |
| `calibration.py` | §11.2 F3, S-14 | Platt and isotonic (PAV) calibration |
| `conformal.py` | §11.2 F4 | Class-conditional split conformal sets, alpha = 0.10 |
| `metrics.py` | §14 M1-M10 | AUROC, AUPRC, Brier/scaled Brier, calibration intercept and slope, ICI, ECE, sensitivity/specificity, threshold rule, conformal coverage and efficiency, net benefit; optional weights |
| `stats.py` | §10, §15 | Bootstrap CIs, paired bootstrap, PSU-within-stratum bootstrap, Holm |
| `models.py` | §11 | Interfaces for BL-1 to BL-6 and F2 (packages not installed); non-learning `FixedScoreStub` for plumbing tests |
| `harness.py` | §12-§16 | Seeds -> split -> equal-budget CV tuning -> OOF internal metrics (raw; and calibrated, on the threshold scale) -> refit -> F3/F4/threshold on D-cal (records whether the Platt fit preserves score order) -> frozen model applied once to validation; JSONL run records; real-data guard |
| `reproducibility.py` | §22 | Deterministic settings, config/data hashes, environment and Git records |
| `synthetic.py` | — | Synthetic generators (arbitrary values; IDs from 9,000,001) |

Not yet implemented: F5 TreeSHAP explanation stability (needs `shap`, `xgboost`); classifier
training tests (need D-002 install and a D-040 Rule S authorisation).

Tests: `python3 -I -B -m unittest discover -s tests/models` and `tests/nhanes` (dataset assembly).
