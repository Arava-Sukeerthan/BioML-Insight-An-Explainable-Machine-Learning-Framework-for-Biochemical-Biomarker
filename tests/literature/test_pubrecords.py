"""Validation tests for the literature-metadata workflow (LIT-002).

ALL FIXTURE RECORDS IN THIS FILE ARE SYNTHETIC SOFTWARE-TEST DATA. They are not real
publications: titles start with "SYNTHETIC", PMIDs are in the 9000000xx range, and DOIs use the
non-existent prefix 10.0000. They must never be copied into research records.

Run from the repository root:
    python3 -I -m unittest discover -s tests -v
"""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "literature"))
import pubrecords as pr  # noqa: E402
import fetch_pubmed_eutils as eu  # noqa: E402

QUERIES = [
    {"query_id": "Q-TEST-A", "row_type": "planned", "source": "pubmed", "query_string": "synthetic A AND 1800/01/01:{RUN_DATE}[edat]"},
    {"query_id": "Q-TEST-B", "row_type": "planned", "source": "pubmed", "query_string": "synthetic B"},
    {"query_id": "Q-TEST-CN", "row_type": "planned", "source": "consensus", "query_string": "synthetic consensus question"},
]


def connector_article(pmid, title, doi=None, journal="Synthetic Journal A", year="2021", last="Alpha",
                      pmc=None, types=("Journal Article",)):
    return {"identifiers": {"pmid": pmid, "doi": doi, "pmc": pmc}, "title": title,
            "abstract": f"Synthetic abstract for {pmid}.", "doi": doi,
            "journal": {"title": journal, "iso_abbreviation": "Synth J"},
            "authors": [{"last_name": last, "fore_name": "Test", "initials": "T"}],
            "publication_date": {"year": year}, "article_types": list(types), "language": "eng"}


def write_json(lit, name, provenance, response):
    p = lit / "raw_exports" / name
    p.write_text(json.dumps({"provenance": provenance, "response": response}, indent=1))
    return name


