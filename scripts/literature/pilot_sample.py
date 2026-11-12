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

Drawing the real sample needs, separately: the freeze, the D-035 record §6 conditions, the Stage-0
rows (written before the draw, D-093) and the D-077 (6) authorisation. The command-line entry point refuses to run without a registered frozen
version and an authorisation verified against DECISION_LOG.md.

Phase 1 corrections (researcher authorisation 2026-11-11): the frame uses the shared checked Stage-0
guards (stage0.check_types: A1 union guard, A2 unsupported-variant stop), so an unsupported type is
never silently treated as an ordinary record; the run authorisation is verified; the sidecar records
the SHA-256 of publications.jsonl and source_records.jsonl.

Stage B preparation (D-095, researcher authorisation 2026-11-11): the frame must also equal the
committed D-044 scope snapshot minus the seven approved Stage-0 records (identity, not only counts;
P17); `--frame-only` validates the frame without drawing or writing anything (P15); the D-077 (6)
authorisation must be complete, bound to the inventory used, and unused (P16; single-use ledger).

Pre-commit audit corrections (researcher authorisation 2026-11-11): before drawing, decisions.csv must
hold exactly the seven approved Stage-0 rows with their approved codes (M2, D-093); a --write run holds
the run lock, writes each output without ever overwriting (temporary file, then hard link), and
records "started" before and "completed" after its outputs (L5).
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import hashlib
import io
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
# P17 (Stage B preparation, D-095): frame identity. The frame must equal the committed D-044 scope
# snapshot (1,470 IDs; scope/D-044_scope_snapshot.md) minus the seven Stage-0 records of the
# F1-PILOT-FRAME status-history row of D-063 (P0028, P0099, P0113, P0624, P0830 -> E5; P0931, P0939
# -> E7). Counts alone are not enough.
SCOPE_SNAPSHOT_RELPATH = "scope/D-044_scope_paper_ids.csv"
APPROVED_SCOPE_SNAPSHOT_SHA256 = "a5d4851f764ad0843115740d85e8f6e2bed1596883bf11cc22c63fbf631253ea"
APPROVED_SCOPE_SIZE = 1470
APPROVED_STAGE0_CODES = {"P0028": "E5", "P0099": "E5", "P0113": "E5", "P0624": "E5", "P0830": "E5",
                         "P0931": "E7", "P0939": "E7"}
APPROVED_STAGE0_IDS = tuple(APPROVED_STAGE0_CODES)
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


def load_scope_snapshot(path, expected_sha256=APPROVED_SCOPE_SNAPSHOT_SHA256):
    """Paper IDs of the committed D-044 scope snapshot; the file must match its recorded SHA-256."""
    path = Path(path)
    if not path.exists():
        raise PilotSampleError(f"scope snapshot {path} not found")
    if expected_sha256 is not None and hashlib.sha256(path.read_bytes()).hexdigest() != expected_sha256:
        raise PilotSampleError(f"scope snapshot {path.name} does not match its recorded SHA-256")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "paper_id" not in (reader.fieldnames or []):
            raise PilotSampleError(f"scope snapshot {path.name} has no paper_id column")
        ids = [r["paper_id"] for r in reader]
    bad = [p for p in ids if not stage0._valid_id(p or "")]
    if bad:
        raise PilotSampleError(f"scope snapshot {path.name} has malformed paper_ids: {bad[:5]}")
    return ids


def _id_key(p):
    return int(p[1:])


