# Session log — 2026-11-11 — B1-B6-APPROVALS

**Objective** (researcher prompt "The researcher has approved B1–B6 according to the recommendations in the latest decision report", 2026-11-11):
- record B1–B6;
- implement the D-098 adjudication marker and the undefined-κ handling, with protocol text and synthetic tests;
- finalise D-097 and D-099;
- update D-102, keeping the custodian appointment pending;
- finalise the identifier and the Q-088 wording;
- review the amended D-084 procedure;
- produce the final drafts.

**Not authorised and not done**: push; freeze; activation-condition records; run authorisations; Stage 0; sampling; real-data processing; stage or commit; resolving Q-085, Q-096 or Q-092 (c).

## State
- **Start:** HEAD `c6e1b14` (preparation package, local, 1 commit ahead of the remote); clean working tree.
- **End:** HEAD unchanged; uncommitted changes; nothing staged.

## Approved recommendations (decision report of 2026-11-11, section B)
- **B1:** keep `criteria_v1.1+protocol_v0.2` → D-103.
- **B2:** the FROZEN / SUPERSEDED wording → D-104.
- **B3:** (1) no code match; (2) keep counting; (3) distinct adjudication marker; (4) undefined κ = not passed → D-098.
- **B4:** finalise D-097.
- **B5:** finalise D-099, including the interrupted-run rule; steps (3) and (4) after the freeze → D-099.
- **B6:** hash-first with an independent custodian and a salted file → D-102.

## Implementation choices (for content approval)
- The marker value `researcher:adjudication` follows the existing namespaced screener value `rule:stage0`. Plain `screener=researcher` keeps its meaning for full-text verification rows (D-035 G4; `pubrecords.RESEARCHER`).
- Pilot files are checked for their screener, so a researcher pilot file passed as the adjudication file is refused.
- Statuses chosen:

  | Decision | Status |
  |---|---|
  | D-097 | APPROVED — implementation decision (as D-088) |
  | D-098, D-102 | APPROVED — CONDITIONAL (inactive for screening), like the other pilot rules (D-094, D-101) |
  | D-099 | APPROVED (governance and implementation) |
  | D-103, D-104 | APPROVED (documentation) |

## Review of the amended freeze procedure (criteria v1.1 §11; D-084)
- **Finding: the registry was missing.** No step created `criteria_registry.json`, which D-085 B2 creates at the freeze. Added as **step 9a**: in the freeze-entry commit, copied from the freeze entry.
- **Finding: the superseded notes.** The freeze commit also changes v1.0 and v0.1 (D-090/D-104). **Step 6** now lists the freeze commit's exact contents, with no other files.
- **Finding: the placeholders.** The D-104 wording needs the freeze-entry ID and the dates in the files, but not the hash. **Step 8** now reserves the ID before the freeze commit.
- **Finding: open questions at the freeze.** Only Q-082 to Q-084 were listed. **Step 5** now also lists open questions needed after the freeze (Q-085, Q-092 (c), Q-096).
- **Step 1** now names D-080 to D-104. **Step 3** names §7a.
- These amendments are draft text for the researcher's approval; D-084 stays approved in principle.

## Text replaced in the decision log (preserved verbatim)
These rows were written earlier on 2026-11-11 and are included in commit `c6e1b14`, so the earlier text is also in Git history.

- **D-097, status cell** (before):

  > **APPROVED — PROVISIONAL** (subject to final review; not final). Earlier: PROPOSED (STAGE-B-AUDIT-CORRECTIONS, 2026-11-11)

- **D-097, approved by cell** (before):

  > Researcher (owner), 2026-11-11 — researcher prompt "Prepare the final governance reconciliation" (2026-11-11): "Q-092: provisionally accept D-097, subject to final review."

- **D-098, decision cell** (before):

  > **Proposal: operational definitions for the D-025 pass rule (for Q-091; thresholds unchanged).** (a) A disagreement on a code is a pilot record for which exactly one of the two screeners gives that code as its primary exclusion code. (b) An include/exclude conflict counts as resolved only when a separate adjudication row for the same paper, at `title_abstract`, with `screener=researcher`, records the agreed decision `exclude` ("adjudicated agreement on the exclusion", D-025 as written in protocol v0.1 §7); an adjudicated `include` or `uncertain` leaves the conflict unresolved for the pass evaluation; the latest such row per paper is the agreed decision; any other adjudication row is refused. (c) When Cohen's κ is undefined (chance agreement 1), the evaluation is reported as undetermined and the researcher decides; D-025 does not provide for this case, so the tool never reports a pass without κ ≥ 0.60. Part (b) was aligned with the D-025 wording on 2026-11-11 (consistency condition of the provisional acceptance; earlier wording in the status history)

- **D-098, status cell** (before):

  > **APPROVED — PROVISIONAL** (subject to consistency with D-025; part (b) aligned with D-025 on 2026-11-11; not final). Earlier: PROPOSED (STAGE-B-AUDIT-CORRECTIONS, 2026-11-11)

