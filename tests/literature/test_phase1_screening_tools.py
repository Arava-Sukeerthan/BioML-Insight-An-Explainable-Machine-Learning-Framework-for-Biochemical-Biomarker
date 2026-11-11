"""Phase 1 screening tools (researcher authorisation 2026-11-01): synthetic fixtures only.

Covers the approved decisions A1-A5 (Stage-0 generator), B2-B4 (frozen criteria-version registry
and validator), C1-C4 (pilot sampler) and D1-D3, D5 (blinded pilot sheet), and the five Phase 1
corrections (researcher authorisation 2026-11-11): verified run authorisation, atomic Stage-0 writes,
shared checked Stage-0 guards in the sampler, input-file SHA-256s, and input validation (calendar
dates; in-scope guards; sample/sidecar agreement). Stage B preparation (D-095, 2026-11-11): exact
D-088 status and bindings, single-use ledger (P16); frame identity against the D-044 snapshot (P17);
frame-only mode (P15); pilot agreement, template and adjudication queue (P18); D4 sheet path (D-096).
Pre-commit audit corrections (2026-11-11): Stage-0 rows before the draw (M2); adjudication evidence (M5);
all duplicate pairs in the queue (L3); run lock, ledger events, interrupted runs, no-overwrite outputs (L5).
No test reads the real inventory, the scope-snapshot CSV or the publications file, or writes inside
the repository; tests read the real DECISION_LOG.md and D-044_scope_snapshot.md (governance
documents) to confirm that no run authorisation exists and that the frame constants match the record.
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
import pilot_agreement as pa  # noqa: E402

COMMIT = "a" * 40
SHA_C = "b" * 64
SHA_P = "c" * 64
VERSION = "criteria_vX.Y+protocol_vX.Z"   # fixture identifier; the real one is set at the freeze (B1)
INV = "d" * 64                              # fixture inventory SHA-256
FREEZE_ID = "D-999"                         # fixture freeze entry
S6_IDS = [f"D-98{i}" for i in range(1, 7)]  # fixture D-035 §6 records, one per condition (D-092)


def bindings(inventory_sha256=INV, criteria_version=VERSION, freeze=FREEZE_ID, s6=None, single="yes"):
    """D-088 (4) bindings in the D-095 syntax (synthetic values)."""
    return (f" criteria_version: {criteria_version}; inventory_sha256: {inventory_sha256}; "
            f"freeze_entry: {freeze}; d035_s6_records: {', '.join(s6 or S6_IDS)}; single_use: {single}")


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
        self._freeze_written = self._s6_written = False

    def cleanup(self):
        self._tmp.cleanup()

    def entry(self, **over):
        e = {"criteria_version": VERSION, "decision_id": "D-999", "criteria_path": "c.md", "protocol_path": "p.md",
             "freeze_commit": COMMIT, "criteria_sha256": SHA_C, "protocol_sha256": SHA_P,
             "effective_date": "2099-01-01"}
        e.update(over)
        return e

    def row(self, decision_id, text, status="**APPROVED**"):
        with open(self.log, "a", encoding="utf-8") as f:
            f.write(f"| {decision_id} | 2099-01-01 (TEST) | {text} | {status} | r | researcher |\n")

    def log_row(self, decision_id=FREEZE_ID, text=None):
        """A decision row (the fixture freeze entry by default; written once)."""
        if decision_id == FREEZE_ID and text is None:
            if self._freeze_written:
                return
            self._freeze_written = True
        self.row(decision_id, text or f"freeze {VERSION} commit {COMMIT} sha {SHA_C} {SHA_P}")

    def base(self):
        """Freeze entry and the six D-035 §6 condition records that a complete authorisation binds."""
        self.log_row()
        if not self._s6_written:
            for i, d in enumerate(S6_IDS, start=1):
                self.row(d, f"**D-035 §6 condition {i} recorded as met.** (fixture)")
            self._s6_written = True

    def add_auth(self, decision_id, clause, status=None, marker=True, inventory_sha256=INV,
                 criteria_version=VERSION, binding=None):
        """A run-authorisation row in the D-088 form (complete unless overridden)."""
        self.base()
        b = bindings(inventory_sha256, criteria_version) if binding is None else binding
        text = (pr.RUN_AUTHORISATION_MARKERS[clause] + b) if marker else f"mentions {clause} only"
        self.row(decision_id, text, status or pr.RUN_AUTHORISATION_STATUS)

    def ledger_done(self, ref, clause, tool):
        """A completed run in the ledger (started, then completed)."""
        pr.record_authorisation_start(self.lit, ref, clause, tool, "2099-01-01T00:00:00+00:00")
        pr.record_authorisation_completion(self.lit, ref, clause, tool, "2099-01-01T00:00:01+00:00")

    def frozen(self):
        """Fixture freeze: decision row plus registry entry."""
        self.log_row()
        self.registry([self.entry()])

    def snapshot(self, ids, name=None):
        path = self.lit / (name or ps.SCOPE_SNAPSHOT_RELPATH)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write("paper_id,pmid\n" + "".join(f"{p},\n" for p in ids))
        return path

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
        self.fx = FixtureDir()
        self.addCleanup(self.fx.cleanup)
        self.fx.frozen()
        self.fx.add_auth("D-902", "D-077 (6)")

    def write(self, path, ref="D-902", inventory_sha256=INV):
        return sheet.write_sheet(self.rows, path, ["P0002"], ref, lit_dir=self.fx.lit, inventory_sha256=inventory_sha256)

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
        with self.assertRaisesRegex(sheet.PilotSheetError, "inventory SHA-256 differs"):
            self.write(self.repo / "ignored" / "a.csv", inventory_sha256="e" * 64)
        self.assertFalse((self.repo / "ignored" / "a.csv").exists())
        self.write(self.repo / "ignored" / "b.csv")
        with self.assertRaisesRegex(sheet.PilotSheetError, "already exists"):
            self.write(self.repo / "ignored" / "b.csv")

    def test_default_path_in_this_repository_is_ignored(self):
        """D4 (D-096): the default sheet path is now ignored by Git and untracked, so the tool may write it."""
        self.assertTrue(sheet.path_is_git_ignored(REPO / "research/literature" / sheet.DEFAULT_SHEET))



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
        self.fx.frozen()
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
        cases = [("D-977", "D-074 (f)", "not a decision"), ("D-99", "D-074 (f)", "not a decision ID"),
                 ("", "D-074 (f)", "not a decision ID"), ("abc", "D-077 (6)", "not a decision ID"),
                 ("D-901", "D-077 (6)", "does not begin with"), ("D-902", "D-074 (f)", "does not begin with"),
                 ("D-903", "D-074 (f)", "not an unconditional approval"),
                 ("D-904", "D-074 (f)", "not an unconditional approval"),
                 ("D-905", "D-074 (f)", "does not begin with"), ("D-906", "D-077 (6)", "more than one")]
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
        self.fx.frozen()
        self.inv_sha = self.fx.write_data([
            {"paper_id": "P0001", "member_types": [["News"]]},
            {"paper_id": "P0002", "member_types": [["Journal Article"], ["Journal Article"]]},
            {"paper_id": "P0003", "member_types": [["Journal Article", "Retracted Publication"]]},
            {"paper_id": "P0004", "member_types": [["Clinical Trial, Phase IV"]], "query_ids": "Q-PM-04"}])
        self.fx.add_auth("D-901", "D-074 (f)", inventory_sha256=self.inv_sha)
        self.path = self.fx.lit / "screening" / "decisions.csv"

    def run_cli(self, *extra):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            stage0.main(["--lit-dir", str(self.fx.lit), "--authorization", "D-901", "--expected-inventory-sha256",
                         self.inv_sha, "--criteria-version", VERSION, *extra])
        return json.loads(buf.getvalue())

    def test_cli_write_path_hashes_and_single_use(self):
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
        uses = pr.authorisation_uses(self.fx.lit)
        self.assertEqual([(u["authorization"], u["tool"], u["event"]) for u in uses],
                         [("D-901", "stage0", "started"), ("D-901", "stage0", "completed")])
        self.assertFalse((self.fx.lit / pr.RUN_LOCK_FILE).exists())     # lock released
        with self.assertRaisesRegex(SystemExit, "single use"):        # D-088 (4): one write per authorisation
            self.run_cli("--write")
        self.assertEqual(self.path.read_bytes(), before)
        again = self.run_cli()                                         # a dry run stays idempotent
        self.assertEqual((again["new_rows"], again["written"], again["skipped_existing"]), (0, False, ["P0001", "P0003"]))

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

    def test_cli_refuses_criteria_version_other_than_bound(self):
        with self.assertRaisesRegex(SystemExit, "criteria_version differs"):
            stage0.main(["--lit-dir", str(self.fx.lit), "--authorization", "D-901", "--expected-inventory-sha256",
                         self.inv_sha, "--criteria-version", VERSION + "b"])
        self.assertFalse(self.path.exists())

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
        fx.frozen()
        inv_sha = fx.write_data([{"paper_id": "P0001", "member_types": [["Journal Article"],
                                                                     ["Journal Article", "Retracted Publication"]]}])
        fx.add_auth("D-902", "D-077 (6)", inventory_sha256=inv_sha)
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
        self.fx.frozen()
        self.inv_sha = self.fx.write_data([
            {"paper_id": "P0001", "member_types": [["Journal Article"]], "title": "T1", "abstract": "A1"},
            {"paper_id": "P0002", "member_types": [["Letter"]], "title": "T2", "abstract": ""}])
        self.fx.add_auth("D-902", "D-077 (6)", inventory_sha256=self.inv_sha)
        self.fx.ledger_done("D-902", "D-077 (6)", "pilot_sample")       # the draw comes first
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

    def run_cli(self, ref="D-902", out=None):
        with contextlib.redirect_stdout(io.StringIO()):
            return sheet.main(["--lit-dir", str(self.fx.lit), "--authorization", ref, "--abstract-status",
                               str(self.status), "--out", str(out or self.out)])

    def test_cli_writes_blinded_sheet(self):
        self.assertEqual(self.run_cli(), 0)
        with open(self.out, newline="", encoding="utf-8") as f:
            data = list(csv.reader(f))
        self.assertEqual(data[0], sheet.ALLOWED_COLUMNS)
        self.assertEqual([r[0] for r in data[1:]], ["P0001", "P0002"])
        self.assertEqual(data[2][3], "unavailable — PubMed")
        self.assertEqual([(u["tool"], u["event"]) for u in pr.authorisation_uses(self.fx.lit)],
                         [("pilot_sample", "started"), ("pilot_sample", "completed"),
                          ("pilot_sheet", "started"), ("pilot_sheet", "completed")])
        self.assertEqual(sorted(p.name for p in self.out.parent.iterdir()), ["pilot_sheet_researcher.csv"])  # no temp
        other = self.repo / "ignored" / "second_sheet.csv"
        with self.assertRaisesRegex(SystemExit, "single use"):        # one sheet per authorisation
            self.run_cli(out=other)
        self.assertFalse(other.exists())

    def test_cli_refuses_on_sample_sidecar_disagreement(self):
        for over in ({"seed": 4005}, {"sample_size": 3}, {"inventory_sha256": "0" * 64},
                     {"allocation": {"F": 2}}, {"sampling_script": "other.py"}, {"authorization": "D-903"}):
            self.write_sample(**over)
            with self.assertRaisesRegex(SystemExit, "refused", msg=over):
                self.run_cli()
            self.assertFalse(self.out.exists())

    def test_cli_refuses_when_inventory_changed_since_draw(self):
        (self.fx.lit / "paper_inventory.json").write_text("[]", encoding="utf-8")
        with self.assertRaisesRegex(SystemExit, "inventory SHA-256 differs"):   # P16: bound inventory
            self.run_cli()
        self.assertFalse(self.out.exists())

    def test_cli_refuses_missing_sidecar_or_authorisation(self):
        with self.assertRaisesRegex(SystemExit, "refused"):
            self.run_cli("D-999")
        (self.fx.lit / "screening" / "pilot_sample.provenance.json").unlink()
        with self.assertRaisesRegex(SystemExit, "provenance sidecar"):
            self.run_cli()
        self.assertFalse(self.out.exists())



# ------------------------------------------------------------------ Q-090 / D-088: anchored marker
class RunAuthorisationMarkerAnchoring(unittest.TestCase):
    """The Decision cell must BEGIN with the exact bold marker (D-088; answers Q-090)."""

    M74 = "**Run authorisation under D-074 (f).**"
    M77 = "**Run authorisation under D-077 (6).**"
    BIND = bindings()
    STATUS = "**APPROVED** — run authorisation (single use)"

    def setUp(self):
        self.fx = FixtureDir()
        self.addCleanup(self.fx.cleanup)
        self.fx.frozen()
        self.fx.base()
        self.n = 910

    def row(self, decision, status=None, cell_prefix=" ", cell_suffix=" "):
        ref = f"D-{self.n}"
        self.n += 1
        with open(self.fx.log, "a", encoding="utf-8") as f:
            f.write(f"|{' ' if ref else ''}{ref} | 2099-01-01 (TEST) |{cell_prefix}{decision}{cell_suffix}| "
                    f"{status or self.STATUS} | r | researcher |\n")
        return ref

    def ok(self, ref, clause="D-074 (f)"):
        return pr.verify_run_authorisation(self.fx.lit, ref, clause)

    def refused(self, ref, clause="D-074 (f)", msg="refused"):
        with self.assertRaisesRegex(pr.RunAuthorisationError, msg, msg=(ref, clause)):
            pr.verify_run_authorisation(self.fx.lit, ref, clause)

    def test_markers_are_the_approved_bold_sentences(self):
        self.assertEqual(pr.RUN_AUTHORISATION_MARKERS, {"D-074 (f)": self.M74, "D-077 (6)": self.M77})

    def test_marker_at_beginning_accepted(self):
        self.assertEqual(self.ok(self.row(self.M74 + self.BIND)), "D-910")
        self.assertEqual(self.ok(self.row(self.M77 + self.BIND), "D-077 (6)"), "D-911")

    def test_surrounding_whitespace_ignored_explicitly(self):
        self.assertTrue(self.ok(self.row(self.M74 + self.BIND, cell_prefix="    ", cell_suffix="   ")))
        self.assertTrue(self.ok(self.row(self.M74 + self.BIND, cell_prefix="\t ")))

    def test_marker_in_middle_or_at_end_rejected(self):
        self.refused(self.row("Approved design." + " " + self.M74 + self.BIND), msg="does not begin with")
        self.refused(self.row("Binds the run." + self.BIND + " " + self.M74), msg="does not begin with")

    def test_q090_style_description_rejected(self):
        text = (f"**Q-090: run-authorisation convention.** A run authorisation is a separate row whose Decision "
                f"cell begins with {self.M74} or {self.M77}; status {self.STATUS}")
        for status in ("**APPROVED — implementation decision**", "**APPROVED**", self.STATUS):
            ref = self.row(text, status=status)
            for clause in ("D-074 (f)", "D-077 (6)"):
                self.refused(ref, clause)

    def test_near_miss_markers_rejected(self):
        for decision in ("Run authorisation under D-074 (f)." + self.BIND,          # not bold
                         "**run authorisation under D-074 (f).**" + self.BIND,      # case
                         "**Run authorisation under D-074 (f). **" + self.BIND,     # inner space
                         "**Run authorisation under D-074 (f)**" + self.BIND,       # no full stop
                         "> " + self.M74 + self.BIND,                                # leading character
                         "x" + self.M74 + self.BIND):
            self.refused(self.row(decision), msg="does not begin with")

    def test_wrong_clause_rejected(self):
        self.refused(self.row(self.M77 + self.BIND), "D-074 (f)", msg="does not begin with")
        self.refused(self.row(self.M74 + self.BIND), "D-077 (6)", msg="does not begin with")

    def test_conditional_and_in_principle_rejected(self):
        for status in ("**APPROVED — CONDITIONAL (inactive)**", "**APPROVED IN PRINCIPLE**",
                       "**APPROVED — implementation decision**", "PROPOSED", "PENDING"):
            self.refused(self.row(self.M74 + self.BIND, status=status), msg="not an unconditional approval")

    def test_duplicate_decision_rows_rejected(self):
        with open(self.fx.log, "a", encoding="utf-8") as f:
            for _ in range(2):
                f.write(f"| D-950 | 2099-01-01 (TEST) | {self.M74}{self.BIND} | {self.STATUS} | r | researcher |\n")
        self.refused("D-950", msg="more than one")

    def test_real_decision_log_has_no_cell_beginning_with_a_marker(self):
        log = REPO / "logs" / "DECISION_LOG.md"
        starts = [line[:60] for line in log.read_text(encoding="utf-8").splitlines()
                  if line.startswith("| D-") and len(line.split("|")) > 4
                  and line.split("|")[3].strip().startswith(tuple(pr.RUN_AUTHORISATION_MARKERS.values()))]
        self.assertEqual(starts, [])


# ------------------------------------------------------------------ Stage B preparation (D-095): P16
class RunAuthorisationBindings(unittest.TestCase):
    """P16: exact D-088 status, complete and consistent bindings, single use (synthetic log only)."""

    def setUp(self):
        self.fx = FixtureDir()
        self.addCleanup(self.fx.cleanup)
        self.fx.frozen()
        self.fx.base()
        self.n = 700

    def auth(self, binding=None, status=None, clause="D-074 (f)"):
        ref = f"D-{self.n}"
        self.n += 1
        self.fx.add_auth(ref, clause, status=status, binding=binding)
        return ref

    def refused(self, ref, msg, clause="D-074 (f)", **kw):
        with self.assertRaisesRegex(pr.RunAuthorisationError, msg, msg=ref):
            pr.verify_run_authorisation(self.fx.lit, ref, clause, **kw)

    def test_complete_authorisation_accepted_and_matched(self):
        ref = self.auth()
        self.assertEqual(pr.verify_run_authorisation(self.fx.lit, ref, "D-074 (f)", inventory_sha256=INV,
                                                     criteria_version=VERSION), ref)
        ref77 = self.auth(clause="D-077 (6)")
        self.assertEqual(pr.verify_run_authorisation(self.fx.lit, ref77, "D-077 (6)", inventory_sha256=INV), ref77)

    def test_backticks_tolerated(self):
        b = bindings().replace("criteria_version:", "`criteria_version`:").replace(VERSION, f"`{VERSION}`")
        self.assertTrue(pr.verify_run_authorisation(self.fx.lit, self.auth(binding=b), "D-074 (f)"))

    def test_status_must_be_exact(self):
        for status in ("**APPROVED**", "**APPROVED** — run authorisation", "**APPROVED** — run authorisation (single use); note",
                       "**APPROVED** - run authorisation (single use)"):
            self.refused(self.auth(status=status), "not exactly")

    def test_missing_duplicated_or_malformed_bindings(self):
        full = bindings()
        for key in ("criteria_version", "inventory_sha256", "freeze_entry", "d035_s6_records", "single_use"):
            parts = [x for x in full.split(";") if not x.strip().startswith(key + ":")]
            self.refused(self.auth(binding=";".join(parts)), f"{key}.*exactly once")
            self.refused(self.auth(binding=full + f"; {key}: x"), f"{key}.*exactly once")
        for bad in (bindings(inventory_sha256="d" * 63), bindings(inventory_sha256="D" * 64),
                    bindings(freeze="D-99"), bindings(single="no"), bindings(criteria_version="has space"),
                    bindings().replace("single_use: yes", "single_use: yes please")):
            self.refused(self.auth(binding=bad), "malformed")
        self.refused(self.auth(binding=" no bindings at all"), "exactly once")

    def test_six_distinct_section6_records_required(self):
        self.refused(self.auth(binding=bindings(s6=S6_IDS[:5])), "six distinct")
        self.refused(self.auth(binding=bindings(s6=S6_IDS[:5] + [S6_IDS[0]])), "six distinct")

    def test_bound_decisions_must_exist_be_approved_and_distinct(self):
        self.refused(self.auth(binding=bindings(freeze="D-970")), "freeze entry.*not a decision")
        self.fx.row("D-971", "freeze proposal", status="PROPOSED")
        self.refused(self.auth(binding=bindings(freeze="D-971")), "freeze entry D-971 is not approved")
        self.refused(self.auth(binding=bindings(s6=S6_IDS[:5] + ["D-972"])), "§6 record.*not a decision")
        self.fx.row("D-973", "**D-035 §6 condition 6 recorded as met.** (pending)", status="PENDING")
        self.refused(self.auth(binding=bindings(s6=S6_IDS[:5] + ["D-973"])), "D-973 is not approved")
        self.refused(self.auth(binding=bindings(freeze=S6_IDS[0])), "distinct")
        self.fx.row("D-974", "freeze duplicate")
        self.fx.row("D-974", "freeze duplicate")
        self.refused(self.auth(binding=bindings(freeze="D-974")), "more than one decision row")

    def test_section6_records_must_cover_conditions_once(self):
        self.fx.row("D-975", "**D-035 §6 condition 1 recorded as met.** again")
        self.refused(self.auth(binding=bindings(s6=["D-975"] + S6_IDS[1:5] + [S6_IDS[0]])), "not 1 to 6")
        self.fx.row("D-976", "**D-035 §6 condition 6 recorded as met.** **D-035 §6 condition 5 recorded as met.**")
        self.refused(self.auth(binding=bindings(s6=S6_IDS[:5] + ["D-976"])), "exactly one")
        self.fx.row("D-977", "no condition named")
        self.refused(self.auth(binding=bindings(s6=S6_IDS[:5] + ["D-977"])), "exactly one")
        # a decision that only mentions a condition (like D-091 in the real log) is not a condition record
        self.fx.row("D-978", "**Q-086: scope of D-035 record §6 condition 6.** **D-035 §6 condition 6 recorded as met.**")
        self.refused(self.auth(binding=bindings(s6=S6_IDS[:5] + ["D-978"])), "must begin with")
        self.fx.row("D-979", "D-035 §6 condition 6 recorded as met. (not bold)")
        self.refused(self.auth(binding=bindings(s6=S6_IDS[:5] + ["D-979"])), "must begin with")

    def test_registry_must_name_the_bound_freeze_and_version(self):
        self.refused(self.auth(binding=bindings(criteria_version="other_v")), "not a registered frozen version")
        self.fx.row("D-968", f"second freeze {VERSION} commit {COMMIT} sha {SHA_C} {SHA_P}")
        self.refused(self.auth(binding=bindings(freeze="D-968")), "does not match the registry")
        (self.fx.lit / pr.CRITERIA_REGISTRY_FILE).unlink()
        self.refused(self.auth(), "freeze required")

    def test_run_inputs_must_match_bindings(self):
        ref = self.auth()
        self.refused(ref, "inventory SHA-256 differs", inventory_sha256="e" * 64)
        self.refused(ref, "criteria_version differs", criteria_version=VERSION + "b")

    def test_single_use_ledger(self):
        ref74, ref77 = self.auth(), self.auth(clause="D-077 (6)")
        pr.check_authorisation_unused(self.fx.lit, ref74, "D-074 (f)", "stage0")
        self.fx.ledger_done(ref74, "D-074 (f)", "stage0")
        with self.assertRaisesRegex(pr.RunAuthorisationError, "already used.*single use"):
            pr.check_authorisation_unused(self.fx.lit, ref74, "D-074 (f)", "stage0")
        self.fx.ledger_done(ref77, "D-077 (6)", "pilot_sample")
        pr.check_authorisation_unused(self.fx.lit, ref77, "D-077 (6)", "pilot_sheet")     # draw, then one sheet
        pr.require_completed_use(self.fx.lit, ref77, "pilot_sample")
        with self.assertRaisesRegex(pr.RunAuthorisationError, "single use"):
            pr.check_authorisation_unused(self.fx.lit, ref77, "D-077 (6)", "pilot_sample")
        with self.assertRaisesRegex(pr.RunAuthorisationError, "cannot use"):
            pr.check_authorisation_unused(self.fx.lit, ref77, "D-077 (6)", "stage0")
        with self.assertRaisesRegex(pr.RunAuthorisationError, "single use"):          # same ID, other clause
            pr.check_authorisation_unused(self.fx.lit, ref74, "D-077 (6)", "pilot_sample")
        with self.assertRaisesRegex(pr.RunAuthorisationError, "no completed pilot_sample"):
            pr.require_completed_use(self.fx.lit, ref74, "pilot_sample")

    def test_malformed_ledger_fails_closed(self):
        path = self.fx.lit / pr.RUN_LEDGER_FILE
        base = {"authorization": "D-700", "clause": "D-074 (f)", "tool": "stage0", "run_time_utc": "t"}
        line = lambda **kw: json.dumps({**base, **kw}) + "\n"          # noqa: E731
        for content in ("not json\n", json.dumps({"authorization": "D-700"}) + "\n", "[]\n",
                        line(), line(event="finished"), line(event="completed"),
                        line(event="started") + line(event="started")):
            path.write_text(content, encoding="utf-8")
            with self.assertRaisesRegex(pr.RunAuthorisationError, "malformed|not JSON|unknown event|inconsistent"):
                pr.check_authorisation_unused(self.fx.lit, "D-700", "D-074 (f)", "stage0")

    def test_real_decision_log_holds_no_complete_authorisation(self):
        log = (REPO / "logs" / "DECISION_LOG.md").read_text(encoding="utf-8")
        self.assertNotIn(pr.RUN_AUTHORISATION_STATUS, [l.split("|")[4].strip() for l in log.splitlines()
                                                         if l.startswith("| D-") and len(l.split("|")) > 5])
        self.assertFalse((REPO / "research/literature" / pr.RUN_LEDGER_FILE).exists())


# ------------------------------------------------------------------ P17: frame identity
class FrameIdentity(unittest.TestCase):
    SNAP = [f"P{n:04d}" for n in range(1, 11)]

    def frame(self, ids):
        return {"B": [p for p in ids if int(p[1:]) % 2], "untagged": [p for p in ids if not int(p[1:]) % 2]}

    def check(self, frame, snap=None, stage0_ids=("P0003",), size=10):
        return ps.verify_frame_identity(frame, self.SNAP if snap is None else snap, stage0_ids, size)

    def test_identity_accepted(self):
        self.assertEqual(self.check(self.frame([p for p in self.SNAP if p != "P0003"])), 9)

    def test_missing_additional_and_duplicated_ids_rejected(self):
        expected = [p for p in self.SNAP if p != "P0003"]
        with self.assertRaisesRegex(ps.PilotSampleError, r"missing \['P0005'\]"):
            self.check(self.frame([p for p in expected if p != "P0005"]))
        with self.assertRaisesRegex(ps.PilotSampleError, r"additional \['P0011'\]"):
            self.check(self.frame(expected + ["P0011"]))
        with self.assertRaisesRegex(ps.PilotSampleError, r"additional \['P0003'\]"):    # Stage-0 record kept
            self.check(self.frame(self.SNAP))
        dup = self.frame(expected)
        dup["untagged"].append("P0001")                                                  # same ID in two strata
        with self.assertRaisesRegex(ps.PilotSampleError, "duplicated in the frame"):
            self.check(dup)
        # same count, different identity: counts alone would pass
        swapped = self.frame([p for p in expected if p != "P0002"] + ["P0012"])
        self.assertEqual(sum(len(v) for v in swapped.values()), 9)
        with self.assertRaisesRegex(ps.PilotSampleError, "identity mismatch"):
            self.check(swapped)

    def test_snapshot_problems_rejected(self):
        expected = self.frame([p for p in self.SNAP if p != "P0003"])
        with self.assertRaisesRegex(ps.PilotSampleError, "duplicated in the scope snapshot"):
            self.check(expected, snap=self.SNAP + ["P0001"], size=None)
        with self.assertRaisesRegex(ps.PilotSampleError, "expected 11"):
            self.check(expected, size=11)
        with self.assertRaisesRegex(ps.PilotSampleError, "not in the scope snapshot"):
            self.check(expected, stage0_ids=("P0003", "P0099"))

    def test_load_scope_snapshot(self):
        fx = FixtureDir()
        self.addCleanup(fx.cleanup)
        path = fx.snapshot(self.SNAP)
        self.assertEqual(ps.load_scope_snapshot(path, sha(path)), self.SNAP)
        with self.assertRaisesRegex(ps.PilotSampleError, "recorded SHA-256"):
            ps.load_scope_snapshot(path, "0" * 64)
        with self.assertRaisesRegex(ps.PilotSampleError, "not found"):
            ps.load_scope_snapshot(fx.lit / "nope.csv", None)
        bad = fx.snapshot(["P0001", "X2"], name="bad.csv")
        with self.assertRaisesRegex(ps.PilotSampleError, "malformed"):
            ps.load_scope_snapshot(bad, None)
        nocol = fx.lit / "nocol.csv"
        nocol.write_text("id\nP0001\n", encoding="utf-8")
        with self.assertRaisesRegex(ps.PilotSampleError, "no paper_id column"):
            ps.load_scope_snapshot(nocol, None)

    def test_constants_match_governance_records(self):
        """The snapshot hash and size come from D-044_scope_snapshot.md; the seven Stage-0 IDs from the
        F1-PILOT-FRAME row of D-063 (documents only; the inventory is not read)."""
        md = (REPO / "research/literature/scope/D-044_scope_snapshot.md").read_text(encoding="utf-8")
        self.assertIn(ps.APPROVED_SCOPE_SNAPSHOT_SHA256, md)
        self.assertIn("1,470 rows plus a header", md)
        f1 = [l for l in (REPO / "logs/DECISION_LOG.md").read_text(encoding="utf-8").splitlines()
              if "| F1-PILOT-FRAME | D-063 |" in l]
        self.assertEqual(len(f1), 1)
        import re
        listed = re.search(r"Stage-0 exclusions \(([^)]*)\)", f1[0]).group(1)
        self.assertEqual(tuple(re.findall(r"P\d{4}", listed)), ps.APPROVED_STAGE0_IDS)
        self.assertEqual(ps.APPROVED_FRAME_SIZE, ps.APPROVED_SCOPE_SIZE - len(ps.APPROVED_STAGE0_IDS))


# ------------------------------------------------------------------ P15: frame-only mode; full synthetic draw
class FrameOnlyAndDraw(unittest.TestCase):
    """Synthetic three-record scope: P0002 is a Stage-0 record (Editorial)."""

    def setUp(self):
        self.fx = ToolFixture()
        self.addCleanup(self.fx.cleanup)
        self.inv = self.fx.write_data([
            {"paper_id": "P0001", "member_types": [["Journal Article"]], "themes": "B"},
            {"paper_id": "P0002", "member_types": [["Editorial"]], "themes": "B"},
            {"paper_id": "P0003", "member_types": [["Journal Article"]], "themes": "F"}])
        path = self.fx.snapshot(["P0001", "P0002", "P0003"])
        (self.fx.lit / "records" / "dedup_review.csv").write_text("paper_id_a,paper_id_b\nP0001,P0009\n",
                                                                   encoding="utf-8")
        for name, value in (("APPROVED_SCOPE_SNAPSHOT_SHA256", sha(path)), ("APPROVED_SCOPE_SIZE", 3),
                            ("APPROVED_STAGE0_IDS", ("P0002",)), ("APPROVED_STAGE0_CODES", {"P0002": "E5"}),
                            ("APPROVED_FRAME_SIZE", 2),
                            ("APPROVED_STRATUM_SIZES", {"B": 1, "F": 1}), ("ALLOCATION", {"B": 1, "F": 1})):
            patcher = mock.patch.object(ps, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def cli(self, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            ps.main(["--lit-dir", str(self.fx.lit), "--expected-inventory-sha256", self.inv, *args])
        return json.loads(buf.getvalue())

    def screening_files(self):
        return sorted(p.name for p in (self.fx.lit / "screening").iterdir() if p.name != "decisions.csv")

    def authorise_draw(self, stage0_rows=True):
        self.fx.frozen()
        self.fx.add_auth("D-902", "D-077 (6)", inventory_sha256=self.inv)
        if stage0_rows:
            self.fx.decisions([stage0_row("P0002")])                     # D-093: Stage-0 rows first

    def test_frame_only_valid_frame_no_draw_no_output(self):
        with mock.patch.object(ps, "draw", side_effect=AssertionError("draw called")):
            out = self.cli("--frame-only")
        self.assertEqual((out["frame_valid"], out["frame_size"], out["drawn"], out["written"]), (True, 2, False, False))
        self.assertEqual({k: v for k, v in out["stratum_sizes"].items() if v}, {"B": 1, "F": 1})
        self.assertEqual(out["publications_jsonl_sha256"], sha(self.fx.lit / "records" / "publications.jsonl"))
        self.assertEqual(self.screening_files(), [])

    def test_frame_only_invalid_frames_stop(self):
        cases = [("APPROVED_FRAME_SIZE", 3, "frame mismatch"),
                 ("APPROVED_STRATUM_SIZES", {"B": 2, "F": 0}, "frame mismatch"),
                 ("APPROVED_STAGE0_IDS", ("P0001",), "identity mismatch"),
                 ("APPROVED_SCOPE_SNAPSHOT_SHA256", "0" * 64, "recorded SHA-256")]
        for name, value, msg in cases:
            with mock.patch.object(ps, name, value), mock.patch.object(ps, "draw", side_effect=AssertionError):
                with self.assertRaisesRegex(SystemExit, msg, msg=name):
                    self.cli("--frame-only")
        self.fx.snapshot(["P0001", "P0002", "P0003", "P0004"])          # an ID the inventory lacks
        with self.assertRaisesRegex(SystemExit, "frame check failed"):
            self.cli("--frame-only")
        with self.assertRaisesRegex(SystemExit, "inventory SHA-256"):
            ps.main(["--lit-dir", str(self.fx.lit), "--expected-inventory-sha256", "0" * 64, "--frame-only"])
        self.assertEqual(self.screening_files(), [])

    def test_frame_only_rejects_write_or_authorisation(self):
        for extra in (["--write"], ["--authorization", "D-902"]):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                self.cli("--frame-only", *extra)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.cli()                                                      # a draw needs --authorization
        self.assertEqual(self.screening_files(), [])

    def test_authorised_synthetic_draw_is_single_use(self):
        self.authorise_draw()
        out = self.cli("--authorization", "D-902", "--write")
        self.assertEqual((out["sample_size"], out["frame_size"]), (2, 2))
        self.assertEqual(out["duplicate_pairs_in_sample"], [{"paper_id_a": "P0001", "paper_id_b": "P0009",
                                                              "drawn": ["P0001"]}])
        self.assertEqual(self.screening_files(), ["pilot_sample.csv", "pilot_sample.provenance.json",
                                                  "run_authorisation_ledger.jsonl"])
        (self.fx.lit / "screening" / "pilot_sample.csv").unlink()
        (self.fx.lit / "screening" / "pilot_sample.provenance.json").unlink()
        with self.assertRaisesRegex(SystemExit, "single use"):            # even with the outputs removed
            self.cli("--authorization", "D-902", "--write")
        self.assertEqual(self.screening_files(), ["run_authorisation_ledger.jsonl"])

    def test_draw_refuses_identity_mismatch_before_drawing(self):
        self.authorise_draw()
        with mock.patch.object(ps, "APPROVED_STAGE0_IDS", ("P0001",)), \
                mock.patch.object(ps, "draw", side_effect=AssertionError("draw called")):
            with self.assertRaisesRegex(ps.PilotSampleError, "identity mismatch"):
                self.cli("--authorization", "D-902", "--write")
        self.assertEqual(self.screening_files(), [])


# ------------------------------------------------------------------ P18: pilot follow-on tools
def prow(pid, decision, code="", screener="assistant", **desc):
    r = {c: "" for c in pa.TEMPLATE_COLUMNS}
    r.update({"paper_id": pid, "stage": "title_abstract", "decision": decision, "reason_code": code,
              "screener": screener, "date": "2099-01-01", "justification": "paraphrase", "criteria_version": VERSION})
    if decision in ("include", "uncertain"):             # D-060 (6) required descriptors (synthetic values)
        r.update({"rq_tags": "RQ1", "record_type": "original", "biomarker_class": "routine_chemistry",
                  "dim_explainability": "unclear", "dim_uncertainty": "unclear", "dim_calibration": "unclear",
                  "validation_design": "unclear"})
        if decision == "include":
            r["tier"] = "3"
    r.update(desc)
    return r


class PilotAgreement(unittest.TestCase):
    def test_cohen_kappa_textbook_values(self):
        # 2x2 example: 20 yes/yes, 5 yes/no, 10 no/yes, 15 no/no -> po 0.70, pe 0.50, kappa 0.40
        a = ["y"] * 25 + ["n"] * 25
        b = ["y"] * 20 + ["n"] * 5 + ["y"] * 10 + ["n"] * 15
        self.assertAlmostEqual(pa.cohen_kappa(a, b), 0.4)
        self.assertEqual(pa.cohen_kappa(["x", "y"], ["x", "y"]), 1.0)
        self.assertIsNone(pa.cohen_kappa(["x", "x"], ["x", "x"]))       # undefined: chance agreement 1
        # three levels, worked by hand: po = 7/10; pe = (4*4 + 4*3 + 2*3)/100 = 0.34; kappa = 0.36/0.66
        a3 = ["i", "i", "i", "i", "e", "e", "e", "e", "u", "u"]
        b3 = ["i", "i", "i", "e", "e", "e", "u", "i", "u", "u"]
        self.assertAlmostEqual(pa.cohen_kappa(a3, b3), 0.36 / 0.66)
        with self.assertRaises(pa.PilotAgreementError):
            pa.cohen_kappa(["x"], [])

    def rows(self):
        a = [prow("P0001", "include", rq_tags="RQ1;RQ3", dim_calibration="yes"),
             prow("P0002", "exclude", "E4"), prow("P0003", "exclude", "E2"),
             prow("P0004", "uncertain", rq_tags="RQ5", needs_human="yes"), prow("P0005", "exclude", "E12")]
        r = [prow("P0001", "include", screener="researcher", rq_tags="RQ3;RQ1", dim_calibration="unclear"),
             prow("P0002", "exclude", "E4", screener="researcher"), prow("P0003", "exclude", "E3", screener="researcher"),
             prow("P0004", "uncertain", screener="researcher", rq_tags="RQ5"),
             prow("P0005", "include", screener="researcher", rq_tags="RQ6")]
        return a, r

    def test_metrics_and_pass_rule(self):
        a, r = self.rows()
        res = pa.agreement(a, r, sample_ids=[f"P000{i}" for i in range(1, 6)])
        self.assertEqual(res["n"], 5)
        self.assertEqual(res["three_level"]["percent_agreement"], 80.0)
        self.assertAlmostEqual(res["three_level"]["kappa"], round(pa.cohen_kappa([x["decision"] for x in a],
                                                                                 [x["decision"] for x in r]), 4))
        self.assertEqual(res["primary_code"], {"both_exclude": 2, "same_code": 1})
        self.assertEqual(res["disagreements_per_code"], {"E2": 1, "E3": 1, "E12": 1})
        self.assertEqual((res["include_exclude_conflicts"], res["unresolved_conflicts"]), (["P0005"], ["P0005"]))
        self.assertEqual(res["descriptor_agreement"]["rq_tags"], {"n": 2, "agree": 2, "percent": 100.0})  # set-valued
        self.assertEqual(res["descriptor_agreement"]["dim_calibration"]["agree"], 1)
        self.assertEqual(res["disagreement_ids"], ["P0003", "P0005"])
        self.assertFalse(res["pass"])                                       # unresolved conflict
        self.assertEqual((res["pass_rule"]["kappa_threshold"], res["pass_rule"]["max_disagreements_per_code"]),
                         (0.60, 2))

    def test_pass_rule_components(self):
        a = [prow(f"P{i:04d}", "include") for i in range(1, 7)] + [prow(f"P{i:04d}", "exclude", "E2") for i in range(7, 13)]
        r = [dict(x, screener="researcher") for x in a]
        self.assertTrue(pa.agreement(a, r)["pass"])
        r3 = [dict(x, reason_code="E3") if x["decision"] == "exclude" and int(x["paper_id"][1:]) < 10 else x for x in r]
        self.assertFalse(pa.agreement(a, r3)["pass"])                      # 3 disagreements on E2 and on E3
        r2 = [dict(x, reason_code="E3") if x["decision"] == "exclude" and int(x["paper_id"][1:]) < 9 else x for x in r]
        self.assertTrue(pa.agreement(a, r2)["pass"])                       # 2 per code: still fewer than 3
        conflict = [dict(x, decision="exclude", reason_code="E2") if x["paper_id"] == "P0001" else x for x in r]
        self.assertFalse(pa.agreement(a, conflict)["pass"])
        adj = [prow("P0001", "exclude", "E2", screener="researcher")]       # agreement on the exclusion (D-025)
        res = pa.agreement(a, conflict, adjudication_rows=adj)
        self.assertTrue(res["pass"])
        self.assertEqual(res["adjudicated_decisions"], {"P0001": "exclude"})
        restored = pa.agreement(a, conflict, adjudication_rows=[prow("P0001", "include", screener="researcher")])
        self.assertEqual(restored["unresolved_conflicts"], ["P0001"])        # a wrongful exclusion stays a failure
        self.assertFalse(restored["pass"])
        same = [prow("P0001", "include"), prow("P0002", "include")]
        self.assertIsNone(pa.agreement(same, [dict(x, screener="researcher") for x in same])["pass"])  # kappa undefined

    def test_inconsistent_inputs_rejected(self):
        a, r = self.rows()
        with self.assertRaisesRegex(pa.PilotAgreementError, "different records"):
            pa.agreement(a, r[:-1])
        with self.assertRaisesRegex(pa.PilotAgreementError, "exactly the pilot sample"):
            pa.agreement(a, r, sample_ids=["P0001"])
        with self.assertRaisesRegex(pa.PilotAgreementError, "more than one"):
            pa.agreement(a + [a[0]], r)
        with self.assertRaisesRegex(pa.PilotAgreementError, "not a title_abstract"):
            pa.agreement([dict(a[0], stage="full_text")] + a[1:], r)

    def test_report_markdown_holds_no_text_fields(self):
        a, r = self.rows()
        a[0]["justification"] = "SECRET-JUSTIFICATION"
        md = pa.report_markdown(pa.agreement(a, r))
        self.assertIn("NOT PASSED", md)
        self.assertNotIn("SECRET-JUSTIFICATION", md)
        self.assertIn("Cohen's kappa", md)


class PilotTemplateAndQueue(unittest.TestCase):
    def setUp(self):
        self.fx = FixtureDir()
        self.addCleanup(self.fx.cleanup)

    def test_template_rows(self):
        rows = pa.make_template(["P0010", "P0002"], VERSION)
        self.assertEqual([r["paper_id"] for r in rows], ["P0002", "P0010"])
        self.assertEqual(list(rows[0]), pa.TEMPLATE_COLUMNS)
        self.assertEqual({(r["stage"], r["screener"], r["criteria_version"], r["decision"]) for r in rows},
                         {("title_abstract", "researcher", VERSION, "")})
        self.assertNotIn("abstract", pa.TEMPLATE_COLUMNS)
        self.assertNotIn("title", pa.TEMPLATE_COLUMNS)
        with self.assertRaises(pa.PilotAgreementError):
            pa.make_template(["P0001", "P0001"], VERSION)
        with self.assertRaises(pa.PilotAgreementError):
            pa.make_template(["P0001"], "has space")

    def test_template_cli_and_filled_template_validates(self):
        sample = self.fx.lit / "screening" / "pilot_sample.csv"
        sample.write_text("paper_id,stratum\nP0002,F\nP0001,B\n", encoding="utf-8")
        out = self.fx.lit / "screening" / "pilot_decisions_researcher.csv"
        with contextlib.redirect_stdout(io.StringIO()):
            pa.main(["template", "--sample", str(sample), "--criteria-version", VERSION, "--out", str(out)])
        with open(out, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        for r in rows:
            r.update({"decision": "exclude", "reason_code": "E2", "date": "2099-01-01", "justification": "paraphrase"})
        filled = self.fx.lit / "screening" / "filled.csv"
        with open(filled, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=pa.TEMPLATE_COLUMNS)
            w.writeheader()
            w.writerows(rows)
        self.assertEqual(len(pr.load_screening_decisions(self.fx.lit, path=filled)), 2)
        with self.assertRaisesRegex(ValueError, "decision"):                 # the empty template is not a decision file
            pr.load_screening_decisions(self.fx.lit, path=out)
        with self.assertRaisesRegex(SystemExit, "already exists"):
            pa.main(["template", "--sample", str(sample), "--criteria-version", VERSION, "--out", str(out)])

    def test_queue_reasons(self):
        a = [prow("P0001", "uncertain"), prow("P0002", "exclude", "E12"), prow("P0003", "include", needs_human="yes"),
             prow("P0004", "include"), prow("P0005", "exclude", "E2"), prow("P0006", "include")]
        r = [dict(x, screener="researcher") for x in a]
        r[4] = dict(r[4], reason_code="E3")
        r[5] = dict(r[5], decision="exclude", reason_code="E2")
        q = pa.build_adjudication_queue({"assistant": a, "researcher": r}, [("P0004", "P0099"), ("P0098", "P0097")])
        got = {x["paper_id"]: x["reasons"] for x in q}
        self.assertEqual(got, {"P0001": "uncertain", "P0002": "E12", "P0003": "needs_human",
                               "P0004": "possible_duplicate_with:P0099", "P0005": "pilot_disagreement",
                               "P0006": "pilot_disagreement", "P0097": "possible_duplicate_with:P0098",
                               "P0098": "possible_duplicate_with:P0097", "P0099": "possible_duplicate_with:P0004"})
        stages = {x["paper_id"]: x["stage"] for x in q}
        self.assertEqual((stages["P0004"], stages["P0097"], stages["P0099"]), ("title_abstract", "", ""))
        self.assertEqual(q[0]["screeners"], "assistant;researcher")
        self.assertEqual(list(q[0]), pa.QUEUE_COLUMNS)

    def test_queue_uses_latest_row_per_stage(self):
        rows = [prow("P0001", "uncertain"), prow("P0001", "include")]       # adjudicated later
        self.assertEqual(pa.build_adjudication_queue({"assistant": rows}), [])

    def test_report_and_queue_cli(self):
        a, r = PilotAgreement().rows()
        paths = {}
        for label, rows in (("assistant", a), ("researcher", r)):
            path = self.fx.lit / "screening" / f"pilot_decisions_{label}.csv"
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=pa.TEMPLATE_COLUMNS)
                w.writeheader()
                w.writerows(rows)
            paths[label] = path
        md = self.fx.lit / "screening" / "pilot_report.md"
        with contextlib.redirect_stdout(io.StringIO()) as buf:
            pa.main(["report", "--lit-dir", str(self.fx.lit), "--assistant", str(paths["assistant"]),
                     "--researcher", str(paths["researcher"]), "--out", str(md)])
        self.assertFalse(json.loads(buf.getvalue())["pass"])
        self.assertIn("NOT PASSED", md.read_text(encoding="utf-8"))
        queue = self.fx.lit / "screening" / "adjudication_queue.csv"
        with contextlib.redirect_stdout(io.StringIO()):
            pa.main(["queue", "--lit-dir", str(self.fx.lit), "--decisions", f"assistant={paths['assistant']}",
                     f"researcher={paths['researcher']}", "--out", str(queue)])
        with open(queue, newline="", encoding="utf-8") as f:
            self.assertEqual([x["paper_id"] for x in csv.DictReader(f)], ["P0003", "P0004", "P0005"])
        with self.assertRaisesRegex(SystemExit, "distinct label=path"):
            pa.main(["queue", "--lit-dir", str(self.fx.lit), "--decisions", str(paths["assistant"]),
                     "--out", str(queue) + "2"])


# ------------------------------------------------------------------ Pre-commit audit corrections (2026-11-11)
def s0(pid, code="E5", **over):
    r = {"paper_id": pid, "stage": "title_abstract", "decision": "exclude", "reason_code": code,
         "screener": "rule:stage0"}
    r.update(over)
    return r


class Stage0RowsBeforeDraw(unittest.TestCase):
    """M2 (D-093): the approved Stage-0 rows must exist, and match, before the draw."""
    CODES = {"P0002": "E5", "P0005": "E7"}

    def test_matching_rows_accepted(self):
        rows = [s0("P0002"), s0("P0005", "E7"), dict(s0("P0001"), screener="assistant")]
        self.assertEqual(ps.verify_stage0_rows(rows, self.CODES), 2)

    def test_missing_extra_duplicate_or_wrong_rows_rejected(self):
        cases = [([s0("P0002")], r"missing Stage-0 rows for \['P0005'\]"),
                 ([s0("P0002"), s0("P0005", "E7"), s0("P0009")], r"outside the approved list: \['P0009'\]"),
                 ([s0("P0002"), s0("P0002"), s0("P0005", "E7")], "P0002: 2 Stage-0 rows"),
                 ([s0("P0002", "E7"), s0("P0005", "E7")], "expected title_abstract/exclude/E5"),
                 ([s0("P0002"), s0("P0005", "E7", stage="full_text")], "expected title_abstract/exclude/E7"),
                 ([s0("P0002"), s0("P0005", "", decision="include")], "expected title_abstract/exclude/E7"),
                 ([], "missing Stage-0 rows")]
        for rows, msg in cases:
            with self.assertRaisesRegex(ps.PilotSampleError, msg, msg=msg):
                ps.verify_stage0_rows(rows, self.CODES)

    def test_codes_match_the_f1_record(self):
        f1 = [l for l in (REPO / "logs/DECISION_LOG.md").read_text(encoding="utf-8").splitlines()
              if "| F1-PILOT-FRAME | D-063 |" in l][0]
        import re
        m = re.search(r"\(([^)]*)\s*→ E5;\s*([^)]*)→ E7\)", f1)
        e5, e7 = re.findall(r"P\d{4}", m.group(1)), re.findall(r"P\d{4}", m.group(2))
        self.assertEqual(ps.APPROVED_STAGE0_CODES, {**{p: "E5" for p in e5}, **{p: "E7" for p in e7}})
        self.assertEqual(ps.APPROVED_STAGE0_IDS, tuple(ps.APPROVED_STAGE0_CODES))

    def test_draw_refused_without_stage0_rows(self):
        case = FrameOnlyAndDraw("test_frame_only_valid_frame_no_draw_no_output")
        case.setUp()
        self.addCleanup(case.doCleanups)
        case.authorise_draw(stage0_rows=False)
        with mock.patch.object(ps, "draw", side_effect=AssertionError("draw called")):
            with self.assertRaisesRegex(ps.PilotSampleError, "D-093"):
                case.cli("--authorization", "D-902", "--write")
        self.assertEqual(case.screening_files(), [])            # nothing written, no ledger entry, lock released
        case.fx.decisions([stage0_row("P0002")])                # the run is still possible once the rows exist
        self.assertEqual(case.cli("--authorization", "D-902", "--write")["sample_size"], 2)


class AdjudicationEvidence(unittest.TestCase):
    """M5: only a valid adjudication row resolves an include/exclude conflict."""

    def setUp(self):
        self.a = [prow("P0001", "include"), prow("P0002", "exclude", "E2")]
        self.r = [prow("P0001", "exclude", "E2", screener="researcher"), prow("P0002", "exclude", "E2", screener="researcher")]

    def test_valid_adjudication_resolves(self):
        res = pa.agreement(self.a, self.r, adjudication_rows=[prow("P0001", "exclude", "E2", screener="researcher")])
        self.assertEqual((res["unresolved_conflicts"], res["adjudicated_decisions"]), ([], {"P0001": "exclude"}))

    def test_latest_row_is_the_agreed_decision(self):
        rows = [prow("P0001", "exclude", "E2", screener="researcher"), prow("P0001", "include", screener="researcher")]
        res = pa.agreement(self.a, self.r, adjudication_rows=rows)
        self.assertEqual(res["adjudicated_decisions"], {"P0001": "include"})
        self.assertEqual(res["unresolved_conflicts"], ["P0001"])

    def test_only_agreement_on_the_exclusion_resolves(self):
        """D-025 (protocol v0.1 §7): "without adjudicated agreement on the exclusion"."""
        for decision, code, resolved in (("exclude", "E2", True), ("include", "", False), ("uncertain", "", False)):
            row = prow("P0001", decision, code, screener="researcher")
            res = pa.agreement(self.a, self.r, adjudication_rows=[row])
            self.assertEqual(res["unresolved_conflicts"], [] if resolved else ["P0001"], msg=decision)

    def test_wrong_paper_stage_screener_or_decision_rejected(self):
        bad = [(prow("P0009", "include", screener="researcher"), "not a pilot record"),
               (prow("P0001", "include", screener="researcher", stage="full_text"), "stage"),
               (prow("P0001", "include"), "screener=researcher"),
               (prow("P0001", "abstract_only", screener="researcher"), "not a pilot decision")]
        for row, msg in bad:
            with self.assertRaisesRegex(pa.PilotAgreementError, msg, msg=msg):
                pa.agreement(self.a, self.r, adjudication_rows=[row])

    def test_adjudication_of_another_record_does_not_resolve(self):
        res = pa.agreement(self.a, self.r, adjudication_rows=[prow("P0002", "exclude", "E2", screener="researcher")])
        self.assertEqual(res["unresolved_conflicts"], ["P0001"])
        self.assertFalse(res["pass"])


class RunConcurrencyAndInterruption(unittest.TestCase):
    """L5: run lock, interrupted runs, no-overwrite outputs, ledger consistency (synthetic only)."""

    def setUp(self):
        self.case = FrameOnlyAndDraw("test_frame_only_valid_frame_no_draw_no_output")
        self.case.setUp()
        self.addCleanup(self.case.doCleanups)
        self.case.authorise_draw()
        self.fx = self.case.fx
        self.lock = self.fx.lit / pr.RUN_LOCK_FILE

    def draw(self):
        return self.case.cli("--authorization", "D-902", "--write")

    def test_concurrent_run_refused_by_lock(self):
        with pr.run_lock(self.fx.lit):                             # another run holds the lock
            with self.assertRaisesRegex(SystemExit, "another authorised run is in progress"):
                self.draw()
        self.assertEqual(self.case.screening_files(), [])
        self.draw()                                                 # lock released: the run proceeds
        self.assertFalse(self.lock.exists())

    def test_stale_lock_is_not_removed_automatically(self):
        self.lock.write_text("{}", encoding="utf-8")                # left by a killed process
        with self.assertRaisesRegex(SystemExit, "interrupted"):
            self.draw()
        self.assertTrue(self.lock.exists())

    def test_lock_released_after_failure(self):
        with mock.patch.object(ps, "verify_stage0_rows", side_effect=ps.PilotSampleError("forced")):
            with self.assertRaises(ps.PilotSampleError):
                self.draw()
        self.assertFalse(self.lock.exists())

    def test_interrupted_draw_consumes_authorisation_and_blocks_the_sheet(self):
        real = pr.write_new_file_atomically
        calls = []

        def crash_on_sidecar(path, text, check=None):
            calls.append(path)
            if len(calls) == 2:
                raise OSError("simulated crash")
            return real(path, text, check)

        with mock.patch.object(pr, "write_new_file_atomically", side_effect=crash_on_sidecar):
            with self.assertRaisesRegex(OSError, "simulated crash"):
                self.draw()
        self.assertEqual([e["event"] for e in pr.authorisation_uses(self.fx.lit)], ["started"])
        self.assertFalse(self.lock.exists())
        self.assertEqual(sorted(p.name for p in (self.fx.lit / "screening").iterdir() if p.name.endswith(".tmp")), [])
        (self.fx.lit / "screening" / "pilot_sample.csv").unlink()  # even after cleaning up the partial output
        with self.assertRaisesRegex(SystemExit, "never completed"):
            self.draw()
        with self.assertRaisesRegex(pr.RunAuthorisationError, "no completed pilot_sample"):
            pr.require_completed_use(self.fx.lit, "D-902", "pilot_sample")

    def test_stage0_write_holds_lock_and_records_both_events(self):
        st = Stage0Corrections("test_dry_run_writes_nothing")
        st.setUp()
        self.addCleanup(st.doCleanups)
        with pr.run_lock(st.fx.lit):
            with self.assertRaisesRegex(SystemExit, "in progress"):
                st.run_cli("--write")
        self.assertEqual(pr.authorisation_uses(st.fx.lit), [])
        st.run_cli("--write")
        self.assertEqual([e["event"] for e in pr.authorisation_uses(st.fx.lit)], ["started", "completed"])

    def test_completion_requires_a_start(self):
        with self.assertRaisesRegex(pr.RunAuthorisationError, "started=False"):
            pr.record_authorisation_completion(self.fx.lit, "D-902", "D-077 (6)", "pilot_sample", "t")
        pr.record_authorisation_start(self.fx.lit, "D-902", "D-077 (6)", "pilot_sample", "t")
        pr.record_authorisation_completion(self.fx.lit, "D-902", "D-077 (6)", "pilot_sample", "t")
        with self.assertRaisesRegex(pr.RunAuthorisationError, "completed=True"):
            pr.record_authorisation_completion(self.fx.lit, "D-902", "D-077 (6)", "pilot_sample", "t")


class NoOverwriteOutputs(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)

    def test_existing_file_never_overwritten(self):
        target = self.dir / "out.csv"
        target.write_text("original", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            pr.write_new_file_atomically(target, "new")
        self.assertEqual(target.read_text(encoding="utf-8"), "original")
        self.assertEqual(sorted(p.name for p in self.dir.iterdir()), ["out.csv"])     # no temp left

    def test_failed_check_writes_nothing(self):
        def refuse(tmp):
            raise ValueError("not ignored")
        with self.assertRaisesRegex(ValueError, "not ignored"):
            pr.write_new_file_atomically(self.dir / "out.csv", "x", check=refuse)
        self.assertEqual(list(self.dir.iterdir()), [])

    def test_sheet_temp_file_must_be_ignored(self):
        repo = self.dir / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        (repo / ".gitignore").write_text("only/sheet.csv\n", encoding="utf-8")   # ignores the file, not its temp
        fx = FixtureDir()
        self.addCleanup(fx.cleanup)
        fx.frozen()
        fx.add_auth("D-902", "D-077 (6)")
        rows = sheet.build_rows(["P0002"], PUBS)
        with self.assertRaisesRegex(sheet.PilotSheetError, "temporary file"):
            sheet.write_sheet(rows, repo / "only" / "sheet.csv", ["P0002"], "D-902", lit_dir=fx.lit, inventory_sha256=INV)
        self.assertEqual(list((repo / "only").iterdir()), [])

    def test_sheet_cli_refuses_without_completed_draw(self):
        case = PilotSheetCli("test_cli_writes_blinded_sheet")
        case.setUp()
        self.addCleanup(case.doCleanups)
        (case.fx.lit / pr.RUN_LEDGER_FILE).unlink()               # no draw recorded
        with self.assertRaisesRegex(SystemExit, "no completed pilot_sample"):
            case.run_cli()
        self.assertFalse(case.out.exists())

    def test_sheet_cli_bad_path_does_not_consume_authorisation(self):
        case = PilotSheetCli("test_cli_writes_blinded_sheet")
        case.setUp()
        self.addCleanup(case.doCleanups)
        with self.assertRaisesRegex(SystemExit, "not ignored"):
            case.run_cli(out=case.repo / "tracked" / "sheet.csv")
        self.assertEqual([e["tool"] for e in pr.authorisation_uses(case.fx.lit)], ["pilot_sample", "pilot_sample"])
        self.assertEqual(case.run_cli(), 0)                          # the authorisation is still usable


if __name__ == "__main__":
    unittest.main()
