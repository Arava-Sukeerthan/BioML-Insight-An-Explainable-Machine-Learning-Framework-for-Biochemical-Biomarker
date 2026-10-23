# Literature Research Plan

| Field | Value |
|---|---|
| Task | BIO-001 (2026-10-23) |
| Version | 1.0 — **DRAFT, pending researcher approval** |
| Role | Overview of how existing work will be investigated. The detailed, executable design is in `search_strategy.md` (v1.0.1), `search_queries.csv`, `screening_criteria.md` and `collection_workflow.md` (LIT-001/LIT-002). If this overview and those files disagree, the detailed files apply and the difference is logged as an open question. |
| Search status | Updated LIT-003 (2026-10-23): PubMed (15 queries), arXiv via alphaXiv (5) and web search (6) **executed**; 2,979 publications collected and deduplicated; bibliographic verification automatic (`verification_report.md`). Consensus, Europe PMC, Crossref, Semantic Scholar and repository APIs not run (`access_report.md`). **Nothing screened or extracted.** |
| References | **This document cites no publications.** Candidate foundational items recalled from memory are listed as **unverified** seeds in `search_strategy.md` §4.11 and may not be cited until verified. |

---

## 1. Provisional research question `[OPEN]`
> To what extent can a classification framework for metabolic disorders based on biochemical
> biomarkers combine (i) explanation of its predictions, (ii) calibrated probabilities and
> (iii) uncertainty estimates, while keeping discrimination comparable to standard baselines,
> and does that behaviour hold on independent data?

The literature review exists to test whether this question is worth asking. Specifically: is it
already answered, partly answered, or still open, and for which disorders and datasets? It does
**not** exist to justify a predetermined framework. The question may be narrowed or changed after
Stage D (decisions D-013, D-016).

## 2. Principal literature themes
| Theme | Topic | Review question (`search_strategy.md` §1.2) | Main evidence sought |
|---|---|---|---|
| A | Metabolomics-based metabolic-disorder classification | RQ1 (metabolomics strand, Q-PM-01, Q-PM-03) | Original studies: disorders, platforms, models, sample sizes, validation designs |
| B | Biochemical (routine clinical-chemistry) biomarker-based ML | RQ1 (routine-biochemistry strand, Q-PM-02) | As A, for laboratory panels (glucose, HbA1c, lipids, liver enzymes, etc.) |
| C | Explainable ML for biomedical prediction | RQ2 (Q-PM-04, Q-PM-05) | Which explanation methods are used, and whether their stability or faithfulness is evaluated |
| D | Probability calibration and uncertainty estimation | RQ3 (Q-PM-06–08) | Calibration measures and recalibration; conformal and other uncertainty-quantification methods for tabular classifiers; how often applied studies report them |
| E | Independent validation and cross-cohort generalisation | RQ4 (Q-PM-09, Q-PM-10) | How often external validation is done; performance and calibration change under dataset shift; batch/site effects |
| F | Existing integrated frameworks combining several components | RQ5 (Q-PM-11, Q-PM-12) | **Closest prior art**: pipelines covering ≥ 3 of {biomarker selection, classification, explainability, calibration/uncertainty} |
| (cross-cutting) | Methodological quality and reported limitations | RQ6 (Q-PM-13, Q-PM-14) | Reviews, reporting guidelines, risk-of-bias tools, leakage and reproducibility studies |

## 3. Candidate scholarly databases
Access status was **tested** on 2026-10-14 (probes PROBE-01…12) and re-checked for the APIs on
2026-10-23 (BIO-001: `curl` to E-utilities, Europe PMC, Crossref, Semantic Scholar and arXiv API
all returned no connection, HTTP 000). Listing a source here does **not** mean it has been searched.

