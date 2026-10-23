# Approval Request — decisions before pilot screening

| Field | Value |
|---|---|
| Task | LIT-004-REVIEW-AND-DECISIONS (2026-10-23) |
| Status | **Awaiting the researcher's explicit approval. Nothing here is approved.** The researcher's LIT-004-REVIEW-AND-DECISIONS prompt states preferences for D-027, Q-031 and Q-032, and asks that they be prepared for explicit approval. They are recorded as PROPOSED in `logs/DECISION_LOG.md` |
| How to approve | Reply with, for example, "Approve D-027, D-028 (option a), D-029 (option a), D-030". Each approval is then entered in `DECISION_LOG.md` with the date and "researcher" |

## 1. Decisions prepared from the researcher's stated preferences

### D-027 — screening file and fallback keys (exists, PROPOSED since LIT-004-WORKFLOW-FIXES)
**Exact text for approval:** "`screening/decisions.csv` is the canonical screening-decision file
(columns and values as in `schemas/screening_decision.schema.json`). Records without a persistent
bibliographic identifier and without a year receive the deterministic registry key
`source_record:<source_record_id>`. The URL-key alternative is rejected."

Conflict check `[EVIDENCE]`: none with an approved decision. Two draft documents use other wording:
- `screening_criteria.md` §6 and `search_strategy.md` §6.2 (both unapproved) name two files and use `record_id`. Implementation notes already point to D-027.
- On approval, their text is amended to match. That amendment is part of this approval.

Already implemented and tested on the PR branch.

### D-028 — `publication_type` vs `record_type` (Q-031)
Researcher's stated preference: keep both fields. `publication_type` records source-provided
bibliographic metadata; `record_type` records our normalised screening classification.

**Conflict found** `[EVIDENCE]`: in the current schema, the verbatim source metadata already lives in a third field.
- `source_publication_types` holds the source's own types (e.g., PubMed `Journal Article;Preprint`).
- `publication_type` (LIT-001 / D-024 schema, all values currently empty) is a judgement enum: `original_research, methodological, software_framework, guideline, review_lead, preprint_original, other`. Source metadata cannot supply values such as "methodological" or "original research" without someone judging the paper.

So the preference cannot be applied by documentation alone. Options:

| Option | Exact text for approval | Change needed |
|---|---|---|
| **a** (recommended) | "`source_publication_types` = types exactly as the source gives them. `publication_type` = a normalised summary derived **only** from source metadata by a fixed mapping, with values `journal_article, preprint, review, erratum_or_correction, retraction_notice, editorial_comment_letter, conference_paper, patent, web_page_unknown, other`. `record_type` = the screener's classification (`original, methodological, software, guideline, review_lead, preprint, notice`)" | Schema enum of `publication_type` replaced (no record has a value, so nothing is lost); mapping implemented and tested; `publication_type` removed from the manual fields |
| b | "`publication_type` keeps its LIT-001 meaning (manual classification at extraction); `record_type` is the screening classification; source metadata stays in `source_publication_types`" | Documentation only; but two judgement fields remain (the overlap Q-031 asked about) |

### D-029 — required screening descriptors (Q-032)
Researcher's stated preference:
- all four descriptors are required for `include` and `uncertain`;
- each allows `yes`, `no` or `unclear`;
- no positive result is inferred from missing abstract information.

**Conflict found** `[EVIDENCE]`: the proposed D-026 (`screening_protocol.md` §2) and the implemented schema give `dim_independent_validation` the values `external / temporal / internal_only / unclear`, not `yes/no/unclear`.

| Option | Exact text for approval |
|---|---|
| **a** (recommended) | "For every `include` or `uncertain` row, `dim_explainability`, `dim_uncertainty`, `dim_calibration` and `dim_independent_validation` are required, each `yes`, `no` or `unclear`. `yes` only when the title/abstract states it. `no` only when the abstract states its absence or describes a design that excludes it (e.g., 'internal cross-validation only' → validation `no`). Not mentioned, or no abstract → `unclear`. The design detail moves to a new optional column `validation_design` (`external / temporal / internal_only / unclear`). D-026's four-value enum is revised accordingly" |
| b | As (a), but `dim_independent_validation` keeps `external / temporal / internal_only / unclear` (it then does not follow the yes/no/unclear rule) |

Either option revises proposed D-026 (not approved), so no approved decision changes.
Not implemented yet: the enforcement and enum change follow the approval.

## 2. Further decisions prepared in this task

| ID | Decision | Document |
|---|---|---|
| D-030 | Version links without merging (`version_of`, `correction_of`, `duplicate_of`, `different`, `withdrawn` in `records/dedup_decisions.csv`), counted as reports vs studies. **Alternative to** A-4 (secondary → E8) | `research/literature/version_linking_proposal.md` |
| Scope | Q-001, Q-002 (+ new Q-033 proteomics), broader biomedical ML rule, Q-007/D-009, Q-022 | `research/methodology/scope_decision_brief.md` |

## 3. Exact approvals needed before the pilot can be generated

| # | Item | Why it blocks the pilot |
|---|---|---|
| 1 | D-027 | Format the pilot decisions are written in |
| 2 | D-029 (option a or b) and D-026 | Which descriptors are recorded and required in the pilot |
| 3 | D-028 (option a or b) | Meaning of `record_type` used at screening |
| 4 | Q-001 (disorders), Q-002 (biomarker strands) and Q-033 (proteomics) | E4/E3 decisions in the pilot |
| 5 | Rule for broader biomedical ML (brief §3) | E4 vs `non_metabolic_method_exemplar` |
| 6 | Q-007 / D-009 (Q-PM-02 option A or B) | Which records the sample is drawn from (stratum B) |
| 7 | Q-022 (D-005, D-006, D-007 as executed, with deviations) | Screening must run on an approved search |
| 8 | D-025 / Q-026 (pilot design, seed 4004) or the `screening_criteria.md` §7 alternative | Defines the sample itself |
| 9 | D-008 / Q-008 (researcher audit) and the pilot's blinded second screening | Without a second screener the pilot cannot measure agreement |
| 10 | D-030 or A-4, plus Q-024 | Only if the 15 pairs are to be decided before the pilot. Otherwise the protocol rule applies: both records of a pair are screened, and the pair is listed in the pilot report |
| 11 | Screening-criteria amendments A-1, A-2, A-5, A-6 (and A-3 / Q-028 for RQ5 counting) | The pilot tests a fixed criteria version |

Not blocking the pilot, but still open: D-010 / Q-011 (storage; no off-device backup), D-012 / D-023
(transcription controls), D-024 (inventory schema).
