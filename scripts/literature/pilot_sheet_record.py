"""Pilot sheet record (decision D-125): the six-field metadata record of the blinded pilot sheet.

PROPOSED tool, standard library only. It never modifies the sheet and never writes the run-authorisation
ledger, so it does not consume any authorisation. It prints and records no paper identifier, title or
abstract: its output and error messages contain counts, field names and hashes only.

Record (exactly these six fields; keys sorted, indent 1, UTF-8, LF, trailing newline):
  authorization  the D-077 (6) authorisation (decision ID) under which the sheet was generated
  columns        the seven ordered sheet columns (pilot_sheet.ALLOWED_COLUMNS)
  generated_utc  `run_time_utc` of the COMPLETED `pilot_sheet` entry of the run-authorisation ledger
  rows           number of data rows (60)
  sha256         SHA-256 of the exact bytes of the sheet file
  size_bytes     size of the sheet file in bytes

Subcommands
  write   Dry run by default: reads the sheet (read-only) and validates it; with --write it creates
          <lit-dir>/screening/pilot_sheet_record.json and refuses to overwrite an existing record.
          Checks, all fail-closed: the sheet is Git-ignored and untracked; the record path does not exist and
          is not ignored (so it can be committed); the sheet is UTF-8 without a BOM with exactly the seven
          allowed columns in order and 60 data rows of seven cells; its paper IDs equal the pilot sample (no
          duplicates, ascending numeric order); abstract and abstract_status are consistent (D-068 (8), D-079);
          the sample and its provenance sidecar agree with the inventory and the authorisation; the ledger
          chain is intact and holds exactly one completed `pilot_sample` and one completed `pilot_sheet` run
          under the authorisation, the latter with the same row count and inventory hash.
  verify  Hash-and-size comparison of a file with a record. The file is read as bytes only and never parsed,
          so it can be used before the file is opened (prompt step 2).
Exit status: 0 = success / match, 2 = refused or mismatch (message on stderr).

Usage:
  python3 -I scripts/literature/pilot_sheet_record.py write --lit-dir research/literature --authorization D-122 [--sheet PATH] [--write]
  python3 -I scripts/literature/pilot_sheet_record.py verify --record PATH --file PATH
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pubrecords as pr  # noqa: E402  (standard library only)
import pilot_sheet as ps  # noqa: E402  (standard library only)

RECORD_KEYS = ("authorization", "columns", "generated_utc", "rows", "sha256", "size_bytes")
RECORD_REL = Path("screening") / "pilot_sheet_record.json"
SAMPLE_REL = Path("screening") / "pilot_sample.csv"
SIDECAR_REL = Path("screening") / "pilot_sample.provenance.json"
EXPECTED_ROWS = 60
CLAUSE = "D-077 (6)"
_AUTH = re.compile(r"D-\d{3}")
_SHA = re.compile(r"[0-9a-f]{64}")
_TIME = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+00:00")
_PID = re.compile(r"P\d+")


class SheetRecordError(ValueError):
    """A check failed. Messages carry counts and field names only, never sheet content."""


def validate_record(record):
    """The record schema: exactly the six fields with the required forms."""
    if not isinstance(record, dict) or sorted(record) != sorted(RECORD_KEYS):
        raise SheetRecordError("record does not have exactly the six required fields")
    if not (isinstance(record["authorization"], str) and _AUTH.fullmatch(record["authorization"])):
        raise SheetRecordError("record: malformed authorization")
    if record["columns"] != list(ps.ALLOWED_COLUMNS):
        raise SheetRecordError("record: columns differ from the allowed columns")
    if not (isinstance(record["generated_utc"], str) and _TIME.fullmatch(record["generated_utc"])):
        raise SheetRecordError("record: malformed generated_utc")
    if not (type(record["rows"]) is int and record["rows"] == EXPECTED_ROWS):
        raise SheetRecordError(f"record: rows is not {EXPECTED_ROWS}")
    if not (isinstance(record["sha256"], str) and _SHA.fullmatch(record["sha256"])):
        raise SheetRecordError("record: malformed sha256")
    if not (type(record["size_bytes"]) is int and record["size_bytes"] >= 1):
        raise SheetRecordError("record: malformed size_bytes")
    return record


def record_text(record):
    return json.dumps(record, indent=1, sort_keys=True, ensure_ascii=True) + "\n"


def inspect_sheet(raw, sample_ids):
    """Validate the sheet bytes against the allow-list, the row count and the sample (read-only)."""
    if len(sample_ids) != EXPECTED_ROWS or len(set(sample_ids)) != len(sample_ids):
        raise SheetRecordError(f"the pilot sample does not hold {EXPECTED_ROWS} distinct records")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise SheetRecordError("sheet is not valid UTF-8") from None
    if text.startswith("\ufeff"):
        raise SheetRecordError("sheet starts with a byte-order mark")
    try:
        table = list(csv.reader(io.StringIO(text, newline="")))
    except csv.Error:
        raise SheetRecordError("sheet is not parseable as CSV") from None
    if not table or table[0] != list(ps.ALLOWED_COLUMNS):
        raise SheetRecordError(f"header differs from the {len(ps.ALLOWED_COLUMNS)} allowed columns in order")
    body = table[1:]
    if len(body) != EXPECTED_ROWS:
        raise SheetRecordError(f"sheet has {len(body)} data rows (expected {EXPECTED_ROWS})")
    for n, row in enumerate(body, start=1):
        if len(row) != len(ps.ALLOWED_COLUMNS):
            raise SheetRecordError(f"data row {n} has {len(row)} cells (expected {len(ps.ALLOWED_COLUMNS)})")
    ids = [r[0] for r in body]
    if not all(_PID.fullmatch(i) for i in ids) or not all(_PID.fullmatch(i) for i in sample_ids):
        raise SheetRecordError("malformed paper_id values")
    if len(set(ids)) != len(ids):
        raise SheetRecordError(f"sheet has {len(ids) - len(set(ids))} duplicate paper_id values")
    missing, extra = set(sample_ids) - set(ids), set(ids) - set(sample_ids)
    if missing or extra:
        raise SheetRecordError(f"sheet ids differ from the pilot sample ({len(missing)} missing, {len(extra)} unexpected)")
    if ids != sorted(ids, key=lambda p: int(p[1:])):
        raise SheetRecordError("sheet rows are not in ascending numeric paper_id order")
    bad = 0
    for row in body:
        abstract, status = row[2], row[3]
        if ps.is_missing_abstract(abstract):
            bad += (abstract != "") or (status not in ps.ABSTRACT_STATUSES)
        else:
            bad += status != ""
    if bad:
        raise SheetRecordError(f"{bad} rows have an inconsistent abstract / abstract_status combination")


def load_sample(lit, authorization):
    """The pilot sample rows and the inventory hash, after the existing provenance check."""
    sample, side, inv = lit / SAMPLE_REL, lit / SIDECAR_REL, lit / "paper_inventory.json"
    for p in (sample, side, inv):
        if not p.is_file():
            raise SheetRecordError(f"missing required input: {p.name}")
    with open(sample, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    try:
        sidecar = json.loads(side.read_text(encoding="utf-8"))
    except ValueError:
        raise SheetRecordError("the provenance sidecar is not valid JSON") from None
    inv_sha = hashlib.sha256(inv.read_bytes()).hexdigest()
    try:
        ps.verify_sample_provenance(rows, sidecar, inv_sha, authorization)
    except ps.PilotSheetError as e:
        raise SheetRecordError(str(e)) from None
    return rows, inv_sha


def ledger_generation_time(lit, authorization, rows, inv_sha):
    """`run_time_utc` of the completed pilot_sheet ledger entry, after the ledger checks."""
    try:
        uses = pr.authorisation_uses(lit)            # validates the hash chain and the event consistency
    except pr.RunAuthorisationError as e:
        raise SheetRecordError(str(e)) from None
    mine = [(i, e) for i, e in enumerate(uses) if e["authorization"] == authorization]

    def one(tool, event):
        hits = [(i, e) for i, e in mine if e["tool"] == tool and e["event"] == event and e["clause"] == CLAUSE]
        if len(hits) != 1:
            raise SheetRecordError(f"the ledger holds {len(hits)} '{event}' entries for {tool} under "
                                   f"{authorization} (expected 1)")
        return hits[0]

    for tool in ("pilot_sample", "pilot_sheet"):
        one(tool, "started")
    i_sample, _ = one("pilot_sample", "completed")
    i_sheet, done = one("pilot_sheet", "completed")
    if i_sheet < i_sample:
        raise SheetRecordError("the sheet run is recorded before the draw in the ledger")
    other = {e["tool"] for _, e in mine} - {"pilot_sample", "pilot_sheet"}
    if other:
        raise SheetRecordError("the ledger shows other tools under this authorisation")
    if done.get("rows") != str(rows):
        raise SheetRecordError("the ledger's sheet row count differs from the sheet file")
    if done.get("inventory_sha256") != inv_sha:
        raise SheetRecordError("the ledger's inventory hash differs from the inventory")
    stamp = done.get("run_time_utc")
    if not (isinstance(stamp, str) and _TIME.fullmatch(stamp)):
        raise SheetRecordError("the ledger's sheet completion time is malformed")
    return stamp


def _is_ignored(path):
    path = Path(path).resolve()
    git_dir = path.parent
    while not git_dir.exists():
        git_dir = git_dir.parent
    try:
        code = subprocess.run(["git", "-C", str(git_dir), "check-ignore", "-q", str(path)],
                              capture_output=True, timeout=60).returncode
    except (OSError, subprocess.SubprocessError):
        raise SheetRecordError("cannot run git to check the ignore rules") from None
    if code not in (0, 1):
        raise SheetRecordError("git check-ignore failed")
    return code == 0


def check_record_path(lit):
    out = Path(lit) / RECORD_REL
    if out.exists():
        raise SheetRecordError("refused: the sheet record already exists (it is never overwritten)")
    if _is_ignored(out):
        raise SheetRecordError("refused: the record path is Git-ignored, so the record could not be committed")
    return out


def build_record(lit, authorization, sheet=None):
    """Validate everything and return (record, sheet bytes). Writes nothing."""
    lit = Path(lit)
    if not (isinstance(authorization, str) and _AUTH.fullmatch(authorization)):
        raise SheetRecordError("malformed authorization")
    sheet = Path(sheet) if sheet else lit / ps.DEFAULT_SHEET
    if not sheet.is_file():
        raise SheetRecordError("sheet file not found")
    if not ps.path_is_git_ignored(sheet):
        raise SheetRecordError("refused: the sheet is not Git-ignored (or is tracked)")
    check_record_path(lit)
    raw = sheet.read_bytes()                          # one read: the hash, the size and the checks use these bytes
    sample_rows, inv_sha = load_sample(lit, authorization)
    inspect_sheet(raw, [r["paper_id"] for r in sample_rows])
    stamp = ledger_generation_time(lit, authorization, EXPECTED_ROWS, inv_sha)
    record = {"authorization": authorization, "columns": list(ps.ALLOWED_COLUMNS), "generated_utc": stamp,
              "rows": EXPECTED_ROWS, "sha256": hashlib.sha256(raw).hexdigest(), "size_bytes": len(raw)}
    return validate_record(record), raw


def write_record(lit, record, raw, sheet):
    """Create the record without overwriting; re-check that the sheet was not changed meanwhile."""
    out = check_record_path(lit)
    if hashlib.sha256(Path(sheet).read_bytes()).hexdigest() != record["sha256"]:
        raise SheetRecordError("refused: the sheet changed while the record was being prepared")
    try:
        pr.write_new_file_atomically(out, record_text(validate_record(record)))
    except FileExistsError:
        raise SheetRecordError("refused: the sheet record already exists (it is never overwritten)") from None
    return out


def verify_file(record_path, file_path):
    """(match, sha256, size, record): bytes only, the file is never parsed."""
    try:
        record = validate_record(json.loads(Path(record_path).read_text(encoding="utf-8")))
    except ValueError as e:
        if isinstance(e, SheetRecordError):
            raise
        raise SheetRecordError("the record is not valid JSON") from None
    raw = Path(file_path).read_bytes()
    sha, size = hashlib.sha256(raw).hexdigest(), len(raw)
    return (sha == record["sha256"] and size == record["size_bytes"]), sha, size, record


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("write")
    w.add_argument("--lit-dir", required=True)
    w.add_argument("--authorization", required=True)
    w.add_argument("--sheet")
    w.add_argument("--write", action="store_true", help="create the record (default: dry run)")
    v = sub.add_parser("verify")
    v.add_argument("--record", required=True)
    v.add_argument("--file", required=True)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "write":
            record, raw = build_record(a.lit_dir, a.authorization, a.sheet)
            print(record_text(record), end="")
            if a.write:
                sheet = Path(a.sheet) if a.sheet else Path(a.lit_dir) / ps.DEFAULT_SHEET
                out = write_record(a.lit_dir, record, raw, sheet)
                print(f"wrote {out}")
            else:
                print("dry run: nothing written")
        else:
            ok, sha, size, record = verify_file(a.record, a.file)
            print(f"{'MATCH' if ok else 'MISMATCH'}: sha256 {sha} ({'equal' if sha == record['sha256'] else 'DIFFERS'}), "
                  f"size {size} ({'equal' if size == record['size_bytes'] else 'DIFFERS'})")
            return 0 if ok else 2
    except (SheetRecordError, OSError) as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
