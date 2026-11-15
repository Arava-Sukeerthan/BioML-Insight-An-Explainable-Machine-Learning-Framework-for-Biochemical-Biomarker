"""Tests for scripts/literature/crossref_export_check.py (Q-099 proposal). SYNTHETIC fixtures only:
fake DOIs (10.0000/...), fake paper IDs, temporary directories. Nothing is registered."""
import csv
import datetime as dt
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "literature"))
import crossref_export_check as X  # noqa: E402

NOW = dt.datetime(2026, 11, 12, 12, 0, tzinfo=dt.timezone.utc)
HEADERS = "HTTP/1.1 200 Connection established\r\n\r\nHTTP/2 200\r\ndate: Thu, 12 Nov 2026 10:00:00 GMT\r\ncontent-type: application/json\r\n"


def body(doi, **extra):
    msg = {"DOI": doi, "title": ["SYNTHETIC title"], "container-title": ["Synthetic Journal"],
           "author": [{"family": "Alpha", "given": "T", "sequence": "first"}]}
    msg.update(extra)
    return json.dumps({"status": "ok", "message-type": "work", "message": msg}).encode()


class Package:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.rows = []

    def add(self, doi="10.0000/x.1", pid="P0001", content=None, headers=HEADERS, **override):
        n = len(self.rows)
        content = body(doi) if content is None else content
        (self.dir / f"CR_{n}.json").write_bytes(content)
        (self.dir / f"CR_{n}.headers.txt").write_text(headers, encoding="latin-1")
        row = {"file": f"CR_{n}.json", "headers_file": f"CR_{n}.headers.txt", "doi": doi, "paper_id": pid,
               "url": X.API + doi.lower(), "retrieved_at_utc": "2026-11-12T10:00:00+00:00",
               "tool": "curl 8.x", "exported_by": "researcher", "sha256": hashlib.sha256(content).hexdigest()}
        row.update(override)
        self.rows.append(row)
        return self

    def check(self, **kw):
        with open(self.dir / "provenance.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=X.PROVENANCE_COLS)
            w.writeheader()
            w.writerows(self.rows)
        return X.check_package(self.dir, now=NOW, **kw)


class ExportCheck(unittest.TestCase):
    def setUp(self):
        self.p = Package()
        self.addCleanup(self.p.tmp.cleanup)

    def problems(self, rep):
        return [q for r in rep["rows"] for q in r["problems"]]

    def test_well_formed_export_is_accepted_and_nothing_is_written(self):
        self.p.add()
        rep = self.p.check()
        before = {x.name: x.read_bytes() for x in self.p.dir.iterdir()}
        self.assertEqual(rep["status"], "accepted", rep)
        X.check_package(self.p.dir, now=NOW)
        self.assertEqual({x.name: x.read_bytes() for x in self.p.dir.iterdir()}, before)   # read-only

    def test_altered_body_is_rejected(self):
        self.p.add()
        (self.p.dir / "CR_0.json").write_bytes(body("10.0000/x.1", title=["changed"]))
        self.assertIn("SHA-256 of the body differs from the recorded value", self.problems(self.p.check()))

    def test_doi_mismatch_wrong_url_and_bad_time_are_rejected(self):
        content = body("10.0000/other")
        rep = self.p.add(content=content, url="https://doi.org/10.0000/x.1",
                         retrieved_at_utc="2026-11-12T10:00:00").check()
        probs = self.problems(rep)
        self.assertIn("DOI in the response differs from the requested DOI", probs)
        self.assertIn("url is not the Crossref works URL of the normalised DOI", probs)
        self.assertIn("retrieved_at_utc has no explicit UTC offset", probs)

    def test_future_time_missing_fields_and_bad_ids(self):
        rep = self.p.add(pid="X1", retrieved_at_utc="2027-01-01T00:00:00+00:00", tool="", exported_by=" ").check()
        probs = self.problems(rep)
        for p in ("paper_id is not of the form P####", "retrieved_at_utc is in the future", "tool is empty",
                  "exported_by is empty"):
            self.assertIn(p, probs)

    def test_header_status_and_date_required(self):
        rep = self.p.add(headers="HTTP/2 404\r\ndate: x\r\n").add("10.0000/x.2", "P0002", headers="HTTP/2 200\r\n").check()
        probs = self.problems(rep)
        self.assertTrue(any(p.startswith("final HTTP status is not 200") for p in probs))
        self.assertIn("header file has no Date header", probs)

    def test_malformed_body_and_duplicates(self):
        rep = self.p.add(content=b"{not json").add("10.0000/X.1", "P0001").check()
        probs = self.problems(rep)
        self.assertTrue(any(p.startswith("body is not a well-formed Crossref work response") for p in probs))
        self.assertIn("DOI listed more than once", probs)
        self.assertIn("paper_id listed more than once", probs)

    def test_inventory_doi_must_match(self):
        inv = self.p.dir / "inv.json"
        inv.write_text(json.dumps([{"paper_id": "P0001", "doi": "10.0000/x.9"}]), encoding="utf-8")
        rep = self.p.add().check(inventory=inv)
        self.assertIn("inventory DOI of this paper differs from the requested DOI", self.problems(rep))

    def test_missing_or_malformed_provenance_is_refused(self):
        self.assertEqual(X.check_package(self.p.dir, now=NOW)["status"], "refused")
        (self.p.dir / "provenance.csv").write_text("file,doi\nx,y\n", encoding="utf-8")
        self.assertEqual(X.check_package(self.p.dir, now=NOW)["status"], "refused")


if __name__ == "__main__":
    unittest.main()
