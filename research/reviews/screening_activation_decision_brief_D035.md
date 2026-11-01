# Screening-Activation Decision Brief — D-035 record §6

| Field | Value |
|---|---|
| Task | SCREENING-ACTIVATION-BRIEF (2026-10-29, Day 16; assistant label, no researcher task ID) |
| Status | **For the researcher's decisions. Nothing is approved, recorded, activated or implemented by this brief.** Decision statuses, question statuses, criteria, protocols, schemas, code and the inventory are unchanged |
| Screening status | **INACTIVE.** No record has been screened; `research/literature/screening/` does not exist; all 3,386 inventory records are `not_screened` |
| Built from (read 2026-10-29) | `GOVERNANCE.md`; `CLAUDE.md` (incl. uncommitted §1a, D-041 PROPOSED); `research/literature/research_plan.md`; `research/methodology/research_integrity.md`; `logs/DECISION_LOG.md` (rows and Status history); `research/reviews/unresolved_questions.md`; `research/reviews/daily_review_log.md`; `research/reviews/Q-041_decision_record_D035.md` §6; `research/reviews/final_confirmation_sheet_LIT-004.md` ("Pilot-blocking items after confirmation", R5); `research/literature/reviews/LIT-005_evidence_review.md` §8; `research/literature/screening_criteria.md`; `research/literature/screening_protocol.md`; `research/methodology/experimental_protocol_v0.1_draft.md` §23; `research/setup/environment_assessment.md` (2026-10-29 addendum, uncommitted) |
| Labels | `[EVIDENCE]` = stated in a repository record cited in the same row; `[RECOMMENDATION]` = assistant proposal, not approved; `[HYPOTHESIS]` = assistant estimate, not measured; `[OPEN]` = listed in `unresolved_questions.md` (`GOVERNANCE.md` §1) |

A recommendation in this brief is **not** researcher approval (`CLAUDE.md` rule 7).

---

## 1. Confirmed facts `[EVIDENCE]`

1. D-035 "governs no screening until" six conditions are met (`Q-041_decision_record_D035.md` §6). Condition 1 (**Q-039**, classification status column) is **met** by D-036 (`LIT-005_evidence_review.md` §8). Conditions 2–6 are **unmet**.
2. D-031 (RQ5 counting rule) is APPROVED — CONDITIONAL and "not applied in screening" until C1–C4 are met. C2, C3 and C4 were answered at decision level by D-032, D-033 and D-034. **C1 (R5/D-029) is still open** (Status history, RQ5-DECISIONS row for D-031).
3. D-032 to D-038 are **APPROVED — CONDITIONAL, inactive**. D-032's approval is recorded in the Status history; its original row still reads PROPOSED, as the log's convention requires.
4. `screening_criteria.md` is **v1.0, DRAFT**. `screening_protocol.md` is **v0.1, DRAFT, PROPOSED** (D-025, D-026). **No v1.1 criteria or v0.2 protocol exist** in the repository.
5. Raw exports are **absent from this container**: `raw_exports/` holds only `MANIFEST.csv` and `README.md`, and `pubrecords.py verify` reports all 244 missing. A rebuild is therefore impossible here until the archives are restored (Q-063).
6. No independent bibliographic index is reachable: 10 hosts gave CONNECT 403 on 2026-10-29 (`environment_assessment.md` addendum). Under `research_plan.md` §6, `partially_verified` records **may be screened** but **not cited**.

## 2. The five unmet D-035 §6 conditions

Terminology is taken verbatim from `Q-041_decision_record_D035.md` §6.

