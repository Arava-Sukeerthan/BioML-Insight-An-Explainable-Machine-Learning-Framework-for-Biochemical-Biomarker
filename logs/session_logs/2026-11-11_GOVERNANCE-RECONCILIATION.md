# Session log — 2026-11-11 — GOVERNANCE-RECONCILIATION

**Objective** (researcher prompt "Prepare the final governance reconciliation", 2026-11-11):
- record the researcher's preferences:
  - Q-085 unresolved;
  - D-090 at the formal freeze;
  - D-098, D-097 and D-099 provisionally accepted;
  - Q-094 Option A;
  - Q-095: no exposure, and a hash-first workflow to be proposed;
- reconcile D-090 and D-091;
- integrate the procedure into protocol v0.2;
- propose the hash-first workflow;
- update the register and traceability; preserve history.

**Not authorised and not done**: a decision on Q-085; a freeze; activation-condition records; real-data operations or processing; stage, commit or push.

## State
- **Start:** HEAD `8d9bd79`, 18 uncommitted files of the Stage B package, nothing staged.
- **End:** HEAD unchanged; uncommitted; nothing staged.

## Work
1. **Decision log.**
   - D-090: the researcher's timing.
   - D-091: open point on item (a), registered as Q-096.
   - D-097, D-098, D-099 → **APPROVED — PROVISIONAL**.
   - D-100 → **APPROVED** (Option A).
   - New D-101 (requirement) and D-102 (PROPOSED workflow).
   - 10 status-history rows.
   - Cross-references in D-092, D-094 and D-095 updated; a note added to the D-097–D-100 introduction.
   - IDs D-101, D-102 and Q-096 checked as unused first.
2. **D-025 consistency check of D-098.** D-025 approved "pass criteria and adjudication as written" in protocol v0.1 §7: "no record excluded by one screener that the other judged `include` without adjudicated agreement on the exclusion" and "no systematic disagreement on any single code (≥ 3 disagreements on one code)".
   - (a) is consistent.
   - (b) as proposed let any adjudicated decision (include, exclude or uncertain) resolve a conflict. That is broader than "agreement on the exclusion". It is aligned in the D-098 text, the protocol and `pilot_agreement.py`: only an adjudicated `exclude` resolves the conflict.
   - (c) is not covered by D-025. The tool never reports a pass without κ ≥ 0.60.
   - The protocol v0.2 "Pass" row had shortened the D-025 wording; it is restored.
3. **Option A.**
   - Protocol v0.2 §7a holds the procedure. It is updated for D-101, with D-102 marked PROPOSED and the D-098 rules.
   - `pilot_procedure_assistant.md` is a pointer. It was first written saying the procedure "is approved, committed, hashed and frozen"; I corrected this before the end of the task to say nothing is approved as final content or frozen.
4. **Register.**
   - Q-088, Q-091, Q-092, Q-093, Q-094 and Q-095 updated.
   - Q-096 added.
   - Q-085 unchanged.
5. **Consistency of D-097 to D-102.**
   - Statuses: D-097, D-098 and D-099 are provisional; D-100 and D-090 approved; D-101 approved and conditional; D-102 proposed.
   - The provisional statuses begin "**APPROVED — PROVISIONAL**", so the tools, which require the `**APPROVED**` prefix for a freeze entry or a condition record, cannot use them as such.
   - The D-099 Decision text still reads "Already implemented as run safety, for confirmation"; its status cell records the provisional acceptance.
   - The D-100 text still describes both options; its status records Option A.

## Text replaced in this task (preserved verbatim)
These texts were written earlier on 2026-11-11 and never committed.

- **D-090, decision cell** (before):

  > **Q-088 (part): superseded notes.** `screening_criteria.md` (v1.0) and `screening_protocol.md` (v0.1) are preserved, and each is marked as superseded when the updated texts are ready. Assistant reading, recorded for the researcher to confirm: "ready" means the freeze commit, when criteria v1.1 and protocol v0.2 take effect (criteria v1.1 §11 step 2); until then the historical files carry no superseded note, because the drafts are not in force. Refines D-081 ("stay unchanged"): their content stays unchanged; only the note is added. Not decided: the final status wording (Q-088 stays partly open)

