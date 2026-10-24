# Project Governance

Source: researcher instructions issued with prompt `P001` (2026-10-14). This file restates
those instructions so they are versioned with the project. It must not be changed without a
DECISION_LOG entry approved by the researcher.

## 1. Research principles

1. Never fabricate publications, authors, DOIs, datasets, experimental results, statistical findings, or citations.
2. Never invent model-performance values.
3. Never manipulate labels, remove valid observations without justification, or alter results to favour the proposed method.
4. Never present synthetic data or simulated results as genuine biomedical observations.
5. Use genuine, documented datasets for the empirical investigation.
6. Synthetic data only for clearly labelled software tests or explicitly separated simulation studies.
7. Never claim novelty without examining the closest existing research.
8. Distinguish established evidence, preliminary hypotheses, methodological recommendations, and unresolved questions.
9. Never silently modify an approved research decision.
10. Never claim a task is complete unless its deliverables exist and have been checked.

### Evidence labels (used in all research documents)

| Label | Meaning |
|---|---|
| `[EVIDENCE]` | Supported by a verified source recorded in `paper_inventory` |
| `[HYPOTHESIS]` | Preliminary expectation, not yet tested |
| `[RECOMMENDATION]` | Methodological proposal by the assistant, pending approval |
| `[OPEN]` | Unresolved question; also listed in `research/reviews/unresolved_questions.md` |

## 2. Stages and gates

| Stage | Content | Exit criterion (gate) |
|---|---|---|
| A | Research setup, literature-search design | Search strategy approved |
| B | Literature collection, source verification | Inventory built; every entry verified against a bibliographic source |
| C | Critical comparison of existing methods | Comparison reviewed by researcher |
| D | Research gap and feasibility | Gap + main contribution approved |
| E | Framework design, experimental protocol | Protocol approved (frozen before modelling) |
| F | Dataset acquisition, quality assessment | Primary dataset + outcome definition approved |
| G | Baseline implementation | Baselines run under frozen protocol |
| H | Proposed-method implementation | Implementation tested |
| I | Comparative evaluation, explainability, calibration, uncertainty, ablation, robustness | All pre-registered analyses run and logged |
| J | Reproducibility audit, manuscript | Clean-environment re-run reproduces logged results |

No stage is skipped to meet the deadline. **No predictive model training and no performance
claims during Days 1–20.**

Synthetic-only software verification that satisfies Rule S (DECISION_LOG D-040) is not predictive model training or modelling for the purposes of this section.

### Decisions reserved for the researcher
- Primary dataset
- Main research contribution
- Outcome (label) definition
- Final evaluation protocol
- Any change to an already approved decision

## 3. Proposed schedule (status: PROPOSED — see DECISION_LOG D-001)

Day 1 = 2026-10-14; Day 45 = 2026-11-27. Researcher time ≈ 1 h/day.

| Days | Dates | Stages |
|---|---|---|
| 1–2 | 10-14 → 10-15 | A |
| 3–8 | 10-16 → 10-21 | B |
| 9–12 | 10-22 → 10-25 | C |
| 13–16 | 10-26 → 10-29 | D, start of F (feasibility only, no modelling) |
| 17–20 | 10-30 → 11-02 | E, F (data acquisition + quality assessment, protocol freeze) |
| 21–25 | 11-03 → 11-07 | G |
| 26–31 | 11-08 → 11-13 | H |
| 32–39 | 11-14 → 11-21 | I |
| 40–45 | 11-22 → 11-27 | J |

## 4. Change tracking

Before modifying work: inspect `git status`, identify and preserve user changes, review
relevant files, preserve approved decisions. After every task: record files created /
modified / deleted, validation commands with actual outcomes, errors, incomplete work and
open questions in `logs/CHANGELOG.md` and `logs/PROMPT_LOG.md`; update `logs/DECISION_LOG.md`
only when a decision is proposed, approved, rejected, or revised; record the commit hash when
a commit is created.

## 5. End-of-task report (every prompt)

1. Task ID and objective · 2. Work completed · 3. Files created · 4. Files modified ·
5. Findings with evidence · 6. Decisions requiring approval · 7. Validation and actual outcome ·
8. Errors/limitations · 9. Unresolved questions · 10. Recommended next prompt ·
11. Approximate researcher review time.
