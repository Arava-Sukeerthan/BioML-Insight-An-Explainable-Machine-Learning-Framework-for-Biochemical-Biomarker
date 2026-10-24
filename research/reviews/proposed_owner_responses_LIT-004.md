# PROPOSED Owner Responses — LIT-004 ballot (version 1, awaiting owner confirmation)

| Field | Value |
|---|---|
| Task | LIT-004-PROPOSED-RESPONSES (2026-10-24) |
| Status | **PROPOSED. NOT RECORDED. NOT APPROVED.** These are the responses the owner's prompt of 2026-10-24 proposes for `research/reviews/owner_review_ballot_LIT-004.md` (the authoritative ballot, unchanged). The prompt states they are "proposed responses for owner review, not permission to bypass the repository's approval process" |
| Decision log | `logs/DECISION_LOG.md` is **unchanged**. No entry is marked APPROVED, REJECTED or DEFERRED |
| How this becomes a decision | The owner confirms explicitly, e.g. "I confirm that proposed response set v1 in `proposed_owner_responses_LIT-004.md` is to be recorded" (or confirms selected items, or amends). A separate step then records each confirmed response in `logs/DECISION_LOG.md` with the date and "researcher", keeping every condition listed below. Implementation is a further, separate task |
| Nothing done in this task | No screening, no pilot sample, no pair resolution, no schema, criteria or code change, no spot-check run (Item 11 runs only after confirmation) |

Notation:
- **Response** = the ballot field that would be ticked.
- **Conditions** = what stays open even after confirmation. Each condition must be carried into the decision-log entry.

---

## Summary

| # | ID | Proposed response | Conditions / open dependencies kept |
|---|---|---|---|
| 1 | D-027 | APPROVE (limited) | Only the file, key scheme and required columns. Descriptor columns follow Items 2, 3 and 7 |
| 2 | D-028 | 2a APPROVE · 2b APPROVE · 2c REJECT · 2d APPROVE | Mapping table versioned; every extension logged |
| 3 | D-029 (+ D-026) | APPROVE option (a), **conditional** | Final wording of the definitions (ballot Item 3, C-3 to C-6) to be confirmed before implementation; silence = `unclear` |
| 4 | D-030 | **MODIFY** | Group-level retraction rule replaced by the procedure in §4 below |
| 5 | Q-024 / Q-029 | APPROVE ballot option (c): defer all 15 pair decisions until after the pilot | Who decides after the pilot is still open. Q-029 follows D-030 |
| 6 | Q-001 | APPROVE (main list provisional) | Obesity, thyroid dysfunction and PCOS **remain pending** |
| 7 | Q-002 / Q-035 | APPROVE | `biomarker_class` values as in the ballot. Required status follows Item 3 |
| 8 | Q-033 | APPROVE option (a): proteomics **remains pending** | Flag `scope_pending_proteomics` |
| 9 | Q-007 / D-009 | APPROVE option (a): screen all 743 | Exclusions counted by code; recall limitations reported. Depends on Items 6–8 |
| 10 | Q-022 (D-005, D-006, D-007) | APPROVE option (a): as executed, with limitations | All 30 unexecuted searches listed; no comprehensiveness claim. Ballot option (b) (re-run when access exists) neither chosen nor excluded |
| 11 | D-012 / D-023 / Q-036 | APPROVE: arXiv spot-check to be run; web-file checks documented as not performed | D-012/D-023 approval **conditional on the arXiv spot-check outcome**. A failed check reopens the item |
| 12 | D-010 / Q-011 | APPROVE option (a) | **No off-device backup exists**; recorded as a limitation, not as resolved |
| 13 | D-008 / Q-008 | APPROVE | — |
| 14 | D-025 / Q-026 | APPROVE | Pilot generated only after every pilot-blocking item is recorded (section A) |
| 15 | A-1, A-2, A-5, A-6 / A-4 / A-3 | A-1, A-2, A-5, A-6 APPROVE · A-4 REJECT (in favour of D-030) · A-3 DEFER | A-3 depends on Item 16 |
| 16 | A-3 / Q-028 | **DEFER** | Options reproduced in §16 below without a recommendation |
| 17 | D-024 | APPROVE with the revised D-028 and D-029 | Q-034 enum not mentioned in the prompt; see §17 |

---

## 1. D-027
**Response:** APPROVE, limited to `screening/decisions.csv` as the canonical file, the key scheme
`source_record:<source_record_id>` for records with no persistent identifier and no year, and the
required columns `paper_id, stage, decision, reason_code, screener, date, justification`.

**Not covered by this approval:** the optional descriptor columns. They follow Items 2d, 3 and 7.