| Source | Planned role | Access at present |
|---|---|---|
| PubMed | Primary, reproducible source (15 planned queries) | Usable through the PubMed connector. The official E-utilities API is blocked (client written and tested offline, Q-003) |
| Europe PMC | Preprints, full-text search, repository citations (6 queries) | Blocked. Run if the host is enabled or the researcher exports results |
| Crossref | DOI and metadata verification; keyword search (3 queries) | Blocked |
| Semantic Scholar | CS/ML venues (5 queries) | Blocked. Consensus connector as a partial, non-reproducible proxy (10 queries) |
| Google Scholar | Recall check (4 queries) | Not accessible to the assistant; optional manual search by the researcher (Q-009) |
| arXiv (via alphaXiv) | ML-methods literature for themes C, D, E, F (5 queries) | Usable through the connector |
| Publisher websites | IEEE, ACM, Springer/BMC, Elsevier, Nature, OUP, Wiley, MDPI, Frontiers, PLOS, ACS, PMLR (5 domain-restricted web queries) | Search works; pages cannot be opened. Every hit needs verification elsewhere |
| Metabolomics Workbench / MetaboLights | Publications linked to repository datasets (theme A, E) | APIs blocked; PubMed route (Q-PM-15) and web search fallback |

## 4. Proposed search concepts
The concept blocks are defined in `search_strategy.md` §3. Exact strings are in `search_queries.csv`.
- **D** metabolic disorders · **M** metabolomics/lipidomics · **B** routine biochemical biomarkers · **L** machine learning
- **X** explainability · **C** calibration · **U** uncertainty · **E** external validation / dataset shift · **F** biomarker selection · **Q** methodological quality

Theme-to-block mapping: A = D∧M∧L; B = D∧B∧L; C = (M∨B)∧L∧X; D = L∧(C∨U), applied and
methodological; E = D∧(M∨B)∧L∧E plus methodological shift; F = (M∨B)∧L∧F∧X∧(C∨U) plus
framework/pipeline title terms. Known term problems (e.g., "calibration" retrieving
analytical-chemistry calibration, ambiguity of "LIME" and "SHAP") and how they are handled are
documented in `search_strategy.md` §3.1.

## 5. Preliminary eligibility criteria
Full criteria with codes are in `screening_criteria.md` (draft). Summary:

**Inclusion (preliminary):** peer-reviewed article, full conference paper, or flagged preprint;
English; original research, methodological paper, software/framework paper, or reporting
guideline (reviews used as lead sources); human data for application themes A, B and the
application parts of C/E; supervised classification or risk-probability models; biochemical
biomarkers (metabolomics/lipidomics, newborn-screening MS/MS, routine clinical chemistry, or
mixed sets in which they are substantive); target disorder within the provisional scope (Q-001).
Methodological papers for themes C, D, E and F may come from any biomedical domain.

**Exclusion (preliminary):** non-human data for application themes; no predictive model;
non-biochemical inputs only (imaging, genomics, microbiome, wearables, questionnaires);
disorder out of scope; editorials, comments, conference abstracts, protocols without results;
non-English; retracted; insufficient abstract and no full text; regression-only targets for theme
A/B. Sample size, journal and country are **not** exclusion criteria.

Pending inputs: disorder scope (Q-001), biomarker class (Q-002), date windows (D-007, Q-010),
handling of the routine-biochemistry strand (D-009, Q-007).

## 6. Publication verification requirements
From `search_strategy.md` §7 and `collection_workflow.md` §4.3:
- A publication may be **cited** in project documents only if `verification_status = verified`. That requires title, first author, year, venue and at least one persistent identifier (PMID, DOI or arXiv ID) retrieved from an authoritative index, and consistent with a second source.
- `partially_verified` (one index only) records can be screened but not cited. `unverified` records (web search, memory seeds, secondary citations) are looked up before use. `failed` records are excluded.
- Reviews are lead sources. A finding is attributed to an original study only after that study itself is retrieved and verified.
- Retractions, errata and expressions of concern are checked from publication-type metadata.
- Preprints are labelled as such. The published version is preferred.
- Raw tool outputs are saved unchanged with SHA-256 checksums. Transcribed connector output is spot-checked (≥ 10 % re-fetch, D-012).
- DOIs, author names and numbers are never completed from memory.

