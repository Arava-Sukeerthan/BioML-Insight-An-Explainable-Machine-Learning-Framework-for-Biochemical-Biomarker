"""Tests for scripts/models: splits, equal tuning budget, in-fold preprocessing, model registry,
reproducibility helpers and the experiment harness.

ALL DATA ARE SYNTHETIC (scripts/models/synthetic.py; fixed seeds; arbitrary ranges). No NHANES data,
no network. The harness is exercised only with the NON-LEARNING FixedScoreStub, so no predictive
classifier is trained (classifier tests await authorisation under D-040, Rule S). Run logs go to
temporary directories.
"""
import hashlib
import json
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "models"))
import harness as H  # noqa: E402
import models as MD  # noqa: E402
import reproducibility as R  # noqa: E402
import splits as SP  # noqa: E402
import tuning as T  # noqa: E402
from preprocess import InFoldPreprocessor, PreprocessingError  # noqa: E402
from synthetic import synthetic_binary_task, synthetic_feature_frame  # noqa: E402

CONFIG = json.loads((REPO / "scripts" / "models" / "experiment_config_draft.json").read_text(encoding="utf-8"))


class Splits(unittest.TestCase):
    def test_stratified_split_disjoint_complete_and_proportional(self):
        y = np.array([1] * 650 + [0] * 350)
        tr, cal = SP.stratified_split(y, 0.2, seed=1)
        self.assertEqual(len(set(tr) | set(cal)), 1000)
        self.assertFalse(set(tr) & set(cal))
        self.assertAlmostEqual(y[cal].mean(), 0.65, delta=0.002)

    def test_deterministic_by_seed(self):
        y = np.array([1, 0] * 100)
        a, b = SP.stratified_split(y, 0.2, 5), SP.stratified_split(y, 0.2, 5)
        np.testing.assert_array_equal(a[1], b[1])
        self.assertFalse(np.array_equal(a[1], SP.stratified_split(y, 0.2, 6)[1]))

    def test_kfold_partition_and_balance(self):
        y = np.array([1] * 60 + [0] * 40)
        folds = SP.stratified_kfold(y, 5, seed=2)
        tested = np.concatenate([te for _, te in folds])
        self.assertEqual(sorted(tested.tolist()), list(range(100)))
        for _, te in folds:
            self.assertEqual(y[te].sum(), 12)

    def test_grouped_folds_keep_groups_together(self):
        groups = np.repeat(np.arange(12), 5)
        for tr, te in SP.grouped_kfold(groups, 4, seed=3):
            self.assertFalse(set(groups[tr]) & set(groups[te]))

    def test_seed_derivation(self):
        self.assertEqual(SP.derive_seeds(7, 5), SP.derive_seeds(7, 5))
        self.assertEqual(len(set(SP.derive_seeds(7, 5))), 5)

    def test_too_small_class_rejected(self):
        with self.assertRaises(ValueError):
            SP.stratified_kfold(np.array([1, 1, 1, 0]), 2, seed=0)


class Tuning(unittest.TestCase):
    def test_every_method_has_exactly_the_common_budget(self):
        self.assertEqual(T.check_equal_budget(CONFIG), 40)
        for name, mcfg in CONFIG["methods"].items():
            self.assertEqual(len(T.configurations_for(mcfg, 40, seed=1)), 40, name)

    def test_unequal_budget_rejected(self):
        bad = {"tuning_budget": 40, "methods": {"BL-1": {"grid": {"C": [1, 2], "l1_ratio": [0.5]}}}}
        with self.assertRaises(ValueError):
            T.check_equal_budget(bad)

    def test_sampling_reproducible_and_within_bounds(self):
        space = CONFIG["methods"]["BL-3"]["search_space"]
        a = T.sample_configurations(space, 40, seed=9)
        self.assertEqual(a, T.sample_configurations(space, 40, seed=9))
        self.assertNotEqual(a, T.sample_configurations(space, 40, seed=10))
        for c in a:
            self.assertTrue(0.01 <= c["learning_rate"] <= 0.3)
            self.assertTrue(2 <= c["max_depth"] <= 6)

    def test_invalid_space_and_selection(self):
        with self.assertRaises(ValueError):
            T.sample_configurations({"x": {"type": "loguniform", "low": 0, "high": 1}}, 3, 0)
        self.assertEqual(T.select_best([0.5, 0.3, 0.3, float("nan")]), 1)


