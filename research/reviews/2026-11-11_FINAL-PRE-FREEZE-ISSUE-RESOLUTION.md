# Final pre-freeze issue resolution and governance audit (2026-11-11)

> **Status of this report:** assistant audit for the researcher. **It approves nothing** (`CLAUDE.md` rule 7). It does not:
> - freeze anything, or record a freeze entry, criteria registry, fixed-inventory entry, D-035 §6 condition row or run authorisation;
> - change any decision status, close any question, or turn any proposal into a rule;
> - read, screen, sample or rebuild any research record.
>
> **Labels:** `[EVIDENCE]` means checked with a real command in this task; `[REPORTED]` means stated by the researcher and not observed by the assistant; `[HYPOTHESIS]`, `[RECOMMENDATION]` and `[OPEN]` follow `GOVERNANCE.md` §1.

## Section 1 — Executive summary
- **Both documents are ready for your content review.** Criteria v1.1 and protocol v0.2 are final drafts, not frozen and not in force. Every open question that either text refers to is listed in criteria §11 step 5.
- **The freeze is still blocked, but only by your own approvals.** These are:
  - content approval of both texts;
  - approval of the amended §11 procedure (D-084);
  - a decision on how D-107 stands at the freeze;
  - the freeze-entry ID and dates;
  - Git authorisation.
- **Activation and operation are not ready.** Q-085, Q-096 and Q-097 must be decided before activation. Before the first authorised run (Stage 0), steps (3) and (4) of D-099 must be implemented. Before the pilot, the D-102 revision, the D-096 extension and the custodian are needed.
- **Main new findings:**
  1. **Provenance (D-107, Q-097).** New evidence was found in the T2 session's own scratch files. They survive in this container but are not committed:
     - the current `source_records.jsonl` has the same SHA-256 as the pre-T2 backup, as hashed at 09:44 on 2026-11-01;
     - the current `publications.jsonl` has the same SHA-256 as the outputs of four earlier offline builds from the same raw exports;
     - its modification time falls inside the recorded T2 build window.

     This makes the link between the ignored files and the T2 rebuild strong. It is **still not verified**, because no hash of `publications.jsonl` was recorded at T2 and the scratch evidence is not durable. D-107 is assessed as **partially verified**.
  2. **The Google Drive backup holds the raw-export archives only** (LIT-003, LIT-005). No record shows a researcher-held copy of the two ignored record files. One of the Q-097 options ("comparison with a researcher-held copy") therefore has no copy to compare with on the present record.
  3. **The approval package gave the wrong timing for D-099 steps (3) and (4).** It placed them before the pilot draw. D-099 requires them "before the first authorised run", which is the Stage-0 run. Corrected.
  4. **D-108 is internally consistent, with no circular dependency.** However, it does not state:
     - that the D-102 revision and custodian must be in place before the D-077 (6) authorisation, which covers delivery of the researcher's sheet;
     - what happens if the inventory changes after the fixed-inventory entry;
     - that D-099 (3) and (4) precede the first authorisation.

     I recommend approving it with these three points added (Section 4).
  5. **Two historical status cells in criteria §9** showed out-of-date statuses without saying so. Annotated; the original text is kept.
  6. **The D-102 status cell is ambiguous.** It reads "effective at the v1.1 freeze (2026-11-11)", which could be read as a freeze date. No freeze has happened. A clarification is proposed and not applied, because decision-log status cells are not changed.
- **No researcher-owned decision was taken.** D-107 is still APPROVED IN PRINCIPLE — subject to verification. D-108 is still PROPOSED. The D-102 revision is still pending.

## Section 2 — Repository state `[EVIDENCE]` (2026-11-11, 13:53:59Z)
| Item | Value |
|---|---|
| Branch | `claude/eloquent-mccarthy-bqtxr3-part1` |
| HEAD | `c6e1b14c81821c0cddca26af1d0070829152999c` |
| Remote branch | `8d9bd79b923e4ed52d104c33c6766414240999b8`; local is 1 ahead, 0 behind; not pushed |
| Staged files | none (`git diff --cached --name-only` → 0) |
| Modified at the start of this task (uncommitted, earlier approved work) | `logs/CHANGELOG.md`, `logs/DECISION_LOG.md`, `logs/PROMPT_LOG.md`, the criteria v1.1 and protocol v0.2 texts, `research/reviews/daily_review_log.md`, `research/reviews/unresolved_questions.md`, `scripts/literature/pilot_agreement.py`, `tests/literature/test_phase1_screening_tools.py` |
| Untracked at the start | six 2026-11-11 session logs (AUDIT-DECISIONS, B1-B6-APPROVALS, D1-D2-APPLIED, FINAL-PRE-FREEZE-AUDIT, GOVERNANCE-REVIEW-FIXES, PRE-FREEZE-GOVERNANCE-REVIEW); `research/reviews/final_pre_freeze_approval_package_2026-11-11.md` |
| Files actually located | approval package: `research/reviews/final_pre_freeze_approval_package_2026-11-11.md`; governance review: `logs/session_logs/2026-11-11_PRE-FREEZE-GOVERNANCE-REVIEW.md` |
| Baseline | Copies of all changed and untracked files, and the full working-tree diff (900 lines), saved outside the repository before editing |