| # | Condition (exact wording) | Current state `[EVIDENCE]` | Evidence needed to satisfy it | Kind of blocker |
|---|---|---|---|---|
| 2 | "**Q-040** — screening retention of non-metabolic 3-of-5 frameworks is decided" | Q-040 Open | A researcher answer to Q-040: retain non-metabolic 3-of-5 frameworks at screening (e.g., a flag instead of `exclude E4`), or accept that the near-RQ5 group (D-034) covers metabolic and exemplar records only. Q-040 records the risk of the second option: an incomplete near-RQ5 comparison could overstate novelty | **Researcher decision** (documentation only; no network) |
| 3 | "**D-027 and D-024** (screening-file and inventory schemas) are approved" | Both PROPOSED. D-027 is implemented on the branch; D-024 is recommended "APPROVE (conditional on R5)" (`final_confirmation_sheet_LIT-004.md` R1), because D-024 includes the D-029 descriptor fields | Researcher approval of D-027 and D-024 (R1 and v1 Item 1 of the confirmation sheet). D-024 depends on condition 4 | **Researcher decision**; ordering depends on condition 4 |
| 4 | "the remaining **R5/D-029** items (validation design, the required-descriptor rule, triggers) are decided" | D-029 PROPOSED — awaiting explicit approval; not implemented. R5 lines for `dim_explainability`, `dim_uncertainty`, `dim_calibration` and `validation_design` are unanswered. Q-032 (required-descriptor rule) Open. D-026 stays open until D-029 is decided | Researcher choices on R5 (each line: approve / reject / modify / defer) and on D-029 option (a) or (b). Note: for RQ5 component statuses, D-035 §2 already replaces the abstract-statement standard (confirmation sheet, R5 update note) | **Researcher decision**; then implementation (see condition 6, item 8) |
| 5 | "D-031–D-035 are written into `screening_criteria.md` **v1.1** and protocol **v0.2**, frozen as the pilot's `criteria_version`" | Neither document exists; criteria v1.0 and protocol v0.1 are drafts | After conditions 2–4: assistant drafts v1.1 and v0.2 with the approved wording only; the researcher approves and freezes them as `criteria_version` | **Documentation** (assistant drafting) + **researcher approval** to freeze |
| 6 | "the other pilot-blocking items are resolved" | Unmet. Authoritative list: `final_confirmation_sheet_LIT-004.md`, "Pilot-blocking items after confirmation" (see §3) | Each item in §3 resolved | Mixed (see §3) |

## 3. Condition 6 — the other pilot-blocking items

Item numbers are those of `final_confirmation_sheet_LIT-004.md`, "Pilot-blocking items after confirmation". Items 4 and 5 are marked "not pilot-blocking" there and are omitted.

