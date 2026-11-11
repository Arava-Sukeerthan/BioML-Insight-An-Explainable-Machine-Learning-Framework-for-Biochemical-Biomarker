#!/usr/bin/env python3
"""Pilot follow-on tools (Stage B preparation, P18; researcher authorisation 2026-11-11, D-095).

Three utilities for the D-025 pilot, tested on synthetic fixtures only:

* `template`: the researcher decision template `pilot_decisions_researcher.csv` (protocol v0.2 §7).
  One title/abstract row per sampled `paper_id`, in the screening-record format (criteria v1.1 §6),
  with `stage`, `screener` and `criteria_version` filled in and every decision field empty. It holds
  paper IDs only, never a title or abstract.
* `report`: agreement between the assistant's and the researcher's pilot decisions (protocol v0.2
  §7 "Agreement" and "Pass"): percentage agreement and Cohen's kappa on the three-level decision
  (include / exclude / uncertain) and on include versus not include; primary-code agreement;
  disagreements per exclusion code; per-descriptor agreement. The thresholds are those approved in
  D-025 and are not changed here: kappa (3-level) >= 0.60; no record excluded by one screener and
  included by the other without adjudicated agreement; fewer than 3 disagreements on any single code.
  The operational definitions used to evaluate them (what counts as a disagreement on a code, what
  counts as adjudicated agreement, an undefined kappa) are D-098, APPROVED — PROVISIONAL (subject to
  consistency with D-025; not final). Adjudication rows must be for a pilot paper, at
  `title_abstract`, with `screener=researcher` and a pilot decision (include / exclude / uncertain);
  the latest such row per paper is the agreed decision. An include/exclude conflict counts as
  resolved only when the agreed decision is `exclude` ("adjudicated agreement on the exclusion",
  D-025 as written in protocol v0.1 §7).
* `queue`: the adjudication queue `screening/adjudication_queue.csv` (protocol v0.2 §5 item 4):
  every `uncertain`, every E12, every `needs_human=yes`, every possible-duplicate pair (all pairs of
  `records/dedup_review.csv`; a member without a decision is listed with an empty `stage`), and, for
  the pilot, every record on which the two screeners disagree.

Every decision file is first validated with the repository validator
(`pubrecords.load_screening_decisions`). Outputs hold IDs, codes and counts only (D-010; D-089).
Running these tools on real pilot decisions needs the pilot to have been authorised and screened.
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

DECISION_LEVELS = ("include", "exclude", "uncertain")
EXCLUSION_CODES = tuple(f"E{i}" for i in range(1, 13))
DESCRIPTORS = ("rq_tags", "record_type", "biomarker_class", "dim_explainability", "dim_uncertainty",
               "dim_calibration", "validation_design", "scope_flags")
SET_VALUED = ("rq_tags", "scope_flags")
KAPPA_THRESHOLD = 0.60            # D-025 pass criterion (unchanged)
MAX_CODE_DISAGREEMENTS = 2        # D-025: "fewer than 3 disagreements on any single code" (unchanged)
TEMPLATE_COLUMNS = pr.SCREENING_REQUIRED + pr.SCREENING_OPTIONAL
QUEUE_COLUMNS = ["paper_id", "stage", "reasons", "screeners"]


class PilotAgreementError(ValueError):
    """Inputs are inconsistent; nothing is computed or written."""


def cohen_kappa(a, b):
    """Cohen's kappa for two equal-length label sequences; None when undefined (chance agreement 1)."""
    if not a or len(a) != len(b):
        raise PilotAgreementError("kappa needs two non-empty sequences of equal length")
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in set(ca) | set(cb))
    if pe == 1:
        return None
    return (po - pe) / (1 - pe)


def pilot_rows(rows, label):
    """{paper_id: row} for one screener's pilot file: title/abstract rows only, one per paper_id."""
    out = {}
    for r in rows:
        if r["stage"] != "title_abstract":
            raise PilotAgreementError(f"{label}: {r['paper_id']} is not a title_abstract row")
        if r["decision"] not in DECISION_LEVELS:
            raise PilotAgreementError(f"{label}: {r['paper_id']} decision {r['decision']!r} is not a pilot decision")
        if r["paper_id"] in out:
            raise PilotAgreementError(f"{label}: {r['paper_id']} has more than one pilot row")
        out[r["paper_id"]] = r
    return out


def _value(row, key):
    v = row.get(key, "") or ""
    return frozenset(t for t in v.split(";") if t) if key in SET_VALUED else v


