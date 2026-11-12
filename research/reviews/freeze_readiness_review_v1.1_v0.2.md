# Freeze-readiness review — screening criteria v1.1 and screening protocol v0.2

| Field | Value |
|---|---|
| Task | FREEZE-READINESS-REVIEW (researcher prompt, 2026-11-01) |
| Prepared | 2026-11-01 (verified container date), at HEAD `bf0c579` |
| Status | **Decision support only. Every replacement text, option and checklist item below is a proposal, not an approved scientific decision.** Nothing here freezes criteria v1.1 or protocol v0.2, classifies a record, marks a D-035 record §6 condition as met, or authorises a pilot draw, screening, extraction or training |
| Documents reviewed | `research/literature/screening_criteria_v1.1_draft.md`, `research/literature/screening_protocol_v0.2_draft.md`, `research/literature/screening_protocol.md` (v0.1) §3, `research/literature/screening_criteria.md` (v1.0) §4, `research/literature/search_strategy.md` §6.1, `research/reviews/Q-041_decision_record_D035.md` §6, `logs/DECISION_LOG.md` (D-025, D-035, D-063, D-066, D-068, D-069, D-070, D-072, D-074, D-077, D-078), `GOVERNANCE.md` §2, `CLAUDE.md`, session logs WORKSTREAM-C and T2-REBUILD (2026-11-01) |
| Later note (added 2026-11-01, after this review) | Point-in-time document: the analysis below is unchanged and reflects the state at HEAD `bf0c579` before the researcher's decisions. Parts of it were subsequently overtaken by D-079 (R1 adopted for the six records in §E) and by the FREEZE-DRAFT-CORRECTIONS work (Option A retained, §C; the §B replacement passages applied to the drafts in revised form; the Stage-0 list re-verified, with its confirmation at the freeze still open). See `logs/DECISION_LOG.md` and `logs/session_logs/2026-11-01_FREEZE-DRAFT-CORRECTIONS.md` |
| Labels | `[EVIDENCE]` verified in the repository; `[RECOMMENDATION]` assistant proposal pending approval; `[OPEN]` unresolved (`GOVERNANCE.md` §1) |

## A. Executive summary
**Completed** `[EVIDENCE]`:
- **Validator (Workstream C, commit `2fcc7b9`, pushed):**
  - `scope_flags` accepts exactly the D-069 (E) vocabulary;
  - the two non-metabolic retention tags may co-occur (D-070);
  - repeated tokens are rejected (D-078);
  - the D-060 (6) exemption covers only Stage-0 rule rows as defined by D-068 (5) (Option A: `is_stage0_rule_row()`, `scripts/literature/pubrecords.py:1694`, used at `:1769`).
- **T2 (commit `bf0c579`, pushed):**
  - `publication_type` populated for all 3,386 records; `unmapped_publication_types` empty;
  - `biomarker_class` and `screening_validation_design` added (null);
  - `dim_independent_validation` removed from the inventory output and both generated-output schemas;
  - `publication_type` required in the publication schema.
  - Same paper IDs and order, registry, provenance and verification statuses (3,348 / 37 / 1 / 0); pilot frame 1,463.
  - Inventory SHA-256: `b668dbde42473baa49ac1f02f89f900e94e39159c82efb8175ba125fef06d054` (JSON).
- **Tests at T2:** literature 217, data protection (strict) 10, NHANES 29, all OK; query table PASS (168 rows).

**Unresolved** `[OPEN]`:
- the freeze of criteria v1.1 and protocol v0.2 (D-035 record §6, condition 5);
- the classification of six in-scope records without an abstract (D-068 (8));
- confirmation of the Stage-0 type list at the freeze (D-068 (5));
- whether the drafts' Stage-0 wording is meant as Option A or Option B (§C);
- several draft passages that describe completed work as pending (§B);
- a `criteria_version` identifier (§G).

