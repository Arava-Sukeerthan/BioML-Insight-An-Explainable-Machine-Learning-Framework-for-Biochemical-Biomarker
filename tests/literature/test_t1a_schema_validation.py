"""T1-A tests: screening fields and descriptors (D-028 2d, D-029/D-060, D-058), controlled
scope_flags tokens (D-057, D-061), the D-028 publication_type mapping, and compatibility.

ALL FIXTURE RECORDS IN THIS FILE ARE SYNTHETIC SOFTWARE-TEST DATA (titles start with
"SYNTHETIC", URLs use example.org or arxiv.org with non-existent IDs, PMIDs 9000000xx, DOI
prefixes 10.0000 and, only to show that DOI prefixes are ignored, 10.1101/synthetic.*). They are
not real publications and must never be copied into research records. No test reads or writes the
real research inventory: every build runs in a temporary directory.

Run from the repository root:
    python3 -I -m unittest discover -s tests/literature -v
"""
import csv
import json
import re
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_pubrecords import REPO, connector_article, write_json, pr  # noqa: E402
from test_screening_and_ids import WebFixture, D060_SYNTHETIC  # noqa: E402
import make_literature_reports as mlr  # noqa: E402

SCHEMAS = REPO / "research" / "literature" / "schemas"
HEADER = pr.SCREENING_REQUIRED + pr.SCREENING_OPTIONAL


def ta_row(pid, decision="include", **kw):
    """A complete title_abstract row in HEADER order (SYNTHETIC values); kw overrides columns."""
    rec = {"paper_id": pid, "stage": "title_abstract", "decision": decision, "reason_code": "",
           "screener": "assistant", "date": "2026-10-15",
           "justification": "" if decision == "include" else "SYNTHETIC test justification",
           **D060_SYNTHETIC}
    rec.update(kw)
    return [rec.get(c, "") for c in HEADER]


