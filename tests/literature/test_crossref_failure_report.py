"""Failure reports for runs that do not finish: planning failures and KeyboardInterrupt
(failure-report reliability review, 2026-11-01).

ALL RESPONSES ARE SYNTHETIC (DOIs use the non-existent prefix 10.0000). No network: requests go
through a fake transport and urllib's urlopen is patched to fail if reached. Everything is written to
temporary directories.

Checked here: an "incomplete" report is printed before the original exception is re-raised
unchanged (same object, same traceback); a failure while writing that report never replaces the
original exception; the lock and the persisted state stay consistent; completed runs say so.

Run from the repository root:
    python3 -I -m unittest discover -s tests/literature -p test_crossref_failure_report.py -v
"""
import contextlib
import io
import json
import sys
import traceback
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_crossref_failure_paths import Case, OsProxy  # noqa: E402
from test_crossref_robustness import U1, U6, body  # noqa: E402
from test_crossref_verification import FakeTransport  # noqa: E402
from test_pubrecords import pr  # noqa: E402
import fetch_crossref as fc  # noqa: E402


class InterruptingTransport(FakeTransport):
    """FakeTransport raises only Exception subclasses; this one raises KeyboardInterrupt for one URL."""

    def __init__(self, script, interrupt_url):
        super().__init__(script)
        self.interrupt_url = interrupt_url

    def get(self, url):
        if url == self.interrupt_url:
            self.urls.append(url)
            raise KeyboardInterrupt()
        return super().get(url)


class ReportCase(Case):
    def main_expecting(self, exc_type, pids, transport=None, write_inventory=True, pilot=None):
        """Run main(); return (raised exception, parsed stdout report, stderr text)."""
        if write_inventory:
            pilot_path = self.write_pilot_and_inventory(pids)
        else:
            pilot_path = pilot
        out, err = io.StringIO(), io.StringIO()
        argv = ["--pilot", str(pilot_path), "--run-date", "2026-11-01", "--lit-dir", str(self.lit), "--execute"]
        caught = None
        with mock.patch.object(fc, "Transport", lambda: transport or FakeTransport({})), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:                        # not assertRaises: it drops the traceback we want to inspect
                fc.main(argv)
            except BaseException as e:  # noqa: B036
                caught = e
        self.assertIsInstance(caught, exc_type)
        return caught, json.loads(out.getvalue()), err.getvalue()


class TestPlanningFailures(ReportCase):
    def test_missing_pilot_file(self):
        exc, report, _ = self.main_expecting(FileNotFoundError, [], write_inventory=False,
                                             pilot=self.lit / "absent.csv")
        self.assertEqual((report["status"], report["completed"]), ("incomplete", False))
        self.assertEqual(report["failure_stage"], "reading_pilot")
        self.assertEqual(report["exception"], "FileNotFoundError")
        self.assertIsNone(report["partial_report"])
        self.assertIn("load_pilot", "".join(traceback.format_tb(exc.__traceback__)))   # original traceback
        self.assertEqual(self.files(), [])

    def test_missing_inventory(self):
        pilot = self.lit / "pilot.csv"
        pilot.write_text("paper_id\nP0001\n")
        exc, report, _ = self.main_expecting(FileNotFoundError, [], write_inventory=False, pilot=pilot)
        self.assertEqual(report["failure_stage"], "planning")
        self.assertIsNone(report["partial_report"])
        self.assertIn("paper_inventory.json", report["message"])
        self.assertEqual(self.files(), [])                     # no lock, no raw file, no manifest

    def test_unreadable_manifest_during_planning(self):
        pilot = self.write_pilot_and_inventory(["P0001"])
        (self.raw / "MANIFEST.csv").write_bytes(b"\xff\xfe broken")
        out = io.StringIO()
        with contextlib.redirect_stdout(out), self.assertRaises(UnicodeDecodeError):
            fc.main(["--pilot", str(pilot), "--run-date", "2026-11-01", "--lit-dir", str(self.lit), "--execute"])
        report = json.loads(out.getvalue())
        self.assertEqual((report["status"], report["failure_stage"]), ("incomplete", "planning"))
        self.assertFalse((self.raw / fc.LOCK_NAME).exists())
        self.assertEqual((self.raw / "MANIFEST.csv").read_bytes(), b"\xff\xfe broken")   # untouched


