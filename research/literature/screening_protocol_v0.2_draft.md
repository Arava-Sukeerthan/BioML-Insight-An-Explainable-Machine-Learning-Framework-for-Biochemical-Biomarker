# Title/Abstract and Full-Text Screening Protocol — version 0.2 (DRAFT)

| Field | Value |
|---|---|
| Task | SCREENING-PREREQ-DECISIONS-2 (2026-10-30; assistant draft) |
| Version | **0.2 — DRAFT for researcher review. NOT frozen. Not in force.** |
| Replaces | `screening_protocol.md` v0.1 only when the researcher approves and freezes this text together with `screening_criteria_v1.1_draft.md` as the pilot's `criteria_version` (D-035 record §6, condition 5). v0.1 is kept unchanged |
| Screening status | **INACTIVE.** No record has been screened, labelled or sampled. No pilot sample exists |
| Scope of claims | The protocol does not assume that the BioML-Insight framework is new or better. Screening describes the existing evidence; any research gap is decided later (Stage D, D-016) from verified, screened evidence |
| Governing decisions | As in criteria v1.1 §9, plus D-008, D-010, D-012/D-023, D-025, D-042, D-044, D-045, D-061, D-062, D-063, D-068. Traced in §11 |

---

## 1. Input set
| Item | Value | Source |
|---|---|---|
| Records to screen | **1,470** publication records (D-044 scope) | `paper_inventory.json` SHA-256 `a509538dc5e1cf41cd7a4e180ed17df86f6d4cd83a7d227abea073f1689af4a3`; re-counted 2026-10-30 from `paper_inventory.csv` query IDs |
| Q-PM-02 | All 743 records, all inside the 1,470 (D-009) | Inventory check 2026-10-30 |
| Without abstract | 6 records in scope (`abstract_available=False`); before screening each is to be classed as *not retrieved* or *unavailable*, and retrieval completed where feasible under separate authorisation (D-068 (8), (9)) | Inventory check 2026-10-30 |
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
Five components, `yes` only for a qualifying procedure applied with a documented output (D-032; D-035 §2); `unclear` = assessed but unresolved; empty = not assessed. Statuses are **confirmed** only on a `full_text` row; a full-text RQ5 assessment records all five. The build derives `rq5_coverage_group` (`qualified` ≥ 4, `near_rq5` = 3, `below_threshold` 0–2) and `rq5_coverage_provisional` (D-034, D-036, D-037) from confirmed statuses; screeners never assign it. Researcher verification of `qualified`/`near_rq5` records: new `full_text` row with `screener=researcher` (D-035 G4). Reporting of four-`yes` subgroups per D-038.

## 3. Decision rules
| Distinction | Rule (doubt → `uncertain`) | Basis |
|---|---|---|
| Metabolic vs broader biomedical targets | RQ1 requires a §2.1 target. Non-metabolic targets are E4 **unless** retained as `non_metabolic_method_exemplar` (RQ2–RQ5 methods applicable to tabular/omics/lab data) **or** flagged `non_metabolic_rq5_candidate` (≥ 3 possible RQ5 components counting `unclear`) | Criteria v1.1 §1 E4; D-055; D-059 |
| Biochemical vs imaging-/genetics-only inputs | §2.2; multi-omics with a substantive metabolomics layer eligible (`uncertain` if unclear whether metabolites enter the model) | D-043; D-057 |
| Original vs reviews, notices, retractions, duplicates | Reviews: `review_lead` only. Errata → Stage 0 E5. Retractions → Stage 0 E7. Duplicates → E8 only after a recorded decision; A-4 deferred (D-030), both records of a pair screened | D-059 |
| RQ5 routing | ≥ 3 possible components counting `unclear` → `uncertain`, `needs_human=yes`, full text | D-060 (4) |
| Missing abstract (title/abstract only) | `uncertain` → full text unless Stage-0 E5/E7 or a title-level E1 (frozen wording); **no E4**; method descriptors and `validation_design` `unclear`; `biomarker_class` `unclear` unless the title explicitly supports it; all five preliminary component statuses `unclear` ("no abstract"); `rq_tags`/`record_type` provisional; no RQ5-based tier | D-060 (2) as amended by D-068; D-059 A-6 |

**Stage 0 (automatic, counted, reversible):** PubMed types *Editorial*, *Comment*, *News*, *Published Erratum* → E5; *Retracted Publication* → E7; letters are not auto-excluded. Rows carry `screener=rule:stage0`, which is used only on `exclude` rows with E5 or E7 from source publication types (D-068 (5); list to be verified against its approved source at the freeze). All Stage-0 decisions are listed in the pilot report.

## 4. Possible duplicates and versions
Unchanged from v0.1 §4: no pair decision exists; both records are screened; pairs are listed in the pilot report. A-4 and D-030 are deferred/proposed. E8 only after a recorded decision.

## 5. Ambiguity handling, adjudication and audit trail
1. **When in doubt, `uncertain`.** Exclusion needs a positive reason found in the title/abstract.
2. **Every row records** `screener`, `date`, `justification` (≤ 1 sentence, quoting the decisive phrase where possible) and `criteria_version` (the frozen version string).
3. **Append-only:** decisions are never edited or deleted; a correction or adjudication is a new row (`screener=researcher` for adjudication), and the build uses the latest row per `paper_id` and `stage` while keeping all rows. The build rejects rows that blank a recorded component (D-036).
4. **Adjudication queue** (`screening/adjudication_queue.csv`): every `uncertain`, every E12, every `needs_human=yes`, all possible-duplicate pairs.
5. **Criteria changes** after screening starts: question in `unresolved_questions.md`; accepted change logged in `DECISION_LOG.md` as a new criteria version; every record decided under the old wording with an affected code is re-screened.
6. **Provenance:** decisions refer to `paper_id` only; source records, raw exports and the manifest are never edited by screening. Inventory and reports are regenerated by the build, not by hand.
7. **Data protection:** no abstracts or raw records enter committed files (D-010).