class TestSchemaCorrectness(unittest.TestCase):
    def setUp(self):
        self.sd = json.load(open(SCHEMAS / "screening_decision.schema.json"))
        self.inv = json.load(open(SCHEMAS / "paper_inventory.schema.json"))["items"]["properties"]
        self.pub = json.load(open(SCHEMAS / "publication_record.schema.json"))["properties"]

    def test_record_type_is_the_d028_2d_list(self):
        approved = ("original", "methodological", "software", "guideline", "review_lead", "other")
        self.assertEqual(pr.SCREENING_ENUMS["record_type"], ("",) + approved)
        self.assertEqual(self.sd["properties"]["record_type"]["enum"], ["", *approved])
        self.assertEqual(self.inv["record_type"]["enum"], [*approved, None])
        for gone in ("preprint", "notice"):
            self.assertNotIn(gone, pr.SCREENING_ENUMS["record_type"])

    def test_descriptor_enums(self):
        vd = ("external", "temporal", "internal_only", "none", "not_applicable", "unclear")       # D-060 (1)
        bc = ("metabolomics_lipidomics", "newborn_screening_msms", "routine_chemistry", "mixed_both",
              "other", "unclear")                                                                  # D-058
        self.assertEqual(pr.SCREENING_ENUMS["validation_design"], ("",) + vd)
        self.assertEqual(pr.SCREENING_ENUMS["biomarker_class"], ("",) + bc)
        self.assertEqual(self.inv["screening_validation_design"]["enum"], [*vd, None])
        self.assertEqual(self.inv["biomarker_class"]["enum"], [*bc, None])
        self.assertEqual(pr.TITLE_ABSTRACT_REQUIRED,
                         ("rq_tags", "record_type", "biomarker_class", "dim_explainability",
                          "dim_uncertainty", "dim_calibration", "validation_design"))       # D-060 (6)

    def test_publication_type_enum_matches_mapping(self):
        expected = ("retraction_notice", "expression_of_concern", "erratum_or_correction", "study_protocol",
                    "dataset", "preprint", "review", "guideline_or_consensus", "editorial_comment_letter",
                    "conference_paper", "journal_article", "unknown", "other")
        self.assertEqual(pr.PUBLICATION_TYPES, expected)
        self.assertEqual(len(pr.PUBLICATION_TYPES), 13)
        self.assertEqual(self.inv["publication_type"]["enum"], [*expected, None])
        self.assertEqual(self.pub["publication_type"]["enum"], list(expected))

    def test_retired_column_out_of_screening_schema(self):
        self.assertEqual(pr.RETIRED_SCREENING_COLUMNS, ("dim_independent_validation",))
        self.assertNotIn("dim_independent_validation", self.sd["properties"])
        self.assertNotIn("dim_independent_validation", self.sd["x-column-order"])
        self.assertNotIn("dim_independent_validation", pr.SCREENING_OPTIONAL)
        self.assertNotIn("dim_independent_validation", pr.SCREENING_ENUMS)
        # inventory and publication schemas keep it (always null) until T2
        self.assertIn("dim_independent_validation", mlr.INV_COLS)
        self.assertIn("dim_independent_validation", self.inv)

    def test_extraction_validation_design_unchanged(self):
        self.assertIn("validation_design", mlr.EXTRACTION_FIELDS)
        self.assertIn("validation_design", mlr.MANUAL_FIELDS)
        self.assertEqual(mlr.MANUAL_DEFAULTS["validation_design"], mlr.SENTINEL)
        self.assertEqual(self.inv["validation_design"],
                         {"type": ["string", "null"], "description": "Sentinel 'REQUIRES FULL-TEXT REVIEW' until extracted."})
        self.assertIn("screening_validation_design", mlr.INV_COLS)
        self.assertNotIn("screening_validation_design", mlr.MANUAL_FIELDS)

    def test_scope_flag_patterns_match_code(self):
        self.assertEqual(pr.SCOPE_FLAG_TOKENS, ("scope_pending_proteomics", "non_metabolic_rq5_candidate"))
        manual = re.compile(self.sd["properties"]["scope_flags"]["pattern"])
        built = re.compile(self.inv["scope_flags"]["pattern"])
        good = ["", "scope_pending_proteomics", "non_metabolic_rq5_candidate",
                "scope_pending_proteomics;non_metabolic_rq5_candidate"]
        bad = ["retracted", "scope_pending", "lr_only", "prognostic", "non_metabolic_method_exemplar",
               "abstract_only", "expression_of_concern", "scope_pending_proteomics;;non_metabolic_rq5_candidate",
               " scope_pending_proteomics", "scope_pending_proteomics; non_metabolic_rq5_candidate"]
        for v in good:
            with self.subTest(good=v):
                self.assertTrue(manual.fullmatch(v))
                self.assertEqual(pr.scope_flag_errors(v), [])
        for v in bad:
            with self.subTest(bad=v):
                self.assertFalse(manual.fullmatch(v))
                self.assertTrue(pr.scope_flag_errors(v))
        self.assertTrue(built.fullmatch("retracted;scope_pending_proteomics"))
        for word in ("abstract_only", "expression_of_concern", "lr_only", "prognostic"):
            self.assertNotIn(word, self.inv["scope_flags"]["description"])
            self.assertFalse(built.fullmatch(word))


