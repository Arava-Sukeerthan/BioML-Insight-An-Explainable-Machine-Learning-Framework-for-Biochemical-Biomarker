# Final independent review — screening criteria v1.1 and screening protocol v0.2 (2026-11-11)

> **Nature of this report.** This is an independent methodological and governance review by the assistant. **It is not an approval, a freeze or an activation** (`CLAUDE.md` rule 7). It changes no decision status, closes no question and modifies neither reviewed document.
>
> **Labels:**
> - `[EVIDENCE]`: checked in this review by reading the cited text, or by a command whose output is reported;
> - `[HYPOTHESIS]`: a reasoned judgement that is not proven;
> - `[RECOMMENDATION]`: a suggestion for the researcher, not applied;
> - `[OPEN]`: undecided.
>
> Passing software tests are **not** evidence of scientific validity.

## Section 1 — Executive summary
**Overall.** Criteria v1.1 and protocol v0.2 are scientifically coherent and carefully conservative at the decision level:
- "when in doubt → `uncertain`";
- "silence is never `no`";
- no exclusion because an abstract is missing;
- full-text confirmation for RQ5.

They are internally consistent on decision IDs, codes, the identifier and the freeze wording. **They are suitable for your content approval**, provided you knowingly accept the scientific limitations below. None of these limitations needs a rule change before the freeze. Several should be stated or decided before screening.

**Major findings (most important first):**
1. **Scope versus the research questions** (criteria §0, §3; protocol §1). The approved D-044 scope excludes the dedicated RQ2, RQ3, RQ4 and RQ6 search strands (Q-PM-04 to Q-PM-10, Q-PM-13, Q-PM-14). The criteria still define full inclusion rules for RQ2a, RQ3a, RQ4b and RQ6, which will therefore be met only by records retrieved incidentally through the RQ1, RQ5 and G queries. Neither document says so explicitly; they say only that "the review reports the reduced scope". This is a **methodological concern and a researcher decision**: state it in the texts, or accept it as a reporting obligation.
2. **The wording of RQ1–RQ6 is not part of the reviewed documents.** It lives in `search_strategy.md` §1.2 (DRAFT, "pending researcher approval"). Its RQ5 sentence still omits probability calibration, although the 2026-10-24 note there says it "is to be aligned when criteria v1.1 is written". Criteria v1.1 operationalises RQ5 with five components (calibration included), so the operational definition and the question text differ. **Governance inconsistency (outside the two texts); a researcher decision.**
3. **A single AI screener for the main screening** (D-008; acknowledged in `search_strategy.md` §1.3). Dual screening applies to 60 pilot records only, and the D-008 audit (25 + 25) is small. The documents describe this correctly. It is the main **screening-bias risk**, and it limits what the review may claim ("structured literature review with systematic elements", not a systematic review).
4. **Reproducibility of the AI screener.** Neither text requires recording the assistant's model identifier or version, or the screening instructions used, for each batch. R1 mentions "same model and tools" for the pilot custodian only. Another researcher could reproduce the *rules* but not the *assistant's decisions*. `[RECOMMENDATION]`: researcher decision.
5. **Tier 3 inclusion at abstract level** (criteria §5, unchanged since v1.0). Tier-3 RQ1 records are "coded from the abstract; full text read for a random sample only". Some RQ1 includes are therefore never confirmed at full text. This affects the validity of RQ1 counts and descriptors. **Methodological concern; a researcher decision** (state it as a limitation, or require full text).
6. **Q-082** (retracted articles without the PubMed type) may stay open at the freeze (D-083). Its "Needed by" is "before such a record is screened", but such a record cannot be recognised in advance, and it could appear in the pilot sample. `[RECOMMENDATION]`: decide it before the pilot.
7. **D-102 clause (1)** (a salt line in the decision CSV) is still the approved, conditional text. It cannot be implemented, and protocol §7a step 5 correctly marks the revision as pending. The protocol no longer states the **independent-custodian requirement** of D-102 (3), nor that R1 needs a D-096 extension; both were moved to the pending revision. This is not an error, but it is a gap for a reader of the protocol alone.
8. **The previous audit's D-099 correction is stricter than D-099.** The approval package now says D-099 steps (3) and (4) are needed "before step 4" (the first authorisation). D-099 says "before the first authorised run", which is step 5. **Governance inconsistency (minor)** in the package; the two reviewed texts are correct (protocol §7).
9. **P1 (the D-102 status-cell date)** is safe to apply **only as a statement of fact**: the date coincides with the recorded approval, and no freeze exists. It must not be applied as a claim about what the writer meant (Section 5.3).
10. **Minor documentation errors:**
    - protocol §1 says abstracts are "restorable from the verified archives". The archives hold raw exports; abstracts are recovered by a rebuild after restoring them;
    - `biomarker_class` has no value for proteomics, although proteomics is a pending in-scope class;
    - the `validation_design` = `external` definition lists "public dataset" without requiring separation from the development data (compare `research_integrity.md` §11).

**Freeze.** After your explicit decisions, the freeze can proceed:
- content approval of both texts;
- approval of the amended §11 (D-084);
- your position on D-107;
- the freeze-entry ID and dates;
- Git authorisation.

**Activation and operation remain blocked.** See Section 12.

