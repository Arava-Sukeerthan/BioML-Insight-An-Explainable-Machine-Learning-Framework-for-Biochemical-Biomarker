"""Rule S synthetic verification of the BL-1..BL-6 / F2 harness (approval item A4). READY, NOT RUN.

GATED: every test is skipped unless BOTH
  * the environment variable RULE_S_AUTHORISATION names the decision-log ID that approves A4, and
  * the A3 packages (scikit-learn, xgboost) are installed.
It is deliberately NOT part of scripts/run_checks.sh, and nothing here runs today: no classifier has
been fitted in this repository. ALL DATA ARE SYNTHETIC (scripts/models/synthetic.py); results are
software verification only and are never reported as evidence of model performance.

Test plan (the A4 wording; criteria fixed before any run):
  (1) runs complete with exactly 40 configurations per method;
  (2) seed-identical reruns give identical results;
  (3) validation labels never change development results;
  (4) negative control: labels independent of features -> AUROC within 0.5 +/- 0.05 at n = 3,000.
Each method's wall-clock time is recorded, to check the experiment window. One summary entry per run
is appended to logs/SYNTHETIC_VERIFICATION_LOG.md (aggregate values only).

Run (after A3 and A4 are recorded):
  RULE_S_AUTHORISATION=D-nnn environment/.venv/bin/python -I -m unittest discover -s tests/synthetic_harness -v
"""
import datetime as dt
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "models"))
import harness as H  # noqa: E402
import metrics as M  # noqa: E402
import models as MD  # noqa: E402
from synthetic import synthetic_binary_task  # noqa: E402

AUTH = os.environ.get("RULE_S_AUTHORISATION", "").strip()
METHODS_REQUIRED = ("BL-1", "BL-2", "BL-3", "BL-4", "BL-5", "BL-6", "F2")
AVAILABLE = all(MD.availability()[m][0] for m in METHODS_REQUIRED)
METHODS = ("BL-1", "BL-2", "BL-3", "BL-4", "BL-5", "BL-6", "F2")
COLS = ["LBXTC", "LBDHDD", "BMXBMI", "LBXSATSI", "LBXSGTSI"]
LOG = REPO / "logs" / "SYNTHETIC_VERIFICATION_LOG.md"
CONFIG = json.loads((REPO / "scripts" / "models" / "experiment_config_draft.json").read_text(encoding="utf-8"))
RESULTS = {}


def frame(n, seed, signal=1.0):
    X, y, _ = synthetic_binary_task(n, seed, n_features=len(COLS), signal=signal)
    return pd.DataFrame(X, columns=COLS), y


def config(n_seeds=1):
    cfg = dict(CONFIG)
    cfg.update({"n_seeds": n_seeds, "columns": COLS})
    return cfg


@unittest.skipUnless(AUTH, "Rule S synthetic verification needs RULE_S_AUTHORISATION (approval item A4)")
@unittest.skipUnless(AVAILABLE, "A3 packages (scikit-learn, xgboost) are not installed")
class RuleSHarness(unittest.TestCase):
    def test_1_budget_and_runtime(self):
        X, y = frame(3000, 1)
        Xv, yv = frame(1500, 2)
        for m in METHODS:
            with self.subTest(method=m), tempfile.TemporaryDirectory() as d:
                t0 = time.time()
                rec = H.run_experiment(config(), m, X, y, "SYNTHETIC", d, validation=(Xv, yv))
                RESULTS.setdefault(m, {})["seconds_one_seed"] = round(time.time() - t0, 1)
                self.assertTrue(all(len(r["cv_log_loss"]) == 40 for r in rec["per_seed"]))

    def test_2_seed_reproducibility(self):
        X, y = frame(1500, 3)
        for m in METHODS:
            with self.subTest(method=m), tempfile.TemporaryDirectory() as d:
                a = H.run_experiment(config(), m, X, y, "SYNTHETIC", d)
                b = H.run_experiment(config(), m, X, y, "SYNTHETIC", d)
                self.assertEqual(a["per_seed"], b["per_seed"])

    def test_3_validation_isolation(self):
        X, y = frame(1500, 4)
        Xv, yv = frame(800, 5)
        for m in METHODS:
            with self.subTest(method=m), tempfile.TemporaryDirectory() as d:
                a = H.run_experiment(config(), m, X, y, "SYNTHETIC", d, validation=(Xv, yv))
                b = H.run_experiment(config(), m, X, y, "SYNTHETIC", d, validation=(Xv, 1 - yv))
                self.assertEqual(a["per_seed"], b["per_seed"])

    def test_4_negative_control(self):
        X, y = frame(3000, 6, signal=0.0)                     # labels independent of the features
        Xv, yv = frame(3000, 7, signal=0.0)
        for m in METHODS:
            with self.subTest(method=m), tempfile.TemporaryDirectory() as d:
                rec = H.run_experiment(config(), m, X, y, "SYNTHETIC", d, validation=(Xv, yv))
                auc = rec["temporal_validation"]["auroc"]
                RESULTS.setdefault(m, {})["null_auroc"] = round(auc, 4)
                self.assertLessEqual(abs(auc - 0.5), 0.05)

    @classmethod
    def tearDownClass(cls):
        if not RESULTS:
            return
        stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
        lines = [f"\n## Rule S harness run {stamp} (authorisation {AUTH}) — SYNTHETIC software verification, not evidence",
                 "| Method | Seconds (1 seed, n = 3,000) | Null-control AUROC |", "|---|---|---|"]
        lines += [f"| {m} | {RESULTS[m].get('seconds_one_seed', '—')} | {RESULTS[m].get('null_auroc', '—')} |"
                  for m in METHODS if m in RESULTS]
        with open(LOG, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    unittest.main()
