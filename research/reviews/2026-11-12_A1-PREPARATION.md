# A1 preparation (2026-11-12, after A5; nothing in A1 approved or recorded)

> **Not done:** no decision-log change; no Stage-0 run in the repository; no Git operation; no pilot; no data.
>
> **State checked:**
> - branch `claude/eloquent-mccarthy-bqtxr3-part1` at `2246ca7`, equal to the remote ref (`git ls-remote`);
> - working tree clean before this file was created.
>
> **Labels:**
> - **[CONFIRMED-R]** confirmed by the researcher in the prompt of 2026-11-12;
> - **[V]** verified by command today;
> - **[PENDING]** awaiting the researcher.

## 1. Researcher responses received (to be quoted in the A1 records)
| # | Response (researcher prompt, 2026-11-12, after A5) | Status | Where it goes once A1 is approved |
|---|---|---|---|
| R-a | "The original WhatsApp approval date, wording and approver cannot genuinely be supplied." | **[CONFIRMED-R]** | The Q-063 answer (either wording) records them as "not available", and the D-114 to D-121 status-history quotation. Q-063 in `unresolved_questions.md` is closed only when the wording is chosen |
| R-b | "Conditions 1, 2 and 4 may be treated as 'met at decision level', acknowledging their conditional approval status." | **[CONFIRMED-R]** | D-115 (row 1: D-036), D-116 (row 2: D-055 and D-061) and D-118 (row 4: D-060 as amended by D-068). The proposed status-history wording: "recorded as met at decision level; the underlying decisions remain APPROVED — CONDITIONAL until activation" |
| R-c | "The researcher is ready to authorise one Stage-0 run under the existing safeguards." | **[CONFIRMED-R] readiness in principle.** **Not** the run authorisation | Becomes D-121 only when you approve D-121 explicitly |

**Not yet received:**
- the Q-063 wording choice (§2);
- explicit approval of D-114 to D-121 (§3);
- explicit authorisation of the Stage-0 dry run, write, and dedicated commit and push (§4).

## 2. Q-063 — the two wordings (no selection inferred)
**(A) Alternative wording:**
> "Q-063: answered — preservation status 'off-device backup designated; integrity and privacy researcher-reported; not independently verified' (not PRESERVED). Archive integrity is verified in the container; the WhatsApp approval date, wording and approver are not available; conditions are not recorded. I accept this as sufficient to record the fixed-inventory entry, with the limitation stated."

**(B) PRESERVED wording** (originally drafted for A1):
> "Q-063: PRESERVED with recorded limitation (approval date, wording and approver not available; conditions none reported)."

**(B) also requires your dated written confirmation now** that:
- the Google Drive copies exist;
- they are private;
- they are intact.

These are **[R]** facts; the assistant cannot observe Drive.

**Difference:**
- (A) never uses "PRESERVED" and states that the backup is not independently verified. The manuscript discloses this.
- (B) uses "PRESERVED", resting on your written confirmation.
- D-114 to D-121 are identical under both.

## 3. D-114 to D-121 — exact entries (from `2026-11-12_CONSOLIDATED-APPROVAL-REQUEST.md` Appendix A; texts unchanged)
`<DATE>` and `<researcher prompt quotation>` are filled in at recording. **IDs D-114 to D-122 are unused** in `DECISION_LOG.md` **[V]**: there are 0 occurrences, and the last row is D-113.

