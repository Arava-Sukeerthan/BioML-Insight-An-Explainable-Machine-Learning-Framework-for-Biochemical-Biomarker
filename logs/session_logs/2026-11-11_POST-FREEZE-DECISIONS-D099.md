# Session log — 2026-11-11 — POST-FREEZE-DECISIONS and D099-STEPS-3-4

**Prompts (2026-11-11)**:
1. "We have reviewed the post-freeze researcher decision brief": Q-085 option A; Q-096 yes; Q-097 option C with the sidecar stop rule; D-108 approved with one refinement; D-099 steps (3) and (4) implementation authorised; Q-063 to stay open.
2. "The D-099 steps (3) and (4) implementation has been completed in the working tree and verified successfully": records authorised.

**Not done**:
- fixed-inventory entry, condition rows, run authorisations;
- Stage 0, screening, sampling, extraction, pilot work;
- dataset download or inspection, model work;
- changes to the frozen texts;
- stage, commit, push or merge.

## D-099 steps (3) and (4)
**`scripts/literature/pubrecords.py`:**
- **`check_ledger_matches_head(lit_dir)`** (step 3): refuses unless `screening/run_authorisation_ledger.jsonl` equals its committed version at HEAD.
  - Accepted: no ledger in the working tree or at HEAD.
  - Refused: no Git repository; Git unavailable; no HEAD; untracked ledger; changed, staged-uncommitted or deleted committed ledger.
  - Called first in `record_authorisation_start`, so a refusal happens before any write. Local read-only Git commands only.
- **`_append_ledger`** writes `prev_sha256`, the SHA-256 of the ledger bytes before the entry. It refuses a caller-supplied value and an already broken chain.
- **`authorisation_uses`** recomputes the chain and refuses a missing `prev_sha256`, a broken link or a missing final newline. An edit of the final entry is caught by step (3).

**`tests/literature/test_phase1_screening_tools.py`:**
- `FixtureDir` now creates a temporary Git repository and has a `commit()` helper; `ledger_done` commits after each simulated run (D-099 (1)).
- `test_malformed_ledger_fails_closed` now builds chained lines and expects a case-specific message (strengthened: the repeated-event case again reaches the "inconsistent" check).
- New `LedgerPersistence`, 18 tests:
  - **step (3):** accepted (no ledger; committed ledger); refused (uncommitted change, untracked, staged-uncommitted, deleted, non-Git directory); an edited final entry is caught by HEAD; a real pilot draw refuses before writing any sample;
  - **step (4):** chain linkage; edited, deleted or reordered lines; missing `prev_sha256`; truncation; caller-supplied `prev_sha256`; append on a broken chain;
  - **real repository:** no real ledger.

**Results** (2026-11-11, 15:45:23Z–15:46:39Z): literature 365 OK; data protection 10 OK; NHANES 29 OK; query table PASS 168 rows; whitespace clean.

**Mutation checks** (the 18 new tests plus the strengthened malformed-ledger test):

| Mutation | Failing |
|---|---|
| None (baseline) | 0/19 |
| HEAD check removed | 7/19 |
| Pre-change chain reader | 7/19 |
| Pre-change writer (no `prev_sha256`) | 16/19 |
| Restored | 0/19 |

## Decisions recorded
- **D-111:** Q-085, option A.
- **D-112:** Q-096, yes.
- **D-113:** Q-097, option C, with the stop rule.
- **D-108:** status changed to APPROVED with the refinement.

**D-108 original status-cell text, preserved verbatim:**

> **PROPOSED** — remains PROPOSED until the researcher approves the exact amended order

**Original "Approved by" cell:**

> — (assistant proposal; awaiting the researcher)

History rows: D-111–D-113, D-108, D-093, D-107, D-099. Register: Q-085, Q-096 and Q-097 marked answered, with their earlier status text kept.

## Q-063 — kept open
Unfilled: the WhatsApp approval date, the approval wording, the approver identity and the researcher's PRESERVED decision. "None reported" (conditions) is unchanged. Nothing recorded.

## Integrity
- Frozen texts unchanged: criteria `8511be1b…a8d6`, protocol `f6304198…c8fb`.
- Research data and ignored records unchanged.
- No `research/literature/screening/` folder.
- Nothing staged or committed.