## 2. D-028
**Responses:**
- **2a APPROVE.** Roles: verbatim `source_publication_types` (never dropped); `publication_type` derived only from source metadata by the versioned mapping table; `record_type` filled by the screener.
- **2b APPROVE.** Source database = arXiv → `preprint`.
- **2c REJECT.** No URL or DOI-prefix inference. Affected records stay `unknown`.
- **2d APPROVE.** `record_type` = `original, methodological, software, guideline, review_lead, other`.

**Conditions kept:** retracted articles keep their type and the `retracted` flag (E7). Notices are typed separately. Unrecognised source types go to `other` and are listed in `unmapped_publication_types`. Any extension of the table is a logged change.

## 3. D-029 (revises D-026)
**Response:** APPROVE ballot option (a), **conditional**:
- three method descriptors (`dim_explainability`, `dim_uncertainty`, `dim_calibration`: `yes/no/unclear`) plus a separate `validation_design` (`external/temporal/internal_only/none/not_applicable/unclear`);
- **silence in the title/abstract means `unclear`, never `no`;**
- the exact definitions (ballot Item 3: the meaning table, the term rules C-3 to C-6, the `validation_design` values and the human-review triggers) are **not final**. They are presented once more for confirmation before implementation.

**Open:** that confirmation of the final definitions. D-026 stays open until it is recorded as revised by D-029.

## 4. D-030 — MODIFY: evidence-based retraction procedure

**Response:** MODIFY. Keep the reversible, provenance-preserving links without merging (ballot Item 4, §4.1, §4.2 except the retraction bullet, and the §4.3 counting specification). **Replace** the ballot's retraction rule ("If the primary of a version group is retracted, the whole group is excluded under E7 … other versions are not used as evidence") with the procedure below.

### 4.1 Principles
1. A retraction applies to the **retracted article**. Only a record that is itself retracted gets E7.
2. Related records (other versions, web copies, correction or retraction notices) are **never excluded automatically** because of a retraction elsewhere in the group. Each one is decided on recorded evidence, with human review where the evidence is unclear.
3. Nothing is merged or deleted. Every decision is a row with a justification, so it can be reversed.

### 4.2 Procedure

| Record | Handling | Evidence required | Human review |
|---|---|---|---|
| **Retracted article** (source type *Retracted Publication*, or the target of a linked retraction notice) | `exclude E7` at Stage 0 (existing rule) | The source metadata, or the linked notice | No, unless the metadata conflict |
| **Retraction notice** (*Retraction of Publication*) | `exclude E5` at Stage 0 (notice, not a study); linked with `retraction_of` | Source type | No |
| **Correction notice / expression of concern** about the retracted article | `exclude E5` at Stage 0; linked with `correction_of` | Source type | No |
| **`duplicate_of` copy** of the retracted article (the same publication, another URL) | Counted once, as a duplicate of the retracted article (`duplicate_removed`), so it is not screened separately and not counted as a separate exclusion | The `duplicate_of` link and its evidence | Only for the link decision itself |
| **Other version** (`version_of`, e.g. the preprint of a retracted journal article, or the journal version of a retracted preprint) | **Not excluded automatically.** Set to `uncertain` with `needs_human=yes`, then decided on the evidence (next table) | The retraction notice's stated reason, and the status of that version at its own server or journal | **Yes**, always |

**How a related version is decided** (screener proposes, owner confirms):

| Evidence found | Decision for the related version |
|---|---|
| The version is itself withdrawn or retracted by its server or journal | `exclude E7` (it is retracted itself), citing that notice |
| The notice gives a reason that invalidates the shared data or results (e.g., fabricated, falsified or unreliable data; unreliable analysis; duplicated data) | `exclude E12` with the justification "evidence invalidated by the retraction of Pxxxx (reason: …)" and the notice cited. This uses the existing catch-all code with a mandatory justification (A-2), and no new code is needed |
| The notice gives a reason that does not concern the shared data or results (e.g., publisher error, journal-level duplicate publication, authorship or consent dispute that the notice states does not affect the findings) | Screened normally on its own merits, flagged `related_to_retracted:Pxxxx`. If included, it is reported with the flag, and a sensitivity analysis without it is planned |
| No notice text available, or the reason is unclear | `uncertain`, `needs_human=yes`. Not excluded and not included until evidence is obtained. Listed in the adjudication queue |

**PRISMA accounting.**
- The retracted article: Stage 0, E7.
- Notices: Stage 0, E5.
- `duplicate_of` copies: duplicates removed.
- Related versions: by their own decision (E7, E12, included with flag, or pending).
- No record is counted twice, and the flow diagram notes how many records were decided under this procedure.

