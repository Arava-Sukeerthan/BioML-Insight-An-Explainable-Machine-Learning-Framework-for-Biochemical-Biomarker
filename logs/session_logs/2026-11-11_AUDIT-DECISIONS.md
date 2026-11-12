# Session log — 2026-11-11 — AUDIT-DECISIONS

**Prompts**:
- "I have reviewed the final consistency and governance audit dated 2026-11-11" (decisions A1, A2, A3, B1, B2);
- "We have reviewed the latest audit verification report, proposed_changes.py and A3_D-102_revision_design.md" (corrections and design work);
- "Researcher instructions — BioML-Insight governance update (2026-11-11)": apply `proposed_changes_v2.py --with-q063`; keep D-108 PROPOSED; R1 selected as primary design, R2 as fallback; prepare the D-102 (R1) wording for review; Q-063 stays Open.

**Not authorised and not done**:
- commit, push, merge, staging;
- freeze; registry; fixed-inventory entry; activation-condition rows; run authorisations;
- Stage 0; pilot draw; researcher sheet; real screening;
- custodian appointment; keys; encryption; blinding tools.

## State
- **Start:** HEAD `c6e1b14` (local, 1 commit ahead of the remote); uncommitted B1–B6 work (9 modified files, 1 new); nothing staged.
- **End:** HEAD unchanged; the B1–B6 work preserved; the changes below added; nothing staged.

## A2 verification (2026-11-11; read-only: hashing and Git history; no record read or screened)
- **(i) Verified:** `research/literature/paper_inventory.json`, 7,415,048 bytes, SHA-256 `b668dbde42473baa49ac1f02f89f900e94e39159c82efb8175ba125fef06d054`.
  - Identical from five methods: `sha256sum`, Python `hashlib`, `openssl dgst -sha256`, `git show HEAD:<path>`, `git show bf0c579:<path>`.
  - Git blob `59e087e923527b87508068487b58a3dac382e59c` at both commits.
  - Last changed in `bf0c579` (2026-11-01, T2 rebuild); unchanged since; the working copy equals HEAD.
  - The T2 session log records the same SHA-256.
  - The CSV twin `paper_inventory.csv` is `00062fed6d7aad189af86e4e489488db45d347f5426acf0f393695f406a194ef`, as recorded in `collection_stats.json`.
- **(ii) Observed only** (local workspace, 2026-11-11):
  - `records/publications.jsonl`: `0141d5d8734ef9e5fd30c3add62ec468f3b088edc79ec3062f8b3acd9b9dd192`;
  - `records/source_records.jsonl`: `78eba1d36cc791a9cb4bc9b9cc07b8512d5e12945630c4f9b7d29bfd2d379460`.
- **(iii) Provenance of (ii) incomplete.** No committed record gives their SHA-256 after the T2 rebuild. The T2 log states only that `publications.jsonl` changed and `source_records.jsonl` did not. The observed values are not verified build hashes.

## Application of `proposed_changes_v2.py --with-q063`
- **Pre-checks:**
  - each replacement target was found exactly once (criteria §4 bullet; §11 step 5 tail; §9 anchor row; the decision-log anchor row);
  - the decision log ended with a newline;
  - exactly one Q-063 row, with "Needed by" `2026-10-31`;
  - D-105 to D-109 unused.
- **Rollback:** the three target files were copied outside the repository with their SHA-256 values, and the script ran with automatic restore on failure. It applied cleanly; no restore was needed.
- **Line counts** (against the pre-application copies):

  | File | Added | Removed |
  |---|---|---|
  | criteria v1.1 | 4 | 2 |
  | register (Q-063 row only) | 1 | 1 |
  | decision log | 21 | 0 |

- **Afterwards**, as record-keeping of the researcher's decisions in the same prompt, three status-history rows:
  - D-106: the Q-063 wording was applied; Q-063 is still Open;
  - D-109: R1 selected, R2 fallback, design only;
  - D-108: kept PROPOSED.
- CHANGELOG, PROMPT_LOG and the daily review log were appended.

## Prepared for review (outside the repository; not applied)
- the D-102 (R1) revision text;
- A3 v2 (R1/R2 comparison);
- the freeze-readiness checklist.

## Verification
The actual test outcomes are in the task report of this prompt.
