# Literature Search Strategy

| Field | Value |
|---|---|
| Task | LIT-001 (Stage A) |
| Version | 1.0 — **DRAFT, pending researcher approval** |
| Prepared | 2026-10-14 |
| Status of searches | **Not run.** Only capability probes and count-only pilots were executed (listed in `search_queries.csv`, `row_type` = `capability_probe` / `pilot_count`). No records have been collected. |
| Companion files | `search_queries.csv` (exact queries, dates, counts), `screening_criteria.md` (eligibility), `schemas/` (record formats; see `collection_workflow.md`), `../reviews/unresolved_questions.md` |

---

## 1. Purpose and review type

### 1.1 Purpose
To identify, verify, and critically compare the literature that bears on the six review
questions below. The output is the evidence base for Stages C (critical comparison) and D
(research gap and feasibility). The search is **not** intended to justify a predetermined
framework.

### 1.2 Review questions (RQ)
| RQ | Question | Main evidence sought |
|---|---|---|
| RQ1 | Which ML methods are used for biochemical-biomarker-based metabolic-disorder classification? | Original application studies |
| RQ2 | Which explainability techniques are used to interpret biomedical and metabolomics classifiers, and how are they evaluated? | Application + methodological studies |
| RQ3 | How are probability calibration and uncertainty estimation handled in biomedical ML? | Methodological papers + domain applications |
| RQ4 | How are external validation and cross-cohort generalization (dataset shift) addressed? | External-validation studies + methodological papers |
| RQ5 | Which existing frameworks combine biomarker selection, classification, explainability, and uncertainty estimation? | Closest prior art (critical for any novelty claim) |
| RQ6 | Which methodological limitations are reported, and what research opportunities follow? | Meta-research, reviews, appraisal of included studies |

### 1.3 Structured literature review vs. formally systematic review
| Feature | Formally systematic review (e.g., PRISMA 2020 compliant) | This project (as currently resourced) |
|---|---|---|
| Registered a-priori protocol (e.g., PROSPERO / OSF) | Required/expected | Not registered; this file is versioned in Git as the protocol |
| Databases | Several major bibliographic databases (typically incl. Embase, Scopus/Web of Science) | PubMed (complete, reproducible); Consensus, arXiv, and web search as supplementary; Europe PMC, Crossref, Semantic Scholar planned but **currently blocked** |
| Screening | Two independent reviewers, disagreement resolution | One screener (assistant) + researcher audit of a random sample (§6.4) |
| Risk-of-bias appraisal | Formal validated tool | Structured appraisal informed by PROBAST/TRIPOD-type domains (§8.2); not a formal PROBAST assessment unless approved |
| Completeness claim | Supported | **Not claimed** |

**Classification:** this is a **structured literature review with systematic elements**:
documented, reproducible, dated queries; explicit eligibility criteria; deduplication and a
PRISMA-style record-flow diagram. The manuscript must not describe it as a "systematic
review" or claim exhaustive coverage. Upgrading would require at least: protocol
registration before screening, a second independent screener, and access to further
databases (see Q-006).

---

## 2. Search-capability assessment (verified 2026-10-14)

Every capability below was **tested**, not assumed; the test rows are `PROBE-01` to
`PROBE-12` in `search_queries.csv`. Test results were discarded and not added to the inventory.

| Resource | Route tested | Result | Role in this strategy |
|---|---|---|---|
| **PubMed** | PubMed connector (search, metadata, ID conversion, related articles, PMC full text) | **Works.** Returns total hit count, PMIDs (paginated), PubMed's query translation, full metadata incl. DOI/PMCID/publication types | **Primary, reproducible source** |
| PubMed connector limits | Pilot queries | Max **20 boolean operators** and **5 wildcards** per query (`PILOT-01`, `PILOT-02` rejected) | Queries were designed within these limits (§4.3) |
| **Europe PMC** | REST API via container and via WebFetch | **Blocked** (proxy 403 / DNS failure) | Queries prepared; run only if access is enabled or researcher exports manually |
| **Crossref** | REST API | **Blocked** | Queries prepared; would mainly serve DOI verification |
| **Semantic Scholar** | Graph API | **Blocked** | Queries prepared; Consensus used as a partial proxy |
| **Google Scholar** | Direct and via web search (`site:`) | **Not accessible** | Optional manual search by researcher only |
| **Consensus** | Consensus connector | **Works**, free tier: 10 results/search, no paging, no DOIs | Supplementary semantic search (recall check) |
| **arXiv** | alphaXiv connector | **Works**; ranked, non-boolean, 2 searches per message | ML-methods literature (RQ2–RQ5) |
| **Publisher websites** | WebSearch with `allowed_domains` | **Search works**; pages cannot be opened (WebFetch fails) | Supplementary discovery; every hit verified elsewhere |
| **Metabolomics Workbench / MetaboLights** | REST APIs | **Blocked** | PubMed route (`Q-PM-15`) + web search fallback; APIs if enabled |
| PMC full text | PubMed connector `get_full_text_article` | Available for open-access PMC articles (exercised only for metadata so far) | Full-text screening and extraction |

