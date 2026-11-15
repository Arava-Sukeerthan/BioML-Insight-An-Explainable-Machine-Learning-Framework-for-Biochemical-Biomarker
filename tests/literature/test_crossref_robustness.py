"""Regression and failure-injection tests for the Crossref defect corrections (audit of 2026-10-31).

ALL FIXTURE RECORDS AND RESPONSES ARE SYNTHETIC SOFTWARE-TEST DATA (titles start with "SYNTHETIC",
DOIs use the non-existent prefix 10.0000). No test contacts a network service: requests go through
a fake transport and urllib's urlopen is patched to fail if reached. Failures are injected by
patching file-system and registration calls; nothing outside a temporary directory is written.

Run from the repository root:
    python3 -I -m unittest discover -s tests/literature -p test_crossref_robustness.py -v
"""
import hashlib
import http.client
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_crossref_verification import (CrossrefFixture, FakeTransport, OUTPUTS, TEST_YEAR_RULE,  # noqa: E402
                                        append_manifest_row, crossref_body, no_network)
from test_pubrecords import pr  # noqa: E402
import fetch_crossref as fc  # noqa: E402

DOI1 = "10.0000/x.1"
U1 = fc.API + DOI1
U6 = fc.API + "10.0000/x.6"


def body(doi=DOI1, title="SYNTHETIC one", override=None):
    """A synthetic response; `override` replaces message fields verbatim (to build wrong shapes)."""
    msg = json.loads(crossref_body(doi, title, "Alpha", "Synthetic Journal A"))
    msg["message"].update(override or {})
    return json.dumps(msg, sort_keys=True).encode()


