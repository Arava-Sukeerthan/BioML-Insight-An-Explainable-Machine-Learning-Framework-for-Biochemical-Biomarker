"""Run a stored PubMed query through the official NCBI E-utilities API and save raw responses.

Status (2026-10-14): eutils.ncbi.nlm.nih.gov is BLOCKED by this environment's network policy,
so this client has only been tested against a fake transport (tests/literature). Until the host
is allow-listed, use the PubMed connector route described in collection_workflow.md.

Access conditions respected (NCBI E-utilities usage guidelines):
  * at most 3 requests/second without an API key, 10/second with NCBI_API_KEY;
  * `tool` identifies this project; `email` is sent only if NCBI_EMAIL is set by the researcher;
  * large result sets are fetched in batches (esearch retmax <= 10000; efetch via POST, 200 IDs);
  * no scraping of web pages: only documented API endpoints.

For each run it writes, under research/literature/raw_exports/:
  <QUERY_ID>_<YYYY-MM-DD>_esearch_<k>.json   raw esearch JSON (one per 10k-ID page)
  <QUERY_ID>_<YYYY-MM-DD>_efetch_<k>.xml     raw efetch XML (one per 200-ID batch)
and registers every file in raw_exports/MANIFEST.csv via pubrecords.register_raw.

Usage:
  python3 -I scripts/literature/fetch_pubmed_eutils.py Q-PM-01 [--run-date 2026-10-16] [--dry-run]
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pubrecords  # noqa: E402

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
TOOL = "bioml-insight-litreview"
ESEARCH_PAGE = 10000
EFETCH_BATCH = 200


class Transport:
    """Real HTTP transport. Tests substitute an object with the same `request` method."""

    def __init__(self, api_key=None):
        self.min_interval = 0.1 if api_key else 0.34
        self._last = 0.0

    def request(self, url, data=None):
        wait = self.min_interval - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(url, data=data, headers={"User-Agent": TOOL})
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read()
        self._last = time.monotonic()
        return body


def common_params():
    p = {"tool": TOOL}
    if os.environ.get("NCBI_EMAIL"):
        p["email"] = os.environ["NCBI_EMAIL"]
    if os.environ.get("NCBI_API_KEY"):
        p["api_key"] = os.environ["NCBI_API_KEY"]
    return p


def load_query(lit_dir, query_id):
    with open(Path(lit_dir) / "search_queries.csv", newline="") as f:
        for r in csv.DictReader(f):
            if r["query_id"] == query_id:
                if r["source"] != "pubmed" or r["row_type"] != "planned":
                    raise ValueError(f"{query_id} is not a planned PubMed query")
                return r["query_string"]
    raise KeyError(query_id)


def run(query_id, run_date, lit_dir="research/literature", transport=None, dry_run=False):
    lit_dir = Path(lit_dir)
    term = load_query(lit_dir, query_id).replace("{RUN_DATE}", run_date.replace("-", "/"))
    transport = transport or Transport(os.environ.get("NCBI_API_KEY"))
    params = common_params()
    if dry_run:
        return {"query_id": query_id, "term": term, "params": {k: v for k, v in params.items() if k != "api_key"}}
    raw_dir = lit_dir / "raw_exports"
    raw_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{query_id}_{run_date}"
    if any(raw_dir.glob(stem + "_*")):
        raise FileExistsError(f"raw exports for {stem} already exist; raw files are immutable")

    pmids, total, page = [], None, 0
    while total is None or len(pmids) < total:
        q = {**params, "db": "pubmed", "term": term, "retmode": "json",
             "retstart": str(len(pmids)), "retmax": str(ESEARCH_PAGE)}
        ts = pubrecords.utc_now()
        body = transport.request(BASE + "esearch.fcgi", urllib.parse.urlencode(q).encode())
        res = json.loads(body)["esearchresult"]
        total = int(res["count"])
        if total > ESEARCH_PAGE:
            raise ValueError(f"{query_id}: {total} hits; PubMed esearch cannot page beyond "
                             f"{ESEARCH_PAGE} records. Split the query by date range.")
        ids = res.get("idlist", [])
        fname = f"{stem}_esearch_{page:02d}.json"
        (raw_dir / fname).write_bytes(body)
        pubrecords.register_raw(lit_dir, fname, query_id, "pubmed", "eutils_esearch",
                                BASE + "esearch.fcgi",
                                {k: v for k, v in q.items() if k not in ("api_key", "email")},
                                ts, len(ids), transcribed=False,
                                notes=f"reported count={total}")
        if not ids:
            break
        pmids.extend(ids)
        page += 1

    for k in range(0, len(pmids), EFETCH_BATCH):
        batch = pmids[k:k + EFETCH_BATCH]
        q = {**params, "db": "pubmed", "id": ",".join(batch), "retmode": "xml"}
        ts = pubrecords.utc_now()
        body = transport.request(BASE + "efetch.fcgi", urllib.parse.urlencode(q).encode())
        fname = f"{stem}_efetch_{k // EFETCH_BATCH:03d}.xml"
        (raw_dir / fname).write_bytes(body)
        pubrecords.register_raw(lit_dir, fname, query_id, "pubmed", "eutils_efetch",
                                BASE + "efetch.fcgi",
                                {"db": "pubmed", "retmode": "xml", "n_ids": len(batch),
                                 "first_id": batch[0], "last_id": batch[-1]},
                                ts, len(batch), transcribed=False)
    return {"query_id": query_id, "term": term, "reported_total": total, "retrieved": len(pmids)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query_id")
    ap.add_argument("--run-date", default=dt.date.today().isoformat())
    ap.add_argument("--lit-dir", default="research/literature")
    ap.add_argument("--dry-run", action="store_true", help="print the substituted query; no network")
    a = ap.parse_args(argv)
    print(json.dumps(run(a.query_id, a.run_date, a.lit_dir, dry_run=a.dry_run), indent=2))


if __name__ == "__main__":
    main()
