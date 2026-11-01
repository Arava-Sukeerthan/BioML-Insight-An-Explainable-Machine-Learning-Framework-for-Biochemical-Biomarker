"""Tests for Crossref verification lookups (WP2): fetch_crossref.py and the build safeguards in
pubrecords.py.

ALL FIXTURE RECORDS AND RESPONSES IN THIS FILE ARE SYNTHETIC SOFTWARE-TEST DATA. They are not real
publications or real Crossref responses: titles start with "SYNTHETIC", PMIDs are in the 9000001xx
range and DOIs use the non-existent prefix 10.0000. No test contacts any network service: every
request goes through a fake transport, and urllib's urlopen is patched to fail if it is ever reached.

Run from the repository root:
    python3 -I -m unittest discover -s tests/literature -v
"""
import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_pubrecords import connector_article, write_json, pr  # noqa: E402
import fetch_crossref as fc  # noqa: E402

TEST_YEAR_RULE = ("published-print",)   # test-only: the real rule is a pending researcher decision

QUERIES = [{"query_id": "Q-TEST-CR", "row_type": "planned", "source": "pubmed",
            "query_string": "synthetic crossref fixture"}]
BASE = [  # pmid, doi, title, author, journal, year
    ("900000101", "10.0000/cr.1", "SYNTHETIC crossref match target one", "Alpha", "Synthetic Journal A", "2021"),
    ("900000102", "10.0000/cr.2", "SYNTHETIC crossref conflict target two", "Beta", "Synthetic Journal B", "2020"),
    ("900000103", None, "SYNTHETIC title only target three", "Gamma", "Synthetic Journal C", "2022"),
    # two PubMed records with the same DOI but different PMIDs: identifier conflict, never merged,
    # so DOI 10.0000/cr.dup belongs to two publications
    ("900000104", "10.0000/cr.dup", "SYNTHETIC duplicate doi record four", "Delta", "Synthetic Journal D", "2019"),
    ("900000105", "10.0000/cr.dup", "SYNTHETIC duplicate doi record five", "Epsilon", "Synthetic Journal D", "2019"),
]


def crossref_body(doi, title, family, venue, year=None, sequence="first", **extra):
    msg = {"DOI": doi, "title": [title] if title else [], "container-title": [venue] if venue else [],
           "author": ([{"family": family, "given": "Test", "sequence": sequence}] if family else []),
           "type": "journal-article"}
    if year is not None:
        msg["published-print"] = {"date-parts": [[year, 1]]}
        msg["issued"] = {"date-parts": [[year]]}
    msg.update(extra)
    return json.dumps({"status": "ok", "message-type": "work", "message": msg}, sort_keys=True).encode()


class FakeTransport:
    """Returns queued (status, body) pairs or raises queued exceptions; records every URL."""

    def __init__(self, script):
        self.script, self.urls = dict(script), []

    def get(self, url):
        self.urls.append(url)
        queue = self.script[url]
        item = queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def no_network(*a, **k):
    raise AssertionError("network access attempted in a test")


def append_manifest_row(lit, name, query_id, route, pid, source="crossref"):
    """Simulates a hand-edited manifest row (bypasses register_raw and its checks)."""
    path = lit / "raw_exports" / name
    row = {c: "" for c in pr.MANIFEST_COLS}
    row.update(raw_file=name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(), query_id=query_id,
               source=source, route=route, endpoint_or_tool="synthetic",
               request_json=json.dumps({"doi": "10.0000/cr.1", "paper_id": pid}),
               retrieved_at="2026-10-31T10:00:00+00:00", n_items="1", transcribed="no",
               transcription_check="not_applicable")
    with open(lit / "raw_exports" / "MANIFEST.csv", "a", newline="") as f:
        csv.DictWriter(f, fieldnames=pr.MANIFEST_COLS).writerow(row)


