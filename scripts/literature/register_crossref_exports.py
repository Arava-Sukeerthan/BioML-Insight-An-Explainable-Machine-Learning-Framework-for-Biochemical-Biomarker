"""Register researcher-downloaded Crossref exports as D-064 second-source evidence (Q-099 workflow, step 3).

Status: PROPOSAL; running it with --write needs the researcher's approval of Q-098 and Q-099 and an
explicit authorisation reference. Without --write it only reports what it would register.

Order (each step must pass; nothing is registered if any export in the package is rejected):
  1. crossref_export_check.check_package (body hash, URL, DOI, headers, UTC time, duplicates, inventory
     DOI), run against the inventory;
  2. each body and header file must already be in <lit>/raw_exports/ (git-ignored; backed up off-device
     under D-010) and must not already be registered (raw files are immutable);
  3. the year rule must be decided (pubrecords.CROSSREF_YEAR_FIELDS is not None, Q-098), so that the
     intake check also applies the year parsing;
  4. each body is registered with the existing pubrecords.register_raw under query ID
     VERIFY-CR-<paper_id>, route crossref_works, source crossref, with the researcher-export provenance
     in endpoint_or_tool, request_json and notes (header file name and SHA-256, exporter, tool).
The header file itself is not a manifest row (it is not a search or verification response); its
SHA-256 is recorded in the request of its body row. Attachment to publications, verification status
and the inventory change only through an authorised rebuild (pubrecords.build), never here.

Usage: python3 -I scripts/literature/register_crossref_exports.py --lit-dir research/literature \
           --package research/literature/raw_exports --authorization D-nnn [--write]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import crossref_export_check as X  # noqa: E402
import pubrecords as pr  # noqa: E402


class RegistrationError(ValueError):
    pass


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def plan(lit_dir, package_dir, authorization, now=None):
    lit_dir, package_dir = Path(lit_dir), Path(package_dir)
    if not (authorization or "").strip():
        raise RegistrationError("an authorisation reference is required")
    if pr.CROSSREF_YEAR_FIELDS is None:
        raise RegistrationError("the Crossref year rule (Q-098) is not decided; nothing is registered")
    raw = (lit_dir / "raw_exports").resolve()
    if package_dir.resolve() != raw:
        raise RegistrationError(f"exports must be placed in {raw} (git-ignored) before registration")
    report = X.check_package(package_dir, lit_dir / "paper_inventory.json", now=now)
    if report["status"] != "accepted":
        raise RegistrationError("export check failed: " + json.dumps(
            [r for r in report.get("rows", []) if r["status"] != "accepted"] or report.get("reason")))
    registered = {r["raw_file"] for r in pr.read_manifest(lit_dir)}
    with open(package_dir / "provenance.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        for name in (r["file"], r["headers_file"]):
            if name in registered:
                raise RegistrationError(f"{name} is already registered (raw files are immutable)")
        doi = pr.normalize_doi(r["doi"])
        out.append({
            "raw_file": r["file"], "query_id": pr.VERIFY_PREFIX + r["paper_id"], "source": "crossref",
            "route": pr.CROSSREF_ROUTE,
            "endpoint_or_tool": f"researcher export ({r['tool']}): {r['url']}",
            "request": {"doi": doi, "paper_id": r["paper_id"], "exported_by": r["exported_by"],
                        "headers_file": r["headers_file"], "headers_sha256": _sha(package_dir / r["headers_file"])},
            "retrieved_at": r["retrieved_at_utc"],
            "notes": f"researcher export (Q-099); authorisation {authorization}; headers {r['headers_file']}",
        })
    return out


def register(lit_dir, entries):
    rows = []
    for e in entries:
        rows.append(pr.register_raw(lit_dir, e["raw_file"], e["query_id"], e["source"], e["route"],
                                    e["endpoint_or_tool"], e["request"], e["retrieved_at"], 1, False,
                                    notes=e["notes"]))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lit-dir", required=True)
    ap.add_argument("--package", required=True)
    ap.add_argument("--authorization", required=True)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    try:
        entries = plan(a.lit_dir, a.package, a.authorization)
    except (RegistrationError, ValueError) as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    if a.write:
        register(a.lit_dir, entries)
    print(json.dumps({"would_register" if not a.write else "registered": [e["raw_file"] for e in entries]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