class Fixture:
    """Builds a temporary literature directory with synthetic raw exports."""

    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.lit = Path(self.tmp.name) / "literature"
        (self.lit / "raw_exports").mkdir(parents=True)
        with open(self.lit / "search_queries.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["query_id", "row_type", "source", "query_string"])
            w.writeheader()
            w.writerows(QUERIES)

    def reg(self, name, qid, source, route, n, transcribed=True, request=None):
        return pr.register_raw(self.lit, name, qid, source, route, "synthetic-tool", request or {},
                               "2026-10-14T10:00:00+00:00", n, transcribed)

    def standard(self):
        # PubMed search A: complete (3 of 3). Search B: incomplete (1 of 2 retrieved).
        self.reg(write_json(self.lit, "Q-TEST-A_search_00.json", {}, {
            "pmids": ["900000001", "900000002", "900000003"], "total_count": 3}),
            "Q-TEST-A", "pubmed", "pubmed_connector_search", 3, request={"retstart": 0})
        self.reg(write_json(self.lit, "Q-TEST-B_search_00.json", {}, {
            "pmids": ["900000002"], "total_count": 2}),
            "Q-TEST-B", "pubmed", "pubmed_connector_search", 1, request={"retstart": 0})
        self.reg(write_json(self.lit, "META_batch_000.json", {}, {"articles": [
            connector_article("900000001", "SYNTHETIC classifier of metabolic markers in cohort one",
                              doi="10.0000/test.1", pmc="PMC9000001"),
            connector_article("900000002", "SYNTHETIC explainable model for lipid profiles in adults",
                              doi="10.0000/test.2", year="2020", last="Beta"),
            connector_article("900000003", "SYNTHETIC conformal prediction for glucose biomarkers study",
                              year="2022", last="Gamma"),
        ]}), "META", "pubmed", "pubmed_connector_metadata", 3)
        # Consensus transcription
        self.reg(write_json(self.lit, "Q-TEST-CN_consensus.json", {}, {"records": [
            # same DOI as 900000001 in another form; journal written differently -> conflict kept
            {"title": "SYNTHETIC classifier of metabolic markers in cohort one", "authors": ["Test Alpha"],
             "year": 2021, "journal": "Synth. J. Alpha", "doi": "https://doi.org/10.0000/TEST.1",
             "url": "https://example.org/synthetic/1"},
            # same normalised title as 900000002 but year differs by one -> review, not merged
            {"title": "Synthetic explainable model for lipid profiles in adults.", "authors": ["Beta, Test"],
             "year": 2021, "journal": "Synthetic Journal A", "url": "https://example.org/synthetic/2"},
            # near-identical title to 900000003, same first author -> fuzzy review
            {"title": "SYNTHETIC conformal predictions for glucose biomarker study", "authors": ["Gamma, Test"],
             "year": 2022, "journal": "Synthetic Journal A", "url": "https://example.org/synthetic/3"},
            # claims PMID 900000001 but a different DOI -> identifier conflict, never merged
            {"title": "SYNTHETIC unrelated record with conflicting identifiers", "authors": ["Delta, Test"],
             "year": 2019, "journal": "Other", "doi": "10.0000/test.9", "pmid": "900000001"},
        ]}), "Q-TEST-CN", "consensus", "structured_transcription", 4)


class TestNormalisation(unittest.TestCase):
    def test_doi(self):
        for raw in ["10.0000/ABC.1", "https://doi.org/10.0000/abc.1", "doi: 10.0000/abc.1.",
                    "http://dx.doi.org/10.0000/abc.1"]:
            self.assertEqual(pr.normalize_doi(raw), "10.0000/abc.1")
        self.assertIsNone(pr.normalize_doi("not a doi"))

    def test_ids(self):
        self.assertEqual(pr.normalize_pmid(" 900000001 "), "900000001")
        self.assertIsNone(pr.normalize_pmid("0"))
        self.assertEqual(pr.normalize_pmcid("pmc123"), "PMC123")
        self.assertEqual(pr.normalize_arxiv("https://arxiv.org/abs/2101.00001v3"), "2101.00001")
        self.assertEqual(pr.normalize_arxiv("arXiv:2101.00001"), "2101.00001")

    def test_title(self):
        self.assertEqual(pr.normalize_title("<i>Naïve</i>  Bayes: a SYNTHETIC test."),
                         "naive bayes a synthetic test")


class TestParsers(unittest.TestCase):
    def test_connector_article_keeps_original(self):
        art = connector_article("900000010", "SYNTHETIC title", doi="10.0000/X.10", pmc="9000010")
        m = pr.parse_connector_article(art)
        self.assertEqual((m["pmid"], m["doi"], m["pmcid"], m["year"]),
                         ("900000010", "10.0000/x.10", "PMC9000010", 2021))
        self.assertIs(m["original"], art)
        self.assertEqual(m["source_url"], "https://pubmed.ncbi.nlm.nih.gov/900000010/")

    def test_efetch_xml(self):
        xml = b"""<?xml version="1.0"?><PubmedArticleSet><PubmedArticle><MedlineCitation>
          <PMID>900000020</PMID><Article><Journal><JournalIssue><PubDate><MedlineDate>2019 Nov-Dec</MedlineDate>
          </PubDate></JournalIssue><Title>Synthetic Journal B</Title></Journal>
          <ArticleTitle>SYNTHETIC <i>structured</i> abstract record</ArticleTitle>
          <ELocationID EIdType="doi">10.0000/test.20</ELocationID>
          <Abstract><AbstractText Label="BACKGROUND">Synthetic background.</AbstractText>
          <AbstractText Label="RESULTS">Synthetic results.</AbstractText></Abstract>
          <AuthorList><Author><LastName>Epsilon</LastName><ForeName>Test</ForeName><Initials>T</Initials></Author>
          <Author><CollectiveName>Synthetic Consortium</CollectiveName></Author></AuthorList>
          <Language>eng</Language><PublicationTypeList><PublicationType>Retracted Publication</PublicationType>
          </PublicationTypeList></Article></MedlineCitation><PubmedData><ArticleIdList>
          <ArticleId IdType="pubmed">900000020</ArticleId><ArticleId IdType="pmc">PMC9000020</ArticleId>
          </ArticleIdList></PubmedData></PubmedArticle></PubmedArticleSet>"""
        (m,) = pr.parse_efetch_xml(xml)
        self.assertEqual(m["title"], "SYNTHETIC structured abstract record")
        self.assertEqual(m["year"], 2019)
        self.assertEqual(m["doi"], "10.0000/test.20")
        self.assertEqual(m["pmcid"], "PMC9000020")
        self.assertEqual(m["abstract"], "BACKGROUND: Synthetic background. RESULTS: Synthetic results.")
        self.assertEqual(m["authors"][1], {"collective_name": "Synthetic Consortium"})
        self.assertIn("Retracted Publication", m["publication_types"])
        self.assertIn("<PMID>900000020</PMID>", m["original"])


class TestManifest(unittest.TestCase):
    def test_checksum_detects_edits_and_duplicates(self):
        fx = Fixture()
        name = write_json(fx.lit, "x.json", {}, {"pmids": [], "total_count": 0})
        fx.reg(name, "Q-TEST-A", "pubmed", "pubmed_connector_search", 0)
        self.assertEqual(pr.verify_manifest(fx.lit, pr.read_manifest(fx.lit)), [])
        with self.assertRaises(ValueError):
            fx.reg(name, "Q-TEST-A", "pubmed", "pubmed_connector_search", 0)
        (fx.lit / "raw_exports" / name).write_text("edited")
        self.assertTrue(pr.verify_manifest(fx.lit, pr.read_manifest(fx.lit)))
        with self.assertRaises(RuntimeError):
            pr.build(fx.lit, today="2026-10-14")


class TestBuild(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture()
        self.fx.standard()
        self.report = pr.build(self.fx.lit, today="2026-10-14")
        self.pubs = self.load()

    def load(self):
        with open(self.fx.lit / "records" / "publications.jsonl") as f:
            return [json.loads(line) for line in f]

    def by_title(self, needle, year=None):
        return [p for p in self.pubs if needle in p["title"] and (year is None or p["year"] == year)]

    def test_counts_and_completeness(self):
        # 3 + 1 PubMed hits + 4 Consensus records = 8 source records; DOI variant merges with
        # 900000001 and the repeated PMID 900000002 merges across queries -> 6 publications
        self.assertEqual(self.report["source_records"], 8)
        self.assertEqual(self.report["publications"], 6)
        comp = self.report["search_completeness"]
        self.assertTrue(comp["Q-TEST-A"]["complete"])
        self.assertFalse(comp["Q-TEST-B"]["complete"])

    def test_doi_variant_merged_and_conflict_preserved(self):
        (p,) = self.by_title("cohort one")
        self.assertEqual(p["n_source_records"], 2)
        # also one side of the open identifier-conflict pair -> an open review outranks "merged"
        self.assertEqual(p["duplicate_status"], "possible_duplicate_review")
        self.assertEqual(p["source_databases"], ["pubmed", "consensus"])
        self.assertEqual(p["journal"], "Synthetic Journal A")          # from PubMed (priority)
        conflict = [c for c in p["metadata_conflicts"] if c["field"] == "journal"]
        self.assertEqual(len(conflict), 1)
        self.assertEqual({v["value"] for v in conflict[0]["values"]},
                         {"Synthetic Journal A", "Synth. J. Alpha"})
        self.assertEqual(p["full_text_availability"], "pmc_record")
        # PubMed data were transcribed and not yet spot-checked -> capped
        self.assertEqual(p["verification_status"], "partially_verified")
        self.assertEqual(sorted(s["query_id"] for s in p["search_provenance"]), ["Q-TEST-A", "Q-TEST-CN"])

    def test_same_pmid_across_queries_merged(self):
        (p,) = self.by_title("lipid profiles", year=2020)
        self.assertEqual(sorted(s["query_id"] for s in p["search_provenance"]), ["Q-TEST-A", "Q-TEST-B"])

    def test_uncertain_matches_flagged_not_merged(self):
        with open(self.fx.lit / "records" / "dedup_review.csv", newline="") as f:
            review = list(csv.DictReader(f))
        reasons = sorted(r["reason"] for r in review)
        self.assertIn("same_title_year_differs_by_1", reasons)
        self.assertIn("fuzzy_title", reasons)
        self.assertTrue(any(r.startswith("identifier_conflict") for r in reasons))
        (p,) = self.by_title("lipid profiles", year=2021)
        self.assertEqual(p["duplicate_status"], "possible_duplicate_review")
        (q,) = self.by_title("conflicting identifiers")
        self.assertEqual(q["n_source_records"], 1)                    # not merged into 900000001
        (p,) = self.by_title("cohort one")
        self.assertNotEqual(q["paper_id"], p["paper_id"])             # registry must not re-merge them
        self.assertIn(p["paper_id"], q["possible_duplicates"])
        self.assertTrue(self.report["registry_conflicts"])
        self.assertEqual(q["verification_status"], "unverified")      # consensus only

    def test_ids_stable_after_new_data(self):
        before = {p["title"]: p["paper_id"] for p in self.pubs}
        self.fx.reg(write_json(self.fx.lit, "Q-TEST-B_search_01.json", {}, {
            "pmids": ["900000004"], "total_count": 2}),
            "Q-TEST-B", "pubmed", "pubmed_connector_search", 1, request={"retstart": 1})
        report = pr.build(self.fx.lit, today="2026-10-15")
        after = {p["title"]: p["paper_id"] for p in self.load() if p["title"]}
        for t, pid in before.items():
            if t:
                self.assertEqual(after[t], pid)
        self.assertTrue(report["search_completeness"]["Q-TEST-B"]["complete"])
        self.assertEqual(report["source_records_missing_metadata"], 1)   # 900000004 has no metadata yet

    def test_manual_inputs_survive_rebuild(self):
        (a,) = self.by_title("lipid profiles", year=2020)
        (b,) = self.by_title("lipid profiles", year=2021)
        (c,) = self.by_title("conformal prediction for")
        (d,) = self.by_title("conformal predictions")
        rec = self.fx.lit / "records"
        with open(rec / "dedup_decisions.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["paper_id_a", "paper_id_b", "decision", "reviewer", "date", "note"])
            w.writerow([a["paper_id"], b["paper_id"], "same", "researcher", "2026-10-15", "test"])
            w.writerow([c["paper_id"], d["paper_id"], "different", "researcher", "2026-10-15", "test"])
        (self.fx.lit / "screening").mkdir()
        with open(self.fx.lit / "screening" / "decisions.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["paper_id", "stage", "decision", "reason_code", "screener", "date", "justification"])
            w.writerow([c["paper_id"], "title_abstract", "exclude", "E3", "assistant", "2026-10-15", "test"])
        pr.build(self.fx.lit, today="2026-10-15")
        self.pubs = self.load()
        merged = [p for p in self.pubs if p["paper_id"] == a["paper_id"]][0]
        self.assertEqual(merged["n_source_records"], 3)
        self.assertFalse(any(p["paper_id"] == b["paper_id"] for p in self.pubs))
        # year conflict 2020 vs 2021 is now recorded, so the record needs review
        self.assertEqual(merged["verification_status"], "needs_review")
        excluded = [p for p in self.pubs if p["paper_id"] == c["paper_id"]][0]
        self.assertEqual((excluded["screening_decision"], excluded["exclusion_reason"]), ("exclude", "E3"))
        self.assertEqual(excluded["duplicate_status"], "unique")       # "different" decision honoured

    def test_spot_check_detects_transcription_error(self):
        # re-fetch of two PMIDs; one title differs from the transcribed original
        self.fx.reg(write_json(self.fx.lit, "META_refetch_000.json", {}, {"articles": [
            connector_article("900000001", "SYNTHETIC classifier of metabolic markers in cohort one",
                              doi="10.0000/test.1", pmc="PMC9000001"),
            connector_article("900000003", "SYNTHETIC conformal prediction for glucose biomarker study",
                              year="2022", last="Gamma"),
        ]}), "META", "pubmed", "pubmed_connector_metadata", 2)
        status, n, mism = pr.spot_check(self.fx.lit, "META_batch_000.json", "META_refetch_000.json")
        self.assertEqual((status, n), ("failed", 2))
        self.assertEqual([(m["pmid"], m["field"]) for m in mism], [("900000003", "title")])
        row = [r for r in pr.read_manifest(self.fx.lit) if r["raw_file"] == "META_batch_000.json"][0]
        self.assertEqual(row["transcription_check"], "failed")

    def test_public_index_has_no_abstracts(self):
        with open(self.fx.lit / "records" / "publications_index.csv", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 6)
        self.assertNotIn("abstract", rows[0])
        self.assertTrue(all(r["abstract_available"] in ("True", "False") for r in rows))

    def test_spot_check_upgrades_verification(self):
        for name in ("Q-TEST-A_search_00.json", "META_batch_000.json"):
            pr.set_transcription_check(self.fx.lit, name, "passed", "synthetic test")
        pr.build(self.fx.lit, today="2026-10-15")
        (p,) = [x for x in self.load() if x["title"] and "cohort one" in x["title"]]
        self.assertEqual(p["verification_status"], "verified")


class FakeTransport:
    """Stands in for NCBI E-utilities; returns synthetic responses and records requests."""

    def __init__(self):
        self.calls = []

    def request(self, url, data=None):
        self.calls.append((url, data.decode() if data else None))
        if url.endswith("esearch.fcgi"):
            return json.dumps({"esearchresult": {"count": "2", "retstart": "0",
                                                 "idlist": ["900000031", "900000032"]}}).encode()
        ids = [i for i in data.decode().split("id=")[1].split("&")[0].split("%2C")]
        arts = "".join(
            f"<PubmedArticle><MedlineCitation><PMID>{i}</PMID><Article><Journal><JournalIssue><PubDate>"
            f"<Year>2023</Year></PubDate></JournalIssue><Title>Synthetic Journal C</Title></Journal>"
            f"<ArticleTitle>SYNTHETIC eutils record {i}</ArticleTitle><AuthorList><Author><LastName>Zeta{i}"
            f"</LastName></Author></AuthorList></Article></MedlineCitation></PubmedArticle>" for i in ids)
        return f"<PubmedArticleSet>{arts}</PubmedArticleSet>".encode()


class TestEutilsClient(unittest.TestCase):
    def test_fetch_saves_raw_and_builds(self):
        fx = Fixture()
        t = FakeTransport()
        out = eu.run("Q-TEST-A", "2026-10-16", fx.lit, transport=t)
        self.assertEqual((out["reported_total"], out["retrieved"]), (2, 2))
        self.assertIn("1800%2F01%2F01%3A2026%2F10%2F16%5Bedat%5D", t.calls[0][1])  # {RUN_DATE} substituted
        self.assertIn("tool=bioml-insight-litreview", t.calls[0][1])
        rows = pr.read_manifest(fx.lit)
        self.assertEqual([r["route"] for r in rows], ["eutils_esearch", "eutils_efetch"])
        self.assertTrue(all(r["transcribed"] == "no" for r in rows))
        self.assertTrue(all("api_key" not in r["request_json"] and "email" not in r["request_json"] for r in rows))
        with self.assertRaises(FileExistsError):     # raw exports are never overwritten
            eu.run("Q-TEST-A", "2026-10-16", fx.lit, transport=t)
        report = pr.build(fx.lit, today="2026-10-16")
        self.assertEqual(report["publications"], 2)
        self.assertEqual(report["verification_status"], {"partially_verified": 2})
        self.assertTrue(report["search_completeness"]["Q-TEST-A"]["complete"])

    def test_rejects_non_pubmed_query(self):
        fx = Fixture()
        with self.assertRaises(ValueError):
            eu.run("Q-TEST-CN", "2026-10-16", fx.lit, transport=FakeTransport())


class TestRealQueryTable(unittest.TestCase):
    """The project's own query table must stay valid (no network)."""

    def test_project_queries_validate(self):
        sys.path.insert(0, str(REPO / "scripts" / "literature"))
        import validate_search_queries as v
        self.assertEqual(v.main(str(REPO / "research" / "literature" / "search_queries.csv")), 0)

    def test_dry_run_substitutes_run_date(self):
        out = eu.run("Q-PM-01", "2026-10-16", REPO / "research" / "literature", dry_run=True)
        self.assertIn("2015/01/01:2026/10/16[edat]", out["term"])
        self.assertNotIn("{RUN_DATE}", out["term"])


if __name__ == "__main__":
    unittest.main()
