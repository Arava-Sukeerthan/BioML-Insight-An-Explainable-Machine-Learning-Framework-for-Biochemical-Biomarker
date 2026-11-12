"""Tests for scripts/literature/register_crossref_exports.py (Q-099 workflow). SYNTHETIC fixtures in
temporary directories only; the real manifest is never touched."""
import csv
import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "literature"))
sys.path.insert(0, str(REPO / "tests" / "literature"))
import pubrecords as pr  # noqa: E402
import register_crossref_exports as RG  # noqa: E402
from test_crossref_export_check import NOW, Package  # noqa: E402

RULE = ("published-print", "published-online")


class Registration(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lit = Path(self.tmp.name)
        (self.lit / "paper_inventory.json").write_text(json.dumps([{"paper_id": "P0001", "doi": "10.0000/x.1"}]))
        self.pkg = Package()
        self.addCleanup(self.pkg.tmp.cleanup)
        self.pkg.dir = self.lit / "raw_exports"
        self.pkg.dir.mkdir()
        self.pkg.add()
        self.pkg.check()                      # writes provenance.csv

    def plan(self, **kw):
        return RG.plan(self.lit, kw.get("package", self.lit / "raw_exports"), kw.get("auth", "D-999"), now=NOW)

    def test_refused_without_year_rule_or_authorisation(self):
        with mock.patch.object(pr, "CROSSREF_YEAR_FIELDS", None):
            with self.assertRaisesRegex(RG.RegistrationError, "Q-098"):
                self.plan()
        with mock.patch.object(pr, "CROSSREF_YEAR_FIELDS", RULE):
            with self.assertRaisesRegex(RG.RegistrationError, "authorisation"):
                self.plan(auth=" ")

    def test_refused_outside_raw_exports_and_on_failed_check(self):
        with mock.patch.object(pr, "CROSSREF_YEAR_FIELDS", RULE):
            with self.assertRaisesRegex(RG.RegistrationError, "raw_exports"):
                self.plan(package=self.lit)
            (self.lit / "raw_exports" / "CR_0.json").write_bytes(b"{}")      # body altered after export
            with self.assertRaisesRegex(RG.RegistrationError, "export check failed"):
                self.plan()

    def test_registers_with_provenance_and_never_twice(self):
        with mock.patch.object(pr, "CROSSREF_YEAR_FIELDS", RULE):
            entries = self.plan()
            self.assertFalse((self.lit / "raw_exports" / "MANIFEST.csv").exists())   # plan writes nothing
            RG.register(self.lit, entries)
            (row,) = pr.read_manifest(self.lit)
            self.assertEqual((row["query_id"], row["route"], row["source"]), ("VERIFY-CR-P0001", "crossref_works", "crossref"))
            self.assertTrue(row["endpoint_or_tool"].startswith("researcher export (curl 8.x)"))
            req = json.loads(row["request_json"])
            self.assertEqual(req["exported_by"], "researcher")
            self.assertEqual(len(req["headers_sha256"]), 64)
            self.assertIn("authorisation D-999", row["notes"])
            with self.assertRaisesRegex(RG.RegistrationError, "already registered"):
                self.plan()


if __name__ == "__main__":
    unittest.main()
