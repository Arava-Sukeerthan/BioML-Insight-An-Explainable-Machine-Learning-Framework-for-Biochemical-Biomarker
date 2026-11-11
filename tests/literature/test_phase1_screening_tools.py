"""Phase 1 screening tools (researcher authorisation 2026-11-01): synthetic fixtures only.

Covers the approved decisions A1-A5 (Stage-0 generator), B2-B4 (frozen criteria-version registry
and validator), C1-C4 (pilot sampler) and D1-D3, D5 (blinded pilot sheet), and the five Phase 1
corrections (researcher authorisation 2026-11-11): verified run authorisation, atomic Stage-0 writes,
shared checked Stage-0 guards in the sampler, input-file SHA-256s, and input validation (calendar
dates; in-scope guards; sample/sidecar agreement). No test reads the real inventory or the
publications file, or writes inside the repository; one test reads the real DECISION_LOG.md
(a governance document) to confirm it holds no run authorisation.
"""
import contextlib
import csv
import hashlib
import io
import json
import os
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "literature"))
import pubrecords as pr  # noqa: E402
import stage0  # noqa: E402
import pilot_sample as ps  # noqa: E402
import pilot_sheet as sheet  # noqa: E402

COMMIT = "a" * 40
SHA_C = "b" * 64
SHA_P = "c" * 64
VERSION = "criteria_vX.Y+protocol_vX.Z"   # fixture identifier; the real one is set at the freeze (B1)


def rec(pid, types="", queries="Q-PM-01", themes=""):
    return {"paper_id": pid, "query_ids": queries, "source_publication_types": types, "retrieval_themes": themes}