Consequences:
1. The **reproducible core** of the review is PubMed. Everything else is supplementary and
   reported separately in the flow diagram.
2. Preprints (medRxiv/bioRxiv) and non-MEDLINE journals are under-covered until Europe PMC is
   reachable; CS venues (IEEE, ACM, NeurIPS, ICML) are covered only through arXiv, Consensus and
   web search.
3. **Forward citation searching** ("cited by") is not available through any working tool. Backward
   citation searching is possible for open-access papers through PMC full text.

---

## 3. Concept framework

Six concept blocks are combined per RQ. Full, unrestricted versions are used for Europe PMC;
compact versions for the PubMed connector (§4.3).

| Block | Concept | Key terms (illustrative; exact strings in `search_queries.csv`) |
|---|---|---|
| D | Metabolic disorders | MeSH *Metabolic Diseases* (exploded); metabolic syndrome; diabetes; prediabetes; insulin resistance; fatty liver; NAFLD; MASLD; dyslipidaemia; hyperuricaemia/gout; inborn errors of metabolism; newborn screening |
| M | Metabolomics | MeSH *Metabolomics*; metabolom\*; metabonom\*; lipidom\*; acylcarnitine; tandem mass spectrometry (newborn screening) |
| B | Routine biochemical biomarkers | laboratory test\*; biochemical marker\*/parameter\*; clinical chemistry; blood test\*; routine laboratory; MeSH *Clinical Laboratory Techniques*; MeSH *Biomarkers* (only in narrower combinations) |
| L | Machine learning | MeSH *Machine Learning*; machine learning; deep learning; AI; random forest; gradient boosting; XGBoost/LightGBM/CatBoost; SVM; neural networks; PLS-DA; elastic net |
| X | Explainability | explainab\*; interpretab\*; SHAP; Shapley; local interpretable model-agnostic explanations; feature/permutation importance; partial dependence; counterfactual |
| C | Calibration | Brier score; calibration slope/plot/-in-the-large; expected calibration error; Platt scaling; isotonic regression; temperature scaling; reliability diagram |
| U | Uncertainty | conformal prediction/predictor; uncertainty quantification/estimation; predictive uncertainty; Venn-Abers; selective prediction; reject option; Monte Carlo dropout; deep ensembles; Bayesian neural networks |
| E | External validation / shift | external validation; independent/validation cohort; cross-/multi-cohort; transportability; dataset/distribution/covariate/domain shift; domain adaptation; batch/site effects |
| F | Biomarker selection | feature/variable/biomarker selection; recursive feature elimination; stability selection |
| Q | Methodological quality | risk of bias; PROBAST; TRIPOD; data leakage; overfitting; methodological/reporting quality; reproducibility |

RQ-to-block mapping (PubMed IDs): RQ1 = D∧M∧L (`Q-PM-01`), D∧B∧L (`Q-PM-02`),
IEM∧L∧MS/MS (`Q-PM-03`); RQ2 = M∧L∧X (`Q-PM-04`), D∧B∧L∧X (`Q-PM-05`); RQ3 = L∧C∧target
(`Q-PM-06`), L∧U∧target (`Q-PM-07`), methodological (`Q-PM-08`); RQ4 = D∧(M∨B)∧L∧E
(`Q-PM-09`), L∧shift∧target (`Q-PM-10`); RQ5 = (M∨B)∧L∧F∧X∧(C∨U) (`Q-PM-11`),
framework/pipeline titles (`Q-PM-12`); RQ6 = target∧L∧Q (`Q-PM-13`), reviews (`Q-PM-14`);
repositories (`Q-PM-15`).