class TestKeyboardInterrupt(ReportCase):
    def test_interrupt_between_papers_reports_partial_results_then_reraises(self):
        t = InterruptingTransport({U1: [(200, body())]}, U6)
        exc, report, _ = self.main_expecting(KeyboardInterrupt, ["P0001", "P0006"], t)
        self.assertEqual((report["status"], report["completed"], report["exception"]),
                         ("incomplete", False, "KeyboardInterrupt"))
        self.assertEqual(report["failure_stage"], "finishing")   # interrupt surfaced after `finally` ran
        partial = report["partial_report"]
        self.assertEqual(partial["status"], "incomplete")
        self.assertEqual([(r["paper_id"], r["outcome"]) for r in partial["results"]], [("P0001", "saved")])
        self.assertEqual(partial["orphans"], [])
        self.assertFalse((self.raw / fc.LOCK_NAME).exists())
        self.assertEqual([r["query_id"] for r in pr.read_manifest(self.lit)], ["VERIFY-CR-P0001"])
        # resume with the same command line: completed run, clearly marked
        status, resumed, _ = self.run_main(["P0001", "P0006"], {U6: [(200, body("10.0000/x.6"))]})
        self.assertEqual(status, 0)
        self.assertEqual(resumed["status"], "finished")
        self.assertEqual([r["outcome"] for r in resumed["results"]], ["already_registered", "saved"])

    def test_interrupt_during_save_lists_the_orphan(self):
        def interrupt(*a):
            raise KeyboardInterrupt()
        with mock.patch.object(fc, "os", OsProxy(link=interrupt)):
            _, report, _ = self.main_expecting(KeyboardInterrupt, ["P0001"], FakeTransport({U1: [(200, body())]}))
        self.assertEqual(report["partial_report"]["orphans"], ["CR_2026-11-01_000.json.partial"])
        self.assertEqual(report["partial_report"]["results"], [])          # no outcome recorded for P0001
        self.assertFalse((self.raw / fc.LOCK_NAME).exists())
        self.assertFalse((self.raw / "MANIFEST.csv").exists())

    def test_incomplete_report_never_claims_completion(self):
        t = InterruptingTransport({}, U1)
        _, report, _ = self.main_expecting(KeyboardInterrupt, ["P0001"], t)
        text = json.dumps(report)
        self.assertNotIn('"finished"', text)
        self.assertNotIn('"saved"', text)
        self.assertFalse(report["completed"])


class TestReportWritingNeverReplacesTheError(ReportCase):
    def test_failure_report_construction_error_keeps_the_original_exception(self):
        t = InterruptingTransport({}, U1)
        self.write_pilot_and_inventory(["P0001"])
        err = io.StringIO()
        with mock.patch.object(fc, "failure_report", side_effect=RuntimeError("report bug (injected)")), \
                mock.patch.object(fc, "Transport", lambda: t), contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(err), self.assertRaises(KeyboardInterrupt):
            fc.main(["--pilot", str(self.lit / "pilot.csv"), "--run-date", "2026-11-01", "--lit-dir", str(self.lit),
                     "--execute"])
        self.assertIn("failure report could not be written: RuntimeError", err.getvalue())

    def test_broken_stdout_and_stderr_are_tolerated(self):
        class Broken(io.StringIO):
            def write(self, s):
                raise OSError("broken pipe (injected)")
        with contextlib.redirect_stderr(Broken()):
            fc.emit_failure_report(KeyboardInterrupt(), {"stage": "fetching"}, stream=Broken())   # no exception

    def test_reraised_exception_is_the_same_object(self):
        sentinel = RuntimeError("unexpected (injected)")

        def failing_run(*a, progress=None, **k):
            progress["stage"] = "fetching"
            progress["report"] = {"status": "incomplete", "results": []}
            raise sentinel
        pilot = self.write_pilot_and_inventory(["P0001"])
        out = io.StringIO()
        caught = None
        with mock.patch.object(fc, "run", failing_run), contextlib.redirect_stdout(out):
            try:
                fc.main(["--pilot", str(pilot), "--run-date", "2026-11-01", "--lit-dir", str(self.lit)])
            except RuntimeError as e:
                caught = e
        self.assertIs(caught, sentinel)
        self.assertIn("failing_run", "".join(traceback.format_tb(caught.__traceback__)))
        self.assertEqual(json.loads(out.getvalue())["failure_stage"], "fetching")

    def test_orphan_listing_failure_in_finally_does_not_replace_the_interrupt(self):
        progress = {}
        real = fc.orphans
        calls = []

        def orphans(lit_dir):
            calls.append(1)
            if len(calls) > 1:                                   # the call in `finally`
                raise RuntimeError("listing failed (injected)")
            return real(lit_dir)
        with mock.patch.object(fc, "orphans", orphans), self.assertRaises(KeyboardInterrupt):
            fc.run(["P0001"], "2026-11-01", self.lit, self.inv, InterruptingTransport({}, U1),
                   sleep=lambda s: None, execute=True, progress=progress)
        report = progress["report"]
        self.assertIsNone(report["orphans"])
        self.assertIn("orphan listing failed", report["warnings"][0])
        self.assertFalse((self.raw / fc.LOCK_NAME).exists())