class FixtureDir:
    """Temporary repo-like tree: <tmp>/research/literature and <tmp>/logs/DECISION_LOG.md."""

    def __init__(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.lit = self.root / "research" / "literature"
        (self.lit / "screening").mkdir(parents=True)
        (self.root / "logs").mkdir()
        self.log = self.root / "logs" / "DECISION_LOG.md"
        self.log.write_text("| ID | Decision |\n|---|---|\n", encoding="utf-8")

    def cleanup(self):
        self._tmp.cleanup()

    def entry(self, **over):
        e = {"criteria_version": VERSION, "decision_id": "D-999", "criteria_path": "c.md", "protocol_path": "p.md",
             "freeze_commit": COMMIT, "criteria_sha256": SHA_C, "protocol_sha256": SHA_P,
             "effective_date": "2099-01-01"}
        e.update(over)
        return e

    def log_row(self, decision_id="D-999", text=None):
        text = text or f"freeze {VERSION} commit {COMMIT} sha {SHA_C} {SHA_P}"
        with open(self.log, "a", encoding="utf-8") as f:
            f.write(f"| {decision_id} | {text} |\n")

    def add_auth(self, decision_id, clause, status="**APPROVED**", marker=True):
        text = (pr.RUN_AUTHORISATION_MARKERS[clause] + ": fixture") if marker else f"mentions {clause} only"
        with open(self.log, "a", encoding="utf-8") as f:
            f.write(f"| {decision_id} | 2099-01-01 (TEST) | {text} | {status} | r | researcher |\n")

    def registry(self, entries=None, raw=None):
        p = self.lit / pr.CRITERIA_REGISTRY_FILE
        p.write_text(raw if raw is not None else json.dumps({"frozen_versions": entries}), encoding="utf-8")

    def decisions(self, rows, header=None):
        header = header or pr.SCREENING_REQUIRED + ["criteria_version"]
        with open(self.lit / "screening" / "decisions.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)


def union_of(recs):
    return {r["paper_id"]: stage0.split_types(r["source_publication_types"]) for r in recs}


def stage0_row(pid="P0001", version=VERSION):
    return [pid, "title_abstract", "exclude", "E5", "rule:stage0", "2099-01-01", "Stage 0", version]


# ------------------------------------------------------------------ A: Stage-0 generator
class Stage0Rules(unittest.TestCase):
    def test_single_types(self):
        for t in ("Editorial", "Comment", "News", "Published Erratum"):
            self.assertEqual(stage0.classify([t]), ("E5", "b"), t)
        self.assertEqual(stage0.classify(["Retracted Publication"]), ("E7", "a"))

    def test_letter_and_retraction_notice_not_stage0(self):
        self.assertIsNone(stage0.classify(["Letter"]))
        self.assertIsNone(stage0.classify(["Retraction of Publication"]))
        self.assertEqual(stage0.classify(["Retraction of Publication", "Retracted Publication"]), ("E7", "a"))

    def test_e7_over_e5(self):
        self.assertEqual(stage0.classify(["Editorial", "Retracted Publication"]), ("E7", "a"))
        self.assertEqual(stage0.classify(["Journal Article", "Retracted Publication"]), ("E7", "a"))

    def test_mixed_types(self):
        self.assertEqual(stage0.classify(["Comment", "Research Support, Non-U.S. Gov't"]), ("E5", "b"))
        self.assertIsNone(stage0.classify(["Comment", "Journal Article"]))
        self.assertIsNone(stage0.classify(["Comment", "Letter"]))
        self.assertIsNone(stage0.classify(["Comment", "Some Unknown Type"]))
        self.assertIsNone(stage0.classify(["Research Support, Non-U.S. Gov't"]))   # no Stage-0 E5 type
        self.assertIsNone(stage0.classify([]))

    def test_clinical_trial_protocol_never_qualifies(self):
        self.assertIsNone(stage0.classify(["Comment", "Clinical Trial Protocol"]))
        self.assertNotIn("Clinical Trial Protocol", stage0.KEEP_NOT_USED_TYPES)
        self.assertEqual(stage0.unsupported_variants(["Clinical Trial Protocol"]), [])

    def test_unsupported_variants_stop(self):
        for t in ("Clinical Trial, Phase IV", "Research Support, American Recovery and Reinvestment Act"):
            with self.assertRaisesRegex(stage0.Stage0Error, "unsupported publication-type variants"):
                stage0.generate_rows([rec("P0001", f"Comment;{t}")], {"P0001": ["Comment", t]}, "2099-01-01", VERSION)

    def test_a1_guard_union_disagreement(self):
        with self.assertRaisesRegex(stage0.Stage0Error, "A1 guard"):
            stage0.generate_rows([rec("P0001", "Journal Article")],
                                 {"P0001": ["Journal Article", "Retracted Publication"]}, "2099-01-01", VERSION)
        with self.assertRaisesRegex(stage0.Stage0Error, "member-type union missing"):
            stage0.generate_rows([rec("P0001", "Comment")], {}, "2099-01-01", VERSION)

    def test_rows_and_template(self):
        recs = [rec("P0002", "Editorial;Retracted Publication"), rec("P0001", "News"),
                rec("P0003", "Journal Article"), rec("P0004", "Comment", queries="Q-PM-04")]
        union = {r["paper_id"]: stage0.split_types(r["source_publication_types"]) for r in recs}
        rows, report = stage0.generate_rows(recs, union, "2099-01-01", VERSION)
        self.assertEqual([r["paper_id"] for r in rows], ["P0001", "P0002"])     # scope + order
        self.assertEqual(rows[0], {"paper_id": "P0001", "stage": "title_abstract", "decision": "exclude",
                                   "reason_code": "E5", "screener": "rule:stage0", "date": "2099-01-01",
                                   "justification": "Stage 0 (D-074 (b)): source publication types = News; E5",
                                   "criteria_version": VERSION})
        self.assertEqual(rows[1]["justification"],
                         "Stage 0 (D-074 (a)): source publication types = Editorial;Retracted Publication; E7")
        self.assertEqual((report["in_scope"], report["E5"], report["E7"], report["not_stage0"]), (3, 1, 1, 1))

    def test_idempotent_against_existing_rows(self):
        recs = [rec("P0001", "News")]
        union = {"P0001": ["News"]}
        existing = [{"paper_id": "P0001", "screener": "rule:stage0", "criteria_version": VERSION}]
        rows, report = stage0.generate_rows(recs, union, "2099-01-01", VERSION, existing)
        self.assertEqual((rows, report["skipped_existing"]), ([], ["P0001"]))
        rows, report = stage0.generate_rows(recs, union, "2099-01-01", VERSION + "b", existing)
        self.assertEqual((rows, report["existing_other_version"]), ([], ["P0001"]))

    def test_input_gates(self):
        union = {"P0001": ["News"]}
        for bad in ("", " ", "has space"):
            with self.assertRaises(stage0.Stage0Error):
                stage0.generate_rows([rec("P0001", "News")], union, "2099-01-01", bad)
        with self.assertRaisesRegex(stage0.Stage0Error, "invalid paper_id"):
            stage0.generate_rows([rec("X1", "News")], {"X1": ["News"]}, "2099-01-01", VERSION)
        with self.assertRaisesRegex(stage0.Stage0Error, "duplicate"):
            stage0.generate_rows([rec("P0001", "News"), rec("P0001", "News")], union, "2099-01-01", VERSION)

    def test_utc_run_date_format(self):
        self.assertRegex(stage0.utc_run_date(), r"^\d{4}-\d{2}-\d{2}$")

    def test_generated_rows_pass_validator(self):
        fx = FixtureDir()
        self.addCleanup(fx.cleanup)
        fx.log_row()
        fx.registry([fx.entry()])
        rows, _ = stage0.generate_rows([rec("P0001", "News")], {"P0001": ["News"]}, "2099-01-01", VERSION)
        fx.decisions([[r[k] for k in pr.SCREENING_REQUIRED + ["criteria_version"]] for r in rows])
        self.assertEqual(len(pr.load_screening_decisions(fx.lit)), 1)

    def test_cli_refuses_without_frozen_version(self):
        fx = FixtureDir()
        self.addCleanup(fx.cleanup)
        fx.add_auth("D-901", "D-074 (f)")
        with self.assertRaises(SystemExit) as cm:
            stage0.main(["--lit-dir", str(fx.lit), "--authorization", "D-901", "--expected-inventory-sha256", "0",
                         "--criteria-version", VERSION])
        self.assertIn("not a registered frozen version", str(cm.exception))
        for ref in (" ", "D-999"):
            with self.assertRaises(SystemExit) as cm:
                stage0.main(["--lit-dir", str(fx.lit), "--authorization", ref, "--expected-inventory-sha256", "0",
                             "--criteria-version", VERSION])
            self.assertIn("refused", str(cm.exception))


# ------------------------------------------------------------------ B: criteria-version registry
class CriteriaRegistry(unittest.TestCase):
    def setUp(self):
        self.fx = FixtureDir()
        self.addCleanup(self.fx.cleanup)

    def test_no_registry_keeps_previous_behaviour(self):
        self.assertIsNone(pr.load_criteria_registry(self.fx.lit))
        self.fx.decisions([stage0_row(version="")])
        self.assertEqual(len(pr.load_screening_decisions(self.fx.lit)), 1)

    def test_malformed_version_rejected_without_registry(self):
        self.fx.decisions([stage0_row(version="has space")])
        with self.assertRaisesRegex(ValueError, "malformed criteria_version"):
            pr.load_screening_decisions(self.fx.lit)

    def test_registered_version_accepted(self):
        self.fx.log_row()
        self.fx.registry([self.fx.entry()])
        self.assertEqual(pr.load_criteria_registry(self.fx.lit), frozenset({VERSION}))
        self.fx.decisions([stage0_row()])
        self.assertEqual(len(pr.load_screening_decisions(self.fx.lit)), 1)

    def test_missing_draft_or_wrong_version_rejected(self):
        self.fx.log_row()
        self.fx.registry([self.fx.entry()])
        for v, msg in (("", "required once a frozen version"),
                       ("criteria_v1.1+protocol_v0.2", "not a registered frozen version"),
                       ("other", "not a registered frozen version")):
            self.fx.decisions([stage0_row(version=v)])
            with self.assertRaisesRegex(ValueError, msg):
                pr.load_screening_decisions(self.fx.lit)

    def test_malformed_registry_fails_closed(self):
        self.fx.log_row()
        cases = [("raw", "{not json"), ("raw", "[]"), ("entries", []), ("entries", ["x"]),
                 ("entries", [self.fx.entry(freeze_commit="abc")]),
                 ("entries", [self.fx.entry(criteria_sha256="short")]),
                 ("entries", [self.fx.entry(effective_date="")]),
                 ("entries", [{k: v for k, v in self.fx.entry().items() if k != "decision_id"}])]
        for kind, value in cases:
            if kind == "raw":
                self.fx.registry(raw=value)
            else:
                self.fx.registry(value)
            with self.assertRaises(pr.CriteriaRegistryError, msg=repr(value)):
                pr.load_criteria_registry(self.fx.lit)

    def test_contradictory_or_unconfirmed_registry_fails_closed(self):
        self.fx.log_row()
        self.fx.registry([self.fx.entry(), self.fx.entry(effective_date="2099-02-02")])
        with self.assertRaisesRegex(pr.CriteriaRegistryError, "contradictory"):
            pr.load_criteria_registry(self.fx.lit)
        self.fx.registry([self.fx.entry(decision_id="D-998")])
        with self.assertRaisesRegex(pr.CriteriaRegistryError, "not found"):
            pr.load_criteria_registry(self.fx.lit)
        self.fx.log_row("D-997", "freeze without hashes")
        self.fx.registry([self.fx.entry(decision_id="D-997")])
        with self.assertRaisesRegex(pr.CriteriaRegistryError, "does not state"):
            pr.load_criteria_registry(self.fx.lit)

    def test_missing_decision_log_fails_closed(self):
        self.fx.registry([self.fx.entry()])
        self.fx.log.unlink()
        with self.assertRaisesRegex(pr.CriteriaRegistryError, "decision log"):
            pr.load_criteria_registry(self.fx.lit)

    def test_validator_fails_closed_on_bad_registry(self):
        self.fx.registry(raw="{")
        self.fx.decisions([stage0_row()])
        with self.assertRaises(pr.CriteriaRegistryError):
            pr.load_screening_decisions(self.fx.lit)

    def test_schema_pattern_is_format_only(self):
        schema = json.loads((REPO / "research/literature/schemas/screening_decision.schema.json").read_text())
        pat = schema["properties"]["criteria_version"]["pattern"]
        import re
        for ok in ("", "v0.1", "criteria_v1.1+protocol_v0.2", VERSION):
            self.assertRegex(ok, pat)
        for bad in ("has space", " lead", "a/b"):
            self.assertNotRegex(bad, pat)
        self.assertNotIn("criteria_version", schema["required"])

    def test_real_repository_has_no_registry(self):
        self.assertFalse((REPO / "research/literature" / pr.CRITERIA_REGISTRY_FILE).exists())


# ------------------------------------------------------------------ C: pilot sampler
def reference_draw(frame, allocation, seed):
    """Independent restatement of D-077 (1)-(4) for cross-checking."""
    rng = random.Random(seed)
    out = []
    for s in ("F", "D", "C", "E", "A", "Q", "B", "untagged"):
        ids = sorted(frame.get(s, []), key=lambda p: int(p[1:]))
        pairs = [(rng.random(), p) for p in ids]
        out += [(p, s) for _, p in sorted(pairs)[:allocation.get(s, 0)]]
    return sorted(out, key=lambda x: (("F", "D", "C", "E", "A", "Q", "B", "untagged").index(x[1]), int(x[0][1:])))


class PilotSampler(unittest.TestCase):
    def test_approved_parameters_preserved(self):
        self.assertEqual((ps.SAMPLE_SIZE, ps.SEED, ps.APPROVED_FRAME_SIZE), (60, 4004, 1463))
        self.assertEqual(ps.ALLOCATION, {"F": 8, "D": 7, "C": 7, "E": 7, "A": 8, "Q": 7, "B": 8, "untagged": 8})
        self.assertEqual(ps.STRATUM_ORDER, ("F", "D", "C", "E", "A", "Q", "B", "untagged"))
        self.assertEqual(ps.RAREST_THEME_ORDER, ("F", "D", "C", "E", "A", "Q", "B"))
        self.assertEqual(ps.APPROVED_STRATUM_SIZES,
                         {"B": 623, "A": 365, "untagged": 173, "F": 120, "C": 93, "E": 68, "D": 13, "Q": 8})
        self.assertEqual(sum(ps.APPROVED_STRATUM_SIZES.values()), ps.APPROVED_FRAME_SIZE)

    def test_rarest_theme(self):
        self.assertEqual(ps.stratum_of("B;F"), "F")
        self.assertEqual(ps.stratum_of("A;Q;B"), "A")
        self.assertEqual(ps.stratum_of(""), "untagged")

    def test_frame_excludes_stage0_and_out_of_scope(self):
        recs = [rec("P0001", "Journal Article", themes="B"), rec("P0002", "Editorial", themes="B"),
                rec("P0003", "Journal Article", queries="Q-PM-04", themes="B"), rec("P0004", "Letter", themes="")]
        frame = ps.build_frame(recs, union_of(recs))
        self.assertEqual((frame["B"], frame["untagged"]), (["P0001"], ["P0004"]))

    def test_frame_mismatch_stops(self):
        frame = {"B": ["P0001", "P0002"], "untagged": []}
        self.assertEqual(ps.verify_frame(frame, 2, {"B": 2, "untagged": 0}), {"B": 2, "untagged": 0})
        with self.assertRaisesRegex(ps.PilotSampleError, "frame mismatch"):
            ps.verify_frame(frame, 3, {"B": 2, "untagged": 0})
        with self.assertRaisesRegex(ps.PilotSampleError, "frame mismatch"):
            ps.verify_frame(frame, 2, {"B": 1, "untagged": 1})
        with self.assertRaisesRegex(ps.PilotSampleError, "frame mismatch"):
            ps.verify_frame(frame)                       # approved record, not this fixture

    def test_draw_matches_d077_and_is_deterministic(self):
        frame = {s: [f"P{1000 + 37 * i + n}" for n in range(15)] for i, s in enumerate(ps.STRATUM_ORDER)}
        a = ps.draw(frame)
        self.assertEqual(a, ps.draw(frame))
        self.assertEqual(a, reference_draw(frame, ps.ALLOCATION, 4004))
        self.assertEqual(len(a), 60)
        for s, k in ps.ALLOCATION.items():
            self.assertEqual(sum(1 for _, x in a if x == s), k)
        self.assertEqual(len({p for p, _ in a}), 60)
        self.assertNotEqual(a, ps.draw(frame, seed=4005))

    def test_allocation_exceeding_stratum_stops(self):
        with self.assertRaisesRegex(ps.PilotSampleError, "exceeds"):
            ps.draw({"F": ["P0001"]})

    def test_duplicate_ids_stop(self):
        recs = [rec("P0001", "Journal Article"), rec("P0001", "Journal Article")]
        with self.assertRaises(ps.PilotSampleError):
            ps.build_frame(recs, union_of(recs))

    def test_duplicate_pairs_reported_not_removed(self):
        rep = ps.duplicate_pairs_in_sample(["P0001", "P0005"], [("P0001", "P0002"), ("P0003", "P0004"),
                                                                ("P0005", "P0001")])
        self.assertEqual(rep, [{"paper_id_a": "P0001", "paper_id_b": "P0002", "drawn": ["P0001"]},
                               {"paper_id_a": "P0005", "paper_id_b": "P0001", "drawn": ["P0001", "P0005"]}])

    def test_sample_rows_and_sidecar(self):
        rows = ps.sample_rows([("P0001", "F")], "d" * 64)
        self.assertEqual(rows, [{"paper_id": "P0001", "stratum": "F", "seed": "4004", "inventory_sha256": "d" * 64,
                                 "sampling_script": "scripts/literature/pilot_sample.py"}])
        meta = ps.sidecar([("P0001", "F")], "d" * 64, "D-999", {"F": 1}, [], COMMIT, "e" * 64, "2099-01-01T00:00:00+00:00")
        for k in ("sampling_script", "script_commit", "script_sha256", "run_time_utc", "authorization",
                  "inventory_sha256", "seed", "allocation", "stratum_sizes", "duplicate_pairs_in_sample"):
            self.assertIn(k, meta)

    def test_cli_refuses_without_authorisation_or_freeze(self):
        fx = FixtureDir()
        self.addCleanup(fx.cleanup)
        fx.add_auth("D-901", "D-074 (f)")          # wrong clause for the draw
        fx.add_auth("D-902", "D-077 (6)")
        for ref in (" ", "D-999", "D-901"):
            with self.assertRaises(SystemExit) as cm:
                ps.main(["--lit-dir", str(fx.lit), "--authorization", ref, "--expected-inventory-sha256", "0"])
            self.assertIn("refused", str(cm.exception))
        with self.assertRaises(SystemExit) as cm:
            ps.main(["--lit-dir", str(fx.lit), "--authorization", "D-902", "--expected-inventory-sha256", "0"])
        self.assertIn("freeze required", str(cm.exception))


# ------------------------------------------------------------------ D: blinded pilot sheet
PUBS = {
    "P0002": {"title": "T2", "abstract": "A2", "year": 2020, "journal": "J2",
              "publication_types": ["Journal Article", "Comment"], "publication_type": "editorial_comment_letter",
              "screening_decision": "exclude", "exclusion_reason": "E5", "rq5_coverage_group": "qualified",
              "screening_details": {"rq_tags": "RQ1"}, "verification_status": "verified"},
    "P0001": {"title": "T1", "abstract": "[Abstract not available]", "year": None, "journal": "",
              "publication_types": ["Letter"]},
}


class BlindedSheet(unittest.TestCase):
    def test_allow_list_and_no_leak(self):
        rows = sheet.build_rows(["P0002", "P0001"], PUBS, {"P0001": "unavailable — PubMed"})
        self.assertEqual(sheet.ALLOWED_COLUMNS, ["paper_id", "title", "abstract", "abstract_status", "year",
                                                 "venue", "types"])
        for r in rows:
            self.assertEqual(list(r), sheet.ALLOWED_COLUMNS)
        text = json.dumps(rows)
        for leaked in ("exclude", "E5", "qualified", "RQ1", "verified", "editorial_comment_letter"):
            self.assertNotIn(leaked, text)

    def test_verbatim_types_order_and_missing_values(self):
        rows = sheet.build_rows(["P0002", "P0001"], PUBS, {"P0001": "unavailable — PubMed"})
        self.assertEqual([r["paper_id"] for r in rows], ["P0001", "P0002"])
        self.assertEqual(rows[1]["types"], "Journal Article;Comment")
        self.assertEqual((rows[0]["abstract"], rows[0]["abstract_status"], rows[0]["year"], rows[0]["venue"]),
                         ("", "unavailable — PubMed", "", ""))
        self.assertEqual((rows[1]["year"], rows[1]["abstract_status"]), ("2020", ""))

    def test_missing_abstract_needs_recorded_status(self):
        with self.assertRaisesRegex(sheet.PilotSheetError, "not inferred"):
            sheet.build_rows(["P0001"], PUBS)
        with self.assertRaisesRegex(sheet.PilotSheetError, "not a D-068"):
            sheet.build_rows(["P0001"], PUBS, {"P0001": "gone"})
        with self.assertRaisesRegex(sheet.PilotSheetError, "has an abstract"):
            sheet.build_rows(["P0002"], PUBS, {"P0002": "unavailable"})

    def test_row_set_integrity(self):
        with self.assertRaisesRegex(sheet.PilotSheetError, "duplicate"):
            sheet.build_rows(["P0002", "P0002"], PUBS)
        with self.assertRaisesRegex(sheet.PilotSheetError, "not found"):
            sheet.build_rows(["P0003"], PUBS)
        with self.assertRaises(sheet.PilotSheetError):
            sheet.check_columns(sheet.ALLOWED_COLUMNS + ["exclusion_reason"])
        with self.assertRaises(sheet.PilotSheetError):
            sheet.check_columns(list(reversed(sheet.ALLOWED_COLUMNS)))

    def test_default_filename(self):
        self.assertEqual(sheet.DEFAULT_SHEET, "screening/pilot_sheet_researcher.csv")


class SheetOutputPaths(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        (self.repo / ".gitignore").write_text("ignored/\n", encoding="utf-8")
        self.rows = sheet.build_rows(["P0002"], PUBS)
        self.log = self.root / "DECISION_LOG.md"
        self.log.write_text(f"| D-902 | 2099-01-01 (TEST) | {pr.RUN_AUTHORISATION_MARKERS['D-077 (6)']} | "
                            f"**APPROVED** | r | researcher |\n", encoding="utf-8")

    def write(self, path, ref="D-902"):
        return sheet.write_sheet(self.rows, path, ["P0002"], ref, decision_log=self.log)

    def test_writes_only_to_ignored_path(self):
        out = self.write(self.repo / "ignored" / "sheet.csv")
        with open(out, newline="", encoding="utf-8") as f:
            data = list(csv.reader(f))
        self.assertEqual(data[0], sheet.ALLOWED_COLUMNS)
        self.assertEqual(len(data), 2)

    def test_refuses_non_ignored_or_outside_repo(self):
        for p in (self.repo / "tracked_dir" / "sheet.csv", self.root / "outside" / "sheet.csv"):
            with self.assertRaisesRegex(sheet.PilotSheetError, "not ignored by Git"):
                self.write(p)
            self.assertFalse(p.exists())

    def test_refuses_without_authorisation_or_existing_file(self):
        for ref in (" ", "D-999"):
            with self.assertRaisesRegex(sheet.PilotSheetError, "refused"):
                self.write(self.repo / "ignored" / "a.csv", ref)
        with self.assertRaisesRegex(sheet.PilotSheetError, "no decision log"):
            sheet.write_sheet(self.rows, self.repo / "ignored" / "a.csv", ["P0002"], "D-902")
        self.assertFalse((self.repo / "ignored" / "a.csv").exists())
        self.write(self.repo / "ignored" / "b.csv")
        with self.assertRaisesRegex(sheet.PilotSheetError, "already exists"):
            self.write(self.repo / "ignored" / "b.csv")

    def test_default_path_in_this_repository_is_not_ignored(self):
        """D4 deferred: the default sheet path is not ignored yet, so the tool must refuse it."""
        self.assertFalse(sheet.path_is_git_ignored(REPO / "research/literature" / sheet.DEFAULT_SHEET))



# ------------------------------------------------------------------ Phase 1 corrections (2026-11-11)
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class ToolFixture(FixtureDir):
    """FixtureDir plus a synthetic inventory, publications.jsonl and source_records.jsonl."""

    def write_data(self, pubs):
        """pubs: list of dicts with paper_id, query_ids, themes, member_types (list of lists) and
        optional title/abstract/year/journal; the publication-level types are the first member's."""
        (self.lit / "records").mkdir(exist_ok=True)
        inv, src, pub_lines = [], [], []
        for p in pubs:
            members = p["member_types"]
            prov = []
            for i, types in enumerate(members):
                sid = f"SR-{p['paper_id']}-{i}"
                src.append({"source_record_id": sid, "publication_types": types})
                prov.append({"source_record_id": sid, "query_id": "Q-PM-01"})
            inv.append({"paper_id": p["paper_id"], "query_ids": p.get("query_ids", "Q-PM-01"),
                        "source_publication_types": ";".join(members[0]), "retrieval_themes": p.get("themes", "")})
            pub_lines.append({"paper_id": p["paper_id"], "search_provenance": prov, "publication_types": members[0],
                              "title": p.get("title", "T"), "abstract": p.get("abstract", "A"),
                              "year": p.get("year", 2020), "journal": p.get("journal", "J")})
        (self.lit / "paper_inventory.json").write_text(json.dumps(inv), encoding="utf-8")
        with open(self.lit / "records" / "source_records.jsonl", "w", encoding="utf-8") as f:
            f.writelines(json.dumps(r) + "\n" for r in src)
        with open(self.lit / "records" / "publications.jsonl", "w", encoding="utf-8") as f:
            f.writelines(json.dumps(r) + "\n" for r in pub_lines)
        return sha(self.lit / "paper_inventory.json")


class RunAuthorisation(unittest.TestCase):
    def setUp(self):
        self.fx = FixtureDir()
        self.addCleanup(self.fx.cleanup)
        self.fx.add_auth("D-901", "D-074 (f)")
        self.fx.add_auth("D-902", "D-077 (6)")
        self.fx.add_auth("D-903", "D-074 (f)", status="**APPROVED — CONDITIONAL (inactive)**")
        self.fx.add_auth("D-904", "D-074 (f)", status="**APPROVED IN PRINCIPLE**")
        self.fx.add_auth("D-905", "D-074 (f)", marker=False)
        self.fx.add_auth("D-906", "D-077 (6)")
        self.fx.add_auth("D-906", "D-077 (6)")

    def test_valid_references(self):
        self.assertEqual(pr.verify_run_authorisation(self.fx.lit, "D-901", "D-074 (f)"), "D-901")
        self.assertEqual(pr.verify_run_authorisation(self.fx.lit, " D-902 ", "D-077 (6)"), "D-902")

    def test_invented_malformed_or_unauthorising_references(self):
        cases = [("D-999", "D-074 (f)", "not a decision"), ("D-99", "D-074 (f)", "not a decision ID"),
                 ("", "D-074 (f)", "not a decision ID"), ("abc", "D-077 (6)", "not a decision ID"),
                 ("D-901", "D-077 (6)", "does not state"), ("D-902", "D-074 (f)", "does not state"),
                 ("D-903", "D-074 (f)", "not an unconditional approval"),
                 ("D-904", "D-074 (f)", "not an unconditional approval"),
                 ("D-905", "D-074 (f)", "does not state"), ("D-906", "D-077 (6)", "more than one")]
        for ref, clause, msg in cases:
            with self.assertRaisesRegex(pr.RunAuthorisationError, msg, msg=(ref, clause)):
                pr.verify_run_authorisation(self.fx.lit, ref, clause)
        with self.assertRaisesRegex(pr.RunAuthorisationError, "unknown authorisation clause"):
            pr.verify_run_authorisation(self.fx.lit, "D-901", "D-099 (z)")

    def test_missing_decision_log(self):
        self.fx.log.unlink()
        with self.assertRaisesRegex(pr.RunAuthorisationError, "not found"):
            pr.verify_run_authorisation(self.fx.lit, "D-901", "D-074 (f)")

    def test_real_decision_log_holds_no_run_authorisation(self):
        """No existing decision (including D-074, D-077, D-080 to D-087) authorises a real run."""
        log = REPO / "logs" / "DECISION_LOG.md"
        ids = sorted({line.split("|")[1].strip() for line in log.read_text(encoding="utf-8").splitlines()
                      if line.startswith("| D-")})
        for must in ("D-074", "D-077", "D-084"):
            self.assertIn(must, ids)          # the parse found the decision table
        for ref in ids:
            for clause in pr.RUN_AUTHORISATION_MARKERS:
                with self.assertRaises(pr.RunAuthorisationError, msg=(ref, clause)):
                    pr.verify_run_authorisation(REPO / "research" / "literature", ref, clause)


class Stage0Corrections(unittest.TestCase):
    def setUp(self):
        self.fx = ToolFixture()
        self.addCleanup(self.fx.cleanup)
        self.fx.log_row()
        self.fx.registry([self.fx.entry()])
        self.fx.add_auth("D-901", "D-074 (f)")
        self.inv_sha = self.fx.write_data([
            {"paper_id": "P0001", "member_types": [["News"]]},
            {"paper_id": "P0002", "member_types": [["Journal Article"], ["Journal Article"]]},
            {"paper_id": "P0003", "member_types": [["Journal Article", "Retracted Publication"]]},
            {"paper_id": "P0004", "member_types": [["Clinical Trial, Phase IV"]], "query_ids": "Q-PM-04"}])
        self.path = self.fx.lit / "screening" / "decisions.csv"

    def run_cli(self, *extra):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            stage0.main(["--lit-dir", str(self.fx.lit), "--authorization", "D-901", "--expected-inventory-sha256",
                         self.inv_sha, "--criteria-version", VERSION, *extra])
        return json.loads(buf.getvalue())

    def test_cli_write_path_hashes_and_idempotence(self):
        report = self.run_cli("--write")
        self.assertTrue(report["written"])
        self.assertEqual(report["new_rows"], 2)
        self.assertEqual(report["publications_jsonl_sha256"], sha(self.fx.lit / "records" / "publications.jsonl"))
        self.assertEqual(report["source_records_jsonl_sha256"], sha(self.fx.lit / "records" / "source_records.jsonl"))
        self.assertEqual(report["inventory_sha256"], self.inv_sha)
        self.assertEqual(report["authorization"], "D-901")
        rows = pr.load_screening_decisions(self.fx.lit)
        self.assertEqual([(r["paper_id"], r["reason_code"]) for r in rows], [("P0001", "E5"), ("P0003", "E7")])
        before = self.path.read_bytes()
        again = self.run_cli("--write")
        self.assertEqual((again["new_rows"], again["written"], again["skipped_existing"]), (0, False, ["P0001", "P0003"]))
        self.assertEqual(self.path.read_bytes(), before)

    def test_dry_run_writes_nothing(self):
        report = self.run_cli()
        self.assertEqual((report["new_rows"], report["written"]), (2, False))
        self.assertFalse(self.path.exists())

    def test_out_of_scope_unsupported_variant_does_not_stop(self):
        self.assertEqual(self.run_cli()["in_scope"], 3)     # P0004 (Phase IV) is outside D-044

    def test_cli_refuses_hash_mismatch(self):
        with self.assertRaisesRegex(SystemExit, "inventory SHA-256"):
            stage0.main(["--lit-dir", str(self.fx.lit), "--authorization", "D-901", "--expected-inventory-sha256",
                         "0" * 64, "--criteria-version", VERSION])

    def _existing(self):
        self.fx.decisions([stage0_row("P0009")])
        return self.path.read_bytes()

    def assert_unchanged(self, before):
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual([p.name for p in self.path.parent.iterdir()], ["decisions.csv"])   # no temp file left

    def test_atomic_write_invalid_combined_content_leaves_file_unchanged(self):
        before = self._existing()
        bad = {"paper_id": "P0001", "stage": "title_abstract", "decision": "exclude", "reason_code": "E99",
               "screener": "rule:stage0", "date": "2099-01-01", "justification": "x", "criteria_version": VERSION}
        with self.assertRaises(ValueError):
            stage0.write_rows_atomically(self.fx.lit, [bad])
        self.assert_unchanged(before)

    def test_atomic_write_validation_failure_leaves_file_unchanged(self):
        before = self._existing()
        rows, _ = stage0.generate_rows([rec("P0001", "News")], {"P0001": ["News"]}, "2099-01-01", VERSION)
        with mock.patch.object(stage0, "_validate_candidate", side_effect=ValueError("forced")):
            with self.assertRaisesRegex(ValueError, "forced"):
                stage0.write_rows_atomically(self.fx.lit, rows)
        self.assert_unchanged(before)
        stage0.write_rows_atomically(self.fx.lit, rows)              # the real validation passes
        self.assertEqual(len(pr.load_screening_decisions(self.fx.lit)), 2)

    def test_existing_file_without_criteria_version_column_refused(self):
        self.fx.decisions([[*stage0_row("P0009")[:7]]], header=pr.SCREENING_REQUIRED)
        before = self.path.read_bytes()
        rows, _ = stage0.generate_rows([rec("P0001", "News")], {"P0001": ["News"]}, "2099-01-01", VERSION)
        with self.assertRaisesRegex(SystemExit, "no criteria_version column"):
            stage0.write_rows_atomically(self.fx.lit, rows)
        self.assertEqual(self.path.read_bytes(), before)

    def test_invalid_calendar_dates(self):
        for bad in ("2026-02-30", "2026-13-01", "2026-1-01", "20260101", "", None, "2026-11-11T00:00"):
            with self.assertRaisesRegex(stage0.Stage0Error, "calendar date", msg=repr(bad)):
                stage0.generate_rows([rec("P0001", "News")], {"P0001": ["News"]}, bad, VERSION)
        rows, _ = stage0.generate_rows([rec("P0001", "News")], {"P0001": ["News"]}, "2028-02-29", VERSION)
        self.assertEqual(rows[0]["date"], "2028-02-29")

    def test_union_missing_source_record_stops(self):
        with open(self.fx.lit / "records" / "source_records.jsonl", "w", encoding="utf-8") as f:
            f.write("")
        with self.assertRaisesRegex(stage0.Stage0Error, "not found"):
            stage0.load_member_union(self.fx.lit)


class SamplerSharedGuards(unittest.TestCase):
    def test_unsupported_variant_in_scope_stops_frame(self):
        recs = [rec("P0001", "Comment;Clinical Trial, Phase IV")]
        with self.assertRaisesRegex(ps.PilotSampleError, "unsupported publication-type variants"):
            ps.build_frame(recs, union_of(recs))

    def test_union_disagreement_or_missing_union_stops_frame(self):
        recs = [rec("P0001", "Journal Article")]
        with self.assertRaisesRegex(ps.PilotSampleError, "disagree"):
            ps.build_frame(recs, {"P0001": ["Journal Article", "Retracted Publication"]})
        with self.assertRaisesRegex(ps.PilotSampleError, "union missing"):
            ps.build_frame(recs, {})

    def test_out_of_scope_records_not_type_checked(self):
        recs = [rec("P0001", "Journal Article", themes="B"),
                rec("P0002", "Comment;Clinical Trial, Phase IV", queries="Q-PM-04")]
        frame = ps.build_frame(recs, {"P0001": ["Journal Article"]})
        self.assertEqual(frame["B"], ["P0001"])

    def test_cli_frame_uses_shared_guards(self):
        fx = ToolFixture()
        self.addCleanup(fx.cleanup)
        fx.log_row()
        fx.registry([fx.entry()])
        fx.add_auth("D-902", "D-077 (6)")
        inv_sha = fx.write_data([{"paper_id": "P0001", "member_types": [["Journal Article"],
                                                                     ["Journal Article", "Retracted Publication"]]}])
        with self.assertRaisesRegex(ps.PilotSampleError, "disagree"):
            ps.main(["--lit-dir", str(fx.lit), "--authorization", "D-902", "--expected-inventory-sha256", inv_sha])


class RegistryDuplicates(unittest.TestCase):
    def test_identical_duplicate_entries_accepted_once(self):
        fx = FixtureDir()
        self.addCleanup(fx.cleanup)
        fx.log_row()
        fx.registry([fx.entry(), fx.entry()])
        self.assertEqual(pr.load_criteria_registry(fx.lit), frozenset({VERSION}))


class PilotSheetCli(unittest.TestCase):
    def setUp(self):
        self.fx = ToolFixture()
        self.addCleanup(self.fx.cleanup)
        self.fx.add_auth("D-902", "D-077 (6)")
        self.inv_sha = self.fx.write_data([
            {"paper_id": "P0001", "member_types": [["Journal Article"]], "title": "T1", "abstract": "A1"},
            {"paper_id": "P0002", "member_types": [["Letter"]], "title": "T2", "abstract": ""}])
        self.repo = self.fx.root / "outrepo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        (self.repo / ".gitignore").write_text("ignored/\n", encoding="utf-8")
        self.out = self.repo / "ignored" / "pilot_sheet_researcher.csv"
        self.status = self.fx.root / "status.json"
        self.status.write_text(json.dumps({"P0002": "unavailable — PubMed"}), encoding="utf-8")
        self.write_sample()

    def write_sample(self, **side_over):
        rows = [{"paper_id": "P0001", "stratum": "F", "seed": "4004", "inventory_sha256": self.inv_sha,
                 "sampling_script": ps.SCRIPT_RELPATH},
                {"paper_id": "P0002", "stratum": "D", "seed": "4004", "inventory_sha256": self.inv_sha,
                 "sampling_script": ps.SCRIPT_RELPATH}]
        path = self.fx.lit / "screening" / "pilot_sample.csv"
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=ps.SAMPLE_COLUMNS)
            w.writeheader()
            w.writerows(rows)
        side = {"sampling_script": ps.SCRIPT_RELPATH, "seed": 4004, "sample_size": 2, "inventory_sha256": self.inv_sha,
                "allocation": {"F": 1, "D": 1, "C": 0}, "authorization": "D-902"}
        side.update(side_over)
        path.with_suffix(".provenance.json").write_text(json.dumps(side), encoding="utf-8")

    def run_cli(self, ref="D-902"):
        with contextlib.redirect_stdout(io.StringIO()):
            return sheet.main(["--lit-dir", str(self.fx.lit), "--authorization", ref, "--abstract-status",
                               str(self.status), "--out", str(self.out)])

    def test_cli_writes_blinded_sheet(self):
        self.assertEqual(self.run_cli(), 0)
        with open(self.out, newline="", encoding="utf-8") as f:
            data = list(csv.reader(f))
        self.assertEqual(data[0], sheet.ALLOWED_COLUMNS)
        self.assertEqual([r[0] for r in data[1:]], ["P0001", "P0002"])
        self.assertEqual(data[2][3], "unavailable — PubMed")

    def test_cli_refuses_on_sample_sidecar_disagreement(self):
        for over in ({"seed": 4005}, {"sample_size": 3}, {"inventory_sha256": "0" * 64},
                     {"allocation": {"F": 2}}, {"sampling_script": "other.py"}, {"authorization": "D-903"}):
            self.write_sample(**over)
            with self.assertRaisesRegex(SystemExit, "refused", msg=over):
                self.run_cli()
            self.assertFalse(self.out.exists())

    def test_cli_refuses_when_inventory_changed_since_draw(self):
        (self.fx.lit / "paper_inventory.json").write_text("[]", encoding="utf-8")
        with self.assertRaisesRegex(SystemExit, "inventory changed"):
            self.run_cli()

    def test_cli_refuses_missing_sidecar_or_authorisation(self):
        with self.assertRaisesRegex(SystemExit, "refused"):
            self.run_cli("D-999")
        (self.fx.lit / "screening" / "pilot_sample.provenance.json").unlink()
        with self.assertRaisesRegex(SystemExit, "provenance sidecar"):
            self.run_cli()
        self.assertFalse(self.out.exists())


if __name__ == "__main__":
    unittest.main()
