"""Pilot screening commitments for the single-researcher workflow (R2-solo; PROPOSED revision of D-102 and
D-109, not yet approved). Standard library only, so that the researcher can run it on their own computer,
outside any assistant session, from a plain download of the repository.

Commitment formula (decision sheet 2026-11-12 §1 row 6, drafted for R1-min and reused unchanged):
    C = SHA-256( b"bioml-insight pilot commitment v1\\n" + S + b"\\n" + F )
S = 64 lowercase hex characters (256-bit salt, ASCII); F = the canonical bytes of the pilot decision file.

Canonical file F: UTF-8 without BOM; header exactly pilot_agreement.TEMPLATE_COLUMNS (in that order); one
title_abstract row per sampled paper_id, in the template order (ascending numeric paper_id); written by
csv.DictWriter with its default CRLF line terminator (the template convention). `make` re-reads the edited
file (a BOM is tolerated on input), validates it and re-serialises it; the CANONICAL file it writes is the
one to disclose. A file that fails a check is refused, never repaired.

Subcommands
  make    (researcher, own computer)  validate + canonicalise the decision file, generate the salt, write
          <out-dir>/pilot_decisions_<screener>.csv (canonical), <out-dir>/pilot_<screener>_commitment.salt and
          <out-dir>/pilot_<screener>_commitment.json; print the commitment. Refuses to overwrite.
  verify  (after disclosure)  recompute the commitment from the disclosed file and salt and compare it with
          the commitment record; checks row count, criteria_version, screener and sample SHA-256.
  order   (in the repository)  check in Git history that the commitment files and the disclosed files were
          added in the order researcher commitment -> assistant commitment -> researcher file -> assistant file.
Exit status: 0 = success, 2 = refused or mismatch (message on stderr).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import re
import secrets
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pubrecords as pr  # noqa: E402  (standard library only)
import pilot_agreement as pa  # noqa: E402  (standard library only)

FORMULA = "sha256(b'bioml-insight pilot commitment v1\\n' + salt + b'\\n' + canonical_file) v1"
PREFIX = b"bioml-insight pilot commitment v1\n"
SALT_RE = re.compile(r"[0-9a-f]{64}")
SCREENERS = ("researcher", "assistant")
DECISIONS = ("include", "exclude", "uncertain")
RECORD_KEYS = ("formula", "screener", "commitment", "rows", "criteria_version", "sample_sha256", "created_utc")


class CommitmentError(ValueError):
    pass


def commitment(salt, canonical_bytes):
    if not isinstance(salt, str) or not SALT_RE.fullmatch(salt):
        raise CommitmentError("salt must be 64 lowercase hex characters")
    return hashlib.sha256(PREFIX + salt.encode("ascii") + b"\n" + canonical_bytes).hexdigest()


def sample_ids(sample_path):
    with open(sample_path, newline="", encoding="utf-8") as f:
        ids = [r["paper_id"] for r in csv.DictReader(f)]
    if not ids or len(ids) != len(set(ids)):
        raise CommitmentError(f"{sample_path}: empty sample or duplicate paper_id")
    return ids


def _ordered(ids):
    return sorted(ids, key=pa._pid_key)                  # the order of pilot_agreement.make_template


def canonical_bytes(path, ids, screener, criteria_version, lit_dir=None):
    """Read a pilot decision file, check it and return its canonical bytes. Never repairs content."""
    if screener not in SCREENERS:
        raise CommitmentError(f"screener must be one of {SCREENERS}")
    raw = Path(path).read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise CommitmentError(f"{path}: not UTF-8") from None
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if reader.fieldnames != pa.TEMPLATE_COLUMNS:
        raise CommitmentError(f"{path}: header differs from the pilot template columns")
    rows = list(reader)
    problems = []
    for n, r in enumerate(rows, start=2):
        if None in r or any(v is None for v in r.values()):
            problems.append(f"line {n}: wrong number of cells")
            continue
        for k, v in r.items():
            if v != v.strip():
                problems.append(f"line {n}: leading/trailing whitespace in {k}")
        if r["stage"] != "title_abstract":
            problems.append(f"line {n}: stage {r['stage']!r}")
        if r["screener"] != screener:
            problems.append(f"line {n}: screener {r['screener']!r} (expected {screener!r})")
        if r["criteria_version"] != criteria_version:
            problems.append(f"line {n}: criteria_version {r['criteria_version']!r}")
        if r["decision"] not in DECISIONS:
            problems.append(f"line {n}: decision {r['decision']!r}")
    got = [r["paper_id"] for r in rows]
    if len(got) != len(set(got)):
        problems.append("duplicate paper_id")
    if set(got) != set(ids):
        problems.append(f"paper_ids differ from the sample (missing {sorted(set(ids) - set(got))[:5]}, "
                        f"extra {sorted(set(got) - set(ids))[:5]})")
    if problems:
        raise CommitmentError(f"{path}: " + "; ".join(problems[:10]))
    order = {pid: i for i, pid in enumerate(_ordered(ids))}
    rows.sort(key=lambda r: order[r["paper_id"]])
    out = io.StringIO(newline="")
    w = csv.DictWriter(out, fieldnames=pa.TEMPLATE_COLUMNS)
    w.writeheader()
    w.writerows(rows)
    data = out.getvalue().encode("utf-8")
    _validate_with_pubrecords(data, lit_dir)
    return data


def _validate_with_pubrecords(data, lit_dir):
    """Full screening-record validation by the build's validator; with the repository's literature folder
    the frozen criteria_version registry is enforced as well."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "pilot_decisions.csv"
        p.write_bytes(data)
        try:
            pr.load_screening_decisions(Path(lit_dir or d), p)
        except ValueError as e:
            raise CommitmentError(f"screening-record validation failed: {e}") from None


