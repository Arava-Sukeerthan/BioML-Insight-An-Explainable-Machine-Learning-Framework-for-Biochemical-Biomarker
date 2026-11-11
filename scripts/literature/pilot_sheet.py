#!/usr/bin/env python3
"""Blinded researcher pilot sheet (Phase 1 implementation; researcher authorisation 2026-11-01).

The researcher's sheet shows title, abstract, year, venue and types, and no assistant decision
(protocol v0.2 §7; v0.1 §7 names `screening/pilot_sheet_researcher.csv`, decision D2). Approved
Phase 1 defaults: D1 `types` = verbatim source publication types; D3 the sheet is written only to a
path that Git ignores, because it contains abstracts and abstracts never enter committed files
(D-010; protocol v0.2 §5 item 7); D5 the sheet is built from this allow-list only:

    paper_id, title, abstract, abstract_status, year, venue, types

`abstract_status` uses only the D-068 (8) and D-079 labels; it is left empty when an abstract is
present and is never inferred: a record without an abstract needs a supplied status. No assistant
decision, exclusion reason, RQ tag, tier, descriptor, retrieval theme, stratum or verification field
can appear.

Generating the real sheet needs an authorised pilot sample (D-077 (6)) and an ignored output path
(the targeted .gitignore rule is deferred, decision D4). The command-line entry point refuses
otherwise. Researcher screening responses are recorded separately in pilot_decisions_researcher.csv
(protocol v0.2 §7); the sheet carries exactly the seven columns above and no response column.

Phase 1 corrections (researcher authorisation 2026-11-11): the run authorisation is verified
against DECISION_LOG.md; before a sheet is built, the pilot sample, its provenance sidecar and the
current inventory must agree.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pubrecords as pr  # noqa: E402

ALLOWED_COLUMNS = ["paper_id", "title", "abstract", "abstract_status", "year", "venue", "types"]   # D5
ABSTRACT_STATUSES = frozenset({"not retrieved", "unavailable", "unavailable — PubMed"})          # D-068 (8); D-079
DEFAULT_SHEET = "screening/pilot_sheet_researcher.csv"                                         # D2
_PLACEHOLDER = re.compile(r"^\s*\[?\s*abstract not available\s*\]?\.?\s*$", re.I)


class PilotSheetError(ValueError):
    """Stop condition; nothing is written."""


def is_missing_abstract(text):
    """D-068 (8): empty, absent or a source placeholder such as "[Abstract not available]"."""
    return not (text or "").strip() or bool(_PLACEHOLDER.match(text))


def build_rows(sample_ids, publications, abstract_status=None):
    """Return sheet rows (allow-listed columns only), ordered by paper_id.

    sample_ids: the authorised sample's paper_ids. publications: {paper_id: publication record}
    with title, abstract, year, journal, publication_types. abstract_status: {paper_id: label} for
    records without an abstract."""
    abstract_status = abstract_status or {}
    if len(sample_ids) != len(set(sample_ids)):
        raise PilotSheetError("duplicate paper_id in the sample")
    missing = [p for p in sample_ids if p not in publications]
    if missing:
        raise PilotSheetError(f"sample records not found in the publications: {missing}")
    rows = []
    for pid in sorted(sample_ids, key=lambda p: int(p[1:])):
        pub = publications[pid]
        abstract = pub.get("abstract") or ""
        status = abstract_status.get(pid, "")
        if status and status not in ABSTRACT_STATUSES:
            raise PilotSheetError(f"{pid}: abstract status {status!r} is not a D-068 (8) / D-079 label")
        if is_missing_abstract(abstract):
            if not status:
                raise PilotSheetError(f"{pid}: no abstract and no recorded status (not inferred)")
            abstract = ""
        elif status:
            raise PilotSheetError(f"{pid}: status {status!r} given for a record that has an abstract")
        types = pub.get("publication_types") or []
        rows.append({"paper_id": pid, "title": pub.get("title") or "", "abstract": abstract,
                     "abstract_status": status, "year": "" if pub.get("year") in (None, "") else str(pub["year"]),
                     "venue": pub.get("journal") or "",
                     "types": ";".join(types) if isinstance(types, list) else str(types)})
    check_row_set(rows, sample_ids)
    return rows


def check_columns(header):
    """D5: the header must equal the allow-list exactly (no extra, missing or reordered column)."""
    if list(header) != ALLOWED_COLUMNS:
        raise PilotSheetError(f"sheet columns {list(header)} differ from the allow-list {ALLOWED_COLUMNS}")


def check_row_set(rows, sample_ids):
    ids = [r["paper_id"] for r in rows]
    if len(ids) != len(set(ids)) or set(ids) != set(sample_ids):
        raise PilotSheetError("sheet rows do not equal the authorised sample")
    for r in rows:
        check_columns(r.keys())


def path_is_git_ignored(path):
    """D3: True only if Git reports the path as ignored and it is not tracked; any error -> False."""
    path = Path(path).resolve()
    git_dir = path.parent
    while not git_dir.exists():
        git_dir = git_dir.parent
    try:
        ignored = subprocess.run(["git", "-C", str(git_dir), "check-ignore", "-q", str(path)],
                                 capture_output=True).returncode == 0
        tracked = subprocess.run(["git", "-C", str(git_dir), "ls-files", "--error-unmatch", str(path)],
                                 capture_output=True).returncode == 0
    except OSError:
        return False
    return ignored and not tracked


def verify_sample_provenance(sample_rows, sidecar, inventory_sha256, authorization):
    """Correction 5: the pilot sample and its provenance sidecar must agree with each other, with
    the current inventory and with the sheet's authorisation. Raises PilotSheetError otherwise."""
    if not isinstance(sidecar, dict):
        raise PilotSheetError("provenance sidecar is not a JSON object")
    ids = [r.get("paper_id") for r in sample_rows]
    problems = []
    if not ids or len(ids) != len(set(ids)):
        problems.append("sample is empty or has duplicate paper_ids")
    if sidecar.get("sample_size") != len(ids):
        problems.append(f"sample_size {sidecar.get('sample_size')!r} != {len(ids)} rows")
    for key, side_key in (("seed", "seed"), ("inventory_sha256", "inventory_sha256"),
                          ("sampling_script", "sampling_script")):
        values = {str(r.get(key)) for r in sample_rows}
        if values != {str(sidecar.get(side_key))}:
            problems.append(f"{key} differs between sample and sidecar")
    counts = {}
    for r in sample_rows:
        counts[r.get("stratum")] = counts.get(r.get("stratum"), 0) + 1
    allocation = {s: k for s, k in (sidecar.get("allocation") or {}).items() if k}
    if counts != allocation:
        problems.append("stratum counts differ from the sidecar allocation")
    if sidecar.get("inventory_sha256") != inventory_sha256:
        problems.append("the inventory changed since the draw")
    if sidecar.get("authorization") != authorization:
        problems.append("the sheet authorisation differs from the draw authorisation")
    if problems:
        raise PilotSheetError("refused: " + "; ".join(problems))