- **D-098, approved by cell** (before):

  > Researcher (owner), 2026-11-11 — researcher prompt "Prepare the final governance reconciliation" (2026-11-11): "Q-091: provisionally accept D-098, subject to consistency with D-025."

- **D-099, decision cell** (before):

  > **Proposal: ledger persistence and tamper evidence (for Q-093; audit finding H1).** Already implemented as run safety, for confirmation: an exclusive run lock; a "started" entry before and a "completed" entry after each authorised write; an interrupted run consumes its authorisation (fail closed) and its outputs are inspected by hand. Proposed procedure, not implemented: (1) after each authorised run, the ledger and the run's committable outputs (not the private sheet) are committed in one dedicated commit naming the authorisation, and pushed, before any further authorised run; (2) a status-history row in `DECISION_LOG.md` records each use ("D-nnn used by <tool>; ledger commit <hash>"), so the decision log also shows the use; (3) before each authorised run, the tools refuse if the ledger differs from its committed version at `HEAD`; (4) each ledger entry carries the SHA-256 of the ledger content before it (a hash chain), so an edited or deleted line is detectable; (5) the session log records the ledger's SHA-256 after each run

- **D-099, status cell** (before):

  > **APPROVED — PROVISIONAL** (including the rule that an interrupted run consumes its authorisation; not final). Implemented: the run lock, the two ledger events and that rule. Not yet implemented: steps (1)–(5); implementing (3) and (4) needs separate authorisation. Earlier: PROPOSED (STAGE-B-AUDIT-CORRECTIONS, 2026-11-11)

- **D-099, approved by cell** (before):

  > Researcher (owner), 2026-11-11 — researcher prompt "Prepare the final governance reconciliation" (2026-11-11): "Q-093: provisionally accept D-099, including the rule that an interrupted run consumes its authorisation."

- **D-102, decision cell** (before):

  > **Proposal: hash-first blinding workflow (for Q-095; meets D-101).** (1) The assistant writes its validated pilot decision file to a sealed holding location that Git ignores (proposed rule `research/literature/screening/sealed/`; not yet in `.gitignore`). (2) A commitment record `screening/pilot_assistant_commitment.json` holding the SHA-256 of the file's exact bytes, its row count, the `criteria_version` and the time (no decision, code or justification) is committed and pushed before the researcher's sheet is delivered. (3) The researcher screens independently; the researcher's decision file is validated and committed. (4) Only then is the sealed file disclosed: copied unchanged to `screening/pilot_decisions_assistant.csv` and committed; its SHA-256 must equal the commitment, otherwise an integrity failure is recorded and no agreement is computed. (5) The order commitment → researcher file → disclosure is checked in the Git history and recorded in the session log. (6) Open points: custody of the sealed file until disclosure (the working container is temporary), the ignore rule, and tool support (`pilot_agreement.py` commitment and verification commands, a refusal to compute agreement before verified disclosure), each needing the researcher's approval or authorisation

- **D-102, status cell** (before):

  > **PROPOSED**

- **D-102, approved by cell** (before):

  > — (assistant proposal requested by the researcher; awaiting the researcher)

## Verification (2026-11-11 09:34:32–09:36:02 UTC; actual outcomes)

| Command | Outcome |
|---|---|
| `python3 -I -B -m unittest discover -s tests/literature -p "test_phase1_screening_tools.py"` | Ran 130, OK |
| `python3 -I -B -m unittest discover -s tests/literature` | Ran 347, OK |
| `DATA_PROTECTION_STRICT=1 python3 -I -B -m unittest discover -s tests/data_protection` | Ran 10, OK |
| `python3 -I -B -m unittest discover -s tests/nhanes` | Ran 29, OK |
| `python3 -I -B scripts/literature/validate_search_queries.py research/literature/search_queries.csv` | PASS: 168 rows |
| SHA-256 of the ignored data files; data, scope, v1.0, v0.1 and `.gitignore` compared with `c6e1b14` | unchanged |
| Real decision log, 87 decision IDs | no run authorisation, no condition row |

- A first attempt at the decision-log edit stopped with a Python quoting error before writing anything. The second attempt applied the edit.
- A first attempt at the test edit used line numbers that were off by one and stopped on its own check before writing anything. Text matching was then used.

## Remaining blockers
- **Freeze:**
  - content approval of both final drafts;
  - approval of the amended §11 procedure (D-084);
  - reservation of the freeze-entry ID and the dates;
  - the separate freeze commit, freeze entry and registry.
- **Activation, after the freeze:**
  - Q-085 and Q-096;
  - the six condition rows.
- **Before the first run:**
  - D-099 steps (3) and (4);
  - D-102 tool support and ignore rule;
  - custodian appointment;
  - Q-092 (c) if a real frame-only check is wanted;
  - the run authorisations.

## Git
Uncommitted; nothing staged; not pushed. PR #17 not changed.
