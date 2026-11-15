# Final pre-freeze approval package — criteria v1.1 and protocol v0.2 (2026-11-11; comprehensive governance review)

> Assistant review prepared for the researcher. It **approves nothing, freezes nothing, records no activation condition, creates no fixed-inventory entry, registry or run authorisation, and authorises no Git operation** (`CLAUDE.md` rule 7). No ID, date, signature, hash or approval in this package is invented: placeholders are marked `<…>`.

> **Follow-up (2026-11-11):** the issue-resolution audit `research/reviews/2026-11-11_FINAL-PRE-FREEZE-ISSUE-RESOLUTION.md` supersedes the readiness summary in section H (no single percentage) and adds the provenance evidence for Q-097 and the D-108 assessment.

> **Final version for confirmation (2026-11-11, COMPLETION-BATCH-E).** The six researcher-approved mechanical corrections are applied (criteria §4 and §11; protocol §1 and §7a step 5; package §E; a D-102 history row). No rule, code, threshold, RQ or decision status changed. Sections H and I below are the confirmation sheet. The basis is `research/reviews/2026-11-11_FINAL-INDEPENDENT-CRITERIA-PROTOCOL-REVIEW.md`.

## A. Current project and repository state (verified 2026-11-11)

| Item | State |
|---|---|
| Branch | `claude/eloquent-mccarthy-bqtxr3-part1` |
| HEAD | `c6e1b14c81821c0cddca26af1d0070829152999c` ("Stage B preparation package (pre-freeze; synthetic fixtures only)") |
| Remote | `origin/…-part1` at `8d9bd79`; local is 1 commit ahead, 0 behind; **not pushed** |
| Working tree | Approved documentation, governance and D-098 code changes, uncommitted; **nothing staged** |
| Documents | `screening_criteria_v1.1.md` and `screening_protocol_v0.2.md`: **FINAL DRAFT for researcher content approval; NOT frozen; not in force** |
| Screening | **Inactive.** No Stage 0, sample, researcher sheet, screening output, registry, activation record, fixed-inventory entry or run authorisation exists |
| PR #17 | Open, not merged; description not updated |

## B. Final criteria v1.1 review summary
- **Scientific content unchanged:**
  - scope (§0, §2), RQ criteria (§3);
  - inclusion I-C1–I-C4 and exclusion E1–E12 (number and meaning unchanged; primary code D-080, D-074 (d));
  - decision tree with `uncertain` → full text (§4; D-105);
  - tiers (§5); record format (§6); pilot and audit pointers (§7).
- **Governance text:**
  - D-107 is described as *approved in principle, subject to verification* in §0 and §11 steps 1 and 10;
  - D-108 is named only as a proposal;
  - §11 step 5 lists every open item;
  - §11 runs steps 1–11 plus 9a, in order and without circularity;
  - step 11 states that the freeze authorises nothing.
- **Labels:** the Version row reads "FINAL DRAFT … NOT frozen"; the identifier is `criteria_v1.1+protocol_v0.2` (D-103); the FROZEN wording is reserved for the freeze commit (D-104).

## C. Final protocol v0.2 review summary
- **Scientific content unchanged:**
  - input set (§1); descriptors (§2, §2a); decision rules and Stage 0 (§3); duplicates (§4); audit trail (§5); codes (§6);
  - pilot (§7): 60 records, seed 4004, D-063 allocation, D-077 draw, D-025 pass rule with the D-098 definitions;
  - expansion (§8); citation (§9).
- **Governance text:**
  - §1 and §10 row 6 describe D-107 as approved in principle and D-108 as proposed;
  - §10 row 6 separates the verified inventory hash from the unverified provenance of the ignored files (Q-097);
  - §7 states D-101 and defers the workflow details to the pending D-102 revision;
  - §7a step 5 states that the D-102 revision is pending, with R1 as the selected design and R2 as the fallback (design only), and that the pilot cannot start until it is approved;
  - no custodian is appointed and nothing is implemented.
- **Historical rows:** the earlier salt workflow appears only in a dated traceability row (§11, B1–B6). The later §11 rows record that the workflow is pending.
- **Labels:** as for the criteria.

## D. Outstanding governance decisions and their exact statuses

