# Session log — 2026-10-30 — LIT-PRESERVATION-V1-V5

**Objective** (researcher prompts, 2026-10-30; no task ID assigned, the label is the assistant's): after two read-only preservation audits and a verification plan, verify the LIT-003 and LIT-005 raw-export archives (V1), list and safety-check LIT-005 (V2), extract it into a temporary directory and check each file (V3), restore both archives and run the full `verify` (V4), then prepare the preservation records and the LIT-005 per-file evidence (V5). Each phase was authorised separately. **Not authorised**: commit, push, PR or issue changes, inventory build or derived records, deleting or altering restored files, screening, experiments, closing backup or storage questions.

## V1 — archive checksums (tool output)
| Archive | Size (expected) | SHA-256 (expected) | Result |
|---|---|---|---|
| LIT-003 | 3,647,967 (3,647,967) | `69e690f06834758aea76bca99ec4699c2abb2dac9aa776798aecf0366bd60c0e` (same) | match |
| LIT-005 | 479,473 (479,473) | `7b7d4674426c7581839b970cad37e21251ade0bf22d295814ac542bd7ec96ea1` (same) | match |

The first request found no upload; the archives were then uploaded by the researcher. Expected values from `research/literature/preservation/preservation_status.md`.

## V2 and V3 — LIT-005 (tool output)
| Check | Result |
|---|---|
| Entries listed without extraction | 39 regular files; 0 absolute, `..`, non-normalised, link, duplicate, unexpected or missing entries vs the 39 LIT-005 rows of `MANIFEST.csv` |
| Extraction | `tarfile` with `filter="data"` into a temporary directory outside the repository |
| Per-file SHA-256 vs `MANIFEST.csv` | 39 matched, 0 mismatched, 0 missing, 0 unexpected |
| Archive after | unchanged |

The V3 script also wrote a one-line note file with the temporary path; it was not authorised and was deleted with the temporary directory. No other temporary files remained.

## V4 — restoration of both archives (tool output)
| Step | Result |
|---|---|
| Start state | branch `claude/eloquent-mccarthy-bqtxr3-part1` at `ec526277508231047fcef8e5456ba85609963d05`; tracked tree clean; `raw_exports/` held only `MANIFEST.csv` and `README.md` |
| LIT-003 inspection | 211 entries (209 files, 2 directories under `lit003_raw_exports/`); 205 raw files plus 4 documented companion files; 0 unsafe or unexpected entries |
| Per-file check after safe extraction (outside the repository) | LIT-003 205/205, LIT-005 39/39 match `MANIFEST.csv` |
| Companion files (not restored) | `SHA256SUMS.txt` = committed `archive_contents_SHA256SUMS.txt`; archived `MANIFEST.csv` and `README.md` = `b48adde` versions; `raw_exports_inventory.csv` = committed file |
| Conflicts | 0 of 244 destinations existed |
| Restoration | 244 files created with exclusive create (`xb`), each re-hashed |
| `PYTHONDONTWRITEBYTECODE=1 python3 -I -B scripts/literature/pubrecords.py verify` | exit 0; `OK: all raw exports match MANIFEST.csv` |
| After | `MANIFEST.csv`, `README.md` and both archives unchanged; tracked tree clean; 244 ignored entries, all restored files; temporary directories removed; no build |

## V5 — evidence and records
| File | Change |
|---|---|
| `research/literature/preservation/LIT-005_archive_contents_SHA256SUMS.txt` (new) | 39 per-file SHA-256 lines with archive entry paths, sorted; SHA-256 of the file `26462b91f954e415b410eeeb2720f47fda39e8b1fac7c3ce0affcaf0bcb5ea60` |
| `research/literature/preservation/LIT-005_raw_exports_inventory.csv` (new) | 39 rows in the LIT-003 inventory format; SHA-256 of the file `3ea1922a4666fff0a46481c8741556776d8dac454f5fcdc029f3719289b38e49` |
| `research/literature/preservation/preservation_status.md` (+46) | one status-history row per archive; new final section (observed results, new evidence, researcher-reported Google Drive check, what is and is not established) |
| `research/reviews/unresolved_questions.md` (1 cell) | Q-063 status: "Open — partly addressed", with what remains |
| `logs/CHANGELOG.md` (+24), `logs/PROMPT_LOG.md` (+10), `research/reviews/daily_review_log.md` (+7) | task entries |
| this file (new) | session log |

The two evidence files were generated from the archive members read in memory; every hash equals the restored file and the committed `MANIFEST.csv` (39/39), and every file parses as JSON. Neither file existed before; nothing was overwritten.

## Validation (before this log was written)
| Check | Result |
|---|---|
| `pubrecords.py verify` (re-run) | exit 0; `OK: all raw exports match MANIFEST.csv` |
| Archives (re-checked) | 3,647,967 / `69e690f0…0c0e` and 479,473 / `7b7d4674…6ea1`: unchanged |
| LIT-005 listing | 39 lines, 39 unique paths, sorted; 39/39 equal `MANIFEST.csv` and the restored files; no LIT-003 companion file listed; inventory 39 rows agree with the listing |
| `git diff --check` | clean |
| Unchanged | `raw_exports/MANIFEST.csv` and `README.md`, `paper_inventory.*`, `records/`, `search_queries.csv`, `research/methodology/`, `GOVERNANCE.md`, `CLAUDE.md`, `scripts/`, `tests/`, `archive_contents_SHA256SUMS.txt`, `raw_exports_inventory.csv`, `logs/DECISION_LOG.md` |
| Not run | `tests/literature`, `tests/data_protection` and the query validator (not part of this authorisation); the data-protection tests scan new tabular files and should be run before any commit |

## Researcher-reported (not observed)
- Both archives downloaded back from Google Drive matched their local originals in PowerShell (2026-10-30; no values supplied).
- D: and E: are partitions of the same physical disk.

## Git state
Uncommitted when written; not pushed. No commit, PR, issue or comment.

## Outstanding
1. Backup on a separate physical device (researcher).
2. Google Drive approval as project storage (researcher decision).
3. Q-063 closure (researcher decision); the restored files exist only in this workspace.
4. Data-protection and literature tests before any commit.
