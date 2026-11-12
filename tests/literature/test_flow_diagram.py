"""Tests for scripts/literature/flow_diagram.py. SYNTHETIC decision rows in temporary directories only;
nothing is written. Refusal without screening is tested on isolated temporary directories. One test
reads the real screening/decisions.csv (Stage 0 under D-121, 2026-11-12) and checks that the real
flow counts reconcile with that run; it reads, never writes."""
import contextlib
import csv
import io
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "literature"))
import flow_diagram as FD  # noqa: E402
import pubrecords as pr  # noqa: E402

SCOPE = [f"P{n:04d}" for n in range(1, 11)]       # 10 synthetic in-scope records
TA_FULL = dict(rq_tags="RQ1", record_type="original", biomarker_class="routine_chemistry",
               dim_explainability="no", dim_uncertainty="no", dim_calibration="no", validation_design="internal_only")


def row(pid, stage, decision, code="", screener="assistant", **kw):
    r = {c: "" for c in pr.SCREENING_REQUIRED + pr.SCREENING_OPTIONAL}
    r.update(paper_id=pid, stage=stage, decision=decision, reason_code=code, screener=screener,
             date="2026-11-20", justification="synthetic" if decision in ("exclude", "uncertain") else "",
             criteria_version="criteria_v1.1+protocol_v0.2")
    if stage == "title_abstract" and decision in ("include", "uncertain"):
        r.update(TA_FULL)
    r.update(kw)
    return r


class FlowDiagram(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lit = Path(self.tmp.name)
        (self.lit / "scope").mkdir()
        with open(self.lit / FD.SCOPE_FILE, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["paper_id"])
            w.writeheader()
            w.writerows({"paper_id": p} for p in SCOPE)

    def write(self, rows):
        (self.lit / "screening").mkdir(exist_ok=True)
        with open(self.lit / "screening" / "decisions.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=pr.SCREENING_REQUIRED + pr.SCREENING_OPTIONAL)
            w.writeheader()
            w.writerows(rows)

    def base_rows(self):
        return [row("P0001", "title_abstract", "exclude", "E5", screener=pr.STAGE0_SCREENER),
                row("P0002", "title_abstract", "exclude", "E4"),
                row("P0003", "title_abstract", "include"), row("P0003", "full_text", "include"),
                row("P0004", "title_abstract", "uncertain"), row("P0004", "full_text", "exclude", "E2"),
                row("P0005", "title_abstract", "include"), row("P0005", "full_text", "abstract_only"),
                row("P0006", "title_abstract", "include"),
                # superseded: P0007 first excluded, then adjudicated to include
                row("P0007", "title_abstract", "exclude", "E4"),
                row("P0007", "title_abstract", "include", screener="researcher")]

    def test_counts_reconcile_and_use_latest_rows(self):
        self.write(self.base_rows())
        c = FD.flow_counts(self.lit)
        self.assertEqual((c["scope"], c["stage0_excluded"], c["ta_screened"], c["awaiting_ta"]), (10, 1, 6, 3))
        self.assertEqual((c["ta_excluded"], c["ft_sought"], c["ta_include"], c["ta_uncertain"]), (1, 5, 4, 1))
        self.assertEqual((c["included"], c["ft_excluded"], c["ft_abstract_only"], c["awaiting_ft"]), (1, 1, 1, 2))
        self.assertEqual(c["rows_superseded"], 1)
        self.assertEqual(c["stage0_by_code"], {"E5": 1})
        md = FD.to_markdown(c)
        self.assertIn("| **Included** | **1** |", md)
        self.assertIn("flowchart TD", md)
        self.assertNotIn("synthetic", md)                  # no justification text leaks into the output

    def test_refuses_without_decisions(self):
        with self.assertRaises(FD.FlowError):
            FD.flow_counts(self.lit)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(FD.main(["--lit-dir", str(self.lit)]), 2)

    def test_refuses_invalid_rows(self):
        self.write([row("P0002", "title_abstract", "exclude", "")])        # exclude without a code
        with self.assertRaises(ValueError):
            FD.flow_counts(self.lit)
        self.write([row("P0003", "title_abstract", "include", rq_tags="")])  # D-060 (6) descriptors missing
        with self.assertRaises(ValueError):
            FD.flow_counts(self.lit)

    def test_refuses_out_of_scope_and_orphan_full_text(self):
        self.write([row("P0099", "title_abstract", "exclude", "E4")])
        with self.assertRaisesRegex(FD.FlowError, "outside the D-044 scope"):
            FD.flow_counts(self.lit)
        self.write([row("P0002", "title_abstract", "exclude", "E4"), row("P0002", "full_text", "include")])
        with self.assertRaisesRegex(FD.FlowError, "without a title/abstract include"):
            FD.flow_counts(self.lit)

    def test_refuses_without_decisions_file_or_rows_in_isolated_directory(self):
        # replaces the former real-repository check (no decisions file before Stage 0): without screening
        # the generator must refuse, never draw zeros; isolated temporary directory, independent of the repo
        (self.lit / "screening").mkdir()
        with self.assertRaisesRegex(FD.FlowError, "does not exist: no screening has been recorded"):
            FD.flow_counts(self.lit)
        with open(self.lit / "screening" / "decisions.csv", "w", newline="") as f:
            csv.DictWriter(f, fieldnames=pr.SCREENING_REQUIRED + pr.SCREENING_OPTIONAL).writeheader()
        with self.assertRaisesRegex(FD.FlowError, "has no decision rows"):
            FD.flow_counts(self.lit)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(FD.main(["--lit-dir", str(self.lit)]), 2)

    def test_real_repository_reconciles_with_the_stage0_run(self):
        # Stage 0 ran once under D-121 (single use, consumed): 1,470 in scope, 7 excluded (E5 5, E7 2).
        # These Stage-0 figures are permanent; later screening may only move records out of awaiting_ta.
        c = FD.flow_counts(REPO / "research" / "literature")
        self.assertEqual((c["scope"], c["stage0_excluded"], c["stage0_by_code"]), (1470, 7, {"E5": 5, "E7": 2}))
        self.assertEqual(c["criteria_versions"], ["criteria_v1.1+protocol_v0.2"])
        self.assertEqual(c["stage0_excluded"] + c["ta_screened"] + c["awaiting_ta"], c["scope"])
        self.assertEqual(c["awaiting_ta"], 1463 - c["ta_screened"])    # 1,463 before any title/abstract screening


if __name__ == "__main__":
    unittest.main()
