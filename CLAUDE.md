# CLAUDE.md — BioML-Insight

Persistent instructions for every assistant session in this repository.

History: created in LIT-002 (2026-10-14) as a pointer to `GOVERNANCE.md` (decision D-011,
proposed). Expanded in **BIO-001 (2026-10-23)** with the rules the researcher listed in the
BIO-001 prompt (decision D-022, proposed). `GOVERNANCE.md` was **not** changed: under its own
rule, a change to it needs a researcher-approved DECISION_LOG entry. Where this file adds rules
that are not in `GOVERNANCE.md` (PR per task, no automatic merge), they are researcher instructions
taken from the BIO-001 prompt. Read both files before every task.

## 1. Research-integrity rules (non-negotiable)
1. Never fabricate scientific publications, authors, DOIs, citations, datasets, experimental results or statistics. Never invent performance values.
2. Never present synthetic observations as genuine biomedical data. Synthetic data are allowed only for clearly labelled software tests or explicitly separate simulation studies.
3. Use real, documented datasets for the actual empirical research (`research/methodology/research_integrity.md`).
4. Never manipulate experimental results, labels or observations so that the proposed method outperforms the baselines. Do not tune more on the proposed method than on the baselines.
5. Never claim novelty without first investigating the closest existing studies (review question RQ5 / theme F).
6. Distinguish verified evidence from hypotheses and recommendations. Label statements `[EVIDENCE]`, `[HYPOTHESIS]`, `[RECOMMENDATION]` or `[OPEN]` (definitions in `GOVERNANCE.md` §1).
7. A recommendation produced by Claude Code is **not** researcher approval.

## 2. Working rules
8. Preserve the researcher's existing work. Run `git status` first, never discard uncommitted changes, and do not overwrite or delete files without a documented reason. If an equivalent file already exists, update it instead of creating a duplicate.
9. Record important modifications in `logs/CHANGELOG.md`. Record only work that was actually done. If validation was not performed, say so.
10. Do not silently modify approved research decisions (`logs/DECISION_LOG.md`). A revision is a new entry that references the old one.
11. The following are reserved for the researcher: the primary disorder, primary dataset, outcome definition, main contribution, evaluation protocol, and any change to an approved decision.
12. Do not claim a task is complete without verifying its deliverables with real commands. Record the actual outcomes.
13. No model training and no performance claims before Day 21 (2026-11-03), and not before the experimental protocol is approved.

## 3. Every task
1. Pre-task: run `git status`, `git log`, read the relevant files, and identify user changes.
2. Work, then validate with real commands.
3. Update `logs/CHANGELOG.md`, `logs/PROMPT_LOG.md`, a session log in `logs/session_logs/`, and `research/reviews/daily_review_log.md`. Update `logs/DECISION_LOG.md` only for decisions. Put open questions in `research/reviews/unresolved_questions.md`.
4. **Task-completion report after every prompt.** Use the fields requested in the prompt; at minimum the 11 points in `GOVERNANCE.md` §5.
5. **Pull request for each completed task** when repository permissions allow. One branch per task (or the branch the session designates), PR into the default branch, PR number and URL recorded in CHANGELOG and PROMPT_LOG. If a PR cannot be created, do not claim it was. Report the branch, the commit and the remaining steps instead.
6. **Never merge pull requests automatically.** Never force-push. Never change branch-protection rules.

## 4. Practical notes
- Tests: `python3 -I -m unittest discover -s tests/literature -v`
- Query table check: `python3 -I scripts/literature/validate_search_queries.py research/literature/search_queries.csv`
- Literature plan (overview): `research/literature/research_plan.md`. Detailed strategy and queries: `search_strategy.md`, `search_queries.csv`. Workflow: `collection_workflow.md`.
- Integrity protocol for data and experiments: `research/methodology/research_integrity.md`
- The GitHub repository is **public**. Do not commit raw literature exports, abstracts or raw data (see `.gitignore`).
- Network: most bibliographic and data APIs are blocked from the container (re-checked 2026-10-23); see `research/setup/environment_assessment.md`.
