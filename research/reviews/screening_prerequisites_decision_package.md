# Screening prerequisites — recommendations and approval request (2026-10-30)

| Field | Value |
|---|---|
| Task | SCREENING-PREREQ-DECISIONS (2026-10-30; assistant label, no researcher task ID) |
| Status | **Recommendations for the owner's explicit approval.** Nothing in §2–§4 is approved, recorded or implemented. Only the selections in §1 were recorded (`logs/DECISION_LOG.md`, D-055–D-057 and Status history) |
| Built from | `logs/DECISION_LOG.md`; `research/reviews/unresolved_questions.md`; `owner_review_ballot_LIT-004.md` (Ballot); `final_confirmation_sheet_LIT-004.md` (Sheet); `proposed_owner_responses_LIT-004.md` (Proposed); `screening_activation_decision_brief_D035.md` (Brief, incl. §11); `Q-041_decision_record_D035.md` §2, §6; `RQ5_component_decisions_D032-D034.md` |
| Criteria used | Reproducibility, completeness, traceability, screening consistency, resistance to bias, fair comparison. Not: making the proposed framework look better |
| Labels | `[RECOMMENDATION]` = assistant proposal, not approval (`CLAUDE.md` rule 7). `[EVIDENCE]` = stated in a cited record |

The researcher's general instruction to prefer publication-quality options is **not** treated as approval of any line below. Each line needs an explicit owner answer (§5).

## 1. Recorded on 2026-10-30 (researcher selections in the prompt of 2026-10-30)

| Item | Recorded as | Status | Not established by it |
|---|---|---|---|
| Q-040 | D-055 | APPROVED — CONDITIONAL (inactive for screening) | Flag name and rule (to be written into criteria v1.1, A-2) |
| Q-001 | D-056 | Same | D-013 (primary disorder); tag rename `scope_pending_disorder` |
| Q-033 | D-057 | Same | — |
| D-027 | Status history; row updated | APPROVED (limited): file, required columns, `source_record:<id>` key | Optional descriptor columns (D-028, D-029, Q-035); part (b) (with D-024) |
| D-008 / Q-008 | Status history; row updated | APPROVED — CONDITIONAL (inactive for screening) | That the audit has been done (it has not) |
| Q-036 | Answered; D-012/D-023 unchanged | D-012, D-023 stay PROPOSED | That the arXiv spot-check ran or passed (it has not run) |
| Q-011 / D-010 | D-010-APPROVAL (earlier the same day) | D-010 APPROVED; Q-011 Answered | Date and wording of the WhatsApp approval; PRESERVED status; Q-063 (Open) |

## 2. Recommendations on the remaining decisions `[RECOMMENDATION]`

### 2.1 Q-035 / ballot Item 7 — `biomarker_class`
- **Options (Ballot Item 7):** (a) both strands plus `biomarker_class` (`metabolomics_lipidomics / newborn_screening_msms / routine_chemistry / mixed_both / other / unclear`); (b) both strands without the field ("strand = retrieval theme; not recommended"); (c) one strand only — **excluded** by D-043 (APPROVED: both strands, distinct).
- **Recommend: (a).** D-043 requires the two categories to be discussed separately. Without a content field, strand membership would rest on which query retrieved a record, which is not evidence of content and is not reproducible as a classification. Risk: one more judgement per record; its agreement is measured in the pilot (per-descriptor agreement, Item 14). Reporting note: totals should count unique records, with `mixed_both` shown in both strands **and** as its own row, so no record is double-counted in a total.
- **Depends on:** D-057 (done). **Feeds:** D-029 required fields, D-024, criteria v1.1.

### 2.2 D-028 / ballot Item 2 — record-type fields (four separate lines)
| Line | Options | Recommend | Benefit | Risk |
|---|---|---|---|---|
| 2a roles and mapping table | Approve / reject / modify / defer | **APPROVE** | Source metadata kept verbatim; normalised type derived only by a versioned table; 0 unmapped types in current data `[EVIDENCE]` (Ballot 2a) | Table must be extended by logged change only |
| 2b arXiv source rule (arXiv → `preprint`) | Same | **APPROVE** | Uses source metadata (which index), not a heuristic; 76 arXiv records otherwise `unknown` | None material |
| 2c URL / DOI-prefix rules | Same (the line approves "no URL/DOI rules") | **APPROVE the "no rules" line** (i.e. reject heuristics) | Avoids inferring type from patterns | Some records stay `unknown` (honest) |
| 2d `record_type` values | Same | **APPROVE** `original, methodological, software, guideline, review_lead, other` | Removes overlap with `publication_type` | — |
- **Depends on:** D-024 (schema), D-025 (protocol §2 list), D-030 (notices; not pilot-blocking for current data).

