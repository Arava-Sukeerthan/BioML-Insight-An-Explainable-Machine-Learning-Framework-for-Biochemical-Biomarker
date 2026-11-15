# Methods — literature review (manuscript draft section)

> **Draft, 2026-11-12. Facts only.** Every number below is copied from repository records (sources in square brackets, to be removed before submission). No screening has taken place, so this section contains no screening results, included studies, synthesis or citations. Bracketed placeholders are completed only from authorised, logged work. **No reference is cited:** no inventory record is yet `verified` (`research_plan.md` §6).

## 2.1 Design
We conducted a structured literature review with systematic elements to characterise machine-learning studies that classify metabolic disorders from biochemical biomarkers. It also examines how such studies explain predictions, assess probability calibration, estimate uncertainty and validate on independent data, and identifies the closest existing integrated frameworks. It is not a formally systematic review and makes no claim of completeness [D-005; `search_strategy.md` §1.3]. The search strategy, eligibility criteria and screening protocol were versioned in a public Git repository; no protocol was registered in an external registry.

## 2.2 Information sources and searches
- **PubMed:** 15 queries, executed on 2026-10-23 with an entry-date cap of 2026-10-23. They returned 3,413 hits (2,866 unique PMIDs); every query was retrieved completely [`collection_summary.md` §1].
- **arXiv:** 5 queries through the alphaXiv connector, returning 76 records (title and identifier only).
- **Publisher and web searches:** 5 queries and 1 repository query, returning 54 records (title and URL only).
- **Supplementary searches on 2026-10-28:** 8 further PubMed queries and one alphaXiv transcription [`search_queries.csv`].
- **Not searched:** Consensus (quota exhausted); Europe PMC, Crossref, Semantic Scholar and repository APIs (hosts unreachable from the computing environment); Google Scholar (manual only) [`access_report.md`; `environment_assessment.md`].
- **Raw output:** every search output was saved unchanged as a raw export file with a SHA-256 checksum (244 files) [`raw_exports/MANIFEST.csv`]. Connector output transcribed by the tool was spot-checked by re-fetching at least 10% of it [D-012].

## 2.3 Record management and verification
- **Deduplication:** 3,998 source records were deduplicated into 3,386 publication records: 471 merged duplicates, and 30 publication records in 15 pairs flagged for a manual duplicate decision [`records/build_report.json`].
- **Bibliographic verification:** this required full agreement of title, first author, year, venue and a persistent identifier with an independently established second source [D-064]. At the time of writing, 3,348 records were partially verified, 37 unverified and 1 needed review; none was verified [`verification_report.md`].
- **Retractions:** four records carried a retraction flag from publication-type metadata [`build_report.json`].

## 2.4 Screening scope
Title/abstract screening is restricted to the 1,470 records retrieved by at least one of these queries [D-044; `scope/D-044_scope_snapshot.md`]:
- the core classification queries for RQ1 (Q-PM-01 to Q-PM-03);
- the integrated-framework queries for RQ5 (Q-PM-11 and Q-PM-12);
- seven of the eight supplementary queries of 2026-10-28 (G-1 to G-7). G-8 is excluded.

The supplementary queries add targeted coverage of external validation (RQ4: G-1, G-4) and methodological limitations (RQ6: G-3, G-6, G-7). The dedicated strands for explainability (RQ2; Q-PM-04, Q-PM-05), calibration and uncertainty (RQ3; Q-PM-06 to Q-PM-08), external validation (Q-PM-09, Q-PM-10) and limitations (Q-PM-13, Q-PM-14) are outside the scope. Evidence for RQ2 and RQ3 therefore comes only from records retrieved by in-scope queries, and is incidental rather than representative. RQ4 and RQ6 are covered only partly.

## 2.5 Eligibility criteria and screening procedure
- **Freeze:** eligibility criteria (v1.1) and the screening protocol (v0.2) were frozen before any screening, as `criteria_v1.1+protocol_v0.2` [freeze entry D-110, effective 2026-11-11; SHA-256 8511be1b…06d8 and f6304198…c8fb].
- **Inclusion** requires, among other criteria:
  - a peer-reviewed article, full conference paper or preprint in English;
  - a supervised classification or risk-probability model;
  - biochemical-biomarker inputs (metabolomics or lipidomics, newborn-screening tandem mass spectrometry, or routine clinical chemistry);
  - a target within the predefined metabolic-disorder scope.
- **Reviews** are retained only as lead sources.
- **Uncertain records** at title/abstract are sent to full-text assessment, and a missing abstract never leads to exclusion.
- **Planned procedure** [pending: screening activation under D-108 (approval item A1); the blinding arrangement of the pilot (R1-min revision of D-102 with an independent custodian, approval item A2)]. Written in the past tense only after the step has taken place:
  1. automatic exclusion of PubMed publication types *Editorial*, *Comment*, *News* and *Published Erratum* (exclusion code E5), and *Retracted Publication* (E7);
  2. a stratified pilot of 60 records, screened independently and blinded by the assistant and the researcher. Pass will require Cohen's κ ≥ 0.60, no unresolved include/exclude conflict and fewer than three disagreements on any exclusion code [D-025; D-098];
  3. title/abstract screening of the remaining records in batches;
  4. a blinded researcher audit of 25 inclusions and 25 exclusions [D-008];
  5. full-text assessment in tier order, with records routed for the integrated-framework question assessed component by component (feature selection, classification, explainability, calibration, uncertainty) and verified by the researcher [D-031–D-038].
- **Tier-3 records:** these are classification studies addressing none of explainability, calibration or uncertainty, or external validation. They are included on title/abstract evidence, and only a random sample is read in full.

## 2.6 Limitations of the review methods (stated in advance)
- A single primary screener (the assistant) is used outside the 60-record pilot and the 50-record audit.
- Several bibliographic databases could not be searched, and citation-level verification depends on second sources that were partly unreachable.
- RQ2 and RQ3 are covered only incidentally, and RQ4 and RQ6 only partly (§2.4).
- Tier-3 records are included on abstract-level evidence.

[Results: flow-diagram counts, screening outcomes and agreement statistics are added only after authorised screening has taken place.]
