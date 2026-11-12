"""Tests for scripts/models: metrics, calibration maps, conformal sets, resampling statistics.

ALL DATA ARE SYNTHETIC (hand-written vectors or numpy draws with fixed seeds). No NHANES data, no
file access, no network. No predictive classifier is trained: the routines tested are evaluation
formulas and post-hoc maps with at most two parameters.

Run: python3 -I -B -m unittest discover -s tests/models -v
"""
import sys
import unittest
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "models"))
import metrics as M  # noqa: E402
import stats as S  # noqa: E402
from calibration import IsotonicCalibrator, PlattCalibrator, pava  # noqa: E402
from conformal import MondrianConformal  # noqa: E402
from glm import fit_logistic, sigmoid  # noqa: E402


class Metrics(unittest.TestCase):
    def test_auroc_textbook_and_ties(self):
        self.assertAlmostEqual(M.auroc([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8]), 0.75)
        self.assertAlmostEqual(M.auroc([0, 1], [0.5, 0.5]), 0.5)
        self.assertAlmostEqual(M.auroc([0, 0, 1, 1], [0.1, 0.2, 0.3, 0.4]), 1.0)

    def test_auroc_weights_equal_duplication(self):
        y, p = [0, 1, 0, 1, 1], [0.2, 0.3, 0.6, 0.7, 0.1]
        dup_y = [0, 1, 1, 0, 1, 1, 1]
        dup_p = [0.2, 0.3, 0.3, 0.6, 0.7, 0.1, 0.1]
        self.assertAlmostEqual(M.auroc(y, p, w=[1, 2, 1, 1, 2]), M.auroc(dup_y, dup_p))

    def test_auprc_hand_computed(self):
        # ranks: 0.9(1) 0.8(0) 0.7(1) 0.6(0); AP = 0.5*1 + 0.5*(2/3)
        self.assertAlmostEqual(M.auprc([1, 0, 1, 0], [0.9, 0.8, 0.7, 0.6]), 0.5 + 1 / 3)

    def test_brier_and_scaled(self):
        self.assertAlmostEqual(M.brier([0, 1], [0.2, 0.6]), (0.04 + 0.16) / 2)
        self.assertAlmostEqual(M.scaled_brier([0, 1, 0, 1], [0.5] * 4), 0.0)

    def test_calibration_slope_intercept_recover_known_distortion(self):
        rng = np.random.default_rng(1)
        z = rng.normal(0, 1.5, 40000)
        y = (rng.random(z.size) < sigmoid(z)).astype(int)
        ok = M.calibration_intercept_slope(y, sigmoid(z))
        self.assertAlmostEqual(ok["slope"], 1.0, delta=0.05)
        self.assertAlmostEqual(ok["intercept"], 0.0, delta=0.05)
        over = M.calibration_intercept_slope(y, sigmoid(2 * z))     # too extreme -> slope ~0.5
        self.assertAlmostEqual(over["slope"], 0.5, delta=0.04)

    def test_ici_small_when_calibrated_large_when_not(self):
        rng = np.random.default_rng(2)
        p = rng.uniform(0.05, 0.95, 3000)
        y = (rng.random(p.size) < p).astype(int)
        self.assertLess(M.ici(y, p), 0.03)
        self.assertGreater(M.ici(y, np.clip(p + 0.2, 0, 1)), 0.12)

    def test_ece_threshold_rule_and_sensitivity(self):
        self.assertAlmostEqual(M.ece([0, 1], [0.05, 0.95], bins=10), 0.05)
        y = np.array([1, 1, 1, 1, 1, 0, 0, 0])
        p = np.array([0.9, 0.8, 0.7, 0.6, 0.2, 0.5, 0.3, 0.1])
        t = M.threshold_for_sensitivity(y, p, 0.80)               # 4 of 5 positives at or above t
        self.assertAlmostEqual(t, 0.6)
        ss = M.sensitivity_specificity(y, p, t)
        self.assertAlmostEqual(ss["sensitivity"], 0.8)
        self.assertAlmostEqual(ss["specificity"], 1.0)

    def test_threshold_rule_matches_exhaustive_search_including_ties(self):
        # protocol v1.0 candidate section 2: the LARGEST t with sensitivity(p >= t) >= target
        rng = np.random.default_rng(5)
        for trial in range(200):
            n = int(rng.integers(5, 60))
            p = np.round(rng.random(n), 1)                    # coarse values -> many ties (isotonic-like)
            y = (rng.random(n) < 0.5).astype(int)
            if y.sum() == 0 or y.sum() == n:
                continue
            target = float(rng.choice([0.5, 0.8, 0.9, 1.0]))
            t = M.threshold_for_sensitivity(y, p, target)
            ok = [c for c in np.unique(p) if (p[y == 1] >= c).mean() >= target]
            self.assertEqual(t, max(ok), msg=f"trial {trial}")

    def test_net_benefit_formula(self):
        nb = M.net_benefit([1, 0, 1, 0], [0.9, 0.6, 0.4, 0.1], [0.5])
        self.assertAlmostEqual(nb[0.5], 1 / 4 - 1 / 4 * 1.0)

    def test_input_validation(self):
        for bad in (([0, 2], [0.1, 0.2]), ([0, 1], [0.1, 1.2]), ([], []), ([0, 1], [0.1])):
            with self.assertRaises(ValueError):
                M.brier(*bad)
        with self.assertRaises(ValueError):
            M.auroc([1, 1], [0.2, 0.3])