| Item | Recorded status (decision log or register) | What is still needed |
|---|---|---|
| D-084 (freeze procedure) | APPROVED IN PRINCIPLE | Your approval of the final amended §11 text |
| D-101 (no exposure of assistant decisions) | APPROVED — CONDITIONAL (inactive) | Nothing before the freeze |
| D-102 (blinding workflow) | APPROVED — CONDITIONAL (inactive); **revision pending** (clause (1) not implementable) | The revision text (R1 with the C3 additions), before the pilot |
| D-106 (freeze open-items list) | APPROVED (status cell left as recorded) | — |
| D-107 (inventory-hash sequencing principle) | **APPROVED IN PRINCIPLE — subject to verification** (status cell left as recorded) | Settling the provenance of the ignored files (Q-097); a full approval or a revision of D-107 is your decision |
| D-108 (exact amended order) | **PROPOSED** | Approval or rejection, before activation |
| D-109 (A3 design; R1 primary, R2 fallback) | APPROVED — design work only | — |
| Q-063 (raw-export backup and restore) | **Open — partly addressed** | Backup provenance settled (record the approval details; decide the PRESERVED status); a verified restore in each new workspace before any rebuild or provenance check |
| Q-085 (condition 3) | Open | Your decision, before activation |
| Q-092 (c) (real frame-only check) | Partly answered; (c) Open | Your decision, before any real frame-only check |
| Q-096 (scope of condition 6 (a)) | Open | Your decision, before activation |
| Q-097 (provenance of the ignored files) | Open | Your decision, before the fixed-inventory entry |
| Q-082, Q-083, Q-084 | Open (kept open at the freeze, D-083) | As their "Needed by" |
| Q-021, Q-042, Q-064; D-030 | Open / PROPOSED | As their "Needed by" |
| D-096 extension (custodian receives the private sheet) | Not yet decided | Your decision, before the pilot (R1) |
| Custodian appointment; access control; keys; tools | Not done | Before the pilot |

**Verified facts, kept separate from requirements:**
- **(i) Verified:** `paper_inventory.json` SHA-256 `b668dbde42473baa49ac1f02f89f900e94e39159c82efb8175ba125fef06d054`, by five methods; unchanged since `bf0c579`.
- **(ii) Observed only:** the Git-ignored `publications.jsonl` (`0141d5d8…d192`) and `source_records.jsonl` (`78eba1d3…9460`); their **provenance is not established** (Q-097).
- **(iii) Q-063:** a private Google Drive folder was designated as the off-device backup (D-010; Q-011 (b)). Drive-copy SHA-256 values were reported by you as matching the recorded values; the assistant did not observe them.

## E. Freeze procedure, proposed sequence and unresolved dependencies

**The freeze itself (criteria §11):**
1. Your content approval (step 3) and approval of the amended §11 (D-084).
2. Reserve the freeze-entry ID and the dates (step 8).
3. Freeze commit: only the two texts with the FROZEN line, plus the superseded notes on v1.0 and v0.1 (steps 2, 6).
4. SHA-256 of both texts from that commit (step 7).
5. Freeze entry and registry in one commit (steps 9, 9a).

**After the freeze — proposed sequence D-108 (PROPOSED, not approved):**
1. the freeze;
2. the fixed-inventory entry;
3. the six activation-condition rows;
4. the D-074 (f) authorisation;
5. the Stage-0 rows;
6. the D-077 (6) authorisation;
7. the pilot draw.

There is no circular dependency. The hash is fixed (2) before condition 6 is recorded (3), and the authorisations (4, 6) bind the same hash.

**Unresolved dependencies (not freeze blockers):**
- before step 2: Q-097 (provenance method) and Q-063 (backup provenance settled; verified restore in the working space);
- before step 3: Q-085, Q-096;
- before step 5 at the latest (the first authorised run, the Stage-0 run): D-099 steps (3) and (4) implemented and tested (D-099: "required before the first authorised run"). Corrected 2026-11-11 (Batch E): earlier wording placed them before step 7, then before step 4; "before step 4" applies only if you adopt the D-108 refinement that requires it;
- before step 7 and the pilot screening: the D-102 revision, the D-096 extension, the custodian, the tools, the B2 cross-check;
- before any real frame-only check: Q-092 (c).

**The freeze authorises no Stage-0 run, sampling or screening** (§11 step 11).

## F. Freeze-entry fields requiring researcher input (do not create before approval)

