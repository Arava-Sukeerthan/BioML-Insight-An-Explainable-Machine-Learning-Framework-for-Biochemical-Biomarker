# Session log — 2026-10-23 — LIT-004-WORKFLOW-FIXES

**Objective**: resolve reproducibility blockers B-1, B-3, B-4 before screening. **No screening.**

| Step | Outcome |
|---|---|
| Pre-task `git status` / `git log` | Clean; branch `claude/sweet-brahmagupta-urw7l1` at `8056054` (PR #2) |
| Investigation B-1 | 9 publications (P2980–P2988), all web-search records with title + URL only, had no registry key (`record_keys()` needs an identifier or title + year), so their IDs depended on build order. 2,970 others stable. `screening_protocol.md` cites P2980–P2982, P2987, P2988 |
| Key choice | `source_record:<source_record_id>` (unique per raw-file row, so collision-free). URL key considered: a URL shared by two unmerged records would let one of them change ID; kept as an alternative in D-027 |
| Migration | Pre-fix outputs copied to the scratchpad; `migrate-fallback-keys` added 9 registry rows mapping to the existing IDs (`records/id_migration_LIT-004.csv`) |
| Rebuild check | `build` + `make_literature_reports.py` twice: index and registry byte-identical; ID → source-record mapping identical to the pre-fix build; 2,979 publications; 0 without registry key; all 2,979 `not_screened` |
| Inventory check | Compared with `HEAD`: no existing value changed; 9 new columns, empty |
| Format (B-3) | Documents compared: `screening_criteria.md` §6 and `search_strategy.md` §6.2 (two files, `record_id`, rq_tags/tier/scope_flags), `collection_workflow.md` + code (`screening/decisions.csv`), protocol §2 (descriptors). Implemented: the code's file plus every documented column (optional). Notes added, document text unchanged |
| Status (B-4) | Inventory enum aligned with the publication record; report script maps the actual decision |
| Defect fixed during work | The new orphan check first rejected a legitimate `same` dedup decision (the absorbed ID disappears by design); now only one ID of a `same` pair must survive |
| Tests | 43/43 OK (21 new) |
| Not done | No screening, no pilot sample, no duplicate decision, no change to strategy or scope |
