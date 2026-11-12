"""Tests for scripts/literature/expansion.py. SYNTHETIC paper IDs and decision rows only, in memory or
temporary directories; no real decision exists and none is written."""
import csv
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "literature"))
sys.path.insert(0, str(REPO / "tests" / "literature"))
import expansion as EX  # noqa: E402
import pubrecords as pr  # noqa: E402
from test_flow_diagram import row  # noqa: E402

FRAME = [f"P{n:04d}" for n in range(1, 1464)]           # 1,463 synthetic frame IDs
PILOT = FRAME[::24][:60]
assert len(PILOT) == 60


class Batches(unittest.TestCase):
    def test_partition_is_complete_disjoint_balanced_and_excludes_pilot(self):
        rows = EX.assign_batches(FRAME, PILOT, seed="S1")
        ids = [r["paper_id"] for r in rows]
        self.assertEqual(len(ids), 1463 - 60)
        self.assertEqual(len(set(ids)), len(ids))
        self.assertFalse(set(ids) & set(PILOT))
        sizes = {}
        for r in rows:
            sizes[r["batch"]] = sizes.get(r["batch"], 0) + 1
        self.assertEqual(len(sizes), 5)                      # ceil(1403 / 300)
        self.assertLessEqual(max(sizes.values()) - min(sizes.values()), 1)
        self.assertLessEqual(max(sizes.values()), 300)

    def test_deterministic_given_seed_and_seed_changes_order(self):
        a = EX.assign_batches(FRAME, PILOT, seed="S1")
        self.assertEqual(a, EX.assign_batches(FRAME, PILOT, seed="S1"))
        self.assertNotEqual([r["paper_id"] for r in a], [r["paper_id"] for r in EX.assign_batches(FRAME, PILOT, seed="S2")])

    def test_pilot_outside_frame_refused(self):
        with self.assertRaises(EX.ExpansionError):
            EX.assign_batches(FRAME[:10], ["P9999"], seed="S1")


class Audit(unittest.TestCase):
    def setUp(self):
        self.batches = EX.assign_batches(FRAME, PILOT, seed="S1")
        b12 = [r["paper_id"] for r in self.batches if r["batch"] in ("1", "2")]
        self.rows = []
        for i, pid in enumerate(b12):
            if i % 3 == 0:
                self.rows.append(row(pid, "title_abstract", "include"))
            elif i % 3 == 1:
                self.rows.append(row(pid, "title_abstract", "exclude", "E4"))
            else:
                self.rows.append(row(pid, "title_abstract", "exclude", "E5", screener=pr.STAGE0_SCREENER))

    def test_sample_sizes_blinded_and_deterministic(self):
        s = EX.audit_sample(self.rows, self.batches, [1, 2], seed="A1")
        self.assertEqual(len(s), 50)
        self.assertEqual(set(s[0]), set(EX.AUDIT_COLUMNS))  # no decision column
        dec = {r["paper_id"]: r["decision"] for r in self.rows}
        self.assertEqual(sum(dec[x["paper_id"]] == "include" for x in s), 25)
        stage0 = {r["paper_id"] for r in self.rows if r["screener"] == pr.STAGE0_SCREENER}
        self.assertFalse({x["paper_id"] for x in s} & stage0)  # Stage-0 rows are not audited
        self.assertEqual(s, EX.audit_sample(self.rows, self.batches, [1, 2], seed="A1"))

    def test_latest_row_counts_and_shortage_refused(self):
        pid = next(r["paper_id"] for r in self.rows if r["decision"] == "include")
        later = self.rows + [row(pid, "title_abstract", "exclude", "E4", screener="researcher")]
        s = EX.audit_sample(later, self.batches, [1, 2], seed="A1", n_include=1, n_exclude=1)
        self.assertEqual(len(s), 2)
        with self.assertRaisesRegex(EX.ExpansionError, "too few"):
            EX.audit_sample(self.rows[:10], self.batches, [1, 2], seed="A1")

    def test_outputs_are_never_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "batches.csv"
            EX._write_new(out, EX.BATCH_COLUMNS, self.batches)
            with self.assertRaises(EX.ExpansionError):
                EX._write_new(out, EX.BATCH_COLUMNS, self.batches)
            with open(out, newline="") as f:
                self.assertEqual(len(list(csv.DictReader(f))), 1403)


if __name__ == "__main__":
    unittest.main()
