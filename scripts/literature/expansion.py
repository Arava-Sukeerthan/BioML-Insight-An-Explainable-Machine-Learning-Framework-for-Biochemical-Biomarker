"""Expansion screening support (screening protocol v0.2 §8): batch assignment and the D-008 audit sample.

Status: READY, NOT RUN. Expansion starts only after a passed pilot and the researcher's approval
(protocol v0.2 §8). The frozen texts fix "batches of about 300" and "25 include + 25 exclude"; they fix
neither the batch order nor the audit sampling method (audit timing is Q-084, open). Both are explicit
parameters here, so the seed and rule used are recorded in every output and can be fixed by decision:

  batches  -- the pilot frame (D-044 scope minus the approved Stage-0 IDs; pilot_sample.build_frame)
              minus the 60 pilot records, in a seeded pseudo-random order (SHA-256 of "<seed>:<paper_id>"),
              split into near-equal consecutive batches of at most --max-size (default 300).
              Output: paper_id, batch, order, seed. No titles, abstracts or decisions.
  audit    -- from VALIDATED decisions (pubrecords.load_screening_decisions), the latest title/abstract
              row per record in the given batches; Stage-0 rule rows excluded; a seeded sample of
              --n-include `include` and --n-exclude `exclude` records. Output: paper_id and order only
              (blinded: the decision is never written to the audit list). Refuses if a class has too
              few records.
Both refuse to overwrite an existing output (append-only audit trail).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pubrecords as pr  # noqa: E402

BATCH_COLUMNS = ["paper_id", "batch", "order", "seed"]
AUDIT_COLUMNS = ["paper_id", "order", "seed", "batches"]


class ExpansionError(ValueError):
    pass


def _key(seed, pid):
    return hashlib.sha256(f"{seed}:{pid}".encode()).hexdigest()


def assign_batches(frame_ids, pilot_ids, seed, max_size=300):
    frame_ids, pilot_ids = set(frame_ids), set(pilot_ids)
    if not pilot_ids <= frame_ids:
        raise ExpansionError("pilot records outside the frame: " + ", ".join(sorted(pilot_ids - frame_ids)[:5]))
    remaining = sorted(frame_ids - pilot_ids, key=lambda p: _key(seed, p))
    if not remaining:
        raise ExpansionError("no records remain after the pilot")
    k = math.ceil(len(remaining) / max_size)
    base, extra = divmod(len(remaining), k)
    rows, i = [], 0
    for b in range(1, k + 1):
        size = base + (1 if b <= extra else 0)
        for pid in remaining[i:i + size]:
            i += 1
            rows.append({"paper_id": pid, "batch": str(b), "order": str(i), "seed": str(seed)})
    return rows


def audit_sample(decision_rows, batch_rows, batches, seed, n_include=25, n_exclude=25):
    in_batches = {r["paper_id"] for r in batch_rows if int(r["batch"]) in set(batches)}
    if not in_batches:
        raise ExpansionError(f"no records in batches {sorted(batches)}")
    latest = {}
    for r in decision_rows:
        if r["stage"] == "title_abstract" and r["paper_id"] in in_batches:
            latest[r["paper_id"]] = r
    manual = [r for r in latest.values() if not pr.is_stage0_rule_row(r)]
    pools = {"include": sorted((r["paper_id"] for r in manual if r["decision"] == "include"), key=lambda p: _key(seed, p)),
             "exclude": sorted((r["paper_id"] for r in manual if r["decision"] == "exclude"), key=lambda p: _key(seed, p))}
    need = {"include": n_include, "exclude": n_exclude}
    short = {d: (len(pools[d]), need[d]) for d in pools if len(pools[d]) < need[d]}
    if short:
        raise ExpansionError(f"too few decisions for the audit sample (available, needed): {short}")
    chosen = pools["include"][:n_include] + pools["exclude"][:n_exclude]
    chosen.sort(key=lambda p: _key(f"{seed}:order", p))       # mix classes so the order reveals nothing
    tag = ";".join(str(b) for b in sorted(batches))
    return [{"paper_id": p, "order": str(i + 1), "seed": str(seed), "batches": tag} for i, p in enumerate(chosen)]


def _write_new(path, columns, rows):
    path = Path(path)
    if path.exists():
        raise ExpansionError(f"{path} already exists (append-only audit trail)")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def _read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("batches")
    b.add_argument("--lit-dir", required=True)
    b.add_argument("--expected-inventory-sha256", required=True)
    b.add_argument("--pilot-sample", required=True)
    b.add_argument("--seed", required=True)
    b.add_argument("--max-size", type=int, default=300)
    b.add_argument("--authorization", required=True, help="DECISION_LOG ID approving expansion (protocol v0.2 §8)")
    b.add_argument("--out", required=True)
    a_ = sub.add_parser("audit")
    a_.add_argument("--lit-dir", required=True)
    a_.add_argument("--batches-file", required=True)
    a_.add_argument("--batches", type=int, nargs="+", required=True)
    a_.add_argument("--seed", required=True)
    a_.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "batches":
            import pilot_sample as ps
            import stage0
            lit = Path(a.lit_dir)
            records = stage0.load_inventory(lit, a.expected_inventory_sha256)
            union, _ = stage0.load_member_union(lit)
            frame = ps.build_frame(records, union)
            ps.verify_frame_identity(frame, ps.load_scope_snapshot(lit / ps.SCOPE_SNAPSHOT_RELPATH),
                                     ps.APPROVED_STAGE0_IDS, ps.APPROVED_SCOPE_SIZE)
            ps.verify_frame(frame)                                  # sizes equal the approved record
            frame_ids = [pid for stratum in frame for pid in frame[stratum]]
            rows = assign_batches(frame_ids, [r["paper_id"] for r in _read(a.pilot_sample)], a.seed, a.max_size)
            _write_new(a.out, BATCH_COLUMNS, rows)
            print(f"wrote {a.out}: {len(rows)} records in {rows[-1]['batch']} batches (authorisation {a.authorization})")
        else:
            rows = audit_sample(pr.load_screening_decisions(Path(a.lit_dir)), _read(a.batches_file),
                                a.batches, a.seed)
            _write_new(a.out, AUDIT_COLUMNS, rows)
            print(f"wrote {a.out}: {len(rows)} records (decisions not included)")
    except (ExpansionError, ValueError) as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