| ID | Entry (exact) | Status column as drafted |
|---|---|---|
| D-114 | **Fixed inventory for Stage 0 and the pilot.** (i) `research/literature/paper_inventory.json` SHA-256 `b668dbde42473baa49ac1f02f89f900e94e39159c82efb8175ba125fef06d054`: verified (equal to the committed blob at HEAD and at `bf0c579`; five methods on 2026-11-11; re-hashed 2026-11-12). (ii) Observed on <DATE>: `records/publications.jsonl` `0141d5d8734ef9e5fd30c3add62ec468f3b088edc79ec3062f8b3acd9b9dd192`; `records/source_records.jsonl` `78eba1d36cc791a9cb4bc9b9cc07b8512d5e12945630c4f9b7d29bfd2d379460`. (iii) Provenance of (ii): "Consistent with the T2 build; not verified by a committed hash." (D-113). Raw exports 244/244 match `MANIFEST.csv` on <DATE>. A new entry is required if any of these hashes changes (D-108). At the draw the sidecar hashes must equal (ii), otherwise the pilot stops (D-113). Records no condition and authorises no run | APPROVED (governance decision) |
| D-115 | **D-035 §6 condition 1 recorded as met.** Q-039 answered by D-036 (classification status column `dim_classification`). Authorises no run | APPROVED (governance decision) |
| D-116 | **D-035 §6 condition 2 recorded as met.** Q-040 answered by D-055 (non-metabolic 3-of-5 frameworks retained with a flag; flag name D-061). Authorises no run | APPROVED (governance decision) |
| D-117 | **D-035 §6 condition 3 recorded as met.** D-027 and D-024 approved for screening as specified in D-111; D-027 part (b) and D-024's remaining extraction fields are excluded and must be resolved before full-text extraction. Authorises no run | APPROVED (governance decision) |
| D-118 | **D-035 §6 condition 4 recorded as met.** The remaining R5/D-029 items are decided by D-060 (as amended by D-068). Authorises no run | APPROVED (governance decision) |
| D-119 | **D-035 §6 condition 5 recorded as met.** Screening criteria v1.1 and protocol v0.2 frozen as `criteria_v1.1+protocol_v0.2` (freeze entry D-110, effective 2026-11-11); "`screening_criteria.md` v1.1" refers to `screening_criteria_v1.1.md` (D-081). Authorises no run | APPROVED (governance decision) |
| D-120 | **D-035 §6 condition 6 recorded as met.** Closed list of D-091: (a) Phase 1 and Stage B tools and the D-098 code committed and tested at `a0af2ad` (D-112; literature tests 365 OK); (b) the D-096 ignore rules in `.gitignore`; (c) the D-088 binding checks implemented (D-095) in the D-097 format; (d) the inventory hash fixed by D-114. Authorises no run | APPROVED (governance decision) |
| D-121 | **Run authorisation under D-074 (f).** criteria_version: criteria_v1.1+protocol_v0.2; inventory_sha256: b668dbde42473baa49ac1f02f89f900e94e39159c82efb8175ba125fef06d054; freeze_entry: D-110; d035_s6_records: D-115, D-116, D-117, D-118, D-119, D-120; single_use: yes; scope: one Stage-0 run by `scripts/literature/stage0.py` (D-085 A1–A5) on the fixed inventory D-114; the ledger and outputs are committed and pushed in one dedicated commit before any further run (D-099 (1)) | APPROVED — run authorisation (single use) |

**Re-verification today [V]:**
- `paper_inventory.json` = `b668dbde…d054`, equal to `HEAD:` blob;
- `publications.jsonl` = `0141d5d8…`; `source_records.jsonl` = `78eba1d3…`;
- `pubrecords.py verify`: "all raw exports match MANIFEST.csv".

**D-120 (a) note:** HEAD is now `2246ca7` (A5). Between `a0af2ad` and `2246ca7`, `scripts/literature/`, `tests/literature/` and `.gitignore` changed **only by additions**: 5 new tools and 5 new test files; no existing tool and no ignore rule changed **[V]**. The drafted text stays accurate, because it states a fact about `a0af2ad`. The literature suite is now 392 OK.
- *Optional clarifying clause, only if you want it:* "(unchanged at `2246ca7`; A5 added five tools and their tests; literature tests 392 OK)".
- The dry run accepted the text as drafted. No change is made without your instruction.

**Consequences:**
- Q-063 is closed with the chosen wording.
- The inventory is bound to `b668dbde…` (D-108: any change needs a new entry).
- All six D-035 §6 conditions are recorded as met. Rows 1, 2 and 4 are met **at decision level**; their underlying decisions remain conditionally approved.
- Screening becomes activatable.
- D-121 authorises **exactly one** Stage-0 write. It is consumed even if interrupted (D-099), and a further run needs a new row.

**Dependencies:**
- D-114 must precede D-120 (d) and D-121.
- D-115 to D-120 must precede D-121 (`d035_s6_records`).
- D-110 (freeze) and D-111 (condition 3) are already APPROVED.
- D-122 (pilot draw) is **not** part of A1; it needs A2 and a custodian.

