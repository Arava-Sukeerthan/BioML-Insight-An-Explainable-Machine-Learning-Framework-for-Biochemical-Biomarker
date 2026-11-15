"""Tests for scripts/literature/pilot_commitment.py (PROPOSED R2-solo revision of D-102/D-109).
SYNTHETIC paper IDs, decisions and salts in temporary directories only; no real pilot sample, decision,
salt or commitment is created, and nothing is written inside the repository."""
import contextlib
import csv
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "literature"))
sys.path.insert(0, str(REPO / "tests" / "literature"))
import pilot_commitment as PC  # noqa: E402
import pilot_agreement as pa  # noqa: E402
from test_flow_diagram import row  # noqa: E402

CV = "criteria_v1.1+protocol_v0.2"
IDS = ["P0010", "P0002", "P0101", "P0007"]            # deliberately unsorted; template order is numeric
SALT = "0123456789abcdef" * 4                          # synthetic test salt, never a real one


def decision_rows(screener="researcher", **over):
    rows = [row("P0002", "title_abstract", "exclude", "E4", screener=screener),
            row("P0007", "title_abstract", "include", screener=screener),
            row("P0010", "title_abstract", "uncertain", screener=screener),
            row("P0101", "title_abstract", "exclude", "E5", screener=screener)]
    for r in rows:
        r.update({"criteria_version": CV, **over})
    return rows


