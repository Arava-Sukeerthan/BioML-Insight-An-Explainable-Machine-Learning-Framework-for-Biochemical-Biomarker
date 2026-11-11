#!/usr/bin/env python3
"""Stage-0 generator (Phase 1 implementation; researcher authorisation 2026-11-01).

Writes automatic Stage-0 `exclude` rows from source publication types only. It never screens
content. Rules, all from approved decisions:

* Stage-0 types (D-082; D-068 (5); protocol v0.1 §3 via D-025): Editorial, Comment, News,
  Published Erratum -> E5; Retracted Publication -> E7. Letters are not excluded automatically;
  Retraction of Publication is not a Stage-0 type (D-072).
* Several types (D-074): (a) Retracted Publication present -> E7, whatever the other types, and E7
  is the primary Stage-0 code (D-074 (d); D-080 exception); (b) otherwise E5 only if every type is
  a Stage-0 E5 type or a D-028 keep-but-not-used type; (c) any other combination -> no row.
* Approved Phase 1 defaults: A1 publication-level `source_publication_types` with a stop guard
  against the union of member types; A2 closed keep-but-not-used list with stop-and-report for new
  "Clinical Trial…"/"Research Support…" variants (Clinical Trial Protocol is class-bearing and never
  qualifies); A3 stage=title_abstract; A4 UTC run date; A5 the approved justification template.

Interpretation applied (D-082 base rule): a record qualifies under D-074 (b) only if it carries at
least one Stage-0 E5 type; a record with only keep-but-not-used types gets no row.

Running against the real inventory needs, separately: a frozen criteria version (criteria v1.1 §11),
the D-035 record §6 conditions, Q-089 (timing) and the D-074 (f) authorisation. The command-line
entry point refuses to run without a registered frozen version, an authorisation verified against
DECISION_LOG.md (pubrecords.verify_run_authorisation) and a matching inventory SHA-256. Writes are
atomic: the combined file is validated before it replaces screening/decisions.csv.

Phase 1 corrections (researcher authorisation 2026-11-11): verified run authorisation; atomic write;
shared checked Stage-0 guards (check_types), applied to D-044 in-scope records and reused by the
pilot sampler; SHA-256 of publications.jsonl and source_records.jsonl in the run report; run_date
validated as a real calendar date.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pubrecords as pr  # noqa: E402

STAGE0_E5_TYPES = frozenset({"Editorial", "Comment", "News", "Published Erratum"})
STAGE0_E7_TYPE = "Retracted Publication"
# D-028 2a keep-but-not-used types (D-074 (b)); the closed list of the existing code, without
# Retracted Publication, which D-074 (a) handles.
KEEP_NOT_USED_TYPES = frozenset(pr.PUBLICATION_TYPES_IGNORED - {STAGE0_E7_TYPE})
STAGE0_RELEVANT = STAGE0_E5_TYPES | {STAGE0_E7_TYPE}
VARIANT_PREFIXES = ("Clinical Trial", "Research Support")
CLASS_BEARING_EXCEPTIONS = frozenset({"Clinical Trial Protocol"})   # D-028 class study_protocol
# D-044 screening scope (records retrieved by G-1…G-7, Q-PM-01, -02, -03, -11, -12).
D044_QUERY_IDS = frozenset({f"Q-PM-G{i}" for i in range(1, 8)} | {"Q-PM-01", "Q-PM-02", "Q-PM-03",
                                                                  "Q-PM-11", "Q-PM-12"})
STAGE = "title_abstract"                                            # A3
JUSTIFICATION = "Stage 0 (D-074 ({clause})): source publication types = {types}; {code}"   # A5


class Stage0Error(ValueError):
    """Stop-and-report condition; nothing is written."""


def split_types(value):
    """Verbatim source publication types from an inventory value (list or ';'-joined string)."""
    if isinstance(value, (list, tuple)):
        return [t for t in value if t]
    return [t for t in str(value or "").split(";") if t]


def unsupported_variants(types):
    """A2: new Clinical Trial / Research Support variants not on the closed list."""
    return sorted(t for t in types if t.startswith(VARIANT_PREFIXES)
                  and t not in KEEP_NOT_USED_TYPES and t not in CLASS_BEARING_EXCEPTIONS)


def classify(types):
    """Return (reason_code, clause) or None for one record's verbatim source types."""
    types = set(types)
    if STAGE0_E7_TYPE in types:
        return "E7", "a"
    if types & STAGE0_E5_TYPES and types <= (STAGE0_E5_TYPES | KEEP_NOT_USED_TYPES):
        return "E5", "b"
    return None