class Preprocessing(unittest.TestCase):
    COLS = ["LBXSATSI", "TRIG", "LBXTC", "RIAGENDR", "BMXBMI"]

    def test_statistics_learnt_from_training_rows_only(self):
        tr = synthetic_feature_frame(200, 1, self.COLS, missing_rate=0.1)
        te = synthetic_feature_frame(50, 2, self.COLS, missing_rate=0.1) * 0 + 1e6   # extreme test rows
        te["RIAGENDR"] = 1.0
        pre = InFoldPreprocessor(self.COLS).fit(tr)
        fill_before = dict(pre.fill_)
        pre.transform(te)
        self.assertEqual(pre.fill_, fill_before)
        self.assertAlmostEqual(pre.fill_["LBXTC"], float(tr["LBXTC"].dropna().median()))

    def test_indicators_log_transform_and_sex_coding(self):
        tr = synthetic_feature_frame(400, 3, self.COLS, missing_rate=0.0)
        tr.loc[:39, "LBXTC"] = np.nan          # 10% missing -> indicator
        tr.loc[:7, "BMXBMI"] = np.nan          # 2% missing -> no indicator
        pre = InFoldPreprocessor(self.COLS).fit(tr)
        self.assertEqual(pre.indicators_, ["LBXTC"])
        Z = pre.transform(tr)
        self.assertEqual(Z.shape, (400, 6))
        self.assertTrue(np.isfinite(Z).all())
        np.testing.assert_allclose(Z[50, 1], np.log1p(tr.loc[50, "TRIG"]))
        self.assertTrue(set(np.unique(Z[:, 3])) <= {0.0, 1.0})

    def test_leakage_and_input_errors(self):
        with self.assertRaises(Exception):
            InFoldPreprocessor(["LBXGLU", "LBXTC"])                 # outcome variable as predictor
        pre = InFoldPreprocessor(self.COLS)
        with self.assertRaises(PreprocessingError):
            pre.transform(synthetic_feature_frame(5, 1, self.COLS))  # not fitted
        tr = synthetic_feature_frame(20, 1, self.COLS)
        with self.assertRaises(PreprocessingError):
            pre.fit(tr.drop(columns="TRIG"))
        neg = tr.copy()
        neg.loc[0, "TRIG"] = -5
        with self.assertRaises(PreprocessingError):
            pre.fit(neg)
        bad_sex = tr.copy()
        bad_sex.loc[0, "RIAGENDR"] = 3
        with self.assertRaises(PreprocessingError):
            pre.fit(bad_sex)

    def test_scaling_uses_training_mean_and_sd(self):
        tr = synthetic_feature_frame(300, 4, self.COLS, missing_rate=0.0)
        Z = InFoldPreprocessor(self.COLS, scale=True).fit_transform(tr)
        np.testing.assert_allclose(Z[:, :5].mean(axis=0), 0, atol=1e-9)


class Registry(unittest.TestCase):
    def test_registry_covers_documented_models_and_reports_missing_packages(self):
        self.assertEqual(set(MD.REGISTRY), {"BL-1", "BL-2", "BL-3", "BL-4", "BL-5", "BL-6", "F2"})
        for name, (ok, missing) in MD.availability().items():
            if not ok:
                with self.assertRaisesRegex(RuntimeError, "not installed"):
                    MD.build_model(name, {}, 0)

    def test_stub_learns_nothing(self):
        X = np.array([[0.0], [1.0]])
        stub = MD.FixedScoreStub(coef=2.0)
        before = stub.predict_proba(X)
        stub.fit(X, np.array([1, 0]))
        np.testing.assert_array_equal(before, stub.predict_proba(X))


