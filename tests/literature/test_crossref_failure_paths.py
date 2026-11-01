"""Failure-path tests for fetch_crossref.py and the manifest write in pubrecords.register_raw
(software gap closure, 2026-11-01).

ALL RESPONSES ARE SYNTHETIC (DOIs use the non-existent prefix 10.0000). No network: requests go
through a fake transport and urllib's urlopen is patched to fail if reached. Failures are injected
by replacing the `os` module reference of one module with a proxy that fails a chosen call, or by
raising KeyboardInterrupt from the fake transport. Everything is written to temporary directories.

What these tests show is the behaviour of the code at each injected failure point. They do not show
behaviour after a real power loss or kernel crash, and they do not make the persistence path atomic:
see the fetch_crossref.py docstring ("Persistence and interruptions").

Run from the repository root:
    python3 -I -m unittest discover -s tests/literature -p test_crossref_failure_paths.py -v
"""
import contextlib
import io
import json
import os
import stat
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_crossref_robustness import DOI1, U1, U6, FetchCase, body  # noqa: E402
from test_crossref_verification import FakeTransport  # noqa: E402
from test_pubrecords import pr  # noqa: E402
import fetch_crossref as fc  # noqa: E402

U7, U8 = fc.API + "10.0000/x.7", fc.API + "10.0000/x.8"


class OsProxy:
    """Stands in for the `os` module inside one module; delegates everything except the methods
    given as overrides (callables replacing os.<name>)."""

    def __init__(self, **overrides):
        self._overrides = overrides

    def __getattr__(self, name):
        return self._overrides.get(name) or getattr(os, name)


def failing_fsync(predicate, exc=OSError("fsync failed (injected)")):
    def fsync(fd):
        if predicate(fd):
            raise exc
        return os.fsync(fd)
    return fsync


def is_dir(fd):
    return stat.S_ISDIR(os.fstat(fd).st_mode)


class Case(FetchCase):
    def setUp(self):
        super().setUp()
        self.inv += [{"paper_id": "P0007", "doi": "10.0000/x.7"}, {"paper_id": "P0008", "doi": "10.0000/x.8"}]

    def write_pilot_and_inventory(self, pids):
        pilot = self.lit / "pilot.csv"
        pilot.write_text("paper_id\n" + "".join(p + "\n" for p in pids))
        with open(self.lit / "paper_inventory.json", "w") as f:
            json.dump(self.inv, f)
        return pilot

    def run_main(self, pids, script, execute=True):
        pilot = self.write_pilot_and_inventory(pids)
        t = FakeTransport(script)
        out = io.StringIO()
        argv = ["--pilot", str(pilot), "--run-date", "2026-11-01", "--lit-dir", str(self.lit)]
        with mock.patch.object(fc, "Transport", lambda: t), contextlib.redirect_stdout(out):
            status = fc.main(argv + (["--execute"] if execute else []))
        return status, json.loads(out.getvalue()), t


class TestSyncFailures(Case):
    """Gaps 1 and 2: manifest fsync and directory fsync failures."""

    def test_manifest_fsync_failure_is_reported_with_the_state_on_disk(self):
        # register_raw writes the row, then its fsync fails: the run stops and says what is on disk
        with mock.patch.object(pr, "os", OsProxy(fsync=failing_fsync(lambda fd: True))):
            report = self.run_fc({U1: [(200, body())], U6: [(200, body("10.0000/x.6"))]}, pids=("P0001", "P0006"))
        self.assertTrue(report["aborted"])
        (entry,) = report["results"]
        self.assertEqual(entry["outcome"], "persistence_error")
        self.assertIn("fsync failed", entry["error"])
        self.assertTrue(entry["file_saved"])
        self.assertTrue(entry["manifest_row_present"])       # written, durability not confirmed
        self.assertFalse((self.raw / fc.LOCK_NAME).exists())
        self.assertEqual(report["orphans"], [])
        # resume: the registered paper is skipped, the second is fetched; nothing is duplicated
        report2 = self.run_fc({U6: [(200, body("10.0000/x.6"))]}, pids=("P0001", "P0006"))
        self.assertEqual([r["outcome"] for r in report2["results"]], ["already_registered", "saved"])
        self.assertEqual([r["query_id"] for r in pr.read_manifest(self.lit)], ["VERIFY-CR-P0001", "VERIFY-CR-P0006"])

    def test_manifest_fsync_failure_on_a_new_manifest_keeps_a_parseable_file(self):
        with mock.patch.object(pr, "os", OsProxy(fsync=failing_fsync(lambda fd: True))):
            report = self.run_fc({U1: [(200, body())]})
        self.assertEqual(report["results"][0]["outcome"], "persistence_error")
        self.assertEqual(fc.manifest_problems(self.lit), [])          # header and row complete
        self.assertTrue((self.raw / "MANIFEST.csv").read_bytes().endswith(b"\r\n"))

    def test_directory_fsync_failure_keeps_the_file_and_warns(self):
        with mock.patch.object(fc, "os", OsProxy(fsync=failing_fsync(is_dir))):
            report = self.run_fc({U1: [(200, body())]})
        self.assertEqual(report["results"][0]["outcome"], "saved")
        self.assertNotIn("aborted", report)
        self.assertEqual(len(report["warnings"]), 1)
        self.assertIn("directory fsync failed", report["warnings"][0])
        self.assertEqual([r["raw_file"] for r in pr.read_manifest(self.lit)], ["CR_2026-10-31_000.json"])

    def test_no_warnings_key_when_nothing_went_wrong(self):
        report = self.run_fc({U1: [(200, body())]})
        self.assertNotIn("warnings", report)

    def test_partial_file_fsync_failure_stops_before_any_final_file(self):
        partial_fsync = failing_fsync(lambda fd: not is_dir(fd))
        with mock.patch.object(fc, "os", OsProxy(fsync=partial_fsync)):
            report = self.run_fc({U1: [(200, body())]})
        self.assertEqual(report["results"][0]["outcome"], "persistence_error")
        self.assertFalse(report["results"][0]["file_saved"])
        self.assertFalse(report["results"][0]["manifest_row_present"])
        self.assertEqual(report["orphans"], ["CR_2026-10-31_000.json.partial"])
        self.assertFalse((self.raw / "MANIFEST.csv").exists())


