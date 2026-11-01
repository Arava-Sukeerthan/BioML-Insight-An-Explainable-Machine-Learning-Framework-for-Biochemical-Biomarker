# Title/Abstract and Full-Text Screening Protocol — version 0.2 (DRAFT)

| Field | Value |
|---|---|
| Task | SCREENING-PREREQ-DECISIONS-2 (2026-10-30; assistant draft) |
| Version | **0.2 — DRAFT for researcher review. NOT frozen. Not in force.** |
| Proposed `criteria_version` | `criteria_v1.1+protocol_v0.2` — **proposed identifier only, not a frozen or effective version** (proposed by the assistant at the researcher's request, 2026-11-01); see criteria v1.1 header. Effective only through an explicit, approved freeze decision; proposed procedure (not executed) in criteria v1.1 §11 |
| Replaces | `screening_protocol.md` v0.1 only when the researcher approves and freezes this text together with `screening_criteria_v1.1_draft.md` as the pilot's `criteria_version` (D-035 record §6, condition 5). v0.1 is kept unchanged |
| Screening status | **INACTIVE.** No record has been screened, labelled or sampled. No pilot sample exists |
| Scope of claims | The protocol does not assume that the BioML-Insight framework is new or better. Screening describes the existing evidence; any research gap is decided later (Stage D, D-016) from verified, screened evidence |
| Governing decisions | As in criteria v1.1 §9, plus D-008, D-010, D-012/D-023, D-025, D-042, D-044, D-045, D-061, D-062, D-063, D-068, D-077, D-078, D-079. Traced in §11 |

---

## 1. Input set
| Item | Value | Source |
|---|---|---|
| Records to screen | **1,470** publication records (D-044 scope) | Defined by D-044 on `paper_inventory.json` SHA-256 `a509538dc5e1cf41cd7a4e180ed17df86f6d4cd83a7d227abea073f1689af4a3` (commit `ffee9ec`); re-counted 2026-10-30 from `paper_inventory.csv` query IDs. Later inventories: `e20ce77e9e3af3bafdd4d6ae38a36213df2d98eb2dc89b2ecfebb4178a84341f` (commit `b81c4e7`) and, after the T2 rebuild, `b668dbde42473baa49ac1f02f89f900e94e39159c82efb8175ba125fef06d054` (commit `bf0c579`). Same 1,470 in-scope `paper_id`s in the same order in all three (T2 log for `b81c4e7` → `bf0c579`; read-only comparison of all three on 2026-11-01, recorded in `logs/CHANGELOG.md`, PRE-FREEZE-CORRECTIONS; IDs and order only; authorises no pilot draw). The hashes are not interchangeable; the inventory used at the pilot draw is hashed and recorded then (D-077 (5)); see criteria v1.1 §0 |
| Q-PM-02 | All 743 records, all inside the 1,470 (D-009) | Inventory check 2026-10-30 |
| Without abstract | 6 records in scope (`abstract_available=False`): P0522, P0559, P0624, P0938, P1154, P3061. Classified 2026-11-01 as *unavailable — PubMed* (R1, D-079): each PubMed record was retrieved and carries PubMed's placeholder "[Abstract not available]"; this does not establish that no abstract exists in any other source. Retrieval from other sources only under separate authorisation (D-068 (9)) | Inventory check 2026-10-30; raw metadata check 2026-11-01; D-079 |
| Abstracts | Only in the git-ignored build output (`records/publications.jsonl`, D-010); restorable from the verified archives (`preservation/preservation_status.md`) | — |
| Retrieval themes | Context only: retrieval by a theme's query is not evidence that a paper addresses that theme. 173 in-scope records (LIT-005 G-queries) carry no theme | Inventory check 2026-10-30 |
| Not in scope | 1,916 inventory records outside D-044: neither screened nor excluded; the reduced scope is reported | D-044 |

## 2. Labels and descriptors
**Decision** (one per record and stage): `include`, `exclude` (one primary E-code + one-line justification), `uncertain` (to full text; never dropped), `abstract_only` (full-text stage only).

**Required for `include` and `uncertain` at title/abstract (D-060 (6))**: `rq_tags`; `record_type` (`original / methodological / software / guideline / review_lead / other`, D-028 2d); `biomarker_class` (D-058); `dim_explainability`, `dim_uncertainty`, `dim_calibration` (`yes/no/unclear`); `validation_design` (`external / temporal / internal_only / none / not_applicable / unclear`, strongest stated). Optional for `exclude`. Stage-0 rule rows exempt.

**Meaning at title/abstract (D-029 as specified by D-060):**

| Descriptor | `yes` | `no` | `unclear` |
|---|---|---|---|
| `dim_explainability` | A **named** explanation/attribution method applied to the model's predictions (SHAP, LIME, permutation importance, PDP/ICE, counterfactuals, attention analysis, rule extraction, coefficients/odds ratios presented as the explanation) | Stated absence, or a fully described analysis that clearly contains none | "Interpretable/explainable/transparent" without a method; built-in importance without a named procedure; no abstract |
| `dim_uncertainty` | A **named** prediction-level uncertainty method (conformal sets/intervals, Bayesian predictive uncertainty, MC dropout, ensembles **used to quantify** uncertainty, abstention on an uncertainty score) | Stated absence, or fully described analysis with point predictions only | Ensemble/random forest without an uncertainty use; CIs of a **performance metric** only; "reliable/robust"; no abstract |
| `dim_calibration` | **Probability** calibration assessed or corrected, named (calibration plot/curve, slope/intercept, ECE/MCE, Hosmer–Lemeshow, Spiegelhalter, Platt/isotonic/temperature scaling) | Stated absence; or "calibration" only in the analytical-chemistry sense (stated in the justification) | Brier score alone; "well-calibrated" without method; no abstract |

These descriptors record **what the title/abstract states**, for triage only. They never count toward D-031/D-034 (D-035 G2). RQ5 component statuses are assessed at full text under D-035 §2 (unchanged; see §2a).

**`validation_design`:** `external` = different cohort/site/centre/country/public dataset; `temporal` = later patients, same source; `internal_only` = CV, bootstrap or random hold-out of the development cohort; `none` = apparent performance only; `not_applicable` = no predictive model evaluated; `unclear` = not stated, or "validation cohort" without origin, or no abstract.

**`publication_type`:** derived by the build from source metadata through the versioned D-028 mapping table (never hand-edited). arXiv records → `preprint` (D-028 2b). No URL- or DOI-prefix rules (D-028 2c). *Retracted Publication* sets the `retracted` flag only.

### 2a. RQ5 component evidence (D-031–D-038, unchanged from v0.1 §2a)
Five components, `yes` only for a qualifying procedure applied with a documented output (D-032; D-035 §2); `unclear` = assessed but unresolved; empty = not assessed. Statuses are **confirmed** only on a `full_text` row; a full-text RQ5 assessment records all five. The build derives `rq5_coverage_group` (`qualified` ≥ 4, `near_rq5` = 3, `below_threshold` 0–2) and `rq5_coverage_provisional` (D-034, D-036, D-037) from confirmed statuses; screeners never assign it. Researcher verification of `qualified`/`near_rq5` records: new `full_text` row with `screener=researcher` (D-035 G4). Reporting of four-`yes` subgroups per D-038. **`non_metabolic_rq5_candidate` at full text (D-075):** a component is *possible* when its full-text status is `yes` or `unclear`; every `full_text` row for the record, including verification and adjudication rows, carries the flag only when `yes` + `unclear` ≥ 3 among its five statuses, and otherwise omits it and explains why in the justification. Possible components are not confirmed components: `unclear` never counts as `yes`, and coverage groups are derived from confirmed statuses only. The title/abstract row keeps its flag unchanged.

## 3. Decision rules
| Distinction | Rule (doubt → `uncertain`) | Basis |
|---|---|---|
| Metabolic vs broader biomedical targets | RQ1 requires a §2.1 target. Non-metabolic targets are E4 **unless** retained as `non_metabolic_method_exemplar` (RQ2–RQ5 methods applicable to tabular/omics/lab data) **or** flagged `non_metabolic_rq5_candidate` (≥ 3 possible RQ5 components counting `unclear`); both may be set on one record (D-070). At full text the flag is reassessed (§2a); without it, E4 applies unless the record qualifies as `non_metabolic_method_exemplar` or meets another applicable RQ (D-075) | Criteria v1.1 §1 E4; D-055; D-059; D-075 |
| Biochemical vs imaging-/genetics-only inputs | §2.2; multi-omics with a substantive metabolomics layer eligible (`uncertain` if unclear whether metabolites enter the model) | D-043; D-057 |
| Original vs reviews, notices, retractions, duplicates | Reviews: `review_lead` only. Errata → Stage 0 E5. Retractions → Stage 0 E7. Retraction notices (`retraction_notice`) → manual screening; E5 if excluded, with the retracted article's `paper_id` in the justification or a statement that it is not in the inventory; not E7 merely because the article is retracted (D-076). Duplicates → E8 only after a recorded decision; A-4 deferred (D-030), both records of a pair screened | D-059; D-076 |
| RQ5 routing | ≥ 3 possible components counting `unclear` → `uncertain`, `needs_human=yes`, full text | D-060 (4) |
| Missing abstract (title/abstract only) | `uncertain` → full text unless Stage-0 E5/E7 or a title-level E1 (frozen wording); **no E4**; method descriptors and `validation_design` `unclear`; `biomarker_class` `unclear` unless the title explicitly supports it; all five preliminary component statuses `unclear` ("no abstract"); `rq_tags`/`record_type` provisional; no RQ5-based tier | D-060 (2) as amended by D-068; D-059 A-6 |

**Stage 0 (automatic, counted, reversible):** PubMed types *Editorial*, *Comment*, *News*, *Published Erratum* → E5; *Retracted Publication* → E7; letters are not auto-excluded. Rows written by this rule carry `screener=rule:stage0`. **Timing (from approved decisions):** Stage-0 rows are screening decisions, so none is written to `decisions.csv` before D-035 record §6 is met (D-035 record §6: "D-035 governs no screening until" the conditions hold; D-068, D-072 and D-074 are inactive for screening until then; D-074 is effective only at the v1.1 freeze); each row carries the frozen `criteria_version` (criteria v1.1 §6; §5 item 2). The pilot frame (§7) is computed from source publication types in the inventory and does not depend on Stage-0 rows. **[OPEN — researcher decision and implementation; Q-089]:** when, after activation, Stage-0 rows are written (before the pilot draw, with the pilot, or at expansion), and the tool that writes them: no committed script generates Stage-0 rows; the validator only checks the exemption scope (Option A). Writing such a script needs separate authorisation. A Stage-0 rule row is an `exclude` row with E5 or E7 from source publication types, and only such rows are exempt from the D-060 (6) descriptor requirement (D-068 (5); Option A, as implemented by the validator): an `include` or `uncertain` title/abstract row is never exempt, whatever its screener. The exemption's scope is the only software-checked rule; other rows carrying this screener value are not rejected for that reason. The type list was compared with protocol v0.1 §3 on 2026-10-31 and re-verified on 2026-11-01 (identical types and codes); its explicit confirmation is part of the freeze (D-068 (5)). *Retraction of Publication* notices are not Stage-0 types (D-072); they are screened manually (§3; D-076), unless the record also carries *Retracted Publication*, which makes it a Stage-0 E7 exclusion (D-074 (a)). Records with several source types (D-074): if they include *Retracted Publication*, Stage-0 E7 applies whatever the other types, and E7 is primary over E5; otherwise Stage-0 E5 applies only if every type is a Stage-0 E5 type or a D-028 keep-but-not-used type (criteria v1.1 §4); every other combination is screened normally. All Stage-0 decisions are listed in the pilot report.

## 4. Possible duplicates and versions
Unchanged from v0.1 §4: no pair decision exists; both records are screened; pairs are listed in the pilot report. A-4 and D-030 are deferred/proposed. E8 only after a recorded decision.

## 5. Ambiguity handling, adjudication and audit trail
1. **When in doubt, `uncertain`.** Exclusion needs a positive reason found in the title/abstract.
2. **Every row records** `screener`, `date`, `justification` (≤ 1 sentence, quoting the decisive phrase where possible) and `criteria_version` (the frozen version string). Not yet enforced: the screening schema types `criteria_version` as an optional string and no validator checks it against a frozen identifier (implementation gap; needs separate authorisation).
3. **Append-only:** decisions are never edited or deleted; a correction or adjudication is a new row (`screener=researcher` for adjudication), and the build uses the latest row per `paper_id` and `stage` while keeping all rows. The build rejects rows that blank a recorded component (D-036). Full-text and adjudication rows set `non_metabolic_rq5_candidate` by the D-075 rule (§2a).
4. **Adjudication queue** (`screening/adjudication_queue.csv`): every `uncertain`, every E12, every `needs_human=yes`, all possible-duplicate pairs.
5. **Criteria changes** after screening starts: question in `unresolved_questions.md`; accepted change logged in `DECISION_LOG.md` as a new criteria version; every record decided under the old wording with an affected code is re-screened.
6. **Provenance:** decisions refer to `paper_id` only; source records, raw exports and the manifest are never edited by screening. Inventory and reports are regenerated by the build, not by hand.
7. **Data protection:** no abstracts or raw records enter committed files (D-010).

## 6. Exclusion codes
E1–E12 as in criteria v1.1 §1 (numbering unchanged; schema pattern `^E(1[0-2]|[1-9])$`). **Primary code when several apply [OPEN — researcher decision; Q-081]:** v0.1 §5 states "The first applicable code in numerical order is the primary reason", but no approved decision adopts this general rule (D-074 status); it is carried only as the proposed convention (criteria v1.1 §1 note). Approved: a Stage-0 row qualifying for both E7 and E5 takes E7 (D-074 (d)).

## 7. Pilot (D-025, D-059 A-1)
| Item | Rule |
|---|---|
| When | Only after D-035 record §6 conditions 1–6 are met **and recorded**, criteria v1.1 / protocol v0.2 are frozen, **and** the researcher has separately and explicitly authorised the draw (D-077 (6)). Not before. Meeting the other prerequisites does not authorise the draw |
| Size, seed | 60 records; stratified random; seed **4004** recorded in the pilot file |
| Sampling frame | The 1,470-record D-044 scope, excluding Stage-0 records; records without abstracts allowed |
| Strata and allocation | **D-063 (APPROVED — CONDITIONAL, inactive):** near-equal allocation B 8, A 8, untagged 8, F 8, C 7, E 7, D 7, Q 7 (= 60). Frame (revised after D-074, researcher approval of F1, 2026-10-31; D-063 status history): the 1,470 D-044 records minus 7 Stage-0 records = 1,463 (eligible B 623, A 365, untagged 173, F 120, C 93, E 68, D 13, Q 8; D-063 originally used 9 Stage-0 records and 1,461); rarest-theme rule F, D, C, E, A, Q, B; no theme → untagged. **Deterministic draw:** paper IDs sorted ascending within each stratum; one `random.Random(4004)`; strata drawn in the order F, D, C, E, A, Q, B, untagged; inventory SHA-256 and script recorded in `pilot_sample.csv`. **Sampling call (D-077):** within each stratum, one key `rng.random()` is drawn for each `paper_id` in ascending order, and the *k* records with the smallest `(key, paper_id)` pairs are selected. A theme-representation design, not a population-proportional sample. The sample is **not** generated |
| Screeners | The assistant and **the researcher (second screener)** screen the same 60 **independently and blinded**. The researcher's sheet shows title, abstract, year, venue and types, and no assistant decision. **The researcher must personally perform the 60 blinded assessments**; the pilot is not complete until they are recorded |
| Agreement | Percentage agreement; Cohen's κ on 3-level decision and on include vs not; primary-code agreement; per-descriptor agreement (incl. `biomarker_class`, `validation_design`) |
| Pass | κ (3-level) ≥ 0.60 **and** no record excluded by one screener and included by the other without adjudicated agreement **and** fewer than 3 disagreements on any single code |
| If not passed | Disagreements reviewed together; criteria clarified (new version); second pilot of 40 new records, same strata rule, next seed. **[OPEN — researcher decision; Q-083]:** no approved decision defines the retry beyond this summary (protocol v0.1 §7; D-025 approved its "pass criteria and adjudication as written" but does not name the retry): the seed and its derivation ("next seed"), the allocation of 40 records across the D-063 strata, the frame (whether the first 60 are excluded) and its recording in a pilot file. D-063 and D-077 cover the first 60 only |
| Outputs | `screening/pilot_sample.csv` (IDs, stratum, seed, inventory SHA-256 and the sampling script; D-063, D-077), `pilot_decisions_assistant.csv`, `pilot_decisions_researcher.csv`, `pilot_report.md` (metrics computed by script) |
| Missing-abstract review | The researcher reviews every title/abstract decision on a record without an abstract; such records are listed separately in `pilot_report.md` with their D-068 (8) status, *not retrieved* or *unavailable*; the six current records are classified *unavailable — PubMed* (D-079) (D-068 (10)) |

## 8. Expansion and audit
* Only after a passed pilot and researcher approval: remaining D-044 records in batches of about 300.
* **Audit (D-008):** after the first two expansion batches (timing taken from protocol v0.1 §7 "Expansion" row; D-008 sets none; [OPEN — researcher confirmation; Q-084]; criteria v1.1 §7), the researcher blind-audits 25 `include` + 25 `exclude`; κ < 0.60 or a wrongful exclusion → criteria clarification and re-screening of affected records. Selected 2026-10-30; **not performed**.
* **Missing-abstract review (D-068 (10)):** in every expansion batch, every title/abstract decision on a record without an abstract is reviewed by the researcher, in addition to the D-008 audit.

## 9. Verification and citation (unchanged requirements)
Screening may use `partially_verified` records; only `verified` records may be **cited** (`research_plan.md` §6). The arXiv transcription spot-check passed for the 5 LIT-003 arXiv files (2026-10-30) and is recorded in `MANIFEST.csv` (`transcription_check=passed`). It used the same connector, so it is not independent metadata verification; `verified` additionally needs a second agreeing source, and whether a web result counts is Q-068 (open). At the next build, 2 of the 76 records (P2870, P2941; also retrieved by Q-WS-02/Q-WS-04) could become `verified` under the current rule if their web members carry metadata (not checkable in this workspace); this should be reviewed with Q-068 before any citation. Q-AX-G9 and web files remain unchecked.

## 10. Activation checklist (all must be recorded before the pilot)
| # | D-035 record §6 condition | Assessment on 2026-11-01 (not a formal record; refreshed in FREEZE-DRAFT-CORRECTIONS and the pre-freeze documentation correction) |
|---|---|---|
| 1 | Q-039 | Assessed as met at decision level (D-036; `DECISION_LOG.md` status history: "Q-039 condition met by D-036"); not formally recorded as a D-035 §6 condition |
| 2 | Q-040 | Assessed as met at decision level; not formally recorded (D-055; flag name D-061, effective at freeze; may co-occur with `non_metabolic_method_exemplar`, D-070) |
| 3 | D-027, D-024 approved | Assessed as met at decision level; not formally recorded (D-027 limited; D-024 conditional, R5 condition met). **[OPEN — researcher decision; Q-085]:** whether D-027's limited approval (required columns and key only) and D-024's conditional approval satisfy "approved" |
| 4 | R5/D-029 remaining items | Assessed as met at decision level; not formally recorded (D-060) |
| 5 | Criteria v1.1 / protocol v0.2 frozen | **Unmet**: drafts exist (revised 2026-10-31 for D-070–D-076 and 2026-11-01 for D-077–D-079 and the freeze-readiness corrections); review and freeze pending. Q-080 answered by D-074; Q-078 answered by D-075; Q-079 answered by D-076 (2026-10-31) |
| 6 | Other pilot-blocking items | **Unmet**. Done: arXiv spot-check recorded in `MANIFEST.csv`; pilot allocation decided (D-063); implementation of D-028 2a–2d, D-029 as specified in D-060, D-057, D-058 and D-061 with tests (T1-A, commit `d1aaceb`; 122 literature tests passed on that commit). Also done: validator support for the D-069 vocabulary with the D-070 co-occurrence rule and rejection of repeated tokens (D-078), and the D-068 (5) Stage-0 exemption limit (Option A), with tests (commit `2fcc7b9`); the T2 rebuild with removal of `dim_independent_validation` from generated outputs and schemas (commit `bf0c579`; inventory SHA-256 `b668dbde…`); classification of the 6 in-scope records without an abstract as *unavailable — PubMed* (D-079). Pending: the researcher's recording of this condition (implementation complete is not the same as recorded as met). The D-035 record does not itemise condition 6; the items above are those documented, not a closed list **[OPEN; Q-086]** |

**Status terms.** *Assessed as met at decision level* means the governing decision exists; it is not a formal record that the condition is met. **No condition 1–6 has been formally recorded as met.** Conditions 5 and 6 are **unmet**. **[OPEN — researcher decision; Q-087]:** whether conditions 1–4 need their own formal record or are recorded together with conditions 5 and 6 in one D-035 §6 record. Until the researcher records them, §7 does not treat any condition as met.

## 11. Traceability: changes from v0.1
| § | Change | Governing decision |
|---|---|---|
| §1 | Input set = 1,470 (was 2,979 inventory); Q-PM-02 all screened | D-044; D-009 |
| §2 | Required descriptors; `record_type` list without `preprint`/`notice`; `validation_design` replaces `dim_independent_validation`; `biomarker_class`; descriptor meanings; triage-only use | D-028; D-029; D-058; D-060 |
| §2 | `publication_type` from mapping table; arXiv → preprint; no URL/DOI rules | D-028 |
| §2a | Unchanged | D-031–D-038 |
| §3 | E4 exceptions incl. D-055 flag; RQ5 routing at ≥ 3; missing-abstract rule | D-055; D-059; D-060 |
| §4 | Unchanged; A-4 deferred | D-059; D-030 |
| §5 | Audit-trail rules made explicit (append-only, required fields, provenance) | D-027; D-036; D-010 |
| §7 | Sampling frame = D-044 scope; researcher as second screener; near-equal allocation | D-025; D-059 A-1; D-063 |
| §8 | Audit selected, not performed | D-008 |
| §9 | Spot-check outcome (recorded in `MANIFEST.csv`); citation limits | D-012; D-023; Q-021/Q-064/Q-068 |
| §2, §3 | Flag name; RQ5 tier rule | D-061; D-062 |
| §3 | Both non-metabolic retention tags allowed on one record; retraction notices not Stage-0 types; Stage-0 list compared with v0.1 §3; multi-type handling settled (D-074); notice coding settled (D-076) | D-070; D-072; D-068 (5); D-074; D-076 |
| §10 | Checklist refreshed to the state on 2026-10-31 | Researcher-approved documentation update (H1-H8-DECISIONS) |
| §6 | Stage-0 rows qualifying for both E7 and E5 take E7 | D-074 |
| Header; §1; §3; §10 | Proposed `criteria_version`; six records without an abstract classified *unavailable — PubMed* (R1); Stage-0 exemption worded as its scope (Option A, matching the validator); type list re-verified against v0.1 §3; §10 refreshed (validator, T2 and classification done; no condition recorded as met) | D-068 (5), (8); D-078; D-079; researcher directions 2026-11-01 |
| §2a, §3, §5 | `non_metabolic_rq5_candidate` reassessed on full-text, verification and adjudication rows (possible = `yes` or `unclear`; flag only when ≥ 3) | D-075 |
| §7 | Pilot frame revised after D-074 (1,463; F1); sampling call fixed as random-key selection | D-063 (status history); D-077 |
| §5, §6, §7, §8, §10 | Pre-freeze reconciliation (2026-11-01): general code precedence, retry procedure, audit timing, condition 3 and the scope of condition 6 marked [OPEN]; missing-abstract statuses aligned with D-068 (8) and D-079; `criteria_version` enforcement gap stated. No approved rule changed; the general code-precedence rule, which no approved decision adopts, is now presented as a proposed convention | D-008; D-024; D-025; D-027; D-035 record §6; D-063; D-068 (8); D-074; D-077; D-079 |
| §8 of v0.1 (blockers B-1…B-6) | Superseded by §10 checklist; B-1, B-3, B-4 implemented (D-027 limited); B-2 = D-030 open; B-5 resolved in this workspace by restoration (Q-063 open); B-6 answered by D-008, D-009, D-043, D-056, D-057 (Q-022 still open) | As listed |