class TestScreeningValidation(unittest.TestCase):
    def setUp(self):
        self.fx = WebFixture()
        self.fx.build()
        self.ids = sorted(p["paper_id"] for p in self.fx.pubs())
        self.pubs_path = self.fx.lit / "records" / "publications.jsonl"

    def assert_rejected(self, rows, *fragments, header=HEADER):
        before = self.pubs_path.read_bytes()
        report_before = (self.fx.lit / "records" / "build_report.json").read_bytes()
        self.fx.write_decisions(rows, header=header)
        with self.assertRaises(ValueError) as cm:
            self.fx.build(today="2026-10-16")
        for frag in fragments:
            self.assertIn(frag, str(cm.exception))
        self.assertEqual(self.pubs_path.read_bytes(), before)               # nothing written
        self.assertEqual((self.fx.lit / "records" / "build_report.json").read_bytes(), report_before)
        return str(cm.exception)

    def test_complete_include_and_uncertain_rows_accepted(self):
        a, b = self.ids[:2]
        self.fx.write_decisions([ta_row(a, "include"), ta_row(b, "uncertain")], header=HEADER)
        self.fx.build(today="2026-10-16")
        got = {p["paper_id"]: p for p in self.fx.pubs()}
        self.assertEqual(got[a]["screening_decision"], "include")
        self.assertEqual(got[b]["screening_details"]["validation_design"], "unclear")
        self.assertEqual(got[b]["screening_details"]["biomarker_class"], "metabolomics_lipidomics")

    def test_exclude_without_descriptors_accepted(self):
        self.fx.write_decisions([[self.ids[0], "title_abstract", "exclude", "E3", "assistant", "2026-10-15",
                                  "SYNTHETIC no model"]])
        self.fx.build(today="2026-10-16")

    def test_stage0_rule_rows_exempt(self):
        a, b, c = self.ids[:3]
        self.fx.write_decisions([
            [a, "title_abstract", "exclude", "E5", pr.STAGE0_SCREENER, "2026-10-15", "SYNTHETIC Stage 0"],
            [b, "title_abstract", "include", "", pr.STAGE0_SCREENER, "2026-10-15", ""],
            [c, "title_abstract", "uncertain", "", pr.STAGE0_SCREENER, "2026-10-15", "SYNTHETIC Stage 0"],
        ])
        self.fx.build(today="2026-10-16")
        # the exemption is for that exact screener value only
        self.assert_rejected([[b, "title_abstract", "include", "", "rule:stage0x", "2026-10-15", ""]],
                             "D-060 (6)", header=pr.SCREENING_REQUIRED)

    def test_full_text_rows_not_subject_to_title_abstract_rule(self):
        a, b = self.ids[:2]
        self.fx.write_decisions([
            [a, "full_text", "include", "", "assistant", "2026-10-16", ""],
            [b, "full_text", "uncertain", "", "assistant", "2026-10-16", "SYNTHETIC unclear at full text"],
        ])
        self.fx.build(today="2026-10-16")

    def test_each_missing_required_descriptor_rejected(self):
        a = self.ids[0]
        for decision in ("include", "uncertain"):
            for col in pr.TITLE_ABSTRACT_REQUIRED:
                with self.subTest(decision=decision, missing=col):
                    msg = self.assert_rejected([ta_row(a, decision, **{col: ""})], "line 2", a, col, "D-060 (6)")
                    others = [c for c in pr.TITLE_ABSTRACT_REQUIRED if c != col]
                    self.assertFalse(any(f"'{c}'" in msg for c in others))   # only the missing one named
        with self.subTest("file without the descriptor columns"):
            self.assert_rejected([[a, "title_abstract", "include", "", "assistant", "2026-10-15", ""]],
                                 "D-060 (6)", header=pr.SCREENING_REQUIRED)

    def test_invalid_values_rejected(self):
        a = self.ids[0]
        cases = [("record_type", v) for v in ("preprint", "notice", "Original", "review")] + \
                [("validation_design", v) for v in ("yes", "internal", "External", "cross_validation")] + \
                [("biomarker_class", v) for v in ("metabolomics", "proteomics", "both", "Unclear")]
        for col, value in cases:
            with self.subTest(col=col, value=value):
                self.assert_rejected([ta_row(a, **{col: value})], "line 2", f"{col}={value!r}")

    def test_scope_flags(self):
        a = self.ids[0]
        for value in ("scope_pending_proteomics", "non_metabolic_rq5_candidate",
                      "scope_pending_proteomics;non_metabolic_rq5_candidate"):
            with self.subTest(accepted=value):
                self.fx.write_decisions([ta_row(a, scope_flags=value)], header=HEADER)
                self.fx.build(today="2026-10-16")
                (p,) = [p for p in self.fx.pubs() if p["paper_id"] == a]
                self.assertEqual(p["screening_details"]["scope_flags"], value)        # stored as written
        rejected = {
            "lr_only": "not in", "scope_pending": "not in", "prognostic": "not in",
            "non_metabolic_method_exemplar": "not in", "abstract_only": "not in",
            "expression_of_concern": "not in", "retracted": "derived by the build",
            "scope_pending_proteomics;retracted": "derived by the build",
            "scope_pending_proteomics;;non_metabolic_rq5_candidate": "empty token",
            ";scope_pending_proteomics": "empty token", "scope_pending_proteomics;": "empty token",
            " scope_pending_proteomics": "whitespace", "scope_pending_proteomics ": "whitespace",
            "scope_pending_proteomics; non_metabolic_rq5_candidate": "whitespace",
        }
        for value, frag in rejected.items():
            with self.subTest(rejected=value):
                self.assert_rejected([ta_row(a, scope_flags=value)], "line 2", a, f"scope_flags={value!r}", frag)

    def test_retired_column_rejected_not_converted(self):
        a = self.ids[0]
        old = pr.SCREENING_REQUIRED + ["dim_independent_validation"]
        self.assert_rejected([[a, "title_abstract", "exclude", "E3", "assistant", "2026-10-15", "x", "external"]],
                             "retired columns ['dim_independent_validation']", "not converted", header=old)
        both = HEADER + ["dim_independent_validation"]
        self.assert_rejected([ta_row(a) + ["external"]], "retired columns", header=both)

    def test_files_without_new_columns_load_where_supported(self):
        # exclude-only and full-text files written before T1-A (required columns only) still load
        a, b = self.ids[:2]
        self.fx.write_decisions([[a, "title_abstract", "exclude", "E3", "assistant", "2026-10-15", "x"],
                                 [b, "full_text", "abstract_only", "", "assistant", "2026-10-16", ""]])
        self.fx.build(today="2026-10-16")
        self.fx.reports()
        inv = self.fx.inventory()
        self.assertEqual(inv[a]["screening_status"], "exclude")
        self.assertIsNone(inv[a]["biomarker_class"])
        self.assertIsNone(inv[a]["screening_validation_design"])