class TestCommandLineExitStatus(Case):
    """Gaps 3, 4 and 5: exit status through main() and the report for mixed outcomes."""

    def test_failed_response_exits_1(self):
        status, report, _ = self.run_main(["P0001"], {U1: [(404, b"Resource not found.")]})
        self.assertEqual(status, 1)
        self.assertEqual(report["results"][0]["outcome"], "failed")
        self.assertEqual(report["results"][0]["http_status"], 404)

    def test_exhausted_retries_exit_1(self):
        status, report, t = self.run_main(["P0001"], {U1: [(503, b""), (503, b""), (503, b"")]})
        self.assertEqual(status, 1)
        self.assertEqual(report["results"][0]["attempts"], 3)

    def test_malformed_response_exits_1(self):
        for bad in (b"<html>", body(override={"title": "SYNTHETIC string"}), body("10.0000/other")):
            with self.subTest(body=bad[:30]):
                status, report, _ = self.run_main(["P0001"], {U1: [(200, bad)]})
                self.assertEqual(status, 1)
                self.assertEqual(report["results"][0]["outcome"], "malformed")
                self.assertFalse((self.raw / "MANIFEST.csv").exists())

    def test_all_saved_exits_0_and_dry_run_exits_0(self):
        status, report, _ = self.run_main(["P0001"], {U1: [(200, body())]})
        self.assertEqual((status, report["results"][0]["outcome"]), (0, "saved"))
        status, report, t = self.run_main(["P0006"], {}, execute=False)
        self.assertEqual((status, report["results"][0]["outcome"], t.urls), (0, "dry_run", []))

    def test_refused_run_exits_1(self):
        status, report, t = self.run_main(["P0001", "P9999"], {})
        self.assertEqual(status, 1)
        self.assertTrue(report["refused"])
        self.assertEqual(t.urls, [])

    def test_mixed_outcomes_produce_one_complete_report(self):
        script = {U1: [(404, b"")], U6: [(200, b"not json")], U7: [RuntimeError("transport bug (injected)")],
                  U8: [(200, body("10.0000/x.8"))]}
        status, report, t = self.run_main(["P0001", "P0006", "P0007", "P0008"], script)
        self.assertEqual(status, 1)
        self.assertEqual([(r["paper_id"], r["outcome"]) for r in report["results"]],
                         [("P0001", "failed"), ("P0006", "malformed"), ("P0007", "error"), ("P0008", "saved")])
        self.assertNotIn("aborted", report)
        self.assertEqual(report["orphans"], [])
        self.assertEqual([r["query_id"] for r in pr.read_manifest(self.lit)], ["VERIFY-CR-P0008"])
        self.assertFalse((self.raw / fc.LOCK_NAME).exists())


