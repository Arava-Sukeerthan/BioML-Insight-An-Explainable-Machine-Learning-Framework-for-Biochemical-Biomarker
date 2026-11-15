"""Tests for scripts/literature/pilot_sheet_record.py (decision D-125). SYNTHETIC paper IDs, titles, abstracts,
sample, ledger and inventory in temporary Git repositories only. No real pilot sample, sheet, ledger entry or
sheet record is read or created, and nothing is written inside the repository."""
import contextlib
import csv
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "literature"))
import pubrecords as pr  # noqa: E402
import pilot_sheet as ps  # noqa: E402
import pilot_sheet_record as SR  # noqa: E402

AUTH = "D-122"
CLAUSE = "D-077 (6)"
T_DRAW = "2031-02-03T04:00:00+00:00"
T_SHEET_START = "2031-02-03T04:10:00+00:00"
T_SHEET_DONE = "2031-02-03T04:10:07+00:00"
IDS60 = [f"P{n:04d}" for n in range(11, 11 + 60 * 3, 3)]            # synthetic, ascending, 60


class Fix:
    """A temporary Git repository with a synthetic inventory, pilot sample, provenance sidecar and sheet."""

    def __init__(self, ids=None, abstract_missing=(4, 33), build_sheet=True):
        self.ids = list(IDS60 if ids is None else ids)
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.lit = self.root / "research" / "literature"
        (self.lit / "screening").mkdir(parents=True)
        for cmd in (["init", "-q"], ["config", "user.email", "fixture@example.invalid"],
                    ["config", "user.name", "fixture"], ["config", "commit.gpgsign", "false"]):
            self.git(*cmd)
        (self.root / ".gitignore").write_text(
            "research/literature/screening/pilot_sheet_researcher.csv\n"
            "research/literature/screening/*_sheet_*.csv\nresearch/literature/screening/.*.tmp\n*.tmp\n", encoding="utf-8")
        (self.lit / "paper_inventory.json").write_bytes(b'[{"paper_id": "P0000", "note": "synthetic inventory"}]\n')
        self.inv_sha = hashlib.sha256((self.lit / "paper_inventory.json").read_bytes()).hexdigest()
        self.write_sample()
        self.missing = set(abstract_missing)
        if build_sheet:
            self.write_sheet()
        self.git("commit", "-q", "--allow-empty", "-m", "fixture start")
        self.commit()

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True)

    def commit(self, message="fixture"):
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", message)

    def cleanup(self):
        self._tmp.cleanup()

    # ---- inputs
    def write_sample(self, sidecar_over=None, sample_rows=None):
        strata = {}
        rows = []
        for i, pid in enumerate(self.ids):
            s = "A" if i % 2 else "B"
            strata[s] = strata.get(s, 0) + 1
            rows.append({"paper_id": pid, "stratum": s, "seed": "4004", "inventory_sha256": self.inv_sha,
                         "sampling_script": "scripts/literature/pilot_sample.py"})
        rows = sample_rows if sample_rows is not None else rows
        with open(self.lit / "screening" / "pilot_sample.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["paper_id", "stratum", "seed", "inventory_sha256", "sampling_script"])
            w.writeheader()
            w.writerows(rows)
        side = {"sample_size": len(rows), "seed": 4004, "inventory_sha256": self.inv_sha,
                "sampling_script": "scripts/literature/pilot_sample.py", "allocation": strata, "authorization": AUTH}
        side.update(sidecar_over or {})
        (self.lit / "screening" / "pilot_sample.provenance.json").write_text(json.dumps(side), encoding="utf-8")

    def sheet_rows(self):
        out = []
        for i, pid in enumerate(self.ids):
            missing = i in self.missing
            abstract = "" if missing else (f"LEAKABS-{i} synthetic text, with a comma, \"quotes\", an em dash — and κ."
                                           + ("\nSecond line." if i % 9 == 0 else ""))
            out.append({"paper_id": pid, "title": f"LEAKTITLE-{i} synthetic title", "abstract": abstract,
                        "abstract_status": "unavailable — PubMed" if missing else "", "year": str(2000 + i % 25),
                        "venue": f"Synthetic Journal {i % 7}", "types": "Journal Article;Synthetic"})
        return out

    def write_sheet(self, rows=None, header=None, lineterminator="\r\n", bom=False, encoding="utf-8"):
        buf = io.StringIO(newline="")
        w = csv.DictWriter(buf, fieldnames=header or ps.ALLOWED_COLUMNS, lineterminator=lineterminator,
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(self.sheet_rows() if rows is None else rows)
        data = buf.getvalue().encode(encoding)
        if bom:
            data = b"\xef\xbb\xbf" + data
        self.sheet.write_bytes(data)
        return data

    @property
    def sheet(self):
        return self.lit / ps.DEFAULT_SHEET

    @property
    def record(self):
        return self.lit / SR.RECORD_REL

    @property
    def ledger(self):
        return self.lit / pr.RUN_LEDGER_FILE

    # ---- ledger (D-099: committed after each run)
    def ledger_run(self, tool, started, done, details=None, ref=AUTH):
        pr.record_authorisation_start(self.lit, ref, CLAUSE, tool, started)
        pr.record_authorisation_completion(self.lit, ref, CLAUSE, tool, done, details)
        self.commit(f"ledger {tool}")

    def ledger_default(self, rows="60", inv=None):
        self.ledger_run("pilot_sample", T_DRAW, T_DRAW)
        self.ledger_run("pilot_sheet", T_SHEET_START, T_SHEET_DONE,
                        {"inventory_sha256": inv or self.inv_sha, "rows": rows})


class SheetRecordBase(unittest.TestCase):
    def setUp(self):
        self.fx = Fix()
        self.addCleanup(self.fx.cleanup)

    def cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = SR.main(list(args))
            except SystemExit as e:
                code = e.code
        return code, out.getvalue(), err.getvalue()

    def write_args(self, *extra, auth=AUTH):
        return ["write", "--lit-dir", str(self.fx.lit), "--authorization", auth, *extra]

    def no_leak(self, text):
        self.assertNotIn("LEAK", text)
        for pid in self.fx.ids:
            self.assertNotIn(pid, text)
        self.assertIsNone(re.search(r"\bP\d{2,}\b", text), msg="a paper-id-like token appears in the output")

    def refused(self, needle, *extra, auth=AUTH):
        code, out, err = self.cli(*self.write_args(*extra, auth=auth))
        self.assertEqual(code, 2, msg=(out, err))
        self.assertIn(needle, err)
        self.assertEqual(out, "")
        self.no_leak(out + err)
        self.assertFalse(self.fx.record.exists())
        return err


class HappyPath(SheetRecordBase):
    def test_dry_run_prints_six_fields_and_writes_nothing(self):
        self.fx.ledger_default()
        before = self.fx.sheet.read_bytes()
        code, out, err = self.cli(*self.write_args())
        self.assertEqual((code, err), (0, ""))
        body, _, tail = out.partition("dry run")
        self.assertIn("nothing written", tail)
        rec = json.loads(body)
        self.assertEqual(sorted(rec), sorted(SR.RECORD_KEYS))
        self.assertFalse(self.fx.record.exists())
        self.assertEqual(self.fx.sheet.read_bytes(), before)
        self.no_leak(out)

    def test_write_creates_exactly_the_six_field_record(self):
        self.fx.ledger_default()
        data = self.fx.sheet.read_bytes()
        code, out, err = self.cli(*self.write_args("--write"))
        self.assertEqual((code, err), (0, ""))
        self.assertTrue(self.fx.record.is_file())
        text = self.fx.record.read_text(encoding="utf-8")
        rec = json.loads(text)
        self.assertEqual(sorted(rec), sorted(SR.RECORD_KEYS))
        self.assertEqual(rec["authorization"], AUTH)
        self.assertEqual(rec["columns"], list(ps.ALLOWED_COLUMNS))
        self.assertEqual(rec["rows"], 60)
        self.assertEqual(rec["sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(rec["size_bytes"], len(data))
        self.assertEqual(text, SR.record_text(rec))
        self.assertTrue(text.endswith("}\n") and "\r" not in text)
        self.assertEqual(list(rec), sorted(rec))                      # keys sorted
        self.no_leak(out + text)
        SR.validate_record(rec)

    def test_generated_utc_comes_from_the_completed_ledger_entry(self):
        self.fx.ledger_default()
        self.cli(*self.write_args("--write"))
        rec = json.loads(self.fx.record.read_text(encoding="utf-8"))
        self.assertEqual(rec["generated_utc"], T_SHEET_DONE)
        self.assertNotIn(rec["generated_utc"], (T_SHEET_START, T_DRAW))
        done = [e for e in pr.authorisation_uses(self.fx.lit) if e["tool"] == "pilot_sheet" and e["event"] == "completed"]
        self.assertEqual(rec["generated_utc"], done[0]["run_time_utc"])

    def test_sheet_ledger_and_authorisation_are_not_modified(self):
        self.fx.ledger_default()
        sheet, ledger = self.fx.sheet.read_bytes(), self.fx.ledger.read_bytes()
        stat = os.stat(self.fx.sheet)
        self.cli(*self.write_args("--write"))
        self.assertEqual(self.fx.sheet.read_bytes(), sheet)
        self.assertEqual(os.stat(self.fx.sheet).st_mtime_ns, stat.st_mtime_ns)
        self.assertEqual(self.fx.ledger.read_bytes(), ledger)          # no ledger entry: nothing consumed

    def test_never_overwrites_an_existing_record(self):
        self.fx.ledger_default()
        self.cli(*self.write_args("--write"))
        first = self.fx.record.read_bytes()
        code, out, err = self.cli(*self.write_args("--write"))
        self.assertEqual(code, 2)
        self.assertIn("already exists", err)
        code, out, err = self.cli(*self.write_args())                  # a dry run refuses as well
        self.assertEqual(code, 2)
        self.assertEqual(self.fx.record.read_bytes(), first)
        with self.assertRaises(SR.SheetRecordError):
            SR.write_record(self.fx.lit, json.loads(first), self.fx.sheet.read_bytes(), self.fx.sheet)
        self.assertEqual(self.fx.record.read_bytes(), first)

    def test_sheet_changed_while_preparing_is_refused(self):
        self.fx.ledger_default()
        record, raw = SR.build_record(self.fx.lit, AUTH)
        self.fx.sheet.write_bytes(raw + b" ")
        with self.assertRaisesRegex(SR.SheetRecordError, "changed while"):
            SR.write_record(self.fx.lit, record, raw, self.fx.sheet)
        self.assertFalse(self.fx.record.exists())

    def test_numeric_not_lexicographic_id_order(self):
        ids = ["P99", "P100"] + [f"P{n}" for n in range(101, 159)]
        fx = Fix(ids=ids)
        self.addCleanup(fx.cleanup)
        fx.ledger_default()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(SR.main(["write", "--lit-dir", str(fx.lit), "--authorization", AUTH]), 0)
        rows = fx.sheet_rows()
        fx.sheet.unlink()
        fx.write_sheet(rows=sorted(rows, key=lambda r: r["paper_id"]))             # lexicographic order: P100 before P99
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(SR.main(["write", "--lit-dir", str(fx.lit), "--authorization", AUTH]), 2)


class SheetChecks(SheetRecordBase):
    def setUp(self):
        super().setUp()
        self.fx.ledger_default()

    def replace_sheet(self, **kw):
        self.fx.sheet.unlink(missing_ok=True)
        self.fx.write_sheet(**kw)

    def test_wrong_row_counts(self):
        rows = self.fx.sheet_rows()
        for n_rows in (rows[:-1], rows + [dict(rows[0], paper_id="P9999")]):
            self.replace_sheet(rows=n_rows)
            self.refused("data rows")
            self.fx.sheet.unlink()

    def test_column_problems(self):
        base = list(ps.ALLOWED_COLUMNS)
        cases = {"reordered": [base[1], base[0], *base[2:]], "missing": base[:-1],
                 "renamed": [*base[:-1], "decision"], "extra": [*base, "researcher_decision"]}
        for name, header in cases.items():
            rows = [{c: "x" for c in header} for _ in range(60)]
            self.replace_sheet(rows=[dict(r, paper_id=pid) for r, pid in zip(rows, self.fx.ids)], header=header)
            self.refused("header differs")
            self.fx.sheet.unlink()

    def test_bom_and_invalid_utf8(self):
        self.replace_sheet(bom=True)
        self.refused("byte-order mark")
        self.fx.sheet.unlink()
        self.fx.write_sheet()
        raw = self.fx.sheet.read_bytes().replace(b"synthetic title", "synth\xe9tic title".encode("latin-1"), 1)
        self.fx.sheet.write_bytes(raw)
        self.refused("not valid UTF-8")

    def test_cell_count(self):
        raw = self.fx.sheet.read_bytes().decode("utf-8").split("\r\n")
        raw[5] = raw[5].rsplit(",", 1)[0]                                              # drop the last cell of a row
        self.fx.sheet.write_bytes("\r\n".join(raw).encode("utf-8"))
        err = self.refused("cells")
        self.assertIn("(expected 7)", err)

    def test_id_problems(self):
        rows = self.fx.sheet_rows()
        cases = {"unexpected id": [dict(rows[0], paper_id="P9998")] + rows[1:],
                 "duplicate id": [rows[0], dict(rows[1], paper_id=rows[0]["paper_id"])] + rows[2:],
                 "malformed id": [dict(rows[0], paper_id="X0001")] + rows[1:],
                 "reordered": [rows[1], rows[0]] + rows[2:]}
        needles = {"unexpected id": "differ from the pilot sample", "duplicate id": "duplicate paper_id",
                   "malformed id": "malformed paper_id", "reordered": "ascending numeric"}
        for name, rr in cases.items():
            self.replace_sheet(rows=rr)
            self.refused(needles[name])
            self.fx.sheet.unlink()

    def test_abstract_and_status_problems(self):
        rows = self.fx.sheet_rows()
        miss = next(i for i, r in enumerate(rows) if r["abstract"] == "")
        have = next(i for i, r in enumerate(rows) if r["abstract"] != "")
        cases = {"missing abstract without status": dict(rows[miss], abstract_status=""),
                 "abstract with a status": dict(rows[have], abstract_status="unavailable"),
                 "invalid status label": dict(rows[miss], abstract_status="n/a"),
                 "placeholder left in the file": dict(rows[miss], abstract="[Abstract not available]")}
        for name, row in cases.items():
            i = miss if "missing" in name or "invalid" in name or "placeholder" in name else have
            rr = list(rows)
            rr[i] = row
            self.replace_sheet(rows=rr)
            self.refused("abstract_status", )
            self.fx.sheet.unlink()


class LedgerChecks(SheetRecordBase):
    def test_no_ledger_entries(self):
        self.refused("ledger holds 0 'started' entries")

    def test_sheet_run_started_but_not_completed(self):
        self.fx.ledger_run("pilot_sample", T_DRAW, T_DRAW)
        pr.record_authorisation_start(self.fx.lit, AUTH, CLAUSE, "pilot_sheet", T_SHEET_START)
        self.fx.commit()
        self.refused("'completed' entries for pilot_sheet")

    def test_draw_missing(self):
        self.fx.ledger_run("pilot_sheet", T_SHEET_START, T_SHEET_DONE, {"inventory_sha256": self.fx.inv_sha, "rows": "60"})
        self.refused("pilot_sample")

    def test_another_authorisation_is_not_accepted(self):
        self.fx.ledger_run("pilot_sample", T_DRAW, T_DRAW, ref="D-999")
        self.fx.ledger_run("pilot_sheet", T_SHEET_START, T_SHEET_DONE,
                           {"inventory_sha256": self.fx.inv_sha, "rows": "60"}, ref="D-999")
        self.refused("ledger holds 0")

    def test_row_count_and_inventory_mismatch_in_ledger(self):
        self.fx.ledger_default(rows="59")
        self.refused("row count differs")

    def test_inventory_hash_mismatch_in_ledger(self):
        self.fx.ledger_default(inv="0" * 64)
        self.refused("inventory hash differs")

    def test_sheet_recorded_before_the_draw(self):
        self.fx.ledger_run("pilot_sheet", T_SHEET_START, T_SHEET_DONE, {"inventory_sha256": self.fx.inv_sha, "rows": "60"})
        self.fx.ledger_run("pilot_sample", T_DRAW, T_DRAW)
        self.refused("before the draw")

    def test_other_tool_under_the_authorisation(self):
        self.fx.ledger_default()
        pr._append_ledger(self.fx.lit, {"authorization": AUTH, "clause": CLAUSE, "tool": "stage0", "event": "started",
                                        "run_time_utc": "2031-02-04T00:00:00+00:00"})
        self.fx.commit()
        self.refused("other tools")

    def test_broken_hash_chain(self):
        self.fx.ledger_default()
        text = self.fx.ledger.read_text(encoding="utf-8")
        self.fx.ledger.write_text(text.replace(T_DRAW, "2031-02-03T04:00:09+00:00", 1), encoding="utf-8")
        self.refused("hash chain")

    def test_malformed_completion_time(self):
        self.fx.ledger_run("pilot_sample", T_DRAW, T_DRAW)
        self.fx.ledger_run("pilot_sheet", T_SHEET_START, "13 Nov 2031",
                           {"inventory_sha256": self.fx.inv_sha, "rows": "60"})
        self.refused("completion time is malformed")


class SampleAndGitChecks(SheetRecordBase):
    def test_sample_and_sidecar_problems(self):
        self.fx.ledger_default()
        self.fx.write_sample(sidecar_over={"sample_size": 59})
        self.refused("sample_size")
        self.fx.write_sample(sidecar_over={"authorization": "D-123"})
        self.refused("authorisation differs")
        self.fx.write_sample(sidecar_over={"allocation": {"A": 1, "B": 1}})
        self.refused("stratum counts differ")
        self.fx.write_sample()
        (self.fx.lit / "paper_inventory.json").write_bytes(b"[]\n")
        self.refused("inventory changed since the draw")

    def test_missing_provenance_sidecar(self):
        self.fx.ledger_default()
        (self.fx.lit / "screening" / "pilot_sample.provenance.json").unlink()
        self.refused("missing required input")

    def test_sample_of_59_records(self):
        fx = Fix(ids=IDS60[:-1], abstract_missing=(4,))
        self.addCleanup(fx.cleanup)
        fx.ledger_default(rows="59")
        self.fx = fx
        self.refused("does not hold 60")

    def test_tracked_sheet_is_refused(self):
        self.fx.ledger_default()
        self.fx.git("add", "-f", str(self.fx.sheet))
        self.fx.git("commit", "-q", "-m", "track the sheet")
        self.refused("not Git-ignored")

    def test_sheet_not_ignored_is_refused(self):
        self.fx.ledger_default()
        (self.fx.root / ".gitignore").write_text("", encoding="utf-8")
        self.refused("not Git-ignored")

    def test_ignored_record_path_is_refused(self):
        self.fx.ledger_default()
        with open(self.fx.root / ".gitignore", "a", encoding="utf-8") as f:
            f.write("research/literature/screening/pilot_sheet_record.json\n")
        self.refused("Git-ignored")

    def test_not_a_git_repository(self):
        self.fx.ledger_default()
        shutil.rmtree(self.fx.root / ".git")
        self.refused("not Git-ignored")

    def test_missing_sheet_file(self):
        self.fx.ledger_default()
        self.fx.sheet.unlink()
        self.refused("sheet file not found")

    def test_malformed_authorisation_argument(self):
        self.fx.ledger_default()
        self.refused("malformed authorization", auth="D122")


class VerifyMode(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.d = Path(self.tmp.name)
        self.data = b"\xff\xfe not a csv at all \x00\x01 \r\n" * 40                  # deliberately not parseable
        self.file = self.d / "received.bin"
        self.file.write_bytes(self.data)
        self.rec = self.d / "record.json"
        record = {"authorization": AUTH, "columns": list(ps.ALLOWED_COLUMNS), "generated_utc": T_SHEET_DONE, "rows": 60,
                  "sha256": hashlib.sha256(self.data).hexdigest(), "size_bytes": len(self.data)}
        self.rec.write_text(SR.record_text(record), encoding="utf-8")

    def cli(self, f=None):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = SR.main(["verify", "--record", str(self.rec), "--file", str(f or self.file)])
        return code, out.getvalue(), err.getvalue()

    def test_match_without_parsing(self):
        with mock.patch.object(SR.csv, "reader", side_effect=AssertionError("parsed")), \
                mock.patch.object(SR.csv, "DictReader", side_effect=AssertionError("parsed")):
            code, out, err = self.cli()
        self.assertEqual((code, err), (0, ""))
        self.assertTrue(out.startswith("MATCH"))

    def test_one_byte_change_of_equal_size_is_a_mismatch(self):
        alt = bytearray(self.data)
        alt[10] ^= 0x01
        other = self.d / "altered.bin"
        other.write_bytes(bytes(alt))
        code, out, _ = self.cli(other)
        self.assertEqual(code, 2)
        self.assertIn("MISMATCH", out)
        self.assertIn("size %d (equal)" % len(self.data), out)
        self.assertIn("(DIFFERS)", out)

    def test_size_change_is_a_mismatch(self):
        other = self.d / "short.bin"
        other.write_bytes(self.data[:-1])
        code, out, _ = self.cli(other)
        self.assertEqual(code, 2)
        self.assertIn("size %d (DIFFERS)" % (len(self.data) - 1), out)

    def test_bad_record_or_missing_file(self):
        self.rec.write_text("{not json", encoding="utf-8")
        self.assertEqual(self.cli()[0], 2)
        self.rec.write_text(json.dumps({"sha256": "0" * 64}), encoding="utf-8")
        self.assertEqual(self.cli()[0], 2)
        self.assertEqual(self.cli(self.d / "absent.bin")[0], 2)


class RecordSchema(unittest.TestCase):
    GOOD = {"authorization": AUTH, "columns": list(ps.ALLOWED_COLUMNS), "generated_utc": T_SHEET_DONE, "rows": 60,
            "sha256": "a" * 64, "size_bytes": 1234}

    def test_good_record_passes(self):
        self.assertEqual(SR.validate_record(dict(self.GOOD)), self.GOOD)

    def test_each_violation_is_rejected(self):
        bad = {"missing key": {k: v for k, v in self.GOOD.items() if k != "rows"},
               "extra key": dict(self.GOOD, titles=["x"]),
               "authorisation form": dict(self.GOOD, authorization="D122"),
               "reordered columns": dict(self.GOOD, columns=list(reversed(ps.ALLOWED_COLUMNS))),
               "time without offset": dict(self.GOOD, generated_utc="2031-02-03T04:10:07"),
               "time with other offset": dict(self.GOOD, generated_utc="2031-02-03T04:10:07+01:00"),
               "rows 59": dict(self.GOOD, rows=59), "rows as text": dict(self.GOOD, rows="60"),
               "uppercase hash": dict(self.GOOD, sha256="A" * 64), "short hash": dict(self.GOOD, sha256="a" * 63),
               "size zero": dict(self.GOOD, size_bytes=0), "size as bool": dict(self.GOOD, size_bytes=True),
               "size as text": dict(self.GOOD, size_bytes="12")}
        for name, rec in bad.items():
            with self.assertRaises(SR.SheetRecordError, msg=name):
                SR.validate_record(rec)

    def test_real_record_if_present_is_valid(self):
        # state-independent: nothing is required of the real repository before the pilot sheet exists
        path = REPO / "research" / "literature" / SR.RECORD_REL
        if path.exists():
            SR.validate_record(json.loads(path.read_text(encoding="utf-8")))

    def test_module_uses_only_the_standard_library(self):
        src = (REPO / "scripts" / "literature" / "pilot_sheet_record.py").read_text(encoding="utf-8")
        mods = {m.group(1).split(".")[0] for m in re.finditer(r"^(?:import|from)\s+([A-Za-z_][\w.]*)", src, re.M)}
        mods -= {"__future__"}
        self.assertTrue(mods <= set(sys.stdlib_module_names) | {"pubrecords", "pilot_sheet"}, msg=mods)


if __name__ == "__main__":
    unittest.main()