## Section 2 — Files and evidence inspected
| File | Version or state | SHA-256 (2026-11-11, at the start of this review) |
|---|---|---|
| `research/literature/screening_criteria_v1.1.md` | 222 lines; FINAL DRAFT, uncommitted changes on top of HEAD `c6e1b14` | `748a731349081480c9daa45eb5b2b76e7e8274bb2a19541288ea4194e7802e52` |
| `research/literature/screening_protocol_v0.2.md` | 165 lines; FINAL DRAFT, uncommitted | `775b20055c30d20d72bf20893270e44387270e256461dd1dd4ff73f279d74e68` |
| `research/reviews/2026-11-11_FINAL-PRE-FREEZE-ISSUE-RESOLUTION.md` | primary governance reference (uncommitted) | — |
| `logs/DECISION_LOG.md` | rows for D-008, D-009, D-025, D-031, D-035, D-044, D-063, D-074, D-077, D-083, D-084, D-088, D-091–D-109, and the 2026-11-11 status-history rows | — |
| `research/reviews/unresolved_questions.md` | Q-082 to Q-085, Q-092, Q-096, Q-097 | — |
| `research/reviews/final_pre_freeze_approval_package_2026-11-11.md` | sections A–H | — |
| Session log `2026-11-11_B1-B6-APPROVALS.md` | for P1 | — |
| `research/literature/search_strategy.md` §1.2–1.3; `research_plan.md` §1–2; `search_queries.csv` (`rq` column) | RQ wording; query-to-RQ mapping | — |
| `research/methodology/research_integrity.md` §11 | the meaning of external validation | — |
| `scripts/literature/pilot_agreement.py`; `tests/literature/test_phase1_screening_tools.py` | D-098 implementation | — |

**Evidence limitations:**
- **Not inspected:** no research-record content, no abstract, and not the private D-035 record files beyond what the decision log quotes.
- **R1/R2 design notes:** the R1 text exists in this repository only as the copy in the previous audit report §5.2. The A3 design notes are scratch files outside the repository.
- **Researcher-reported facts** (the Google Drive hashes) were not verified.
- **Logs not updated:** by instruction, this review creates one file only, so `CHANGELOG`, `PROMPT_LOG`, the daily review log and a session log were **not** updated. This departs from `CLAUDE.md` §3.3 under your explicit instruction for this task.

## Section 3 — Scientific criteria review

### 3.1 Research scope (criteria §0, §2) `[EVIDENCE]`
- **Disorders (§2.1):**
  - In-scope, pending (obesity, thyroid, PCOS; flagged `scope_pending_disorder`) and out-of-scope categories are distinguishable.
  - Complications are out of scope when they are themselves the target. This is a clear rule, but it needs judgement for composite targets (e.g., "diabetes with nephropathy risk"). `[HYPOTHESIS]` moderate disagreement risk, which the pilot should show.
- **Obesity as a target** is pending while obesity-related metabolic syndrome is in scope. Clear enough with the flag.
- **Biomarkers (§2.2):**
  - The in, pending (proteomics, `scope_pending_proteomics`) and out (E3) classes are clearly listed.
  - **Concern:** the mixed-feature rule ("stated, or ≥ 1 biochemical marker among the final predictors") sets a very low bar. One routine laboratory value among many clinical variables qualifies. At title/abstract, the final predictors are often not reported, so `uncertain` follows, which is correct but costly.
  - **Terminology gap:** `biomarker_class` has no proteomics value. A proteomics-only included record would be coded `other`, which loses the D-057 distinction.
- **Proteomics:** handled consistently as pending in criteria §2.2, §6 (`scope_flags`) and protocol §3.

### 3.2 Inclusion I-C1 to I-C4
| Code | Assessment |
|---|---|
| I-C1 | Clear. "Preprints flagged; published version preferred" depends on version linking, which is deferred (D-030), so both versions are screened and may be **double counted** in the synthesis until D-030 is decided (DEFERRED) |
| I-C2 | "Abstract sufficient for the extraction fields of the relevant RQ" cannot be fully judged at title/abstract, because full-text availability is unknown. In practice it is applied as E9 at full text. Acceptable, but it is **not objective at stage 1**; the "doubt → `uncertain`" rule covers it |
| I-C3 | Clear; E6 applies only to records that are themselves non-English, and missing language is not E6 (good) |
| I-C4 | **Ambiguity with RQ6.** I-C4 admits reviews "only as lead sources (`record_type=review_lead`)", but RQ6 includes "systematic/scoping reviews, meta-research" as primary evidence, and only *narrative* reviews without methodological content are restricted to `review_lead`. The `record_type` vocabulary has no value for an RQ6 systematic review other than `review_lead` or `other`. Two screeners could code the same systematic review differently. **Researcher decision** (clarify I-C4 versus RQ6) |

### 3.3 Exclusion E1 to E12
| Code | Assessment |
|---|---|
| E1 | Well bounded (D-073): excludes only if the record fails RQ2a, RQ3a, RQ4b, RQ5 and RQ6 as well |
| E2 | Worded universally ("no supervised predictive model…"), but RQ2a, RQ3a, RQ4b and RQ6 methodological works, reporting guidelines and risk-of-bias tools may develop no model. The §4 rule "exclusion requires failing all RQs" prevents wrongful exclusion, but E2 has no limitation note like E1, and the §3 table lists E2 under RQ1 only. **Documentation concern:** a screener reading §1 alone could mis-apply E2. Suggest an E1-style note |
| E3 | The same issue as E2 for methodological RQ2a and RQ3a papers on non-biochemical tabular data; the note covers RQ1, RQ2b and RQ4a only |
| E4 | Complex but fully specified (D-055, D-061, D-075). Reproducibility depends on the full-text component statuses. Acceptable; the pilot will test it |
| E5 | Clear; includes the D-076 retraction-notice handling |
| E6 | Clear |
| E7 | Clear for Stage 0. **[OPEN: Q-082]** for retracted articles without the PubMed type, which is a gap at manual screening |
| E8 | Deferred (D-030); both records of a pair are screened. Clear |
| E9 | Clear (full-text stage) |
| E10 | Practically inapplicable inside the D-044 scope (all records come from dated queries). Harmless |
| E11 | Clear (RQ1) |
| E12 | Catch-all, with a mandatory justification and a 100 % pilot audit. Appropriate |