def write_sheet(rows, out_path, sample_ids, authorization, lit_dir=None, decision_log=None):
    if lit_dir is None and decision_log is None:
        raise PilotSheetError("refused: no decision log to verify the D-077 (6) authorisation")
    try:
        pr.verify_run_authorisation(lit_dir or ".", authorization, "D-077 (6)", decision_log=decision_log)
    except pr.RunAuthorisationError as e:
        raise PilotSheetError(str(e)) from None
    if not path_is_git_ignored(out_path):
        raise PilotSheetError(f"refused: {out_path} is not ignored by Git (abstracts must not enter tracked files)")
    check_row_set(rows, sample_ids)
    out = Path(out_path)
    if out.exists():
        raise PilotSheetError(f"refused: {out} already exists")
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ALLOWED_COLUMNS, extrasaction="raise")
        w.writeheader()
        w.writerows(rows)
    with open(out, newline="", encoding="utf-8") as f:
        check_columns(next(csv.reader(f)))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lit-dir", required=True)
    ap.add_argument("--authorization", required=True, help="DECISION_LOG ID recording the D-077 (6) authorisation")
    ap.add_argument("--abstract-status", help="JSON file {paper_id: label} for records without an abstract")
    ap.add_argument("--out", default=None, help=f"default: <lit-dir>/{DEFAULT_SHEET}")
    a = ap.parse_args(argv)
    lit = Path(a.lit_dir)
    try:
        auth = pr.verify_run_authorisation(lit, a.authorization, "D-077 (6)")
    except pr.RunAuthorisationError as e:
        raise SystemExit(str(e)) from None
    sample_path = lit / "screening" / "pilot_sample.csv"
    side_path = sample_path.with_suffix(".provenance.json")
    if not sample_path.exists() or not side_path.exists():
        raise SystemExit("refused: no authorised pilot sample with its provenance sidecar")
    with open(sample_path, newline="") as f:
        sample_rows = list(csv.DictReader(f))
    try:
        sidecar = json.loads(side_path.read_text(encoding="utf-8"))
        inv_sha = hashlib.sha256((lit / "paper_inventory.json").read_bytes()).hexdigest()
        verify_sample_provenance(sample_rows, sidecar, inv_sha, auth)
    except (ValueError, OSError) as e:
        raise SystemExit(str(e)) from None
    sample_ids = [r["paper_id"] for r in sample_rows]
    wanted = set(sample_ids)
    pubs = {}
    with open(lit / "records" / "publications.jsonl", encoding="utf-8") as f:
        for line in f:
            p = json.loads(line)
            if p["paper_id"] in wanted:
                pubs[p["paper_id"]] = p
    status = json.loads(Path(a.abstract_status).read_text(encoding="utf-8")) if a.abstract_status else {}
    try:
        rows = build_rows(sample_ids, pubs, status)
        out = write_sheet(rows, Path(a.out) if a.out else lit / DEFAULT_SHEET, sample_ids, auth, lit_dir=lit)
    except PilotSheetError as e:
        raise SystemExit(str(e)) from None
    print(f"wrote {out} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