def in_d044_scope(record):
    return bool(set(split_types(record.get("query_ids"))) & D044_QUERY_IDS)


def valid_run_date(value):
    """A4 input check: a real calendar date written YYYY-MM-DD."""
    if not (isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)):
        return False
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def check_types(records, member_union_types):
    """Shared checked guards (also used by the pilot sampler). Every record needs a valid, unique
    paper_id. For D-044 in-scope records: A2 stops on an unsupported Clinical Trial / Research
    Support variant; A1 stops when the Stage-0 types disagree with the union of member types (or
    the union is missing). Out-of-scope records are never classified, so they are not type-checked.
    Raises Stage0Error; returns nothing."""
    ids = [r.get("paper_id") for r in records]
    if len(ids) != len(set(ids)):
        raise Stage0Error("duplicate paper_id in input")
    variants, disagreements, missing = {}, [], []
    for r in records:
        pid = r.get("paper_id") or ""
        if not _valid_id(pid):
            raise Stage0Error(f"invalid paper_id {pid!r}")
        if not in_d044_scope(r):
            continue
        types = split_types(r.get("source_publication_types"))
        bad = unsupported_variants(types)
        if bad:
            variants[pid] = bad
        if pid not in member_union_types:
            missing.append(pid)
            continue
        union = set(split_types(member_union_types[pid]))
        if (set(types) & STAGE0_RELEVANT) != (union & STAGE0_RELEVANT):
            disagreements.append(pid)
    if variants:
        raise Stage0Error(f"unsupported publication-type variants (stop and report): {variants}")
    if missing:
        raise Stage0Error(f"member-type union missing (A1 guard): {missing}")
    if disagreements:
        raise Stage0Error(f"Stage-0 types disagree with the member union (A1 guard): {disagreements}")


def checked_classify(record):
    """classify() for a record that has passed check_types()."""
    return classify(split_types(record.get("source_publication_types")))


def generate_rows(records, member_union_types, run_date, criteria_version, existing_rows=()):
    """Build Stage-0 rows (no file I/O).

    records: inventory rows with paper_id, query_ids, source_publication_types.
    member_union_types: {paper_id: union of member source records' types} for the A1 guard.
    existing_rows: rows already in screening/decisions.csv (append-only; never edited).
    Returns (rows, report). Raises Stage0Error on any stop-and-report condition."""
    if not pr.CRITERIA_VERSION_FORMAT.fullmatch(criteria_version or ""):
        raise Stage0Error("a frozen criteria_version is required")
    if not valid_run_date(run_date):
        raise Stage0Error(f"run_date {run_date!r} is not a real calendar date (YYYY-MM-DD)")
    check_types(records, member_union_types)
    done = {}
    for e in existing_rows:
        if e.get("screener") == pr.STAGE0_SCREENER:
            done.setdefault(e.get("paper_id"), set()).add(e.get("criteria_version", ""))
    rows, report = [], {"in_scope": 0, "E5": 0, "E7": 0, "skipped_existing": [],
                        "existing_other_version": [], "not_stage0": 0}
    for r in sorted(records, key=lambda x: int(x["paper_id"][1:])):
        if not in_d044_scope(r):
            continue
        report["in_scope"] += 1
        types = split_types(r.get("source_publication_types"))
        hit = checked_classify(r)
        if hit is None:
            report["not_stage0"] += 1
            continue
        code, clause = hit
        pid = r["paper_id"]
        if pid in done:
            key = "skipped_existing" if criteria_version in done[pid] else "existing_other_version"
            report[key].append(pid)
            continue
        rows.append({"paper_id": pid, "stage": STAGE, "decision": "exclude", "reason_code": code,
                     "screener": pr.STAGE0_SCREENER, "date": run_date,
                     "justification": JUSTIFICATION.format(clause=clause, types=";".join(types), code=code),
                     "criteria_version": criteria_version})
        report[code] += 1
    return rows, report


