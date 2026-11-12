"""Tests for scripts/literature/rq5_review.py. SYNTHETIC decision rows only; nothing is written. Refusal
without screening and the Q-101 completeness gate are tested on isolated temporary directories."""
import contextlib
import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "literature"))
sys.path.insert(0, str(REPO / "tests" / "literature"))
import rq5_review as RV  # noqa: E402
import pubrecords as pr  # noqa: E402
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
        # isolated temporary directory without screening/decisions.csv (replaces the former real-repository
        # check, which held only before Stage 0); refusal is exit code 2 with a reason, never an empty matrix
        with tempfile.TemporaryDirectory() as tmp:
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                self.assertEqual(RV.main(["--lit-dir", tmp]), 2)
            self.assertIn("no screening has been recorded", err.getvalue())


# ------------------------------------------------------------------ Q-101: completeness gate (2026-11-12)
SCOPE5 = [f"P{n:04d}" for n in range(1, 6)]          # synthetic D-044 scope of five records


def stage0(pid):
    return row(pid, "title_abstract", "exclude", "E5", screener=pr.STAGE0_SCREENER)


def routed(pid):
    return row(pid, "title_abstract", "include", rq_tags="RQ5")


class RQ5Completeness(unittest.TestCase):
    """"Review complete: yes" only when (1) no in-scope record awaits title/abstract screening and (2) every
    RQ5-routed record has a confirmed full-text assessment and no matrix record awaits researcher
    verification. Isolated temporary directories; synthetic rows only."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lit = Path(self.tmp.name)
        (self.lit / "scope").mkdir()
        (self.lit / "screening").mkdir()
        with open(self.lit / "scope" / "D-044_scope_paper_ids.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["paper_id"])
            w.writeheader()
            w.writerows({"paper_id": p} for p in SCOPE5)
        (self.lit / "paper_inventory.json").write_text(
            json.dumps([{"paper_id": p, "verification_status": "unverified"} for p in SCOPE5]))

    def write(self, rows):
        with open(self.lit / "screening" / "decisions.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=pr.SCREENING_REQUIRED + pr.SCREENING_OPTIONAL)
            w.writeheader()
            w.writerows(rows)

    def run_cli(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = RV.main(["--lit-dir", str(self.lit)])
        return code, out.getvalue(), err.getvalue()

    def summary(self, rows):
        self.write(rows)
        decisions = pr.load_screening_decisions(self.lit, self.lit / "screening" / "decisions.csv")
        flow = RV.fd.flow_counts(self.lit)
        return RV.summarise(RV.matrix(decisions), RV.pending_assessment(decisions), flow)

    def assertIncomplete(self, out):
        self.assertTrue(out.startswith("**INCOMPLETE"), out[:80])
        self.assertIn("Review complete: NO", out)
        self.assertNotIn("Review complete: yes", out)

    def test_empty_screening_inventory(self):
        self.write([])                                                   # decisions file without rows
        code, out, err = self.run_cli()
        self.assertEqual((code, out), (2, ""))
        self.assertIn("has no decision rows", err)
        empty = {"scope": 0, "stage0_excluded": 0, "ta_screened": 0, "awaiting_ta": 0}
        s = RV.summarise([], (), empty)                                  # an empty scope is never complete
        self.assertEqual((s["screening_complete"], s["review_complete"]), (False, False))

    def test_records_awaiting_screening(self):
        rows = [stage0("P0001")]                                         # the real state after Stage 0
        s = self.summary(rows)
        self.assertEqual(s["screening"]["awaiting_ta"], 4)
        self.assertFalse(s["screening_complete"])
        self.assertTrue(s["rq5_routed_records_complete"])               # vacuous: nothing routed yet ...
        self.assertFalse(s["review_complete"])                          # ... so never a complete review
        code, out, _ = self.run_cli()
        self.assertEqual(code, 0)
        self.assertIncomplete(out)
        self.assertIn("4 of 5 in-scope record(s) awaiting screening", out)
        self.assertIn("routing is not final until title/abstract screening is complete", out)

    def test_partially_screened_inventory(self):
        rows = [stage0("P0001"), row("P0002", "title_abstract", "exclude", "E4"),
                routed("P0003"), ft("P0003", "yes", "yes", "yes", "yes", "yes", screener="researcher")]
        s = self.summary(rows)
        self.assertEqual((s["screening"]["awaiting_ta"], s["screening_complete"]), (2, False))
        self.assertTrue(s["rq5_routed_records_complete"])
        self.assertFalse(s["review_complete"])
        self.assertIncomplete(self.run_cli()[1])

    def test_fully_screened_with_incomplete_rq5_review(self):
        base = [stage0("P0001"), row("P0002", "title_abstract", "exclude", "E4"),
                row("P0004", "title_abstract", "exclude", "E4"), row("P0005", "title_abstract", "exclude", "E4")]
        # (i) a routed record without a confirmed full-text assessment
        s = self.summary(base + [routed("P0003")])
        self.assertTrue(s["screening_complete"])
        self.assertEqual(s["pending_full_text_assessment"], ["P0003"])
        self.assertEqual((s["rq5_routed_records_complete"], s["review_complete"]), (False, False))
        self.assertIncomplete(self.run_cli()[1])
        # (ii) assessed, but awaiting researcher verification
        s = self.summary(base + [routed("P0003"), ft("P0003", "yes", "yes", "yes", "yes", "yes")])
        self.assertEqual(s["verification_queue"], ["P0003"])
        self.assertEqual((s["screening_complete"], s["review_complete"]), (True, False))
        self.assertIncomplete(self.run_cli()[1])

    def test_genuinely_completed_rq5_review(self):
        rows = [stage0("P0001"), row("P0002", "title_abstract", "exclude", "E4"),
                routed("P0003"), ft("P0003", "yes", "yes", "yes", "yes", "yes", screener="researcher"),
                row("P0004", "title_abstract", "include"), row("P0005", "title_abstract", "exclude", "E4")]
        s = self.summary(rows)
        self.assertEqual((s["screening_complete"], s["rq5_routed_records_complete"], s["review_complete"]),
                         (True, True, True))
        code, out, _ = self.run_cli()
        self.assertEqual(code, 0)
        self.assertFalse(out.startswith("**INCOMPLETE"))
        self.assertIn("Review complete: yes", out)
        self.assertIn("0 of 5 in-scope record(s) awaiting screening", out)

    def test_summarise_without_screening_counts_fails_closed(self):
        rows = [r for r in RV.matrix([routed("P0003"), ft("P0003", "yes", "yes", "yes", "yes", "yes",
                                                         screener="researcher")])]
        s = RV.summarise(rows, ())                                       # no screening counts supplied
        self.assertTrue(s["rq5_routed_records_complete"])
        self.assertEqual((s["screening_complete"], s["review_complete"]), (False, False))
        md = RV.to_markdown(rows, s)
        self.assertTrue(md.startswith("**INCOMPLETE"))
        self.assertIn("status not available", md)

    def test_real_repository_never_reports_complete_while_records_await_screening(self):
        # read-only, state-independent: whatever the screening progress, a complete review requires that no
        # in-scope record awaits title/abstract screening, and the banner agrees with the summary
        lit = REPO / "research" / "literature"
        decisions = pr.load_screening_decisions(lit, lit / "screening" / "decisions.csv")
        flow = RV.fd.flow_counts(lit)
        s = RV.summarise(RV.matrix(decisions, RV.load_bibliographic_status(lit)), RV.pending_assessment(decisions), flow)
        self.assertEqual(s["screening"]["awaiting_ta"], flow["awaiting_ta"])
        if flow["awaiting_ta"] > 0:
            self.assertFalse(s["review_complete"])
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(RV.main(["--lit-dir", str(lit)]), 0)
        self.assertEqual(out.getvalue().startswith("**INCOMPLETE"), not s["review_complete"])
        self.assertEqual("Review complete: yes" in out.getvalue(), s["review_complete"])


if __name__ == "__main__":
    unittest.main()