- **Contradictions with the inclusion criteria:** none found.
- **Primary-code rule** (D-080, first applicable code in numerical order): reproducible. Its result depends on whether RQ-scoped codes (E1–E4, E11) count as "applicable" to a record that fails all RQs for other reasons. This is a minor ambiguity, and the pilot's per-code agreement will show it.

### 3.4 Screening decisions (criteria §4, §6; protocol §2, §3, §5)
- **Decisions:** `include`, `exclude` and `uncertain` are clearly separated, and `abstract_only` is allowed at full text only.
- **Exclusions need a positive reason** (§4; protocol §5 item 1).
- **Missing information:** missing abstracts give `uncertain` → full text, with no E4 and no `yes` from missing information. Language missing is not E6. "Silence is never `no`". **No silent conversion of missing information into exclusion** `[EVIDENCE]`.
- **Gap:** the criteria §4 tree shows Stage 2 as INCLUDE / EXCLUDE / ABSTRACT_ONLY, while §6 also allows `uncertain` at full text. An unresolved full-text `uncertain` goes to the adjudication queue (protocol §5 item 4), but neither text names its terminal resolution. **Documentation concern (minor).**

### 3.5 Research questions RQ1–RQ6
- **Where they are defined:** the questions themselves are defined in `search_strategy.md` §1.2 (DRAFT), not in the reviewed texts. The criteria operationalise them in §3.
- **RQ5 threshold:** "at least 4 of 5" is represented consistently `[EVIDENCE]`: criteria §3 (D-031), §5 (Tier 1: y + u ≥ 4; D-062) and §6; protocol §2a (`qualified` ≥ 4, `near_rq5` = 3); research_plan theme F, inactive note.
- **RQ5 question text:** the question in `search_strategy.md` §1.2 still omits calibration, and the alignment promised there has not been made (Finding 2).
- **Assumed outcomes:** no question assumes an outcome. The protocol header "Scope of claims" states that screening does not assume the framework is new or better. Good.
- **Compatibility with the scope:** RQ1 and RQ5 are well served by the D-044 scope. RQ2, RQ3, RQ4 and RQ6 are served only incidentally (Finding 1).
- **Project-level question:** it contains "discrimination comparable to standard baselines". "Comparable" is undefined, but it belongs to D-019 (evaluation protocol, PENDING), not to these texts. DEFERRED.

## Section 4 — Protocol review

### 4.1 Reproducibility
- **Reproducible from the texts:**
  - the rules, codes and descriptors (with definitions; protocol §2 table);
  - Stage 0;
  - the pilot sampling (seed, order, allocation, key procedure, frame checks);
  - the agreement computation;
  - the pass rule;
  - the audit trail (append-only rows, latest row per paper and stage).
- **Not reproducible from the texts:**
  - the assistant's individual decisions (Finding 4);
  - the D-035 record §2 component definitions, which are referenced, not included (they live in `research/reviews/Q-041_decision_record_D035.md`; acceptable if that file is frozen alongside — `[RECOMMENDATION]` name it in the freeze entry);
  - the RQ wording (Finding 2).

### 4.2 Workflow
- **Stages and order:** freeze → (D-035 §6) → Stage 0 → pilot → expansion in batches of about 300 → D-008 audit. Clear.
- **Responsibilities:**
  - the assistant is the primary screener;
  - the researcher is the second pilot screener;
  - the researcher verifies `qualified`/`near_rq5` (D-035 G4) and reviews every no-abstract decision (D-068 (10)).
- **Disagreements:** handled through the adjudication queue and joint review.
- **Full-text escalation:** `uncertain`, RQ5 routing and no-abstract records.
- **Record-keeping:** paraphrased justifications (D-089); `criteria_version` on every row once frozen.
- **Gap (RQ5 confirmation bias):** only `qualified` and `near_rq5` records are verified by the researcher. Records the assistant places in `below_threshold` after full text are not verified, so a systematic under-crediting of prior art would go unnoticed. This matters for any novelty claim (theme F). `[RECOMMENDATION]` A researcher spot-check of `below_threshold` records among those routed to full text under RQ5. **Researcher decision.**

### 4.3 Agreement and adjudication (B3 / D-098) `[EVIDENCE]`
| Approved rule | Protocol §7 "Pass" | Code (`pilot_agreement.py`) | Test |
|---|---|---|---|
| (a) Code disagreement = exactly one screener gives that code as its primary exclusion code; an include/exclude disagreement counts toward the excluding screener's code | stated | `per_code` counts records where exactly one screener's primary code is the code; `MAX_CODE_DISAGREEMENTS = 2` (≥ 3 fails) | "D-098 (a)…" ok |
| (b) Only an adjudicated `exclude` resolves an include/exclude conflict | stated ("whatever its code"; latest adjudication row) | `unresolved = [p … if agreed.get(p) != "exclude"]` | `test_only_agreement_on_the_exclusion_resolves` ok |
| (c) Undefined κ → NOT PASSED | stated | `passed = kappa3 is not None and …` | the test asserts `pass=False`, `kappa_undefined=True` |
| (d) `screener=researcher:adjudication` | stated (§7; §5 item 3) | `ADJUDICATION_SCREENER`; other screeners are refused | `test_marker_and_pilot_screeners` |

**No conflicting wording found.**

**Methodological notes (no change proposed to the approved rules):**
- **Precision of κ:** with n = 60, a κ of about 0.6 has a wide confidence interval (`[HYPOTHESIS]` roughly ± 0.15–0.2). The pass decision rests on a point estimate.
- **Prevalence:** κ is sensitive to it, so high raw agreement can give a low κ.
- **(c) can fail perfect agreement:** for example, if all 60 decisions are identical in one category. This is unlikely with a theme-stratified sample.
- `[RECOMMENDATION]` Report the confidence interval and the prevalence alongside κ in `pilot_report.md` (a reporting addition; researcher decision).

