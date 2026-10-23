# Scope Decision Brief (before pilot screening)

| Field | Value |
|---|---|
| Task | LIT-004-REVIEW-AND-DECISIONS (2026-10-23) |
| Status | **Brief for the researcher. Nothing in it is approved.** Every option keeps the earlier proposals (Q-001, Q-002, D-008, D-009, Q-022) open; none is superseded |
| Sources | `screening_criteria.md` §1–§3 (draft v1.0), `screening_protocol.md` §3 (draft v0.1), `research_plan.md` §2, §5, `search_strategy.md` §6, `logs/DECISION_LOG.md`, `research/reviews/unresolved_questions.md`, `research/literature/records/collection_stats.json`, `paper_inventory.json` |

Labels: `[EVIDENCE]` from project files and counts; `[RECOMMENDATION]` assistant proposal; `[OPEN]` needs the researcher.

## 1. Metabolic disorders in scope (Q-001)

**Current provisional scope** `[EVIDENCE]` (`screening_criteria.md` §2.1, unchanged since LIT-001):
- in scope: type 1, type 2 and gestational diabetes; prediabetes / impaired glucose regulation;
  insulin resistance; metabolic syndrome; NAFLD/MASLD/NASH/MASH; dyslipidaemias; hyperuricaemia and gout;
  inborn errors of metabolism, including newborn-screening targets;
- retained but tagged `scope_pending`: obesity (as a classification target), thyroid dysfunction, PCOS;
- out of scope (E4): complications as the target (e.g., retinopathy, nephropathy), cardiovascular events,
  cancer, infection, except as method exemplars (§3 below).

**Options** `[OPEN]`
| Option | Effect |
|---|---|
| 1a. Confirm the list as it stands, `scope_pending` disorders kept and tagged | Nothing is lost; the pending three can be dropped later without re-screening |
| 1b. Confirm and move obesity / thyroid / PCOS fully in or fully out | Resolves the tag now. "Out" means E4 for those records |
| 1c. Narrow to a disorder group now (e.g., diabetes spectrum only) | Smaller workload, but D-013 says the primary disorder should be chosen from the landscape, not before it |

`[RECOMMENDATION]` 1a. The primary disorder (D-013) is a later, separate decision, and a broad
landscape is what Stage D needs.

## 2. Biochemical biomarkers and data modalities (Q-002)

**Current provisional scope** `[EVIDENCE]` (§2.2): metabolomics/lipidomics (MS or NMR, any
biofluid or tissue); newborn-screening MS/MS profiles; routine clinical chemistry (glucose, HbA1c,
lipids, liver enzymes, renal markers, insulin/C-peptide, uric acid; CBC only with chemistry);
mixed feature sets in which biochemical markers are substantive (≥ 1 among the final predictors,
or stated). Out (E3): imaging-only, genomics/transcriptomics/methylation-only, microbiome-only,
free-text-only, CGM/wearable-only, questionnaire-only. Multi-omics with metabolomics as one
substantive layer: eligible (`screening_protocol.md` §3).

**Gaps found in the definitions** `[EVIDENCE]`
- **Proteomics** (and other protein-biomarker panels, e.g. cytokines) is listed neither in scope nor out of scope (new Q-033).
- "Substantive" for mixed sets has two different tests (stated vs ≥ 1 final predictor); the abstract usually shows only one. The protocol sends unclear cases to `uncertain`.

**Options** `[OPEN]`: 2a both strands (metabolomics + routine chemistry), as now; 2b metabolomics/lipidomics only;
2c routine chemistry only. Separately: proteomics in, out, or `scope_pending`.

`[RECOMMENDATION]` 2a, with proteomics `scope_pending` until Q-033 is answered, so nothing has
to be re-screened whichever way it is decided.

## 3. Broader biomedical ML studies

**Current rule** `[EVIDENCE]` (`screening_criteria.md` §3, `screening_protocol.md` §3): an applied model for
a non-metabolic target is `exclude E4` for RQ1. It may be **retained** for RQ2–RQ5 only if it
develops or evaluates explanation, calibration, uncertainty, validation/shift or integrated-framework
methods applicable to tabular, omics or laboratory data (`scope_flags=non_metabolic_method_exemplar`).
RQ5 keeps any domain as closest prior art.