- **D-091, decision cell** (before):

  > **Q-086: scope of D-035 record §6 condition 6.** Condition 6 ("the other pilot-blocking items are resolved") is the closed list: (a) the Phase 1 tools committed and tested; (b) the D4 ignore rule in place; (c) the D-088 binding checks in place; (d) the inventory hash fixed for the pilot. Records no condition as met

- **D-097, status cell** (before):

  > **PROPOSED**

- **D-097, approved by cell** (before):

  > — (assistant proposal; awaiting the researcher)

- **D-098, status cell** (before):

  > **PROPOSED**

- **D-098, approved by cell** (before):

  > — (assistant proposal; awaiting the researcher)

- **D-099, status cell** (before):

  > **PROPOSED**

- **D-099, approved by cell** (before):

  > — (assistant proposal; awaiting the researcher)

- **D-100, status cell** (before):

  > **PROPOSED**

- **D-100, approved by cell** (before):

  > — (assistant proposal; awaiting the researcher)

- **D-098, decision text, parts (b) and (c)** (before):

  > (b) An include/exclude conflict is resolved only by a separate adjudication row for the same paper, at `title_abstract`, with `screener=researcher` and a pilot decision (include / exclude / uncertain); the latest such row per paper is the agreed decision; any other adjudication row is refused. (c) When Cohen's κ is undefined (chance agreement 1), the evaluation is reported as undetermined and the researcher decides

- **D-092, cross-reference** (before → after):

  > it is the assistant's proposal D-097 (PROPOSED; Q-092)

  → it is D-097 (originally an assistant proposal; status in its own row; Q-092)

- **D-094, cross-reference** (before → after):

  > (assistant proposal D-098, PROPOSED; Q-091)

  → (D-098, originally an assistant proposal; status in its own row; Q-091)

- **D-094, cross-reference** (before → after):

  > (assistant proposal D-100, PROPOSED; Q-094)

  → (D-100, originally an assistant proposal; status in its own row; Q-094)

- **D-095, cross-reference** (before → after):

  > in the format the assistant proposes in D-097 (PROPOSED; not approved; Q-092)

  → in the format of D-097 (originally an assistant proposal; status in its own row; Q-092)

- **D-095, cross-reference** (before → after):

  > The formats and definitions that the code implements for D-097 and D-098 are assistant proposals, exercised only with synthetic fixtures until the researcher decides.

  → The formats and definitions that the code implements for D-097 and D-098 were written as assistant proposals and are exercised only with synthetic fixtures; their status is recorded in their own rows.

## Verification (2026-11-11 08:56:30–08:58:03 UTC; actual outcomes)

| Command | Outcome |
|---|---|
| `python3 -I -B -m unittest discover -s tests/literature -p "test_phase1_screening_tools.py"` | Ran 127, OK |
| `python3 -I -B -m unittest discover -s tests/literature` | Ran 344, OK |
| `DATA_PROTECTION_STRICT=1 python3 -I -B -m unittest discover -s tests/data_protection` | Ran 10, OK |
| `python3 -I -B -m unittest discover -s tests/nhanes` | Ran 29, OK |
| `python3 -I -B scripts/literature/validate_search_queries.py research/literature/search_queries.csv` | PASS: 168 rows |
| SHA-256 of the ignored data files; `git diff --quiet HEAD` on the inventory, records, scope, raw exports, v1.0 and v0.1 | unchanged |

- A first combined check wrongly included `.gitignore`, which already differs from HEAD because of the D4 rules (STAGE-B-PREPARATION). The re-run without it confirmed the data files are unchanged. `.gitignore` was not changed in this task.
- 85 decision IDs: none is accepted as a run authorisation; no row is a condition record.

## Outstanding researcher decisions
- Q-085.
- Q-088 (final status wording).
- Final confirmation of D-097 (and Q-092 (c)), D-098 and D-099.
- Implementation of D-099 steps (1)–(5).
- D-102 (Q-095): the workflow and its open points (custody of the sealed file, the ignore rule, tool support).
- Q-096 (scope of D-091 item (a)).
- Then: content approval of criteria v1.1 and protocol v0.2 (including §7a); approval of the §11 procedure; the freeze; the six condition rows; the two run authorisations.

## Git
Uncommitted; nothing staged; not pushed. PR #17 not changed.