class TestProcessLevelBehaviour(ReportCase):
    """In a child process: report on stdout, original traceback on stderr, non-zero exit status.
    run() is replaced inside the child by a function that raises, so no network code can run."""

    CHILD = (
        "import sys; sys.path.insert(0, {scripts!r}); import fetch_crossref as fc\n"
        "def run(*a, progress=None, **k):\n"
        "    progress['stage'] = 'fetching'; progress['report'] = {{'status': 'incomplete', 'results': []}}\n"
        "    raise {exc}\n"
        "fc.run = run\n"
        "sys.exit(fc.main(['--pilot', {pilot!r}, '--run-date', '2026-11-01', '--lit-dir', {lit!r}]))\n")

    def child(self, exc):
        import subprocess
        pilot = self.write_pilot_and_inventory(["P0001"])
        scripts = str(Path(fc.__file__).resolve().parent)
        code = self.CHILD.format(scripts=scripts, exc=exc, pilot=str(pilot), lit=str(self.lit))
        return subprocess.run([sys.executable, "-I", "-B", "-c", code], capture_output=True, text=True, timeout=60)

    def test_keyboard_interrupt_in_a_process(self):
        r = self.child("KeyboardInterrupt()")
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(json.loads(r.stdout)["exception"], "KeyboardInterrupt")
        self.assertIn("KeyboardInterrupt", r.stderr)            # original traceback still printed

    def test_planning_style_error_in_a_process(self):
        r = self.child("ValueError('bad inventory (injected)')")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(json.loads(r.stdout)["status"], "incomplete")
        self.assertIn("ValueError: bad inventory (injected)", r.stderr)


class TestLockLifecycle(ReportCase):
    def test_lock_write_failure_releases_the_lock_this_run_created(self):
        def failing_write(fd, data):
            raise OSError("disk full (injected)")
        progress = {}
        with mock.patch.object(fc, "os", OsProxy(write=failing_write)), self.assertRaises(OSError):
            fc.run(["P0001"], "2026-11-01", self.lit, self.inv, FakeTransport({}), sleep=lambda s: None,
                   execute=True, progress=progress)
        self.assertFalse((self.raw / fc.LOCK_NAME).exists())
        self.assertEqual(progress["report"]["status"], "incomplete")

    def test_a_lock_created_by_another_run_is_never_removed(self):
        lock = self.raw / fc.LOCK_NAME
        real_open = fc.os.open

        def racing_open(path, flags, *a):
            if str(path).endswith(fc.LOCK_NAME):
                lock.write_text("pid 2 (another run)\n")         # appears between check and create
                raise FileExistsError(path)
            return real_open(path, flags, *a)
        with mock.patch.object(fc, "os", OsProxy(open=racing_open)):
            report = fc.run(["P0001"], "2026-11-01", self.lit, self.inv, FakeTransport({}), sleep=lambda s: None,
                            execute=True)
        self.assertEqual((report["status"], report["refused"]), ("refused", True))
        self.assertEqual(lock.read_text(), "pid 2 (another run)\n")


class TestCompletedRunsAreMarked(ReportCase):
    def test_statuses(self):
        status, report, _ = self.run_main(["P0001"], {U1: [(200, body())]})
        self.assertEqual((status, report["status"]), (0, "finished"))
        status, report, _ = self.run_main(["P0006"], {U6: [(404, b"")]})
        self.assertEqual((status, report["status"], report["results"][0]["outcome"]), (1, "finished", "failed"))
        status, report, _ = self.run_main(["P0001", "P9999"], {})
        self.assertEqual((status, report["status"]), (1, "refused"))
        with mock.patch.object(pr, "register_raw", side_effect=OSError("injected")):
            status, report, _ = self.run_main(["P0007"], {fc.API + "10.0000/x.7": [(200, body("10.0000/x.7"))]})
        self.assertEqual((status, report["status"]), (1, "aborted"))
        for r in (report,):
            self.assertNotIn("completed", r)                    # only failure reports carry `completed`


if __name__ == "__main__":
    unittest.main()