`[EVIDENCE]` The inventory contains many such records: several of the 15 dedup pairs alone concern
Alzheimer's disease, sepsis, depression, pulmonary hypertension and cancer (titles in
`records/dedup_review.csv`). Their number is unknown until screening.

**Options** `[OPEN]`
| Option | Effect |
|---|---|
| 3a. Keep the current rule | Method exemplars available for RQ2–RQ5; requires a judgement per record |
| 3b. Retain only methodological papers (new methods or method evaluations); exclude every applied non-metabolic study, even one that reports SHAP or calibration | Fewer, clearer decisions; loses applied examples of how calibration/uncertainty are reported |
| 3c. Exclude all non-metabolic records except RQ5 frameworks | Smallest set; weakens RQ2–RQ4 |

`[RECOMMENDATION]` 3a, with a sharper test written into the criteria: "retained only if the
abstract states that the explanation, calibration, uncertainty or validation method is itself
developed, compared or evaluated; merely applying it is E4".

## 4. The routine-biochemistry query Q-PM-02 (Q-007 / D-009)

`[EVIDENCE]`
- Q-PM-02 returned 743 records; 626 of them were retrieved by **no other query**, i.e. 21 % of the 2,979 publications.
- 83 of the 743 were also retrieved by a theme C, D or E query (explainability, calibration/uncertainty, validation). This is a **retrieval-overlap proxy**. Option B as defined in D-009 (term matching in title/abstract) has not been applied, and its real size is unknown.

**Options** (D-009, unchanged) `[OPEN]`
| Option | Screening | Reporting consequence |
|---|---|---|
| A. Screen all 743 at title/abstract; full text by tier | All records screened | Standard flow diagram |
| B. Screen only records that also match XAI/calibration/UQ/external-validation terms; characterise the rest by a random sample | Fewer records | The search was **executed** without the restriction, so B is a post-search restriction. The flow diagram must show the records retrieved but not screened, the rule used, and the sample. The RQ1 landscape for routine chemistry is then an estimate, not a count |

`[RECOMMENDATION]` A (as D-009 already recommends). Title/abstract screening of 743 records is
feasible, and B would weaken the RQ1 description for exactly the biomarker class that matters most for dataset feasibility.

## 5. Audits and approvals for the executed search (Q-022, Q-008 / D-008)

`[EVIDENCE]` The LIT-003 searches ran while these proposals were still PROPOSED:
- D-005, the review type;
- D-006, the sources and routes;
- D-007, the date windows;
- D-010, the storage rule;
- D-012 and D-023, the transcription checks.

Deviations from the strategy are documented in `access_report.md` and `collection_summary.md` §7:
- Consensus was not run (quota exhausted).
- Europe PMC, Crossref, Semantic Scholar and the repository APIs were not run (hosts blocked).
- The search ran on Day 10 instead of Day 3.
- The web domain filter was not honoured.
- arXiv records have no authors.
- The off-device backup is unavailable.

**Approvals and audits still needed** `[OPEN]`
| Item | What the researcher decides |
|---|---|
| Q-022 | Approve D-005, D-006, D-007 as executed, **including** the deviations above. Otherwise name the changes, and the affected queries are re-run |
| D-010 / Q-011 | Approve the storage rule, and accept or resolve the missing off-device backup |
| D-012 / D-023 | Approve the transcription controls (15/15 PubMed queries identical on re-fetch) |
| D-008 / Q-008 | Confirm the researcher audit: 25 includes + 25 excludes, blinded (about 60–75 min), and the κ < 0.60 rule |
| D-025 / Q-026 | Approve the 60-record pilot (or keep the `screening_criteria.md` §7 pilot) |

`[RECOMMENDATION]` Approve D-005–D-007 as executed, with the deviations recorded as limitations rather than re-run now. Most of them are access limits that a re-run in this container would not remove.