### 4.4 Pilot methodology
- **Distinct from Stage 0:** the frame excludes the seven Stage-0 records, and Stage-0 rows are written before the draw (D-093).
- **Purpose:** to calibrate the criteria (agreement, per-code consistency).
- **Limitations:** stated ("a theme-representation design, not a population-proportional sample"). `[RECOMMENDATION]` State explicitly that pilot κ is not an estimate of agreement over the whole screening set.
- **Sampling:** fully deterministic (D-063, D-077) and checked against the D-044 snapshot.
- **Failed pilot:** depends on Q-083 (OPEN; may stay open, D-083).
- **No operation before approval:** the draw needs the freeze, all six §6 records and a D-077 (6) authorisation. Assistant screening also needs the D-102 revision and D-099 (3)/(4) (§7a step 1). **No pilot operation can begin before its approvals under the texts** `[EVIDENCE]`.
- **Remaining risk:** the frame-only check (`--frame-only`) is not gated in code. Q-092 (c) is open, and the protocol says it needs your explicit authorisation. This is a procedural safeguard, not a technical one.

### 4.5 Blinding and data protection (§7, §7a)
| Check | Result |
|---|---|
| R1 preferred, R2 fallback, design only | §7a step 5: "R1 selected as the design, R2 as the fallback (D-109; design only)" ✔ |
| D-102 operational revision pending | §7a step 5 [OPEN]; "the pilot cannot start until the revision is approved" ✔ |
| No salt in a screening CSV | Protocol text: no salt described ✔. **But** approved D-102 clause (1) still prescribes a salt line; it is unimplementable and the revision is pending. **Governance inconsistency, acknowledged; researcher decision** |
| The commitment does not expose the salt early | Not in the protocol (deferred to the revision). The R1 text (previous audit §5.2) keeps `S` secret until disclosure and excludes it, and any unsalted hash, from the commitment record ✔ (design only) |
| Independent custodian requirement explicit | **Not explicit in protocol v0.2** (removed from §7 by D1–D2; deferred to the revision). Explicit in D-102 (3). Gap for a reader of the protocol |
| D-096 extension recognised | **Not in protocol v0.2.** Recognised in the audit report and package only |
| Access, encryption, key custody, disclosure not shown as implemented | ✔ "nothing implemented"; outputs say "form and timing set by the revision" |
| Threat model not overstated | The protocol makes no claim. D-102 (3) correctly says a Git-ignored folder in the working session is not sufficient. The R1 draft's "blinded by access control" holds **only if** the custodian's account and environment are actually inaccessible to the researcher. Separate sessions under one account would **not** satisfy it `[HYPOTHESIS]`. The revision should say this explicitly |

**Design approval (D-109) ≠ operational approval.** The texts keep these apart.

**Data protection:**
- the private sheet is never committed (D-096);
- justifications are paraphrased (D-089);
- no abstracts are committed (§5 item 7).

## Section 5 — Governance consistency

### 5.1 Decision references
**Classification key:**
1. correctly represented;
2. correctly represented but conditional;
3. proposed and not approved;
4. historical status only;
5. missing or inconsistent;
6. requires a researcher decision.

| Decision | Where | Class | Note |
|---|---|---|---|
| D-084 | criteria §11 heading and intro; package | 2 + 6 | "approved in principle; final amended text submitted"; your approval is needed |
| D-097 | protocol §7 (binding format and condition wording); criteria §11 step 10 | 1 | — |
| D-098 | protocol §7 "Pass" (a)–(d); §5 item 3 | 2 | Conditional and inactive; implemented and tested (synthetic) |
| D-099 | protocol §7 ("before the first authorised run"; implemented after the freeze) | 1 | The package's "before step 4" is stricter than D-099 → 5 (package only) |
| D-100 | protocol §7a | 1 | — |
| D-101 | protocol §7 and §7a step 4 | 2 | — |
| D-102 | protocol §7 and §7a step 5; criteria §11 step 5 | 2 + 6 | Clause (1) unimplementable; revision pending; custodian not stated in the protocol (gap) |
| D-103 | both headers; §11 | 1 | — |
| D-104 | both Version rows; §11 step 2 | 1 | — |
| D-105 | criteria §4 | 1 | — |
| D-106 | criteria §11 step 5 | 1 | The step 5 list is complete (checked against the register by script in the previous audit; spot-checked here) |
| D-107 | criteria §0 and §11 steps 1, 10; protocol §1 and §10 row 6 | 2 + 6 | "approved in principle, subject to verification" everywhere |
| D-108 | both headers; criteria §0 and §11 steps 1, 5; protocol §1 and §10 row 6 | 3 | "proposal", "proposed", "not approved" everywhere; never stated as a rule |
| D-109 | protocol §7a step 5 | 1 | "design only" |
| Historical rows | criteria §9 rows 172 and 177 (annotated 2026-11-11); protocol §11 rows for the governance reconciliation and B1–B6 ("D-102 approved (salt…)") | 4 | Dated; later rows give the current state |

### 5.2 D-107 and Q-097
**Representation in the texts** `[EVIDENCE]`: protocol §10 row 6 says "Verified on 2026-11-11: `paper_inventory.json` `b668dbde…d054` (commit `bf0c579`); the provenance of the ignored files is not yet established (Q-097)". **This is accurate.** Neither text adopts any Q-097 option, which is correct.

**Correction to the premise of this task.** The task describes the "current recommendation" as option (c). The previous audit report recommended differently:
- §3.4 named option (a), an authorised scratch rebuild, as "the smallest independent check";
- §3.5 proposed recording the provenance as "consistent with the T2 build … not verified by a committed hash", with (a) optional.

