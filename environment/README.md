# Environment (D-002: PROPOSED)

Status on 2026-11-12: **not approved, nothing installed.** `requirements-proposed.txt` lists the
proposed pins. Present in the container: Python 3.13.17, numpy 2.5.3, pandas 3.0.5. Missing: scipy,
scikit-learn, xgboost, shap, statsmodels, matplotlib.

## After authorisation (not yet done)
1. `python3 -m venv .venv && . .venv/bin/activate` (the venv is git-ignored; do not commit it).
2. `pip install -r environment/requirements-proposed.txt`
3. Run every suite (`sh scripts/run_checks.sh`).
4. Freeze: `pip freeze > environment/requirements.lock`, then add `--hash` entries
   (`pip download -r environment/requirements.lock -d /tmp/wheels` and `pip hash`) and commit the lock.

## Deterministic execution (implemented in `scripts/models/reproducibility.py`)
- All randomness comes from numpy Generators seeded from `master_seed` in the configuration
  (`splits.derive_seeds`); learners get `random_state` from the same seeds.
- `set_deterministic()` sets OMP/OPENBLAS/MKL/NUMEXPR threads to 1 before learners are imported.
- Every run record stores the configuration hash, seeds, data fingerprint, Git commit and dirty flag,
  Python and package versions, and thread settings.
- Reproducibility check (Stage J): rerun from the lock file must reproduce the logged results exactly
  (synthetic version tested in `tests/models/test_pipeline_scaffolding.py`).

## Resolution check (2026-11-12; nothing installed)
`pip install --dry-run --ignore-installed --only-binary=:all: -r <pins>` resolved all eight pins without conflict for CPython 3.13 on Linux x86_64. Imports and runtime behaviour are **not** tested.

Findings, reported without changing any pin (decision: A3 and Q-048):
1. **Pre-release dependency.** `formulaic` (via statsmodels) requires `wrapt>=1.17.0rc1` on Python 3.13, so pip selects the pre-release `wrapt 2.6.0.dev1`. Proposed: pin `wrapt==2.5.2` (latest final) in the lock file.
2. **Unneeded GPU library.** `xgboost==3.4.1` pulls in `nvidia-nccl-cu13` (206.6 MB), a GPU library unused on this CPU-only machine. Alternatives: `xgboost-cpu==3.4.1`, or scikit-learn histogram gradient boosting.