class PilotCommitment(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.d = Path(self.tmp.name)
        self.sample = self.d / "pilot_sample.csv"
        with open(self.sample, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["paper_id", "stratum"])
            w.writeheader()
            w.writerows({"paper_id": p, "stratum": "B"} for p in IDS)
        self.out = self.d / "private"

    def write(self, rows, name="edited.csv", order=None, bom=False, lineterminator="\r\n", header=None):
        p = self.d / name
        rows = [rows[i] for i in order] if order else rows
        buf = io.StringIO(newline="")
        w = csv.DictWriter(buf, fieldnames=header or pa.TEMPLATE_COLUMNS, lineterminator=lineterminator,
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
        p.write_bytes((b"\xef\xbb\xbf" if bom else b"") + buf.getvalue().encode("utf-8"))
        return p

    def make(self, path, screener="researcher", **kw):
        return PC.make(path, self.sample, screener, CV, self.out, lit_dir=self.d, **kw)

    # ---- formula
    def test_formula_known_answer(self):
        data = b"a,b\r\n1,2\r\n"
        expected = hashlib.sha256(b"bioml-insight pilot commitment v1\n" + SALT.encode() + b"\n" + data).hexdigest()
        self.assertEqual(PC.commitment(SALT, data), expected)
        for bad in ("", SALT.upper(), SALT[:-1], SALT + "0", "g" * 64):
            with self.assertRaises(PC.CommitmentError):
                PC.commitment(bad, data)

    # ---- canonicalisation
    def test_equivalent_inputs_give_identical_canonical_bytes(self):
        base = PC.canonical_bytes(self.write(decision_rows()), IDS, "researcher", CV)
        variants = [self.write(decision_rows(), "v1.csv", order=[3, 1, 0, 2]),          # other row order
                    self.write(decision_rows(), "v2.csv", bom=True),                     # Excel BOM
                    self.write(decision_rows(), "v3.csv", lineterminator="\n")]          # LF line endings
        for v in variants:
            self.assertEqual(PC.canonical_bytes(v, IDS, "researcher", CV), base, msg=v.name)
        self.assertFalse(base.startswith(b"\xef\xbb\xbf"))
        self.assertTrue(base.endswith(b"\r\n"))
        ids_in_order = [r["paper_id"] for r in csv.DictReader(io.StringIO(base.decode()))]
        self.assertEqual(ids_in_order, ["P0002", "P0007", "P0010", "P0101"])

    def test_invalid_files_refused_not_repaired(self):
        rows = decision_rows()
        cases = {
            "header": self.write(rows, "h.csv", header=pa.TEMPLATE_COLUMNS[::-1]),
            "missing row": self.write(rows[:3], "m.csv"),
            "extra row": self.write(rows + [row("P0999", "title_abstract", "exclude", "E4",
                                                screener="researcher", criteria_version=CV)], "x.csv"),
            "duplicate": self.write(rows + [rows[0]], "d.csv"),
            "screener": self.write(decision_rows(screener="assistant"), "s.csv"),
            "criteria_version": self.write(decision_rows(criteria_version="criteria_v1.0+protocol_v0.2"), "c.csv"),
            "decision": self.write([dict(rows[0], decision="maybe")] + rows[1:], "dec.csv"),
            "whitespace": self.write([dict(rows[0], reason_code="E4 ")] + rows[1:], "w.csv"),
            "stage": self.write([dict(rows[0], stage="full_text")] + rows[1:], "st.csv"),
            "validator": self.write([dict(rows[0], reason_code="")] + rows[1:], "v.csv"),   # exclude without code
        }
        for name, p in cases.items():
            with self.assertRaises(PC.CommitmentError, msg=name):
                PC.canonical_bytes(p, IDS, "researcher", CV)
        latin = self.d / "latin1.csv"
        latin.write_bytes(self.write(rows).read_bytes().replace(b"synthetic", "synth\xe9tic".encode("latin-1")))
        with self.assertRaisesRegex(PC.CommitmentError, "not UTF-8"):
            PC.canonical_bytes(latin, IDS, "researcher", CV)

    # ---- make / verify
    def test_make_then_verify_round_trip(self):
        rec, names = self.make(self.write(decision_rows()), salt=SALT)
        self.assertEqual(sorted(rec), sorted(PC.RECORD_KEYS))
        self.assertEqual((rec["rows"], rec["screener"], rec["criteria_version"]), (4, "researcher", CV))
        self.assertEqual(rec["sample_sha256"], hashlib.sha256(self.sample.read_bytes()).hexdigest())
        self.assertEqual(rec["commitment"], PC.commitment(SALT, names["file"].read_bytes()))
        text = names["record"].read_text()
        self.assertNotIn(SALT, text)                                     # the record never holds the salt
        for word in ("include", "exclude", "E4", "synthetic"):           # ... nor any decision content
            self.assertNotIn(word, text)
        self.assertEqual(PC.verify(names["file"], names["salt"], names["record"], self.sample, lit_dir=self.d)["commitment"],
                         rec["commitment"])

    def test_salt_is_fresh_256_bit_hex(self):
        with mock.patch.object(PC.secrets, "token_hex", wraps=PC.secrets.token_hex) as th:
            _, names = self.make(self.write(decision_rows()))
        th.assert_called_once_with(32)
        self.assertRegex(names["salt"].read_text(), r"^[0-9a-f]{64}\n$")

    def test_make_never_overwrites(self):
        self.make(self.write(decision_rows()), salt=SALT)
        with self.assertRaisesRegex(PC.CommitmentError, "already exists"):
            self.make(self.write(decision_rows(), "again.csv"), salt=SALT)

    def test_mismatches_are_integrity_failures(self):
        rec, names = self.make(self.write(decision_rows()), salt=SALT)
        other = self.d / "other.salt"
        other.write_text("f" * 64 + "\n")
        with self.assertRaisesRegex(PC.CommitmentError, "INTEGRITY FAILURE"):
            PC.verify(names["file"], other, names["record"], self.sample, lit_dir=self.d)
        changed = self.d / "changed" / names["file"].name
        changed.parent.mkdir()
        changed.write_bytes(names["file"].read_bytes().replace(b",include,", b",exclude,E4", 1))
        with self.assertRaises(PC.CommitmentError):                                   # altered decision
            PC.verify(changed, names["salt"], names["record"], self.sample, lit_dir=self.d)
        noncanon = self.d / "noncanon.csv"
        noncanon.write_bytes(names["file"].read_bytes().replace(b"\r\n", b"\n"))
        with self.assertRaisesRegex(PC.CommitmentError, "not the canonical file"):
            PC.verify(noncanon, names["salt"], names["record"], self.sample, lit_dir=self.d)
        rec2 = dict(rec, sample_sha256="0" * 64)
        bad_rec = self.d / "bad.json"
        bad_rec.write_text(json.dumps(rec2))
        with self.assertRaisesRegex(PC.CommitmentError, "sample SHA-256"):
            PC.verify(names["file"], names["salt"], bad_rec, self.sample, lit_dir=self.d)
        bad_rec.write_text(json.dumps(dict(rec, extra=1)))
        with self.assertRaisesRegex(PC.CommitmentError, "malformed commitment record"):
            PC.verify(names["file"], names["salt"], bad_rec, self.sample, lit_dir=self.d)

    def test_frozen_criteria_version_enforced_with_repository_registry(self):
        p = self.write(decision_rows(criteria_version="criteria_vX.Y+protocol_vX.Z"))
        PC.canonical_bytes(p, IDS, "researcher", "criteria_vX.Y+protocol_vX.Z", lit_dir=self.d)   # no registry
        with self.assertRaises(PC.CommitmentError):              # the real registry knows only the frozen version
            PC.canonical_bytes(p, IDS, "researcher", "criteria_vX.Y+protocol_vX.Z",
                               lit_dir=REPO / "research" / "literature")

    def test_cli_make_and_verify_exit_codes(self):
        p = self.write(decision_rows())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(PC.main(["make", "--file", str(p), "--sample", str(self.sample), "--screener", "researcher",
                                      "--criteria-version", CV, "--out-dir", str(self.out), "--lit-dir", str(self.d)]), 0)
        self.assertIn("send ONLY", out.getvalue())
        self.assertNotIn(self.out.joinpath("pilot_researcher_commitment.salt").read_text().strip(), out.getvalue())
        args = ["verify", "--file", str(self.out / "pilot_decisions_researcher.csv"),
                "--salt-file", str(self.out / "pilot_researcher_commitment.salt"),
                "--record", str(self.out / "pilot_researcher_commitment.json"), "--sample", str(self.sample),
                "--lit-dir", str(self.d)]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(PC.main(args), 0)
        (self.out / "pilot_researcher_commitment.salt").write_text("e" * 64 + "\n")
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(PC.main(args), 2)

    # ---- Git order
    def test_order_check(self):
        def repo_with(order):
            d = Path(tempfile.mkdtemp(dir=self.d))
            g = lambda *a: subprocess.run(["git", *a], cwd=d, check=True, capture_output=True)   # noqa: E731
            g("init", "-q")
            g("config", "user.email", "fixture@example.invalid")
            g("config", "user.name", "fixture")
            g("config", "commit.gpgsign", "false")
            s = d / "research" / "literature" / "screening"
            s.mkdir(parents=True)
            for group in order:
                for name in group:
                    (s / name).write_text("x\n")
                g("add", "-A")
                g("commit", "-q", "-m", "step")
            return d
        names = PC.ORDER_PATHS
        self.assertEqual(list(PC.check_order(repo_with([[n] for n in names]))), list(names))
        swapped = [[names[0]], [names[2]], [names[1]], [names[3]]]      # researcher file before assistant commitment
        with self.assertRaisesRegex(PC.CommitmentError, "order violated"):
            PC.check_order(repo_with(swapped))
        same = [[names[0], names[1]], [names[2]], [names[3]]]            # two steps in one commit
        with self.assertRaisesRegex(PC.CommitmentError, "order violated"):
            PC.check_order(repo_with(same))
        with self.assertRaisesRegex(PC.CommitmentError, "exactly one adding commit"):
            PC.check_order(repo_with([[n] for n in names[:3]]))

    def test_tool_uses_only_the_standard_library(self):
        for name in ("pilot_commitment.py", "pilot_agreement.py", "pubrecords.py"):
            src = (REPO / "scripts" / "literature" / name).read_text(encoding="utf-8")
            imports = {line.split()[1].split(".")[0] for line in src.splitlines()
                       if line.startswith(("import ", "from ")) and not line.startswith("from __future__")}
            self.assertTrue(imports <= set(sys.stdlib_module_names) | {"pubrecords", "pilot_agreement"},
                            msg=(name, imports - set(sys.stdlib_module_names)))


if __name__ == "__main__":
    unittest.main()
