"""Crossref /works/{DOI} lookups for an authorised verification pilot (WP2; D-064 second source).

Status: written and tested only against a fake transport (tests/literature). It has never contacted
Crossref. api.crossref.org was blocked by this environment's network policy when last checked
(2026-10-29, research/setup/environment_assessment.md). Running it for real needs the researcher's
authorisation and an allowed host.

What it does, for each paper ID in a pilot file (CSV with a `paper_id` column):
  * takes the DOI from research/literature/paper_inventory.json and normalises it with
    pubrecords.normalize_doi; the whole run is refused before any request if a paper ID is unknown,
    listed twice, has no or an invalid DOI, or shares its DOI with another inventory record;
  * requests https://api.crossref.org/works/{DOI} once, retrying (bounded, with backoff) only on HTTP
    429, HTTP 5xx and transport errors such as timeouts;
  * saves a successful, well-formed response byte for byte as raw_exports/CR_<run-date>_<nnn>.json
    (git-ignored) and registers it in raw_exports/MANIFEST.csv with its SHA-256, endpoint, request
    (DOI, paper ID) and retrieval time, under query ID "VERIFY-CR-<paper_id>";
  * writes nothing (no raw file, no manifest row) for a failed request or a malformed response:
    non-JSON body, no `message` object, or a returned DOI that differs from the requested DOI.

It never changes a verification status: statuses change only through an authorised build, which
attaches these records as second-source evidence to the listed paper IDs (pubrecords.build).
No network access unless --execute is given.

Usage:
  python3 -I scripts/literature/fetch_crossref.py --pilot PILOT.csv --run-date 2026-11-01 [--execute]
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pubrecords  # noqa: E402

API = "https://api.crossref.org/works/"
USER_AGENT = "bioml-insight-literature-verification/0.1 (no contact address configured)"
RETRY_STATUS = frozenset({429}) | frozenset(range(500, 600))


class Transport:
    """Real HTTP transport. Tests substitute an object with the same `get` method.
    Returns (status, body); raises OSError (incl. timeouts) for transport failures."""

    def __init__(self, user_agent=USER_AGENT, timeout=60):
        self.user_agent, self.timeout = user_agent, timeout

    def get(self, url):
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read() if hasattr(e, "read") else b""


def load_pilot(path):
    with open(path, newline="") as f:
        return [(r.get("paper_id") or "").strip() for r in csv.DictReader(f)]


def plan(pilot_ids, inventory):
    """Returns (list of (paper_id, doi), problems). Any problem refuses the whole run."""
    by_pid = {r["paper_id"]: r for r in inventory}
    doi_owners = {}
    for r in inventory:
        d = pubrecords.normalize_doi(r.get("doi"))
        if d:
            doi_owners.setdefault(d, set()).add(r["paper_id"])
    out, problems, seen_pid, seen_doi = [], [], set(), set()
    for pid in pilot_ids:
        if not pid:
            problems.append("empty paper_id in pilot file")
            continue
        if pid in seen_pid:
            problems.append(f"{pid}: listed more than once")
            continue
        seen_pid.add(pid)
        rec = by_pid.get(pid)
        if rec is None:
            problems.append(f"{pid}: not in the inventory")
            continue
        raw = rec.get("doi")
        doi = pubrecords.normalize_doi(raw)
        if not raw:
            problems.append(f"{pid}: no DOI")
            continue
        if not doi:
            problems.append(f"{pid}: invalid DOI {raw!r}")
            continue
        if doi in seen_doi:
            problems.append(f"{pid}: DOI {doi} already requested for another pilot paper")
            continue
        if doi_owners.get(doi, set()) != {pid}:
            problems.append(f"{pid}: DOI {doi} is shared with {sorted(doi_owners[doi] - {pid})}")
            continue
        seen_doi.add(doi)
        out.append((pid, doi))
    return out, problems


def fetch(url, transport, sleep=time.sleep, attempts=3, backoff=2.0):
    """One logical request with bounded retries. Returns dict(status, body, attempts, error)."""
    last = {"status": None, "body": None, "attempts": 0, "error": None}
    for n in range(1, attempts + 1):
        last["attempts"] = n
        try:
            status, body = transport.get(url)
            last.update(status=status, body=body, error=None)
        except OSError as e:          # URLError, timeouts, connection resets
            last.update(status=None, body=None, error=f"{type(e).__name__}: {e}")
            status = None
        if status is not None and status not in RETRY_STATUS:
            return last
        if n < attempts:
            sleep(backoff ** n)
    return last


def check_response(body, requested_doi):
    """Returns the parsed document if well formed and for the requested DOI; raises ValueError."""
    doc = json.loads(body)
    message = doc.get("message") if isinstance(doc, dict) else None
    meta = pubrecords.parse_crossref_work(message)          # raises ValueError if malformed
    if meta["doi"] != requested_doi:
        raise ValueError(f"returned DOI {meta['doi']} differs from requested DOI {requested_doi}")
    return doc


def run(pilot_ids, run_date, lit_dir="research/literature", inventory=None, transport=None,
        sleep=time.sleep, pause=1.0, execute=False):
    lit_dir = Path(lit_dir)
    if inventory is None:
        with open(lit_dir / "paper_inventory.json") as f:
            inventory = json.load(f)
    requests, problems = plan(pilot_ids, inventory)
    report = {"run_date": run_date, "execute": execute, "planned": len(requests), "problems": problems,
              "results": []}
    if problems:
        report["refused"] = True
        return report
    raw_dir = lit_dir / "raw_exports"
    stem = f"CR_{run_date}_"
    if execute and any(raw_dir.glob(stem + "*")):
        raise FileExistsError(f"raw exports {stem}* already exist; raw files are immutable")
    transport = transport or Transport()
    saved = 0
    for k, (pid, doi) in enumerate(requests):
        url = API + urllib.parse.quote(doi, safe="/")
        if not execute:
            report["results"].append({"paper_id": pid, "doi": doi, "url": url, "outcome": "dry_run"})
            continue
        if k:
            sleep(pause)
        res = fetch(url, transport, sleep)
        entry = {"paper_id": pid, "doi": doi, "url": url, "attempts": res["attempts"], "http_status": res["status"]}
        if res["status"] != 200:
            entry["outcome"] = "failed"
            entry["error"] = res["error"] or f"HTTP {res['status']}"
            report["results"].append(entry)
            continue
        try:
            check_response(res["body"], doi)
        except ValueError as e:
            entry.update(outcome="malformed", error=str(e))
            report["results"].append(entry)
            continue
        ts = pubrecords.utc_now()
        name = f"{stem}{saved:03d}.json"
        raw_dir.mkdir(parents=True, exist_ok=True)
        (raw_dir / name).write_bytes(res["body"])
        pubrecords.register_raw(lit_dir, name, pubrecords.VERIFY_PREFIX + pid, "crossref",
                                pubrecords.CROSSREF_ROUTE, url, {"doi": doi, "paper_id": pid}, ts, 1,
                                transcribed=False, notes="Crossref verification lookup (D-064 second source)")
        saved += 1
        entry.update(outcome="saved", raw_file=name)
        report["results"].append(entry)
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pilot", required=True, help="CSV with a paper_id column (authorised pilot)")
    ap.add_argument("--run-date", required=True)
    ap.add_argument("--lit-dir", default="research/literature")
    ap.add_argument("--execute", action="store_true", help="contact Crossref (default: dry run)")
    a = ap.parse_args(argv)
    report = run(load_pilot(a.pilot), a.run_date, a.lit_dir, execute=a.execute)
    print(json.dumps(report, indent=2))
    return 1 if report.get("refused") else 0


if __name__ == "__main__":
    sys.exit(main())