**Why the freeze is not authorised yet:** both drafts are marked "DRAFT … NOT frozen. Not in force." (criteria v1.1 line 6; protocol v0.2 line 6). Their text needs the corrections in §B and the decisions in §I before it can be frozen accurately. The freeze, and recording conditions 5 and 6, belong to the researcher (D-035; `CLAUDE.md` §2 rule 11).

## B. Outdated draft passages (proposed replacements; not applied)
| # | File and reference | Current wording (quoted) | Why outdated | Proposed replacement `[RECOMMENDATION]` | Support |
|---|---|---|---|---|---|
| B1 | `screening_protocol_v0.2_draft.md` §10, line 102 (condition 6 row) | "Pending: validator support for the D-069 vocabulary with the D-070 co-occurrence rule (the validator currently accepts only `scope_pending_proteomics` and `non_metabolic_rq5_candidate`); the Stage-0 limit (… the code currently exempts any `rule:stage0` row); tests for both; the rebuild (T2, not authorised) and the removal of `dim_independent_validation` from generated outputs and schemas; classification of the 6 in-scope records …" | The validator, the Stage-0 limit, their tests and T2 (including the removal) are implemented and committed | "**Unmet** (implementation complete; formal recording pending). Done: … (as now); validator support for the D-069 vocabulary with the D-070 co-occurrence rule and rejection of repeated tokens (D-078), and the D-068 (5) Stage-0 exemption limit (Option A), with tests (commit `2fcc7b9`); T2 rebuild with removal of `dim_independent_validation` from generated outputs and schemas (commit `bf0c579`; inventory SHA-256 `b668dbde…`). Pending: classification of the 6 in-scope records without an abstract as *not retrieved* or *unavailable* (D-068 (8)); the researcher's recording of condition 6" | Commits `2fcc7b9`, `bf0c579`; session logs `2026-11-01_WORKSTREAM-C.md`, `2026-11-01_T2-REBUILD.md`; D-078 |
| B2 | `screening_protocol_v0.2_draft.md` §10, line 95 (table heading) | "State on 2026-10-31 (refreshed in H1-H8-DECISIONS)" | The table no longer reflects the current state once B1 is applied | "State on <date of the edit> (refreshed after WORKSTREAM-C and T2-REBUILD)" | As B1 |
| B3 | `screening_criteria_v1.1_draft.md` §6, line 138 (final sentence) | "…the always-null inventory column `dim_independent_validation` is removed from generated outputs and schemas only in a separately authorised rebuild task (T2)." | T2 has removed it | "…the former inventory column `dim_independent_validation` was removed from generated outputs and schemas in the T2 rebuild (2026-11-01)." | Commit `bf0c579`; D-060 (1); D-029 |
| B4 | `screening_criteria_v1.1_draft.md` §6, line 135 (`scope_flags` row) | Lists the five tokens and the co-occurrence; does not say a token may appear only once | D-078 (approved 2026-11-01) is not reflected | Append: "Each token at most once per value (D-078)." | D-078 |
| B5 | `screening_criteria_v1.1_draft.md` header, line 10 (governing decisions) | "… D-068, D-069, D-070–D-076. Every change from v1.0 is traced in §9" | D-077 and D-078 are absent (protocol v0.2 line 10 already lists D-077) | "… D-068, D-069, D-070–D-076, D-077, D-078 …", with a matching §9 row for D-078 | D-077; D-078 |
| B6 | `screening_criteria_v1.1_draft.md` §6, line 138 (first sentence) and `screening_protocol_v0.2_draft.md` §3, line 55 | Criteria: "Stage-0 rule rows (`screener=rule:stage0`; only `exclude` rows with E5 or E7, D-068 (5)) need only the always-required columns." Protocol: "Rows carry `screener=rule:stage0`, which is used only on `exclude` rows with E5 or E7 from source publication types (D-068 (5); …)" | Not outdated, but ambiguous: the protocol sentence states a **usage** restriction (Option B), while the implementation enforces only the **exemption scope** (Option A) | Depends on the decision in §C. Under Option A: "The D-060 (6) exemption covers only Stage-0 rule rows: `exclude` rows with E5 or E7 and `screener=rule:stage0` (D-068 (5))." Under Option B: keep the wording and add "rows with `screener=rule:stage0` that are not such rows are rejected by the validator" (requires the changes in §C) | D-068 (5); `pubrecords.py:1694`, `:1769`; `test_option_b_not_adopted` |

