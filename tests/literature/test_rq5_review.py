"""Tests for scripts/literature/rq5_review.py. SYNTHETIC decision rows only; nothing is written."""
import contextlib
import io
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "literature"))
sys.path.insert(0, str(REPO / "tests" / "literature"))
import rq5_review as RV  # noqa: E402
from test_flow_diagram import row  # noqa: E402


def ft(pid, fs, cl, ex, ca, un, screener="assistant", decision="include"):
    return row(pid, "full_text", decision, screener=screener, dim_feature_selection=fs, dim_classification=cl,
               dim_explainability=ex, dim_calibration=ca, dim_uncertainty=un, date="2026-11-21")


class RQ5Matrix(unittest.TestCase):
    def rows(self):
        return [
            row("P0001", "title_abstract", "include"), ft("P0001", "yes", "yes", "yes", "yes", "yes"),
            row("P0002", "title_abstract", "include"), ft("P0002", "unclear", "yes", "yes", "yes", "yes"),
            row("P0003", "title_abstract", "include"), ft("P0003", "no", "yes", "yes", "yes", "no"),
            row("P0004", "title_abstract", "include"), ft("P0004", "yes", "yes", "no", "no", "no"),
            row("P0005", "title_abstract", "include"), ft("P0005", "no", "yes", "yes", "yes", "yes"),
            ft("P0005", "no", "yes", "yes", "yes", "yes", screener="researcher"),
        ]

    def test_groups_subgroups_and_queue(self):
        m = {r["paper_id"]: r for r in RV.matrix(self.rows())}
        self.assertEqual(m["P0001"]["d038_subgroup"], "a: 5 yes")
        self.assertEqual(m["P0002"]["d038_subgroup"], "b: 4 yes + unclear feature_selection")
        self.assertEqual(m["P0005"]["d038_subgroup"], "c: 4 yes + 1 no")
        self.assertEqual(m["P0003"]["group"], "near_rq5")
        self.assertEqual(m["P0004"]["group"], "below_threshold")
        self.assertEqual(m["P0005"]["planned_components_covered"],
                         "4/4 (calibration, classification, explainability, uncertainty)")
        s = RV.summarise(list(m.values()))
        self.assertEqual(s["counts"], {"qualified": 3, "near_rq5": 1, "below_threshold": 1})
        self.assertEqual(s["all_five_components"], ["P0001"])
        self.assertNotIn("P0005", s["verification_queue"])         # researcher-verified
        self.assertIn("P0002", s["verification_queue"])

    def test_bibliographic_status_marked_and_completeness_gate(self):
        rows = self.rows() + [row("P0006", "title_abstract", "include", rq_tags="RQ5")]   # routed, no full text
        m = RV.matrix(rows, {"P0001": "verified", "P0002": "partially_verified"})
        by = {r["paper_id"]: r for r in m}
        self.assertTrue(by["P0001"]["citable"])
        self.assertEqual((by["P0002"]["bibliographic_status"], by["P0002"]["citable"]), ("partially_verified", False))
        self.assertEqual(by["P0003"]["bibliographic_status"], "unknown")
        s = RV.summarise(m, RV.pending_assessment(rows))
        self.assertEqual(s["pending_full_text_assessment"], ["P0006"])
        self.assertFalse(s["review_complete"])
        self.assertIn("NO — no contribution or novelty wording is supported yet", RV.to_markdown(m, s))
        self.assertIn("(not citable)", RV.to_markdown(m, s))

    def test_title_abstract_statuses_never_count(self):
        only_ta = [row("P0009", "title_abstract", "include", dim_explainability="yes", dim_calibration="yes",
                       dim_uncertainty="yes")]
        self.assertEqual(RV.matrix(only_ta), [])

    def test_incomplete_full_text_assessment_refused(self):
        with self.assertRaises(ValueError):
            RV.matrix([row("P0001", "title_abstract", "include"), ft("P0001", "yes", "yes", "", "yes", "yes")])

    def test_cli_refuses_without_screening(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(RV.main(["--lit-dir", str(REPO / "research" / "literature")]), 2)


if __name__ == "__main__":
    unittest.main()
