# CLAUDE.md — BioML-Insight

Created in LIT-002 (2026-10-14) because the researcher's prompts refer to "CLAUDE.md". The
authoritative project rules are in **`GOVERNANCE.md`** (restated from prompt P001). Read it
before every task. Status: proposed (decision D-011).

## Non-negotiable rules (summary of GOVERNANCE.md §1)
- Never fabricate publications, authors, DOIs, datasets, results, statistics or citations; never invent performance values.
- Never manipulate labels or remove valid observations without justification; never tune results to favour the proposed method.
- Synthetic data only for clearly labelled software tests or separate simulation studies.
- No novelty claim without examining the closest prior work (RQ5).
- Label statements `[EVIDENCE]` / `[HYPOTHESIS]` / `[RECOMMENDATION]` / `[OPEN]`.
- Never silently change an approved decision (`logs/DECISION_LOG.md`).
- Do not finalise primary dataset, main contribution, outcome definition or evaluation protocol without researcher approval.
- No model training or performance claims before Day 21 and before the protocol is approved.

## Every task
1. `git status` first; preserve user changes; read the relevant files.
2. Work; validate with real commands; record actual outcomes.
3. Update `logs/CHANGELOG.md`, `logs/PROMPT_LOG.md`, a session log in `logs/session_logs/`; `logs/DECISION_LOG.md` only for decisions; `research/reviews/unresolved_questions.md` for open questions.
4. End with the 11-point report (GOVERNANCE.md §5).

## Practical notes
- Tests: `python3 -I -m unittest discover -s tests/literature -v`
- Query table check: `python3 -I scripts/literature/validate_search_queries.py research/literature/search_queries.csv`
- Literature workflow: `research/literature/collection_workflow.md`
- The GitHub repository is public: do not commit raw literature exports or abstracts (see `.gitignore`).
- Network: most bibliographic APIs are blocked; see `research/setup/environment_assessment.md`.
