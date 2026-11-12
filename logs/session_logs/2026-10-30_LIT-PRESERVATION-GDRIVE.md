# Session log — 2026-10-30 — LIT-PRESERVATION-GDRIVE

**Objective** (researcher prompt, 2026-10-30; no task ID assigned, the label is the assistant's): record the researcher's report that explicit approval has been obtained to use their personal Google Drive for research archives, recording only what the available evidence supports; list missing approval details; keep Q-063 open; do not mark preservation complete. **Not authorised**: stage, commit, push, PR or issue changes; changes to protocol, dataset decisions, screening status or experiment authorisation.

## Inspected records
| Record | Finding |
|---|---|
| `preservation_status.md`, "Storage options investigated" | "Researcher's Google Drive": not used, not approved as project storage (2026-10-23) |
| `preservation_status.md`, V1–V4 section (2026-10-30) | Drive copies downloaded back and matched in PowerShell (researcher-reported, no values); Google Drive approval not recorded |
| `unresolved_questions.md` Q-063 | Open — partly addressed; listed "Google Drive not approved as project storage" |
| `unresolved_questions.md` Q-011; `DECISION_LOG.md` D-010 | Storage question Open; D-010 PROPOSED. No storage-approval decision |
| Repository-wide search | No approver, approval date, scope, conditions or wording for Google Drive use recorded anywhere |

## Changes (uncommitted)
| File | Change |
|---|---|
| `research/literature/preservation/preservation_status.md` | one status-history row each for LIT-003 and LIT-005; new final section "Google Drive copies: approval reported (2026-10-30)" |
| `research/reviews/unresolved_questions.md` | Q-063 status cell: Google Drive clause only; still Open |
| `logs/CHANGELOG.md`, `logs/PROMPT_LOG.md`, `research/reviews/daily_review_log.md` | task entries |
| this file (new) | session log |

No DECISION_LOG entry: the approver, date, scope and conditions are not recorded. Google Drive was not accessed.

Revision on review (same day, researcher request): the Drive folder name was removed from all new text (public repository) and replaced by "a private folder in the researcher's personal Google Drive"; the new section was split into four parts: researcher-reported approval, approval details not yet recorded or verified, archive integrity verification (assistant-observed vs researcher-reported), and the unresolved backup-requirement decision. Q-063 and Q-011 stay Open.

## Missing approval details
Approver (owner or supervisor, and who); approval date; form, wording and where it is kept; scope (these archives or all raw exports; files with PubMed abstracts, D-010/Q-011); conditions (access, retention, institutional policy); optionally the Drive copies' SHA-256 values.

## Validation
See the task-completion report of this prompt (`git diff --check`, `pubrecords.py verify`, file list).

## Git state
Uncommitted when written; not pushed. No commit, PR, issue or comment.

## Outstanding
1. Missing approval details (researcher).
2. Backup on a separate physical device, or a researcher decision that the Drive copy meets the off-device requirement.
3. Q-063 closure (researcher decision).
