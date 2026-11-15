"""Crossref /works/{DOI} lookups for an authorised verification pilot (WP2; D-064 second source).

Status: written and tested only against a fake transport and injected failures (tests/literature).
It has never contacted Crossref. api.crossref.org was blocked by this environment's network policy
when last checked (2026-10-29, research/setup/environment_assessment.md). Running it for real needs
the researcher's authorisation and an allowed host.

What it does, for each paper ID in a pilot file (CSV with a `paper_id` column):
  * takes the DOI from research/literature/paper_inventory.json and normalises it with
    pubrecords.normalize_doi; the whole run is refused before any request if a paper ID is unknown,
    listed twice, has no or an invalid DOI, or shares its DOI with another inventory record;
  * the whole run is also refused before any request if raw_exports/MANIFEST.csv is damaged (an
    incomplete last line or a row with missing columns) or if a lock file shows that another run is
    active or an earlier run was interrupted;
  * skips a paper ID that already has a registered lookup (query ID VERIFY-CR-<paper_id>), so an
    interrupted run can be resumed by running it again;
  * requests https://api.crossref.org/works/{DOI}, retrying (bounded, with backoff) only on HTTP 429,
    HTTP 5xx and transport errors (OSError, including timeouts, and http.client.HTTPException);
  * saves a successful, well-formed response byte for byte as raw_exports/CR_<run-date>_<nnn>.json
    (git-ignored) and registers it in raw_exports/MANIFEST.csv with its SHA-256, endpoint, request
    (DOI, paper ID) and retrieval time, under query ID "VERIFY-CR-<paper_id>";
  * writes nothing (no raw file, no manifest row) for a failed request or a malformed response:
    non-JSON or truncated body, no `message` object, wrongly shaped fields, or a returned DOI that
    differs from the requested DOI.

Persistence and interruptions (what is and is not guaranteed):
  * the body is first written to CR_<run-date>_<nnn>.json.partial (exclusive create, flush, fsync),
    read back and compared by SHA-256, then hard-linked to its final name (never overwriting an
    existing file) and only then registered with one fsync'ed manifest append;
  * an existing file is never overwritten or deleted, except the .partial file this run created
    itself once its content is safely under the final name; new files take the next free number;
  * if a step fails, the run stops (report "aborted"), the report is still returned, and every
    unregistered CR_* or .partial file is listed under "orphans". Orphans are never registered or used
    by the build (the build reads only the manifest); they are left for the researcher to inspect;
  * not guaranteed: atomicity on filesystems without POSIX hard links or fsync semantics, and
    consistency after power loss beyond what fsync provides. A crash can leave an orphan file or a
    stale lock file; neither changes the manifest. The lock file is removed by hand after checking.

It never changes a verification status: statuses change only through an authorised build, which
attaches these records as second-source evidence to the listed paper IDs (pubrecords.build).
No network access unless --execute is given.

Usage:
  python3 -I scripts/literature/fetch_crossref.py --pilot PILOT.csv --run-date 2026-11-01 [--execute]
Exit status: 0 when every pilot paper ends saved, skipped as already registered, or dry-run;
1 otherwise (refused, aborted, failed or malformed responses). Every report has a "status":
"refused", "aborted" or "finished" ("finished" = every planned paper processed, whatever its outcome).
If the run does not finish because an exception escapes (for example an unreadable pilot file or
inventory, or Ctrl-C / KeyboardInterrupt), a report with "status": "incomplete" and "completed": false
is printed first, with the stage reached and any partial results, and then the original exception
is re-raised unchanged, so its traceback and Python's exit status follow. Not covered: SIGTERM,
SIGKILL, power loss, and a second Ctrl-C while the first is being handled (no report is printed).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import http.client
import json
import os
import re
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
TRANSPORT_ERRORS = (OSError, http.client.HTTPException)
LOCK_NAME = ".fetch_crossref.lock"
OK_OUTCOMES = frozenset({"saved", "already_registered", "dry_run"})


class Transport:
    """Real HTTP transport. Tests substitute an object with the same `get` method.
    Returns (status, body); raises OSError (incl. timeouts) or http.client.HTTPException for
    transport failures."""

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


def manifest_problems(lit_dir):
    """Problems that make raw_exports/MANIFEST.csv unsafe to append to (nothing is repaired here)."""
    mp = Path(lit_dir) / "raw_exports" / "MANIFEST.csv"
    if not mp.exists():
        return []
    data = mp.read_bytes()
    if not data:
        return []
    problems = []
    if not data.endswith(b"\n"):
        problems.append("MANIFEST.csv: last line is incomplete (interrupted write?)")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return problems + ["MANIFEST.csv: not valid UTF-8"]
    reader = csv.DictReader(text.splitlines())
    if reader.fieldnames != pubrecords.MANIFEST_COLS:
        problems.append("MANIFEST.csv: unexpected header")
        return problems
    for n, row in enumerate(reader, start=2):
        if None in row or any(row.get(c) is None for c in pubrecords.MANIFEST_COLS):
            problems.append(f"MANIFEST.csv line {n}: wrong number of columns")
    return problems


def orphans(lit_dir):
    """Unregistered Crossref files (CR_* raw files or .partial files) in raw_exports. Never deleted."""
    raw_dir = Path(lit_dir) / "raw_exports"
    if not raw_dir.exists():
        return []
    registered = {r["raw_file"] for r in pubrecords.read_manifest(lit_dir)}
    return sorted(p.name for p in raw_dir.glob("CR_*") if p.name not in registered)


def _next_index(raw_dir, stem):
    pat = re.compile(re.escape(stem) + r"(\d{3,})\.json(\.partial)?$")
    used = [int(m.group(1)) for p in raw_dir.glob(stem + "*") if (m := pat.match(p.name))]
    return max(used, default=-1) + 1


def save_raw(raw_dir, name, body, warnings=None):
    """Write body under raw_dir/name without ever overwriting: .partial file (exclusive create, fsync),
    SHA-256 read-back check, hard link to the final name, then removal of this run's own .partial.
    The final directory fsync is best effort: if it fails, the file is kept and, when a `warnings`
    list is given, a warning is added to it (the directory entry may then not be durable yet)."""
    final, partial = raw_dir / name, raw_dir / (name + ".partial")
    with open(partial, "xb") as f:
        f.write(body)
        f.flush()
        os.fsync(f.fileno())
    if hashlib.sha256(partial.read_bytes()).hexdigest() != hashlib.sha256(body).hexdigest():
        raise OSError(f"{partial.name}: read-back does not match the response body")
    os.link(partial, final)          # FileExistsError if the final name exists: never overwrite
    os.unlink(partial)
    try:
        dfd = os.open(raw_dir, os.O_RDONLY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    except OSError as e:              # directory fsync is not supported everywhere; best effort
        if warnings is not None:
            warnings.append(f"{name}: directory fsync failed ({type(e).__name__}: {e}); "
                            "the file is saved but its directory entry may not be durable yet")
    return final


def fetch(url, transport, sleep=time.sleep, attempts=3, backoff=2.0):
    """One logical request with bounded retries. Returns dict(status, body, attempts, error)."""
    last = {"status": None, "body": None, "attempts": 0, "error": None}
    for n in range(1, attempts + 1):
        last["attempts"] = n
        try:
            status, body = transport.get(url)
            last.update(status=status, body=body, error=None)
        except TRANSPORT_ERRORS as e:   # URLError, timeouts, resets, IncompleteRead, RemoteDisconnected
            last.update(status=None, body=None, error=f"{type(e).__name__}: {e}")
            status = None
        if status is not None and status not in RETRY_STATUS:
            return last
        if n < attempts:
            sleep(backoff ** n)
    return last


def check_response(body, requested_doi):
    """Returns the parsed document if well formed and for the requested DOI; raises ValueError."""
    if not isinstance(body, (bytes, bytearray)):
        raise ValueError(f"response body is {type(body).__name__}, not bytes")
    doc = json.loads(body)
    message = doc.get("message") if isinstance(doc, dict) else None
    meta = pubrecords.parse_crossref_work(message)          # raises ValueError if malformed
    if meta["doi"] != requested_doi:
        raise ValueError(f"returned DOI {meta['doi']} differs from requested DOI {requested_doi}")
    return doc


def run(pilot_ids, run_date, lit_dir="research/literature", inventory=None, transport=None,
        sleep=time.sleep, pause=1.0, execute=False, progress=None):
    """Plan, fetch and register the pilot lookups; returns the run report.
    progress: optional dict, updated in place with the current "stage" ("planning", "fetching",
    "finishing", "done") and, once it exists, the partial "report" (the same object that is returned),
    so that a caller can still describe the run if an exception (including KeyboardInterrupt)
    escapes. Every returned report has "status": "refused", "aborted" or "finished"; "finished" means
    every planned paper was processed, not that every lookup succeeded (see "results")."""
    progress = {} if progress is None else progress
    progress["stage"] = "planning"
    lit_dir = Path(lit_dir)
    if inventory is None:
        with open(lit_dir / "paper_inventory.json") as f:
            inventory = json.load(f)
    requests, problems = plan(pilot_ids, inventory)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(run_date)):
        problems.append(f"run date {run_date!r} is not YYYY-MM-DD")
    problems += manifest_problems(lit_dir)
    raw_dir = lit_dir / "raw_exports"
    lock = raw_dir / LOCK_NAME
    if execute and lock.exists():
        problems.append(f"{LOCK_NAME} exists: another run is active or an earlier run was interrupted; "
                        "check the report and the orphans, then remove the lock file by hand")
    report = {"status": "incomplete", "run_date": run_date, "execute": execute, "planned": len(requests),
              "problems": problems, "results": [], "orphans_before": orphans(lit_dir)}
    progress["report"] = report
    if problems:
        report.update(status="refused", refused=True)
        progress["stage"] = "done"
        return report
    done = {r["query_id"] for r in pubrecords.read_manifest(lit_dir)}
    transport = transport or Transport()
    stem = f"CR_{run_date}_"
    requested = 0
    locked = False
    progress["stage"] = "fetching"
    try:
        if execute:
            raw_dir.mkdir(parents=True, exist_ok=True)
            try:
                fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:   # not ours: never removed by this run
                report.update(status="refused", refused=True,
                              problems=[f"{LOCK_NAME} appeared: another run is active"])
                return report
            locked = True             # from here on, `finally` removes the lock this run created
            try:
                os.write(fd, f"pid {os.getpid()} started {pubrecords.utc_now()}\n".encode())
            finally:
                os.close(fd)
        for pid, doi in requests:
            url = API + urllib.parse.quote(doi, safe="/")
            entry = {"paper_id": pid, "doi": doi, "url": url}
            if pubrecords.VERIFY_PREFIX + pid in done:
                entry["outcome"] = "already_registered"
                report["results"].append(entry)
                continue
            if not execute:
                entry["outcome"] = "dry_run"
                report["results"].append(entry)
                continue
            if requested:
                sleep(pause)
            requested += 1
            try:
                res = fetch(url, transport, sleep)
            except Exception as e:          # an unexpected transport failure: record it, go on
                entry.update(outcome="error", error=f"{type(e).__name__}: {e}")
                report["results"].append(entry)
                continue
            entry.update(attempts=res["attempts"], http_status=res["status"])
            if res["status"] != 200:
                entry["outcome"] = "failed"
                entry["error"] = res["error"] or f"HTTP {res['status']}"
                report["results"].append(entry)
                continue
            try:
                check_response(res["body"], doi)
            except Exception as e:          # ValueError for every malformed shape; anything else too
                entry.update(outcome="malformed", error=f"{type(e).__name__}: {e}")
                report["results"].append(entry)
                continue
            name = f"{stem}{_next_index(raw_dir, stem):03d}.json"
            try:
                save_raw(raw_dir, name, res["body"], report.setdefault("warnings", []))
                pubrecords.register_raw(lit_dir, name, pubrecords.VERIFY_PREFIX + pid, "crossref",
                                        pubrecords.CROSSREF_ROUTE, url, {"doi": doi, "paper_id": pid},
                                        pubrecords.utc_now(), 1, transcribed=False,
                                        notes="Crossref verification lookup (D-064 second source)")
                rows = [r for r in pubrecords.read_manifest(lit_dir) if r["raw_file"] == name]
                if len(rows) != 1 or rows[0]["sha256"] != hashlib.sha256(res["body"]).hexdigest():
                    raise OSError(f"{name}: manifest row missing or checksum differs after registration")
            except Exception as e:          # persistence failed: stop, keep everything, report
                entry.update(outcome="persistence_error", raw_file=name, error=f"{type(e).__name__}: {e}")
                # say what is on disk: a failure after the manifest write (e.g. its fsync) leaves the
                # row in place; the paper is then skipped as already registered when the run resumes
                try:
                    entry["file_saved"] = (raw_dir / name).exists()
                    entry["manifest_row_present"] = any(r["raw_file"] == name
                                                        for r in pubrecords.read_manifest(lit_dir))
                except Exception as e2:     # the check itself must not hide the original failure
                    entry["state_check_error"] = f"{type(e2).__name__}: {e2}"
                report["results"].append(entry)
                report["aborted"] = True
                break
            entry.update(outcome="saved", raw_file=name)
            report["results"].append(entry)
    finally:
        # runs on success, on any exception and on KeyboardInterrupt; nothing in here may replace
        # the exception that is propagating
        progress["stage"] = "finishing"
        if locked:
            try:
                lock.unlink()
            except OSError as e:
                report.setdefault("warnings", []).append(f"lock file not removed: {e}")
        try:
            report["orphans"] = orphans(lit_dir)
        except Exception as e:
            report["orphans"] = None
            report.setdefault("warnings", []).append(f"orphan listing failed: {type(e).__name__}: {e}")
        if not report.get("warnings"):
            report.pop("warnings", None)
    if report["status"] == "incomplete":
        report["status"] = "aborted" if report.get("aborted") else "finished"
    progress["stage"] = "done"
    return report


def failure_report(exc, progress):
    """A clearly marked report for a run that did not finish (planning failure, KeyboardInterrupt or
    any other exception escaping run()). It describes only what is known; it is never a substitute
    for the exception, which the caller re-raises."""
    return {"status": "incomplete", "completed": False,
            "failure_stage": progress.get("stage", "reading_pilot"),
            "exception": type(exc).__name__, "message": str(exc),
            "note": ("The run did not finish. Any results below are partial; papers without a result "
                     "were not processed. The original exception and traceback follow on standard "
                     "error. Persisted files and manifest rows are as listed under orphans/results; "
                     "re-run with the same --run-date to resume."),
            "partial_report": progress.get("report")}


def emit_failure_report(exc, progress, stream=None):
    """Print failure_report() as JSON. A failure while doing so is reported on standard error as one
    line, if possible, and otherwise ignored, so it can never replace the original exception."""
    try:
        print(json.dumps(failure_report(exc, progress), indent=2, default=str), file=stream or sys.stdout,
              flush=True)
    except Exception as e:
        try:
            print(f"fetch_crossref: failure report could not be written: {type(e).__name__}: {e}",
                  file=sys.stderr, flush=True)
        except Exception:
            pass


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pilot", required=True, help="CSV with a paper_id column (authorised pilot)")
    ap.add_argument("--run-date", required=True)
    ap.add_argument("--lit-dir", default="research/literature")
    ap.add_argument("--execute", action="store_true", help="contact Crossref (default: dry run)")
    a = ap.parse_args(argv)
    progress = {}
    try:
        report = run(load_pilot(a.pilot), a.run_date, a.lit_dir, execute=a.execute, progress=progress)
    except BaseException as exc:           # incl. KeyboardInterrupt: report, then re-raise unchanged
        emit_failure_report(exc, progress)
        raise
    print(json.dumps(report, indent=2))
    ok = (not report.get("refused") and not report.get("aborted")
          and all(r["outcome"] in OK_OUTCOMES for r in report["results"]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
