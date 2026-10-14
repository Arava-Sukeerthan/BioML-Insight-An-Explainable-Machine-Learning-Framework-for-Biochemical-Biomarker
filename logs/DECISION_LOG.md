# Decision Log

Statuses: `PROPOSED` → `APPROVED` / `REJECTED` / `REVISED`. Approved decisions are never edited
in place; a revision is a new entry referencing the old one.

| ID | Date | Decision | Status | Rationale | Approved by / date |
|---|---|---|---|---|---|
| D-001 | 2026-10-14 | 45-day schedule mapping stages A–J to days (GOVERNANCE.md §3), Day 1 = 2026-10-14 | PROPOSED | Respects the "no modelling in Days 1–20" rule and leaves 6 days for reproducibility audit and manuscript | — |
| D-002 | 2026-10-14 | Primary analysis language Python 3.13 with pinned PyPI packages; R not used unless needed | PROPOSED | Python is installed and PyPI is reachable; R and CRAN are not available | — |
| D-003 | 2026-10-14 | Literature sources: PubMed (primary, biomedical), Consensus (secondary/cross-index), arXiv via alphaXiv (ML methods); web search only to locate dataset documentation. References verified via PMID/DOI metadata from these tools | PROPOSED | Direct Crossref/OpenAlex/Europe PMC APIs are blocked from the container | — |
| D-004 | 2026-10-14 | Git usage: commit and push to `claude/happy-hawking-rxptfv` at the end of each prompt, with the hash recorded in the session log | PROPOSED | The container is ephemeral; uncommitted work is lost. Session instructions require pushing to this branch. Researcher may instead require explicit per-prompt commit approval | — |