That combines (b) and (c). Whichever you choose, option (c) is the most conservative statement and needs no new operation.

| Category | State |
|---|---|
| Verified inventory hash | `b668dbde…d054` (verified; committed) |
| Observed ignored-file hashes | `0141d5d8…d192`, `78eba1d3…9460` (observed 2026-11-11) |
| Strong circumstantial T2 link | T2 pre-build hash list (scratch, uncommitted); four reproducible offline builds; modification time inside the T2 window — **reported in the audit report, not re-inspected in this review** |
| Missing committed post-T2 hash | Yes: no committed record gives either ignored file's post-T2 SHA-256 |
| User-reported Drive agreement | Raw-export archives only (`69e690f0…`, `7b7d4674…`); **researcher-reported, not verified**; does not cover the ignored files |

### 5.3 D-108: assessment of the three proposed additions
1. **D-099 (3)/(4) before the first authorisation.**
   - Sound in purpose.
   - **Stricter than D-099**, which requires them before the first authorised *run* (step 5). The authorisation row binds no code commit, so implementing between steps 4 and 5 would comply with D-099.
   - Adopting "before step 4" is a **new requirement** (your choice). The package correction currently presents it as following from D-099, which it does not, strictly.
2. **D-102 revision and custodian before the D-077 (6) authorisation permits delivery of the researcher's sheet.**
   - Sound. Under R1 the commitment must precede delivery of the researcher's sheet.
   - **Refinement:** the *draw* need not wait, because the commitment record includes the SHA-256 of `pilot_sample.csv`, so the draw precedes the commitment. Only the *sheet's generation or delivery* must follow the commitment.
   - D-077 (6) currently authorises "one draw and then one sheet". Under R1 the custodian also needs the sheet's seven fields (a D-096 extension). The authorisation's scope should say so.
3. **A new fixed-inventory entry if the inputs change.**
   - Sound for any change of the inventory hash or the ignored-file hashes.
   - "Build-code inputs": a code change that leaves the output hashes identical arguably needs re-verification, not a new entry.
   - Your choice of strictness.

**Status:** both texts identify D-108 as PROPOSED ✔. Not approved here.

### 5.4 P1: the D-102 status-cell date
**Evidence** `[EVIDENCE]`:
- the D-102 status cell reads "effective at the v1.1 freeze (2026-11-11); custodian appointment pending … Earlier: PROPOSED (2026-11-11)";
- the history row `2026-11-11 | B1-B6-APPROVALS | D-102 | PROPOSED → **APPROVED — CONDITIONAL**` records the approval on 2026-11-11;
- the B1–B6 session log chose for D-102 the status "APPROVED — CONDITIONAL (inactive for screening), like the other pilot rules (D-094, D-101)", and those carry no date;
- D-098 uses the pattern "(final, 2026-11-11)" for an approval date;
- no freeze entry or `criteria_registry.json` exists.

**Conclusion:**
- It is **demonstrable** that 2026-11-11 is **not a freeze date**: no freeze occurred, and the effective date is set at the freeze.
- It is **demonstrable** that 2026-11-11 is the date of the recorded approval.
- It is **not** recorded what the writer *meant* by the parenthesis.

**P1 is safe to apply if it is worded as fact**, for example: "No status change. The v1.1 freeze has not taken place; '(2026-11-11)' in the status cell coincides with the approval recorded in the B1–B6 history row and is not a freeze or effective date." It needs your authorisation as a decision-log history row. It must not claim the writer's intent.

### 5.5 Open questions
| Q | Status | Stage | Comment |
|---|---|---|---|
| Q-082 | Open (D-083) | before such a record is screened | Practically before the pilot (Finding 6) |
| Q-083 | Open (D-083) | before a second pilot | — |
| Q-084 | Open (D-083) | before expansion | — |
| Q-085 | Open | condition 3 (activation) | — |
| Q-092 (c) | Open | before a real frame-only check | The code does not gate it |
| Q-096 | Open | condition 6 (activation) | — |
| Q-097 | Open | fixed-inventory entry (activation) | — |
| Q-063 | Open — partly addressed | fixed-inventory entry; next rebuild | — |

## Section 6 — Freeze procedure review (criteria §11)
| Requirement | Result |
|---|---|
| Every prerequisite represented | ✔ Content approval (step 3), D-084 approval (intro), ID and dates (step 8), Stage-0 confirmation (step 4), open-items list (step 5) |
| Every open question listed | ✔ Step 5. Every open register question referred to in either text is listed (re-checked: the Q-IDs in both texts versus step 5) |
| No circularity | ✔ The hashes are computed from the freeze commit (step 7) and held in the entry (step 8), not in the texts |
| D-107 / Q-097 positioned correctly | ✔ Step 10 (fixed-inventory entry before the condition-6 row; D-107 in principle); Q-097 in step 5 |
| D-108 not treated as approved | ✔ Steps 1 and 5 |
| D-102 and custodian pending | ✔ Step 5 ("pending revision of D-102"). The custodian is not named in §11, which is correct because it is not a freeze prerequisite |
| Q-082 to Q-084 open at the freeze (D-083) | ✔ |
| Freeze not confused with activation | ✔ Step 10 separates the §6 rows and the authorisations |
| Freeze authorises no real-data work | ✔ Step 11 |
| No dates invented | ✔ `<date>` placeholders; "set by the researcher" |
| Consistent with D-084 (in principle) | ✔ The heading and intro say the text is submitted for approval and not executed |