class PubTypeFixture(WebFixture):
    """WebFixture plus SYNTHETIC PubMed records with chosen publication types, an arXiv record and
    a web record whose DOI has a preprint-server prefix."""

    TYPES = {
        "900000021": ["Retraction of Publication", "Journal Article"],
        "900000022": ["Journal Article", "Retracted Publication"],
        "900000023": ["Journal Article", "Preprint"],
        "900000024": ["Journal Article", "SYNTHETIC Unlisted Type"],
        "900000025": ["SYNTHETIC Unlisted Type"],
        "900000026": ["Research Support, Non-U.S. Gov't"],
        "900000027": [],
    }

    def __init__(self):
        super().__init__()
        with open(self.lit / "search_queries.csv", "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["query_id", "row_type", "source", "query_string"])
            w.writerow({"query_id": "Q-TEST-PT", "row_type": "planned", "source": "pubmed",
                        "query_string": "synthetic publication types"})
            w.writerow({"query_id": "Q-TEST-AXT", "row_type": "planned", "source": "arxiv",
                        "query_string": "synthetic arxiv"})
        pmids = sorted(self.TYPES)
        self.reg(write_json(self.lit, "Q-TEST-PT_search_00.json", {}, {"pmids": pmids, "total_count": len(pmids)}),
                 "Q-TEST-PT", "pubmed", "pubmed_connector_search", len(pmids), request={"retstart": 0})
        self.reg(write_json(self.lit, "META_batch_001.json", {}, {"articles": [
            connector_article(pmid, f"SYNTHETIC publication type case {pmid}", doi=f"10.0000/pt.{pmid}",
                              last=f"Case{pmid[-2:]}", types=types)
            for pmid, types in self.TYPES.items()]}), "META", "pubmed", "pubmed_connector_metadata", len(pmids))
        self.reg(write_json(self.lit, "Q-TEST-AXT_arxiv.json", {}, {"records": [
            {"title": "SYNTHETIC arXiv preprint without source types", "authors": ["Eta, Test"], "year": 2025,
             "arxiv_id": "2601.00099", "url": "https://arxiv.org/abs/2601.00099"}]}),
            "Q-TEST-AXT", "arxiv", "structured_transcription", 1)
        self.reg(write_json(self.lit, "Q-TEST-WS_2026-10-05.json", {}, {"records": [
            {"title": "SYNTHETIC web record with a preprint-server DOI prefix", "doi": "10.1101/synthetic.0001",
             "url": "https://example.org/web/doi"}]}), "Q-TEST-WS", "web", "structured_transcription", 1)


class TestPublicationTypeMapping(unittest.TestCase):
    d = staticmethod(pr.derive_publication_type)

    def test_every_table_row(self):
        expected = {
            "Retraction of Publication": "retraction_notice", "Expression of Concern": "expression_of_concern",
            "Published Erratum": "erratum_or_correction", "Correction": "erratum_or_correction",
            "Clinical Trial Protocol": "study_protocol", "Dataset": "dataset", "Preprint": "preprint",
            "Review": "review", "Systematic Review": "review", "Scoping Review": "review",
            "Meta-Analysis": "review", "Evidence Synthesis": "review",
            "Guideline": "guideline_or_consensus", "Practice Guideline": "guideline_or_consensus",
            "Consensus Statement": "guideline_or_consensus", "Editorial": "editorial_comment_letter",
            "Comment": "editorial_comment_letter", "Letter": "editorial_comment_letter",
            "News": "editorial_comment_letter", "Conference Proceedings": "conference_paper",
            "Congress": "conference_paper", "Journal Article": "journal_article",
        }
        self.assertEqual(expected, {t: v for v, names in pr.PUBLICATION_TYPE_MAP for t in names})
        for source_type, value in expected.items():
            with self.subTest(source_type):
                self.assertEqual(self.d([source_type], ["pubmed"]), value)
                self.assertEqual(self.d([source_type, "Journal Article"], ["pubmed"]), value)

    def test_first_match_precedence(self):
        order = [v for v, _ in pr.PUBLICATION_TYPE_MAP]
        names = {v: n[0] for v, n in pr.PUBLICATION_TYPE_MAP}
        for i, hi in enumerate(order):
            for lo in order[i + 1:]:
                with self.subTest(hi=hi, lo=lo):
                    self.assertEqual(self.d([names[lo], names[hi]], ["pubmed"]), hi)
                    self.assertEqual(self.d([names[hi], names[lo]], ["pubmed"]), hi)

    def test_retraction_notice_versus_retracted_article(self):
        self.assertEqual(self.d(["Retraction of Publication"], ["pubmed"]), "retraction_notice")
        self.assertEqual(self.d(["Journal Article", "Retracted Publication"], ["pubmed"]), "journal_article")

    def test_arxiv_source_database(self):
        self.assertEqual(self.d([], ["arxiv"]), "preprint")
        self.assertEqual(self.d(None, ["arxiv", "web"]), "preprint")
        self.assertEqual(self.d(["Retraction of Publication"], ["arxiv"]), "retraction_notice")   # rows 1-5 first
        self.assertEqual(self.d([], ["pubmed"]), "unknown")
        self.assertEqual(self.d([], ["web"]), "unknown")

    def test_unrecognised_and_missing_types(self):
        self.assertEqual(self.d(["SYNTHETIC Unlisted Type"], ["pubmed"]), "other")
        self.assertEqual(self.d(["Journal Article", "SYNTHETIC Unlisted Type"], ["pubmed"]), "journal_article")
        self.assertEqual(pr.unmapped_publication_types(["Journal Article", "SYNTHETIC Unlisted Type",
                                                        "Retracted Publication"]), ["SYNTHETIC Unlisted Type"])
        self.assertEqual(self.d([], ["pubmed"]), "unknown")
        self.assertEqual(self.d(None, []), "unknown")
        # types kept but not used for the class give no class (T1-A interpretation, reported)
        self.assertEqual(self.d(["Research Support, Non-U.S. Gov't", "Validation Study"], ["pubmed"]), "unknown")

    def test_build_derives_types_and_reports_unmapped(self):
        fx = PubTypeFixture()
        report = fx.build(today="2026-10-16")        # an unrecognised type does not fail the build
        fx.reports()
        pubs = {p["pmid"]: p for p in fx.pubs() if p["pmid"] in PubTypeFixture.TYPES}
        expected = {"900000021": "retraction_notice", "900000022": "journal_article", "900000023": "preprint",
                    "900000024": "journal_article", "900000025": "other", "900000026": "unknown",
                    "900000027": "unknown"}
        self.assertEqual({k: p["publication_type"] for k, p in pubs.items()}, expected)
        self.assertEqual(report["unmapped_publication_types"], {"SYNTHETIC Unlisted Type": 2})
        self.assertEqual(json.load(open(fx.lit / "records" / "build_report.json"))["unmapped_publication_types"],
                         {"SYNTHETIC Unlisted Type": 2})
        self.assertTrue(pubs["900000022"]["retracted"])
        self.assertFalse(pubs["900000021"]["retracted"])
        others = {p["title"]: p for p in fx.pubs()}
        self.assertEqual(others["SYNTHETIC arXiv preprint without source types"]["publication_type"], "preprint")
        web_doi = others["SYNTHETIC web record with a preprint-server DOI prefix"]
        self.assertEqual((web_doi["doi"], web_doi["publication_type"]), ("10.1101/synthetic.0001", "unknown"))
        patents = [p for p in fx.pubs() if any("example.org/patent" in u for u in p["source_urls"])]
        self.assertTrue(patents and all(p["publication_type"] == "unknown" for p in patents))   # no URL rules
        inv = {r["pmid"]: r for r in fx.inventory().values() if r["pmid"] in PubTypeFixture.TYPES}
        for pmid, types in PubTypeFixture.TYPES.items():
            with self.subTest(pmid):
                self.assertEqual(inv[pmid]["publication_type"], expected[pmid])
                self.assertEqual(inv[pmid]["source_publication_types"], ";".join(types) or None)   # verbatim
        self.assertEqual(inv["900000022"]["scope_flags"], "retracted")
        self.assertIsNone(inv["900000021"]["scope_flags"])

    def test_retracted_flag_stays_build_derived(self):
        fx = PubTypeFixture()
        fx.build()
        pid = [p["paper_id"] for p in fx.pubs() if p["pmid"] == "900000022"][0]
        fx.write_decisions([ta_row(pid, scope_flags="scope_pending_proteomics")], header=HEADER)
        fx.build(today="2026-10-16")
        fx.reports()
        self.assertEqual(fx.inventory()[pid]["scope_flags"], "retracted;scope_pending_proteomics")
        fx.write_decisions([ta_row(pid, scope_flags="retracted")], header=HEADER)
        with self.assertRaises(ValueError):
            fx.build(today="2026-10-17")
        fx.reports()                                   # previous valid build: flag kept
        self.assertEqual(fx.inventory()[pid]["scope_flags"], "retracted;scope_pending_proteomics")


class TestFollowUpQ076(unittest.TestCase):
    """T1-A follow-up (owner directions on Q-076(a)-(d), 2026-10-31). SYNTHETIC fixtures only."""

    d = staticmethod(pr.derive_publication_type)

    def test_a_all_ignored_types_give_unknown_and_stay_verbatim(self):
        ignored = sorted(pr.PUBLICATION_TYPES_IGNORED)
        self.assertEqual(self.d(ignored, ["pubmed"]), "unknown")
        self.assertEqual(pr.unmapped_publication_types(ignored), [])
        fx = PubTypeFixture()
        fx.build()
        fx.reports()
        (row,) = [r for r in fx.inventory().values() if r["pmid"] == "900000026"]
        self.assertEqual((row["publication_type"], row["source_publication_types"]),
                         ("unknown", "Research Support, Non-U.S. Gov't"))

    def test_precedence_recognised_type_wins_over_unrecognised(self):
        for known, value in (("Journal Article", "journal_article"), ("Review", "review"),
                             ("Letter", "editorial_comment_letter")):
            for order in ((known, "SYNTHETIC Unlisted Type"), ("SYNTHETIC Unlisted Type", known)):
                with self.subTest(order=order):
                    self.assertEqual(self.d(list(order), ["pubmed"]), value)
                    self.assertEqual(pr.unmapped_publication_types(list(order)), ["SYNTHETIC Unlisted Type"])

    def test_b_arxiv_rule_uses_primary_source_database(self):
        self.assertEqual(self.d([], ["arxiv"]), "preprint")
        self.assertEqual(self.d([], ["arxiv", "web"]), "preprint")
        self.assertEqual(self.d(["Journal Article"], ["pubmed", "arxiv"]), "journal_article")
        self.assertEqual(self.d([], ["pubmed", "arxiv"]), "unknown")
        # build: an arXiv record merged into a PubMed record (same DOI) keeps PubMed as primary source
        fx = PubTypeFixture()
        with open(fx.lit / "search_queries.csv", "a", newline="") as f:
            csv.DictWriter(f, fieldnames=["query_id", "row_type", "source", "query_string"]).writerow(
                {"query_id": "Q-TEST-AXM", "row_type": "planned", "source": "arxiv", "query_string": "synthetic"})
        fx.reg(write_json(fx.lit, "Q-TEST-AXM_arxiv.json", {}, {"records": [
            {"title": "SYNTHETIC publication type case 900000021", "authors": ["Case21, Test"], "year": 2021,
             "doi": "10.0000/pt.900000021", "arxiv_id": "2601.00098",
             "url": "https://arxiv.org/abs/2601.00098"}]}), "Q-TEST-AXM", "arxiv", "structured_transcription", 1)
        fx.build()
        (p,) = [p for p in fx.pubs() if p["pmid"] == "900000021"]
        self.assertEqual(p["source_databases"][:2], ["pubmed", "arxiv"])
        self.assertEqual(p["publication_type"], "retraction_notice")     # PubMed types decide, not arXiv
        (j,) = [p for p in fx.pubs() if p["pmid"] == "900000024"]
        self.assertEqual(j["publication_type"], "journal_article")


class TestFollowUpPublicationTypeEdits(unittest.TestCase):
    """Q-076(c): a non-null publication_type that differs from the derived value is rejected."""

    NAMES = ("paper_inventory.json", "paper_inventory.csv", "records/collection_stats.json",
             "fulltext_review_candidates.csv", "verification_report.md")

    def setUp(self):
        self.fx = PubTypeFixture()
        self.fx.build()
        self.fx.reports()
        self.inv_path = self.fx.lit / "paper_inventory.json"

    def snapshot(self):
        return {n: (self.fx.lit / n).read_bytes() for n in self.NAMES}

    def test_inconsistent_json_edit_rejected_and_nothing_written(self):
        inv = json.load(open(self.inv_path))
        (i,) = [k for k, r in enumerate(inv) if r["pmid"] == "900000023"]       # derived: preprint
        self.assertEqual(inv[i]["publication_type"], "preprint")
        inv[i]["publication_type"] = "journal_article"
        json.dump(inv, open(self.inv_path, "w"))
        before = self.snapshot()
        with self.assertRaises(SystemExit) as cm:
            self.fx.reports()
        self.assertIn(inv[i]["paper_id"], str(cm.exception))
        self.assertIn("publication_type", str(cm.exception))
        self.assertEqual(self.snapshot(), before)

    def test_value_equal_to_derived_is_accepted(self):
        inv = json.load(open(self.inv_path))
        json.dump(inv, open(self.inv_path, "w"))          # rewritten, values unchanged
        self.fx.reports()

    def test_legacy_null_values_accepted(self):
        inv = json.load(open(self.inv_path))
        derived = {r["paper_id"]: r["publication_type"] for r in inv}
        for r in inv:
            r["publication_type"] = None                  # as in inventories built before T1-A
        json.dump(inv, open(self.inv_path, "w"))
        self.fx.reports()
        self.assertEqual({k: r["publication_type"] for k, r in self.fx.inventory().items()}, derived)

    def test_csv_only_edit_rejected_and_nothing_written(self):
        cpath = self.fx.lit / "paper_inventory.csv"
        with open(cpath, newline="") as f:
            rows = list(csv.DictReader(f))
        (i,) = [k for k, r in enumerate(rows) if r["pmid"] == "900000023"]
        rows[i]["publication_type"] = "journal_article"
        with open(cpath, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=mlr.INV_COLS)
            w.writeheader()
            w.writerows(rows)
        before = self.snapshot()
        with self.assertRaises(SystemExit) as cm:
            self.fx.reports()
        self.assertIn(f"{rows[i]['paper_id']}:publication_type", str(cm.exception))
        self.assertEqual(self.snapshot(), before)


class TestFollowUpRetractedCandidates(unittest.TestCase):
    """Q-076(d): retracted records stay out of fulltext_review_candidates.csv whatever other flags they
    carry. The synthetic query Q-TEST-PT is mapped to theme F for this test only."""

    def candidates(self, fx):
        with open(fx.lit / "fulltext_review_candidates.csv", newline="") as f:
            return {r["paper_id"] for r in csv.DictReader(f)}

    def test_retracted_with_other_flag_excluded_and_theme_record_kept(self):
        fx = PubTypeFixture()
        fx.build()
        ids = {p["pmid"]: p["paper_id"] for p in fx.pubs() if p["pmid"] in PubTypeFixture.TYPES}
        retracted, plain = ids["900000022"], ids["900000024"]
        fx.write_decisions([ta_row(retracted, scope_flags="scope_pending_proteomics"),
                            ta_row(plain, scope_flags="scope_pending_proteomics")], header=HEADER)
        fx.build(today="2026-10-16")
        with mock.patch.dict(mlr.THEMES, {"Q-TEST-PT": "F"}):
            fx.reports()
        inv = fx.inventory()
        self.assertEqual(inv[retracted]["scope_flags"], "retracted;scope_pending_proteomics")
        self.assertEqual(inv[plain]["scope_flags"], "scope_pending_proteomics")
        cand = self.candidates(fx)
        self.assertNotIn(retracted, cand)                  # excluded although it has another flag
        self.assertIn(plain, cand)                         # theme F, not retracted: still a candidate
        self.assertTrue(set(ids.values()) - {retracted} <= cand)   # null flags raise nothing

    def test_retracted_alone_excluded(self):
        fx = PubTypeFixture()
        fx.build()
        with mock.patch.dict(mlr.THEMES, {"Q-TEST-PT": "F"}):
            fx.reports()
        (pid,) = [p["paper_id"] for p in fx.pubs() if p["pmid"] == "900000022"]
        self.assertEqual(fx.inventory()[pid]["scope_flags"], "retracted")
        self.assertNotIn(pid, self.candidates(fx))


if __name__ == "__main__":
    unittest.main()