def _pid_key(p):
    return int(p[1:])


def adjudicated_decisions(adjudication_rows, pilot_ids):
    """{paper_id: agreed decision} from adjudication rows (M5). Every row must be a pilot record's
    `title_abstract` row by `screener=researcher` with a pilot decision; otherwise nothing is
    computed. The latest row per paper (append-only order) is the agreed decision."""
    agreed, problems = {}, []
    for r in adjudication_rows:
        pid = r.get("paper_id", "")
        if pid not in pilot_ids:
            problems.append(f"{pid or '?'}: not a pilot record")
        elif r.get("stage") != "title_abstract":
            problems.append(f"{pid}: stage {r.get('stage')!r} (expected title_abstract)")
        elif r.get("screener") != "researcher":
            problems.append(f"{pid}: screener {r.get('screener')!r} (adjudication needs screener=researcher)")
        elif r.get("decision") not in DECISION_LEVELS:
            problems.append(f"{pid}: decision {r.get('decision')!r} is not a pilot decision")
        else:
            agreed[pid] = r["decision"]
    if problems:
        raise PilotAgreementError("invalid adjudication rows: " + "; ".join(problems))
    return agreed


def agreement(assistant_rows, researcher_rows, sample_ids=None, adjudication_rows=()):
    """Agreement metrics and the D-025 pass evaluation for the two pilot files."""
    a, r = pilot_rows(assistant_rows, "assistant"), pilot_rows(researcher_rows, "researcher")
    if set(a) != set(r):
        raise PilotAgreementError(f"the two files cover different records: only assistant "
                                  f"{sorted(set(a) - set(r))}, only researcher {sorted(set(r) - set(a))}")
    if sample_ids is not None and set(a) != set(sample_ids):
        raise PilotAgreementError("the decision files do not cover exactly the pilot sample")
    ids = sorted(a, key=_pid_key)
    n = len(ids)
    da, dr = [a[p]["decision"] for p in ids], [r[p]["decision"] for p in ids]
    ba, br = [d == "include" for d in da], [d == "include" for d in dr]
    kappa3 = cohen_kappa(da, dr)
    conflicts = [p for p in ids if {a[p]["decision"], r[p]["decision"]} == {"include", "exclude"}]
    agreed = adjudicated_decisions(adjudication_rows, set(ids))
    unresolved = [p for p in conflicts if agreed.get(p) != "exclude"]   # D-025: agreement on the exclusion
    both_excl = [p for p in ids if a[p]["decision"] == r[p]["decision"] == "exclude"]
    code_agree = sum(a[p]["reason_code"] == r[p]["reason_code"] for p in both_excl)

    def code(row):
        return row["reason_code"] if row["decision"] == "exclude" else ""

    per_code = {c: sum((code(a[p]) == c) != (code(r[p]) == c) for p in ids) for c in EXCLUSION_CODES}
    per_code = {c: k for c, k in per_code.items() if k}
    descriptors = {}
    both_desc = [p for p in ids if a[p]["decision"] in ("include", "uncertain")
                 and r[p]["decision"] in ("include", "uncertain")]
    for d in DESCRIPTORS:
        same = sum(_value(a[p], d) == _value(r[p], d) for p in both_desc)
        descriptors[d] = {"n": len(both_desc), "agree": same,
                          "percent": None if not both_desc else round(100 * same / len(both_desc), 1)}
    max_code = max(per_code.values(), default=0)
    if kappa3 is None:
        passed = None      # kappa undefined: reported, not decided (Q-091)
    else:
        passed = kappa3 >= KAPPA_THRESHOLD and not unresolved and max_code <= MAX_CODE_DISAGREEMENTS
    return {
        "n": n,
        "three_level": {"percent_agreement": round(100 * sum(x == y for x, y in zip(da, dr)) / n, 1),
                        "kappa": None if kappa3 is None else round(kappa3, 4),
                        "assistant_counts": dict(collections.Counter(da)),
                        "researcher_counts": dict(collections.Counter(dr))},
        "include_vs_not": {"percent_agreement": round(100 * sum(x == y for x, y in zip(ba, br)) / n, 1),
                           "kappa": None if cohen_kappa(ba, br) is None else round(cohen_kappa(ba, br), 4)},
        "primary_code": {"both_exclude": len(both_excl), "same_code": code_agree},
        "disagreements_per_code": per_code,
        "include_exclude_conflicts": conflicts,
        "unresolved_conflicts": unresolved,
        "adjudicated_decisions": {p: agreed[p] for p in conflicts if p in agreed},
        "descriptor_agreement": descriptors,
        "disagreement_ids": [p for p in ids if a[p]["decision"] != r[p]["decision"]
                             or code(a[p]) != code(r[p])],
        "pass": passed,
        "pass_rule": {"kappa_threshold": KAPPA_THRESHOLD, "max_disagreements_per_code": MAX_CODE_DISAGREEMENTS,
                      "per_code_definition": "records where exactly one screener's primary exclusion code is the "
                                             "code (D-098, provisional)",
                      "conflict_resolution": "an adjudication row by the researcher agreeing on the exclusion "
                                             "(D-025; D-098 (b), provisional)"},
    }