def verify_frame_identity(frame, snapshot_ids, stage0_ids=APPROVED_STAGE0_IDS, expected_scope_size=APPROVED_SCOPE_SIZE):
    """P17: stop unless the frame's paper IDs equal the snapshot minus the approved Stage-0 IDs,
    with no ID duplicated in the frame or the snapshot. Returns the frame size."""
    flat = [p for s in frame for p in frame[s]]
    counts = collections.Counter(flat)
    dup = sorted((p for p, n in counts.items() if n > 1), key=_id_key)
    if dup:
        raise PilotSampleError(f"frame identity: paper_ids duplicated in the frame: {dup[:10]} ({len(dup)})")
    snap = list(snapshot_ids)
    snap_dup = sorted((p for p, n in collections.Counter(snap).items() if n > 1), key=_id_key)
    if snap_dup:
        raise PilotSampleError(f"frame identity: paper_ids duplicated in the scope snapshot: {snap_dup[:10]}")
    if expected_scope_size is not None and len(snap) != expected_scope_size:
        raise PilotSampleError(f"frame identity: scope snapshot has {len(snap)} IDs (expected {expected_scope_size})")
    s0 = set(stage0_ids)
    if s0 - set(snap):
        raise PilotSampleError(f"frame identity: Stage-0 IDs not in the scope snapshot: {sorted(s0 - set(snap))}")
    expected = set(snap) - s0
    missing = sorted(expected - counts.keys(), key=_id_key)
    extra = sorted(counts.keys() - expected, key=_id_key)
    if missing or extra:
        raise PilotSampleError(f"frame identity mismatch: missing {missing[:10]} ({len(missing)}); "
                               f"additional {extra[:10]} ({len(extra)})")
    return len(flat)


def verify_stage0_rows(decision_rows, stage0_codes=None):
    """M2 (D-093: Stage-0 rows are written before the pilot draw): stop unless decisions.csv holds
    exactly one `rule:stage0` title/abstract row for each approved Stage-0 record, each an `exclude`
    with the approved code, and no `rule:stage0` row for any other record."""
    stage0_codes = APPROVED_STAGE0_CODES if stage0_codes is None else stage0_codes
    rows = [r for r in decision_rows if r.get("screener") == "rule:stage0"]
    by_id = collections.defaultdict(list)
    for r in rows:
        by_id[r["paper_id"]].append(r)
    problems = []
    missing = sorted(set(stage0_codes) - set(by_id), key=_id_key)
    extra = sorted(set(by_id) - set(stage0_codes), key=_id_key)
    if missing:
        problems.append(f"missing Stage-0 rows for {missing}")
    if extra:
        problems.append(f"Stage-0 rows for records outside the approved list: {extra}")
    for pid, rs in sorted(by_id.items(), key=lambda kv: _id_key(kv[0])):
        if pid not in stage0_codes:
            continue
        if len(rs) != 1:
            problems.append(f"{pid}: {len(rs)} Stage-0 rows (expected 1)")
            continue
        r = rs[0]
        if (r["stage"], r["decision"], r["reason_code"]) != ("title_abstract", "exclude", stage0_codes[pid]):
            problems.append(f"{pid}: Stage-0 row is {r['stage']}/{r['decision']}/{r['reason_code']} "
                            f"(expected title_abstract/exclude/{stage0_codes[pid]})")
    if problems:
        raise PilotSampleError("Stage-0 rows do not match the approved exclusions (D-093): " + "; ".join(problems))
    return len(rows)