class Calibration(unittest.TestCase):
    def test_pava_known_vector(self):
        np.testing.assert_allclose(pava([1, 3, 2, 4]), [1, 2.5, 2.5, 4])
        np.testing.assert_allclose(pava([3, 2, 1]), [2, 2, 2])

    def test_isotonic_monotone_and_ties_consistent(self):
        rng = np.random.default_rng(3)
        s = np.round(rng.random(500), 2)
        y = (rng.random(500) < s).astype(int)
        iso = IsotonicCalibrator().fit(s, y)
        out = iso.predict(np.sort(s))
        self.assertTrue(np.all(np.diff(out) >= -1e-12))
        self.assertEqual(len(set(iso.predict([0.5, 0.5]))), 1)

    def test_platt_recovers_known_map(self):
        rng = np.random.default_rng(4)
        p_raw = rng.uniform(0.02, 0.98, 30000)
        true = sigmoid(0.5 + 0.7 * np.log(p_raw / (1 - p_raw)))
        y = (rng.random(p_raw.size) < true).astype(int)
        pl = PlattCalibrator().fit(p_raw, y)
        self.assertAlmostEqual(pl.coef_[0], 0.5, delta=0.05)
        self.assertAlmostEqual(pl.coef_[1], 0.7, delta=0.05)

    def test_unfitted_and_separation_fail_closed(self):
        with self.assertRaises(RuntimeError):
            PlattCalibrator().predict([0.5])
        with self.assertRaises(ValueError):
            fit_logistic(np.c_[np.ones(4), [1, 2, 3, 4]], [0, 0, 1, 1])


class Conformal(unittest.TestCase):
    def test_class_conditional_coverage(self):
        cover = {0: [], 1: []}
        for rep in range(40):
            rng = np.random.default_rng(100 + rep)
            p = rng.uniform(0, 1, 2000)
            y = (rng.random(p.size) < p).astype(int)
            cp = MondrianConformal(0.10).fit(p[:1000], y[:1000])
            sets = cp.predict_sets(p[1000:])
            yt = y[1000:]
            for c in (0, 1):
                cover[c].append(sets[yt == c, c].mean())
        for c in (0, 1):
            self.assertGreaterEqual(np.mean(cover[c]), 0.895)

    def test_quantile_rank_and_small_class(self):
        cp = MondrianConformal(0.10).fit([0.9, 0.8, 0.2], [1, 1, 0])
        self.assertEqual(cp.q_[0], float("inf"))         # ceil(2 * 0.9) = 2 > n_0 = 1
        sets = cp.predict_sets([0.99])
        self.assertTrue(sets[0, 0])

    def test_invalid_alpha(self):
        with self.assertRaises(ValueError):
            MondrianConformal(0)