**Not outdated** (checked): protocol v0.2 line 19 (six records "to be classed … before screening"; retrieval only under separate authorisation) and line 83 (pilot output records the inventory SHA-256 and the sampling script; corrected in `2fcc7b9`).

## C. Stage-0 rule: Option A versus Option B
- **D-068 (5)** `[EVIDENCE]`, quoted: "For D-060 (6), a Stage-0 rule row is an `exclude` row with reason code E5 or E7 and `screener=rule:stage0`; the exemption covers only such rows."
- **D-060 (6)**: descriptors are required for `include` and `uncertain` rows at title/abstract; "Stage-0 rule rows (`screener=rule:stage0`) are exempt".

| Aspect | Option A — exemption scope (implemented) | Option B — usage restriction (not implemented) |
|---|---|---|
| Rule | No include/uncertain row is exempt from the D-060 (6) descriptors, whatever its screener. Other uses of `screener=rule:stage0` are not rejected | As A, plus every row with `screener=rule:stage0` that is not an `exclude` E5/E7 row is rejected |
| Fit with D-068 (5) | Literal reading: the sentence defines the exemption's scope | Goes beyond the text: it adds a rejection rule that D-068 (5) does not state |
| Fit with D-068 (10) | Consistent | D-068 (10) ("Hard software enforcement is **not approved**") is written for the missing-abstract rule; whether it also limits a Stage-0 usage check is ambiguous `[OPEN]` |
| Fit with the drafts | Matches the exemption sentence in criteria v1.1 line 138 only if read as scope; protocol v0.2 line 55 ("used only on `exclude` rows") reads as a usage rule | Matches protocol v0.2 line 55 literally |
| Implementation | `is_stage0_rule_row()` (`pubrecords.py:1694`); check at `:1769`; researcher authorisation 2026-11-01 (DECISION_LOG status-history row, WORKSTREAM-C) | None |
| Tests | `test_stage0_rule_rows_e5_e7_accepted` (`tests/literature/test_t1a_schema_validation.py:175`), `test_stage0_screener_no_longer_exempts_include_or_uncertain` (`:185`), `test_option_b_not_adopted` (`:202`) | Would invert `test_option_b_not_adopted` |
| If chosen | Edit protocol v0.2 line 55 to the scope wording (§B6) | (1) a new decision entry (it is a new rule); (2) a check in `load_screening_decisions` (`pubrecords.py:1723` ff.) rejecting rows where `screener == STAGE0_SCREENER` and not `is_stage0_rule_row(r)`, with an error naming D-068 (5); (3) replace `test_option_b_not_adopted` with rejection tests (exclude E1/E3 with `rule:stage0`, include and uncertain with complete descriptors, full-text rows); (4) mutation check; (5) full test run and logs. No rebuild needed (no screening file exists) |

**Third reading to note:** Option A plus the protocol sentence kept as a *procedural* rule (who may write `rule:stage0` rows), enforced by human review only. This is consistent with D-068 (10) but leaves the frozen text stating a rule the software does not check. **The choice is the researcher's.**

