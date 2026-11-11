# Session log — 2026-11-11 — PRE-FREEZE-GOVERNANCE-REVIEW

**Prompt**: "We need to complete a comprehensive pre-freeze governance review of the BioML-Insight research repository."

**Scope**: documentation only.

**Not done**:
- freeze; freeze entry; registry; activation rows; fixed-inventory entry; run authorisations;
- Stage 0; sampling; screening;
- custodian; D-102;
- raw-export, inventory or records changes;
- stage, commit, push or merge;
- status-cell changes.

## Baseline (before editing)
- Branch `claude/eloquent-mccarthy-bqtxr3-part1`; HEAD `c6e1b14c81821c0cddca26af1d0070829152999c`; remote `8d9bd79`; 1 ahead, 0 behind; nothing staged.
- 9 modified files and 6 untracked files.
- Working-tree diff (849 lines) and SHA-256 of the 15 changed files saved outside the repository.

## Main finding
The Q-063 register text added under D-106 (2026-11-11) described the off-device backup as "outstanding". The register's own earlier entries and D-010 record otherwise:
- the researcher designated a private Google Drive folder as the off-device backup (Q-011 option (b), 2026-10-30);
- the researcher reported Drive-copy SHA-256 values equal to the recorded values (not observed by the assistant).

What remains open is the backup's provenance (approval details; PRESERVED status) and a verified restore in each new workspace. The wording was corrected; Q-063 stays Open.

## Exact replacements (preserved)
- `research/reviews/unresolved_questions.md`:

  > before: the off-device backup of the raw exports is established and recorded, because the fixed inventory and the Git-ignored record files derive from them.

  after: the provenance of the off-device backup is settled: the private Google Drive folder designated under D-010 (Q-011 option (b)) holds the raw-export archives, with Drive-copy SHA-256 values reported by the researcher as equal to the recorded values (not observed by the assistant); the researcher records the outstanding approval details and decides the PRESERVED status. This is needed because the fixed inventory and the Git-ignored record files derive from those raw exports.

- `research/reviews/unresolved_questions.md`:

  > before: Update 2026-11-11 (D-106): restriction retained: off-device backup / disaster recovery is outstanding, and each workspace in which a rebuild or a provenance check of the ignored record files is run needs a verified restore of the raw exports first.

  after: Update 2026-11-11 (D-106; corrected the same day): restrictions retained: the off-device backup is designated (D-010; private Google Drive folder) but its provenance is not yet settled (approval details to be recorded; PRESERVED status not decided; Drive-copy hashes researcher-reported, not assistant-observed); and each workspace in which a rebuild or a provenance check of the ignored record files is run needs a verified restore of the raw exports first.

- `research/literature/screening_criteria_v1.1.md`:

  > before: The inventory is fixed in a separate decision-log entry before D-035 record §6 condition 6 is recorded (D-107), and the pilot records its SHA-256 again at the draw

  after: The inventory is to be fixed in a separate decision-log entry before D-035 record §6 condition 6 is recorded (D-107, approved in principle, subject to verification; the exact order is the proposal D-108), and the pilot records its SHA-256 again at the draw

- `research/literature/screening_criteria_v1.1.md`:

  > before: 1. The approved decisions written into the texts (D-080 to D-107 and D-109, as recorded in `logs/DECISION_LOG.md`; D-108 is a proposal and is not written in as a rule)

  after: 1. The approved decisions written into the texts (D-080 to D-107 and D-109, as recorded in `logs/DECISION_LOG.md`; D-107 is approved in principle only, subject to verification; D-108 is a proposal and is not written in as a rule)

- `research/literature/screening_criteria_v1.1.md`:

  > before: and its item (d) requires the separate fixed-inventory entry recorded before the condition-6 row, D-107;

  after: and its item (d) requires the separate fixed-inventory entry recorded before the condition-6 row, D-107, approved in principle;

- `research/literature/screening_criteria_v1.1.md`:

  > before: | §1 I-C1–I-C4, E2, E7, E9–E11, RQ2–RQ4, RQ6 | Unchanged | — | — |

  after: | §0; §11 steps 1, 10 | PRE-FREEZE-GOVERNANCE-REVIEW (2026-11-11): D-107 described as approved in principle, subject to verification, wherever its requirement is stated; the exact order named as the proposal D-108. No rule changed | D-107; D-108 (proposed) | D-107: APPROVED IN PRINCIPLE; D-108: PROPOSED |
| §1 I-C1–I-C4, E2, E7, E9–E11, RQ2–RQ4, RQ6 | Unchanged | — | — |

- `research/literature/screening_protocol_v0.2.md`:

  > before: the inventory is fixed in a separate decision-log entry before condition 6 is recorded (D-107), and its SHA-256 is recorded again in `pilot_sample.csv` at the draw (D-077 (5))

  after: the inventory is to be fixed in a separate decision-log entry before condition 6 is recorded (D-107, approved in principle, subject to verification; the exact order is the proposal D-108), and its SHA-256 is recorded again in `pilot_sample.csv` at the draw (D-077 (5))

- `research/literature/screening_protocol_v0.2.md`:

  > before: both run authorisations bind the same `inventory_sha256` (D-107; the amended order is proposed in D-108, not approved).

  after: both run authorisations bind the same `inventory_sha256` (D-107, approved in principle, subject to verification; the amended order is proposed in D-108, not approved).

- `research/literature/screening_protocol_v0.2.md`:

  > before: R1 selected as the design (D-109)].** The pilot cannot start until the revision is approved.

  after: R1 selected as the design, R2 as the fallback (D-109; design only)].** The pilot cannot start until the revision is approved.

- `research/literature/screening_protocol_v0.2.md`:

  > before: | §8 of v0.1 (blockers B-1…B-6) |

  after: | §1; §7a; §10 | PRE-FREEZE-GOVERNANCE-REVIEW (2026-11-11): D-107 described as approved in principle, subject to verification (§1, §10 row 6); the exact order named as the proposal D-108; §7a step 5 names R2 as the fallback (D-109, design only). No custodian appointed; nothing implemented. **No exclusion rule, threshold, sample parameter or RQ changed** | D-107; D-108 (proposed); D-109 |
| §8 of v0.1 (blockers B-1…B-6) |

## Git
Uncommitted; nothing staged; not pushed. PR #17 not changed.