## Section 3 — D-107 provenance investigation

### 3.1 Evidence examined
- **Git history** of `paper_inventory.json` and the tracked `records/` files. The last change was `bf0c579` (2026-11-01 10:05, "T2 inventory rebuild").
- **T2 rebuild log** (`logs/session_logs/2026-11-01_T2-REBUILD.md`) and the T2 session's own working files in the session scratchpad (`t2/before_hashes.txt`, `t2/integrity.txt`, `t2/build.log`, `t2/backup/`).
- **Earlier offline builds** in the scratchpad, made by `run_pipeline.sh`: `pubrecords.build` with `today='2026-10-31'`, then `make_literature_reports.py`, offline on copies:
  - `defectfix/base` and `defectfix/new` (2026-10-31);
  - `nov4/reg/a` and `nov4/reg/b` (2026-11-01, before T2).
- **Git ignore status:** `.gitignore` lines 24–25 ignore both record files; the other six files in `records/` are tracked.
- **Raw exports:** `pubrecords.py --lit-dir research/literature verify` gives "OK: all raw exports match MANIFEST.csv" (exit 0; 244 manifest rows). `MANIFEST.csv` is tracked, unchanged from HEAD, with SHA-256 `c79c3abf…f996`, equal to its T2 pre-build value.
- **Backup documentation** (`research/literature/preservation/preservation_status.md`):
  - the Drive copies are the LIT-003 archive (`69e690f0…0c0e`) and the LIT-005 archive (`7b7d4674…6ea1`);
  - the container copies of the archives (`preservation/archive/`) are **not present** in this workspace.
- **Decision-log entries:** D-107, D-108, D-091 (d), D-088 (4), D-097 (a), D-010 and the Q-011-OPTION-B record.
- **Generation scripts:** `pubrecords.build` writes `records/publications.jsonl` and `records/source_records.jsonl`; `make_literature_reports.py` writes `paper_inventory.json` and `paper_inventory.csv`.
- **Not done:** no record content was read. Only file hashes, sizes, modification times and the tracked inventory's field names (to explain the scratch hashes) were examined.

### 3.2 Provenance evidence matrix
| Artifact | Historical hash | Current hash (2026-11-11) | Git tracking status | Evidence available | Verification status | Remaining gap |
|---|---|---|---|---|---|---|
| `paper_inventory.json` (3,386 records; D-044 scope 1,470; pilot frame 1,463) | `b668dbde42473baa49ac1f02f89f900e94e39159c82efb8175ba125fef06d054` (T2 log, committed) | same | Tracked; blob at `bf0c579` and HEAD | Five hashing methods (AUDIT-DECISIONS); committed blob; T2 log value; re-hashed this task | **Verified** | None for the hash. It is fixed only by a future fixed-inventory entry |
| `paper_inventory.csv` | `00062fed…a194ef` (T2 log; `collection_stats.json`) | not re-hashed this task (tracked, unchanged from HEAD) | Tracked | Committed value | Verified (committed) | — |
| `records/source_records.jsonl` | Pre-T2 `78eba1d3…9460` (`t2/before_hashes.txt`, 2026-11-01 09:44; scratch, uncommitted). The T2 log states it was byte-identical after the build | `78eba1d36cc791a9cb4bc9b9cc07b8512d5e12945630c4f9b7d29bfd2d379460` | Git-ignored | (i) T2 pre-build hash list (scratch); (ii) the T2 log's committed statement "byte-identical"; (iii) the T2 backup copy hashes to the same value; (iv) the four earlier offline builds hash to the same value | **Strongly supported; not verified by a committed hash** | The hash was never committed. The scratch evidence disappears with the container |
| `records/publications.jsonl` | Pre-T2 `5113350e…56fe` (scratch). **No post-T2 hash was recorded** | `0141d5d8734ef9e5fd30c3add62ec468f3b088edc79ec3062f8b3acd9b9dd192` | Git-ignored | (i) modification time 2026-11-01 09:50:15, inside the T2 build window 09:47:45–09:50:17 (T2 log); (ii) the four earlier offline builds from the same raw exports hash to the same value; their inventory differs from the committed one only by the retired `dim_independent_validation` column, which T2 removed in the reports script and not in `pubrecords.build`; (iii) the T2 log (committed) says only `publication_type` changed in this file, and the scratch `integrity.txt` confirms it | **Strongly supported; not verified** | No hash recorded at T2. Modification times can change. The scratch builds' raw inputs were not re-verified in this task |
| Raw exports (244 manifest files) | Per-file SHA-256 in tracked `MANIFEST.csv` | match (verify OK) | Ignored files, tracked manifest | `pubrecords.py verify` (exit 0); manifest unchanged since T2 | **Verified** in this workspace | — |
| LIT-003 / LIT-005 archives (Google Drive) | `69e690f0…0c0e` / `7b7d4674…6ea1` | not observable (no copy in the workspace) | Not in repository | Researcher reports that the Drive-copy hashes equal these values | **`[REPORTED]` only**; not independently verified | Approval details and PRESERVED status (Q-063). These archives contain raw exports, **not** the two ignored record files |