## D. Stage-0 publication-type list
| Source | Status of the source | Types listed | Codes |
|---|---|---|---|
| `search_strategy.md` §6.1 | Search strategy (Stage A) | Editorial, Comment, News, Published Erratum, Retracted Publication; "Letters are not excluded automatically" | Not stated |
| `screening_criteria.md` (v1.0) §4, lines 110–111 | Draft v1.0 ("not approved"; superseded by v1.1 only at the freeze) | {Editorial, Comment, News, Published Erratum, Retracted Publication} | "E5/E7" |
| `screening_protocol.md` (v0.1) §3, lines 81–83 | Approved — conditional, inactive, through D-025 | Editorial, Comment, News, Published Erratum → E5; Retracted Publication → E7; letters not auto-excluded | E5 / E7 |
| D-068 (5) | APPROVED — CONDITIONAL (inactive) | Same four → E5; Retracted Publication → E7; letters not auto-excluded; "accepted provisionally and is to be verified explicitly against its approved source at the v1.1 freeze (D-025's approval cell does not enumerate it)" | E5 / E7 |
| D-072 | APPROVED — CONDITIONAL (inactive) | *Retraction of Publication* **not** added | — |
| D-074 (a)–(c) | APPROVED — CONDITIONAL (inactive) | Multi-type rule: *Retracted Publication* gives E7 whatever else is present (E7 primary); otherwise E5 only if every type is an E5 type or a D-028 keep-but-unused type; everything else is screened normally | E7 / E5 |
| Criteria v1.1 §1 and §4, protocol v0.2 §3 line 55 | Drafts | Same four → E5; Retracted Publication → E7, with the D-072 and D-074 rules | E5 / E7 |

**Exact matches** `[EVIDENCE]`: the five type names are identical in `search_strategy.md` §6.1, v1.0 §4, v0.1 §3, D-068 (5) and the drafts. The E5/E7 assignment is identical in v0.1 §3, D-068 (5) and the drafts. Letters are not auto-excluded in all sources that mention them.

**Discrepancies:** none in the type names or codes.

**Ambiguities to settle at the freeze** `[OPEN]`:
1. D-025 approved protocol v0.1 but, per D-068 (5), its approval cell does not enumerate the list. The list's approved status therefore rests on the approval of v0.1 §3 as a whole plus D-068 (5)'s provisional acceptance, and it must be confirmed explicitly.
2. `search_strategy.md` §6.1 lists the types without codes; the codes come from v0.1 §3.
3. The D-074 (b) keep-but-unused list (*Research Support…*, *Validation Study*, *Multicenter Study*, *Comparative Study*, *Observational Study*, *Randomized Controlled Trial*, *Clinical Trial* and its phases, *Evaluation Study*, *English Abstract*, *Historical Article*, *Video-Audio Media*) is defined by D-074 itself and is not part of the v0.1 list. Confirming the v0.1 list does not by itself confirm D-074 (b), which is separately approved (conditional, inactive).
4. No software generates Stage-0 rows yet. D-074 (f) says Stage-0 row generation needs separate authorisation. The pilot frame of 1,463 was computed read-only with the D-074 rules (excluded: P0028, P0099, P0113, P0624, P0830, P0931, P0939).

## E. Six in-scope records without an abstract (not classified)
| Paper ID | PMID | Source publication types (inventory) | Stage 0 under D-074 | `abstract_available` | Evidence available `[EVIDENCE]` |
|---|---|---|---|---|---|
| P0522 | 37042260 | Letter; Research Support, N.I.H., Extramural | No (contains Letter; D-074 (c)) | false | Retrieved from PubMed; abstract field "[Abstract not available]" in `raw_exports/META_2026-10-23_033.json`; no publisher evidence |
| P0559 | 35639990 | Journal Article; Comment | No (D-074 (c)) | false | Same placeholder (`META_2026-10-23_024.json`); no publisher evidence |
| P0624 | 31711877 | Editorial | **Yes — E5** (D-074 (b)); outside the 1,463 pilot frame | false | Same placeholder (`META_2026-10-23_009.json`); no publisher evidence |
| P0938 | 36645222 | Research Support, Non-U.S. Gov't; Letter; Comment | No (contains Letter; D-074 (c)) | false | Same placeholder (`META_2026-10-23_030.json`); no publisher evidence |
| P1154 | 28071176 | Journal Article | No | false | Same placeholder (`META_2026-10-23_006.json`); no publisher evidence |
| P3061 | 40348673 | Letter | No | false | Same placeholder (`META_2026-10-28_003.json`); no publisher evidence |