### 3.1 Known term problems found during design (evidence: pilot rows)
| Problem | Evidence | Handling |
|---|---|---|
| PubMed automatic term mapping expands *calibration* to *calibrant/calibrator* (analytical chemistry) | `PROBE-01` query translation | Calibration terms only as quoted phrases with `[tiab]` |
| "calibration curve\*" retrieves many analytical-calibration papers | 277 → 606 hits when added (`PILOT-F06` vs `PILOT-F06b`) | Excluded from `Q-PM-06`; recall loss mitigated by `Q-PM-08`, Consensus, citation chasing. **Recall risk acknowledged.** |
| Bare "LIME" matches lime (fruit/calcium) | Known term ambiguity | Only the full phrase "local interpretable model-agnostic" is used |
| "SHAP" also abbreviates a serum protein (serum-derived hyaluronan-associated protein) | Known term ambiguity | Kept (combined with ML block); removed at screening |
| Broad *Biomarkers* MeSH makes RQ1 unscreenable | 2,333 hits (`PILOT-08`) | RQ1 split into metabolomics (430) and routine-biochemistry (740) strands |
| MeSH indexing lags for recent records | General PubMed property | Every MeSH term is paired with free-text `[tiab]` terms |

---

## 4. Sources and queries

### 4.1 Date windows and search snapshot
* **Application literature (RQ1, RQ2, RQ4-applications, RQ6):** records entered in PubMed from
  **2015-01-01** to the run date. Rationale `[HYPOTHESIS]`: most metabolic-disorder ML studies
  that use current toolkits and post-hoc explainers (SHAP, seed S05, recalled as 2017 —
  unverified) are expected to fall in this window. The rationale will be checked in LIT-002 by
  counting pre-2015 hits of Q-PM-01/02 (records before 2015 will be reported, not screened).
  *Proposed; decision D-007.*
* **Methodological literature (RQ3, RQ4-shift, RQ5):** **no lower date limit**, so that foundational
  calibration, conformal-prediction and dataset-shift work is retained.
* **Snapshot:** every PubMed query ends with an Entrez-date cap `…:{RUN_DATE}[edat]`, replaced
  by the actual run date at execution. Re-running the stored query later returns the same
  set apart from deletions or corrections, which makes the search reproducible. The connector accepts and
  translates this clause correctly (`PILOT-E01`, `PILOT-E02`).
* **Update search:** all PubMed queries are re-run before manuscript submission (Stage J) with a
  new cap; only new records are screened; the delta is reported.

### 4.2 Language
English-language records only, applied **at screening** (not as a query filter) so that the
number of non-English exclusions is reported.

### 4.3 PubMed (primary, executable)
* 15 planned queries `Q-PM-01` … `Q-PM-15`, each within connector limits
  (verified by `scripts/literature/validate_search_queries.py`).
* Each planned query has a pilot row with the identical string except the date clause.
* **Pilot hit counts (2026-10-14, count-only, not deduplicated):**

| Query | RQ | Pilot hits |
|---|---|---|
| Q-PM-01 metabolomics strand | RQ1 | 430 |
| Q-PM-02 routine-biochemistry strand | RQ1 | 740 |
| Q-PM-03 inborn errors / newborn screening | RQ1 | 52 |
| Q-PM-04 metabolomics × XAI | RQ2 | 382 |
| Q-PM-05 metabolic biomarkers × XAI | RQ2 | 301 |
| Q-PM-06 calibration | RQ3 | 277 |
| Q-PM-07 uncertainty / conformal | RQ3 | 58 |
| Q-PM-08 calibration/UQ methodology | RQ3 | 150 |
| Q-PM-09 external validation | RQ4 | 260 |
| Q-PM-10 dataset shift | RQ4 | 311 |
| Q-PM-11 integrated frameworks | RQ5 | 100 |
| Q-PM-12 framework/pipeline titles | RQ5 | 19 |
| Q-PM-13 methodological quality | RQ6 | 168 |
| Q-PM-14 systematic/scoping reviews | RQ6 | 99 |
| Q-PM-15 repository-linked publications | RQ1/RQ4 | 18 |
| **Sum (with overlap)** | | **3,365** |