**Current data `[EVIDENCE]`:**
- The three retracted articles (P0931, P0939, P1443) are not in any of the 15 flagged pairs and have no possible duplicates.
- No *Retraction of Publication* record is present. The procedure therefore affects no current record.
- It applies if a link to a retracted article is created later.

**Open:** owner confirmation of this procedure. It is new wording, so it needs explicit confirmation in addition to the rest of D-030.

## 5. Q-024 / Q-029
**Response:** APPROVE ballot option (c). **All 15 pair decisions are deferred until after the pilot.**
- Until then, both records of each pair are screened as separate records, and the pilot report lists the pairs.
- All paper IDs, source records and provenance are preserved; nothing is merged.

**Open:**
- Who decides after the pilot (ballot options a or b) is not chosen.
- Q-029 is answered by D-030 (Item 4) once that is recorded.

## 6. Q-001
**Response:** APPROVE the main disorder list of `screening_criteria.md` §2.1 as the **provisional** screening scope.

**Pending, unchanged:** obesity (as a classification target), thyroid dysfunction, PCOS, included at screening with the tag `scope_pending_disorder`.

**Open:** final disorder scope; D-013 (primary disorder) later.

## 7. Q-002 / Q-035
**Response:** APPROVE two distinct biomarker strands (metabolomics/lipidomics; routine clinical chemistry) and the descriptor `biomarker_class` (`metabolomics_lipidomics / newborn_screening_msms / routine_chemistry / mixed_both / other / unclear`). NBS MS/MS is reported with metabolomics; `mixed_both` is reported in both strands.

**Dependency:** whether `biomarker_class` is required for include/uncertain follows Item 3.

## 8. Q-033
**Response:** APPROVE ballot option (a). **Proteomics remains pending**, included at screening with `scope_pending_proteomics`. Multi-omics studies with a substantive metabolomics layer stay eligible.

**Open:** the final proteomics decision.

## 9. Q-007 / D-009
**Response:** APPROVE option (a): all 743 Q-PM-02 records are screened against the approved criteria. Out-of-scope records are excluded with E3/E4 and counted. The query's recall limitations (ballot Item 9) are reported, and no completeness claim is made for the strand.

**Dependencies:** Items 6–8. **Evidence still needed:** MeSH tree verification before the limitations text is written.

## 10. Q-022 (D-005, D-006, D-007)
**Response:** APPROVE ballot option (a). D-005, D-006 and D-007 are approved **as executed**: 26 of 56 planned searches.

The **30 unexecuted searches**, all to be listed as *not searched*:

| Source | Not executed | Reason |
|---|---|---|
| Consensus | 10 | Quota exhausted |
| Europe PMC | 6 | Host blocked |
| Semantic Scholar | 5 | Host blocked |
| Google Scholar | 4 | Manual only, not done |
| Crossref | 3 | Host blocked |
| Repository APIs (Q-RP-01, Q-RP-02) | 2 | Hosts blocked |

The other deviations are recorded as limitations:
- the web domain filter was not honoured;
- the search ran on Day 10 instead of Day 3;
- arXiv and web records have no date limit and are not reproducible snapshots;
- arXiv records have no authors.

The search is **not** described as comprehensive.

**Open:** ballot option (b) (re-run the blocked searches when access exists) is not chosen, and remains possible.

## 11. D-012 / D-023 / Q-036
**Response:** APPROVE.
- **Run the arXiv spot-check** (≥ 10 % re-fetch of the 5 transcribed arXiv files via alphaXiv) after the owner confirms this response set. It is not run in this task.
- The **web-file checks** (6 files) are documented as **not performed**. That is a limitation: web results cannot be reproduced.

**Condition:** D-012/D-023 are recorded as approved only after the arXiv spot-check passes. If it fails, the item reopens.

Verification statuses are unchanged either way: arXiv `partially_verified`, web `unverified`.

## 12. D-010 / Q-011
**Response:** APPROVE ballot option (a). D-010 (raw exports and abstracts kept out of the public repository) is approved.

The current backup state is documented as a limitation:
- a checksum-verified archive exists in two copies on one computer (owner-reported);
- **no off-device backup exists.**

Nothing may state or imply that an off-device backup exists.

## 13. D-008 / Q-008
**Response:** APPROVE the planned blinded audit: 25 included + 25 excluded decisions after the first expansion batches. κ < 0.60 or a wrong exclusion leads to clarified criteria and re-screening of the affected records.

