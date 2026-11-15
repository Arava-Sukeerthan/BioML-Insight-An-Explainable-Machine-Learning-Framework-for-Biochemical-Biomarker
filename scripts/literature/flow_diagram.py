"""Screening flow diagram (PRISMA-style counts) from VALIDATED screening decisions only.

Reads screening/decisions.csv through pubrecords.load_screening_decisions, the same validator the
build uses (frozen criteria_version enforced once the registry exists), so an invalid row stops the
generator; nothing is silently dropped. It never writes decisions, records or the inventory.

Additional consistency rules (any failure refuses the diagram; exit status 2):
  * every decision's paper_id is in the D-044 screening scope (scope/D-044_scope_paper_ids.csv);
  * the latest row per (paper_id, stage) is used (append-only file; earlier rows are kept, not counted);
  * a full_text row requires a title_abstract decision of include or uncertain for the same record
    (Stage-0 exclusions and title/abstract exclusions never reach full text);
  * counts reconcile: scope = Stage-0 excluded + title/abstract screened + awaiting screening, etc.
Identification counts (source records, publications after deduplication) come from
records/build_report.json when present. Output: Markdown counts table, a Mermaid flowchart and a
JSON object; identifiers and counts only, no titles or abstracts.

With no decisions file the generator refuses (no diagram is drawn from absent screening).
Usage: python3 -I scripts/literature/flow_diagram.py [--lit-dir research/literature] [--decisions PATH]
                                                       [--format markdown|json]
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pubrecords as pr  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
SCOPE_FILE = Path("scope") / "D-044_scope_paper_ids.csv"


class FlowError(ValueError):
    pass


def _latest(rows):
    """Latest row per (paper_id, stage), by file order (append-only)."""
    out = {}
    for r in rows:
        out[(r["paper_id"], r["stage"])] = r
    return out


def _codes(rows):
    c = {}
    for r in rows:
        c[r["reason_code"]] = c.get(r["reason_code"], 0) + 1
    return dict(sorted(c.items(), key=lambda kv: (len(kv[0]), kv[0])))


def flow_counts(lit_dir, decisions_path=None, scope_ids=None):
    lit_dir = Path(lit_dir)
    path = Path(decisions_path) if decisions_path else lit_dir / "screening" / "decisions.csv"
    if not path.exists():
        raise FlowError(f"{path} does not exist: no screening has been recorded, so no flow diagram is drawn")
    rows = pr.load_screening_decisions(lit_dir, path)          # full validation; raises on any invalid row
    if not rows:
        raise FlowError(f"{path} has no decision rows")
    if scope_ids is None:
        with open(lit_dir / SCOPE_FILE, newline="", encoding="utf-8") as f:
            scope_ids = {r["paper_id"] for r in csv.DictReader(f)}
    scope_ids = set(scope_ids)
    outside = sorted({r["paper_id"] for r in rows} - scope_ids)
    if outside:
        raise FlowError(f"{len(outside)} decision(s) for records outside the D-044 scope: {outside[:5]}")
    latest = _latest(rows)
    ta = {pid: r for (pid, st), r in latest.items() if st == "title_abstract"}
    ft = {pid: r for (pid, st), r in latest.items() if st == "full_text"}
    orphan = sorted(pid for pid in ft if pid not in ta or ta[pid]["decision"] not in ("include", "uncertain"))
    if orphan:
        raise FlowError(f"{len(orphan)} full-text decision(s) without a title/abstract include or uncertain: "
                        f"{orphan[:5]}")
    stage0 = [r for r in ta.values() if pr.is_stage0_rule_row(r)]
    manual = [r for r in ta.values() if not pr.is_stage0_rule_row(r)]
    ta_excl = [r for r in manual if r["decision"] == "exclude"]
    ta_fwd = [r for r in manual if r["decision"] in ("include", "uncertain")]
    ft_rows = list(ft.values())
    c = {
        "scope": len(scope_ids),
        "stage0_excluded": len(stage0), "stage0_by_code": _codes(stage0),
        "ta_screened": len(manual),
        "ta_excluded": len(ta_excl), "ta_excluded_by_code": _codes(ta_excl),
        "ta_include": sum(r["decision"] == "include" for r in manual),
        "ta_uncertain": sum(r["decision"] == "uncertain" for r in manual),
        "awaiting_ta": len(scope_ids) - len(ta),
        "ft_sought": len(ta_fwd),
        "ft_assessed": sum(r["decision"] in ("include", "exclude") for r in ft_rows),
        "ft_abstract_only": sum(r["decision"] == "abstract_only" for r in ft_rows),
        "ft_uncertain": sum(r["decision"] == "uncertain" for r in ft_rows),
        "ft_excluded": sum(r["decision"] == "exclude" for r in ft_rows),
        "ft_excluded_by_code": _codes([r for r in ft_rows if r["decision"] == "exclude"]),
        "included": sum(r["decision"] == "include" for r in ft_rows),
        "awaiting_ft": len(ta_fwd) - len(ft_rows),
        "rows_total": len(rows), "rows_superseded": len(rows) - len(latest),
        "criteria_versions": sorted({r["criteria_version"] for r in rows if r["criteria_version"]}),
    }
    # reconciliation (would only fail on a logic error; kept as an explicit guard)
    if c["stage0_excluded"] + c["ta_screened"] + c["awaiting_ta"] != c["scope"]:
        raise FlowError("title/abstract counts do not reconcile with the scope")
    if c["ta_excluded"] + c["ft_sought"] != c["ta_screened"]:
        raise FlowError("title/abstract decisions do not reconcile")
    if (c["ft_excluded"] + c["included"] + c["ft_abstract_only"] + c["ft_uncertain"] + c["awaiting_ft"]
            != c["ft_sought"]):
        raise FlowError("full-text counts do not reconcile")
    rep = lit_dir / "records" / "build_report.json"
    if rep.exists():
        b = json.loads(rep.read_text(encoding="utf-8"))
        c["identified_source_records"] = b.get("source_records")
        c["publications_after_dedup"] = b.get("publications")
    return c


def _fmt_codes(d):
    return "; ".join(f"{k} {v}" for k, v in d.items()) or "none"


def to_markdown(c):
    lines = ["| Step | n |", "|---|---|"]
    if c.get("identified_source_records") is not None:
        lines += [f"| Source records identified | {c['identified_source_records']} |",
                  f"| Publication records after deduplication | {c['publications_after_dedup']} |"]
    lines += [f"| In screening scope (D-044) | {c['scope']} |",
              f"| Excluded at Stage 0 (publication type) | {c['stage0_excluded']} ({_fmt_codes(c['stage0_by_code'])}) |",
              f"| Title/abstract screened | {c['ta_screened']} |",
              f"| Title/abstract excluded | {c['ta_excluded']} ({_fmt_codes(c['ta_excluded_by_code'])}) |",
              f"| Awaiting title/abstract screening | {c['awaiting_ta']} |",
              f"| Sought for full text (include {c['ta_include']}, uncertain {c['ta_uncertain']}) | {c['ft_sought']} |",
              f"| Full text not available (abstract only) | {c['ft_abstract_only']} |",
              f"| Full text assessed | {c['ft_assessed']} |",
              f"| Full text excluded | {c['ft_excluded']} ({_fmt_codes(c['ft_excluded_by_code'])}) |",
              f"| Full text unresolved (uncertain) | {c['ft_uncertain']} |",
              f"| Awaiting full-text assessment | {c['awaiting_ft']} |",
              f"| **Included** | **{c['included']}** |"]
    mer = ["```mermaid", "flowchart TD"]
    if c.get("identified_source_records") is not None:
        mer += [f'  ID["Source records identified: {c["identified_source_records"]}"] --> DD["After deduplication: {c["publications_after_dedup"]}"]',
                f'  DD --> SC["In screening scope: {c["scope"]}"]']
    else:
        mer += [f'  SC["In screening scope: {c["scope"]}"]']
    mer += [f'  SC --> S0["Stage 0 excluded: {c["stage0_excluded"]}"]',
            f'  SC --> TA["Title/abstract screened: {c["ta_screened"]}"]',
            f'  SC --> AW["Awaiting screening: {c["awaiting_ta"]}"]',
            f'  TA --> TX["Excluded: {c["ta_excluded"]}"]',
            f'  TA --> FT["Sought for full text: {c["ft_sought"]}"]',
            f'  FT --> AO["Abstract only: {c["ft_abstract_only"]}"]',
            f'  FT --> FX["Full text excluded: {c["ft_excluded"]}"]',
            f'  FT --> IN["Included: {c["included"]}"]', "```"]
    note = (f"Counts from {c['rows_total']} validated decision rows ({c['rows_superseded']} superseded by later "
            f"rows); criteria version(s): {', '.join(c['criteria_versions']) or 'not recorded'}.")
    return "\n".join(lines) + "\n\n" + "\n".join(mer) + "\n\n" + note + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lit-dir", default=str(REPO / "research" / "literature"))
    ap.add_argument("--decisions")
    ap.add_argument("--format", choices=("markdown", "json"), default="markdown")
    a = ap.parse_args(argv)
    try:
        c = flow_counts(a.lit_dir, a.decisions)
    except (FlowError, ValueError) as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    print(json.dumps(c, indent=2, sort_keys=True) if a.format == "json" else to_markdown(c))
    return 0


if __name__ == "__main__":
    sys.exit(main())