**Recording format** (when approved):
1. the eight rows are inserted after D-113 with `<DATE>` = the approval date and the quotation from your approval prompt;
2. eight status-history rows of the form "| <DATE> | SCREENING-ACTIVATION | D-1nn (new) | Recorded as **APPROVED** … | Researcher (owner), <DATE> — <quotation> |";
3. Q-063 closed in `unresolved_questions.md` with the chosen wording;
4. `run_checks.sh`;
5. one commit of `logs/DECISION_LOG.md`, `research/reviews/unresolved_questions.md` and the logs, pushed normally (A1's "related commit and push").

## 4. Stage-0 readiness
| Requirement | State | Evidence |
|---|---|---|
| A5 commits on the remote | **Met** | `git ls-remote` = `2246ca7d…`; history `a0af2ad → 4262e1f (A5, 64 files) → 2246ca7 (hash record)`; tree clean |
| D-099 (3): ledger equals HEAD | **Met** (no ledger yet: "both absent" is accepted by `check_ledger_matches_head`) | Code read; `research/literature/screening/` does not exist |
| D-099 (4): hash chain | Implemented at `a0af2ad` (D-112) | Ledger entries carry `prev_sha256` |
| Ledger and outputs committable | **Met** | `screening/decisions.csv` and `screening/run_authorisation_ledger.jsonl` are **not** Git-ignored. Private sheets (`*_sheet_*.csv`, `pilot_sheet_researcher.csv`) are ignored |
| Inventory binding | **Met** | Hash equals D-114 and the D-121 binding |
| Frozen criteria/protocol | Unchanged | `8511be1b…`, `f6304198…` |
| Authorisation row D-121 | **Pending** (A1) | The real repository refuses today: "D-121 is not a decision in DECISION_LOG.md" (exit 1). **Fails closed, as required** |
| Dry run with the drafted rows | **Reproduced today** in a disposable copy at `2246ca7` (deleted; the repository untouched) | `in_scope 1470, E5 5, E7 2, not_stage0 1463, new_rows 7, written false`, exit 0; the jsonl hashes in the output equal D-114 (ii). A wrong inventory hash is refused (exit 1) |

**Scope and safeguards:**
- one run by `stage0.py` (D-085 A1–A5): publication-type exclusions only, on the fixed inventory;
- no pilot;
- no custodian step;
- no abstracts shared;
- no data.

**Exact commands** (run only after A1 is approved and recorded, and committed and pushed):
```bash
# 1. dry run — must print in_scope 1470, E5 5, E7 2, new_rows 7, written false; anything else: stop
python3 -I scripts/literature/stage0.py --lit-dir research/literature --authorization D-121 --expected-inventory-sha256 b668dbde42473baa49ac1f02f89f900e94e39159c82efb8175ba125fef06d054 --criteria-version criteria_v1.1+protocol_v0.2
# 2. write (single use; ledger "started" then "completed")
python3 -I scripts/literature/stage0.py --lit-dir research/literature --authorization D-121 --expected-inventory-sha256 b668dbde42473baa49ac1f02f89f900e94e39159c82efb8175ba125fef06d054 --criteria-version criteria_v1.1+protocol_v0.2 --write
# 3. checks, then the D-099 (1) dedicated commit: ledger + decisions.csv only
sh scripts/run_checks.sh
git add -- research/literature/screening/run_authorisation_ledger.jsonl research/literature/screening/decisions.csv
git diff --cached --name-only | wc -l    # must print 2
git commit -m "Stage-0 run under D-121 (D-099 (1))" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CgJ3gRgrYmk9tG8qm9hN8t"
git push -u origin claude/eloquent-mccarthy-bqtxr3-part1
# 4. D-099 (2): status-history row "D-121 used by stage0.py; ledger commit <hash>"; D-099 (5): ledger SHA-256 in the session log; commit + push normally
```

## 5. What the researcher must approve next (copyable; choose and edit)
> "A1. Q-063: <wording (A) | wording (B) with my confirmation of <date> that the Drive copies exist, are private and intact>. I approve D-114 to D-121 as in `2026-11-12_A1-PREPARATION.md` §3 <with | without> the optional D-120 clause, and authorise recording them with the related commit and push, one Stage-0 dry run and write under D-121, and the D-099 dedicated commit and push."