### 2.3 D-029, R5 and Q-032 — screening descriptors
| Line (Sheet R5 / Ballot Item 3) | Options | Recommend | Reason |
|---|---|---|---|
| D-029 design (Ballot Item 3) | (a) three yes/no/unclear method descriptors + separate `validation_design`; (b) keep D-026 `dim_independent_validation` scale; (c) four yes/no/unclear + `validation_design` ("not recommended") | **(a)** | (c) duplicates and can contradict the design; (b) cannot express `none` / `not_applicable`, so apparent-performance studies are indistinguishable from unstated designs |
| `validation_design` | external / temporal / internal_only / none / not_applicable / unclear; strongest stated design recorded | **APPROVE** | Directly supports fair comparison: results are later compared only within comparable validation designs |
| Common rules (silence = `unclear`; missing abstract → descriptors `unclear`, decision `uncertain` unless a title-level reason applies) | Approve / reject / modify / defer | **APPROVE** | Reading silence as `no` would bias prevalence toward absence and bias the Stage D gap (Ballot Item 3) |
| Human-review triggers 1–5 | Same | **APPROVE** (trigger 3 as amended by the next line) | Ambiguous terms, unclear validation, potential RQ5, retained no-abstract records, pilot disagreements all get a human check |
| RQ5 handling of ambiguity | Approve / approve (conditional on R3) / reject / modify / defer | **MODIFY** (wording below) | The Sheet text predates D-031 (≥ 4 of 5), D-034 (`near_rq5` = exactly 3), D-035 G2 (title/abstract statuses are triage only and never count) and D-055 (non-metabolic three-of-five retained). As written, "potential RQ5" uses only the D-031 threshold, so a record with two `yes` and one `unclear` (a possible `near_rq5`) could be excluded before full text, which would make the D-034 near-RQ5 group incomplete |
| `dim_explainability`, `dim_uncertainty`, `dim_calibration` | Approve / reject / modify / defer | **APPROVE as title/abstract triage descriptors** | D-035 §2 already governs RQ5 component statuses (recorded precedence); these lines only route records. Keeping them avoids a second, undefined title/abstract standard |
| Q-032: enforce descriptors for `include` and `uncertain` | Enforce / do not enforce | **Enforce** | Completeness and traceability: an `include` without descriptors cannot be audited or used for triage |

**Proposed MODIFY wording (RQ5 handling of ambiguity):**
> At title/abstract, descriptors are used for triage only and never count toward D-031 or D-034 (D-035 G2). A record is routed to full text (`uncertain`, `needs_human=yes`) if counting its `unclear` components as `yes` would give **three or more** of the five components, the D-034 `near_rq5` floor, so that both `qualified` and `near_rq5` candidates reach full text; this applies equally to records retained under D-055. Coverage groups are derived only from full-text-confirmed statuses (D-034, D-035 G3). Feature selection and classification are read from the abstract and justified in writing.

Benefit: completeness of both RQ5 groups (protects the later novelty assessment against missed prior art). Risk: more full-text work; size unknown until screening.

### 2.4 D-024 / R1 — inventory schema
- **Options (Ballot Item 17):** (a) D-024 with Items 2 and 3 revisions and the Q-034 enum; (b) D-024 as it stands; (c) defer. Sheet R1 adds "APPROVE (conditional on R5)" and states that R1 does not approve Q-034.
- **Recommend:** APPROVE D-024 with the D-028 and D-029 revisions, **conditional on R5**, with **Q-034 decided separately** (R2; not pilot-blocking, needed before extraction). This is option (a) without the Q-034 enum, as `proposed_owner_responses_LIT-004.md` §17 records it.

### 2.5 Q-007 / D-009 — Q-PM-02 (743 records)
- **Options (Ballot Item 9):** (a) screen all 743; (b) screen only records also matching method terms and characterise the rest by a sample.
- **Recommend: (a).** (b) is a post-search restriction and would also **amend the approved D-044 scope** (all Q-PM-02 records are in the 1,470), which needs its own decision. **Needs evidence:** verify the MeSH "Metabolic Diseases" tree before the limitations are written.

### 2.6 D-025 / Q-026 — pilot design and second screener
- **Options (Ballot Item 14):** (a) protocol §7 design (60 records, stratified, seed 4004, blinded independent screening by the assistant **and the owner**, pass at 3-level κ ≥ 0.60 with no unadjudicated include/exclude conflict, < 3 disagreements on any code); (b) criteria §7 pilot (first 30 PMIDs of Q-PM-01 and Q-PM-09); (c) modify.
- **Recommend: (a), with the owner as the blinded second screener.** κ needs two independent screeners; (b) samples two queries only. **Needs a person:** the owner's blinded screening of 60 records. A single-screener pilot is not among the options; it would need a recorded exception and κ could not be reported.