def frame_only(lit, expected_inventory_sha256):
    """P15: validate the sampling frame (count, strata and identity) without drawing or writing.
    Running it on the real inventory is a real-data operation and needs the researcher's explicit
    authorisation (governance; not enforced here because nothing is drawn or written)."""
    records = stage0.load_inventory(lit, expected_inventory_sha256)
    union, input_hashes = stage0.load_member_union(lit)
    try:
        frame = build_frame(records, union)
        snapshot = load_scope_snapshot(lit / SCOPE_SNAPSHOT_RELPATH, APPROVED_SCOPE_SNAPSHOT_SHA256)
        size = verify_frame_identity(frame, snapshot, APPROVED_STAGE0_IDS, APPROVED_SCOPE_SIZE)
        sizes = verify_frame(frame, APPROVED_FRAME_SIZE, APPROVED_STRATUM_SIZES)
    except PilotSampleError as e:
        raise SystemExit(f"frame check failed: {e}") from None
    return {"mode": "frame_only", "frame_valid": True, "frame_size": size, "stratum_sizes": sizes,
            "identity": "equals D-044 snapshot minus the approved Stage-0 IDs",
            "inventory_sha256": expected_inventory_sha256, **input_hashes,
            "drawn": False, "written": False}


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
    ap.add_argument("--authorization", help="DECISION_LOG ID recording the D-077 (6) authorisation (draw)")
    ap.add_argument("--expected-inventory-sha256", required=True)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--frame-only", action="store_true",
                    help="validate the frame only (P15): no draw, no output file, no authorisation consumed")
    a = ap.parse_args(argv)
    lit = Path(a.lit_dir)
    if a.frame_only:
        if a.write or a.authorization:
            ap.error("--frame-only takes neither --write nor --authorization")
        print(json.dumps(frame_only(lit, a.expected_inventory_sha256), indent=1))
        return 0
    if not a.authorization:
        ap.error("--authorization is required unless --frame-only is given")
    try:
        auth = pr.verify_run_authorisation(lit, a.authorization, "D-077 (6)",
                                           inventory_sha256=a.expected_inventory_sha256)
        if a.write:
            with pr.run_lock(lit):
                pr.check_authorisation_unused(lit, auth, "D-077 (6)", "pilot_sample")
                meta = _draw_run(lit, a, auth)
        else:
            meta = _draw_run(lit, a, auth)
    except pr.RunAuthorisationError as e:
        raise SystemExit(str(e)) from None
    print(json.dumps({k: meta[k] for k in ("sample_size", "frame_size", "duplicate_pairs_in_sample")}, indent=1))
    return 0


def _now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _draw_run(lit, a, auth):
    """The draw proper; for --write it runs inside the run lock (L5)."""
    if not pr.load_criteria_registry(lit):
        raise SystemExit("refused: no registered frozen criteria version (freeze required)")
    records = stage0.load_inventory(lit, a.expected_inventory_sha256)
    union, input_hashes = stage0.load_member_union(lit)
    frame = build_frame(records, union)
    snapshot = load_scope_snapshot(lit / SCOPE_SNAPSHOT_RELPATH, APPROVED_SCOPE_SNAPSHOT_SHA256)
    verify_frame_identity(frame, snapshot, APPROVED_STAGE0_IDS, APPROVED_SCOPE_SIZE)
    sizes = verify_frame(frame, APPROVED_FRAME_SIZE, APPROVED_STRATUM_SIZES)
    verify_stage0_rows(pr.load_screening_decisions(lit), APPROVED_STAGE0_CODES)
    selected = draw(frame)
    dups = duplicate_pairs_in_sample([p for p, _ in selected], read_dedup_pairs(lit / "records" / "dedup_review.csv"))
    script = Path(__file__).resolve()
    commit = subprocess.run(["git", "-C", str(script.parent), "rev-parse", "HEAD"], capture_output=True,
                            text=True).stdout.strip()
    meta = sidecar(selected, a.expected_inventory_sha256, auth, sizes, dups, commit,
                   hashlib.sha256(script.read_bytes()).hexdigest(), _now(), input_hashes)
    if a.write:
        out = lit / "screening" / "pilot_sample.csv"
        side = out.with_suffix(".provenance.json")
        if out.exists() or side.exists():
            raise SystemExit(f"refused: {out} or its sidecar already exists (append-only audit trail)")
        buf = io.StringIO(newline="")
        w = csv.DictWriter(buf, fieldnames=SAMPLE_COLUMNS, lineterminator="\r\n")
        w.writeheader()
        w.writerows(sample_rows(selected, a.expected_inventory_sha256))
        details = {"inventory_sha256": a.expected_inventory_sha256, "output": "screening/pilot_sample.csv"}
        pr.record_authorisation_start(lit, auth, "D-077 (6)", "pilot_sample", _now(), details)
        try:
            pr.write_new_file_atomically(out, buf.getvalue())
            pr.write_new_file_atomically(side, json.dumps(meta, indent=1) + "\n")
        except FileExistsError:
            raise SystemExit(f"refused: {out} or its sidecar appeared during the run; nothing was overwritten") from None
        pr.record_authorisation_completion(lit, auth, "D-077 (6)", "pilot_sample", _now(), details)
    return meta


if __name__ == "__main__":
    sys.exit(main())
