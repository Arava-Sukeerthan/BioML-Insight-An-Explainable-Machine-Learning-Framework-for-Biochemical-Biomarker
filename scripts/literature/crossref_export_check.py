"""Read-only checker for researcher-downloaded Crossref /works/{DOI} exports (proposal for Q-099).

Status: PROPOSAL. It supports the open question Q-099 (whether a researcher export counts as "recorded
retrieval" under D-064 (10)). It never registers, copies, moves or changes a file, the manifest, the
inventory or any record. Registration of accepted exports would still go through
pubrecords.register_raw under a separate, explicit authorisation.

An export package is one directory holding:
  * provenance.csv with columns PROVENANCE_COLS (one row per export);
  * for each row, the response body file (byte for byte as received) and a response-header file
    (e.g. from `curl -sS -D <name>.headers.txt -o <name>.json <url>`).

Checks per row (all must pass for status "accepted"):
  * paper_id has the inventory form P#### and DOI and paper_id are each listed once;
  * url is exactly https://api.crossref.org/works/<doi> for the normalised DOI;
  * retrieved_at_utc is an ISO 8601 timestamp with an explicit UTC offset, not in the future;
  * exported_by and tool are filled in;
  * the body file exists, its SHA-256 equals the recorded sha256;
  * the body is a well-formed Crossref work response (pubrecords.parse_crossref_work) and its DOI
    equals the requested DOI;
  * the header file exists, its status line reports HTTP 200 and it has a Date header;
  * optionally (--inventory), the paper's DOI in the inventory equals the requested DOI.
The year is not checked here: its rule is Q-098 (pending).

Usage: python3 -I scripts/literature/crossref_export_check.py EXPORT_DIR [--inventory paper_inventory.json]
Exit status 0 if every row is accepted, 1 otherwise. The JSON report goes to stdout.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pubrecords as pr  # noqa: E402

PROVENANCE_COLS = ("file", "headers_file", "doi", "paper_id", "url", "retrieved_at_utc", "tool",
                   "exported_by", "sha256")
API = "https://api.crossref.org/works/"


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _utc(value, now):
    try:
        t = dt.datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return "retrieved_at_utc is not ISO 8601"
    if t.tzinfo is None or t.utcoffset() != dt.timedelta(0):
        return "retrieved_at_utc has no explicit UTC offset"
    if t > now:
        return "retrieved_at_utc is in the future"
    return None


def _headers_problem(path):
    lines = Path(path).read_text(encoding="latin-1").splitlines()
    statuses = [ln for ln in lines if ln.startswith("HTTP/")]
    if not statuses:
        return "header file has no HTTP status line"
    final = statuses[-1].split()        # the last status line (after any proxy CONNECT or redirect)
    if len(final) < 2 or final[1] != "200":
        return f"final HTTP status is not 200 ({statuses[-1].strip()})"
    if not any(ln.lower().startswith("date:") for ln in lines):
        return "header file has no Date header"
    return None


def _inventory_dois(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    recs = data if isinstance(data, list) else data.get("records", data.get("publications", []))
    return {r.get("paper_id"): pr.normalize_doi(r.get("doi")) for r in recs}


def check_package(export_dir, inventory=None, now=None):
    export_dir = Path(export_dir)
    now = now or dt.datetime.now(dt.timezone.utc)
    prov = export_dir / "provenance.csv"
    if not prov.exists():
        return {"status": "refused", "reason": "provenance.csv missing", "rows": []}
    with open(prov, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != PROVENANCE_COLS:
            return {"status": "refused", "reason": f"provenance.csv columns must be {list(PROVENANCE_COLS)}",
                    "rows": []}
        rows = list(reader)
    if not rows:
        return {"status": "refused", "reason": "provenance.csv has no rows", "rows": []}
    inv = _inventory_dois(inventory) if inventory else None
    dois = [pr.normalize_doi(r["doi"]) for r in rows]
    pids = [r["paper_id"] for r in rows]
    out = []
    for r, doi in zip(rows, dois):
        problems = []
        if not re.fullmatch(r"P\d{4}", r["paper_id"] or ""):
            problems.append("paper_id is not of the form P####")
        if not doi:
            problems.append("DOI is missing or invalid")
        elif dois.count(doi) > 1:
            problems.append("DOI listed more than once")
        if pids.count(r["paper_id"]) > 1:
            problems.append("paper_id listed more than once")
        if doi and r["url"] != API + doi:
            problems.append("url is not the Crossref works URL of the normalised DOI")
        p = _utc(r["retrieved_at_utc"], now)
        if p:
            problems.append(p)
        for k in ("tool", "exported_by"):
            if not (r[k] or "").strip():
                problems.append(f"{k} is empty")
        body = export_dir / (r["file"] or "")
        if not r["file"] or not body.is_file():
            problems.append("body file missing")
        else:
            if _sha256(body) != (r["sha256"] or "").lower():
                problems.append("SHA-256 of the body differs from the recorded value")
            try:
                doc = json.loads(body.read_bytes().decode("utf-8"))
                meta = pr.parse_crossref_work(doc.get("message") if isinstance(doc, dict) else None)
                if doi and meta["doi"] != doi:
                    problems.append("DOI in the response differs from the requested DOI")
            except ValueError as e:
                problems.append(f"body is not a well-formed Crossref work response ({e})")
        hdr = export_dir / (r["headers_file"] or "")
        if not r["headers_file"] or not hdr.is_file():
            problems.append("header file missing")
        else:
            p = _headers_problem(hdr)
            if p:
                problems.append(p)
        if inv is not None:
            if r["paper_id"] not in inv:
                problems.append("paper_id not in the inventory")
            elif doi and inv[r["paper_id"]] != doi:
                problems.append("inventory DOI of this paper differs from the requested DOI")
        out.append({"file": r["file"], "paper_id": r["paper_id"], "doi": doi,
                    "status": "rejected" if problems else "accepted", "problems": problems})
    status = "accepted" if all(o["status"] == "accepted" for o in out) else "rejected"
    return {"status": status, "n": len(out), "n_accepted": sum(o["status"] == "accepted" for o in out),
            "rows": out, "note": "read-only check; nothing registered (Q-099 pending; year rule Q-098 pending)"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("export_dir")
    ap.add_argument("--inventory")
    a = ap.parse_args(argv)
    rep = check_package(a.export_dir, a.inventory)
    print(json.dumps(rep, indent=2, sort_keys=True))
    return 0 if rep["status"] == "accepted" else 1


if __name__ == "__main__":
    sys.exit(main())