### 2.7 Criteria amendments A-1 to A-6 (Ballot Item 15)
| ID | Prerequisite | Prerequisite state | Recommend |
|---|---|---|---|
| A-1 pilot per protocol §7 | D-025 | Open | **Approve together with D-025 (a)**, not before |
| A-2 code clarifications | Q-040 (E4 clause) | Decided (D-055) | **MODIFY**: as proposed, except E4 reads "non-metabolic, unless a method exemplar **or retained under D-055 (flag, not E4)**"; other clauses (E3, E5, E6, E8, E12) approve |
| A-3 descriptors and RQ5 counting rule | D-029/R5; D-031 | R5 open; D-031 decided | **Approve together with R5** |
| A-4 secondary version → E8 | D-030 / R4 | Open | **DEFER with D-030** (the A-2 E8 clause already limits E8 to recorded dedup/version decisions; Q-024 pairs are deferred until after the pilot) |
| A-5 one screening file | D-027 | Approved (limited) | **APPROVE** |
| A-6 no abstract → `uncertain` | R5 common rules | Open | **Approve together with R5 common rules** |

## 3. D-035 record §6 activation conditions (2026-10-30)

| # | Requirement | Current evidence | Status | Exact next action |
|---|---|---|---|---|
| 1 | Q-039 — classification status column | D-036 (APPROVED — CONDITIONAL) | **Met** | — |
| 2 | Q-040 decided | D-055 recorded 2026-10-30 | **Met at decision level**; flag rule still to be written (A-2, condition 5) | Approve A-2 as modified (§2.7) |
| 3 | D-027 and D-024 approved | D-027 APPROVED (limited) 2026-10-30; D-024 PROPOSED | **Unmet** (D-024) | Approve D-024 per §2.4 (after R5) |
| 4 | Remaining R5/D-029 items decided | D-029 PROPOSED; R5 lines unanswered; Q-032 Open | **Unmet** | Answer §2.3 lines |
| 5 | Criteria v1.1 and protocol v0.2 written, frozen as the pilot's `criteria_version` | Not written | **Unmet** | Assistant drafts after §5 answers; owner reviews and freezes |
| 6 | Other pilot-blocking items (Sheet list) | Item 1 (D-031 C1 = R5): unmet. Item 2 (R5): unmet. Item 3 (D-024/D-027): D-024 unmet. Item 6 (arXiv spot-check): authorised (Q-036), **not run**. Item 7 (ballot Items 6–9, 13–15): 6 met (D-056), 7 open (Q-035; Q-002 met by D-043), 8 met (D-057), 9 open (Q-007), 13 met (D-008), 14 open (D-025), 15 open (A-1–A-6). Item 8 (implementation + rebuild): not done. Item 9 (= condition 5): unmet | **Unmet** | §5 answers; spot-check run; authorised implementation and rebuild |

**Screening remains INACTIVE.** No condition is treated as met because a choice was discussed.

## 4. Critical path `[RECOMMENDATION]`

