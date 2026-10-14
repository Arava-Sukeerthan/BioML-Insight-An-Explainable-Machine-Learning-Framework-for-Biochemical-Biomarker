# BioML-Insight

**An Explainable and Uncertainty-Aware Machine Learning Framework for Biochemical Biomarker-Based Metabolic Disorder Classification**

Status: **Stage A — research setup** (Day 1 of a planned 45-day project, started 2026-10-14).
No literature has been collected, no dataset has been selected, and no model has been trained.

## Governance

The project follows the rules in [`GOVERNANCE.md`](GOVERNANCE.md): no fabricated sources,
data, or results; real documented datasets only; researcher approval for primary dataset,
main contribution, outcome definition, and final evaluation protocol.

## Repository layout

```
GOVERNANCE.md                    Research principles, stage gates, schedule (proposed)
research/
  setup/environment_assessment.md  Tools, network access, and limitations
  literature/                      Search strategy, paper inventory, review, gap matrix
  methodology/                     Research questions, hypotheses, framework, protocol, design decisions
  reviews/                         Daily review log and unresolved questions
logs/
  CHANGELOG.md                     File-level change record per task
  PROMPT_LOG.md                    Prompt identifiers and outcomes
  DECISION_LOG.md                  Proposed / approved / rejected / revised decisions
  EXPERIMENT_LOG.md                Experiment runs (none before Stage G)
  session_logs/                    One log per working session
```

Directories for code (`src/`), tests (`tests/`), and data (`data/`) will be created when
the corresponding stage begins. Raw data will not be committed to Git.