### 3.3 The five categories, kept apart
1. **Verified inventory hash:** `paper_inventory.json` `b668dbde…d054` `[EVIDENCE]`.
2. **Observed ignored-file hashes:** `publications.jsonl` `0141d5d8…d192` and `source_records.jsonl` `78eba1d3…9460` `[EVIDENCE: observed]`.
3. **User-reported backup agreement:** the Drive copies of the two raw-export archives match the recorded archive hashes `[REPORTED]`.
4. **Independently verified backup evidence:** none for the Drive copies. What is verified is that the raw exports in this workspace match `MANIFEST.csv` `[EVIDENCE]`.
5. **Unresolved provenance:** no committed record gives the post-T2 SHA-256 of either ignored file, and no backup copy of them is recorded `[OPEN]`.

### 3.4 Can existing evidence link the ignored files to the T2 rebuild? (F)
**Partly.**
- **`source_records.jsonl`:** the link holds if you accept the uncommitted T2 hash list as evidence. Its pre-T2 hash equals the current one, and the committed T2 log says the build left it unchanged.
- **`publications.jsonl`:**
  - What the evidence shows: the current file is the deterministic output of `pubrecords.build` on the current raw exports with the post-defect-fix code. Four independent builds gave the identical hash.
  - `[HYPOTHESIS]` T2 produced this same file, given the modification time and the T2 log's change summary.
  - What is missing: a hash recorded at T2.
- **What would close the gap** (each needs your decision under Q-097; none was done):
  - **(a)** An authorised offline rebuild into a scratch copy outside the repository, from the verified raw exports at a recorded code commit, comparing the output hashes with the observed values. No repository file is overwritten. `[RECOMMENDATION]` This is the smallest independent check.
  - **(b)** Accepting the scratch evidence above as sufficient, recorded with its limitation (uncommitted, ephemeral).
  - **(c)** Accepting the observed hashes with "provenance incomplete" as the stated status (D-108 (iii) already allows this wording).
  - Comparison with a researcher-held copy is possible only if you hold one. None is recorded.