class FetchCase(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch("urllib.request.urlopen", side_effect=no_network)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lit = Path(self.tmp.name)
        self.raw = self.lit / "raw_exports"
        self.raw.mkdir()
        self.inv = [{"paper_id": "P0001", "doi": DOI1}, {"paper_id": "P0006", "doi": "10.0000/x.6"}]

    def run_fc(self, script, pids=("P0001",), **kw):
        return fc.run(list(pids), "2026-10-31", self.lit, self.inv, FakeTransport(script),
                      sleep=lambda s: None, execute=True, **kw)

    def manifest_bytes(self):
        p = self.raw / "MANIFEST.csv"
        return p.read_bytes() if p.exists() else None

    def files(self):
        return sorted(p.name for p in self.raw.iterdir())


class TestParserShapes(unittest.TestCase):
    """A2: wrongly shaped fields are malformed (ValueError), never silently truncated or TypeError."""

    def test_wrong_shapes_raise_value_error(self):
        base = {"DOI": DOI1, "title": ["SYNTHETIC t"], "container-title": ["J"]}
        bad = {"title": ["abc", 5, {"x": 1}, ["ok", 3], [None], True],
               "container-title": ["Journal", 7, {"x": 1}, [1]],
               "author": [{"family": "A"}, "A", [1], [{"family": 3}], [{"name": ["x"]}], [{"sequence": 1}]],
               "DOI": [10.1, None, ["10.0000/x.1"]]}
        for key, values in bad.items():
            for v in values:
                with self.subTest(key=key, value=v), self.assertRaises(ValueError):
                    pr.parse_crossref_work({**base, key: v})

    def test_null_and_empty_fields_are_absent_not_errors(self):
        for v in (None, [], [""]):
            m = pr.parse_crossref_work({"DOI": DOI1, "title": v, "container-title": v, "author": None})
            self.assertIsNone(m["title"])
            self.assertIsNone(m["journal"])
            self.assertEqual(m["authors"], [])

    def test_year_rule_rejects_malformed_date_parts(self):
        for v in ("2021", {"date-parts": "2021"}, {"date-parts": []}, {"date-parts": [[]]},
                  {"date-parts": [[True]]}, {"date-parts": [[{"y": 2021}]]}):
            with self.subTest(v=v), self.assertRaises(ValueError):
                pr.crossref_year({"published-print": v}, ("published-print",))
        self.assertEqual(pr.crossref_year({"published-print": {"date-parts": [[2021, 5]]}}, ("published-print",)), 2021)
        self.assertIsNone(pr.crossref_year({"published-print": "junk"}))      # no rule decided: not read

    def test_fetcher_reports_wrong_shapes_and_truncation_as_malformed(self):
        cases = [body(override={"title": "SYNTHETIC string title"}), body(override={"title": 5}),
                 body(override={"container-title": 7}), body(override={"author": "Alpha"}),
                 body()[:-15], b"\xff\xfe not utf-8", json.dumps([1, 2]).encode()]
        for b in cases:
            with self.subTest(body=b[:30]):
                with tempfile.TemporaryDirectory() as d:
                    lit = Path(d)
                    (lit / "raw_exports").mkdir()
                    r = fc.run(["P0001"], "2026-10-31", lit, [{"paper_id": "P0001", "doi": DOI1}],
                               FakeTransport({U1: [(200, b)]}), sleep=lambda s: None, execute=True)
                    self.assertEqual(r["results"][0]["outcome"], "malformed")
                    self.assertEqual(sorted(p.name for p in (lit / "raw_exports").iterdir()), [])


class TestMarkup(unittest.TestCase):
    """A6: inline markup in Crossref titles is removed without inserting a space."""

    def test_inline_and_block_markup(self):
        cases = {"Glycated HbA<sub>1c</sub> levels": "Glycated HbA1c levels",
                 "<i>In vivo</i> SYNTHETIC": "In vivo SYNTHETIC",
                 "CO<jats:sub>2</jats:sub> and <jats:italic>E. coli</jats:italic>": "CO2 and E. coli",
                 "<mml:math><mml:msub><mml:mi>H</mml:mi><mml:mn>2</mml:mn></mml:msub></mml:math>O": "H2O",
                 "<jats:p>First</jats:p><jats:p>Second</jats:p>": "First Second",
                 "p < 0.05 and HbA1c<6.5%": "p < 0.05 and HbA1c<6.5%",
                 "A &amp; B": "A & B"}
        for raw, want in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(pr.strip_inline_markup(raw), want)
        self.assertEqual(pr.strip_markup("HbA<sub>1c</sub>"), "HbA 1c")    # ordinary parsing unchanged

    def test_subscript_title_agrees_with_plain_pubmed_title(self):
        fx = CrossrefFixture()
        self.addCleanup(fx.tmp.cleanup)
        _, base = fx.build()
        p1 = fx.pid(base, "900000101")
        fx.pilot([p1])
        b = crossref_body("10.0000/cr.1", "SYNTHETIC crossref <i>match</i> target one", "Alpha", "Synthetic Journal A", 2021)
        fx.add_crossref(p1, "10.0000/cr.1", b)
        with mock.patch.object(pr, "CROSSREF_YEAR_FIELDS", TEST_YEAR_RULE):
            _, pubs = fx.build()
        self.assertEqual(pubs[p1]["verification_status"], "verified")
        fx2 = CrossrefFixture()
        self.addCleanup(fx2.tmp.cleanup)
        _, base2 = fx2.build()
        p1 = fx2.pid(base2, "900000101")
        fx2.pilot([p1])
        b = crossref_body("10.0000/cr.1", "SYNTHETIC crossref ma<sub>tch</sub> target one", "Alpha", "Synthetic Journal A", 2021)
        fx2.add_crossref(p1, "10.0000/cr.1", b)
        with mock.patch.object(pr, "CROSSREF_YEAR_FIELDS", TEST_YEAR_RULE):
            _, pubs = fx2.build()
        self.assertEqual(pubs[p1]["verification_status"], "verified")      # "ma<sub>tch</sub>" -> "match"


class TestRouteValidation(unittest.TestCase):
    """A3: VERIFY- query IDs cannot enter ordinary processing through another route."""

    def setUp(self):
        self.fx = CrossrefFixture()
        self.addCleanup(self.fx.tmp.cleanup)
        _, self.base = self.fx.build()
        self.digest = self.fx.digest(*OUTPUTS)
        self.p1 = self.fx.pid(self.base, "900000101")

    def test_register_raw_refuses_verify_ids_on_other_routes(self):
        name = "VERIFY_misrouted.json"
        (self.fx.lit / "raw_exports" / name).write_text(json.dumps({"records": [{"title": "SYNTHETIC x"}]}))
        for route in ("structured_transcription", "pubmed_connector_search", "eutils_efetch"):
            with self.subTest(route=route), self.assertRaises(ValueError):
                pr.register_raw(self.fx.lit, name, pr.VERIFY_PREFIX + self.p1, "crossref", route, "x", {},
                                "2026-10-31T10:00:00+00:00", 1, True)

    def test_build_refuses_a_hand_registered_verify_row_on_another_route(self):
        name = "VERIFY_misrouted.json"
        (self.fx.lit / "raw_exports" / name).write_text(json.dumps(
            {"records": [{"title": "SYNTHETIC misrouted lookup", "doi": "10.0000/new.9", "year": 2020}]}))
        append_manifest_row(self.fx.lit, name, pr.VERIFY_PREFIX + self.p1, "structured_transcription", self.p1)
        with self.assertRaises(RuntimeError) as cm:
            self.fx.build()
        self.assertIn("verification", str(cm.exception))
        self.assertEqual(self.fx.digest(*OUTPUTS), self.digest)            # nothing written, no new paper ID

    def test_build_refuses_a_non_object_crossref_file(self):
        name = "CR_2026-10-31_000.json"
        (self.fx.lit / "raw_exports" / name).write_bytes(json.dumps([1, 2]).encode())
        append_manifest_row(self.fx.lit, name, pr.VERIFY_PREFIX + self.p1, pr.CROSSREF_ROUTE, self.p1)
        self.fx.pilot([self.p1])
        with self.assertRaises(RuntimeError):
            self.fx.build()
        self.assertEqual(self.fx.digest(*OUTPUTS), self.digest)


class TestNoYearRuleAndConflicts(unittest.TestCase):
    """A5: without a year rule Crossref can never verify, but its conflicts still give needs_review
    (D-064 A4). The behaviour is documented and tested, not changed (changing it would be a decision)."""

    def build_with(self, **kw):
        fx = CrossrefFixture()
        self.addCleanup(fx.tmp.cleanup)
        _, base = fx.build()
        p1 = fx.pid(base, "900000101")
        fx.pilot([p1])
        args = dict(title="SYNTHETIC crossref match target one", family="Alpha", venue="Synthetic Journal A", year=2021)
        args.update(kw)
        fx.add_crossref(p1, "10.0000/cr.1", crossref_body("10.0000/cr.1", **args))
        self.assertIsNone(pr.CROSSREF_YEAR_FIELDS)
        report, pubs = fx.build()
        return base, pubs, p1, report

    def test_agreement_without_year_rule_stays_partially_verified(self):
        base, pubs, p1, _ = self.build_with()
        self.assertEqual(pubs[p1]["verification_status"], "partially_verified")

    def test_conflicts_without_year_rule_give_needs_review(self):
        for field, kw in {"venue": dict(venue="Synthetic Journal A : subtitle"),
                          "title": dict(title="SYNTHETIC unrelated title"),
                          "first_author": dict(family="Omega")}.items():
            with self.subTest(field=field):
                base, pubs, p1, report = self.build_with(**kw)
                self.assertEqual(pubs[p1]["verification_status"], "needs_review")
                self.assertIn(field, pubs[p1]["verification_note"])
                self.assertEqual(set(pubs), set(base))                      # no new paper IDs
                for k in ("title", "journal", "year", "authors", "doi", "search_provenance", "source_databases"):
                    self.assertEqual(pubs[p1][k], base[p1][k])              # authoritative fields untouched
                self.assertEqual([c["paper_id"] for c in report["verification_status_changes"]["changed"]], [p1])


class TestPersistenceFailures(FetchCase):
    """A1/A4: failure injection on the save-and-register path."""

    def assert_clean_failure(self, report, manifest_before):
        self.assertTrue(report["aborted"])
        self.assertEqual(report["results"][-1]["outcome"], "persistence_error")
        self.assertEqual(self.manifest_bytes(), manifest_before)           # manifest untouched
        self.assertFalse((self.raw / fc.LOCK_NAME).exists())               # lock released
        self.assertNotIn("CR_2026-10-31_000.json", [r["raw_file"] for r in pr.read_manifest(self.lit)])

    def test_write_failure_leaves_no_final_file_and_reports(self):
        with mock.patch.object(fc.os, "fsync", side_effect=OSError("disk full (injected)")):
            report = self.run_fc({U1: [(200, body())]})
        self.assert_clean_failure(report, None)
        self.assertNotIn("CR_2026-10-31_000.json", self.files())
        self.assertEqual(report["orphans"], ["CR_2026-10-31_000.json.partial"])  # kept for inspection

    def test_readback_mismatch_is_a_persistence_error(self):
        real_read = Path.read_bytes
        with mock.patch.object(Path, "read_bytes", lambda p: b"corrupt" if p.name.endswith(".partial") else real_read(p)):
            report = self.run_fc({U1: [(200, body())]})
        self.assert_clean_failure(report, None)
        self.assertNotIn("CR_2026-10-31_000.json", self.files())

    def test_link_failure_never_overwrites(self):
        with mock.patch.object(fc.os, "link", side_effect=FileExistsError("exists (injected)")):
            report = self.run_fc({U1: [(200, body())]})
        self.assert_clean_failure(report, None)

    def test_registration_failure_leaves_an_orphan_and_a_resumable_state(self):
        with mock.patch.object(pr, "register_raw", side_effect=OSError("interrupted (injected)")):
            report = self.run_fc({U1: [(200, body())], U6: [(200, body("10.0000/x.6"))]}, pids=("P0001", "P0006"))
        self.assert_clean_failure(report, None)
        self.assertEqual(len(report["results"]), 1)                         # stopped after the failure
        self.assertEqual(report["orphans"], ["CR_2026-10-31_000.json"])
        orphan = (self.raw / "CR_2026-10-31_000.json").read_bytes()
        # resume: same run date, nothing deleted, orphan untouched and still unregistered
        report2 = self.run_fc({U1: [(200, body())], U6: [(200, body("10.0000/x.6"))]}, pids=("P0001", "P0006"))
        self.assertEqual([r["outcome"] for r in report2["results"]], ["saved", "saved"])
        self.assertEqual([r["raw_file"] for r in report2["results"]], ["CR_2026-10-31_001.json", "CR_2026-10-31_002.json"])
        self.assertEqual((self.raw / "CR_2026-10-31_000.json").read_bytes(), orphan)
        self.assertEqual(report2["orphans"], ["CR_2026-10-31_000.json"])
        self.assertEqual([r["query_id"] for r in pr.read_manifest(self.lit)], ["VERIFY-CR-P0001", "VERIFY-CR-P0006"])

    def test_interrupted_manifest_append_is_detected_and_never_extended(self):
        self.run_fc({U1: [(200, body())]})
        mp = self.raw / "MANIFEST.csv"
        damaged = mp.read_bytes()[:-20]                                     # simulate a cut-off last row
        mp.write_bytes(damaged)
        t = FakeTransport({})
        report = fc.run(["P0006"], "2026-10-31", self.lit, self.inv, t, sleep=lambda s: None, execute=True)
        self.assertTrue(report["refused"])
        self.assertIn("incomplete", " ".join(report["problems"]))
        self.assertEqual(t.urls, [])
        self.assertEqual(mp.read_bytes(), damaged)                          # not repaired, not extended
        (self.raw / "CR_2026-10-31_005.json").write_bytes(body("10.0000/x.6"))   # a new, unregistered file
        with self.assertRaises(ValueError) as cm:
            pr.register_raw(self.lit, "CR_2026-10-31_005.json", "VERIFY-CR-P0006", "crossref", pr.CROSSREF_ROUTE,
                            "x", {}, "2026-10-31T10:00:00+00:00", 1, False)
        self.assertIn("incomplete", str(cm.exception))
        self.assertEqual(mp.read_bytes(), damaged)

    def test_row_with_missing_columns_refuses_the_run(self):
        self.run_fc({U1: [(200, body())]})
        mp = self.raw / "MANIFEST.csv"
        mp.write_bytes(mp.read_bytes() + b"CR_x.json,abc\r\n")
        report = fc.run(["P0006"], "2026-10-31", self.lit, self.inv, FakeTransport({}), sleep=lambda s: None, execute=True)
        self.assertTrue(report["refused"])
        self.assertIn("wrong number of columns", " ".join(report["problems"]))

    def test_stale_lock_refuses_and_is_left_in_place(self):
        (self.raw / fc.LOCK_NAME).write_text("pid 1\n")
        t = FakeTransport({})
        report = fc.run(["P0001"], "2026-10-31", self.lit, self.inv, t, sleep=lambda s: None, execute=True)
        self.assertTrue(report["refused"])
        self.assertIn("interrupted", " ".join(report["problems"]))      # refused at planning, before any request
        self.assertEqual(t.urls, [])
        self.assertTrue((self.raw / fc.LOCK_NAME).exists())

    def test_already_registered_papers_are_skipped_without_a_request(self):
        self.run_fc({U1: [(200, body())]})
        t = FakeTransport({U6: [(200, body("10.0000/x.6"))]})
        report = fc.run(["P0001", "P0006"], "2026-10-31", self.lit, self.inv, t, sleep=lambda s: None, execute=True)
        self.assertEqual([r["outcome"] for r in report["results"]], ["already_registered", "saved"])
        self.assertEqual(t.urls, [U6])

    def test_successful_save_leaves_no_partial_file_and_matches_bytes(self):
        b = body()
        report = self.run_fc({U1: [(200, b)]})
        self.assertEqual(self.files(), ["CR_2026-10-31_000.json", "MANIFEST.csv"])
        self.assertEqual((self.raw / "CR_2026-10-31_000.json").read_bytes(), b)
        (row,) = pr.read_manifest(self.lit)
        self.assertEqual(row["sha256"], hashlib.sha256(b).hexdigest())
        self.assertEqual(report["orphans"], [])
        self.assertTrue(self.manifest_bytes().endswith(b"\r\n"))


class TestPerRecordErrors(FetchCase):
    """A4: unexpected exceptions are recorded per record and the report is always produced."""

    def test_http_exceptions_are_retried_transport_errors(self):
        script = {U1: [http.client.IncompleteRead(b"{"), http.client.RemoteDisconnected("x"), (200, body())]}
        report = self.run_fc(script)
        self.assertEqual((report["results"][0]["outcome"], report["results"][0]["attempts"]), ("saved", 3))

    def test_unexpected_transport_exception_does_not_stop_the_run(self):
        report = self.run_fc({U1: [RuntimeError("bug in transport (injected)")], U6: [(200, body("10.0000/x.6"))]},
                             pids=("P0001", "P0006"))
        self.assertEqual([r["outcome"] for r in report["results"]], ["error", "saved"])
        self.assertNotIn("aborted", report)
        self.assertFalse((self.raw / fc.LOCK_NAME).exists())

    def test_non_bytes_body_is_malformed(self):
        report = self.run_fc({U1: [(200, None)]})
        self.assertEqual(report["results"][0]["outcome"], "malformed")

    def test_main_exit_status(self):
        pilot = self.lit / "pilot.csv"
        pilot.write_text("paper_id\nP0001\n")
        with open(self.lit / "paper_inventory.json", "w") as f:
            json.dump(self.inv, f)
        with mock.patch("sys.stdout"):
            self.assertEqual(fc.main(["--pilot", str(pilot), "--run-date", "2026-10-31", "--lit-dir", str(self.lit)]), 0)
            (self.raw / fc.LOCK_NAME).write_text("x")
            with mock.patch.object(fc, "Transport", side_effect=AssertionError("no transport expected")):
                self.assertEqual(fc.main(["--pilot", str(pilot), "--run-date", "2026-10-31", "--lit-dir",
                                          str(self.lit), "--execute"]), 1)

    def test_bad_run_date_is_refused(self):
        report = fc.run(["P0001"], "../evil", self.lit, self.inv, FakeTransport({}), sleep=lambda s: None, execute=True)
        self.assertTrue(report["refused"])


if __name__ == "__main__":
    unittest.main()