class CalibrationThenConformalOnSameDcal(unittest.TestCase):
    """The harness fits the calibrator AND the conformal quantiles on D-cal. A strictly increasing
    calibrator (Platt with positive slope) preserves the order of the scores, so the prediction sets
    are identical to those from the raw scores and the split-conformal guarantee is unaffected; a
    non-decreasing calibrator (isotonic) can only add labels (ties), so coverage is not reduced."""

    def setUp(self):
        rng = np.random.default_rng(21)
        self.p_raw = np.clip(rng.beta(2, 2, 800), 1e-6, 1 - 1e-6)
        self.y = (rng.random(800) < self.p_raw ** 1.5).astype(int)   # deliberately miscalibrated
        self.p_new = np.clip(rng.random(2000), 1e-6, 1 - 1e-6)

    def test_platt_positive_slope_gives_identical_sets(self):
        cal = PlattCalibrator().fit(self.p_raw, self.y)
        self.assertGreater(cal.coef_[1], 0)
        raw_sets = MondrianConformal(0.1).fit(self.p_raw, self.y).predict_sets(self.p_new)
        cal_sets = MondrianConformal(0.1).fit(cal.predict(self.p_raw), self.y).predict_sets(cal.predict(self.p_new))
        np.testing.assert_array_equal(raw_sets, cal_sets)

    def test_isotonic_sets_contain_raw_sets(self):
        cal = IsotonicCalibrator().fit(self.p_raw, self.y)
        raw_sets = MondrianConformal(0.1).fit(self.p_raw, self.y).predict_sets(self.p_new)
        iso_sets = MondrianConformal(0.1).fit(cal.predict(self.p_raw), self.y).predict_sets(cal.predict(self.p_new))
        self.assertTrue((iso_sets | ~raw_sets).all())     # raw set membership implies isotonic membership


class Statistics(unittest.TestCase):
    def test_holm_known(self):
        np.testing.assert_allclose(S.holm([0.01, 0.04, 0.03]), [0.03, 0.06, 0.06])

    def test_paired_bootstrap_identical_predictions(self):
        rng = np.random.default_rng(5)
        y = rng.integers(0, 2, 300)
        p = rng.random(300)
        r = S.paired_bootstrap(M.brier, y, p, p, n_boot=200, seed=1)
        self.assertEqual(r["difference"], 0.0)
        self.assertEqual(r["p_value"], 1.0)

    def test_bootstrap_reproducible(self):
        rng = np.random.default_rng(6)
        y = rng.integers(0, 2, 200)
        p = rng.random(200)
        a = S.bootstrap_ci(M.auroc, y, p, n_boot=100, seed=7)
        b = S.bootstrap_ci(M.auroc, y, p, n_boot=100, seed=7)
        self.assertEqual(a, b)

    def test_cluster_bootstrap_resamples_whole_psus_within_strata(self):
        strata = np.array([1, 1, 1, 1, 2, 2, 2, 2])
        psu = np.array([1, 1, 2, 2, 1, 1, 2, 2])
        for idx in S.cluster_bootstrap_indices(strata, psu, 20, seed=3):
            self.assertEqual(idx.size, 8)
            self.assertEqual(sorted(set(strata[idx])), [1, 2])
            for s in (1, 2):
                keys = set(zip(strata[idx][strata[idx] == s], psu[idx][strata[idx] == s]))
                self.assertTrue(keys)


if __name__ == "__main__":
    unittest.main()