### 3.5 Proposed resolution for Q-097 `[RECOMMENDATION]` (not applied)
> **Q-097 (proposed answer for the researcher's decision).** The fixed-inventory entry states:
> - (i) the verified SHA-256 of `paper_inventory.json`;
> - (ii) the observed SHA-256 of the two Git-ignored record files on the day of the entry;
> - (iii) their provenance as "consistent with the T2 build (scratch evidence: pre-build hash list and four reproducible offline builds); not verified by a committed hash";
> - optionally, the result of an authorised scratch rebuild (option (a)), if you authorise one.
>
> If the inventory, raw exports or code commit change after the entry, the entry no longer applies and a new entry is needed.

### 3.6 Assessment of D-107 (J)
| Requirement of D-107 | State |
|---|---|
| Exact inventory SHA-256 independently verified | **Met** (`b668dbde…`) |
| Recorded in a separate entry before condition 6 | **Not yet:** no entry exists (correctly) |
| Condition-6 row references that entry; both authorisations bind the same hash | Future steps |
| Provenance of the ignored files (D-107 (iii)) | **Unresolved:** strong but uncommitted evidence (above) |

**Overall: partially verified.** The status stays **APPROVED IN PRINCIPLE — subject to verification** until you decide. **Smallest safe next action:** your decision on Q-097, choosing (a), (b) or (c) in §3.4.

## Section 4 — D-108 sequence assessment
**References checked `[EVIDENCE]`:**
- criteria header and §0, and §11 steps 1 and 5;
- protocol header, §1, §10 row 5, §10 row 6 (d), and the §11 rows;
- decision log: the D-108 row, the D-093 and D-108 history rows, and the D-107 row;
- approval package: sections B, C, D, E, F and H;
- governance-review session log.

Every reference names D-108 as a proposal: "proposal", "proposed", "PROPOSED" or "not approved". **No wording treats it as an approved rule.**

**One overlap to note:** protocol §10 row 6 (d) states the fixed-inventory entry's content ("together with the observed SHA-256 and provenance status of the Git-ignored record files"). That content comes from D-108 (ii)–(iii), not from D-107. This wording was approved by you as correction C1 (GOVERNANCE-REVIEW-FIXES), so it is not an error. If D-108 is rejected, that sentence needs revisiting (Section 9, P3).

### 4.1 Technical evaluation
| Check | Result |
|---|---|
| Circular dependencies | **None.** Each step needs only earlier steps: the freeze entry ID → condition 5; the fixed-inventory entry → condition 6 (d); the six condition IDs → the D-088 (4) binding `d035_s6_records`; the D-074 (f) authorisation → Stage-0 rows; Stage-0 rows → the draw (D-093; the sampler checks the seven rows) |
| D-035 | Consistent: all six conditions are recorded before any authorisation (D-025, D-063 and D-077 need §6 met before the draw) |
| D-074 (f) | Consistent: its bindings (`criteria_version`, `inventory_sha256`, `freeze_entry`, six condition IDs) all exist by step 4 |
| D-077 (6) | Consistent for the draw. **Gap:** D-077 (6) also covers the researcher's pilot sheet. Under R1 (D-109 design), the custodian's commitment must exist before the sheet is delivered, but the sequence does not require the D-102 revision and custodian before step 6 |
| D-092 / D-097 | Consistent: one row per condition, in the D-097 (b) form; the condition-6 row cites the entry by ID |
| D-107 | Consistent: the entry comes before condition 6, and both authorisations bind the same hash |
| D-093 (approved, conditional) | D-108 inserts one step between the freeze and the §6 records. D-093's timing rule (Stage-0 rows before the draw) is unchanged |
| Hash consistency | Consistent: one hash, from the entry, is bound twice. **Gaps:** (1) nothing states what happens if the inventory changes after the entry; (2) the B2 cross-check (the tool comparing the bound hash with the entry) is deferred |
| Missing prerequisite | D-099 steps (3) and (4) must be implemented "before the first authorised run", which is the D-074 (f) Stage-0 run. D-108 does not mention this; it follows from D-099 |

### 4.2 Recommendation `[RECOMMENDATION]`
**Approve D-108 with three explicit additions:**
1. D-099 steps (3) and (4) implemented and tested before step 4.
2. The D-077 (6) authorisation (step 6) recorded only after the D-102 revision is approved and its custodian and tool preconditions are met. Alternatively, it states that the sheet is not delivered before the commitment exists.
3. If the inventory, raw exports or build code commit change after step 2, a new fixed-inventory entry is needed, and any later step is repeated.

**Rejecting it** keeps the approved D-093 order. That order already requires the freeze before the §6 records, and D-107 (in principle) still requires a separate entry before condition 6. The practical difference is therefore small: D-108 mainly records the exact place and content of the entry.

**Required by:** activation, not the freeze. **It does not block the freeze.**

## Section 5 — D-102 blinding assessment
**References `[EVIDENCE]`:**
- the D-102 row and its history rows (B1-B6-APPROVALS, AUDIT-DECISIONS, GOVERNANCE-REVIEW-FIXES, D1-D2-APPLIED);
- the D-109 row;
- protocol §7 (Screeners and Outputs rows) and §7a (governing line; step 1 last bullet; step 5);
- protocol §11 rows for B1–B6, the governance-review fixes, D1–D2 and the pre-freeze review;
- criteria §9 row 177 and §11 step 5.

**Checks:**
| Check | Result |
|---|---|
| (B) The salt is never placed in the screening CSV | **PASS for current text and code.** D-102 clause (1), "a random salt line", is the recorded clause. The AUDIT-DECISIONS history row records that it cannot be implemented as worded, because the validator refuses a salt row or column. §7a step 5 marks the revision as pending. No script contains "salt" (`grep` over `scripts/`) |
| (C) No exposure of the salt through justifications, logs or reports | **PASS (no salt exists).** The R1 draft forbids `S` in the commitment record before disclosure. Justifications are paraphrased only (D-089) |
| (D) R1 and R2 not described as implemented | **PASS.** §7a step 5 reads "[OPEN … R1 selected as the design, R2 as the fallback (D-109; design only)]"; protocol §11 says "No custodian appointed; nothing implemented" |
| Historical wording | Protocol §11, the B1–B6 row: "D-102 approved (salt, independent custodian; appointment pending)" is a dated traceability row. Later rows record the pending revision. PASS (historical) |
| D-102 status cell | "effective at the v1.1 freeze (2026-11-11)" could be misread as a freeze date. **DOCUMENTATION ERROR (ambiguous)**: a clarification is proposed in Section 9 (P1), not applied |

### 5.1 Unresolved requirements (E)
| Requirement | What is undecided or missing | Approval needed |
|---|---|---|
| Independent custodian | Who; the independence criteria (no stake in the outcome, no communication before disclosure) | Researcher: an appointment row |
| Custodian access | Repository rights (push of the commitment only?); read access to the frozen texts and tools | Researcher |
| Private-sheet access | R1 sends the sheet, which contains abstracts, to the custodian; this extends D-096 | Researcher: a D-096 extension |
| Separate account or environment | R1 requires an environment the researcher cannot access | Researcher: confirm feasibility |
| Same model and tools version | The custodian environment uses the frozen texts and a recorded tools commit; the model identity is recorded | Researcher: confirm what is recorded |
| Commitment generation | `C = SHA-256("bioml-insight pilot commitment v1\n" ‖ S ‖ "\n" ‖ F)`; `S` = 32 secure random bytes; `F` = the exact CSV bytes; no tool exists | Separate implementation authorisation (synthetic tests only) |
| Commitment verification | Recompute `C` from the disclosed `S` and the committed `F`; Git-ancestry order check; no tool exists | As above |
| Key management | Custodian signing and encryption keys and their fingerprints (second-channel confirmation); not created | Researcher and custodian, after approval |
| Recovery | Loss of `S` or `F` is an integrity failure: no agreement is computed; retry under Q-083 (open) | Researcher: confirm; Q-083 |
| Audit trail | Commitment, researcher-file and disclosure commits; session-log record; decision-log failure row | Included in the revision text |
| Threat model | Draft in the A3 v2 design note (scratch, not in the repository): researcher sees the assistant's output early; assistant sees the researcher's file; post-hoc edits of `F`; guessing an unsalted hash | Researcher review |

### 5.2 Revised D-102 proposal (F) — for your consideration; **not recorded**
> **Revision of D-102 (R1, proposed).**
> - (1) Pilot decision files are valid screening CSVs with **no** salt row or column.
> - (2) Commitment `C` as above. The commitment record holds the scheme, `C`, the row count, `criteria_version`, the SHA-256 of `pilot_sample.csv`, the D-077 (6) authorisation ID and the time. It never holds `S`, an unsalted hash of `F`, or any decision, code or count.
> - (3) An independent custodian, appointed in a decision row, runs the assistant's pilot screening in an environment the researcher cannot access, at a recorded tools commit, using the seven blinded-sheet fields only. The custodian receives the private sheet under D-096 terms, extended. The key fingerprint is recorded.
> - (4) Order:
>   - (a) the commitment is committed and pushed before the researcher's sheet is delivered;
>   - (b) the researcher's file is validated, committed and pushed;
>   - (c) only then are `F` and `S` disclosed and committed, with a disclosure record.
> - (5) Verification by recomputing `C` and checking Git ancestry. A mismatch, an order violation or lost material is an integrity failure: no agreement is computed, and the failure is recorded.
> - (6) R2 (the researcher's salted commitment first; the custodian holds an encrypted escrow copy) applies only through a separate decision if no custodian is available.
> - (7) Tool support and the `.gitattributes` rule are a separate implementation authorisation, tested with synthetic fixtures only.
>
> The revision replaces clause (1) and keeps D-102's order.

**Design approval (D-109, given) is not operational approval.** Implementation, a custodian, keys and real data remain unapproved.

## Section 6 — Open questions

### 6.1 Q-082, Q-083, Q-084 (E)
| Field | Q-082 | Q-083 | Q-084 |
|---|---|---|---|
| Current status (register) | Open; kept open at the freeze (D-083, APPROVED) | Open; kept open at the freeze (D-083) | Open; kept open at the freeze (D-083) |
| Issue | How to code a retracted **article** at manual screening when its metadata lack the PubMed *Retracted Publication* type (D-076 (8); Stage-0 E7 triggers only on that type, D-074 (a)) | Failed-pilot retry: seed and derivation, allocation of 40 across the strata, frame (are the first 60 excluded?), recording | Timing of the D-008 blind audit (25 include + 25 exclude): "after the first two batches" (protocol v0.1) or "after the first expansion batches" (criteria v1.1 §7) |
| Needed by | "Before such a record is screened (may stay open at the freeze if recorded as open)" | "Before a second pilot, if the first fails" | "Before expansion screening" |
| Can remain open at freeze? | **Yes:** D-083 and criteria §11 step 5 | **Yes:** D-083 | **Yes:** D-083 |
| Consequence | Such a record cannot be coded consistently until answered; it applies at screening, including pilot records | A failed pilot cannot be repeated reproducibly | Expansion screening cannot start |
| Researcher decision required | Yes | Yes (only if the pilot fails) | Yes |
| Stage | Before screening such records | Before a second pilot | Before expansion screening |

### 6.2 Q-085
- **Question:** D-035 record §6 condition 3 requires D-027 and D-024 to be "approved". D-027 is APPROVED (limited) and D-024 is APPROVED — CONDITIONAL. Do these approvals satisfy condition 3?
- **References:** D-035, D-027, D-024; protocol §10 row 3.
- **Consequence if open:** condition 3 cannot be recorded. Without all six conditions there can be no run authorisation (D-088 (4)), so there is no Stage 0, draw or pilot.
- **Blocks:** activation, not the freeze (it is listed in §11 step 5).
- **Alternatives** (from the wording of the question): (a) yes, the limited and conditional approvals satisfy "approved"; (b) no, full approvals are needed first. Not chosen here.

### 6.3 Q-096
- **Ambiguity:** whether D-091 item (a), "the Phase 1 tools committed and tested", includes the Stage B preparation package tools (D-095) and their corrections. These are:
  - frame identity and frame-only mode;
  - hardened authorisation and the ledger;
  - the pilot-agreement tools;
  - the uncommitted D-098 code.
- **Relationship with D-107:** none directly. D-107 concerns item (d), while Q-096 concerns item (a). Both are part of condition 6.
- **Effect on the six conditions:** condition 6 cannot be recorded until it is settled.
- **Effect on D-108:** it does not change the order. It decides what must be committed and tested before step 3.
- **Decision request:** choose one:
  - **(a) Includes them.** Everything must be committed and tested before condition 6, including the D-098 code changes now uncommitted.
  - **(b) Only the Phase 1 tools** (`7f5b608`, `8d9bd79`). The Stage B tools are covered by D-091 (c) or by separate checks.

  Not chosen here.

### 6.4 Q-092 (c)
- **Outstanding requirement:** the form of your authorisation for a **real** frame-only check (`pilot_sample.py --frame-only`). The code does not gate this mode.
- **Why it is needed:** a real frame-only check reads the real inventory to confirm the 1,463-record frame identity (D-095 P17). It is a real-data operation without a run-authorisation gate.
- **What it would authorise:** the check only, with no draw, no output files and no authorisation consumed.
- **What it would not authorise:** a draw, a sheet, Stage 0 or screening.
- **Stage:** before any real frame-only check. Not before the freeze, and not formally required for activation. It is optional unless you want the check.

### 6.5 Q-097
See Section 3.5 for the proposed answer. **Stage:** before the fixed-inventory entry, so before activation. It does not block the freeze.

## Section 7 — Custodian readiness matrix (no one appointed; nothing created)
| # | Item | Applies to | Current state | Depends on | Researcher approval before implementation |
|---|---|---|---|---|---|
| 1 | Appointment | R1 and R2 | Not done | D-102 revision | **Yes:** a decision row |
| 2 | Independence requirements | R1, R2 | Drafted (no stake; no communication before disclosure) | Revision text | **Yes** |
| 3 | Access permissions | R1 (push of the commitment); R2 (escrow) | Undefined | Revision; repository settings | **Yes** |
| 4 | Private screening-sheet access | R1 only | Not permitted yet (D-096 covers the researcher only) | D-096 extension | **Yes** |
| 5 | Encryption and key custody | R1 signing keys; R2 encryption keys | None created | Revision; custodian | **Yes**, then the custodian generates them |
| 6 | Model and tool version consistency | R1 | Not set up | Frozen texts; tools commit | **Yes:** what is recorded |
| 7 | Commitment generation | R1 custodian; R2 assistant | No tool | Separate implementation authorisation | **Yes** |
| 8 | Commitment verification | Both | No tool | As 7 | **Yes** |
| 9 | Audit trail | Both | Defined in the draft (commits, session log, failure row) | Revision | **Yes** (as part of the revision) |
| 10 | Data retention and deletion | Both | Sheet deleted after use (D-096; §7a step 6); custodian copies undefined | D-096 extension | **Yes** |
| 11 | Conflict of interest | Both | Not assessed | Appointment | **Yes:** a stated declaration |

## Section 8 — Cross-document consistency
Columns: criteria v1.1 (Crit), protocol v0.2 (Prot), decision log (DL), governance review and approval package (GR/Pkg).

| Item | Crit | Prot | DL | GR/Pkg | Result | Required action |
|---|---|---|---|---|---|---|
| Decision IDs referenced exist | all resolve | all resolve | — | all resolve | PASS | — |
| Question IDs referenced exist; open ones listed at freeze | step 5 complete (checked by script) | all in step 5 | — | listed | PASS | — |
| Criteria identifier (D-103) | `criteria_v1.1+protocol_v0.2` | same | D-103 | same | PASS | — |
| Status wording (D-104) | DRAFT; FROZEN reserved | same | D-104 | same | PASS | — |
| D-084 freeze procedure | approved in principle; text submitted | — | APPROVED IN PRINCIPLE | same | PASS | Your approval |
| D-035 condition references | §11 step 10 | §10 rows 1–6, none recorded | D-035, D-092 | same | PASS | — |
| D-074 (f) / D-077 (6) authorisations | §11 step 10 | §7, §10 | D-088, D-097 | same | PASS | — |
| D-097 authorisation format | via step 10 | §7 | final | — | PASS | — |
| D-096 custodian references | — | §7, §7a (researcher only) | researcher only | extension listed as needed | PASS | Researcher decision (extension) |
| D-099 timing | — | §7: "before the first authorised run" | same | **Pkg E placed it before step 7** | **DOCUMENTATION ERROR → corrected** | — |
| D-101 | — | §7, §7a step 4 | CONDITIONAL | same | PASS | — |
| D-102 pending | step 5 | §7a step 5 [OPEN] | CONDITIONAL; revision pending; **status cell "(2026-11-11)" ambiguous** | pending | PASS / DOCUMENTATION ERROR (DL cell) | P1 proposed |
| D-107 | approved in principle (§0, §11) | same (§1, §10) | APPROVED IN PRINCIPLE | same | PASS | Researcher decision (Q-097) |
| D-108 | proposal | proposal | PROPOSED | proposal | PASS | Researcher decision |
| D-109 | named | §7a step 5 | design only | same | PASS | — |
| Inventory hash | — | `b668dbde…d054` | D-107 same | same | PASS | — |
| Ignored-file hashes | — | "provenance not established (Q-097)" | D-107 (ii)–(iii) | same | PASS | EVIDENCE REQUIRED (Q-097) |
| Effective dates | "set by the researcher" | same | none recorded | placeholders | PASS | — |
| Historical status cells, criteria §9 | rows 172 and 177 showed past statuses without saying so | — | — | — | **DOCUMENTATION ERROR → annotated** | — |
| Protocol §10 row 6 (d) includes D-108 (ii)–(iii) content | — | approved C1 wording | D-108 PROPOSED | — | RESEARCHER DECISION REQUIRED (only if D-108 is rejected) | P3 |
| Q-063 backup provenance | listed | — | D-106 history row | consistent | PASS / DEFERRED | Researcher decision |
| "1,470-record inventory" (wording in the task prompt) | the scope is 1,470; the inventory file has 3,386 records | same | D-044 | — | PASS (documents correct) | — |

## Section 9 — Documentation corrections

### 9.1 Applied (mechanical; each target matched exactly once)
| File | Section | Existing wording | Proposed (applied) wording | Evidence | Reason |
|---|---|---|---|---|---|
| criteria v1.1 | §9, `criteria_version` row | status "Proposed" | "Proposed (status when this row was written; the identifier was later approved as D-103, see the B1–B6 row below)" | D-103 row | The status column read as current |
| criteria v1.1 | §9, governance-reconciliation row | "…D-097–D-099: APPROVED — PROVISIONAL; … D-102: PROPOSED" | same text + "(statuses when this row was written; later, 2026-11-11: D-097 and D-099 final, D-098 final and conditional, D-102 APPROVED — CONDITIONAL with its revision pending; current statuses in `logs/DECISION_LOG.md`)" | D-097, D-098, D-099, D-102 rows | As above |
| criteria v1.1 | §9 | — | new traceability row FINAL-PRE-FREEZE-ISSUE-RESOLUTION ("No rule changed") | — | Rule 9 traceability |
| approval package | §E | D-099 (3), (4) listed "before step 7" | separate bullet "before step 4 … D-099 steps (3) and (4)", with a correction note | D-099 status cell: "required before the first authorised run" | Wrong timing |
| approval package | top of §A | — | follow-up note pointing to this report; section H's percentage superseded | — | The task asks for no single percentage |
| `unresolved_questions.md` | Q-097 status | "Open" | "Open. Evidence assembled 2026-11-11 (this report §3); no method chosen; researcher decision" | this report | Pointer only; the question stays open |

No status cell, decision, question resolution, rule or threshold was changed. Protocol v0.2 was not changed by this task.

### 9.2 Proposed, awaiting your approval (not applied)
| # | File | Section | Existing wording | Proposed wording | Evidence | Reason |
|---|---|---|---|---|---|---|
| P1 | `logs/DECISION_LOG.md` | new D-102 status-history row (the status cell stays unchanged) | "effective at the v1.1 freeze (2026-11-11)" | "No status change. Clarification: '(2026-11-11)' in the status cell is the approval date; the v1.1 freeze has not taken place, and D-102 takes effect only at the freeze" | No freeze entry or registry exists (Section 10) | Ambiguity. Its meaning must be confirmed by you |
| P2 | `logs/DECISION_LOG.md` | D-108 (a revised proposal, recorded as an alternative) | current D-108 order | add §4.2 items 1–3 | D-099; D-109 R1; D-107 | Gaps in the sequence |
| P3 | protocol v0.2 | §10 row 6 (d) | "…together with the observed SHA-256 and provenance status of the Git-ignored record files…" | keep if D-108 is approved; revise if it is rejected | D-108 (ii)–(iii); C1 approval | Depends on D-108 |
| P4 | `logs/DECISION_LOG.md` | new D-102 revision row | — | the §5.2 text | D-109 | Your design decision |
| P5 | `unresolved_questions.md` / fixed-inventory entry | Q-097 | — | the §3.5 text | Section 3 | Your decision |

## Section 10 — Test results (actual)
Run 2026-11-11, 14:00:32Z–14:01:44Z, after all corrections in §9.1 (synthetic fixtures only; `-I -B`):

| Check | Result |
|---|---|
| Phase-1 screening tool tests | 130 tests, OK |
| Literature tests (`tests/literature`) | 347 tests, OK |
| Data-protection tests (`DATA_PROTECTION_STRICT=1`) | 10 tests, OK |
| NHANES safeguard tests | 29 tests, OK |
| Search-query table check | PASS: 168 rows |
| Raw exports vs `MANIFEST.csv` (`pubrecords.py verify`, read-only) | OK, exit 0 |
| `git diff --check` / CRLF-aware check | exit 0 / exit 0; no CR or whitespace errors in untracked files |
| SHA-256 of `paper_inventory.json`, `publications.jsonl`, `source_records.jsonl` before and after the tests | all OK (unchanged) |

The checks for no activation, no freeze, no registry, no Stage-0 rows, no sample, no authorisation and nothing staged are listed in the task report of 2026-11-11 and in `logs/session_logs/2026-11-11_FINAL-PRE-FREEZE-ISSUE-RESOLUTION.md`.

## Section 11 — Researcher decision register
| ID | Current status | What is asked | Alternatives (from the records) | Consequences | Required by | Blocks |
|---|---|---|---|---|---|---|
| Content approval of criteria v1.1 | Final draft | Approve the complete text | approve / request changes | Approval enables the freeze | Freeze | **Freeze** |
| Content approval of protocol v0.2 (incl. §7a) | Final draft | Approve | as above | as above | Freeze | **Freeze** |
| D-084 | APPROVED IN PRINCIPLE | Approve the amended §11 text | approve / amend | Needed to execute the freeze | Freeze | **Freeze** |
| D-107 | APPROVED IN PRINCIPLE — subject to verification | Keep it qualified at the freeze, approve it fully, or revise it | as stated | It is listed open at the freeze in any case; full approval needs Q-097 | Before the fixed-inventory entry | Activation |
| Freeze-entry ID and dates | — | Reserve `D-nnn`, the approval date and the effective date | — | Needed for the freeze commit | Freeze | **Freeze** |
| Git authorisation | — | Package G1–G5 | — | No commit or push without it | Each Git step | **Freeze** |
| D-108 | PROPOSED | Approve (with §4.2 additions), approve as is, or reject | as stated | Rejecting keeps the D-093 order and the D-107 principle | Activation | Activation |
| Q-097 | Open | Provenance method | (a) scratch rebuild; (b) accept the scratch evidence; (c) accept as observed with incomplete provenance; (d) compare with a researcher-held copy, if one exists | (a) gives an independent check; (b) and (c) record a limitation | Fixed-inventory entry | Activation |
| Q-063 | Open — partly addressed | Record the approval details; decide the PRESERVED status; verified restore per workspace | — | Rebuilds and provenance checks are restricted until settled | Fixed-inventory entry; next rebuild | Activation |
| Q-085 | Open | Do the limited/conditional approvals satisfy condition 3? | yes / no | No: D-027/D-024 approvals are needed first | Condition 3 | Activation |
| Q-096 | Open | The scope of D-091 (a) | includes the Stage B tools / Phase 1 tools only | Including them requires committing the D-098 code first | Condition 6 | Activation |
| Q-092 (c) | Open | The form of a frame-only-check authorisation | — | No real frame-only check until answered | Before any real frame-only check | Operation (optional) |
| D-102 revision (P4) | Pending (D-109 design only) | Approve the R1 text, or R2 | R1 / R2 | Pilot screening is impossible until approved | Pilot | Operation |
| D-096 extension | Not decided | The custodian receives the private sheet | yes / no (if no, R1 is not workable → R2) | — | Pilot (R1) | Operation |
| Custodian appointment | Not done | Who; their independence; conflict of interest | — | — | Pilot | Operation |
| D-099 (3), (4) implementation authorisation | Approved for after the freeze | — | — | Required before the first authorised run | Before D-074 (f) | Operation |
| Q-082 / Q-083 / Q-084 | Open (D-083) | As in §6.1 | — | As in §6.1 | Screening such records / second pilot / expansion | Later stages |
| P1 (D-102 status-cell clarification) | Proposed | Confirm the meaning | — | Removes the ambiguity | Any time | None |

## Section 12 — Final readiness assessment
| Category | Assessment |
|---|---|
| **1. Documentation readiness** | **Ready.** Both texts are final drafts; the mechanical corrections are applied; the remaining items are your decisions, not drafting |
| **2. Provenance readiness** | **Partial.** Inventory hash verified; raw exports verified against the manifest; ignored-file provenance strongly supported but not verified (Q-097); Drive backup reported only (Q-063) |
| **3. Researcher approval readiness** | **Ready for your review.** The decision register (Section 11) is complete |
| **4. Freeze readiness** | **Blocked only by your approvals and authorisations:** content approvals, D-084, the D-107 position, ID and dates, Git |
| **5. Activation readiness** | **Not ready:** Q-085, Q-096, Q-097, Q-063 provenance, D-108, the fixed-inventory entry, the condition rows |
| **6. Operational readiness** | **Not ready:** D-099 (3)/(4), the D-102 revision, the D-096 extension, the custodian, the tools, the B2 cross-check, run authorisations; Q-092 (c) only if a real frame-only check is wanted |