**Allowed now (no further decision):**
- The arXiv transcription spot-check (≥ 10 % re-fetch of the 5 arXiv raw files via the alphaXiv connector, against the restored raw exports): authorised by the Q-036 answer. Result to be recorded as observed (pass or fail).
- Committing and pushing the uncommitted records (needs the researcher's commit and push authorisation).
- Verifying the MeSH "Metabolic Diseases" tree for the Q-PM-02 limitation text (documentation only).

**Blocked until the §5 answers:** recording D-024, D-028, D-029, Q-032, Q-035, Q-007, D-025, A-1–A-6; drafting v1.1/v0.2.

**Earliest point to draft criteria v1.1 and protocol v0.2:** immediately after the §5 answers are recorded (they supply all wording v1.1 needs; D-030/A-4 can stay deferred because E8 is already limited by A-2).

**Then:** authorised implementation of D-028, D-029, `biomarker_class`, the D-055 flag and scope flags, with tests and a rebuild that changes no paper ID (the raw exports are in this workspace now, Q-063) → owner reviews and freezes v1.1/v0.2 → activation recorded → pilot (owner's blinded 60 records) → screening of the 1,470 D-044 records in batches.

**Realistic content of a 2026-11-02 interim deliverable:** the recorded decisions; the spot-check result; drafts (or frozen versions, if reviewed in time) of criteria v1.1 and protocol v0.2. Not: screening counts, included studies, Stage C comparison, a gap or novelty claim, citable references (Q-021, Q-064, Q-068 open), or model results. D-045 keeps 2026-11-24 as the recorded interim date; 2026-11-02 is not recorded.

## 5. Approval request (copy, edit and return)

> I approve the following, as worded in `research/reviews/screening_prerequisites_decision_package.md` §2:
> - Q-035: option (a) [yes / no / other: …]
> - D-028: 2a [ ], 2b [ ], 2c "no URL/DOI rules" [ ], 2d [ ]
> - D-029: option (a) [ ]
> - R5: `validation_design` [ ]; common rules [ ]; triggers 1–5 [ ]; RQ5 ambiguity as MODIFIED in §2.3 [ ]; `dim_explainability` [ ], `dim_uncertainty` [ ], `dim_calibration` [ ] as title/abstract triage descriptors
> - Q-032: enforce for `include` and `uncertain` [ ]
> - D-024: with D-028/D-029 revisions, Q-034 separate [ ]
> - Q-007 / D-009: option (a), screen all 743 [ ]
> - D-025 / Q-026: option (a), with me as the blinded second screener [ ]
> - A-1 [ ], A-2 as MODIFIED [ ], A-3 [ ], A-4 DEFER with D-030 [ ], A-5 [ ], A-6 [ ]
> Changes: …

Unanswered lines stay PROPOSED/Open.

## 6. Update 2026-10-30 (SCREENING-PREREQ-DECISIONS-3): review summary for criteria v1.1 and protocol v0.2

§1–§5 above are kept as written. Since then: D-058–D-060 (delegated selection), D-061 (OPEN-1) and D-062 (OPEN-2) were recorded; D-012/D-023 approved after the arXiv spot-check passed (25/25) and the outcome was written to `MANIFEST.csv`.

### 6.1 What changes from v1.0 / v0.1 (for the researcher's review)
| Area | Change | Decision |
|---|---|---|
| Records screened | 1,470 (D-044) instead of the whole inventory; all 743 Q-PM-02 records | D-044, D-009 |
| Disorders | Main list approved; obesity, thyroid dysfunction, PCOS pending (`scope_pending`) | D-056 |
| Biomarkers | Two strands; proteomics pending (`scope_pending_proteomics`); new `biomarker_class`; totals count records once | D-043, D-057, D-058 |
| Codes | E3/E5/E6/E8/E12 clarified; E4 not applied to method exemplars or to `non_metabolic_rq5_candidate` records; A-4 deferred | D-059, D-055, D-061 |
| RQ5 | ≥ 4 of 5 components, full-text-confirmed; routing to full text at ≥ 3 counting `unclear`; tier rule | D-031–D-038, D-060, D-062 |
| Descriptors | Required for `include`/`uncertain`; silence ≠ `no`; missing abstract → `uncertain`; `validation_design`; `record_type` list | D-028, D-029, D-060 |
| Pilot | 60, seed 4004, researcher as blinded second screener; strata **open (Q-073)** | D-025, D-059 A-1 |
| Audit | 25 + 25 blinded, after the first two batches | D-008 |

Consistency check (2026-10-30): every decision ID cited in the two drafts exists in `DECISION_LOG.md` (32 each), and every question ID exists in `unresolved_questions.md`.

### 6.2 Still needed before the freeze
1. **Q-073** (researcher): pilot allocation. Recommended: near-equal (B, A, untagged, F 8 each; C, E, D, Q 7 each), reproducible draw as in protocol v0.2 §7.
2. **Implementation** of D-028, D-029/D-060, D-058, D-061 with tests, then a rebuild (separate authorised task; see §6.3).
3. Researcher review and freeze of v1.1 / v0.2; then activation recorded.

### 6.3 Implementation readiness `[RECOMMENDATION]`
- **Q-034 is not a prerequisite:** `extraction_status` is not touched by D-028, D-029, D-058 or D-060; D-024 was approved without it.
- **Decision prerequisites are met** (D-024 conditional with its R5 condition met; D-028, D-029/D-060, D-058 approved; D-061 effective at freeze).
- **Not implemented in this task**, for two reasons:
  1. a rebuild regenerates the committed inventory, so the `paper_inventory.json` SHA-256 recorded in D-044 (`a509538d…f4a3`) will change. Before the rebuild, the 1,470 `paper_id`s should be written to a committed scope list so that D-044's membership stays checkable after it;
  2. the rebuild also applies the recorded spot-check, which may move P2870 and P2941 to `verified` under the rule Q-068 questions.
- **Recommended order:** commit the current work → write the D-044 scope list → implement with tests → rebuild and confirm that no `paper_id` changes and that the 1,470 set is identical → review the verification-status changes.