The number of unique records will be known only after deduplication. Strong overlap is
expected between Q-PM-01/04/05/09/11. Screening workload is discussed in §6.5 and decision D-009.

* **Execution:** `search_articles` with pagination (`retstart`), storing all PMIDs; then
  `get_article_metadata` in batches for title, abstract, authors, journal, year, DOI, PMCID and
  publication types. Raw tool output is saved unchanged (§5.1).
* **Optional cross-check by researcher (~5 min):** run one or two stored queries on
  pubmed.ncbi.nlm.nih.gov and confirm the hit counts match.

### 4.4 Europe PMC (prepared; blocked)
`Q-EP-01` … `Q-EP-06` use the full concept blocks (no operator limit), `TITLE_ABS:` and `MESH:`
fields, `FIRST_PDATE` ranges, and sources MED+PMC+PPR (adds preprints). `Q-EP-06` exploits
Europe PMC full-text indexing to find papers that cite Metabolomics Workbench / MetaboLights
datasets in data-availability statements. Runs only if `www.ebi.ac.uk` is enabled or the
researcher exports results manually (Q-003).

### 4.5 Crossref (prepared; blocked)
`Q-CR-01` … `Q-CR-03` are keyword (`query.bibliographic`) queries because Crossref has no boolean
search; top 200 by relevance. Crossref's main planned role is **metadata/DOI verification** for
records not in PubMed.

### 4.6 Semantic Scholar (prepared; blocked) and Consensus (executable)
`Q-S2-01` … `Q-S2-05` use the bulk-search boolean syntax. Until access is enabled, `Q-CN-01` …
`Q-CN-10` (Consensus, which indexes Semantic Scholar/OpenAlex/PubMed) serve as a **partial,
non-reproducible proxy**: 10 results per query, relevance-ranked. These records are used to
check recall (does PubMed miss relevant work?) and are reported as "other sources".

### 4.7 Google Scholar (not accessible; optional manual)
`Q-GS-01` … `Q-GS-04` are prepared for optional manual use by the researcher (first 100 results
per query). Automated access is neither possible here nor permitted by the service. If used, the
researcher saves titles/links; the assistant verifies each record before inclusion.

### 4.8 Publisher websites (executable, supplementary)
`Q-WS-01` … `Q-WS-05`: WebSearch restricted to publisher/venue domains (IEEE Xplore, ACM DL,
SpringerLink/BMC, ScienceDirect, Nature, OUP, Wiley, MDPI, Frontiers, PLOS, ACS, PMLR). Purpose:
reach CS conference papers and journals poorly indexed in PubMed. Non-reproducible;
every hit must be verified (§7) before entering the inventory.

### 4.9 Specialist metabolomics repositories
* `Q-PM-15` (executable): PubMed records mentioning Metabolomics Workbench or MetaboLights with
  classification/ML terms.
* `Q-RP-01`, `Q-RP-02` (blocked): repository API study searches by disorder term, to identify
  associated publications.
* `Q-RP-03` (executable fallback): domain-restricted web search.
* Scope note: assessing repository **datasets** for this project's own experiments belongs to
  Stage F. Here, repositories are used only to find their associated publications.

### 4.10 arXiv (executable)
`Q-AX-01` … `Q-AX-05` via alphaXiv for ML methodology (conformal prediction for tabular data,
classifier calibration, dataset shift, SHAP reliability, uncertainty-aware explainable
frameworks). Preprints are flagged; published versions are sought and preferred.

### 4.11 Foundational / known-item seeds (UNVERIFIED)
The following items are listed **from the assistant's background knowledge** as candidate
foundational references. **None is verified.** Each will be looked up by title/author in PubMed,
Consensus or arXiv. An item that cannot be located and verified is dropped and is never cited
from this list.