## 14. D-025 / Q-026
**Response:** APPROVE the pilot design in ballot Item 14:
- 60 records, stratified random, seed 4004;
- independent, blinded screening by the assistant and the owner;
- agreement reporting (percentage, κ on 3 levels and on include vs not, exclusion-code agreement, per-descriptor agreement);
- pass criteria as stated in the ballot;
- a second pilot of 40 records if it fails.

**Condition:** the sample is generated only after all pilot-blocking items (section A below) are recorded and implemented.

## 15. Screening-criteria amendments
| Amendment | Response | Note |
|---|---|---|
| A-1 | APPROVE | = Item 14 |
| A-2 | APPROVE | Code clarifications; E1–E12 unchanged. Also used by the §4 retraction procedure (E12 with mandatory justification) |
| A-3 | **DEFER** | Depends on Item 16 |
| A-4 | REJECT | In favour of D-030 (Item 4) |
| A-5 | APPROVE | = Item 1 |
| A-6 | APPROVE | No abstract → `uncertain` unless a title-level E-code applies |

## 16. A-3 / Q-028 — DEFER (options reproduced; no recommendation)

**Response:** DEFER until the owner has reviewed the exact alternatives below.

Exact options, as in the ballot:
> **(a)** Keep four components, with calibration or uncertainty counted as one.
> **(b)** Five components (uncertainty and calibration separate), still ≥ 3.
> **(c)** Five components, ≥ 4.

Components (from `screening_criteria.md` §3, RQ5): biomarker/feature selection; classification; explainability; calibration or uncertainty estimation. Under (b) and (c), calibration and uncertainty count separately.

Consequences, described without preference:

| Option | Which frameworks qualify as closest prior art (RQ5) | Example (hypothetical, for illustration only) | Effect on later work |
|---|---|---|---|
| (a) | ≥ 3 of 4. Calibration and uncertainty together contribute at most one | Selection + classification + calibration qualifies. Classification + calibration + uncertainty does **not** (2 components) | Keeps the current definition. Frameworks that combine calibration and uncertainty without feature selection or explainability fall outside RQ5 |
| (b) | ≥ 3 of 5 | Both examples qualify | The RQ5 set is the largest of the three, and more papers enter the closest-prior-art table that must be complete before any novelty claim. More full-text work for theme F |
| (c) | ≥ 4 of 5 | Neither example qualifies; e.g. selection + classification + explainability + calibration is needed | The RQ5 set is the smallest, limited to more complete frameworks. Fewer papers in the closest-prior-art table, and partial combinations are described under RQ2–RQ4 instead |

Common to all options:
- the choice changes the theme F evidence table and the basis of any later novelty assessment (Stage D);
- it must be made before theme F records are screened, or those records are re-screened afterwards;
- it interacts with Item 3, because the descriptors record calibration and uncertainty separately in every option.

Note: the ballot's Item 16 contains the phrase "Option (b) … is the more cautious choice before a novelty claim". This proposed response does **not** adopt that phrase. The table above is the neutral description. The ballot text itself is unchanged.

## 17. D-024
**Response:** APPROVE D-024 together with the revised D-028 (Item 2) and D-029 (Item 3) definitions.

**Point to confirm:** ballot option (a) also includes the Q-034 enum for `extraction_status` (`not_extracted / abstract_only / full_text`). The owner's prompt does not mention Q-034. Recorded as **D-024 + D-028 + D-029, with Q-034 left open**, unless the owner says to include it.

**Condition:** D-024 is recorded only together with the confirmed D-028 and D-029, after Item 3's definitions are final.

---

## A. Pilot-blocking items still open after confirmation

Even if the whole set is confirmed:
1. the D-029 definitions (Item 3) must be finalised;
2. the D-030 retraction procedure (Item 4) must be confirmed;
3. the arXiv spot-check (Item 11) must be run and pass;
4. A-3 / Q-028 is deferred (Item 16). The pilot can proceed only if theme F records in the pilot are screened with the RQ5 tag left provisional, or Item 16 is decided first. **Owner to choose**;
5. implementation of D-028, D-029, D-030 (links only; no pair decisions), `biomarker_class` and the scope flags, with tests and a rebuild that changes no paper ID;
6. `screening_criteria.md` v1.1 and protocol v0.2, frozen as the pilot's `criteria_version`.

## B. Confirmation line for the owner

> "I confirm that proposed response set v1 (`research/reviews/proposed_owner_responses_LIT-004.md`) is to be recorded in `logs/DECISION_LOG.md`, [all items / items …], [with these changes: …]."

Until such a confirmation is received, every item in `logs/DECISION_LOG.md` keeps its current status.
