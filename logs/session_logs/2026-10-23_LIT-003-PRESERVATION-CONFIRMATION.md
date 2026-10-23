# Session log — 2026-10-23 — LIT-003-PRESERVATION-CONFIRMATION

**Objective**: record the researcher's Windows SHA-256 verification of the downloaded LIT-003 archive, without overstating durable storage.

| Step | Outcome |
|---|---|
| Pre-task `git status` / `git log` | Clean; branch `claude/sweet-brahmagupta-urw7l1` at `f17a4ea` (= origin, PR #2 head) |
| Researcher report | `certutil -hashfile` on the downloaded copy gave `69e690f06834758aea76bca99ec4699c2abb2dac9aa776798aecf0366bd60c0e`, which matches the expected hash (as stated by the researcher; output not observed by the assistant) |
| Container archive re-check | see CHANGELOG validation |
| Status recorded | Downloaded and checksum-verified; **durable storage not confirmed** (no second backup reported); no credentials requested or recorded |
| Raw exports / archive | Not modified; not committed |

## Second update (same day): second local copy
| Step | Outcome |
|---|---|
| Pre-task `git status` / `git log` | Clean; branch at `7b61e83` (= origin) |
| Researcher report | Downloads copy verified with `certutil`; second copy at `%USERPROFILE%\Documents\BioML-Insight-Backup\` also verified (as reported; outputs not observed) |
| Consistency with existing records | No conflict: the earlier records said durable storage was pending; the new information is a second local copy, not an off-device backup |
| Status recorded | Integrity verified; local redundancy (2 copies, same computer); **off-device backup outstanding**. Earlier status kept in a status-history table |
| Raw exports / archive | Not modified; not committed |