class CrossrefFixture:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.lit = Path(self.tmp.name) / "literature"
        (self.lit / "raw_exports").mkdir(parents=True)
        with open(self.lit / "search_queries.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["query_id", "row_type", "source", "query_string"])
            w.writeheader()
            w.writerows(QUERIES)
        self._reg("Q-TEST-CR_search_00.json", {"pmids": [b[0] for b in BASE], "total_count": len(BASE)},
                  "Q-TEST-CR", "pubmed_connector_search", {"retstart": 0})
        self._reg("META_cr.json", {"articles": [
            connector_article(p, t, doi=d, journal=j, year=y, last=a) for p, d, t, a, j, y in BASE]},
            "META", "pubmed_connector_metadata", {})
        for name in ("Q-TEST-CR_search_00.json", "META_cr.json"):
            pr.set_transcription_check(self.lit, name, "passed", "synthetic test")

    def _reg(self, name, response, qid, route, request):
        write_json(self.lit, name, {}, response)
        pr.register_raw(self.lit, name, qid, "pubmed", route, "synthetic-tool", request,
                        "2026-10-14T10:00:00+00:00", 1, True)

    def build(self):
        report = pr.build(self.lit, today="2026-10-15")
        return report, self.pubs()

    def pubs(self):
        with open(self.lit / "records" / "publications.jsonl") as f:
            return {p["paper_id"]: p for p in (json.loads(line) for line in f)}

    def pid(self, pubs, pmid):
        (p,) = [p for p in pubs.values() if p["pmid"] == pmid]
        return p["paper_id"]

    def pilot(self, pids):
        with open(self.lit / "records" / "verification_pilot.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["paper_id", "authorised_by", "date"])
            w.writeheader()
            w.writerows({"paper_id": p, "authorised_by": "synthetic test", "date": "2026-10-31"} for p in pids)

    def add_crossref(self, pid, doi, body, name=None):
        """Register a synthetic Crossref response directly (as fetch_crossref would)."""
        name = name or f"CR_2026-10-31_{len(list((self.lit / 'raw_exports').glob('CR_*'))):03d}.json"
        (self.lit / "raw_exports" / name).write_bytes(body)
        pr.register_raw(self.lit, name, pr.VERIFY_PREFIX + pid, "crossref", pr.CROSSREF_ROUTE,
                        fc.API + doi, {"doi": doi, "paper_id": pid}, "2026-10-31T10:00:00+00:00", 1, False)
        return name

    def venue_map(self, rows):
        with open(self.lit / "records" / "venue_mappings.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(pr.VENUE_MAPPING_COLS))
            w.writeheader()
            w.writerows(rows)

    def digest(self, *names):
        return {n: hashlib.sha256((self.lit / "records" / n).read_bytes()).hexdigest()
                for n in names if (self.lit / "records" / n).exists()}


OUTPUTS = ("publications.jsonl", "source_records.jsonl", "publications_index.csv", "dedup_review.csv",
           "paper_id_registry.csv")


class TestPlanAndFetch(unittest.TestCase):
    """fetch_crossref.py: input checks, retries, failure handling (fake transport only)."""

    def setUp(self):
        patcher = mock.patch("urllib.request.urlopen", side_effect=no_network)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lit = Path(self.tmp.name)
        (self.lit / "raw_exports").mkdir()
        self.inv = [{"paper_id": "P0001", "doi": "https://doi.org/10.0000/X.1"},
                    {"paper_id": "P0002", "doi": "not-a-doi"},
                    {"paper_id": "P0003", "doi": None},
                    {"paper_id": "P0004", "doi": "10.0000/shared"},
                    {"paper_id": "P0005", "doi": "10.0000/SHARED"},
                    {"paper_id": "P0006", "doi": "10.0000/x.6"}]

    def test_doi_normalisation_and_input_problems(self):
        reqs, problems = fc.plan(["P0001", "P0006"], self.inv)
        self.assertEqual(reqs, [("P0001", "10.0000/x.1"), ("P0006", "10.0000/x.6")])
        self.assertEqual(problems, [])
        _, problems = fc.plan(["P0002", "P0003", "P0004", "P0009", "P0001", "P0001", ""], self.inv)
        text = " | ".join(problems)
        for expected in ("P0002: invalid DOI", "P0003: no DOI", "P0004: DOI 10.0000/shared is shared",
                         "P0009: not in the inventory", "P0001: listed more than once", "empty paper_id"):
            self.assertIn(expected, text)

    def test_any_input_problem_refuses_the_whole_run_before_any_request(self):
        t = FakeTransport({})
        report = fc.run(["P0001", "P0002"], "2026-10-31", self.lit, self.inv, t, sleep=lambda s: None, execute=True)
        self.assertTrue(report["refused"])
        self.assertEqual(t.urls, [])
        self.assertFalse((self.lit / "raw_exports" / "MANIFEST.csv").exists())

    def test_dry_run_makes_no_request(self):
        t = FakeTransport({})
        report = fc.run(["P0001"], "2026-10-31", self.lit, self.inv, t, sleep=lambda s: None)
        self.assertEqual([r["outcome"] for r in report["results"]], ["dry_run"])
        self.assertEqual(t.urls, [])

    def test_retries_only_on_429_5xx_and_transport_errors(self):
        u1, u6 = fc.API + "10.0000/x.1", fc.API + "10.0000/x.6"
        ok = crossref_body("10.0000/x.1", "SYNTHETIC one", "Alpha", "Synthetic Journal A")
        sleeps = []
        t = FakeTransport({u1: [(429, b""), (200, ok)], u6: [(404, b"not found")]})
        report = fc.run(["P0001", "P0006"], "2026-10-31", self.lit, self.inv, t, sleep=sleeps.append, execute=True)
        r1, r6 = report["results"]
        self.assertEqual((r1["outcome"], r1["attempts"]), ("saved", 2))
        self.assertEqual((r6["outcome"], r6["attempts"], r6["http_status"]), ("failed", 1, 404))
        self.assertEqual(t.urls, [u1, u1, u6])
        self.assertTrue(sleeps)                      # backoff and pacing go through the injected sleep

    def test_failures_write_no_raw_file_and_no_manifest_row(self):
        u1, u6 = fc.API + "10.0000/x.1", fc.API + "10.0000/x.6"
        t = FakeTransport({u1: [(500, b""), (503, b""), (502, b"")],
                           u6: [TimeoutError("timed out"), OSError("reset"), TimeoutError("timed out")]})
        report = fc.run(["P0001", "P0006"], "2026-10-31", self.lit, self.inv, t, sleep=lambda s: None, execute=True)
        self.assertEqual([(r["outcome"], r["attempts"]) for r in report["results"]], [("failed", 3), ("failed", 3)])
        self.assertIn("TimeoutError", report["results"][1]["error"])
        self.assertEqual(list((self.lit / "raw_exports").glob("CR_*")), [])
        self.assertFalse((self.lit / "raw_exports" / "MANIFEST.csv").exists())

    def test_malformed_responses_are_not_saved(self):
        u1 = fc.API + "10.0000/x.1"
        cases = [b"<html>not json</html>", json.dumps({"status": "ok"}).encode(),
                 json.dumps({"message": {"title": ["no DOI"]}}).encode(),
                 crossref_body("10.0000/other", "SYNTHETIC one", "Alpha", "Synthetic Journal A")]
        for body in cases:
            with self.subTest(body=body[:40]):
                t = FakeTransport({u1: [(200, body)]})
                report = fc.run(["P0001"], "2026-10-31", self.lit, self.inv, t, sleep=lambda s: None, execute=True)
                self.assertEqual(report["results"][0]["outcome"], "malformed")
                self.assertEqual(list((self.lit / "raw_exports").glob("CR_*")), [])
                self.assertFalse((self.lit / "raw_exports" / "MANIFEST.csv").exists())

    def test_successful_response_is_saved_verbatim_with_manifest_provenance(self):
        u1 = fc.API + "10.0000/x.1"
        body = crossref_body("10.0000/x.1", "SYNTHETIC one", "Alpha", "Synthetic Journal A")
        t = FakeTransport({u1: [(200, body)]})
        fc.run(["P0001"], "2026-10-31", self.lit, self.inv, t, sleep=lambda s: None, execute=True)
        raw = self.lit / "raw_exports" / "CR_2026-10-31_000.json"
        self.assertEqual(raw.read_bytes(), body)
        (row,) = pr.read_manifest(self.lit)
        self.assertEqual(row["sha256"], hashlib.sha256(body).hexdigest())
        self.assertEqual((row["query_id"], row["source"], row["route"], row["endpoint_or_tool"]),
                         ("VERIFY-CR-P0001", "crossref", "crossref_works", u1))
        self.assertEqual(json.loads(row["request_json"]), {"doi": "10.0000/x.1", "paper_id": "P0001"})
        self.assertEqual((row["transcribed"], row["transcription_check"]), ("no", "not_applicable"))
        self.assertRegex(row["retrieved_at"], r"^\d{4}-\d\d-\d\dT")

    def test_existing_run_files_are_never_overwritten(self):
        # an unregistered file left by an earlier run keeps its bytes; the new file takes the next number
        old = self.lit / "raw_exports" / "CR_2026-10-31_000.json"
        old.write_bytes(b"{}")
        u1 = fc.API + "10.0000/x.1"
        body = crossref_body("10.0000/x.1", "SYNTHETIC one", "Alpha", "Synthetic Journal A")
        report = fc.run(["P0001"], "2026-10-31", self.lit, self.inv, FakeTransport({u1: [(200, body)]}),
                        sleep=lambda s: None, execute=True)
        self.assertEqual(old.read_bytes(), b"{}")
        self.assertEqual(report["results"][0]["raw_file"], "CR_2026-10-31_001.json")
        self.assertEqual(report["orphans_before"], ["CR_2026-10-31_000.json"])
        self.assertEqual(report["orphans"], ["CR_2026-10-31_000.json"])     # reported, never deleted


class TestParser(unittest.TestCase):
    def test_year_is_empty_until_the_rule_is_decided(self):
        self.assertIsNone(pr.CROSSREF_YEAR_FIELDS)
        msg = json.loads(crossref_body("10.0000/cr.1", "T", "Alpha", "J", year=2021))["message"]
        self.assertIsNone(pr.parse_crossref_work(msg)["year"])
        self.assertEqual(pr.crossref_year(msg, ("published-print",)), 2021)

    def test_first_author_by_sequence_and_markup_stripped(self):
        msg = {"DOI": "10.0000/cr.1", "title": ["SYNTHETIC <i>marked</i> title"], "container-title": ["J"],
               "author": [{"family": "Zeta", "sequence": "additional"}, {"family": "Alpha", "sequence": "first"}]}
        m = pr.parse_crossref_work(msg)
        self.assertEqual(m["authors"][0]["last_name"], "Alpha")
        self.assertEqual(m["title"], "SYNTHETIC marked title")
        self.assertIsNone(m["abstract"])
        self.assertEqual(m["publication_types"], [])

    def test_malformed_message_raises(self):
        for msg in (None, [], {"title": ["no DOI"]}, {"DOI": "not a doi"}):
            with self.subTest(msg=msg), self.assertRaises(ValueError):
                pr.parse_crossref_work(msg)

    def test_crossref_api_record_is_independent_of_pubmed(self):
        a = {"source": "pubmed", "route": "pubmed_connector", "transcribed": False,
             "transcription_check": "not_applicable", "source_url": None, "original": {}}
        c = {"source": "crossref", "route": "crossref_api", "transcribed": False,
             "transcription_check": "not_applicable", "source_url": None, "original": {},
             "authors": [{"last_name": "A"}], "year": None, "journal": "J"}
        self.assertEqual(pr.source_independence(a, c)[0], "independent")

    def test_crossref_record_is_never_the_authoritative_record(self):
        rec = pr.parse_crossref_work(json.loads(crossref_body("10.0000/cr.1", "T", "A", "J"))["message"])
        rec.update(source="crossref", route="crossref_api", metadata_missing=False, transcribed=False,
                   transcription_check="not_applicable", source_record_id="SR-X-00001")
        status, note = pr.auto_verification([rec], [])
        self.assertEqual(status, "unverified")
        self.assertIn("no authoritative index record", note)


class TestBuildSafeguards(unittest.TestCase):
    """pubrecords.build with Crossref verification records attached (synthetic fixture)."""

    def setUp(self):
        self.fx = CrossrefFixture()
        self.addCleanup(self.fx.tmp.cleanup)
        _, self.base = self.fx.build()
        self.base_digest = self.fx.digest(*OUTPUTS)
        self.p1 = self.fx.pid(self.base, "900000101")
        self.p2 = self.fx.pid(self.base, "900000102")
        self.p3 = self.fx.pid(self.base, "900000103")
        self.p4 = self.fx.pid(self.base, "900000104")

    def agreeing(self, **kw):
        args = dict(doi="10.0000/cr.1", title="SYNTHETIC crossref match target one", family="Alpha",
                    venue="Synthetic Journal A", year=2021)
        args.update(kw)
        return crossref_body(args.pop("doi"), **args)

    def assert_build_refused(self):
        with self.assertRaises(RuntimeError):
            self.fx.build()
        self.assertEqual(self.fx.digest(*OUTPUTS), self.base_digest)   # nothing written

    def test_base_fixture_starts_partially_verified(self):
        self.assertEqual(self.base[self.p1]["verification_status"], "partially_verified")

    def test_without_a_year_rule_crossref_cannot_verify(self):
        self.fx.pilot([self.p1])
        self.fx.add_crossref(self.p1, "10.0000/cr.1", self.agreeing())
        report, pubs = self.fx.build()
        self.assertEqual(pubs[self.p1]["verification_status"], "partially_verified")
        self.assertIn("crossref lacks year", pubs[self.p1]["verification_note"])
        self.assertIsNone(report["crossref_verification"]["year_fields"])

    def test_full_agreement_verifies_with_a_test_only_year_rule(self):
        self.fx.pilot([self.p1])
        self.fx.add_crossref(self.p1, "10.0000/cr.1", self.agreeing())
        with mock.patch.object(pr, "CROSSREF_YEAR_FIELDS", TEST_YEAR_RULE):
            _, pubs = self.fx.build()
        self.assertEqual(pubs[self.p1]["verification_status"], "verified")
        self.assertIn("crossref", pubs[self.p1]["verification_note"])

    def test_conflicting_crossref_metadata_gives_needs_review(self):
        cases = {"title": dict(title="SYNTHETIC entirely different title"), "year": dict(year=2019),
                 "first_author": dict(family="Omega")}
        for field, kw in cases.items():
            with self.subTest(field=field):
                fx = CrossrefFixture()
                self.addCleanup(fx.tmp.cleanup)
                _, base = fx.build()
                p1 = fx.pid(base, "900000101")
                fx.pilot([p1])
                fx.add_crossref(p1, "10.0000/cr.1", self.agreeing(**kw))
                with mock.patch.object(pr, "CROSSREF_YEAR_FIELDS", TEST_YEAR_RULE):
                    _, pubs = fx.build()
                self.assertEqual(pubs[p1]["verification_status"], "needs_review")
                self.assertIn(field, pubs[p1]["verification_note"])

    def test_incomplete_crossref_metadata_stays_partially_verified(self):
        self.fx.pilot([self.p1])
        self.fx.add_crossref(self.p1, "10.0000/cr.1", self.agreeing(family=None, venue=None))
        with mock.patch.object(pr, "CROSSREF_YEAR_FIELDS", TEST_YEAR_RULE):
            _, pubs = self.fx.build()
        self.assertEqual(pubs[self.p1]["verification_status"], "partially_verified")
        self.assertIn("lacks", pubs[self.p1]["verification_note"])

    def test_venue_needs_an_explicit_reviewed_mapping(self):
        body = self.agreeing(venue="Synthetic Journal A : official journal of synthetic tests")
        self.fx.pilot([self.p1])
        self.fx.add_crossref(self.p1, "10.0000/cr.1", body)
        with mock.patch.object(pr, "CROSSREF_YEAR_FIELDS", TEST_YEAR_RULE):
            _, pubs = self.fx.build()
            self.assertEqual(pubs[self.p1]["verification_status"], "needs_review")
            self.assertIn("venue", pubs[self.p1]["verification_note"])
            # a near-identical but unlisted mapping does not count (no fuzzy matching)
            self.fx.venue_map([{"authoritative_venue": "Synthetic Journal A",
                                "second_source_venue": "Synthetic Journal A : official journal of synthetic test",
                                "basis": "synthetic", "reviewer": "synthetic test", "date": "2026-10-31"}])
            _, pubs = self.fx.build()
            self.assertEqual(pubs[self.p1]["verification_status"], "needs_review")
            self.fx.venue_map([{"authoritative_venue": "Synthetic Journal A",
                                "second_source_venue": "Synthetic Journal A : official journal of synthetic tests",
                                "basis": "synthetic", "reviewer": "synthetic test", "date": "2026-10-31"}])
            report, pubs = self.fx.build()
        self.assertEqual(pubs[self.p1]["verification_status"], "verified")
        self.assertEqual(report["crossref_verification"]["venue_mappings"], 1)

    def test_incomplete_or_duplicate_venue_mapping_rows_stop_the_build(self):
        good = {"authoritative_venue": "A", "second_source_venue": "B", "basis": "x", "reviewer": "y", "date": "z"}
        for rows in ([{**good, "reviewer": ""}], [good, dict(good)], [{**good, "second_source_venue": "a"}]):
            with self.subTest(rows=rows):
                self.fx.venue_map(rows)
                with self.assertRaises(ValueError):
                    pr.load_venue_mappings(self.fx.lit / "records")

    def test_unmatched_doi_stops_the_build_and_writes_nothing(self):
        self.fx.pilot([self.p1])
        self.fx.add_crossref(self.p1, "10.0000/cr.unknown", self.agreeing(doi="10.0000/cr.unknown"))
        self.assert_build_refused()

    def test_doi_of_two_publications_stops_the_build(self):
        self.fx.pilot([self.p4])
        self.fx.add_crossref(self.p4, "10.0000/cr.dup", self.agreeing(doi="10.0000/cr.dup"))
        self.assert_build_refused()

    def test_title_only_match_is_never_attached(self):
        # same title, author, venue and year as the DOI-less PubMed record three, but a DOI it lacks
        self.fx.pilot([self.p3])
        body = crossref_body("10.0000/cr.3", "SYNTHETIC title only target three", "Gamma", "Synthetic Journal C", 2022)
        self.fx.add_crossref(self.p3, "10.0000/cr.3", body)
        self.assert_build_refused()

    def test_paper_outside_the_pilot_stops_the_build(self):
        self.fx.pilot([self.p2])
        self.fx.add_crossref(self.p1, "10.0000/cr.1", self.agreeing())
        self.assert_build_refused()

    def test_doi_belonging_to_another_paper_stops_the_build(self):
        self.fx.pilot([self.p1, self.p2])
        self.fx.add_crossref(self.p2, "10.0000/cr.1", self.agreeing())
        self.assert_build_refused()

    def test_route_is_reserved_for_verify_query_ids(self):
        name = "CR_2026-10-31_900.json"
        (self.fx.lit / "raw_exports" / name).write_bytes(self.agreeing())
        args = (self.fx.lit, name, "Q-TEST-CR", "crossref", pr.CROSSREF_ROUTE, fc.API,
                {"doi": "10.0000/cr.1", "paper_id": self.p1}, "2026-10-31T10:00:00+00:00", 1, False)
        with self.assertRaises(ValueError):                      # refused at registration
            pr.register_raw(*args)
        append_manifest_row(self.fx.lit, name, "Q-TEST-CR", pr.CROSSREF_ROUTE, self.p1)   # hand-edited manifest
        self.assert_build_refused()                               # and refused again by the build

    def test_publication_metadata_provenance_and_other_statuses_unchanged(self):
        self.fx.pilot([self.p1])
        self.fx.add_crossref(self.p1, "10.0000/cr.1", self.agreeing(venue="Synthetic Journal A (Crossref form)",
                                                                    title="SYNTHETIC crossref match target one"))
        with mock.patch.object(pr, "CROSSREF_YEAR_FIELDS", TEST_YEAR_RULE):
            report, pubs = self.fx.build()
        self.assertEqual(set(pubs), set(self.base))                     # no new or removed paper IDs
        self.assertEqual(self.fx.digest("paper_id_registry.csv"),
                         {"paper_id_registry.csv": self.base_digest["paper_id_registry.csv"]})
        status_fields = {"verification_status", "verification_note"}
        for pid, before in self.base.items():
            after = pubs[pid]
            if pid == self.p1:
                self.assertEqual({k: v for k, v in before.items() if k not in status_fields},
                                 {k: v for k, v in after.items() if k not in status_fields})
            else:
                self.assertEqual(before, after)
        p = pubs[self.p1]
        self.assertEqual(p["journal"], "Synthetic Journal A")            # never overridden
        self.assertEqual(p["source_databases"], ["pubmed"])
        self.assertEqual({s["query_id"] for s in p["search_provenance"]}, {"Q-TEST-CR"})
        self.assertEqual([c["paper_id"] for c in report["verification_status_changes"]["changed"]], [self.p1])
        with open(self.fx.lit / "records" / "publications_index.csv", newline="") as f:
            (row,) = [r for r in csv.DictReader(f) if r["paper_id"] == self.p1]
        self.assertEqual(row["query_ids"], "Q-TEST-CR")
        self.assertEqual(row["source_databases"], "pubmed")

    def test_builds_from_the_same_raw_inputs_are_byte_identical(self):
        self.fx.pilot([self.p1])
        self.fx.add_crossref(self.p1, "10.0000/cr.1", self.agreeing())
        with mock.patch.object(pr, "CROSSREF_YEAR_FIELDS", TEST_YEAR_RULE):
            r1, _ = self.fx.build()
            d1 = self.fx.digest(*OUTPUTS)
            r2, _ = self.fx.build()
            d2 = self.fx.digest(*OUTPUTS)
        self.assertEqual(d1, d2)
        strip = lambda r: {k: v for k, v in r.items() if k not in ("built_at", "verification_status_changes")}
        self.assertEqual(strip(r1), strip(r2))

    def test_reports_keep_verification_lookups_out_of_searches_and_inventory(self):
        import shutil
        import make_literature_reports as mlr
        from test_pubrecords import REPO
        shutil.copytree(REPO / "research" / "literature" / "schemas", self.fx.lit / "schemas")
        mlr.main(["--lit-dir", str(self.fx.lit)])
        inv_before = json.loads((self.fx.lit / "paper_inventory.json").read_text())
        stats_before = json.loads((self.fx.lit / "records" / "collection_stats.json").read_text())
        self.fx.pilot([self.p1])
        self.fx.add_crossref(self.p1, "10.0000/cr.1", self.agreeing())
        self.fx.build()
        mlr.main(["--lit-dir", str(self.fx.lit)])
        inv_after = json.loads((self.fx.lit / "paper_inventory.json").read_text())
        keep = ("query_ids", "source_db", "retrieved_on", "venue", "year", "title", "doi", "publication_type")
        for b, a in zip(inv_before, inv_after):
            self.assertEqual({k: b[k] for k in keep}, {k: a[k] for k in keep})
        stats_after = json.loads((self.fx.lit / "records" / "collection_stats.json").read_text())
        self.assertNotIn("crossref", stats_after["raw_by_source"])
        self.assertEqual(stats_before["raw_by_source"], stats_after["raw_by_source"])
        register = (self.fx.lit / "search_execution_register.md").read_text()
        self.assertNotIn(f"| {pr.VERIFY_PREFIX}", register)                # not listed as a search
        self.assertIn("Second-source verification lookups (not searches): 1 Crossref", register)

    def test_without_verification_files_the_build_is_unchanged(self):
        _, pubs = self.fx.build()
        self.assertEqual(self.fx.digest(*OUTPUTS), self.base_digest)
        report = json.loads((self.fx.lit / "records" / "build_report.json").read_text())
        self.assertNotIn("crossref_verification", report)


if __name__ == "__main__":
    unittest.main()