**Rule** — D-068 (8), quoted:
- "'No abstract' means the record's abstract is empty, absent, or a source placeholder such as '[abstract not available]'."
- "The screening record distinguishes *not retrieved* (an abstract may exist but was not obtained: retrieval failed, metadata incomplete, or the available transcription omits the field) from *unavailable* (the source indicates that no abstract exists)."
- "A retrieval failure is not proof that an abstract is unavailable."
- D-068 (9): retrieve first where feasible; it authorises no retrieval.
- D-068 (10): human enforcement.

**The two readings:**
- **R1:** PubMed's placeholder is "the source indicates that no abstract exists". All six would be classified *unavailable (per PubMed)*.
  - Basis: PubMed is the authoritative record (D-064); every retrieval succeeded.
  - Risk: a publisher may hold an abstract that PubMed lacks.
- **R2:** publication-level evidence is required.
  - Consequence: all six stay unclassified until a publisher check, which needs network access and a separate authorisation (D-068 (9)). This blocks the condition 6 item for six records, one of which (P0624) is outside the frame.

**Consequences common to both readings:**
- Routing does not change: a record without an abstract is `uncertain` and goes to full text, unless a valid Stage-0 or frozen title-level E1 exclusion applies (D-068 (2)). P0624's Stage-0 E5 exclusion governs it either way.
- The classification affects the retrieval step (D-068 (9)) and reporting (protocol v0.2 line 84).

Whichever reading is approved should be applied to all six. Distinguishing P0559 and P1154 (typed *Journal Article*) from the others would need a new, explicitly approved rule. **No record is classified here.**

## F. D-035 record §6 evidence table
Conditions are quoted from `research/reviews/Q-041_decision_record_D035.md` §6. **Implementation complete is not the same as recorded as met:** only the researcher records a condition as met (D-035; D-066 (8)).

| # | Condition | Current status (protocol v0.2 §10) | Evidence | References | Outstanding | Researcher decision? |
|---|---|---|---|---|---|---|
| 1 | Q-039: classification status column | Met (D-036) | D-036 approved; implemented in T1-A | DECISION_LOG D-036; commit `d1aaceb` | — | No |
| 2 | Q-040: retention of non-metabolic 3-of-5 frameworks | Met at decision level | D-055; flag name D-061 (effective at freeze); co-occurrence D-070 | DECISION_LOG D-055, D-061, D-070 | D-061 takes effect at the freeze | Only via the freeze |
| 3 | D-027 and D-024 approved | Met at decision level | D-027 (limited); D-024 (conditional) | DECISION_LOG D-024, D-027 | — | No |
| 4 | Remaining R5/D-029 items | Met at decision level | D-060 | DECISION_LOG D-060; commit `d1aaceb` | — | No |
| 5 | D-031–D-035 written into v1.1 and v0.2, frozen as the pilot's `criteria_version` | **Unmet** | Drafts revised up to 2026-11-01 (D-077 wording in `2fcc7b9`) | Draft headers lines 6 | §B corrections; §C, §D, §E decisions; `criteria_version` identifier; the freeze | **Yes** |
| 6 | Other pilot-blocking items | **Unmet** | Implementation done: arXiv spot-check (`MANIFEST.csv`); D-063 allocation; T1-A (`d1aaceb`); validator and Stage-0 limit with tests (`2fcc7b9`); T2 (`bf0c579`) | Session logs T1-A, WORKSTREAM-C, T2-REBUILD; DECISION_LOG D-063, D-078 | Six-record classification (§E); update of the v0.2 §10 row (§B1); the researcher's recording | **Yes** |