**Weaknesses (documentation; none blocks the freeze):**
- **(i) The step numbers are not chronological.** Step 2 describes the freeze-commit wording, step 3 is the content approval, step 8 reserves the ID before step 6's commit. A reader could execute them out of order. The package §E gives the chronological order. `[RECOMMENDATION]` Add one sentence: "Execution order: 3 → 8 → 6 (with 2) → 7 → 9 + 9a."
- **(ii) No step says what happens if your approval comes with requested changes.** Implicitly a revised text is re-approved before step 6. Suggest saying so.
- **(iii) Step 6 requires that no other file changes in the freeze commit.** It does not say that the pending uncommitted work must be committed first (package G1). This is implicit, and harmless if G1 is followed.
- **(iv) The D-035 record §2 component definitions** (`Q-041_decision_record_D035.md`) are part of the operational definition of RQ5. They are neither frozen with the texts nor hashed in the freeze entry. `[RECOMMENDATION]` Record its SHA-256 in the freeze entry. **Researcher decision.**

## Section 7 — Scientific and methodological risks (prioritised)
| # | Section | Problem | Why it matters | Type | Suggested resolution (not applied) |
|---|---|---|---|---|---|
| R1 | criteria §0, §3; protocol §1 | The D-044 scope omits the dedicated RQ2, RQ3, RQ4 and RQ6 queries (`search_queries.csv`: Q-PM-04–10 → RQ2–RQ4; Q-PM-13–14 → RQ6) | Evidence for RQ2–RQ4 and RQ6 will be incidental and **selection-biased** toward metabolic/RQ1-retrieved records; claims about "how often" calibration or validation is done (RQ3, RQ4) would not generalise | Researcher decision | State in criteria §0 which RQ strands are covered only incidentally; restrict the claims accordingly; or extend the scope by a new decision |
| R2 | `search_strategy.md` §1.2 vs criteria §3 | RQ wording outside the frozen texts; RQ5 question omits calibration | The criteria operationalise a question whose text is unapproved and inconsistent | Governance; researcher decision | Align `search_strategy.md` RQ5, or name the governing RQ text in the freeze entry |
| R3 | protocol §7, §8; D-008 | AI single screener for the main set; small audit | **Screening bias**; κ from 60 pilot records and a 25 + 25 audit give limited assurance against wrongful exclusions | Researcher decision (approved design) | Keep the "structured review with systematic elements" classification; report the audit confidence intervals; consider a larger or stratified exclusion audit |
| R4 | protocol §7a, §8 | Assistant model identity, version and instructions not recorded per batch | **Reproducibility** of decisions | Researcher decision | Record the model identifier and the instruction/tools commit per screening batch in the session log |
| R5 | criteria §5 Tier 3 | RQ1 includes confirmed from the abstract only | **Eligibility validity** of RQ1 counts and descriptors | Researcher decision | Report as a limitation, or require full text for all includes used in the synthesis |
| R6 | protocol §2a; D-035 G4 | Only `qualified`/`near_rq5` are verified by the researcher | **Overclaiming novelty** if prior art is under-credited | Researcher decision | Researcher spot-check of full-text `below_threshold` RQ5-routed records |
| R7 | criteria §1 I-C4 vs §3 RQ6 | Systematic reviews: `review_lead` or RQ6 evidence? | Inconsistent coding; RQ6 counts | Researcher decision | Clarify the `record_type` for RQ6 systematic reviews |
| R8 | criteria §1 E2/E3 | No E1-style limitation note | Possible wrongful exclusion of methodological RQ2a/RQ3a/RQ6 papers by a literal reader | Documentation (wording) | Add notes mirroring E1 (meaning unchanged: §4 already requires failing all RQs) |
| R9 | criteria §2.2 | "≥ 1 biochemical marker among the final predictors" | A weak operational definition of "biochemical-biomarker-based" makes RQ1 heterogeneous | Researcher decision | Keep, but report the share of `mixed_both`/routine-only, or tighten the rule |
| R10 | protocol §2 `validation_design` | "external" includes "public dataset" without requiring separation from development data | **Independent-validation** terminology is looser than `research_integrity.md` §11 | Researcher decision (D-060 (1) wording) | Define "external" as separate from all development data, as stated by the authors; verify at full text |
| R11 | Q-082 | Retracted articles without the PubMed type undecided | A retracted study could enter the evidence base | Researcher decision | Decide before the pilot |
| R12 | criteria §1 I-C1; D-030 | Preprint and published versions both screened | Double counting in the synthesis | Deferred | Decide D-030 before the synthesis |
| R13 | protocol §7 | κ point estimate on n = 60; prevalence effects | Pilot pass/fail instability | Researcher decision (reporting) | Report the CI and prevalence; no rule change |
| R14 | criteria §4, §6 | Terminal handling of a full-text `uncertain` unnamed | Records could remain unresolved | Documentation | State that a full-text `uncertain` is resolved by adjudication |

**Leakage between screening and evaluation:** no direct leakage was found. Screening concerns published studies, not the project's data. An indirect risk is that the same assistant screens RQ5 prior art and later designs the method, which is covered by R6. **Confusion of discrimination, calibration, explanation and uncertainty:** the protocol §2 descriptor table separates them well (for example, "Brier score alone" → `unclear`; performance-metric CIs are not prediction uncertainty). No issue.