def report_markdown(result):
    """Metrics section for pilot_report.md (IDs, codes and counts only)."""
    t, b = result["three_level"], result["include_vs_not"]
    lines = ["## Pilot agreement (computed by scripts/literature/pilot_agreement.py)", "",
             f"- Records: {result['n']}",
             f"- Three-level decision: {t['percent_agreement']} % agreement; Cohen's kappa "
             f"{'undefined' if t['kappa'] is None else t['kappa']}",
             f"- Include vs not include: {b['percent_agreement']} % agreement; Cohen's kappa "
             f"{'undefined' if b['kappa'] is None else b['kappa']}",
             f"- Primary code: {result['primary_code']['same_code']} of {result['primary_code']['both_exclude']} "
             "records excluded by both screeners have the same code",
             f"- Disagreements per code: {result['disagreements_per_code'] or 'none'}",
             f"- Include/exclude conflicts: {result['include_exclude_conflicts'] or 'none'}; unresolved: "
             f"{result['unresolved_conflicts'] or 'none'}", "",
             "| Descriptor | Records (both include/uncertain) | Agree | % |", "|---|---|---|---|"]
    for d, v in result["descriptor_agreement"].items():
        lines.append(f"| `{d}` | {v['n']} | {v['agree']} | {'—' if v['percent'] is None else v['percent']} |")
    verdict = {True: "PASSED", False: "NOT PASSED", None: "UNDETERMINED (kappa undefined; researcher decision)"}
    lines += ["", f"**D-025 pass evaluation: {verdict[result['pass']]}** (kappa >= {KAPPA_THRESHOLD}; no unresolved "
              f"include/exclude conflict; at most {MAX_CODE_DISAGREEMENTS} disagreements on any single code), evaluated "
              "with the operational definitions of D-098 (provisional; not final). The pilot result is decided "
              "by the researcher; this computation does not approve it.", ""]
    return "\n".join(lines)


def make_template(sample_ids, criteria_version, screener="researcher"):
    if len(sample_ids) != len(set(sample_ids)):
        raise PilotAgreementError("duplicate paper_id in the sample")
    if not pr.CRITERIA_VERSION_FORMAT.fullmatch(criteria_version or ""):
        raise PilotAgreementError(f"malformed criteria_version {criteria_version!r}")
    rows = []
    for pid in sorted(sample_ids, key=_pid_key):
        row = {c: "" for c in TEMPLATE_COLUMNS}
        row.update({"paper_id": pid, "stage": "title_abstract", "screener": screener,
                    "criteria_version": criteria_version})
        rows.append(row)
    return rows