## G. Remaining freeze checklist `[RECOMMENDATION]`
1. **Stage-0 rule:** decide Option A, Option B or A with a procedural rule (§C). If B, implement and test first.
2. **Stage-0 type list:** confirm the five types and codes against protocol v0.1 §3 (§D), and confirm that D-074 (b)'s keep-but-unused list is treated as separately approved.
3. **R1 or R2** for the six records (§E), then record their classification (or keep them open under R2 and decide how that affects condition 6).
4. **Outdated passages:** authorise and apply §B1–§B5 and the §B6 variant matching the decision in item 1.
5. **`criteria_version` identifier:** none is defined yet (criteria v1.1 line 136 requires it "always once frozen"). Decide its form, for example `v1.1+p0.2-<freeze date>`, and where it is recorded.
6. **Cross-document consistency review after edits:** governing-decision lists (B5), §9 and §11 traceability tables, the §10 tables, the Stage-0 wording in both drafts, the `scope_flags` wording (B4), and line references to the validator and tests.
7. **D-035 §6:** the researcher records conditions 5 and 6 as met, with this evidence table, in `logs/DECISION_LOG.md` (status-history rows).
8. **Explicit researcher approval of the freeze**, recorded in `logs/DECISION_LOG.md`, with the frozen file versions identified (commit hash and SHA-256 of both files).

## H. Pilot and downstream prerequisites (each needs its own authorisation)
| Step | Prerequisites | Authority |
|---|---|---|
| Pilot draw (D-025, D-063, D-077) | Freeze recorded; D-035 §6 recorded as met; draw authorised (D-077 (6)); frame re-checked at 1,463 on the inventory current at the draw | Researcher |
| Recording at the draw | `screening/pilot_sample.csv` records IDs, stratum, seed 4004, the inventory SHA-256 current at the draw (now `b668dbde…`, not the 2026-10-30 value quoted in D-063) and the sampling script (D-063; D-077 (5); protocol v0.2 line 83) | Part of the draw |
| Pilot screening and audit | Blinded double screening; researcher as second screener; κ ≥ 0.60 and no unresolved include/exclude conflicts (D-025); researcher review of every no-abstract decision (D-068 (10)) | Researcher |
| Screening of the D-044 scope | Pilot passed; schedule revised from measured throughput (D-045); D-008 audits | Researcher |
| Full-text review | Screening results; full-text access (some may need network or researcher-supplied PDFs) | Researcher |
| Stage C | A critical comparison of existing methods reviewed by the researcher (`GOVERNANCE.md` §2) | Researcher |
| Stage D | Gap and main contribution approved (D-016) | Researcher |
| D-016–D-019 | Stage C and D gates passed (D-042 (1)); D-014 for D-017's evidence | Researcher |
| Model training | D-042; protocol draft §26 AB-1 to AB-13; D-013–D-019; NHANES data (absent from the container) | Researcher |

A passing test, a completed implementation or a calendar date does not pass any of these gates (D-042 (3)). The 2026-11-24 date is an interim deliverable without promised model results (D-045).

## I. Decision register for the researcher
| # | Decision | Options | Implications | Evidence needed |
|---|---|---|---|---|
| 1 | Stage-0 rule (§C) | A (scope only, implemented); B (usage restriction, enforced); A + procedural rule (human-enforced) | A: edit protocol line 55. B: new decision entry, code and test changes, then edit criteria line 138 accordingly. A + procedural: wording kept, no software check | D-068 (5) and (10) text; §C table |
| 2 | Stage-0 type list (§D) | Confirm as listed; amend (would need a decision entry and a re-check of the pilot frame) | Confirmation completes D-068 (5)'s freeze requirement | §D comparison |
| 3 | Six records (§E) | R1 for all six; R2 for all six | R1: classifiable now from repository evidence. R2: needs an authorised publisher check (network) | §E evidence; D-068 (8)–(10) |
| 4 | Corrections §B1–§B6 | Approve as proposed; amend; reject | Needed for an accurate frozen text | §B table |
| 5 | `criteria_version` identifier (§G item 5) | Form and location | Needed for every screening row (protocol v0.2 line 62) | — |
| 6 | Freeze | Approve after items 1–5; defer | Opens the D-035 §6 record and the pilot | Corrected drafts; this review |
| 7 | D-035 §6 record | Record conditions 5 and 6 as met; defer | Required before the pilot draw | §F table |
| 8 | Pilot draw | Authorise after item 7; defer | Starts the pilot (D-025) | Freeze record; inventory SHA-256 at the draw |
