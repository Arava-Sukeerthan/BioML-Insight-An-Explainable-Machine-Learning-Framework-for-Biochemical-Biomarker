"""Regression tests for LIT-004-WORKFLOW-FIXES: stable IDs for records without identifier and
year (B-1), one screening-record format (B-3) and screening-status persistence (B-4).

ALL FIXTURE RECORDS IN THIS FILE ARE SYNTHETIC SOFTWARE-TEST DATA (titles start with
"SYNTHETIC", URLs use example.org, PMIDs 9000000xx, DOI prefix 10.0000). They are not real
publications and must never be copied into research records.

Run from the repository root:
    python3 -I -m unittest discover -s tests/literature -v
"""
import csv
import json
import shutil
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_pubrecords import REPO, Fixture, write_json, pr  # noqa: E402
import make_literature_reports as mlr  # noqa: E402

WEB_QUERY = {"query_id": "Q-TEST-WS", "row_type": "planned", "source": "web",
             "query_string": "synthetic web query"}


def web_rows(*titles_urls):
    return {"records": [{"title": t, "url": u} for t, u in titles_urls]}


class WebFixture(Fixture):
    """Standard synthetic fixture plus web-search records that have no identifier and no year."""

    def __init__(self):
        super().__init__()
        with open(self.lit / "search_queries.csv", "a", newline="") as f:
            csv.DictWriter(f, fieldnames=list(WEB_QUERY)).writerow(WEB_QUERY)
        shutil.copytree(REPO / "research" / "literature" / "schemas", self.lit / "schemas")
        self.standard()
        # two different web items with the SAME title and no year (cf. P2980/P2981)
        self.reg(write_json(self.lit, "Q-TEST-WS_2026-10-14.json", {}, web_rows(
            ("SYNTHETIC composition for treating a disorder", "https://example.org/patent/1"),
            ("SYNTHETIC web-only record without year", "https://example.org/web/2"),
            ("SYNTHETIC composition for treating a disorder", "https://example.org/patent/3"),
        )), "Q-TEST-WS", "web", "structured_transcription", 3)

    def build(self, today="2026-10-14"):
        return pr.build(self.lit, today=today)

    def pubs(self):
        with open(self.lit / "records" / "publications.jsonl") as f:
            return [json.loads(line) for line in f]

    def id_to_sources(self):
        return {p["paper_id"]: sorted(s["source_record_id"] for s in p["search_provenance"])
                for p in self.pubs()}

    def web_ids(self):
        return {p["source_urls"][0]: p["paper_id"] for p in self.pubs()
                if p["source_urls"] and "example.org/patent" in p["source_urls"][0]
                or p["source_urls"] and "example.org/web" in p["source_urls"][0]}

    def write_decisions(self, rows, header=None):
        header = header or pr.SCREENING_REQUIRED
        (self.lit / "screening").mkdir(exist_ok=True)
        with open(self.lit / "screening" / "decisions.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)

    def reports(self):
        return mlr.main(["--lit-dir", str(self.lit)])

    def inventory(self):
        with open(self.lit / "paper_inventory.json") as f:
            return {r["paper_id"]: r for r in json.load(f)}


class TestStableIds(unittest.TestCase):
    def setUp(self):
        self.fx = WebFixture()
        self.report = self.fx.build()

    def test_every_publication_has_a_registry_key(self):
        self.assertEqual(self.report["publications_without_stable_registry_key"], 0)
        for p in self.fx.pubs():
            if "example.org/patent" in (p["source_urls"] or [""])[0]:
                self.assertIsNone(p["year"])

    def test_repeated_builds_keep_ids(self):
        first = self.fx.id_to_sources()
        for day in ("2026-10-15", "2026-10-16"):
            self.fx.build(today=day)
            self.assertEqual(self.fx.id_to_sources(), first)

    def test_ids_kept_when_new_records_arrive(self):
        first = self.fx.id_to_sources()
        # a new web search returns new no-year items, including a third same-title item; it sorts
        # before the old file and would have shifted the old IDs under the LIT-003 scheme
        self.fx.reg(write_json(self.fx.lit, "Q-TEST-WS_2026-10-01.json", {}, web_rows(
            ("SYNTHETIC composition for treating a disorder", "https://example.org/patent/9"),
            ("SYNTHETIC another web-only record", "https://example.org/web/8"),
        )), "Q-TEST-WS", "web", "structured_transcription", 2)
        self.fx.build(today="2026-10-15")
        after = self.fx.id_to_sources()
        for pid, srcs in first.items():
            self.assertEqual(after[pid], srcs, pid)
        self.assertEqual(len(after), len(first) + 2)

    def test_same_title_no_year_records_get_distinct_ids_and_stay_flagged(self):
        pats = [p for p in self.fx.pubs() if "composition for treating" in p["title"]]
        self.assertEqual(len(pats), 2)
        self.assertNotEqual(pats[0]["paper_id"], pats[1]["paper_id"])
        for p in pats:   # flagged for a manual decision, never merged automatically
            self.assertEqual(p["n_source_records"], 1)
            self.assertEqual(p["duplicate_status"], "possible_duplicate_review")
        keys = [pr.record_keys({"source_record_id": s["source_record_id"], "title": p["title"]})
                for p in pats for s in p["search_provenance"]]
        self.assertEqual(len({k for ks in keys for k in ks}), 2)   # no key collision

    def test_identifier_records_do_not_get_fallback_keys(self):
        self.assertEqual(pr.record_keys({"pmid": "900000001", "source_record_id": "SR-x-00001"}),
                         ["pmid:900000001"])
        self.assertEqual(pr.record_keys({"title": "SYNTHETIC t", "year": 2020, "source_record_id": "SR-x"}),
                         ["title:synthetic t|2020"])
        self.assertEqual(pr.record_keys({"title": "SYNTHETIC t", "source_record_id": "SR-x-00002"}),
                         ["source_record:SR-x-00002"])

    def test_screening_decision_follows_its_record_after_new_data(self):
        pid = self.fx.web_ids()["https://example.org/web/2"]
        self.fx.write_decisions([[pid, "title_abstract", "uncertain", "", "assistant", "2026-10-15", "test"]])
        self.fx.reg(write_json(self.fx.lit, "Q-TEST-WS_2026-10-02.json", {}, web_rows(
            ("SYNTHETIC yet another web-only record", "https://example.org/web/7"),
        )), "Q-TEST-WS", "web", "structured_transcription", 1)
        self.fx.build(today="2026-10-16")
        (p,) = [p for p in self.fx.pubs() if p["paper_id"] == pid]
        self.assertEqual(p["source_urls"], ["https://example.org/web/2"])
        self.assertEqual(p["screening_decision"], "uncertain")


class TestMigration(unittest.TestCase):
    def test_migration_keeps_existing_ids(self):
        fx = WebFixture()
        fx.build()
        # simulate a LIT-003-era registry: drop the fallback keys, as the old code never wrote them
        reg = fx.lit / "records" / "paper_id_registry.csv"
        rows = list(csv.DictReader(open(reg, newline="")))
        old = [r for r in rows if not r["key"].startswith("source_record:")]
        with open(reg, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["key", "paper_id", "first_seen"])
            w.writeheader()
            w.writerows(old)
        before = fx.id_to_sources()
        mapping = pr.migrate_fallback_keys(fx.lit, today="2026-10-15")
        self.assertEqual(len(mapping), 3)
        self.assertTrue(all(m["paper_id_before"] == m["paper_id_after"] for m in mapping))
        self.assertEqual(pr.migrate_fallback_keys(fx.lit, today="2026-10-16"), [])   # idempotent
        fx.build(today="2026-10-16")
        self.assertEqual(fx.id_to_sources(), before)

    def test_migration_refuses_collision(self):
        fx = WebFixture()
        fx.build()
        reg = fx.lit / "records" / "paper_id_registry.csv"
        rows = list(csv.DictReader(open(reg, newline="")))
        fb = [r for r in rows if r["key"].startswith("source_record:")]
        rest = [r for r in rows if not r["key"].startswith("source_record:")]
        fb[0]["paper_id"] = "P9999"            # registry already maps the key elsewhere
        with open(reg, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["key", "paper_id", "first_seen"])
            w.writeheader()
            w.writerows(rest + fb)
        with self.assertRaises(ValueError):
            pr.migrate_fallback_keys(fx.lit, today="2026-10-15")


class TestScreeningRecords(unittest.TestCase):
    def setUp(self):
        self.fx = WebFixture()
        self.fx.build()
        self.ids = sorted(p["paper_id"] for p in self.fx.pubs())

    def status_of(self):
        return {p["paper_id"]: (p["screening_decision"], p["screening_stage"], p["exclusion_reason"])
                for p in self.fx.pubs()}

    def test_every_status_persists_into_publications_and_inventory(self):
        a, b, c, d = self.ids[:4]
        self.fx.write_decisions([
            [a, "title_abstract", "include", "", "assistant", "2026-10-15", ""],
            [b, "title_abstract", "exclude", "E3", "assistant", "2026-10-15", "no predictive model"],
            [c, "title_abstract", "uncertain", "", "assistant", "2026-10-15", "scope unclear"],
            [d, "full_text", "abstract_only", "", "assistant", "2026-10-15", ""],
        ])
        self.fx.build(today="2026-10-15")
        st = self.status_of()
        self.assertEqual(st[a], ("include", "title_abstract", None))
        self.assertEqual(st[b], ("exclude", "title_abstract", "E3"))
        self.assertEqual(st[c], ("uncertain", "title_abstract", None))
        self.assertEqual(st[d], ("abstract_only", "full_text", None))
        for pid in self.ids[4:]:
            self.assertEqual(st[pid], ("not_screened", None, None))
        self.fx.reports()
        inv = self.fx.inventory()
        self.assertEqual([inv[x]["screening_status"] for x in (a, b, c, d)],
                         ["include", "exclude", "uncertain", "abstract_only"])
        self.assertEqual(inv[b]["exclusion_reason"], "E3")
        self.assertEqual(inv[c]["screening_justification"], "scope unclear")
        self.assertIn("screening decision: uncertain", inv[c]["preliminary_relevance"])
        for pid in self.ids[4:]:
            self.assertEqual(inv[pid]["screening_status"], "not_screened")
            self.assertNotEqual(inv[pid]["screening_status"], "uncertain")
            self.assertTrue(inv[pid]["preliminary_relevance"].endswith("not screened"))
        with open(self.fx.lit / "paper_inventory.csv", newline="") as f:
            csv_status = {r["paper_id"]: r["screening_status"] for r in csv.DictReader(f)}
        self.assertEqual(csv_status[d], "abstract_only")
        stats = json.load(open(self.fx.lit / "records" / "collection_stats.json"))
        self.assertEqual(stats["screening_status"]["not_screened"], len(self.ids) - 4)

    def test_optional_descriptor_columns(self):
        a = self.ids[0]
        self.fx.write_decisions(
            [[a, "title_abstract", "include", "", "assistant", "2026-10-15", "", "RQ1;RQ3", "2", "",
              "original", "yes", "no", "unclear", "external", "v0.1", "no"]],
            header=pr.SCREENING_REQUIRED + ["rq_tags", "tier", "scope_flags", "record_type",
                                            "dim_explainability", "dim_uncertainty", "dim_calibration",
                                            "dim_independent_validation", "criteria_version", "needs_human"])
        self.fx.build(today="2026-10-15")
        self.fx.reports()
        row = self.fx.inventory()[a]
        self.assertEqual((row["rq_tags"], row["tier"], row["record_type"], row["dim_independent_validation"]),
                         ("RQ1;RQ3", 2, "original", "external"))

    def test_feature_selection_descriptor(self):
        # D-032: optional dim_feature_selection column (yes/no/unclear); files without it stay valid.
        # Title/abstract rows: a full-text row must record all component statuses (D-035, G5)
        a, b, c = self.ids[:3]
        header = pr.SCREENING_REQUIRED + ["dim_feature_selection"]
        self.fx.write_decisions([
            [a, "title_abstract", "include", "", "assistant", "2026-10-15", "", "yes"],
            [b, "title_abstract", "uncertain", "", "assistant", "2026-10-15", "selection not reported", "unclear"],
            [c, "title_abstract", "include", "", "assistant", "2026-10-15", "", ""],
        ], header=header)
        self.fx.build(today="2026-10-15")
        details = {p["paper_id"]: p["screening_details"] for p in self.fx.pubs()}
        self.assertEqual(details[a]["dim_feature_selection"], "yes")
        self.assertEqual(details[b]["dim_feature_selection"], "unclear")
        self.assertIsNone(details[c]["dim_feature_selection"])        # empty is not "no"
        self.fx.reports()
        inv = self.fx.inventory()
        self.assertEqual((inv[a]["dim_feature_selection"], inv[c]["dim_feature_selection"]), ("yes", None))
        for bad in ("maybe", "Yes", "true"):
            with self.subTest(bad):
                self.fx.write_decisions([[a, "title_abstract", "include", "", "assistant", "2026-10-15", "", bad]],
                                        header=header)
                with self.assertRaises(ValueError):
                    self.fx.build(today="2026-10-16")
        # unscreened records carry no component value
        self.assertTrue(all(details[p]["dim_feature_selection"] is None for p in (c,)))
        self.assertTrue(all(details.get(p) is None for p in self.ids[3:]))

    def test_latest_stage_wins(self):
        a = self.ids[0]
        self.fx.write_decisions([
            [a, "full_text", "exclude", "E5", "assistant", "2026-10-16", "full text: no biomarkers"],
            [a, "title_abstract", "include", "", "assistant", "2026-10-15", ""],
        ])
        self.fx.build(today="2026-10-16")
        self.assertEqual(self.status_of()[a], ("exclude", "full_text", "E5"))

    def test_invalid_rows_are_rejected(self):
        a = self.ids[0]
        ok = [a, "title_abstract", "include", "", "assistant", "2026-10-15", ""]
        bad = {
            "unknown decision": [a, "title_abstract", "maybe", "", "assistant", "2026-10-15", "x"],
            "old LIT-001 value": [a, "title_abstract", "included", "", "assistant", "2026-10-15", "x"],
            "exclude without code": [a, "title_abstract", "exclude", "", "assistant", "2026-10-15", "x"],
            "code on include": [a, "title_abstract", "include", "E3", "assistant", "2026-10-15", "x"],
            "code E13": [a, "title_abstract", "exclude", "E13", "assistant", "2026-10-15", "x"],
            "code E0": [a, "title_abstract", "exclude", "E0", "assistant", "2026-10-15", "x"],
            "bad stage": [a, "abstract", "include", "", "assistant", "2026-10-15", ""],
            "abstract_only at title_abstract": [a, "title_abstract", "abstract_only", "", "assistant", "2026-10-15", ""],
            "uncertain without justification": [a, "title_abstract", "uncertain", "", "assistant", "2026-10-15", ""],
            "bad date": [a, "title_abstract", "include", "", "assistant", "15/10/2026", ""],
            "empty screener": [a, "title_abstract", "include", "", "", "2026-10-15", ""],
            "bad paper id": ["2980", "title_abstract", "include", "", "assistant", "2026-10-15", ""],
            "explicit not_screened": [a, "title_abstract", "not_screened", "", "assistant", "2026-10-15", "x"],
        }
        for name, row in bad.items():
            with self.subTest(name):
                self.fx.write_decisions([ok, row])
                with self.assertRaises(ValueError):
                    self.fx.build(today="2026-10-15")
        with self.subTest("unknown column"):
            self.fx.write_decisions([ok + ["x"]], header=pr.SCREENING_REQUIRED + ["record_id"])
            with self.assertRaises(ValueError):
                self.fx.build(today="2026-10-15")
        with self.subTest("missing column"):
            self.fx.write_decisions([ok[:-1]], header=pr.SCREENING_REQUIRED[:-1])
            with self.assertRaises(ValueError):
                self.fx.build(today="2026-10-15")
        with self.subTest("bad rq tag"):
            self.fx.write_decisions([ok + ["RQ7"]], header=pr.SCREENING_REQUIRED + ["rq_tags"])
            with self.assertRaises(ValueError):
                self.fx.build(today="2026-10-15")

    def test_rejected_input_leaves_previous_outputs_untouched(self):
        pubs = self.fx.lit / "records" / "publications.jsonl"
        before = pubs.read_bytes()
        self.fx.write_decisions([[self.ids[0], "title_abstract", "exclude", "", "assistant", "2026-10-15", "x"]])
        with self.assertRaises(ValueError):
            self.fx.build(today="2026-10-15")
        self.assertEqual(pubs.read_bytes(), before)

    def test_orphan_paper_id_raises_and_writes_nothing(self):
        pubs = self.fx.lit / "records" / "publications.jsonl"
        before = pubs.read_bytes()
        self.fx.write_decisions([["P9999", "title_abstract", "include", "", "assistant", "2026-10-15", ""]])
        with self.assertRaises(RuntimeError):
            self.fx.build(today="2026-10-15")
        self.assertEqual(pubs.read_bytes(), before)


class TestSchemaConsistency(unittest.TestCase):
    def setUp(self):
        sdir = REPO / "research" / "literature" / "schemas"
        self.sd = json.load(open(sdir / "screening_decision.schema.json"))
        self.inv = json.load(open(sdir / "paper_inventory.schema.json"))

    def test_screening_schema_matches_code(self):
        self.assertEqual(self.sd["required"], pr.SCREENING_REQUIRED)
        self.assertEqual(self.sd["x-column-order"], pr.SCREENING_REQUIRED + pr.SCREENING_OPTIONAL)
        self.assertEqual(set(self.sd["properties"]), set(pr.SCREENING_REQUIRED + pr.SCREENING_OPTIONAL))
        for col, values in pr.SCREENING_ENUMS.items():
            with self.subTest(col):
                self.assertEqual(tuple(self.sd["properties"][col]["enum"]), tuple(values))

    def test_inventory_status_enum_matches_code(self):
        status = self.inv["items"]["properties"]["screening_status"]["enum"]
        self.assertEqual(status, ["not_screened", *pr.SCREENING_DECISIONS])
        self.assertEqual(set(self.inv["items"]["properties"]["screening_stage"]["enum"]) - {None},
                         set(pr.SCREENING_ENUMS["stage"]))

    def test_inventory_columns_match_schema(self):
        self.assertEqual(set(mlr.INV_COLS), set(self.inv["items"]["properties"]))

    def test_publication_schema_accepts_screened_record(self):
        fx = WebFixture()
        fx.build()
        a = sorted(p["paper_id"] for p in fx.pubs())[0]
        fx.write_decisions([[a, "full_text", "abstract_only", "", "assistant", "2026-10-15", ""]])
        fx.build(today="2026-10-15")   # build validates every record against the schema


class TestInventoryRebuild(unittest.TestCase):
    def setUp(self):
        self.fx = WebFixture()
        self.fx.build()
        self.fx.reports()

    def test_manual_extraction_values_survive_rebuild(self):
        inv_path = self.fx.lit / "paper_inventory.json"
        inv = json.load(open(inv_path))
        inv[0]["disorder"] = "SYNTHETIC disorder (test)"
        inv[0]["extraction_status"] = "extracted"
        inv[0]["publication_type"] = "original_research"
        pid = inv[0]["paper_id"]
        json.dump(inv, open(inv_path, "w"))
        self.fx.build(today="2026-10-15")
        self.fx.reports()
        row = self.fx.inventory()[pid]
        self.assertEqual((row["disorder"], row["extraction_status"], row["publication_type"]),
                         ("SYNTHETIC disorder (test)", "extracted", "original_research"))
        self.assertEqual(row["models"], mlr.SENTINEL)
        stats = json.load(open(self.fx.lit / "records" / "collection_stats.json"))
        self.assertEqual(stats["manual_values_carried_forward"], 3)

    def test_manual_values_for_missing_paper_id_stop_the_report(self):
        inv_path = self.fx.lit / "paper_inventory.json"
        inv = json.load(open(inv_path))
        inv.append(dict(inv[0], paper_id="P9999", disorder="SYNTHETIC orphan (test)"))
        json.dump(inv, open(inv_path, "w"))
        before = inv_path.read_bytes()
        with self.assertRaises(SystemExit):
            self.fx.reports()
        self.assertEqual(inv_path.read_bytes(), before)

    def test_rebuild_is_deterministic(self):
        first = (self.fx.lit / "paper_inventory.csv").read_bytes()
        self.fx.build(today="2026-10-15")
        self.fx.reports()
        self.assertEqual((self.fx.lit / "paper_inventory.csv").read_bytes(), first)


class TestIntegrity(unittest.TestCase):
    """LIT-004-REVIEW-AND-DECISIONS: registry append-only, decisions stay attached, invalid input
    cannot erase manual annotations."""

    def setUp(self):
        self.fx = WebFixture()
        self.fx.build()
        self.fx.reports()
        self.reg = self.fx.lit / "records" / "paper_id_registry.csv"

    def test_registry_is_append_only(self):
        before = self.reg.read_bytes()
        self.fx.build(today="2026-10-15")
        self.assertEqual(self.reg.read_bytes(), before)              # no new data -> unchanged
        self.fx.reg(write_json(self.fx.lit, "Q-TEST-WS_2026-10-03.json", {}, web_rows(
            ("SYNTHETIC late web-only record", "https://example.org/web/6"),
        )), "Q-TEST-WS", "web", "structured_transcription", 1)
        self.fx.build(today="2026-10-16")
        pr.migrate_fallback_keys(self.fx.lit, today="2026-10-16")
        after = self.reg.read_bytes()
        self.assertTrue(after.startswith(before))
        self.assertGreater(len(after), len(before))

    def test_decisions_stay_attached_after_rebuilds(self):
        pubs = self.fx.pubs()
        dec = ["include", "exclude", "uncertain"]
        rows, expect = [], {}
        for i, p in enumerate(sorted(pubs, key=lambda p: p["paper_id"])):
            d = dec[i % 3]
            rows.append([p["paper_id"], "title_abstract", d, "E12" if d == "exclude" else "", "assistant",
                         "2026-10-15", "test" if d != "include" else ""])
            expect[p["paper_id"]] = (d, sorted(s["source_record_id"] for s in p["search_provenance"]))
        self.fx.write_decisions(rows)
        # new data merging into an existing record (900000003 again, another query) and a new record
        self.fx.reg(write_json(self.fx.lit, "Q-TEST-B_search_01.json", {}, {
            "pmids": ["900000003"], "total_count": 2}), "Q-TEST-B", "pubmed", "pubmed_connector_search", 1,
            request={"retstart": 1})
        self.fx.reg(write_json(self.fx.lit, "Q-TEST-WS_2026-10-04.json", {}, web_rows(
            ("SYNTHETIC composition for treating a disorder", "https://example.org/patent/5"),
        )), "Q-TEST-WS", "web", "structured_transcription", 1)
        for day in ("2026-10-16", "2026-10-17"):
            self.fx.build(today=day)
            got = {p["paper_id"]: p for p in self.fx.pubs()}
            for pid, (d, srcs) in expect.items():
                self.assertEqual(got[pid]["screening_decision"], d, pid)
                self.assertTrue(set(srcs) <= {s["source_record_id"] for s in got[pid]["search_provenance"]})
            new = [p for p in got.values() if p["paper_id"] not in expect]
            self.assertEqual([p["screening_decision"] for p in new], ["not_screened"])

    def _inv_with_manual(self):
        path = self.fx.lit / "paper_inventory.json"
        inv = json.load(open(path))
        inv[0]["disorder"] = "SYNTHETIC disorder (test)"
        inv[1]["notes"] = "SYNTHETIC manual note (test)"
        json.dump(inv, open(path, "w"))
        self.fx.reports()            # writes the CSV consistently
        return inv[0]["paper_id"], inv[1]["paper_id"]

    def test_manual_note_survives(self):
        a, b = self._inv_with_manual()
        self.fx.build(today="2026-10-15")
        self.fx.reports()
        inv = self.fx.inventory()
        self.assertEqual(inv[a]["disorder"], "SYNTHETIC disorder (test)")
        self.assertEqual(inv[b]["notes"], "SYNTHETIC manual note (test)")

    def test_invalid_screening_input_keeps_annotations(self):
        a, _ = self._inv_with_manual()
        self.fx.write_decisions([[a, "title_abstract", "excluded", "", "assistant", "2026-10-15", "x"]])
        with self.assertRaises(ValueError):
            self.fx.build(today="2026-10-15")
        self.fx.reports()            # runs on the previous, valid build
        self.assertEqual(self.fx.inventory()[a]["disorder"], "SYNTHETIC disorder (test)")
        self.assertEqual(self.fx.inventory()[a]["screening_status"], "not_screened")

    def test_invalid_manual_value_writes_nothing(self):
        import jsonschema
        path = self.fx.lit / "paper_inventory.json"
        inv = json.load(open(path))
        inv[0]["publication_type"] = "SYNTHETIC invalid type"
        json.dump(inv, open(path, "w"))
        before = path.read_bytes(), (self.fx.lit / "paper_inventory.csv").read_bytes()
        with self.assertRaises((jsonschema.ValidationError, SystemExit)):
            self.fx.reports()
        self.assertEqual((path.read_bytes(), (self.fx.lit / "paper_inventory.csv").read_bytes()), before)

    def test_csv_only_edit_is_not_overwritten(self):
        cpath = self.fx.lit / "paper_inventory.csv"
        with open(cpath, newline="") as f:
            rows = list(csv.DictReader(f))
        rows[0]["disorder"] = "SYNTHETIC edited in CSV (test)"
        with open(cpath, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=mlr.INV_COLS)
            w.writeheader()
            w.writerows(rows)
        before = cpath.read_bytes()
        with self.assertRaises(SystemExit):
            self.fx.reports()
        self.assertEqual(cpath.read_bytes(), before)

    def test_not_screened_and_uncertain_are_distinct_everywhere(self):
        ids = sorted(p["paper_id"] for p in self.fx.pubs())
        self.fx.write_decisions([[ids[0], "title_abstract", "uncertain", "", "assistant", "2026-10-15", "x"]])
        self.fx.build(today="2026-10-15")
        self.fx.reports()
        inv = self.fx.inventory()
        self.assertEqual(inv[ids[0]]["screening_status"], "uncertain")
        self.assertEqual({inv[i]["screening_status"] for i in ids[1:]}, {"not_screened"})
        idx = list(csv.DictReader(open(self.fx.lit / "records" / "publications_index.csv", newline="")))
        self.assertEqual({r["screening_decision"] for r in idx if r["paper_id"] != ids[0]}, {"not_screened"})
        self.assertNotIn("not_screened", pr.SCREENING_DECISIONS)   # cannot be written as a decision


class TestRQ5ComponentEvidence(unittest.TestCase):
    """D-035 (Q-041): preliminary vs confirmed component evidence, no silent erasure, completeness,
    researcher verification, and the D-034 coverage-group logic (not wired: Q-039)."""

    COMP = ["dim_feature_selection", "dim_explainability", "dim_calibration", "dim_uncertainty"]

    def setUp(self):
        self.fx = WebFixture()
        self.fx.build()
        self.ids = sorted(p["paper_id"] for p in self.fx.pubs())
        self.header = pr.SCREENING_REQUIRED + self.COMP

    def row(self, pid, stage, dec, screener, date, fs="", x="", c="", u="", why="test"):
        return [pid, stage, dec, "E3" if dec == "exclude" else "", screener, date, why, fs, x, c, u]

    def rq5(self, pid):
        return {p["paper_id"]: p for p in self.fx.pubs()}[pid]["rq5_components"]

    @staticmethod
    def five(fs, cl, x, c, u):
        return {"feature_selection": fs, "classification": cl, "explainability": x,
                "calibration": c, "uncertainty": u}

    # 1, 3
    def test_abstract_stage_yes_is_preliminary_only(self):
        a = self.ids[0]
        self.fx.write_decisions([self.row(a, "title_abstract", "include", "assistant", "2026-10-15",
                                          "yes", "yes", "", "")], header=self.header)
        self.fx.build(today="2026-10-15")
        ev = self.rq5(a)
        self.assertIsNone(ev["confirmed"])
        self.assertEqual(ev["preliminary"]["statuses"]["feature_selection"], "yes")
        self.assertIsNone(ev["preliminary"]["statuses"]["calibration"])     # missing is not "no"
        self.assertIsNone(ev["preliminary"]["statuses"]["classification"])  # no column (Q-039)

    # 2
    def test_full_text_needed_for_confirmation(self):
        a, b = self.ids[:2]
        self.fx.write_decisions([
            self.row(a, "title_abstract", "include", "assistant", "2026-10-15", "yes", "yes", "yes", "yes"),
            self.row(a, "full_text", "include", "assistant", "2026-10-16", "yes", "no", "unclear", "yes"),
            self.row(b, "title_abstract", "include", "assistant", "2026-10-15", "yes", "yes", "yes", "yes"),
            self.row(b, "full_text", "abstract_only", "assistant", "2026-10-16", "yes", "yes", "yes", "yes"),
        ], header=self.header)
        self.fx.build(today="2026-10-16")
        ea, eb = self.rq5(a), self.rq5(b)
        self.assertEqual(ea["confirmed"]["statuses"]["explainability"], "no")
        self.assertEqual(ea["preliminary"]["statuses"]["explainability"], "yes")   # kept, not overwritten
        self.assertIsNone(eb["confirmed"])                                            # no full text
        self.assertIn("abstract_only", eb["confirmation_note"])

    # 3
    def test_full_text_row_without_components_is_not_assessed(self):
        a = self.ids[0]
        self.fx.write_decisions([self.row(a, "full_text", "include", "assistant", "2026-10-16")],
                                header=self.header)
        self.fx.build(today="2026-10-16")
        ev = self.rq5(a)
        self.assertIsNone(ev["confirmed"])
        self.assertIn("not assessed", ev["confirmation_note"])

    # 4
    def test_incomplete_full_text_assessment_rejected(self):
        before = (self.fx.lit / "records" / "publications.jsonl").read_bytes()
        self.fx.write_decisions([self.row(self.ids[0], "full_text", "include", "assistant", "2026-10-16",
                                          "yes", "", "", "")], header=self.header)
        with self.assertRaises(ValueError):
            self.fx.build(today="2026-10-16")
        self.assertEqual((self.fx.lit / "records" / "publications.jsonl").read_bytes(), before)

    # 5
    def test_later_blank_row_cannot_erase(self):
        a = self.ids[0]
        for stage in ("full_text", "title_abstract"):
            with self.subTest(stage):
                self.fx.write_decisions([
                    self.row(a, stage, "include", "assistant", "2026-10-16", "yes", "yes", "no", "unclear"),
                    self.row(a, stage, "include", "assistant", "2026-10-17"),
                ], header=self.header)
                with self.assertRaises(ValueError):
                    self.fx.build(today="2026-10-17")
        # a full-text row without components does not erase title/abstract evidence (kept as preliminary)
        self.fx.write_decisions([
            self.row(a, "title_abstract", "include", "assistant", "2026-10-15", "yes", "", "", ""),
            self.row(a, "full_text", "include", "assistant", "2026-10-16"),
        ], header=self.header)
        self.fx.build(today="2026-10-16")
        self.assertEqual(self.rq5(a)["preliminary"]["statuses"]["feature_selection"], "yes")

    # 6, 7, 8, 9, 10
    def test_coverage_group_logic(self):
        g = pr.derive_rq5_coverage_group
        self.assertEqual(g(self.five("yes", "yes", "yes", "yes", "unclear")), ("qualified", True))
        self.assertEqual(g(self.five("yes", "yes", "yes", "yes", "no")), ("qualified", False))
        self.assertEqual(g(self.five("yes", "yes", "yes", "unclear", "unclear")), ("near_rq5", True))
        self.assertEqual(g(self.five("yes", "yes", "yes", "no", "no")), ("near_rq5", False))
        for n in range(3):
            vals = ["yes"] * n + ["no"] * (5 - n)
            with self.subTest(n_yes=n):
                self.assertEqual(g(self.five(*vals)), ("below_threshold", False))
        self.assertEqual(g(self.five("yes", "yes", "unclear", "unclear", "unclear"))[0], "below_threshold")
        # unclear (assessed) differs from not assessed
        self.assertEqual(g(self.five("yes", "yes", "yes", "yes", None)), (None, None))
        self.assertEqual(g(self.five("yes", "yes", "yes", "yes", "")), (None, None))
        self.assertEqual(g({}), (None, None))
        with self.assertRaises(ValueError):
            g(self.five("yes", "yes", "yes", "yes", "maybe"))

    def test_build_cannot_derive_group_without_classification(self):
        a = self.ids[0]
        self.fx.write_decisions([self.row(a, "full_text", "include", "assistant", "2026-10-16",
                                          "yes", "yes", "yes", "yes")], header=self.header)
        self.fx.build(today="2026-10-16")
        st = self.rq5(a)["confirmed"]["statuses"]
        self.assertIsNone(st["classification"])
        self.assertEqual(pr.derive_rq5_coverage_group(st), (None, None))     # Q-039 blocks derivation
        for p in self.fx.pubs():                                              # unassessed: nothing
            if p["paper_id"] != a:
                self.assertIsNone(p["rq5_components"])

    # 11
    def test_researcher_verification_keeps_audit_trail(self):
        a, b = self.ids[:2]
        self.fx.write_decisions([
            self.row(a, "full_text", "include", "assistant", "2026-10-16", "yes", "yes", "unclear", "yes"),
            self.row(a, "full_text", "include", "researcher", "2026-10-18", "yes", "yes", "no", "yes",
                     why="verified: calibration not assessed"),
            self.row(b, "full_text", "include", "assistant", "2026-10-16", "yes", "yes", "yes", "unclear"),
            self.row(b, "full_text", "include", "researcher", "2026-10-18", "yes", "yes", "yes", "unclear",
                     why="verified"),
        ], header=self.header)
        self.fx.build(today="2026-10-18")
        ea, eb = self.rq5(a)["confirmed"], self.rq5(b)["confirmed"]
        self.assertTrue(ea["researcher_verified"] and ea["changed_by_verification"])
        self.assertEqual(ea["statuses"]["calibration"], "no")
        self.assertEqual(ea["history"][0]["screener"], "assistant")
        self.assertEqual(ea["history"][0]["statuses"]["calibration"], "unclear")   # evidence kept
        self.assertTrue(eb["researcher_verified"])
        self.assertFalse(eb["changed_by_verification"])

    # 12
    def test_ids_and_unscreened_inventory_values_stable(self):
        self.fx.reports()
        before_ids = self.fx.id_to_sources()
        before_inv = self.fx.inventory()
        a = self.ids[0]
        self.fx.write_decisions([self.row(a, "full_text", "include", "assistant", "2026-10-16",
                                          "yes", "yes", "unclear", "no")], header=self.header)
        self.fx.build(today="2026-10-16")
        self.fx.reports()
        self.assertEqual(self.fx.id_to_sources(), before_ids)
        after_inv = self.fx.inventory()
        for pid, row in before_inv.items():
            if pid != a:
                self.assertEqual(after_inv[pid], row)


if __name__ == "__main__":
    unittest.main()