def build_adjudication_queue(decisions_by_screener, dedup_pairs=()):
    """Queue rows (QUEUE_COLUMNS). decisions_by_screener: {label: [validated rows]}; the latest row per
    (paper_id, stage) of each screener is used (append-only files)."""
    latest = {}
    for label, rows in decisions_by_screener.items():
        for r in rows:
            latest[(label, r["paper_id"], r["stage"])] = r
    queue = collections.defaultdict(lambda: {"reasons": set(), "screeners": set()})
    for (label, pid, stage), r in latest.items():
        reasons = []
        if r["decision"] == "uncertain":
            reasons.append("uncertain")
        if r["decision"] == "exclude" and r["reason_code"] == "E12":
            reasons.append("E12")
        if (r.get("needs_human") or "") == "yes":
            reasons.append("needs_human")
        for reason in reasons:
            queue[(pid, stage)]["reasons"].add(reason)
            queue[(pid, stage)]["screeners"].add(label)
    labels = list(decisions_by_screener)
    if len(labels) == 2:
        x, y = labels
        for (label, pid, stage), r in latest.items():
            other = latest.get((y, pid, stage)) if label == x else None
            if other is None:
                continue
            code_r = r["reason_code"] if r["decision"] == "exclude" else ""
            code_o = other["reason_code"] if other["decision"] == "exclude" else ""
            if r["decision"] != other["decision"] or code_r != code_o:
                queue[(pid, stage)]["reasons"].add("pilot_disagreement")
                queue[(pid, stage)]["screeners"].update(labels)
    stages_of = collections.defaultdict(set)
    for (_, pid, stage) in latest:
        stages_of[pid].add(stage)
    for a_id, b_id in dedup_pairs:                 # L3: every pair (protocol v0.2 §5 item 4)
        for pid, other in ((a_id, b_id), (b_id, a_id)):
            for stage in sorted(stages_of.get(pid) or {""}):    # "" = no decision yet
                queue[(pid, stage)]["reasons"].add(f"possible_duplicate_with:{other}")
    return [{"paper_id": pid, "stage": stage, "reasons": ";".join(sorted(v["reasons"])),
             "screeners": ";".join(sorted(v["screeners"]))}
            for (pid, stage), v in sorted(queue.items(), key=lambda kv: (_pid_key(kv[0][0]), kv[0][1]))]


def _write_csv(path, columns, rows):
    path = Path(path)
    if path.exists():
        raise SystemExit(f"refused: {path} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction="raise")
        w.writeheader()
        w.writerows(rows)


def _read_dedup(path):
    with open(path, newline="", encoding="utf-8") as f:
        return [(r["paper_id_a"], r["paper_id_b"]) for r in csv.DictReader(f)]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("template", help="write the researcher decision template")
    t.add_argument("--sample", required=True, help="pilot_sample.csv")
    t.add_argument("--criteria-version", required=True)
    t.add_argument("--out", required=True)
    r = sub.add_parser("report", help="compute pilot agreement")
    r.add_argument("--lit-dir", required=True)
    r.add_argument("--assistant", required=True)
    r.add_argument("--researcher", required=True)
    r.add_argument("--sample", help="pilot_sample.csv (checks coverage)")
    r.add_argument("--adjudication", help="decision rows recording adjudicated agreement")
    r.add_argument("--out", help="write the Markdown metrics section here")
    q = sub.add_parser("queue", help="build the adjudication queue")
    q.add_argument("--lit-dir", required=True)
    q.add_argument("--decisions", nargs="+", required=True, help="label=path, e.g. assistant=a.csv")
    q.add_argument("--dedup", help="records/dedup_review.csv")
    q.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "template":
            with open(a.sample, newline="", encoding="utf-8") as f:
                ids = [row["paper_id"] for row in csv.DictReader(f)]
            _write_csv(a.out, TEMPLATE_COLUMNS, make_template(ids, a.criteria_version))
            print(f"wrote {a.out} ({len(ids)} rows)")
        elif a.cmd == "report":
            lit = Path(a.lit_dir)
            sample = None
            if a.sample:
                with open(a.sample, newline="", encoding="utf-8") as f:
                    sample = [row["paper_id"] for row in csv.DictReader(f)]
            adjudication = pr.load_screening_decisions(lit, path=a.adjudication) if a.adjudication else []
            res = agreement(pr.load_screening_decisions(lit, path=a.assistant),
                            pr.load_screening_decisions(lit, path=a.researcher), sample, adjudication)
            if a.out:
                out = Path(a.out)
                if out.exists():
                    raise SystemExit(f"refused: {out} already exists")
                out.write_text(report_markdown(res), encoding="utf-8")
            print(json.dumps(res, indent=1, default=sorted))
        else:
            lit = Path(a.lit_dir)
            sets = {}
            for spec in a.decisions:
                label, _, path = spec.partition("=")
                if not label or not path or label in sets:
                    raise PilotAgreementError(f"--decisions entries must be distinct label=path ({spec!r})")
                sets[label] = pr.load_screening_decisions(lit, path=path)
            rows = build_adjudication_queue(sets, _read_dedup(a.dedup) if a.dedup else ())
            _write_csv(a.out, QUEUE_COLUMNS, rows)
            print(f"wrote {a.out} ({len(rows)} rows)")
    except PilotAgreementError as e:
        raise SystemExit(f"refused: {e}") from None
    return 0


if __name__ == "__main__":
    sys.exit(main())