| Seed | Topic | As recalled (to verify) |
|---|---|---|
| S01 | Reporting guideline for AI prediction models | TRIPOD+AI statement — Collins et al., BMJ, 2024 |
| S02 | Risk-of-bias tool for prediction models | PROBAST — Wolff et al., Ann Intern Med, 2019; PROBAST+AI update (Moons et al., ~2025) |
| S03 | Calibration in clinical prediction | "Calibration: the Achilles heel of predictive analytics" — Van Calster et al., BMC Med, 2019 |
| S04 | Calibration hierarchy | Van Calster et al., J Clin Epidemiol, 2016 |
| S05 | SHAP | "A unified approach to interpreting model predictions" — Lundberg & Lee, NeurIPS, 2017 |
| S06 | LIME | "Why should I trust you?" — Ribeiro et al., KDD, 2016 |
| S07 | Calibration of modern neural networks | Guo et al., ICML, 2017 |
| S08 | Probability calibration of classifiers | "Predicting good probabilities with supervised learning" — Niculescu-Mizil & Caruana, ICML, 2005 |
| S09 | Conformal prediction foundations | *Algorithmic Learning in a Random World* — Vovk, Gammerman & Shafer, book, 2005 |
| S10 | Conformal prediction tutorial | Angelopoulos & Bates, arXiv, 2021 |
| S11 | Dataset shift in clinical AI | "The clinician and dataset shift in artificial intelligence" — Finlayson et al., NEJM, 2021 |
| S12 | Dataset-shift taxonomy | Moreno-Torres et al., Pattern Recognition, 2012 |
| S13 | Sample size for prediction models | Riley et al., BMJ, 2020 |
| S14 | False discoveries in metabolomics | Broadhurst & Kell, Metabolomics, 2006 |
| S15 | Metabolomics reporting standards (MSI) | Sumner et al., Metabolomics, 2007 |
| S16 | ML comparison across clinical metabolomics datasets | Mendez et al., Metabolomics, 2019 (also surfaced in `PROBE-08`) |
| S17 | Leakage and reproducibility in ML science | Kapoor & Narayanan, Patterns, 2023 |
| S18 | Interpretable models vs. post-hoc explanation | Rudin, Nat Mach Intell, 2019 |
| S19 | ML vs logistic regression for clinical prediction | Christodoulou et al., J Clin Epidemiol, 2019 |
| S20 | Prediction-model development/validation steps | Steyerberg & Vergouwe, Eur Heart J, 2014 |
| S21 | Reporting of reviews and searches | PRISMA 2020 (Page et al., BMJ, 2021); PRISMA-S (Rethlefsen et al., 2021) |

### 4.12 Citation chasing
* **Backward:** reference lists of (a) all included RQ5 closest-prior-art papers, (b) included
  reviews (`Q-PM-14`, lead sources), (c) the 10 most relevant included RQ1–RQ4 papers. Retrieved
  through PMC full text for open-access papers. For paywalled papers, only if the researcher
  provides the PDF.
* **Similar-article expansion:** PubMed `find_related_articles` (top 20) for RQ5 papers only.
* **Forward ("cited by"):** not available with the current tools. This limitation will be reported.
* Records found by citation chasing get `source_db = citation_chasing`, the seed paper ID, and go
  through the same screening and verification.

---

## 5. Record collection

> Implementation (LIT-002): `collection_workflow.md` describes the actual scripts, file
> layout, provenance rules and what has been tested. Where it differs in detail from §5, the
> workflow document describes the implemented behaviour.

### 5.1 Raw exports (immutable)
```
research/literature/raw_exports/<query_id>_<YYYY-MM-DD>.json   # unmodified tool output
research/literature/raw_exports/MANIFEST.csv                    # query_id, run_date, file, sha256, n_records
```
* Raw files are never edited. All processing reads them and writes new files.
* After each run, the query's row in `search_queries.csv` is copied as an `executed` row with
  `run_date`, `hits_total`, the exact executed string (date substituted), and `export_file`.

### 5.2 Normalisation
Scripted: strip HTML; normalise DOIs (lower-case, remove `https://doi.org/`); arXiv IDs without
version suffix; titles normalised for matching (lower-case, Unicode NFKD, punctuation removed,
whitespace collapsed). Original values are kept alongside the normalised ones.

### 5.3 Deduplication (scripted, then manual check)
Order of matching:
1. Same PMID → duplicate.
2. Same normalised DOI → duplicate.
3. Same arXiv ID / PMCID → duplicate.
4. Same normalised title and |year difference| ≤ 1 → duplicate.
5. Title similarity ≥ 0.90 (difflib ratio) with the same first-author surname → **flagged** for manual decision (not merged automatically).

Rules: the record from the most authoritative source is kept (PubMed > Europe PMC > Crossref >
arXiv > Consensus > web). Source and query provenance of every merged record are kept as a
list (`query_ids`). A preprint and its published version are linked, and the published version
is primary. Duplicate counts by rule are reported. The dedup script and its log are committed.