## Section 8 — Cross-document consistency matrix
| Reference | Criteria v1.1 | Protocol v0.2 | Result | Required action |
|---|---|---|---|---|
| Identifier | `criteria_v1.1+protocol_v0.2` (header) | same | PASS | — |
| Version rows / status wording | FINAL DRAFT; FROZEN template (D-104) | same | PASS | — |
| Input set | 1,470 (D-044); inventory hashes listed | same, with full hashes | PASS | — |
| Inventory fixing | D-107 in principle; D-108 proposal (§0) | same (§1, §10 row 6) | PASS | — |
| Ignored-file provenance | — | "not yet established (Q-097)" | PASS / EVIDENCE REQUIRED | Q-097 decision |
| Abstract source | — | "restorable from the verified archives" (§1) | DOCUMENTATION ERROR (minor) | "recoverable by an authorised rebuild from raw exports restored from the archives (Q-063)" |
| Decisions | include/exclude/uncertain/abstract_only (§6) | same (§2) | PASS | — |
| Full-text `uncertain` | allowed (§6), absent from the §4 tree | queue lists every `uncertain` (§5) | DOCUMENTATION ERROR (minor) | Name the terminal handling |
| Exclusion codes | E1–E12 (§1) | "as in criteria §1"; pattern | PASS | — |
| Primary code | D-080 + D-074 (d) | same (§6) | PASS | — |
| E2/E3 scope notes | missing | — | METHODOLOGICAL CONCERN | R8 |
| Stage 0 | §4 types and multi-type rule | §3, same | PASS | — |
| Missing abstract | §4 | §3 table | PASS | — |
| RQ5 threshold 4/5 | §3, §5, §6 | §2a | PASS | — |
| RQ wording | not included | not included | GOVERNANCE INCONSISTENCY | R2 |
| Scope vs RQ2–RQ4 / RQ6 | §0 "reduced scope reported" | §1 "1,916 outside" | METHODOLOGICAL CONCERN | R1 |
| Reviews / RQ6 | I-C4 vs RQ6 | §3 "Reviews: `review_lead` only" | METHODOLOGICAL CONCERN | R7 |
| Disagreement rules (D-098) | — | §7 (a)–(d) | PASS | — |
| Adjudication marker | — | §5 item 3; §7 | PASS | — |
| Pilot prerequisites | §7 → protocol | §7 "When"; §7a step 1 | PASS | — |
| Failed pilot | — | Q-083 [OPEN] | DEFERRED | — |
| Audit timing | §7 Q-084 [OPEN] | §8 Q-084 [OPEN] | DEFERRED | — |
| Blinding | — | §7, §7a step 5 (pending) | PASS / RESEARCHER DECISION REQUIRED | D-102 revision |
| Custodian / D-096 extension | — | not stated | RESEARCHER DECISION REQUIRED | Name them in the revision; optionally reference D-102 (3) in §7a step 5 |
| Data protection | §6 justification rule (D-089) | §5 item 7; D-096 | PASS | — |
| D-099 timing | — | "before the first authorised run" | PASS (texts); GOVERNANCE INCONSISTENCY (package says before step 4) | Align the package wording |
| Conditional decisions | stated per row (§9, §10) | stated | PASS | — |
| Effective dates | "set by the researcher" | same | PASS | — |
| Freeze procedure | §11 | references §11 | PASS (wording weaknesses, §6) | Optional clarifications |
| `validation_design` "external" | §6 (via D-060) | §2 definition | METHODOLOGICAL CONCERN | R10 |
| `biomarker_class` vs proteomics | §2.2 values | — | DOCUMENTATION ERROR (minor) / RESEARCHER DECISION REQUIRED | Add a value, or state that proteomics → `other` with the flag |
| Q-082 timing | §10 [OPEN] | — | RESEARCHER DECISION REQUIRED | R11 |

## Section 9 — Technical evidence and tests
**Previously reported** (the audit report §10; not re-run here): Phase-1 tool tests 130 OK; literature 347 OK; data-protection 10 OK; NHANES 29 OK; query check PASS 168; raw-export verify OK; whitespace exit 0 (14:00:32Z–14:01:44Z).

**Independently executed in this review** (synthetic fixtures only):

| Time (UTC) | Exact command | Actual output |
|---|---|---|
| 2026-11-11 14:21:48Z | `python3 -I -B -m unittest discover -s tests/literature -p "test_phase1_screening_tools.py"` | `Ran 130 tests in 0.552s` / `OK` |
| 14:21:48–49Z | the same, with `-k kappa -k adjudicat -k code -v` | 6 selected tests `ok`, among them "D-098 (a)…", "D-098 (b)…", `test_cohen_kappa_textbook_values`, `test_valid_adjudication_resolves`, `test_adjudication_of_another_record_does_not_resolve` |

**Code inspected** `[EVIDENCE]`:
- `pilot_agreement.py` lines 52–54 (constants) and 103–176 (`adjudicated_decisions`, `agreement`) match D-098 (a)–(d);
- tests at lines 1226–1287 (undefined κ → `pass=False`, `kappa_undefined=True`, "NOT PASSED (kappa undefined)") and 1453–1500 (adjudication).

**Not executed:** the full literature, data-protection and NHANES suites in this review; any real-data workflow.

**Limitations:** these tests show that the software implements the documented rules. They show nothing about the rules' scientific validity, or about whether you have approved them.

