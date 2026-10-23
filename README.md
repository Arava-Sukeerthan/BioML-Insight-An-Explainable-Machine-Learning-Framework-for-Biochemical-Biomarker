# BioML-Insight

**Working research title:** *BioML-Insight: An Explainable and Uncertainty-Aware Machine
Learning Framework for Biochemical Biomarker-Based Metabolic Disorder Classification*

> **Status (2026-10-23, Day 10 of a planned 45-day project, started 2026-10-14):**
> research setup and literature-review preparation. **The research gap, the main contribution
> and the proposed methodology have not been finalised.** No literature search has been run, no
> publication has been collected, no dataset has been selected, and no model has been trained.
> This repository makes **no claim** of predictive performance, superiority over existing
> methods, or novelty.

## Research objective
To find out, from the published evidence and then from experiments on genuine, documented
datasets, whether and how explainability, probability calibration and uncertainty estimation
can be combined with biochemical-biomarker-based classification of metabolic disorders so that
predictions are interpretable and their reliability is reported honestly. Whether such a
combination is new, and whether it is useful, are open questions for the literature review
(Stages B–D). They are not assumptions.

## Provisional research question `[OPEN]`
> To what extent can a classification framework for metabolic disorders based on biochemical
> biomarkers combine (i) explanation of its predictions, (ii) calibrated probabilities and
> (iii) uncertainty estimates, while keeping discrimination comparable to standard baselines,
> and does that behaviour hold on independent data?

This wording is provisional. It depends on pending decisions D-013–D-017 (disorder, dataset,
independent validation, contribution, framework) in [`logs/DECISION_LOG.md`](logs/DECISION_LOG.md)
and may change after the literature review. The six literature-review questions (RQ1–RQ6) are
in [`research/literature/search_strategy.md`](research/literature/search_strategy.md) §1.2.

## Planned research stages
Stage gates are defined in [`GOVERNANCE.md`](GOVERNANCE.md) §2. The day mapping is *proposed*
(D-001) and has slipped; see `research/reviews/unresolved_questions.md` Q-013.

| Phase | Stages | Content | Status |
|---|---|---|---|
| Days 1–20: evidence and design | A | Research setup, governance, literature-search design | Drafted (P001, LIT-001, LIT-002, BIO-001); awaiting approval |
| | B | Literature collection and source verification | Not started |
| | C | Critical comparison of existing methods | Not started |
| | D | Research gap and dataset feasibility | Not started |
| | E | Framework design and experimental protocol (frozen before modelling) | Not started |
| Days 21–45: empirical work | F | Genuine dataset acquisition and quality assessment | Not started |
| | G | Baseline implementation | Not started |
| | H | Proposed-method development | Not started |
| | I | Experiments, statistical evaluation, calibration, uncertainty, ablation | Not started |
| | J | Reproducibility audit and manuscript preparation | Not started |

## Research integrity principles
Full rules: [`CLAUDE.md`](CLAUDE.md), [`GOVERNANCE.md`](GOVERNANCE.md) and
[`research/methodology/research_integrity.md`](research/methodology/research_integrity.md).
- No fabricated publications, citations, DOIs, datasets, results or statistics.
- Real, documented datasets for empirical work. Synthetic data only in clearly labelled software tests.
- No manipulation of results in favour of the proposed method. Negative and inconclusive findings are reported.
- No novelty claim before the closest prior work has been examined.
- Statements are labelled `[EVIDENCE]`, `[HYPOTHESIS]`, `[RECOMMENDATION]` or `[OPEN]`.
- Data leakage must be prevented. External validation and clinical validity must not be claimed unless they were actually shown.
- Researcher approval is required for the primary dataset, the main contribution, the outcome definition and the evaluation protocol. Assistant recommendations are not approvals.

## Repository organisation
```
README.md                        This file
CLAUDE.md                        Persistent assistant instructions
GOVERNANCE.md                    Research principles, stage gates, schedule (proposed)
research/
  setup/environment_assessment.md  Tools, network access, limitations
  literature/                      research_plan.md (overview), search strategy, queries,
                                   screening criteria, collection workflow, schemas/,
                                   raw_exports/ (manifest only in Git)
  methodology/                     research_integrity.md, design decisions; later: research
                                   questions, framework, experimental protocol
  reviews/                         Daily review log, unresolved questions
logs/
  CHANGELOG.md                     Change record per task
  PROMPT_LOG.md                    Prompt/task identifiers, deliverables and outcomes
  DECISION_LOG.md                  Pending / proposed / approved / rejected / revised decisions
  EXPERIMENT_LOG.md                Experiment runs (none before Stage G)
  session_logs/                    One log per working session
scripts/literature/              Query validation, PubMed E-utilities client, record pipeline
tests/literature/                Unit tests (synthetic fixtures only, labelled as such)
```
Directories for analysis code (`src/`), data (`data/`, not committed) and results are created
when the corresponding stage begins.

## Workflow
Each task has an ID (e.g. `BIO-001`). It is logged in `logs/CHANGELOG.md` and `logs/PROMPT_LOG.md`,
ends with a completion report, and is submitted as a pull request. The researcher reviews and
merges; pull requests are not merged automatically.
