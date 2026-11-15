"""Tests for scripts/models/explain.py, survey.py, compare.py and the harness prediction output.

ALL DATA ARE SYNTHETIC (hand-written values or seeded numpy draws). No NHANES data, no network, no
classifier trained (the harness uses the non-learning FixedScoreStub).
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "models"))
import compare as C  # noqa: E402
import metrics as M  # noqa: E402
import explain as E  # noqa: E402
import harness as H  # noqa: E402
import survey as SV  # noqa: E402
from synthetic import synthetic_binary_task  # noqa: E402

CONFIG = json.loads((REPO / "scripts" / "models" / "experiment_config_draft.json").read_text(encoding="utf-8"))


class Explain(unittest.TestCase):
    def test_spearman_known_values_and_ties(self):
        self.assertAlmostEqual(E.spearman([1, 2, 3, 4], [10, 20, 30, 40]), 1.0)
        self.assertAlmostEqual(E.spearman([1, 2, 3, 4], [4, 3, 2, 1]), -1.0)
        self.assertAlmostEqual(E.spearman([1, 2, 2, 3], [1, 2, 3, 4]), np.corrcoef([1, 2.5, 2.5, 4], [1, 2, 3, 4])[0, 1])
        with self.assertRaises(ValueError):
            E.spearman([1, 1, 1], [1, 2, 3])

    def test_importance_stability_and_overlap(self):
        base = np.array([5.0, 4, 3, 2, 1])
        self.assertAlmostEqual(E.rank_stability(np.vstack([base, base * 2, base + 1]))["mean_spearman"], 1.0)
        rng = np.random.default_rng(1)
        noisy = np.vstack([base + rng.normal(0, 3, 5) for _ in range(20)])
        self.assertLess(E.rank_stability(noisy)["mean_spearman"], 1.0)
        self.assertEqual(E.top_k_overlap(base, base[::-1], 2), 0.0)
        np.testing.assert_allclose(E.global_importance([[1, -2], [-3, 4]]), [2, 3])

    def test_direction_and_sign_agreement(self):
        X = np.array([[1.0, 1], [2, 1], [3, 1]])
        A = np.array([[-1.0, 0], [0, 0], [1, 0]])
        np.testing.assert_array_equal(E.mean_direction(A, X), [1, 0])
        self.assertEqual(E.sign_agreement([1, -1, 1], [0.5, -0.2, -0.1]), 2 / 3)


class Survey(unittest.TestCase):
    def test_estimate_and_se_hand_computed(self):
        x = np.array([1.0, 0, 1, 1])
        w = np.ones(4)
        strata = np.array([1, 1, 1, 1])
        psu = np.array([1, 1, 2, 2])
        r = SV.weighted_mean_taylor(x, w, strata, psu)
        self.assertAlmostEqual(r["estimate"], 0.75)
        # z = (x - 0.75)/4 -> PSU totals: (0.25-0.75)/4 = -0.125 ; (0.25+0.25)/4 = 0.125
        # var = 2/1 * (0.125^2 + 0.125^2) = 0.0625 -> se = 0.25
        self.assertAlmostEqual(r["se"], 0.25)

    def test_single_psu_stratum_refused(self):
        with self.assertRaises(ValueError):
            SV.weighted_mean_taylor([1, 0], [1, 1], [1, 1], [1, 1])

    def test_domain_estimation_uses_all_psus(self):
        rng = np.random.default_rng(8)
        n = 400
        strata = np.repeat([1, 2, 3, 4], 100)
        psu = np.tile(np.repeat([1, 2], 50), 4)
        w = rng.uniform(0.5, 2.0, n)
        x = rng.normal(5, 1, n)
        dom = rng.random(n) < 0.4
        r = SV.weighted_mean_taylor(np.where(dom, x, np.nan), w, strata, psu, domain=dom)
        self.assertAlmostEqual(r["estimate"], float(np.average(x[dom], weights=w[dom])))
        # domain=all-ones reproduces the previous (whole-input) behaviour exactly
        full = SV.weighted_mean_taylor(x, w, strata, psu)
        self.assertEqual(SV.weighted_mean_taylor(x, w, strata, psu, domain=np.ones(n)), full)
        # a stratum whose domain members sit in one PSU is still estimable (the other PSU has weight)
        dom2 = dom.copy()
        dom2[(strata == 1) & (psu == 2)] = False
        self.assertTrue(np.isfinite(SV.weighted_mean_taylor(np.where(dom2, x, np.nan), w, strata, psu, domain=dom2)["se"]))
        with self.assertRaises(ValueError):          # subsetting first would lose that PSU and fail
            SV.weighted_mean_taylor(x[dom2 & (strata == 1)], w[dom2 & (strata == 1)],
                                    strata[dom2 & (strata == 1)], psu[dom2 & (strata == 1)])

    def test_smd_and_shift_diagnostics(self):
        self.assertAlmostEqual(SV.standardised_mean_difference([0, 2], [2, 4]), 2 / np.sqrt(2))
        d = SV.shift_diagnostics(pd.DataFrame({"a": [0, 2]}), pd.DataFrame({"a": [2, 4]}), [1, 0], [1, 1])
        self.assertAlmostEqual(d["prevalence_difference"], 0.5)
        self.assertIn("a", d["smd"])


class Compare(unittest.TestCase):
    def test_reference_vs_identical_and_better_model(self):
        rng = np.random.default_rng(2)
        y = rng.integers(0, 2, 400)
        ref = rng.random(400)
        better = np.clip(0.7 * y + 0.3 * ref, 0, 1)
        out = C.compare_to_reference(y, {"ref": ref, "same": ref.copy(), "better": better}, "ref",
                                     metric_names=("auroc", "brier"), n_boot=300, seed=1)
        self.assertEqual(out["auroc"]["same"]["difference"], 0.0)
        self.assertGreater(out["auroc"]["better"]["low"], 0.0)
        self.assertLess(out["brier"]["better"]["high"], 0.0)
        for row in out["auroc"].values():
            self.assertGreaterEqual(row["p_holm"], row["p_value"])

    def test_input_errors_and_margin(self):
        with self.assertRaises(ValueError):
            C.compare_to_reference([0, 1], {"a": [0.1, 0.9]}, "b")
        with self.assertRaises(ValueError):
            C.compare_to_reference([0, 1], {"a": [0.1, 0.9], "b": [0.5]}, "a")
        self.assertTrue(C.non_inferior(-0.01, 0.02))
        self.assertFalse(C.non_inferior(-0.03, 0.02))
        with self.assertRaises(ValueError):
            C.non_inferior(0.0, 0)


class HarnessPredictions(unittest.TestCase):
    def test_predictions_returned_but_not_logged(self):
        X, y, _ = synthetic_binary_task(400, 21, n_features=2)
        Xv, yv, _ = synthetic_binary_task(200, 22, n_features=2)
        cols = ["LBXTC", "LBDHDD"]
        cfg = {k: v for k, v in CONFIG.items() if k != "methods"}
        cfg.update({"n_seeds": 1, "columns": cols, "methods": {"STUB": {"search_space": {
            "coef": {"type": "uniform", "low": -2, "high": 2}, "bias": {"type": "fixed", "value": 0.0},
            "column": {"type": "fixed", "value": 0}}}}})
        with tempfile.TemporaryDirectory() as d:
            rec, preds = H.run_experiment(cfg, "STUB", pd.DataFrame(X, columns=cols), y, "SYNTHETIC", d,
                                          validation=(pd.DataFrame(Xv, columns=cols), yv), return_predictions=True)
            logged = (Path(d) / "runs.jsonl").read_text(encoding="utf-8")
        self.assertEqual(preds["validation"].shape, (200,))
        self.assertEqual(preds["oof_primary"]["p_raw"].shape, (rec["per_seed"][0]["n_train"],))
        self.assertEqual(preds["oof_primary"]["p_calibrated"].shape, (rec["per_seed"][0]["n_train"],))
        # the returned calibrated OOF predictions are the ones summarised in the calibrated internal estimate
        y_tr = np.asarray(y)[preds["oof_primary"]["index"]]
        self.assertAlmostEqual(M.brier(y_tr, preds["oof_primary"]["p_calibrated"]),
                               rec["per_seed"][0]["internal_oof_calibrated"]["brier"])
        self.assertAlmostEqual(M.brier(y_tr, preds["oof_primary"]["p_raw"]), rec["per_seed"][0]["internal_oof"]["brier"])
        self.assertNotIn('"_oof"', logged)
        self.assertNotIn('"p":', logged)


if __name__ == "__main__":
    unittest.main()