### 5.4 Retractions and corrections
PubMed publication types are checked for *Retracted Publication*, *Retraction of Publication*,
*Expression of Concern* and *Published Erratum*. Retracted papers are excluded (code E7).
Expressions of concern are flagged in `notes`.

---

## 6. Screening

Eligibility criteria and decision rules are defined in `screening_criteria.md`.

### 6.1 Stage 0 — automatic publication-type exclusion
Only on PubMed publication types: *Editorial*, *Comment*, *News*, *Published Erratum*, and
*Retracted Publication*. *Letters* are not excluded automatically. Counts are reported.

### 6.2 Stage 1 — title/abstract screening
The assistant screens all records against the criteria. Possible decisions are `include`,
`exclude` (with one primary reason code) and `uncertain`, which goes to full text. Decisions are
stored in `research/literature/screening/title_abstract_decisions.csv` (record ID, decision,
reason code, RQ tags, one-line justification, screener, date).

> **Implementation note (LIT-004-WORKFLOW-FIXES, 2026-10-23; proposed, D-027, not approved).** The pipeline reads a single file, `screening/decisions.csv`, with the stage as a column (`title_abstract` / `full_text`) instead of two files. `record_id` above is the `paper_id`. Required columns: `paper_id, stage, decision, reason_code, screener, date, justification`; optional: `rq_tags, tier, scope_flags, record_type, dim_explainability, dim_uncertainty, dim_calibration, dim_independent_validation, criteria_version, needs_human`. Columns, types and allowed values: `schemas/screening_decision.schema.json`. No documented field was dropped. The text above is kept unchanged until the researcher decides on D-027.

### 6.3 Stage 2 — full-text screening
Full text comes from PMC (open access) through the connector, or from a PDF the researcher
provides. If full text is unavailable, the record may be retained as **abstract-only** if the
abstract supports the required extraction fields. It is flagged and never used for detailed
methodological claims.

### 6.4 Researcher audit (quality control)
* Random sample, seed recorded: **25 included + 25 excluded** title/abstract decisions, plus every
  `uncertain` resolved at full text that the researcher wishes to see.
* The researcher records independent decisions blind to the assistant's decision. The audit sheet
  shows the record without the decision column.
* Agreement is reported as percentage agreement and Cohen's κ.
* If κ < 0.60, or any audited exclusion is judged includable, the criteria are clarified
  (logged in DECISION_LOG) and all exclusions with the affected reason code are re-screened.
* Estimated researcher time: about 60–75 minutes, split across two days.

### 6.5 Workload and prioritisation
The pilot sum is 3,365 records before deduplication. The assistant can screen this volume. The
bottleneck is full-text review. Full texts are therefore prioritised in tiers, and the tiering
is reported:
* **Tier 1:** metabolic/metabolomics biomarker ML studies addressing ≥ 2 of {explainability,
  calibration/uncertainty, external validation}, plus all RQ5 candidates and reporting
  guidelines.
* **Tier 2:** methodological papers for RQ2–RQ4, and studies addressing one of the three aspects.
* **Tier 3:** remaining RQ1 application studies. These are coded from abstracts (method, disorder,
  biomarker type, validation design) to describe the landscape. Full text is read for a
  random sample only.

How strand Q-PM-02 (740 hits) is handled is decision D-009.

---

## 7. Verification of sources

A record may be cited in project documents only when `verification_status = verified`.

| Level | Requirement |
|---|---|
| `verified` | Title, first author, year, venue and ≥ 1 persistent identifier (PMID, DOI, arXiv ID) retrieved from an authoritative index (PubMed metadata, or arXiv via alphaXiv), and consistent with a second source (e.g., PubMed DOI ↔ Consensus/arXiv record, or PMCID full text) |
| `partially_verified` | Found in one authoritative index only |
| `unverified` | Known only from web search, memory (§4.11 seeds), or a secondary citation |
| `failed` | Cannot be located, or metadata conflict unresolved → excluded from use |

Additional rules:
* **Reviews are lead sources.** A finding reported in a review is attributed to the original
  study only after that study itself has been retrieved and verified.
