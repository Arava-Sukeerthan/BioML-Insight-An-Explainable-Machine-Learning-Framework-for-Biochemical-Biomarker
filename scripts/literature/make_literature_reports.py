"""Generate the LIT-003 literature deliverables from the outputs of pubrecords.py build.

Reads (never edits) raw_exports/MANIFEST.csv, search_queries.csv and records/*.jsonl, and writes:
  research/literature/search_execution_register.md   one row per executed search (provenance)
  research/literature/records/collection_stats.json  counts used in the reports (deduplication etc.)
  research/literature/paper_inventory.csv / .json    literature evidence table (abstract-free)
  research/literature/fulltext_review_candidates.csv mechanical priority list (NOT a screening result)
  research/literature/verification_report.md         record-verification report

Nothing here reads abstracts into committed files or extracts study findings: every extraction
field is set to the sentinel "REQUIRES FULL-TEXT REVIEW" until a human/assistant extraction step
fills it from the paper itself. Standard library only (jsonschema optional for validation).

Usage: python3 -I scripts/literature/make_literature_reports.py [--lit-dir research/literature]
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pubrecords as pr  # noqa: E402

SENTINEL = "REQUIRES FULL-TEXT REVIEW"
# Theme letters follow research_plan.md section 2 (A metabolomics, B routine biochemistry,
# C explainability, D calibration/uncertainty, E external validation/shift, F integrated
# frameworks, Q methodological quality / reviews).
THEMES = {
    "Q-PM-01": "A", "Q-PM-02": "B", "Q-PM-03": "A", "Q-PM-04": "C", "Q-PM-05": "C",
    "Q-PM-06": "D", "Q-PM-07": "D", "Q-PM-08": "D", "Q-PM-09": "E", "Q-PM-10": "E",
    "Q-PM-11": "F", "Q-PM-12": "F", "Q-PM-13": "Q", "Q-PM-14": "Q", "Q-PM-15": "A;E",
    "Q-AX-01": "D", "Q-AX-02": "D", "Q-AX-03": "E", "Q-AX-04": "C", "Q-AX-05": "F",
    "Q-WS-01": "A;C", "Q-WS-02": "D", "Q-WS-03": "E", "Q-WS-04": "F", "Q-WS-05": "A", "Q-RP-03": "A",
}
EXTRACTION_FIELDS = ["research_problem", "disorder", "population", "dataset", "sample_size",
                     "biomarker_type", "biomarkers_features", "prediction_target", "models",
                     "validation_design", "explainability", "uncertainty_methods",
                     "calibration_methods", "reported_metrics", "limitations_noted"]
INV_COLS = ["paper_id", "title", "authors", "year", "venue", "doi", "pmid", "arxiv_id", "url", "pmcid",
            "source_db", "query_ids", "retrieved_on", "verification_status", "verification_note",
            "screening_status", "screening_stage", "exclusion_reason", "publication_type", "rq_tags", "tier",
            "scope_flags", "record_type", "dim_explainability", "dim_uncertainty", "dim_calibration",
            "dim_independent_validation", "dim_feature_selection", "dim_classification", "screener",
            "screening_date", "screening_justification",
            "source_publication_types", "abstract_available", "full_text_availability", "retrieval_themes",
            "preliminary_relevance", "extraction_status"] + EXTRACTION_FIELDS + ["notes"]


# Fields filled by people (extraction). A rebuild carries their existing values forward instead
# of resetting them (LIT-004-WORKFLOW-FIXES).
MANUAL_FIELDS = EXTRACTION_FIELDS + ["extraction_status", "publication_type"]
MANUAL_DEFAULTS = {**{k: SENTINEL for k in EXTRACTION_FIELDS}, "extraction_status": "not_extracted",
                   "publication_type": None}
YEAR_NOTE = "year not returned by the source (0 = missing)"   # generated, not a manual note


def _csv_text(v):
    """A value as csv.DictWriter writes it (None -> empty)."""
    return "" if v is None else str(v)


def manual_values(lit):
    """Manual values of the existing inventory, keyed by paper ID. paper_inventory.json is the file
    that is edited; the CSV is a generated copy. If the CSV was changed after it was generated
    (checksum recorded in collection_stats.json), its manual fields must agree with the JSON,
    otherwise an edit made in the CSV would be overwritten silently, so the run stops instead
    (LIT-004-REVIEW-AND-DECISIONS)."""
    jpath, cpath = lit / "paper_inventory.json", lit / "paper_inventory.csv"
    previous = {r["paper_id"]: r for r in json.load(open(jpath))} if jpath.exists() else {}
    spath = lit / "records" / "collection_stats.json"
    recorded = json.load(open(spath)).get("paper_inventory_csv_sha256") if spath.exists() else None
    if cpath.exists() and recorded != pr.sha256_file(cpath):
        with open(cpath, newline="") as f:
            rows = {r["paper_id"]: r for r in csv.DictReader(f)}
        if not previous and any(any(_csv_text(MANUAL_DEFAULTS[k]) != r.get(k, "") for k in MANUAL_FIELDS)
                                or r.get("notes", "") not in ("", YEAR_NOTE) for r in rows.values()):
            raise SystemExit("paper_inventory.csv has manual values but paper_inventory.json is missing "
                             "(nothing written)")
        diff = sorted(f"{pid}:{k}" for pid, r in previous.items() for k in MANUAL_FIELDS + ["notes"]
                      if pid in rows and k in rows[pid] and _csv_text(r.get(k)) != rows[pid][k])
        diff += sorted(f"{pid}:(row only in one file)" for pid in set(rows) ^ set(previous)) if previous else []
        if diff:
            raise SystemExit("paper_inventory.csv and paper_inventory.json disagree on manual fields; "
                             "copy the edits into the JSON file first (nothing written): "
                             + ", ".join(diff[:20]) + (" ..." if len(diff) > 20 else ""))
    out = {}
    for pid, r in previous.items():
        v = {k: r.get(k) for k in MANUAL_FIELDS if k in r and r.get(k) != MANUAL_DEFAULTS[k]}
        if r.get("notes") not in (None, YEAR_NOTE):
            v["notes"] = r["notes"]
        if v:
            out[pid] = v
    return out


def load_jsonl(path):
    with open(path) as f:
        return [json.loads(line) for line in f]


def themes_of(query_ids):
    out = set()
    for q in query_ids:
        out.update(t for t in THEMES.get(q, "").split(";") if t)
    return sorted(out)


def author_string(authors):
    names = []
    for a in authors or []:
        if a.get("collective_name"):
            names.append(a["collective_name"])
        elif a.get("last_name"):
            names.append(f"{a['last_name']} {a.get('initials') or a.get('fore_name') or ''}".strip())
    return "; ".join(names)


def dedup_stats(lit_dir):
    rows = pr.read_manifest(lit_dir)
    records, _ = pr.build_source_records(lit_dir, rows)
    n = len(records)
    # identifier-only clustering (same as step 1 of pr.deduplicate, without the title rules)
    uf = pr._UF(n)
    for key in ("pmid", "doi", "pmcid", "arxiv_id"):
        first = {}
        for i, r in enumerate(records):
            v = r.get(key)
            if v:
                if v in first:
                    a, b = uf.find(first[v]), uf.find(i)
                    if a != b:
                        uf.p[b] = a
                else:
                    first[v] = i
    id_clusters = len({uf.find(i) for i in range(n)})
    by_source = collections.Counter(r["source"] for r in records)
    return records, {"raw_source_records": n, "raw_by_source": dict(by_source),
                     "identifier_clusters": id_clusters,
                     "removed_as_exact_identifier_duplicates": n - id_clusters}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lit-dir", default="research/literature")
    a = ap.parse_args(argv)
    lit = Path(a.lit_dir)
    rec = lit / "records"
    pubs = load_jsonl(rec / "publications.jsonl")
    report = json.load(open(rec / "build_report.json"))
    with open(rec / "dedup_review.csv", newline="") as f:
        review = list(csv.DictReader(f))
    records, stats = dedup_stats(lit)
    stats["publications_retained"] = len(pubs)
    stats["merged_by_title_rule"] = stats["identifier_clusters"] - len(pubs)
    # an identifier conflict prevents a merge, so it can leave more clusters than the identifier
    # pass alone would suggest; report the conflicts separately
    stats["dedup_review_pairs_by_reason"] = dict(collections.Counter(
        r["reason"].split(":")[0] for r in review))
    stats["title_based_duplicate_candidates"] = sum(
        1 for r in review if not r["reason"].startswith("identifier_conflict"))
    stats["identifier_conflict_pairs"] = sum(1 for r in review if r["reason"].startswith("identifier_conflict"))
    stats["records_requiring_manual_dedup_review"] = len(
        {r["paper_id_a"] for r in review} | {r["paper_id_b"] for r in review})
    stats["verification_status"] = report["verification_status"]
    stats["retracted"] = report["retracted"]

    # ---------------- evidence table (paper_inventory) ----------------
    manual_prev = manual_values(lit)
    built = {p["paper_id"] for p in pubs}
    lost = sorted(set(manual_prev) - built)
    if lost:
        raise SystemExit("paper_inventory.json has manual values for paper IDs that are not in the "
                         f"current build (nothing written): {', '.join(lost)}")
    inv = []
    for p in pubs:
        qids = sorted({s["query_id"] for s in p["search_provenance"]})
        th = themes_of(qids)
        sd = p.get("screening_details") or {}
        row = {
            "paper_id": p["paper_id"], "title": p["title"] or "", "authors": author_string(p["authors"]),
            "year": p["year"], "venue": p["journal"] or "", "doi": p["doi"], "pmid": p["pmid"],
            "arxiv_id": p["arxiv_id"], "url": (p["source_urls"] or [None])[0], "pmcid": p["pmcid"],
            "source_db": p["source_databases"][0], "query_ids": ";".join(qids),
            "retrieved_on": min(s["search_timestamp"] for s in p["search_provenance"])[:10],
            "verification_status": p["verification_status"], "verification_note": p["verification_note"],
            "screening_status": p["screening_decision"], "screening_stage": p["screening_stage"],
            "exclusion_reason": p["exclusion_reason"], "publication_type": None,
            "rq_tags": sd.get("rq_tags"), "tier": int(sd["tier"]) if sd.get("tier") else None,
            "scope_flags": ";".join(x for x in (["retracted"] if p["retracted"] else [])
                                    + ((sd.get("scope_flags") or "").split(";")) if x) or None,
            "record_type": sd.get("record_type"), "dim_explainability": sd.get("dim_explainability"),
            "dim_uncertainty": sd.get("dim_uncertainty"), "dim_calibration": sd.get("dim_calibration"),
            "dim_independent_validation": sd.get("dim_independent_validation"),
            "dim_feature_selection": sd.get("dim_feature_selection"),
            "dim_classification": sd.get("dim_classification"),
            "screener": sd.get("screener"), "screening_date": sd.get("date"),
            "screening_justification": sd.get("justification"),
            "source_publication_types": ";".join(p["publication_types"] or []) or None,
            "abstract_available": bool(p["abstract"]),
            "full_text_availability": p["full_text_availability"],
            "retrieval_themes": ";".join(th) or None,
            "preliminary_relevance": (("retrieved by theme(s) " + ", ".join(th) if th else "no theme mapping")
                                      + ("; not screened" if p["screening_decision"] == "not_screened"
                                         else f"; screening decision: {p['screening_decision']}")),
            "extraction_status": "not_extracted",
            **{k: SENTINEL for k in EXTRACTION_FIELDS},
            "notes": None,
        }
        if row["year"] is None:
            row["year"] = 0  # schema requires an integer; 0 = year not returned by the source
            row["notes"] = YEAR_NOTE
        row.update(manual_prev.get(p["paper_id"], {}))
        inv.append(row)
    try:   # validate before anything is written
        import jsonschema
        schema = json.load(open(lit / "schemas" / "paper_inventory.schema.json"))
        jsonschema.validate(inv, schema)
        stats["paper_inventory_schema"] = "valid"
    except ImportError:  # pragma: no cover
        stats["paper_inventory_schema"] = "not checked (jsonschema missing)"
    stats["manual_values_carried_forward"] = sum(len(v) for v in manual_prev.values())
    stats["screening_status"] = dict(sorted(collections.Counter(r["screening_status"] for r in inv).items()))
    with open(lit / "paper_inventory.json", "w") as f:
        json.dump(inv, f, indent=1, ensure_ascii=False)
        f.write("\n")
    with open(lit / "paper_inventory.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=INV_COLS)
        w.writeheader()
        w.writerows(inv)
    stats["paper_inventory_csv_sha256"] = pr.sha256_file(lit / "paper_inventory.csv")

    # ---------------- full-text review candidates (mechanical) ----------------
    cand = []
    for r in inv:
        th = set((r["retrieval_themes"] or "").split(";")) - {""}
        reasons = []
        if "F" in th:
            reasons.append("retrieved by an integrated-framework query (theme F, closest-prior-art candidate)")
        if len(th & {"C", "D", "E"}) >= 2:
            reasons.append("retrieved by >=2 of themes C/D/E")
        if not reasons or r["scope_flags"] == "retracted":
            continue
        cand.append({"paper_id": r["paper_id"], "title": r["title"], "year": r["year"], "pmid": r["pmid"],
                     "doi": r["doi"], "arxiv_id": r["arxiv_id"], "retrieval_themes": r["retrieval_themes"],
                     "full_text_availability": r["full_text_availability"],
                     "verification_status": r["verification_status"], "priority_reason": "; ".join(reasons),
                     "status": "candidate - pending title/abstract screening"})
    with open(lit / "fulltext_review_candidates.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cand[0].keys()) if cand else ["paper_id"])
        w.writeheader()
        w.writerows(cand)
    stats["fulltext_review_candidates"] = len(cand)
    stats["publications_by_theme"] = dict(sorted(collections.Counter(
        t for r in inv for t in (r["retrieval_themes"] or "").split(";") if t).items()))
    stats["publications_with_abstract"] = sum(r["abstract_available"] for r in inv)
    stats["publications_with_doi"] = sum(bool(r["doi"]) for r in inv)
    stats["publications_with_pmcid"] = sum(bool(r["pmcid"]) for r in inv)
    stats["preprints_by_pubmed_type"] = sum("Preprint" in (r["source_publication_types"] or "") for r in inv)
    stats["reviews_by_pubmed_type"] = sum(
        any(t in (r["source_publication_types"] or "") for t in ("Review", "Systematic Review", "Meta-Analysis"))
        for r in inv)
    with open(rec / "collection_stats.json", "w") as f:
        json.dump(stats, f, indent=2, sort_keys=True)
        f.write("\n")

    # ---------------- search execution register ----------------
    manifest = pr.read_manifest(lit)
    queries = {r["query_id"]: r for r in csv.DictReader(open(lit / "search_queries.csv", newline=""))}
    by_q = collections.defaultdict(list)
    for m in manifest:
        if m["query_id"] != "META":
            by_q[m["query_id"]].append(m)
    comp = report["search_completeness"]
    lines = ["# Search Execution Register", "",
             "Generated by `scripts/literature/make_literature_reports.py` from `raw_exports/MANIFEST.csv` and",
             "`search_queries.csv` (LIT-003). Do not edit by hand; re-run the script after a new build.", "",
             "| Search ID | Run date (UTC) | Source / interface | Date restriction | Filters | Records returned | Pagination | Export format | Output location (raw, git-ignored; sha256 in MANIFEST.csv) | Retrieval status | Known limitations |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for qid in sorted(by_q, key=lambda q: (q.startswith(pr.CHECK_PREFIX), q)):
        ms = sorted(by_q[qid], key=lambda m: m["raw_file"])
        base = qid.replace(pr.CHECK_PREFIX, "")
        q = queries.get(base, {})
        n = sum(int(m["n_items"]) for m in ms)
        ts = min(m["retrieved_at"] for m in ms)
        req = [json.loads(m["request_json"] or "{}") for m in ms]
        if ms[0]["route"] == "pubmed_connector_search":
            pag = f"{len(ms)} page(s) x max 200 (retstart {', '.join(str(r.get('retstart', 0)) for r in req)})"
            if base in comp and not qid.startswith(pr.CHECK_PREFIX):
                status = (f"complete: {comp[base]['unique_pmids_retrieved']}/{comp[base]['reported_total']} PMIDs; "
                          f"transcription check {ms[0]['transcription_check']}")
            else:
                status = "verification re-fetch (sort=pub_date); not used as hits"
            lim = "PMIDs transcribed from connector output (checked against re-fetch)"
        else:
            pag = "single ranked list (no paging)"
            status = "executed; records transcribed (titles/IDs only)"
            lim = q.get("notes", "")[:160]
        lines.append(f"| {qid} | {ts} | {ms[0]['source']} / {ms[0]['endpoint_or_tool']} | {q.get('date_limit', '')} | "
                     f"{q.get('other_filters', '') or 'none'} | {n} | {pag} | JSON (tool response + provenance block) | "
                     f"raw_exports/{', '.join(m['raw_file'] for m in ms)} | "
                     f"{status} | {lim} |")
    meta = [m for m in manifest if m["query_id"] == "META"]
    if meta:
        lines += ["", f"Metadata retrieval (not a search): {len(meta)} files `META_*.json`, PubMed connector "
                  f"`get_article_metadata`, {sum(int(m['n_items']) for m in meta)} article objects "
                  f"({min(m['retrieved_at'] for m in meta)} to {max(m['retrieved_at'] for m in meta)}); "
                  "responses saved verbatim by the harness, not transcribed."]
    lines += ["", "## Exact query strings as executed", ""]
    for r in queries.values():
        if r["row_type"] == "executed":
            lines.append(f"- `{r['query_id']}`: `{r['query_string']}`")
    lines += ["", "Exact query strings: `search_queries.csv` (`row_type=executed`, column `query_string`, with the "
              "run date substituted). Each raw file also stores the string sent (`provenance.request`) and, for "
              "PubMed, the connector's query translation.", ""]
    (lit / "search_execution_register.md").write_text("\n".join(lines))

    # ---------------- verification report ----------------
    vs = collections.Counter(p["verification_status"] for p in pubs)
    notes = collections.Counter((p["verification_status"], p["verification_note"].split(":")[0]) for p in pubs)
    v = ["# Record Verification Report", "",
         "Generated by `scripts/literature/make_literature_reports.py` (LIT-003). Statuses follow the rules in",
         "`collection_workflow.md` section 4.3 and describe **bibliographic metadata only**, not scientific content.", "",
         "## Status counts", "", "| Status | Publications |", "|---|---|"]
    v += [f"| {k} | {vs[k]} |" for k in sorted(vs)]
    v += ["", "## Reasons", "", "| Status | Reason | Publications |", "|---|---|---|"]
    v += [f"| {s} | {r} | {c} |" for (s, r), c in sorted(notes.items())]
    v += ["", "## Records with status `verified`", "",
          "Rule D-064 (answers Q-068): the authoritative record agrees on title, first author, year, venue and a "
          "shared persistent identifier with a second source that is independent by recorded provenance and, if "
          "transcribed, spot-checked. Web rows carrying only a title and a URL-parsed identifier do not qualify.", "",
          "| Paper ID | PMID | DOI | Sources |", "|---|---|---|---|"]
    v += [f"| {p['paper_id']} | {p['pmid']} | {p['doi']} | {', '.join(p['source_databases'])} |"
          for p in pubs if p["verification_status"] == "verified"]
    v += ["", "## Records with status `needs_review` or metadata conflicts", "", "| Paper ID | Note | Conflicts |", "|---|---|---|"]
    v += [f"| {p['paper_id']} | {p['verification_note']} | "
          f"{'; '.join(c['field'] + ': ' + ' / '.join(str(x['value']) for x in c['values']) for c in p['metadata_conflicts'])} |"
          for p in pubs if p["verification_status"] == "needs_review" or p["metadata_conflicts"]]
    ss = report.get("verification_second_sources") or {}
    v += ["", "## Second-source evaluation (D-064; report-level only)", "",
          "Classifications and eligibility reasons are reported here only; they are not stored in publication "
          "records. Only `independent` second sources are eligible.", ""]
    if ss:
        for key, label in (("independence", "Independence"), ("eligibility", "Eligibility"), ("results", "Result")):
            v += [f"| {label} | Candidate second sources |", "|---|---|"]
            v += [f"| {k} | {n} |" for k, n in sorted((ss.get(key) or {}).items())] + [""]
        v += ["| Paper ID | Status | Second source | Provider | Independence | Basis | Eligibility | Result |",
              "|---|---|---|---|---|---|---|---|"]
        v += [f"| {p['paper_id']} | {p['verification_status']} | {r['source_record_id']} | {r['provider']} | "
              f"{r['independence']} | {r['independence_basis']} | {r['eligibility_reason']} | {r['result']} |"
              for p in ss.get("publications", []) for r in p["candidates"]]
    else:
        v += ["No second-source evaluation in this build report."]
    sc = report.get("verification_status_changes") or {}
    v += ["", "## Verification status changes since the previous build", ""]
    if not sc:
        v += ["Not recorded in this build report."]
    elif not sc.get("previous_build_available"):
        v += ["No previous build output was available for comparison."]
    else:
        v += [f"- Changed: {len(sc.get('changed', []))}; new publications: {sc.get('new_publications', 0)}; "
              f"removed: {len(sc.get('removed_publications', []))}", "",
              "| Paper ID | Previous | Current | Note |", "|---|---|---|---|"]
        v += [f"| {c['paper_id']} | {c['previous']} | {c['current']} | {c['note']} |" for c in sc.get("changed", [])]
    v += ["", "## Retracted publications (PubMed publication type)", "", "| Paper ID | PMID | Title |", "|---|---|---|"]
    v += [f"| {p['paper_id']} | {p['pmid']} | {p['title']} |" for p in pubs if p["retracted"]]
    v += ["", "## Field completeness (as returned by the sources; nothing filled in by hand)", "",
          f"- Publications: {len(pubs)}",
          f"- With DOI: {stats['publications_with_doi']}; without DOI: {len(pubs) - stats['publications_with_doi']}",
          f"- With PMCID: {stats['publications_with_pmcid']}",
          f"- With abstract returned by the source: {stats['publications_with_abstract']}",
          f"- With no author list returned: {sum(not p['authors'] for p in pubs)}",
          f"- With no year returned: {sum(p['year'] is None for p in pubs)}",
          f"- PubMed type 'Preprint': {stats['preprints_by_pubmed_type']}",
          ""]
    (lit / "verification_report.md").write_text("\n".join(v))
    print(json.dumps(stats, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