| Field | Value or source |
|---|---|
| Freeze-entry ID | `<D-nnn>`: you reserve it before the freeze commit |
| Approval date | `<YYYY-MM-DD>`: the date of your content approval |
| Effective date | `<YYYY-MM-DD>`: set by you at the freeze |
| Applicable document versions | `criteria_v1.1+protocol_v0.2` (D-103); paths `research/literature/screening_criteria_v1.1.md`, `research/literature/screening_protocol_v0.2.md` |
| Freeze commit | `<40-hex>`, known only after the freeze commit exists |
| Applicable document hashes | `<criteria SHA-256>`, `<protocol SHA-256>`, from `git show <freeze commit>:<path> \| sha256sum` |
| Required decision references | D-084 (procedure); D-103 (identifier); D-104 (status wording); D-081 (file names; condition 5 refers to `screening_criteria_v1.1.md`); D-082 / D-068 (5) (Stage-0 confirmation restated); D-083 and D-106 (open items) |
| Open items to list, with "Needed by" | Q-082, Q-083, Q-084; Q-021, Q-042, Q-063, Q-064, Q-085, Q-092 (c), Q-096, Q-097; proposals D-030, D-108; the pending D-102 revision |
| Required sign-off details | Your explicit content approval and §11 approval, quoted with dates in "Approved by / date" |
| Decision cell opening | `**Freeze of screening criteria v1.1 and screening protocol v0.2.**` |
| Status | `**APPROVED** — freeze entry` |
| Statement | The freeze activates no screening and authorises no Stage-0 run, sampling, screening, extraction or training |
| Same commit | `criteria_registry.json` with the eight fields `criteria_version`, `decision_id`, `criteria_path`, `protocol_path`, `freeze_commit`, `criteria_sha256`, `protocol_sha256`, `effective_date`; status-history rows for the decisions that take effect at the freeze (to be checked row by row then) |

## G. Git operation plan (proposed only; no Git operation is authorised by this package)
1. **Pre-freeze documentation commit:** stage exactly the files `git status` shows at that time (on 2026-11-11: 9 modified, plus the new session logs and this package). Run all tests first. Suggested message: "Pre-freeze governance and documentation updates (B1–B6; D-105–D-109; D1–D2; governance review; no freeze)".
2. **Push** `c6e1b14` and commit 1 (a fast-forward), if you authorise it separately.
3. **Freeze commit:** only the two texts (Version rows) and the superseded notes on v1.0/v0.1. Message: "Freeze criteria v1.1 and protocol v0.2 (criteria_v1.1+protocol_v0.2)".
4. **Freeze-entry and registry commit:** the freeze entry with hashes from commit 3, the status-history rows and `criteria_registry.json`; validator and tests run. Message: "Record freeze entry <D-nnn> and criteria registry".
5. **Push and PR #17 description update.** Never merge automatically.

## H. Final confirmation sheet (blockers by stage)
Statuses preserved:
- D-107 APPROVED IN PRINCIPLE — subject to verification;
- Q-097 OPEN;
- D-108 PROPOSED;
- D-102 revision and operational approval pending;
- D-084 APPROVED IN PRINCIPLE.

**Freeze blockers (all are your decisions; nothing else blocks the freeze):**

