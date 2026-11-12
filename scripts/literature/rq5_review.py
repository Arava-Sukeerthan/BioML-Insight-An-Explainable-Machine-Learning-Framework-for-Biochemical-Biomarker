"""RQ5 closest-prior-art matrix from VALIDATED full-text screening decisions (D-031 to D-038).

Status: READY. Input for the Stage D gate and D-016. It never assigns a
status: coverage groups come from pubrecords.derive_rq5_coverage_group on the CONFIRMED (full-text)
component statuses only (D-035); title/abstract statuses are never counted (D-034, D-035 G2).

Output (identifiers and statuses only; no titles, abstracts or quotations):
  * one row per record with confirmed statuses: the five components, the D-034 group, the D-037-A1
    provisional flag, the D-038 subgroup for `qualified` records ((a) 5 yes; (b) 4 yes + 1 unclear,
    naming the component; (c) 4 yes + 1 no), whether the researcher verified it (screener=researcher on
    the latest full-text row), and the overlap with this project's planned framework components;
  * a verification queue: `qualified` and `near_rq5` records not yet researcher-verified, and records
    whose group is provisional;
  * counts per group. Only subgroup (a) may be described as covering all five components (D-038 (2));
  * completeness (Q-101, 2026-11-12), reported as three separate statuses:
      - title/abstract screening complete: every record in the D-044 screening scope has a title/abstract
        decision (Stage-0 or manual), i.e. none awaits screening; counts come from
        flow_diagram.flow_counts (validated and reconciled with the scope);
      - RQ5 evidence review of the records routed so far complete: every record routed toward RQ5 has a
        confirmed full-text component assessment and no matrix record awaits researcher verification.
        While screening is incomplete, routing is not final, so this status alone never means the RQ5
        review is complete;
      - review complete = both. Only then may the output be used as completed RQ5 evidence for D-016.
    Without screening counts (e.g. summarise() called without them) completeness is never claimed
    (fail closed). While incomplete, the output begins with an INCOMPLETE banner.
The planned framework (protocol v1.0 candidate §11.2) covers classification, calibration, uncertainty
and explainability; feature selection is not a framework component. The overlap column is a
descriptive comparison for the gap matrix, not a novelty judgement (CLAUDE.md rule 14).

Usage: python3 -I scripts/literature/rq5_review.py [--lit-dir research/literature] [--decisions PATH]
Refuses (exit 2) without a decisions file, on a file without decision rows, on any invalid row, or when
the decisions do not reconcile with the D-044 scope (the flow_diagram.flow_counts checks).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pubrecords as pr  # noqa: E402
import flow_diagram as fd  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
COMPONENTS = list(pr.RQ5_COMPONENT_FIELDS)
PLANNED = {"classification", "calibration", "uncertainty", "explainability"}
GROUP_ORDER = {"qualified": 0, "near_rq5": 1, "below_threshold": 2}


class RQ5Error(ValueError):
    pass


def d038_subgroup(statuses):
    vals = [statuses[c] for c in COMPONENTS]
    if vals.count("yes") == 5:
        return "a: 5 yes"
    if vals.count("yes") == 4 and vals.count("unclear") == 1:
        return "b: 4 yes + unclear " + next(c for c in COMPONENTS if statuses[c] == "unclear")
    if vals.count("yes") == 4 and vals.count("no") == 1:
        return "c: 4 yes + 1 no"
    return ""


def load_bibliographic_status(lit_dir):
    """paper_id -> verification_status from paper_inventory.json (D-064). Read-only."""
    data = json.loads((Path(lit_dir) / "paper_inventory.json").read_text(encoding="utf-8"))
    recs = data if isinstance(data, list) else data.get("records", data.get("publications", []))
    return {r["paper_id"]: r.get("verification_status") for r in recs}


def matrix(decision_rows, bib_status=None):
    """bib_status: paper_id -> D-064 verification status; a record that is not `verified` is marked
    "not citable" (research_plan.md section 6). Without bib_status every record is marked "unknown"."""
    ev = pr.rq5_component_evidence(decision_rows)          # raises on incomplete or blanked components
    out = []
    for pid, e in ev.items():
        c = e["confirmed"]
        if not c:
            continue
        st = c["statuses"]
        group, provisional = pr.derive_rq5_coverage_group(st)
        if group is None:
            continue
        overlap = sorted(k for k in PLANNED if st[k] == "yes")
        out.append({"paper_id": pid, **{k: st[k] for k in COMPONENTS}, "group": group,
                    "provisional": provisional, "d038_subgroup": d038_subgroup(st) if group == "qualified" else "",
                    "researcher_verified": c["researcher_verified"],
                    "bibliographic_status": (bib_status or {}).get(pid, "unknown"),
                    "citable": (bib_status or {}).get(pid) == "verified",
                    "planned_components_covered": f"{len(overlap)}/4 ({', '.join(overlap) or 'none'})"})
    out.sort(key=lambda r: (GROUP_ORDER[r["group"]], -int(r["planned_components_covered"][0]), r["paper_id"]))
    return out


def pending_assessment(decision_rows):
    """Records routed toward RQ5 at title/abstract (latest row include/uncertain with RQ5 in rq_tags)
    that have no confirmed full-text component assessment yet."""
    ev = pr.rq5_component_evidence(decision_rows)
    latest = {}
    for r in decision_rows:
        if r["stage"] == "title_abstract":
            latest[r["paper_id"]] = r
    routed = {pid for pid, r in latest.items()
              if r["decision"] in ("include", "uncertain") and "RQ5" in (r.get("rq_tags") or "").split(";")}
    return sorted(pid for pid in routed if not (ev.get(pid) or {}).get("confirmed"))


def screening_status(flow):
    """Title/abstract screening status of the whole D-044 scope from flow_diagram.flow_counts output.
    Complete only if the scope is non-empty and no in-scope record awaits title/abstract screening."""
    if flow is None:
        return {"scope": None, "stage0_excluded": None, "ta_screened": None, "awaiting_ta": None,
                "complete": False}
    scope, awaiting = int(flow["scope"]), int(flow["awaiting_ta"])
    return {"scope": scope, "stage0_excluded": int(flow["stage0_excluded"]), "ta_screened": int(flow["ta_screened"]),
            "awaiting_ta": awaiting, "complete": scope > 0 and awaiting == 0}


def summarise(rows, pending=(), screening=None):
    """screening: flow_diagram.flow_counts output for the same decisions. Without it the review is never
    reported complete (fail closed, Q-101)."""
    counts = {g: sum(r["group"] == g for r in rows) for g in GROUP_ORDER}
    queue = [r["paper_id"] for r in rows if (r["group"] in ("qualified", "near_rq5") and not r["researcher_verified"])
             or r["provisional"]]
    scr = screening_status(screening)
    # RQ5 evidence review: no routed record unassessed and no matrix record awaiting researcher
    # verification (D-035, D-038). Screening: no in-scope record awaiting title/abstract screening.
    # Contribution wording (D-016) needs both (CLAUDE.md rule 14; Q-101).
    routed_complete = not pending and not queue
    return {"counts": counts, "verification_queue": sorted(set(queue)),
            "all_five_components": [r["paper_id"] for r in rows if r["d038_subgroup"].startswith("a")],
            "not_citable": [r["paper_id"] for r in rows if not r["citable"]],
            "pending_full_text_assessment": list(pending),
            "screening": scr,
            "screening_complete": scr["complete"],
            "rq5_routed_records_complete": routed_complete,
            "review_complete": scr["complete"] and routed_complete}


def to_markdown(rows, summary):
    head = ["paper_id"] + COMPONENTS + ["group", "provisional", "D-038 subgroup", "researcher verified",
                                       "bibliographic status", "planned components covered"]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in rows:
        lines.append("| " + " | ".join([r["paper_id"]] + [r[k] for k in COMPONENTS] + [
            r["group"], "yes" if r["provisional"] else "no", r["d038_subgroup"] or "—",
            "yes" if r["researcher_verified"] else "no",
            r["bibliographic_status"] + ("" if r["citable"] else " (not citable)"),
            r["planned_components_covered"]]) + " |")
    s = summary
    scr = s["screening"]
    if scr["scope"] is None:
        scr_text = "Title/abstract screening: status not available (completeness not assessed)"
    else:
        scr_text = (f"Title/abstract screening: {scr['awaiting_ta']} of {scr['scope']} in-scope record(s) awaiting "
                    f"screening (Stage-0 excluded {scr['stage0_excluded']}; screened {scr['ta_screened']})")
    banner = "" if s["review_complete"] else (
        "**INCOMPLETE — this RQ5 output is not completed evidence and must not be used for D-016 or any "
        "contribution or novelty wording.**\n\n")
    return (banner + "\n".join(lines) + f"\n\n{scr_text}. "
            f"Screening complete: {'yes' if s['screening_complete'] else 'no'}. "
            f"RQ5 evidence review of the records routed so far: {'complete' if s['rq5_routed_records_complete'] else 'incomplete'}"
            f"{'' if s['screening_complete'] else ' (routing is not final until title/abstract screening is complete)'}."
            f"\n\nCounts: {json.dumps(s['counts'])}. Researcher verification queue: "
            f"{len(s['verification_queue'])} record(s). Not citable (not D-064 verified): {len(s['not_citable'])}. "
            f"Routed records without a full-text assessment: {len(s['pending_full_text_assessment'])}. "
            f"Review complete: {'yes' if s['review_complete'] else 'NO — no contribution or novelty wording is supported yet'}. "
            "Only D-038 subgroup (a) may be described as covering all five components. "
            "Coverage is not a quality or novelty judgement.\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lit-dir", default=str(REPO / "research" / "literature"))
    ap.add_argument("--decisions")
    a = ap.parse_args(argv)
    lit = Path(a.lit_dir)
    path = Path(a.decisions) if a.decisions else lit / "screening" / "decisions.csv"
    try:
        if not path.exists():
            raise RQ5Error(f"{path} does not exist: no screening has been recorded")
        decisions = pr.load_screening_decisions(lit, path)
        flow = fd.flow_counts(lit, path)                    # scope, reconciliation; refuses an empty file
        rows = matrix(decisions, load_bibliographic_status(lit))
        pending = pending_assessment(decisions)
    except (RQ5Error, ValueError) as e:                  # FlowError is a ValueError
        print(f"refused: {e}", file=sys.stderr)
        return 2
    print(to_markdown(rows, summarise(rows, pending, flow)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