def make(path, sample_path, screener, criteria_version, out_dir, now=None, salt=None, lit_dir=None):
    out_dir = Path(out_dir)
    names = {"file": out_dir / f"pilot_decisions_{screener}.csv",
             "salt": out_dir / f"pilot_{screener}_commitment.salt",
             "record": out_dir / f"pilot_{screener}_commitment.json"}
    for p in names.values():
        if p.exists():
            raise CommitmentError(f"refused: {p} already exists (never overwritten)")
    ids = sample_ids(sample_path)
    data = canonical_bytes(path, ids, screener, criteria_version, lit_dir)
    salt = salt or secrets.token_hex(32)
    c = commitment(salt, data)
    record = {"formula": FORMULA, "screener": screener, "commitment": c, "rows": len(ids),
              "criteria_version": criteria_version,
              "sample_sha256": hashlib.sha256(Path(sample_path).read_bytes()).hexdigest(),
              "created_utc": (now or dt.datetime.now(dt.timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")}
    out_dir.mkdir(parents=True, exist_ok=True)
    names["file"].write_bytes(data)
    names["salt"].write_text(salt + "\n", encoding="ascii", newline="\n")
    names["record"].write_text(json.dumps(record, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return record, names


def verify(path, salt_path, record_path, sample_path, lit_dir=None):
    record = json.loads(Path(record_path).read_text(encoding="utf-8"))
    if sorted(record) != sorted(RECORD_KEYS) or record.get("formula") != FORMULA:
        raise CommitmentError(f"{record_path}: malformed commitment record")
    salt_text = Path(salt_path).read_text(encoding="ascii")
    if not re.fullmatch(r"[0-9a-f]{64}\n?", salt_text):
        raise CommitmentError(f"{salt_path}: malformed salt")
    ids = sample_ids(sample_path)
    if hashlib.sha256(Path(sample_path).read_bytes()).hexdigest() != record["sample_sha256"]:
        raise CommitmentError("sample SHA-256 differs from the commitment record")
    if record["rows"] != len(ids):
        raise CommitmentError("row count differs from the sample")
    raw = Path(path).read_bytes()
    data = canonical_bytes(path, ids, record["screener"], record["criteria_version"], lit_dir)
    if raw != data:
        raise CommitmentError(f"{path}: disclosed file is not the canonical file written by `make`")
    if commitment(salt_text.strip(), data) != record["commitment"]:
        raise CommitmentError("INTEGRITY FAILURE: the disclosed file and salt do not reproduce the commitment")
    return record


ORDER_PATHS = ("pilot_researcher_commitment.json", "pilot_assistant_commitment.json",
               "pilot_decisions_researcher.csv", "pilot_decisions_assistant.csv")


def _first_added(repo, relpath):
    out = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H", "--", relpath], cwd=repo,
                         capture_output=True, text=True, timeout=60)
    shas = out.stdout.split()
    if out.returncode != 0 or len(shas) != 1:
        raise CommitmentError(f"{relpath}: expected exactly one adding commit (found {len(shas)})")
    return shas[0]


def check_order(repo, screening_rel="research/literature/screening"):
    """Each file must be added in its own commit, each commit a strict descendant of the previous one."""
    shas = [_first_added(repo, f"{screening_rel}/{name}") for name in ORDER_PATHS]
    for (a, na), (b, nb) in zip(zip(shas, ORDER_PATHS), zip(shas[1:], ORDER_PATHS[1:])):
        anc = subprocess.run(["git", "merge-base", "--is-ancestor", a, b], cwd=repo, capture_output=True, timeout=60)
        if a == b or anc.returncode != 0:
            raise CommitmentError(f"order violated: {na} ({a[:7]}) is not committed strictly before {nb} ({b[:7]})")
    return dict(zip(ORDER_PATHS, shas))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("make")
    m.add_argument("--file", required=True)
    m.add_argument("--sample", required=True, help="pilot_sample.csv")
    m.add_argument("--screener", required=True, choices=SCREENERS)
    m.add_argument("--criteria-version", required=True)
    m.add_argument("--out-dir", required=True, help="a private folder; never the repository")
    v = sub.add_parser("verify")
    v.add_argument("--file", required=True)
    v.add_argument("--salt-file", required=True)
    v.add_argument("--record", required=True)
    v.add_argument("--sample", required=True)
    for sp in (m, v):
        sp.add_argument("--lit-dir", default=str(HERE.parents[1] / "research" / "literature"),
                        help="literature folder (frozen criteria_version registry); default: this repository")
    o = sub.add_parser("order")
    o.add_argument("--repo", default=str(HERE.parents[1]))
    a = ap.parse_args(argv)
    try:
        if a.cmd == "make":
            rec, names = make(a.file, a.sample, a.screener, a.criteria_version, a.out_dir, lit_dir=a.lit_dir)
            print(f"commitment {rec['commitment']}\nsend ONLY: {names['record']}\n"
                  f"keep private until disclosure: {names['file']} and {names['salt']}")
        elif a.cmd == "verify":
            rec = verify(a.file, a.salt_file, a.record, a.sample, lit_dir=a.lit_dir)
            print(f"verified: {rec['screener']} file reproduces commitment {rec['commitment']}")
        else:
            for name, sha in check_order(a.repo).items():
                print(f"{sha[:12]}  {name}")
            print("order verified")
    except (CommitmentError, OSError, json.JSONDecodeError) as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