* **Numbers are copied, not retyped.** Reported metrics, sample sizes and dataset descriptions are
  copied verbatim with their location (section/table/figure). Values taken from an abstract only
  are flagged `abstract_only`.
* Preprints are labelled as such wherever they are cited.
* The verification script and log will be committed (planned for LIT-002).

---

## 8. Data extraction and analysis

### 8.1 Extraction
Fields follow `schemas/paper_inventory.schema.json`: disorder, biomarker type, dataset, sample size,
models, explainability method, calibration/uncertainty method, validation design, reported
metrics (verbatim), limitations, and RQ tags. Extraction is done by the assistant, and the
researcher spot-checks 5 records.

### 8.2 Methodological appraisal (structured, not formal PROBAST)
For each Tier-1/Tier-2 empirical study the following items are coded yes / no / unclear:
* validation design (apparent / CV / nested CV / temporal / external) and leakage safeguards
  (preprocessing and feature selection inside folds);
* sample size and events per class;
* handling of class imbalance and missing data;
* calibration reported, and how;
* uncertainty reported, and how;
* explanation stability or faithfulness assessed;
* external cohort characteristics;
* code and data availability;
* comparison with a simple baseline (e.g., logistic regression).

The items are informed by PROBAST and TRIPOD+AI domains, once those documents are verified
(seeds S01, S02).

### 8.3 Synthesis
* Descriptive counts and evidence tables by RQ: methods, XAI techniques, calibration/UQ
  techniques, validation designs, datasets.
* Narrative critical comparison (Stage C). **No meta-analysis or pooling of performance metrics.**
  Heterogeneous datasets and metrics make pooled estimates misleading, and vote-counting of
  "best algorithm" will not be reported as evidence of superiority.
* Gap matrix (Stage D): RQ × attribute, where every cell links to inventory IDs, and statements are
  labelled `[EVIDENCE]` / `[HYPOTHESIS]` / `[OPEN]`.
* RQ5 closest-prior-art table: must be complete before any novelty claim is made.

### 8.4 Reporting
A PRISMA-2020-style flow diagram (records identified per source, duplicates removed,
screened, excluded with reasons, full-text assessed, included), plus a PRISMA-S-style search
appendix generated from `search_queries.csv`. These are used as reporting templates, without
claiming PRISMA compliance for a systematic review.

---

## 9. Planned execution (subject to approval)

| Task | Content | Proposed day |
|---|---|---|
| LIT-002 | Collection/verification workflow implemented and tested (done 2026-10-14; see `collection_workflow.md`) | Day 1 |
| next | Run Q-PM-01…15 (snapshot), export raw, dedupe; run Consensus, arXiv and publisher queries; verify seeds | Day 3 (2026-10-16) |
| next+1 | Title/abstract screening + audit sample | Days 4–5 |
| next+2 | Full-text screening, extraction, appraisal (Tier 1→2), citation chasing | Days 6–8 |
| (Stage C) | Critical comparison | Days 9–12 |

## 10. Known limitations of this strategy
1. Europe PMC, Crossref, Semantic Scholar, Google Scholar and repository APIs are inaccessible
   at present. Coverage of preprints, CS venues and non-MEDLINE journals is therefore reduced.
2. The PubMed connector's operator and wildcard limits force compact blocks. Some synonyms are
   omitted (e.g., hyperuricaemia, obesity in the PubMed blocks), which costs recall. The
   omissions are explicit in the query strings.
3. Single screener plus a sampled audit, rather than dual independent screening.
4. Consensus, web and arXiv searches are relevance-ranked and not reproducible over time.
5. No forward citation searching.
6. Paywalled full texts depend on researcher access.
7. The disorder and biomarker scope is provisional until Q-001 and Q-002 are answered.

## 11. Change history
| Version | Date | Change | Approved |
|---|---|---|---|
| 1.0 | 2026-10-14 | Initial draft (LIT-001) | Pending |
| 1.0.1 | 2026-10-14 | LIT-002: schema path updated (`schemas/`); pointer to `collection_workflow.md` added; §9 task labels updated (LIT-002 became the workflow task). No change to queries or criteria | Pending |
| 1.0.1 (note) | 2026-10-23 | LIT-004-WORKFLOW-FIXES: implementation note under §6.2 (screening file name and columns as implemented; D-027 proposed). Text, queries and criteria unchanged; no version bump | Pending |