def _valid_id(pid):
    return bool(re.fullmatch(r"P\d{4,}", pid))


def utc_run_date():
    """A4: the generator's run date in UTC."""
    return dt.datetime.now(dt.timezone.utc).date().isoformat()


def sha256_of(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_member_union(lit):
    """Union of member source records' publication types per paper_id, plus input SHA-256s."""
    rec_dir = Path(lit) / "records"
    pub_path, src_path = rec_dir / "publications.jsonl", rec_dir / "source_records.jsonl"
    sr = {}
    with open(src_path, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            sr[r["source_record_id"]] = r
    union = {}
    with open(pub_path, encoding="utf-8") as f:
        for line in f:
            p = json.loads(line)
            members = []
            for e in p["search_provenance"]:
                if e["source_record_id"] not in sr:
                    raise Stage0Error(f"{p['paper_id']}: source record {e['source_record_id']} not found")
                members.append(sr[e["source_record_id"]])
            union[p["paper_id"]] = sorted({t for m in members for t in (m.get("publication_types") or [])})
    return union, {"publications_jsonl_sha256": sha256_of(pub_path),
                   "source_records_jsonl_sha256": sha256_of(src_path)}


def load_inventory(lit, expected_sha256):
    inv_path = Path(lit) / "paper_inventory.json"
    if sha256_of(inv_path) != expected_sha256:
        raise SystemExit("refused: inventory SHA-256 does not match the expected value")
    inv = json.loads(inv_path.read_text(encoding="utf-8"))
    return inv if isinstance(inv, list) else next(v for v in inv.values() if isinstance(v, list))


def _validate_candidate(lit, candidate):
    """Validate a candidate decisions file before it replaces the real one."""
    return pr.load_screening_decisions(lit, path=candidate)


def write_rows_atomically(lit, rows):
    """Append rows to screening/decisions.csv atomically: the original bytes plus the new rows are
    written to a temporary file in the same directory, validated, and only then moved over the
    original (os.replace). On any failure the original file is left unchanged."""
    path = Path(lit) / "screening" / "decisions.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    original = path.read_bytes() if path.exists() else b""
    if original:
        header = next(csv.reader(original.decode("utf-8").splitlines()))
        if "criteria_version" not in header:
            raise SystemExit("refused: existing decisions.csv has no criteria_version column")
        cols = header
    else:
        cols = pr.SCREENING_REQUIRED + ["criteria_version"]
    fd, tmp = tempfile.mkstemp(prefix=".decisions.", suffix=".csv.tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            if original:
                f.write(original.decode("utf-8"))
                if not original.endswith(b"\n"):
                    f.write("\n")
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="raise", restval="")
            if not original:
                w.writeheader()
            w.writerows(rows)
        _validate_candidate(lit, tmp)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lit-dir", required=True)
    ap.add_argument("--authorization", required=True, help="DECISION_LOG ID recording the D-074 (f) authorisation")
    ap.add_argument("--expected-inventory-sha256", required=True)
    ap.add_argument("--criteria-version", required=True)
    ap.add_argument("--write", action="store_true", help="append rows (default: dry run)")
    a = ap.parse_args(argv)
    lit = Path(a.lit_dir)
    try:
        auth = pr.verify_run_authorisation(lit, a.authorization, "D-074 (f)")
    except pr.RunAuthorisationError as e:
        raise SystemExit(str(e)) from None
    frozen = pr.load_criteria_registry(lit)
    if frozen is None or a.criteria_version not in frozen:
        raise SystemExit("refused: criteria_version is not a registered frozen version")
    records = load_inventory(lit, a.expected_inventory_sha256)
    union, input_hashes = load_member_union(lit)
    existing = pr.load_screening_decisions(lit)
    rows, report = generate_rows(records, union, utc_run_date(), a.criteria_version, existing)
    report.update({"inventory_sha256": a.expected_inventory_sha256, **input_hashes, "authorization": auth,
                   "criteria_version": a.criteria_version, "new_rows": len(rows), "written": False})
    if a.write and rows:
        write_rows_atomically(lit, rows)
        report["written"] = True
    print(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
