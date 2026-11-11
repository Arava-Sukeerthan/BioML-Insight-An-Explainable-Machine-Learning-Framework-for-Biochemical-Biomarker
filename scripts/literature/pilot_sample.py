#!/usr/bin/env python3
"""Pilot sampler (Phase 1 implementation; researcher authorisation 2026-11-01).

Implements the approved pilot draw without changing any parameter (C1):
* D-025 / D-063: 60 records, seed 4004; frame = the 1,470 D-044 records minus Stage-0 records
  (1,463 after D-074, D-063 F1 status-history row); strata by the rarest-theme rule in the order
  F, D, C, E, A, Q, B, no theme -> `untagged`; allocation F 8, D 7, C 7, E 7, A 8, Q 7, B 8,
  untagged 8.
* D-077 (1)-(5): one `random.Random(4004)` for the whole draw; strata drawn in the order F, D, C,
  E, A, Q, B, untagged; within a stratum the `paper_id`s are taken in ascending order and one key
  `rng.random()` is drawn per `paper_id`; the k records with the smallest (key, paper_id) pairs are
  selected; the inventory SHA-256 and the script are recorded in `pilot_sample.csv`.
Approved Phase 1 defaults: C2 a JSON sidecar holds the script identity and run metadata; C3 the
draw stops unless the recomputed frame and stratum counts equal the F1 record exactly; C4 the frame
is not changed for unresolved duplicate pairs, whose members are reported if drawn.

Drawing the real sample needs, separately: the freeze, the D-035 record §6 conditions and the
D-077 (6) authorisation. The command-line entry point refuses to run without a registered frozen
version and an authorisation verified against DECISION_LOG.md.

Phase 1 corrections (researcher authorisation 2026-11-11): the frame uses the shared checked Stage-0
guards (stage0.check_types: A1 union guard, A2 unsupported-variant stop), so an unsupported type is
never silently treated as an ordinary record; the run authorisation is verified; the sidecar records
the SHA-256 of publications.jsonl and source_records.jsonl.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pubrecords as pr  # noqa: E402
import stage0  # noqa: E402

SAMPLE_SIZE = 60
SEED = 4004
STRATUM_ORDER = ("F", "D", "C", "E", "A", "Q", "B", "untagged")
RAREST_THEME_ORDER = ("F", "D", "C", "E", "A", "Q", "B")
ALLOCATION = {"F": 8, "D": 7, "C": 7, "E": 7, "A": 8, "Q": 7, "B": 8, "untagged": 8}
APPROVED_FRAME_SIZE = 1463
APPROVED_STRATUM_SIZES = {"B": 623, "A": 365, "untagged": 173, "F": 120, "C": 93, "E": 68, "D": 13, "Q": 8}
SAMPLE_COLUMNS = ["paper_id", "stratum", "seed", "inventory_sha256", "sampling_script"]
SCRIPT_RELPATH = "scripts/literature/pilot_sample.py"
assert sum(ALLOCATION.values()) == SAMPLE_SIZE


class PilotSampleError(ValueError):
    """Stop condition; nothing is drawn or written."""


def stratum_of(themes):
    present = set(stage0.split_types(themes))
    for t in RAREST_THEME_ORDER:
        if t in present:
            return t
    return "untagged"


def build_frame(records, member_union_types):
    """Return {stratum: [paper_id, ...]} for D-044 scope records that are not Stage-0 records.
    The shared checked guards run first (stage0.check_types); any stop condition raises
    PilotSampleError and nothing is drawn."""
    try:
        stage0.check_types(records, member_union_types)
    except stage0.Stage0Error as e:
        raise PilotSampleError(f"Stage-0 guard: {e}") from None
    frame = {s: [] for s in STRATUM_ORDER}
    for r in records:
        if not stage0.in_d044_scope(r):
            continue
        if stage0.checked_classify(r) is not None:
            continue
        frame[stratum_of(r.get("retrieval_themes"))].append(r["paper_id"])
    return frame


def verify_frame(frame, expected_size=APPROVED_FRAME_SIZE, expected_strata=None):
    """C3: stop unless the frame and every stratum size equal the approved record exactly."""
    expected_strata = APPROVED_STRATUM_SIZES if expected_strata is None else expected_strata
    sizes = {s: len(v) for s, v in frame.items()}
    total = sum(sizes.values())
    diffs = {s: (sizes.get(s, 0), n) for s, n in expected_strata.items() if sizes.get(s, 0) != n}
    if total != expected_size or diffs:
        raise PilotSampleError(f"frame mismatch: total {total} (expected {expected_size}); "
                               f"strata (found, expected): {diffs}")
    return sizes


def draw(frame, allocation=None, seed=SEED):
    """D-077 random-key selection. Returns [(paper_id, stratum)] in stratum order, ids ascending."""
    allocation = ALLOCATION if allocation is None else allocation
    rng = random.Random(seed)                       # (1) one generator for the whole draw
    selected = []
    for s in STRATUM_ORDER:                         # (2) fixed stratum order
        k = allocation.get(s, 0)
        ids = sorted(frame.get(s, []), key=lambda p: int(p[1:]))   # (3) ascending paper_id
        if k > len(ids):
            raise PilotSampleError(f"stratum {s}: allocation {k} exceeds {len(ids)} records")
        keyed = [(rng.random(), pid) for pid in ids]                 # (3) one key per paper_id
        chosen = sorted(keyed)[:k]                                   # (4) k smallest (key, paper_id)
        selected += sorted(((pid, s) for _, pid in chosen), key=lambda x: int(x[0][1:]))
    return selected


def duplicate_pairs_in_sample(selected_ids, pairs):
    """C4: report unresolved possible-duplicate pairs with at least one drawn member (no removal)."""
    sel = set(selected_ids)
    out = []
    for a, b in pairs:
        hit = sorted({a, b} & sel)
        if hit:
            out.append({"paper_id_a": a, "paper_id_b": b, "drawn": hit})
    return out


def sample_rows(selected, inventory_sha256):
    return [{"paper_id": pid, "stratum": s, "seed": str(SEED), "inventory_sha256": inventory_sha256,
             "sampling_script": SCRIPT_RELPATH} for pid, s in selected]


def sidecar(selected, inventory_sha256, authorization, frame_sizes, dup_report, script_commit, script_sha256,
            run_time, input_hashes=None):
    """C2: script identity and run metadata (sidecar to pilot_sample.csv)."""
    return {"sampling_script": SCRIPT_RELPATH, "script_commit": script_commit, "script_sha256": script_sha256,
            **(input_hashes or {}),
            "run_time_utc": run_time, "authorization": authorization, "inventory_sha256": inventory_sha256,
            "seed": SEED, "sample_size": len(selected), "allocation": ALLOCATION, "frame_size": sum(frame_sizes.values()),
            "stratum_sizes": frame_sizes, "method": "D-077 random-key selection",
            "duplicate_pairs_in_sample": dup_report}


def read_dedup_pairs(path):
    if not Path(path).exists():
        raise PilotSampleError(f"{path} not found")
    with open(path, newline="", encoding="utf-8") as f:
        return [(r["paper_id_a"], r["paper_id_b"]) for r in csv.DictReader(f)]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lit-dir", required=True)
    ap.add_argument("--authorization", required=True, help="DECISION_LOG ID recording the D-077 (6) authorisation")
    ap.add_argument("--expected-inventory-sha256", required=True)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    lit = Path(a.lit_dir)
    try:
        auth = pr.verify_run_authorisation(lit, a.authorization, "D-077 (6)")
    except pr.RunAuthorisationError as e:
        raise SystemExit(str(e)) from None
    if not pr.load_criteria_registry(lit):
        raise SystemExit("refused: no registered frozen criteria version (freeze required)")
    records = stage0.load_inventory(lit, a.expected_inventory_sha256)
    union, input_hashes = stage0.load_member_union(lit)
    frame = build_frame(records, union)
    sizes = verify_frame(frame)
    selected = draw(frame)
    dups = duplicate_pairs_in_sample([p for p, _ in selected], read_dedup_pairs(lit / "records" / "dedup_review.csv"))
    script = Path(__file__).resolve()
    commit = subprocess.run(["git", "-C", str(script.parent), "rev-parse", "HEAD"], capture_output=True,
                            text=True).stdout.strip()
    meta = sidecar(selected, a.expected_inventory_sha256, auth, sizes, dups, commit,
                   hashlib.sha256(script.read_bytes()).hexdigest(),
                   dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), input_hashes)
    if a.write:
        out = lit / "screening" / "pilot_sample.csv"
        side = out.with_suffix(".provenance.json")
        if out.exists() or side.exists():
            raise SystemExit(f"refused: {out} or its sidecar already exists (append-only audit trail)")
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=SAMPLE_COLUMNS)
            w.writeheader()
            w.writerows(sample_rows(selected, a.expected_inventory_sha256))
        side.write_text(json.dumps(meta, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: meta[k] for k in ("sample_size", "frame_size", "duplicate_pairs_in_sample")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