## 6. Exclusion codes
E1–E12 as in criteria v1.1 §1 (numbering unchanged; schema pattern `^E(1[0-2]|[1-9])$`). First applicable code is primary.

## 7. Pilot (D-025, D-059 A-1)
| Item | Rule |
|---|---|
| When | Only after D-035 record §6 conditions 1–6 are met **and recorded**, and criteria v1.1 / protocol v0.2 are frozen. Not before |
| Size, seed | 60 records; stratified random; seed **4004** recorded in the pilot file |
| Sampling frame | The 1,470-record D-044 scope, excluding Stage-0 records; records without abstracts allowed |
| Strata and allocation | **D-063 (APPROVED — CONDITIONAL, inactive):** near-equal allocation B 8, A 8, untagged 8, F 8, C 7, E 7, D 7, Q 7 (= 60). Frame: the 1,470 D-044 records minus 9 Stage-0 records (eligible B 622, A 364, untagged 173, F 120, C 93, E 68, D 13, Q 8); rarest-theme rule F, D, C, E, A, Q, B; no theme → untagged. **Deterministic draw:** paper IDs sorted ascending within each stratum; one `random.Random(4004)`; strata drawn in the order F, D, C, E, A, Q, B, untagged; inventory SHA-256 and script recorded in `pilot_sample.csv`. A theme-representation design, not a population-proportional sample. The sample is **not** generated |
| Screeners | The assistant and **the researcher (second screener)** screen the same 60 **independently and blinded**. The researcher's sheet shows title, abstract, year, venue and types, and no assistant decision. **The researcher must personally perform the 60 blinded assessments**; the pilot is not complete until they are recorded |
| Agreement | Percentage agreement; Cohen's κ on 3-level decision and on include vs not; primary-code agreement; per-descriptor agreement (incl. `biomarker_class`, `validation_design`) |
| Pass | κ (3-level) ≥ 0.60 **and** no record excluded by one screener and included by the other without adjudicated agreement **and** fewer than 3 disagreements on any single code |
| If not passed | Disagreements reviewed together; criteria clarified (new version); second pilot of 40 new records, same strata rule, next seed |
| Outputs | `screening/pilot_sample.csv` (IDs, stratum, seed), `pilot_decisions_assistant.csv`, `pilot_decisions_researcher.csv`, `pilot_report.md` (metrics computed by script) |
| Missing-abstract review | The researcher reviews every title/abstract decision on a record without an abstract; such records are listed separately in `pilot_report.md` with *not retrieved* / *unavailable* status (D-068 (10)) |

## 8. Expansion and audit
* Only after a passed pilot and researcher approval: remaining D-044 records in batches of about 300.
* **Audit (D-008):** after the first two expansion batches, the researcher blind-audits 25 `include` + 25 `exclude`; κ < 0.60 or a wrongful exclusion → criteria clarification and re-screening of affected records. Selected 2026-10-30; **not performed**.
* **Missing-abstract review (D-068 (10)):** in every expansion batch, every title/abstract decision on a record without an abstract is reviewed by the researcher, in addition to the D-008 audit.

## 9. Verification and citation (unchanged requirements)
Screening may use `partially_verified` records; only `verified` records may be **cited** (`research_plan.md` §6). The arXiv transcription spot-check passed for the 5 LIT-003 arXiv files (2026-10-30) and is recorded in `MANIFEST.csv` (`transcription_check=passed`). It used the same connector, so it is not independent metadata verification; `verified` additionally needs a second agreeing source, and whether a web result counts is Q-068 (open). At the next build, 2 of the 76 records (P2870, P2941; also retrieved by Q-WS-02/Q-WS-04) could become `verified` under the current rule if their web members carry metadata (not checkable in this workspace); this should be reviewed with Q-068 before any citation. Q-AX-G9 and web files remain unchecked.

## 10. Activation checklist (all must be recorded before the pilot)
| # | D-035 record §6 condition | State on 2026-10-30 |
|---|---|---|
| 1 | Q-039 | Met (D-036) |
| 2 | Q-040 | Met at decision level (D-055; flag name D-061, effective at freeze) |
| 3 | D-027, D-024 approved | Met at decision level (D-027 limited; D-024 conditional, R5 condition met) |
| 4 | R5/D-029 remaining items | Met at decision level (D-060) |
| 5 | Criteria v1.1 / protocol v0.2 frozen | **Unmet**: drafts exist; review and freeze pending |
| 6 | Other pilot-blocking items | **Unmet**: implementation of D-028/D-029/D-058/D-060/D-061 + tests + rebuild. Done: arXiv spot-check recorded in `MANIFEST.csv`; pilot allocation decided (D-063) |

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
| §8 of v0.1 (blockers B-1…B-6) | Superseded by §10 checklist; B-1, B-3, B-4 implemented (D-027 limited); B-2 = D-030 open; B-5 resolved in this workspace by restoration (Q-063 open); B-6 answered by D-008, D-009, D-043, D-056, D-057 (Q-022 still open) | As listed |