| # | Decision | What closes it |
|---|---|---|
| F1 | Content approval of criteria v1.1 | Your explicit approval, as is or with any of the section I wording you choose |
| F2 | Content approval of protocol v0.2 (incl. §7a) | As F1 |
| F3 | D-084: approval of the amended §11 (now with the execution order) | Your approval |
| F4 | D-107 position at the freeze | "Remains approved in principle" (listed open in the freeze entry), or a full approval |
| F5 | Freeze-entry ID, approval date, effective date | **Proposed ID: `D-110`** (the next unused ID; D-109 is the last recorded on 2026-11-11). **Approval date `<YYYY-MM-DD>`** and **effective date `<YYYY-MM-DD>`**: your values (not proposed by the assistant). Confirm the ID or name another |
| F6 | Git authorisation | Permission for G1 (pre-freeze commit), G2 (push), G3 (freeze commit), G4 (freeze entry and registry), G5 (push; PR #17 description) |

**Permitted to stay open at the freeze** (listed in the freeze entry, §11 step 5): Q-082, Q-083, Q-084 (D-083); Q-021, Q-042, Q-063, Q-064, Q-085, Q-092 (c), Q-096, Q-097; proposals D-030 and D-108; the pending D-102 revision.

**Activation blockers (after the freeze):**

| # | Item | Who | What closes it |
|---|---|---|---|
| A1 | Q-085 (condition 3) | Researcher | Yes or no |
| A2 | Q-096 (scope of condition 6 (a)) | Researcher | Yes or no; if yes, the D-098 code is committed and tested first |
| A3 | Q-097 (provenance of the ignored files) | Researcher | Option (a), (b) or (c) |
| A4 | Q-063 (backup provenance) | Researcher | Approval details recorded; PRESERVED status decided |
| A5 | D-108 (order) | Researcher | Approve, approve with refinements, or reject |
| A6 | Fixed-inventory entry; six condition rows | Technical, on your instruction | Recorded after A1–A5 |

**Operational blockers (before the runs and the pilot):**

| # | Item | Who | What closes it |
|---|---|---|---|
| O1 | D-099 steps (3) and (4) | Technical | Implemented and tested before step 5 at the latest |
| O2 | B2 cross-check | Technical | Implemented and tested before the first run |
| O3 | D-102 revision (R1; R2 as fallback) | Researcher | Approval of the revision text |
| O4 | D-096 extension | Researcher | Yes or no (if no, R2) |
| O5 | Custodian; keys; commitment tools | Researcher (appointment); technical (tools) | Appointment row; tools tested with synthetic data |
| O6 | Run authorisations D-074 (f), D-077 (6) | Researcher | Authorisation rows |
| O7 | Q-082 | Researcher | Coding rule, preferably before the pilot |

## I. Optional clarifications — researcher decisions (2026-11-11; researcher prompt "We are proceeding toward the documentation freeze." (2026-11-11))
| ID | Decision | Where recorded | Effect |
|---|---|---|---|
| R1 | **LIMITATION ONLY** | Here, for the review's limitations section: "The D-044 scope excludes the dedicated RQ2 (Q-PM-04, Q-PM-05), RQ3 (Q-PM-06 to Q-PM-08), RQ4 (Q-PM-09, Q-PM-10) and RQ6 (Q-PM-13, Q-PM-14) query strands. Evidence for these RQs comes only from records retrieved by the RQ1, RQ5 and G queries; it is reported as incidental, not representative, coverage." | Not written into the criteria or protocol |
| R5 | **LIMITATION ONLY** | Here, for the review's limitations section: "Tier-3 RQ1 records are included on title/abstract evidence; only a random sample is read at full text; their eligibility and descriptors are abstract-level and are reported as such." | Tier rule unchanged |
| R7 | **APPLY option (a)** | Criteria v1.1 I-C4 and §3 RQ6; protocol v0.2 §3 | Systematic and scoping reviews informing RQ6: `record_type=review_lead`, may be tagged RQ6. No rule change |
| R8 | **APPLY** | Criteria v1.1 §1 E2 and E3 clarification column | E1-style note; meaning unchanged (§4) |
| R2 | **APPLY** | `search_strategy.md` §1.2 RQ5 row, note and change history | RQ5 wording names probability calibration (D-031) |

## J. Recorded researcher approvals (2026-11-11; researcher prompt "I confirm the following researcher approvals" (2026-11-11))
These approvals are **documentation approval only**. They do not authorise:
- the freeze execution, the freeze entry or the registry;
- any Git operation (staging, committing, pushing);
- screening, sampling, extraction, pilot work, training, activation or any real-data operation.

| # | Approval as given by the researcher |
|---|---|
| F1 | Content of `research/literature/screening_criteria_v1.1.md` at SHA-256 `ff5ce20e1cd3d939ee50fa5be0309f11a1e338b99194206d0773d8674ad4675d` approved as the final text for the freeze |
| F2 | Content of `research/literature/screening_protocol_v0.2.md`, including §7a, at SHA-256 `836e26fdb2d4865435ec8a3ca5d94ff99fef66c09fda8d6fbd8767ab9cc97c30` approved as the final text for the freeze |
| F3 | Amended freeze procedure (criteria v1.1 §11), including the execution-order paragraph, approved under D-084. The rename was completed in commit `d04ce31` (2026-11-01). No additional clarification sentence is required |
| F4 | D-107 remains APPROVED IN PRINCIPLE — subject to verification, and is listed as open in the freeze entry. Q-097 remains OPEN; D-108 remains PROPOSED; the D-102 revision remains pending |
| F5 | `D-110` approved as the freeze-entry ID, subject to a recheck of its unused status immediately before execution (unused on 2026-11-11 at recording) |
| Approval date | **2026-11-11**, confirmed by the researcher (researcher prompt "I confirm that the F1–F5 approval date is 2026-11-11" (2026-11-11)). Earlier the field read "[ENTER ACTUAL APPROVAL DATE]" |
| Effective date | To be determined separately and recorded only when the freeze is executed |

**Still required before the freeze is executed:**
- a separate freeze-execution authorisation;
- a separate Git authorisation (G1–G5);
- the D-110 recheck;
- a hash recheck: the freeze commit must contain the approved texts unchanged apart from the D-104 status lines.