| Item | Wording (abridged from the sheet) | Current state `[EVIDENCE]` | Kind of blocker |
|---|---|---|---|
| 1 | R3 / Q-028 conditions C1–C4 resolved | C2–C4 answered (D-032–D-034); **C1 = R5/D-029 open** | Researcher decision (same as condition 4) |
| 2 | R5 / D-029 definitions all approved | Unanswered | Researcher decision (same as condition 4) |
| 3 | R1 / D-024 and v1 Item 1 / D-027 recorded | PROPOSED | Researcher decision (same as condition 3) |
| 6 | v1 Item 11: the arXiv spot-check runs and passes, so that D-012/D-023 and Q-022 (v1 Item 10) can be recorded | Q-036 Open; D-012, D-023 PROPOSED; Q-022 Open. 88 arXiv records are `partially_verified` pending this check (`verification_report.md`) | **Researcher answer to Q-036**; then **restored raw exports** (Q-063) and an authorised re-fetch through the alphaXiv connector (reachable per `environment_assessment.md`, LIT-001 addendum; the container's direct arXiv API route is blocked) |
| 7 | v1 Items 6–9, 13–15 recorded: scope (Q-001, Q-002/Q-035, Q-033), Q-PM-02 handling (Q-007/D-009), audit (D-008/Q-008), pilot design (D-025/Q-026), amendments A-1/A-2/A-5/A-6 (A-4, A-3) | All Open / PROPOSED. Proposed responses exist (`proposed_owner_responses_LIT-004.md`, summarised in the confirmation sheet); none is recorded | **Researcher decision** |
| 8 | Implementation of D-027 (built), D-028, D-029, `biomarker_class` and the scope flags, with tests and a rebuild that changes no paper ID or existing value | D-028, D-029 PROPOSED and not implemented; `biomarker_class` depends on Q-035 | After the decisions: authorised **code change** with tests, then a **rebuild**, which needs the **restored raw exports** (Q-063) |
| 9 | `screening_criteria.md` v1.1 and protocol v0.2 written and frozen | Not written | Same as condition 5 |

**Additional practical requirement of the pilot** `[EVIDENCE]`: D-025 (PROPOSED) specifies a 60-record pilot with "blinded double screening, pass at κ ≥ 0.60". This needs a second screener or a recorded researcher decision on single screening (`LIT-005_evidence_review.md` §8, step 3).

## 4. Blockers by kind

| Kind | Items |
|---|---|
| **Researcher approval / decision** (documentation only, no network) | Q-040; D-024; D-027; R5 lines and D-029 option; Q-032; D-028; Q-035 (`biomarker_class`); v1 Items 6–9, 13–15 (Q-001, Q-002, Q-033, Q-007/D-009, D-008/Q-008, D-025/Q-026, amendments); Q-036; freezing v1.1/v0.2; Q-065 |
| **Restored raw evidence** (researcher upload of the LIT-003 and LIT-005 archives; not a network change) | The rebuild in item 8; the arXiv spot-check in item 6 (Q-063) |
| **Network access** | **None of the six conditions needs a network change.** The alphaXiv connector already works. Network access (Q-021, Q-064) matters for **citation**, not for screening activation (see §6) |
| **Documentation by the assistant** (after the decisions above) | Drafting criteria v1.1 and protocol v0.2; recording approved decisions in the decision log; preparing the pilot sample only once all conditions are recorded |
| **Authorised code work** (after decisions) | Item 8 implementation and tests |

## 5. Q-065 — screening scope under the deadline (due **2026-11-01**)

- **Question** `[OPEN]` (verbatim gist): accept the LIT-005 priority strand (G-1…G-7 hits, Q-PM-02, Q-PM-11/12; `LIT-005_evidence_review.md` §8) for title/abstract screening first, with the remaining strands screened only if time permits and the reduced scope reported. Q-065 itself says it "requires the D-035 §6 conditions to be met first".
- **Size** `[EVIDENCE]` (LIT-005 §8, step 4): 194 G-1…G-7 PMIDs, Q-PM-02 (743), Q-PM-11/12 (120 unique). Overlap between these groups has not been computed, so about 1,057 is an upper bound.
- **Feasibility**: the Q-065 statement that full screening is not feasible by 2026-11-12 is an assistant estimate `[HYPOTHESIS]`; no workload was measured (Q-065 correction note).
- **Consequence of each answer** `[RECOMMENDATION]`, not a decision: accepting means the review is reported as covering a prioritised subset, with recall limits stated; this is compatible with D-005 (structured review with systematic elements, PROPOSED) only if described as such. Rejecting means full screening of 3,386 records, with a timeline that has to be stated.
- Q-065 can be **decided** before 11-01 even though screening stays inactive; its effect only starts after activation.

## 6. Q-068 and the conflicting verification requirements (not resolved here)

| Record | Requirement for `verified` `[EVIDENCE]` |
|---|---|
| `collection_workflow.md` §4.3 | "≥ 2 distinct sources agree, ≥ 1 is an authoritative index … with a persistent identifier" |
| `search_strategy.md` §7 | Title, first author, year, venue and ≥ 1 persistent identifier from an authoritative index, "consistent with a second source (e.g., PubMed DOI ↔ Consensus/arXiv record, or PMCID full text)"; web-only records are `unverified` |
| `research_plan.md` §6 | Same as `search_strategy.md` §7; only `verified` records may be cited |
| `verification_report.md` (generated) | The 14 `verified` records used "a web-search result whose URL carried the same DOI or PMCID" as the second source; "agreement covers title and identifier only" |

- Q-068 `[OPEN]` asks which rule applies, with options (a) accept as is, (b) accept only with full field agreement, (c) not accepted. Q-021 `[OPEN]` and Q-064 `[OPEN]` ask which second-source route to use.
- **Relevance to screening**: none of the three blocks screening activation (`partially_verified` records may be screened; `research_plan.md` §6). All three block **citation** in any project document or manuscript.
- This brief does not choose among the options.

## 7. The 2026-11-24 manuscript target

**Facts** `[EVIDENCE]`
- Today is Day 16 (2026-10-29). The protocol draft's milestone table (`experimental_protocol_v0.1_draft.md` §23, `[RECOMMENDATION]`, D-001 PROPOSED) planned researcher decisions for 10-25 → 10-28 and protocol v0.2 for 10-28 → 10-31. Neither has happened: D-013 to D-020 are PENDING and protocol v0.2 does not exist.
- Model training is not permitted before 2026-11-03 and not before D-019 is approved (`CLAUDE.md` rule 13; `GOVERNANCE.md` §2).
- `GOVERNANCE.md` §2: "No stage is skipped to meet the deadline." Stage C's gate is "Comparison reviewed by researcher"; Stage D's gate is "Gap + main contribution approved" (D-016).
- Proposed D-041 (`CLAUDE.md` §1a, uncommitted): acceptance "never justifies skipping a stage or gate".
- The NHANES raw files used by the protocol draft are absent from this container (`data/raw/nhanes/` does not exist).
- Q-013 (schedule slip) and Q-058 (11-24 compresses Stage J) are Open.

**Remaining work before a defensible manuscript, in gate order**
1. Screening activation (§2–§3) → pilot (D-025) → priority or full screening (Q-065) → full-text review of priority records (LIT-005 §8, step 5).
2. A verification route for every cited record (Q-021, Q-064, Q-068).
3. Stage C comparison reviewed; Stage D gap and contribution approved (D-016), including the closest-prior-art review (D-031–D-038).
4. Stage E/F: D-013, D-014, D-015, D-017, D-018, outcome definition; protocol frozen (D-019).
5. Stages G–J under the frozen protocol, then the manuscript.

**Assessment** `[HYPOTHESIS]`, not measured: a complete, defensible manuscript by 2026-11-24 that passes every gate above is unlikely. Screening is not yet active, no literature is citable, and the Stage C–F decisions are pending, with 26 calendar days left. Nothing in this assessment weakens a gate. The options belong to the researcher (D-001, Q-013, Q-058):
- (a) keep 2026-11-24 for an interim deliverable (e.g., a review chapter and methods draft) and set the submission date after Stage J;
- (b) keep the date with the reduced literature scope of Q-065, reported transparently; this still does not lift any gate;
- (c) revise D-001 to a later end date.

**Observation on gate order** `[OPEN]` (Q-069): protocol §23 schedules the D-019 freeze (11-01 → 11-02) and Stage G (from 11-03) before Stage C and Stage D can pass, and protocol §26 (blocker checklist) lists D-016 as "Not blocking training, but needed before submission". `GOVERNANCE.md` §2 lists the stages with gates in order A → J and forbids skipping. Whether Stage E/G work may run in parallel with Stages C–D is not stated in either record.

## 8. Recommended next actions, in dependency order `[RECOMMENDATION]`

| Step | Action | Who | Depends on | Unblocks |
|---|---|---|---|---|
| 0 | Decide whether to commit and push the uncommitted work (SECOND-SOURCE-ACCESS-RECHECK, RESEARCH-AMBITION-D041, this brief); the container is ephemeral | Researcher | — | Preservation |
| 1 | Decide Q-065 (due 11-01) and the schedule question (D-001, Q-013, Q-058, Q-069) | Researcher | — | Scope of everything below |
| 2 | Decide R5 lines and D-029 option; Q-032 | Researcher | — | Condition 4; D-031 C1; item 1–2 |
| 3 | Decide Q-040 | Researcher | — | Condition 2 |
| 4 | Approve or amend D-024 (after step 2) and D-027; decide D-028 and Q-035 | Researcher | Step 2 | Condition 3; item 3 |
| 5 | Record v1 Items 6–9, 13–15 (scope, Q-PM-02, audit, pilot design, amendments) | Researcher | — | Item 7 |
| 6 | Decide Q-036 | Researcher | — | Item 6 |
| 7 | Upload both raw-export archives for restoration (Q-063) | Researcher | — | Items 6 and 8 |
| 8 | Implement D-028/D-029/`biomarker_class`/scope flags with tests; rebuild with no paper-ID change | Assistant, when authorised | Steps 2, 4, 7 | Item 8 |
| 9 | arXiv transcription spot-check via alphaXiv | Assistant, when authorised | Steps 6, 7 | Item 6; then D-012/D-023/Q-022 can be recorded |
| 10 | Draft `screening_criteria.md` v1.1 and protocol v0.2 with approved wording only | Assistant, when authorised | Steps 2–5 | Condition 5 |
| 11 | Approve and freeze v1.1/v0.2 as `criteria_version`; record screening activation | Researcher | Steps 8–10 | Pilot |
| 12 | Pilot (D-025), with a second screener or a recorded single-screener decision | Researcher + assistant | Step 11 | Screening |
| Parallel | Decide Q-021, Q-064, Q-068; optionally allow-list `api.crossref.org`, `www.ebi.ac.uk` | Researcher | — | Citation (not screening) |

## 9. Screening status

**Screening remains INACTIVE.** This brief does not activate screening, generate a pilot sample, assign any label or theme, or change any decision or question status. Activation requires all of conditions 2–6 to be met and recorded by the researcher.

## 10. Unresolved questions referenced
Q-001, Q-002, Q-007, Q-008, Q-013, Q-021, Q-022, Q-026, Q-032, Q-033, Q-035, Q-036, Q-040, Q-058, Q-063, Q-064, Q-065, Q-068 (all Open), and Q-069 (new, Open; added with this brief).

## 11. Status update — 2026-10-30 (SCREENING-READINESS-RECHECK)
Added 2026-10-30 at the researcher's request to accelerate the review toward an interim deliverable on 2026-11-02. Sections 1–10 are unchanged as the record of 2026-10-29. **Nothing is activated, approved or decided by this section.**

### 11.1 What changed since 2026-10-29 `[EVIDENCE]`
| Item | Then | Now |
|---|---|---|
| Q-065 (screening scope) | Open | Answered → **D-044** (APPROVED — CONDITIONAL, inactive for screening): 1,470 records; takes effect only after D-035 §6 is met |
| Q-069 (stage order) | Open | Answered → **D-042** (APPROVED): Stage C and Stage D gates before D-017–D-019 and training; "screening remains inactive" |
| Schedule | D-001 PROPOSED | **D-045** (APPROVED): 2026-11-24 retained as an interim deliverable date; no model results promised; schedule revised after the pilot. A 2026-11-02 interim deliverable is **not** recorded in `DECISION_LOG.md` |
| Raw exports (§1 fact 5) | Absent | **Restored** in this workspace (244/244; `pubrecords.py verify` OK, 2026-10-30). Q-063 Open; the files exist only in this workspace |
| Inventory | 3,386 `not_screened` | Unchanged: 3,386 `not_screened`; verification 14 `verified`, 3,334 `partially_verified`, 37 `unverified`, 1 `needs_review`; `paper_inventory.json` SHA-256 `a509538d…f4a3` (equal to the D-044 value) |

### 11.2 D-035 §6 conditions now
| # | Condition | State |
|---|---|---|
| 1 | Q-039 | **Met** (D-036) |
| 2 | Q-040 decided | **Unmet** (Q-040 Open) |
| 3 | D-027 and D-024 approved | **Unmet** (both PROPOSED) |
| 4 | Remaining R5/D-029 items decided | **Unmet** (D-029 PROPOSED; Q-032 Open) |
| 5 | `screening_criteria.md` v1.1 and protocol v0.2 frozen | **Unmet** (not written) |
| 6 | Other pilot-blocking items (§3) | **Unmet**; item 6 (arXiv spot-check, Q-036) and item 8 (implementation and rebuild) no longer need an archive upload, because the raw exports are restored in this workspace |

**Conclusion:** screening is **not** authorised under current governance (D-035 §6; D-044 "inactive for screening"; D-042 item 4). No record may be screened, labelled or sampled for the pilot yet.

### 11.3 Smallest unblocking path `[RECOMMENDATION]`
| Order | Action | Who | Governance record | Unblocks |
|---|---|---|---|---|
| 1 | Decide R5 lines and the D-029 option; answer Q-032 | Researcher | D-029, Q-032; `final_confirmation_sheet_LIT-004.md` R5 | Condition 4; D-031 C1; items 1–2 |
| 2 | Answer Q-040 | Researcher | Q-040; D-034 | Condition 2 |
| 3 | Approve or amend D-024 and D-027; decide D-028 and Q-035 | Researcher | D-024, D-027, D-028, Q-035 | Condition 3; item 3 |
| 4 | Record v1 Items 6–9, 13–15 and the pilot screener arrangement (second screener or a recorded single-screener decision) | Researcher | Q-001, Q-033, Q-007/D-009, D-008/Q-008, D-025/Q-026 | Item 7; pilot feasibility |
| 5 | Decide Q-036; then the arXiv spot-check via the alphaXiv connector, using the restored raw exports | Researcher, then assistant when authorised | Q-036; D-012, D-023, Q-022 | Item 6 |
| 6 | Implement D-028/D-029/`biomarker_class`/scope flags with tests; rebuild (no paper-ID change) while the raw exports are still in this workspace | Assistant when authorised | Item 8 | Item 8 |
| 7 | Draft criteria v1.1 and protocol v0.2 with approved wording only; researcher approves and freezes; record activation | Assistant drafts; researcher freezes | Condition 5; item 9 | Pilot (D-025), then screening of the 1,470 D-044 records |
| Parallel | Decide Q-021, Q-064, Q-068 | Researcher | — | Citation (not screening) |

Steps 1–4 are documentation-only researcher decisions with prepared options in `owner_review_ballot_LIT-004.md`, `final_confirmation_sheet_LIT-004.md` and `proposed_owner_responses_LIT-004.md`. They can be taken in one session.

### 11.4 What a 2026-11-02 interim deliverable can honestly contain `[RECOMMENDATION]`
- Recorded decisions from steps 1–4, and drafts of criteria v1.1 and protocol v0.2 (step 7 drafting), if the decisions are made in time.
- Search and inventory documentation already in the repository (3,386 records; 1,470 in the D-044 scope; verification counts above).
- **Not** screening results, included-study counts, a Stage C comparison, a gap or novelty claim, citable references (Q-021/Q-064/Q-068 open), or any model result.