def stub_config(columns):
    cfg = {k: v for k, v in CONFIG.items() if k != "methods"}
    cfg.update({"n_seeds": 2, "tuning_budget": 40, "columns": columns,
                "methods": {"STUB": {"search_space": {"coef": {"type": "uniform", "low": -2, "high": 2},
                                                      "bias": {"type": "uniform", "low": -1, "high": 1},
                                                      "column": {"type": "fixed", "value": 0}}}}})
    return cfg


class Harness(unittest.TestCase):
    def data(self, n=600, seed=11):
        X, y, _ = synthetic_binary_task(n, seed, n_features=3)
        cols = ["LBXTC", "LBDHDD", "BMXBMI"]
        return pd.DataFrame(X, columns=cols), y, cols

    def test_end_to_end_synthetic_run_and_log_record(self):
        X, y, cols = self.data()
        Xv, yv, _ = self.data(300, 12)
        with tempfile.TemporaryDirectory() as d:
            rec = H.run_experiment(stub_config(cols), "STUB", X, y, "SYNTHETIC", d, validation=(Xv, yv))
            lines = (Path(d) / "runs.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(len(rec["per_seed"]), 2)
        for r in rec["per_seed"]:
            self.assertEqual(len(r["cv_log_loss"]), 40)                       # equal budget used
            self.assertEqual(r["n_train"] + r["n_cal"], 600)
            self.assertIsInstance(r["calibrator_order_preserving"], bool)    # Platt slope sign recorded
        tv = rec["temporal_validation"]
        for k in ("auroc", "brier", "slope", "ici", "coverage_class_0", "coverage_class_1", "mean_set_size"):
            self.assertIn(k, tv)
        self.assertEqual(rec["config_hash"], R.config_hash(stub_config(cols)))

    def test_threshold_only_used_on_its_own_probability_scale(self):
        # the threshold is fixed on calibrated D-cal probabilities; it must not be applied to the
        # uncalibrated out-of-fold predictions used for internal validation
        X, y, cols = self.data()
        Xv, yv, _ = self.data(300, 12)
        with tempfile.TemporaryDirectory() as d:
            rec = H.run_experiment(stub_config(cols), "STUB", X, y, "SYNTHETIC", d, validation=(Xv, yv))
        for r in rec["per_seed"]:
            self.assertNotIn("sensitivity", r["internal_oof"])
            self.assertNotIn("threshold", r["internal_oof"])
        self.assertNotIn("sensitivity", rec["internal_summary"])
        self.assertIn("sensitivity", rec["temporal_validation"])
        self.assertIn("threshold", rec["temporal_validation"])
        # the calibrated internal estimate is on the threshold's scale, so M7-M9 are reported there
        for k in ("sensitivity", "threshold", "coverage_class_1", "ici"):
            self.assertIn(k, rec["internal_calibrated_summary"])
        for r in rec["per_seed"]:                         # increasing Platt fit: AUROC is unchanged
            self.assertTrue(r["calibrator_order_preserving"])
            self.assertAlmostEqual(r["internal_oof"]["auroc"], r["internal_oof_calibrated"]["auroc"])

    def test_summary_over_seeds_handles_missing_and_nonfinite(self):
        s = H._summarise([{"a": 1.0, "b": float("nan")}, {"a": 3.0, "b": 2.0}, {"a": 2.0}])
        self.assertAlmostEqual(s["a"]["mean"], 2.0)
        self.assertAlmostEqual(s["a"]["sd"], 1.0)
        self.assertEqual((s["a"]["n"], s["a"]["n_missing"]), (3, 0))
        self.assertEqual((s["b"]["n"], s["b"]["n_missing"], s["b"]["mean"]), (1, 2, 2.0))
        empty = H._summarise([{"c": float("nan")}])
        self.assertIsNone(empty["c"]["mean"])

    def test_validation_data_never_influence_development_results(self):
        X, y, cols = self.data()
        Xv, yv, _ = self.data(300, 12)
        with tempfile.TemporaryDirectory() as d:
            a = H.run_experiment(stub_config(cols), "STUB", X, y, "SYNTHETIC", d, validation=(Xv, yv))
            b = H.run_experiment(stub_config(cols), "STUB", X, y, "SYNTHETIC", d, validation=(Xv, 1 - yv))
        self.assertEqual(a["per_seed"], b["per_seed"])
        self.assertNotEqual(a["temporal_validation"]["auroc"], b["temporal_validation"]["auroc"])

    def test_reproducible_given_seed(self):
        X, y, cols = self.data()
        with tempfile.TemporaryDirectory() as d:
            a = H.run_experiment(stub_config(cols), "STUB", X, y, "SYNTHETIC", d)
            b = H.run_experiment(stub_config(cols), "STUB", X, y, "SYNTHETIC", d)
        self.assertEqual(a["per_seed"], b["per_seed"])
        self.assertEqual(a["data_fingerprint"], b["data_fingerprint"])

    def test_real_data_guard(self):
        X, y, cols = self.data(200)
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(H.HarnessError):
                H.run_experiment(stub_config(cols), "STUB", X, y, "REAL", d)
            with self.assertRaises(H.HarnessError):
                H.run_experiment(stub_config(cols), "STUB", X, y, "REAL", d, authorisation="D-999")  # draft protocol
            with self.assertRaises(H.HarnessError):
                H.run_experiment(stub_config(cols), "STUB", X, y, "UNLABELLED", d)
            self.assertFalse((Path(d) / "runs.jsonl").exists())

    def test_real_data_guard_binds_protocol_hash_and_clean_tree(self):
        # _guard only (never a REAL-labelled run on synthetic data)
        with tempfile.TemporaryDirectory() as d:
            proto = Path(d) / "protocol_v1.0.md"
            proto.write_bytes(b"synthetic frozen protocol text")
            digest = hashlib.sha256(proto.read_bytes()).hexdigest()
            cfg = {"protocol_version": "1.0", "protocol_path": str(proto), "protocol_sha256": digest}
            clean = {"commit": "a" * 40, "dirty": False}
            with mock.patch.object(H, "git_commit", return_value=clean):
                H._guard(cfg, "REAL", "D-999")                                     # accepted
                for bad in ({"protocol_sha256": "0" * 64}, {"protocol_path": None},
                            {"protocol_sha256": "abc"}, {"protocol_version": "1.0-draft"}):
                    with self.assertRaises(H.HarnessError):
                        H._guard({**cfg, **bad}, "REAL", "D-999")
            for g in ({"commit": "a" * 40, "dirty": True}, {"commit": "unknown", "dirty": None}):
                with mock.patch.object(H, "git_commit", return_value=g):
                    with self.assertRaisesRegex(H.HarnessError, "clean, committed"):
                        H._guard(cfg, "REAL", "D-999")
            H._guard({}, "SYNTHETIC", None)                                       # synthetic unaffected

    def test_validation_fingerprint_recorded(self):
        X, y, cols = self.data()
        Xv, yv, _ = self.data(300, 12)
        with tempfile.TemporaryDirectory() as d:
            rec = H.run_experiment(stub_config(cols), "STUB", X, y, "SYNTHETIC", d, validation=(Xv, yv))
        self.assertEqual(rec["validation_fingerprint"], R.data_fingerprint(Xv.to_numpy(dtype=float), yv))
        self.assertNotEqual(rec["validation_fingerprint"], rec["data_fingerprint"])

    def test_column_mismatch_rejected(self):
        X, y, cols = self.data(200)
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(H.HarnessError):
                H.run_experiment(stub_config(cols[::-1]), "STUB", X, y, "SYNTHETIC", d)


class Reproducibility(unittest.TestCase):
    def test_hashes_and_environment_record(self):
        self.assertEqual(R.config_hash({"a": 1, "b": [2]}), R.config_hash({"b": [2], "a": 1}))
        X = np.arange(6).reshape(3, 2)
        self.assertNotEqual(R.data_fingerprint(X, [0, 1, 0]), R.data_fingerprint(X, [0, 1, 1]))
        env = R.environment_record()
        self.assertIn("python", env)
        self.assertIn("numpy", env["packages"])

    def test_set_deterministic_records_threads(self):
        info = R.set_deterministic(123, threads=1)
        self.assertEqual(info["threads"], 1)


if __name__ == "__main__":
    unittest.main()
