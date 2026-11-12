"""Tests for scripts/nhanes/build_dataset.py.

ALL DATA ARE SYNTHETIC component frames (scripts/models/synthetic.py): arbitrary values, IDs from
9,000,001, attrs["synthetic"] = True. They are not NHANES observations. No file is read, no network
is used and no model is fitted.
"""
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "nhanes"))
sys.path.insert(0, str(REPO / "scripts" / "models"))
import build_dataset as B  # noqa: E402
import safeguards as sg  # noqa: E402
from synthetic import synthetic_component_frames  # noqa: E402


class Groups(unittest.TestCase):
    def test_group_sizes_and_leakage_check(self):
        self.assertEqual(len(B.GROUP_A), 21)
        self.assertEqual(len(B.GROUP_C), 6)
        self.assertEqual(B.GROUPS["B"], B.GROUP_A + B.GROUP_C)
        for cols in B.GROUPS.values():
            sg.check_predictors(cols)
        self.assertNotIn("LBXSGL", B.GROUPS["B"])


class Outcome(unittest.TestCase):
    H = [5.6, 5.7, 5.0, 6.0, 5.5]
    G = [99, 90, 100, 110, 105]

    def test_definitions(self):
        np.testing.assert_array_equal(B.outcome(self.H, self.G), [0, 1, 1, 1, 1])
        np.testing.assert_array_equal(B.outcome(self.H, self.G, "S-01"), [0, 1, 0, 1, 0])
        np.testing.assert_array_equal(B.outcome(self.H, self.G, "S-02"), [0, 0, 1, 1, 1])
        np.testing.assert_array_equal(B.outcome(self.H, self.G, "S-03"), [0, 1, 0, 1, 0])
        np.testing.assert_array_equal(B.outcome(self.H, self.G, "S-15a"), [0, 0, 0, 1, 0])

    def test_never_imputed_and_unknown_rejected(self):
        with self.assertRaises(B.DatasetError):
            B.outcome([5.0, np.nan], [90, 95])
        with self.assertRaises(B.DatasetError):
            B.outcome([5.0], [90], "S-99")


class Assembly(unittest.TestCase):
    def setUp(self):
        self.dev = synthetic_component_frames(800, 1, "2017-2020")
        self.val = synthetic_component_frames(600, 2, "2021-2023")

    def test_cascade_matches_shared_rules_and_counts_are_monotone(self):
        ds = B.assemble_period(self.dev, "2017-2020")
        c = list(ds.cascade.values())
        self.assertTrue(all(a >= b for a, b in zip(c, c[1:])))
        self.assertEqual(ds.cascade["E8_analytic_N"], len(ds.y))
        self.assertTrue(ds.synthetic)
        # independent re-statement of E1-E8 on the merged synthetic frames
        d = self.dev["DEMO"].merge(self.dev["DIQ"], on="SEQN").merge(self.dev["GHB"], on="SEQN")
        d = d.merge(self.dev["GLU"].drop(columns="SYNTHETIC_FIXTURE"), on="SEQN", how="left", indicator="g")
        m = ((d.RIDSTATR == 2) & (d.RIDAGEYR >= 20) & (d.g == "both") & (d.WTSAFPRP > 0) & d.LBXGLU.notna()
             & d.LBXGH.notna() & ~(d.RIDEXPRG == 1) & d.DIQ010.isin([2, 3]) & ~(d.DIQ070 == 1))
        self.assertEqual(int(m.sum()), len(ds.y))
        self.assertEqual(sorted(ds.ids.tolist()), sorted(d.SEQN[m].tolist()))

    def test_features_bp_mean_and_triglyceride_mapping(self):
        ds = B.assemble_period(self.val, "2021-2023")
        self.assertEqual(list(ds.features.columns), B.GROUP_A + B.GROUP_C)
        bp = self.val["BPXO"].set_index("SEQN")
        sid = ds.ids[0]
        self.assertAlmostEqual(ds.features.loc[0, "SBP"], bp.loc[sid, ["BPXOSY1", "BPXOSY2", "BPXOSY3"]].mean())
        tg = self.val["TRIGLY"].set_index("SEQN").loc[sid, "LBXTLG"]
        self.assertAlmostEqual(ds.features.loc[0, "TRIG"], tg)

    def test_bp_mean_of_available_readings(self):
        frames = synthetic_component_frames(300, 3, "2017-2020")
        frames["BPXO"].loc[:, "BPXOSY3"] = np.nan
        ds = B.assemble_period(frames, "2017-2020")
        bp = frames["BPXO"].set_index("SEQN").loc[ds.ids[0]]
        self.assertAlmostEqual(ds.features.loc[0, "SBP"], (bp.BPXOSY1 + bp.BPXOSY2) / 2)

    def test_harmonisation_modes(self):
        ref = B.assemble_period(self.val, "2021-2023", harmonisation="S-08")
        with self.assertRaisesRegex(B.DatasetError, "Q-046"):
            B.assemble_period(self.val, "2021-2023", harmonisation="S-09b")
        adj = B.assemble_period(self.val, "2021-2023", harmonisation="S-09b", urdact_policy="unadjusted")
        np.testing.assert_allclose(adj.features["TRIG"], -12.19 + 0.9785 * ref.features["TRIG"])
        np.testing.assert_allclose(adj.features["LBXSATSI"], -1.529 + 1.035 * ref.features["LBXSATSI"])
        np.testing.assert_allclose(adj.features["URDACT"], ref.features["URDACT"])
        dev_ref = B.assemble_period(self.dev, "2017-2020", harmonisation="S-08")
        dev_adj = B.assemble_period(self.dev, "2017-2020", harmonisation="S-09b", urdact_policy="unadjusted")
        pd.testing.assert_frame_equal(dev_ref.features, dev_adj.features)   # 2017-2020 is the reference scale

    def test_period_pair_checks(self):
        dev = B.assemble_period(self.dev, "2017-2020")
        val = B.assemble_period(self.val, "2021-2023")
        B.check_period_pair(dev, val)
        overlap = synthetic_component_frames(800, 1, "2017-2020")
        with self.assertRaises(sg.LeakageError):
            B.check_period_pair(dev, B.assemble_period(overlap, "2017-2020"))
        with self.assertRaises(B.DatasetError):
            B.check_period_pair(dev, B.assemble_period(self.val, "2021-2023", outcome_definition="S-01"))

    def test_input_errors(self):
        frames = dict(self.dev)
        del frames["CBC"]
        with self.assertRaises(B.DatasetError):
            B.assemble_period(frames, "2017-2020")
        dup = dict(self.dev)
        dup["GHB"] = pd.concat([dup["GHB"], dup["GHB"].iloc[:1]])
        with self.assertRaises(sg.LeakageError):
            B.assemble_period(dup, "2017-2020")
        with self.assertRaises(B.DatasetError):
            B.assemble_period(self.dev, "2019")

    def test_real_file_loader_requires_authorisation(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(B.DatasetError, "authorisation"):
                B.load_period_files(d, "2017-2020", {}, authorisation=None)
            with self.assertRaisesRegex(B.DatasetError, "no expected SHA-256"):
                B.load_period_files(d, "2017-2020", {}, authorisation="TEST-ONLY")


if __name__ == "__main__":
    unittest.main()