## Section 10 — Researcher decision register
| Item | Status | Needed for |
|---|---|---|
| Content approval of criteria v1.1 | Final draft | **Freeze** |
| Content approval of protocol v0.2 (incl. §7a) | Final draft | **Freeze** |
| D-084 amended §11 | APPROVED IN PRINCIPLE | **Freeze** |
| D-107 position at the freeze | APPROVED IN PRINCIPLE — subject to verification | Freeze (position); full approval before the fixed-inventory entry |
| Freeze-entry ID, approval and effective dates | — | **Freeze** |
| Git authorisation (package G1–G5) | — | **Freeze** |
| Acceptance of the scope/RQ limitation (R1) and the RQ wording (R2) | — | Recommended before content approval |
| I-C4 vs RQ6 (R7); Tier 3 (R5); `validation_design` (R10); mixed features (R9); proteomics class | — | Recommended before content approval, or accepted as limitations |
| D-035 record §2 file SHA-256 in the freeze entry (§6 (iv)) | — | Freeze (optional) |
| D-108 (and the refinements of its additions, §5.3) | PROPOSED | Activation |
| Q-097 | Open | Fixed-inventory entry |
| Q-063 | Open — partly addressed | Fixed-inventory entry; next rebuild |
| Q-085 | Open | Activation |
| Q-096 | Open | Activation |
| P1 (D-102 status-cell fact) | Proposed | Any time |
| D-102 revision; D-096 extension; custodian; threat-model statement on accounts | Pending | Pilot |
| D-099 (3)/(4) implementation; timing wording in the package | Approved for after the freeze | Before the first authorised run |
| Q-082 | Open (D-083) | Recommended before the pilot |
| Q-092 (c) | Open | Before any real frame-only check |
| Assistant model and version recording (R4); RQ5 `below_threshold` spot-check (R6); κ CI reporting (R13) | — | Before screening |
| Q-083 / Q-084 / D-030 | Open / Open / PROPOSED | Second pilot / expansion / synthesis |

## Section 11 — Recommended corrections (none applied)

### 11.1 Mechanical documentation corrections
| File | Section | Existing | Proposed |
|---|---|---|---|
| protocol v0.2 | §1 "Abstracts" | "restorable from the verified archives" | "recoverable by an authorised rebuild from the raw exports, which are restorable from the archives (`preservation_status.md`; Q-063)" |
| criteria v1.1 | §4 tree / §6 | Stage 2 without `uncertain` | "a full-text `uncertain` is resolved by adjudication (protocol §5 item 4)" |
| approval package | §E | "before step 4 … D-099 steps (3) and (4) … (D-099: 'required before the first authorised run')" | "before step 5 (the first authorised run) at the latest (D-099); before step 4 if you adopt D-108 addition 1" |
| criteria v1.1 | §11 | — | an execution-order sentence (3 → 8 → 6 with 2 → 7 → 9 + 9a) |
| protocol v0.2 | §7a step 5 | — | "D-102 (3) requires an independent custodian; R1 would also require extending D-096" (restates approved D-102 (3); D-096 extension named as needed, not decided) |

### 11.2 Scientific changes requiring researcher approval
R1 (scope statement), R5 (Tier 3), R7 (I-C4/RQ6), R8 (E2/E3 notes; wording that keeps the meaning), R9 (mixed features), R10 (external validation), the proteomics `biomarker_class`.

### 11.3 Governance changes requiring researcher approval
- R2 (RQ wording);
- D-035 §2 file hash in the freeze entry;
- D-108 with refined additions;
- P1 worded as fact;
- the D-102 revision, including the account/environment threat-model statement;
- the D-096 extension;
- R4 (assistant version recording);
- R6 (`below_threshold` spot-check).

### 11.4 Evidence still required
- Q-097 (ignored-file provenance method);
- Q-063 (backup approval details; PRESERVED status);
- the B2 cross-check implementation (before the authorised runs).

### 11.5 Should remain deferred
- Q-083 (until a pilot fails);
- Q-084 (until expansion);
- D-030 (until the synthesis);
- `prognostic` (D-071);
- D-019 / "comparable discrimination" (the evaluation protocol).

## Section 12 — Final readiness assessment
| # | Category | Assessment |
|---|---|---|
| 1 | Scientific content quality | **Good, with stated limitations.** Conservative, well-defined decision rules. Main limitations: incidental coverage of RQ2–RQ4/RQ6 (R1); single AI screener (R3); Tier-3 abstract-only includes (R5) |
| 2 | Methodological reproducibility | **Good for the rules and the sampling; limited for the assistant's decisions** (R4) and dependent on two external definition sources (RQ wording; the D-035 §2 record) |
| 3 | Documentation consistency | **High.** No contradiction between the two texts on rules, codes, decisions or identifiers; minor documentation errors listed in §11.1 |
| 4 | Governance completeness | **Complete for the freeze; incomplete for activation and operation.** D-102 clause (1) is unimplementable as approved (revision pending); the RQ wording is outside the governed texts |
| 5 | Researcher content-approval readiness | **Ready**, provided the R1/R2/R5/R7 limitations are knowingly accepted or decided |
| 6 | Freeze readiness | **Blocked only by your explicit decisions:** content approvals, D-084, the D-107 position, ID and dates, Git |
| 7 | Activation readiness | **Not ready:** Q-085, Q-096, Q-097, Q-063, D-108, the fixed-inventory entry, the six condition rows |
| 8 | Operational readiness | **Not ready:** D-099 (3)/(4), the D-102 revision, the D-096 extension, the custodian, tools, B2, run authorisations; Q-082 recommended before the pilot; Q-092 (c) only for a real frame-only check |

### Concise conclusion
1. **Both documents are scientifically suitable for your content approval.** The scope and RQ limitations (R1, R2) should be accepted knowingly or stated in the texts.
2. **No substantive change to inclusion or exclusion rules, thresholds or RQs is required.** Recommended scientific clarifications (R5, R7–R10) and reporting additions (R3, R4, R13) are for your decision.
3. **Governance inconsistencies remain, all minor or pending by design:**
   - the RQ wording is outside the texts;
   - D-102 clause (1) awaits its revision;
   - the package's D-099 timing is stricter than D-099;
   - the D-102 status-cell date (P1, safe only as fact).
4. **The freeze can proceed after your explicit decisions** (Section 10, rows marked "Freeze").
5. **Still preventing activation:** Q-085, Q-096, Q-097, Q-063, D-108, the fixed-inventory entry and the condition rows. **Still preventing operation:** D-099 (3)/(4), the D-102 revision, the D-096 extension, the custodian, tools and B2, run authorisations, and preferably Q-082.