class TestPlanningFailuresAndInterrupts(Case):
    """Gap 6: documents the actual behaviour. A planning failure or a KeyboardInterrupt raises; no run
    report is produced for it (limitation). The lock is never left behind by an interrupt, and the
    persisted state stays consistent, so the run can be resumed."""

    def test_missing_inventory_raises_before_anything_is_written(self):
        with self.assertRaises(FileNotFoundError):
            fc.run(["P0001"], "2026-11-01", self.lit, None, FakeTransport({}), sleep=lambda s: None, execute=True)
        self.assertEqual(self.files(), [])                     # no lock, no raw file, no manifest

    def test_unreadable_inventory_raises_before_anything_is_written(self):
        (self.lit / "paper_inventory.json").write_text("{not json")
        with self.assertRaises(json.JSONDecodeError):
            fc.run(["P0001"], "2026-11-01", self.lit, None, FakeTransport({}), sleep=lambda s: None, execute=True)
        self.assertEqual(self.files(), [])

    def test_keyboard_interrupt_between_papers(self):
        class InterruptingTransport(FakeTransport):      # FakeTransport raises Exception subclasses only
            def get(self, url):
                if url == U6:
                    raise KeyboardInterrupt()
                return super().get(url)
        with self.assertRaises(KeyboardInterrupt):
            fc.run(["P0001", "P0006"], "2026-10-31", self.lit, self.inv, InterruptingTransport({U1: [(200, body())]}),
                   sleep=lambda s: None, execute=True)
        self.assertFalse((self.raw / fc.LOCK_NAME).exists())     # released in `finally`
        self.assertEqual([r["query_id"] for r in pr.read_manifest(self.lit)], ["VERIFY-CR-P0001"])
        self.assertEqual(fc.orphans(self.lit), [])
        report = self.run_fc({U6: [(200, body("10.0000/x.6"))]}, pids=("P0001", "P0006"))
        self.assertEqual([r["outcome"] for r in report["results"]], ["already_registered", "saved"])

    def test_keyboard_interrupt_during_save_leaves_an_orphan_and_a_resumable_state(self):
        def interrupt(*a):
            raise KeyboardInterrupt()
        with mock.patch.object(fc, "os", OsProxy(link=interrupt)), self.assertRaises(KeyboardInterrupt):
            self.run_fc({U1: [(200, body())]})
        self.assertFalse((self.raw / fc.LOCK_NAME).exists())
        self.assertEqual(fc.orphans(self.lit), ["CR_2026-10-31_000.json.partial"])
        self.assertFalse((self.raw / "MANIFEST.csv").exists())
        report = self.run_fc({U1: [(200, body())]})
        self.assertEqual(report["results"][0]["raw_file"], "CR_2026-10-31_001.json")
        self.assertEqual(report["orphans"], ["CR_2026-10-31_000.json.partial"])   # kept, never deleted


class TestRecovery(Case):
    """Gap 7: recovery from an interrupted write, orphan files, an incomplete manifest line and a
    stale lock. Each repair the code does not make itself is a documented manual step."""

    def test_truncated_partial_file_from_a_crash(self):
        crashed = self.raw / "CR_2026-10-31_000.json.partial"
        crashed.write_bytes(body()[:25])                        # what a crash mid-write could leave
        report = self.run_fc({U1: [(200, body())]})
        self.assertEqual(report["orphans_before"], ["CR_2026-10-31_000.json.partial"])
        self.assertEqual(report["results"][0]["raw_file"], "CR_2026-10-31_001.json")
        self.assertEqual(crashed.read_bytes(), body()[:25])
        self.assertEqual(len(pr.read_manifest(self.lit)), 1)

    def test_orphan_final_file_is_never_registered_by_a_later_run(self):
        orphan = self.raw / "CR_2026-10-31_000.json"
        orphan.write_bytes(body())                              # saved, registration interrupted
        report = self.run_fc({U1: [(200, body())]})
        self.assertEqual(report["results"][0]["raw_file"], "CR_2026-10-31_001.json")
        self.assertEqual([r["raw_file"] for r in pr.read_manifest(self.lit)], ["CR_2026-10-31_001.json"])
        self.assertEqual(report["orphans"], ["CR_2026-10-31_000.json"])

    def test_incomplete_manifest_line_then_manual_repair(self):
        self.run_fc({U1: [(200, body())]})
        mp = self.raw / "MANIFEST.csv"
        good = mp.read_bytes()
        mp.write_bytes(good[:-10])
        refused = fc.run(["P0006"], "2026-10-31", self.lit, self.inv, FakeTransport({}), sleep=lambda s: None, execute=True)
        self.assertTrue(refused["refused"])
        mp.write_bytes(good)                                    # the researcher's manual repair
        report = self.run_fc({U6: [(200, body("10.0000/x.6"))]}, pids=("P0006",))
        self.assertEqual(report["results"][0]["outcome"], "saved")

    def test_stale_lock_then_manual_removal(self):
        lock = self.raw / fc.LOCK_NAME
        lock.write_text("pid 1 started 2026-10-31T00:00:00+00:00\n")
        self.assertTrue(fc.run(["P0001"], "2026-10-31", self.lit, self.inv, FakeTransport({}),
                               sleep=lambda s: None, execute=True)["refused"])
        self.assertEqual(lock.read_text(), "pid 1 started 2026-10-31T00:00:00+00:00\n")
        lock.unlink()                                           # the researcher's manual step
        report = self.run_fc({U1: [(200, body())]})
        self.assertEqual(report["results"][0]["outcome"], "saved")

    def test_dry_run_never_takes_the_lock_or_writes(self):
        report = fc.run(["P0001"], "2026-10-31", self.lit, self.inv, FakeTransport({}), sleep=lambda s: None)
        self.assertEqual(report["results"][0]["outcome"], "dry_run")
        self.assertEqual(self.files(), [])


if __name__ == "__main__":
    unittest.main()