## 7. Evidence-extraction requirements
For each included study (fields in `schemas/paper_inventory.schema.json`, extraction per
`search_strategy.md` §8.1–8.2):
- disorder, outcome definition, biomarker type and panel, platform;
- dataset name/source, population, sample size and class counts, data availability;
- models and baselines, feature-selection method and where it was fitted (inside or outside resampling);
- explainability method and whether its stability or faithfulness was evaluated;
- calibration measures/method, and uncertainty method and its evaluation;
- validation design (apparent / CV / nested CV / temporal / external) and leakage safeguards;
- reported metrics **copied verbatim** with their location (section/table), flagged `abstract_only` when not from the full text;
- stated limitations, code availability, and the RQ/theme tags and tier.

The researcher spot-checks 5 extracted records (planned).

## 8. Research-gap assessment strategy
1. **Evidence tables per theme** (A–F), built only from verified records. These give counts of methods, explanation techniques, calibration/uncertainty techniques and validation designs.
2. **Gap matrix** (planned `research/literature/research_gap_matrix.md`): rows = disorder × biomarker class; columns = explainability, calibration, uncertainty, external validation, integrated framework, code/data availability. Each cell links to inventory IDs. An empty cell is reported as "not found in the searched sources", not as "does not exist".
3. **Closest-prior-art table (theme F)**: every pipeline that combines ≥ 3 components is described in detail (components, data, validation, limitations). This table **must be complete before any novelty claim** (D-016).
4. **Appraisal of quality**: structured appraisal items (`search_strategy.md` §8.2) distinguish areas with *few* studies from areas with *many low-quality* studies.
5. **Feasibility filter**: a gap is only a candidate contribution if genuine data to study it exist (D-014, D-015) and it can be investigated within the schedule.
6. Every gap statement is labelled `[EVIDENCE]`, `[HYPOTHESIS]` or `[OPEN]`. The researcher approves the gap and contribution (Stage D gate). **A gap is a hypothesis until the closest-prior-art check is done.**

## 9. Planned literature-review deliverables
None of these exist yet.
| Deliverable | Planned path | Stage |
|---|---|---|
| Executed query rows, raw exports with manifest | `search_queries.csv`, `raw_exports/MANIFEST.csv` | B |
| Deduplicated, verified publication records and abstract-free index | `records/` (see `collection_workflow.md` §7) | B |
| Screening decisions and researcher audit sample | `screening/` | B |
| Paper inventory with extraction fields | `paper_inventory.csv/.json` | B |
| Record-flow diagram (PRISMA-2020-style) and search appendix | `research/literature/` | B |
| Evidence tables per theme and critical comparison | `literature_review.md` | C |
| Gap matrix and closest-prior-art table | `research_gap_matrix.md` | D |
| Proposed contribution and feasibility note for researcher approval | `research/methodology/` | D |

## 10. Known limitations of the proposed search process
1. Only PubMed (through the connector), arXiv and Consensus are searchable now. Europe PMC, Crossref, Semantic Scholar, Google Scholar and repository APIs are blocked, so preprints, CS venues and non-MEDLINE journals are under-covered.
2. PubMed connector limits (20 operators, 5 wildcards) force compact queries and cost some recall.
3. Connector output must be transcribed into files (the connector cannot write files). Transcription errors are possible and are measured by spot-checks.
4. Single screener (assistant), with a sampled researcher audit rather than dual independent screening. The review is a *structured review with systematic elements* (D-005), not a systematic review.
5. Relevance-ranked sources (Consensus, arXiv, web) are not reproducible over time.
6. No forward citation searching. Backward searching is limited to open-access full texts and PDFs the researcher supplies.
7. Paywalled full texts depend on researcher access (Q-009).
8. The disorder and biomarker scope is provisional (Q-001, Q-002).
9. English only. Non-English work is excluded and counted.
10. Schedule: by 2026-10-23 (Day 10) no search has been run, which is behind the proposed schedule (D-001, Q-013). Compressing Stage B must not reduce verification.

## Change history
| Version | Date | Change | Approved |
|---|---|---|---|
| 1.0 | 2026-10-23 | Initial overview plan (BIO-001); no change to queries or criteria | Pending |
