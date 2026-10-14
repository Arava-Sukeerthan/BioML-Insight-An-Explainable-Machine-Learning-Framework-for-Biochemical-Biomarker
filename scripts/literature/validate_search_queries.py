"""Validate research/literature/search_queries.csv.

Checks:
  * required columns present, query_id unique, controlled vocabularies respected;
  * balanced parentheses and double quotes in every query string;
  * PubMed rows meant for the PubMed connector respect its limits
    (<= 20 boolean operators, <= 5 wildcards), measured after substituting {RUN_DATE};
  * planned PubMed queries match their pilot string apart from the date clause;
  * executed rows have a run date and hit count.

Usage: python3 -I scripts/literature/validate_search_queries.py research/literature/search_queries.csv
Exit code 0 = all checks passed.
"""
import csv
import re
import sys

REQUIRED = ["query_id", "row_type", "rq", "source", "interface", "status", "query_string",
            "date_limit", "other_filters", "result_cap", "run_date", "hits_total",
            "records_retained", "export_file", "linked_ids", "notes"]
ROW_TYPES = {"capability_probe", "pilot_count", "planned", "executed"}
SOURCES = {"pubmed", "europepmc", "crossref", "semantic_scholar", "google_scholar", "consensus",
           "arxiv", "publisher_site", "repository", "web"}
MAX_OPS, MAX_WILDCARDS = 20, 5
DATE_CLAUSE = re.compile(r"\s+AND\s+[0-9/]+:(?:[0-9/]+|\{RUN_DATE\})\[(?:dp|edat)\]")


def strip_quoted(q):
    return re.sub(r'"[^"]*"', '""', q)


def pubmed_limits(q):
    q = q.replace("{RUN_DATE}", "2026/10/14")
    ops = len(re.findall(r"\b(?:AND|OR|NOT)\b", strip_quoted(q)))
    wildcards = q.count("*")
    return ops, wildcards


def balanced(q):
    if q.count('"') % 2:
        return False
    depth = 0
    for ch in strip_quoted(q):
        depth += ch == "("
        depth -= ch == ")"
        if depth < 0:
            return False
    return depth == 0


def main(path):
    errors = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED if c not in reader.fieldnames]
        if missing:
            print("FAIL missing columns:", missing)
            return 1
        rows = list(reader)

    ids = [r["query_id"] for r in rows]
    dups = {i for i in ids if ids.count(i) > 1}
    if dups:
        errors.append(f"duplicate query_id: {sorted(dups)}")
    by_id = {r["query_id"]: r for r in rows}

    for r in rows:
        qid, q = r["query_id"], r["query_string"]
        if r["row_type"] not in ROW_TYPES:
            errors.append(f"{qid}: bad row_type {r['row_type']!r}")
        if r["source"] not in SOURCES:
            errors.append(f"{qid}: bad source {r['source']!r}")
        if not q.strip():
            errors.append(f"{qid}: empty query_string")
        if r["source"] in {"pubmed", "europepmc"} and not balanced(q):
            errors.append(f"{qid}: unbalanced parentheses or quotes")
        if r["row_type"] in {"capability_probe", "pilot_count", "executed"}:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["run_date"]):
                errors.append(f"{qid}: executed/probe/pilot row without ISO run_date")
        if r["row_type"] == "pilot_count" and r["status"] == "pilot_ok" and not r["hits_total"].isdigit():
            errors.append(f"{qid}: successful pilot without integer hits_total")
        if r["source"] == "pubmed" and r["row_type"] == "planned":
            ops, wc = pubmed_limits(q)
            if ops > MAX_OPS or wc > MAX_WILDCARDS:
                errors.append(f"{qid}: exceeds connector limits (ops={ops}, wildcards={wc})")
            pid = r["linked_ids"]
            if pid not in by_id:
                errors.append(f"{qid}: linked pilot {pid!r} not found")
            else:
                a = DATE_CLAUSE.sub("", q)
                b = DATE_CLAUSE.sub("", by_id[pid]["query_string"])
                if a != b:
                    errors.append(f"{qid}: differs from pilot {pid} beyond the date clause")

    counts = {}
    for r in rows:
        counts[(r["row_type"], r["source"])] = counts.get((r["row_type"], r["source"]), 0) + 1
    for k in sorted(counts):
        print(f"{k[0]:17s} {k[1]:17s} {counts[k]}")
    for r in rows:
        if r["source"] == "pubmed" and r["row_type"] == "planned":
            ops, wc = pubmed_limits(r["query_string"])
            print(f"{r['query_id']}: operators={ops} wildcards={wc}")
    if errors:
        print("\nFAIL")
        for e in errors:
            print(" -", e)
        return 1
    print(f"\nPASS: {len(rows)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "research/literature/search_queries.csv"))
