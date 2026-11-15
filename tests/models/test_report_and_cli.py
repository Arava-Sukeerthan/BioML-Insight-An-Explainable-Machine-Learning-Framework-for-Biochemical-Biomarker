"""Tests for scripts/models/report.py and the dataset-build CLI (scripts/nhanes/build_dataset.py).

ALL DATA ARE SYNTHETIC. Outputs go to temporary directories only; the CLI is exercised only on its
refusal paths (it needs real files and an authorisation reference, neither of which is used here).
"""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "models"))
sys.path.insert(0, str(REPO / "scripts" / "nhanes"))
import build_dataset as B  # noqa: E402
import report as RP  # noqa: E402
from synthetic import synthetic_component_frames  # noqa: E402


def record(model, label="SYNTHETIC", auroc=0.7):
    return {"model": model, "data_label": label, "seeds": [1, 2], "config_hash": "ab" * 32,
            "internal_summary": {"auroc": {"mean": auroc, "sd": 0.01}, "brier": {"mean": 0.2, "sd": 0.002}},
            "temporal_validation": {"auroc": auroc - 0.02, "brier": 0.21}}


class ResultsTable(unittest.TestCase):
    def test_table_content_and_label(self):
        t = RP.results_table([record("BL-1"), record("F2", auroc=0.72)], metrics=("auroc", "brier"))
        self.assertIn("Data label: **SYNTHETIC**", t)
        self.assertIn("not evidence of model performance", t)
        self.assertIn("| BL-1 | 2 | abababababab | 0.700 ± 0.010 | 0.200 ± 0.002 | 0.680 | 0.210 |", t)
        self.assertEqual(t.count("\n| F2 "), 1)

    def test_internal_estimate_is_selectable_and_stated(self):
        r = record("F2")
        r["internal_calibrated_summary"] = {"auroc": {"mean": 0.7, "sd": 0.01}, "brier": {"mean": 0.18, "sd": 0.001}}
        t = RP.results_table([r], metrics=("brier",), internal="internal_calibrated_summary")
        self.assertIn("Internal estimate: `internal_calibrated_summary`.", t)
        self.assertIn("| 0.180 ± 0.001 |", t)
        with self.assertRaises(ValueError):
            RP.results_table([r], internal="other")

    def test_mixed_labels_and_empty_refused(self):
        with self.assertRaises(ValueError):
            RP.results_table([record("BL-1"), record("BL-2", label="REAL")])
        with self.assertRaises(ValueError):
            RP.results_table([])

    def test_load_records_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "runs.jsonl"
            p.write_text(json.dumps(record("BL-1")) + "\n\n", encoding="utf-8")
            self.assertEqual(RP.load_records(p)[0]["model"], "BL-1")
            p.write_text("not json\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                RP.load_records(p)


class CalibrationCurve(unittest.TestCase):
    def test_uniform_bins_hand_computed(self):
        rows = RP.calibration_curve([0, 1, 1, 0], [0.05, 0.15, 0.95, 0.92], bins=10)
        self.assertEqual([r["bin"] for r in rows], [0, 1, 9])
        self.assertEqual(rows[2]["n"], 2)
        self.assertAlmostEqual(rows[2]["observed_rate"], 0.5)
        self.assertAlmostEqual(rows[2]["mean_predicted"], 0.935)
        for r in rows:
            self.assertTrue(r["ci_low"] <= r["observed_rate"] <= r["ci_high"])

    def test_quantile_bins_cover_all_cases(self):
        rng = np.random.default_rng(3)
        p = rng.random(500)
        y = (rng.random(500) < p).astype(int)
        rows = RP.calibration_curve(y, p, bins=5, strategy="quantile")
        self.assertEqual(sum(r["n"] for r in rows), 500)
        self.assertEqual(len(rows), 5)

    def test_csv_and_small_cell_protection(self):
        rows = RP.calibration_curve([0, 1, 1, 0], [0.05, 0.15, 0.95, 0.92])
        with tempfile.TemporaryDirectory() as d:
            path = RP.write_csv(rows, Path(d) / "cal.csv")
            self.assertTrue(path.read_text(encoding="utf-8").startswith("bin,lower_edge"))
            with self.assertRaises(ValueError):
                RP.write_csv(rows, Path(d) / "cal2.csv", min_cell=5)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            RP.calibration_curve([0, 2], [0.1, 0.2])
        with self.assertRaises(ValueError):
            RP.calibration_curve([0, 1], [0.1, 0.2], strategy="other")


class DatasetCli(unittest.TestCase):
    def test_git_ignore_check(self):
        self.assertTrue(B._git_ignored(REPO / "data" / "derived" / "nhanes" / "x.csv"))
        self.assertFalse(B._git_ignored(REPO / "scripts" / "nhanes" / "x.csv"))

    def test_outputs_refused_outside_ignored_location(self):
        ds = B.assemble_period(synthetic_component_frames(300, 1, "2017-2020"), "2017-2020")
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(B.DatasetError, "not Git-ignored"):
                B.write_outputs(ds, d)
            with mock.patch.object(B, "_git_ignored", return_value=True):
                path, summary = B.write_outputs(ds, d)
            self.assertEqual(summary["n"], len(ds.y))
            self.assertTrue(summary["synthetic"])
            self.assertEqual(set(summary["complete_cases"]), {"A", "B", "C"})
            head = path.read_text(encoding="utf-8").splitlines()[0].split(",")
            self.assertEqual(head[:2], ["SEQN", "y"])

    def test_cli_refuses_without_authorisation_or_files(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                B.main(["--period", "2017-2020"])
            with tempfile.TemporaryDirectory() as d:
                self.assertEqual(B.main(["--period", "2017-2020", "--authorisation", "TEST-ONLY", "--raw-dir", d]), 2)


if __name__ == "__main__":
    unittest.main()
