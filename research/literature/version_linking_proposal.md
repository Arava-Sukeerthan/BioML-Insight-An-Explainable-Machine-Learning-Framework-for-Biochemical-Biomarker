# Version Linking: Findings and Proposed Representation (blocker B-2)

| Field | Value |
|---|---|
| Task | LIT-004-REVIEW-AND-DECISIONS (2026-10-23) |
| Status | **PROPOSAL (D-030), not approved, not implemented.** None of the 15 pairs has been resolved, and no record was merged, linked or screened |
| Relationship | Answers blocker B-2 in `screening_protocol.md` §8 and offers an **alternative** to amendment A-4 (§4 there: "other version → `exclude E8`"). A-4 stays open. Who decides the pairs is still Q-024 |

## 1. What the current implementation does `[EVIDENCE]`

| Mechanism | Behaviour | Consequence for versions |
|---|---|---|
| Automatic dedup (`pubrecords.py deduplicate`) | Merges records that share a PMID, DOI, PMCID or arXiv ID, or the same normalised title with year ±1, **unless** they carry conflicting identifiers. Flags fuzzy titles (≥ 0.90) and same-title pairs with other differences | A preprint and its journal article normally have different PMIDs and DOIs, so they are never merged by identifier |
| `records/dedup_decisions.csv`, `same` | Merges the two clusters into one publication on the next build; one of the two paper IDs disappears from the outputs (it stays in the registry) | Not a link: the merged record has one title, one year and one set of identifiers, so "preprint" and "journal version" can no longer be counted separately. For pairs with an identifier conflict, `same` is **ignored** by the clustering step |
| `records/dedup_decisions.csv`, `different` | Removes the duplicate flag; both records stay separate | Fine for genuinely distinct records |
| Reversibility | Both decisions are undone by deleting the row and rebuilding: the source records are never changed, and the registry gives each record its old ID back | Reversible, but the edit leaves no history in the file itself |
| Provenance | Every source record is kept in `source_records.jsonl`. A merged publication lists all of them in `search_provenance` | Preserved |

**Gap:** the workflow has no way to say "these are two reports of the same work, keep both".
`search_strategy.md` §5.3 asks for exactly that ("A preprint and its published version are linked,
and the published version is primary"). It is not implemented.

## 2. The 15 pairs, by category (metadata only; nothing decided)

The categories come from the identifiers, publication types and URLs. No paper was read, and a
category is not a decision. `[EVIDENCE]` for the metadata, `[HYPOTHESIS]` for the category.

| Category | Pairs | Metadata observed |
|---|---|---|
| Preprint vs journal version (both PubMed) | P0010/P1368, P1213/P1320, P1360/P1442, P1466/P1479, P2128/P2148, P2140/P2149, P2488/P2535, P2562/P2565 | In each pair one record carries PubMed type *Preprint*, often with a `10.1101` (bioRxiv/medRxiv) or other preprint DOI. 3 pairs have conflicting identifiers (P1213/P1320, P2128/P2148, P2488/P2535), so a `same` decision would not merge them today |
| Preprint vs journal version, title changed | P1421/P1488 | "Lipid Ratios…" (2025 article) vs "Lipidomics…" (2023 preprint). Same work or not is **unclear** from metadata |
| Web record vs PubMed record, same article | P1343/P2987, P0098/P2988 | P2987's URL contains P1343's DOI (`s41598-026-37342-z`). P2988 is an ACS page with the same title as P0098 (an ACS journal); the URL does not contain the DOI |
| Web record vs PubMed record, other version | P0450/P2978 | P2978 is a medRxiv DOI (`10.1101/2024.05.14.24307378`); P0450 is the eLife article |
| arXiv record vs web record of the journal version | P2870/P2982 | P2870 is arXiv `2512.14727`; P2982 is a ScienceDirect page with the same title |
| Correction notice vs article | P0113/P0153 | P0113 has type *Published Erratum* and its own DOI; P0153 is the corrected article |
| Same title, different documents | P2980/P2981 | Two USPTO URLs with different document numbers (8367072, 9925227) |

Shared URLs: **no two publications in the current build share a URL** (checked over all
`source_urls`). The "distinct despite shared URL" case therefore does not occur now, but the
representation below covers it.

## 3. Proposed representation (D-030)

**Principle:** linking never merges. Every record keeps its paper ID, its metadata and its
provenance. A link is a separate, append-only statement about two records, and it can be withdrawn.

**File:** extend the existing `records/dedup_decisions.csv` (so there is still one file for pair
decisions; CLAUDE.md rule 8) with new decision values and three columns:

| Column | Content |
|---|---|
| `paper_id_a`, `paper_id_b`, `reviewer`, `date`, `note` | As now |
| `decision` | Existing `same` (merge) and `different`, plus the proposed values in the table below, plus `withdrawn` (cancels the latest earlier decision for the pair) |
| `primary_paper_id` (new) | For `version_of` and `duplicate_of`: the record that is screened and cited. Empty otherwise |
| `evidence` (new) | What the decision rests on, e.g. "journal article states it is the peer-reviewed version of the preprint DOI …" |
| `link_id` (new) | `L0001`, `L0002`, …. Allows a later row to withdraw a specific decision |

| Decision | Use | Effect in the build |
|---|---|---|
| `version_of` | Preprint and journal (or conference) version of the same work. Primary = the peer-reviewed version (`search_strategy.md` §5.3) | Both records kept. Both get `version_group` = the primary ID. Primary `version_role=primary`, the other `version_role=secondary` |
| `correction_of` | Erratum, corrigendum or expression-of-concern notice and its article. The article is primary | Both kept. The notice gets `version_role=notice` and `notice_for=<article>`. The article gets a flag `has_correction` |
| `duplicate_of` | Web (or other secondary-source) record that is the **same publication** as an indexed PubMed/arXiv record (the same article at another URL) | Both kept. The web record gets `version_role=duplicate`; its URL and query provenance are listed on the primary as an additional retrieval route |
| `different` | Genuinely distinct records despite similar titles or a shared URL | Duplicate flag removed (as now) |
| `same` | Kept for compatibility. **Recommended not to be used** for the 15 pairs, because it hides one of the two records | Merge (as now) |

The build would only add derived fields (`version_group`, `version_role`, `linked_paper_ids`,
`notice_for`, `has_correction`) to the publication record and the inventory. It changes no paper
ID and no registry row. Removing or withdrawing a link and rebuilding restores the exact previous
state, and the history stays in the file. A pair without a decision stays
`possible_duplicate_review`: both records are screened normally (as `screening_protocol.md` §4 already says).

Validation the build would apply: both IDs exist in the build; the primary is one of the two;
a record is primary in at most one `version_of` group, and no chain or cycle (A→B, B→C) is
allowed without an explicit group decision; `correction_of` needs one side with a notice type
or a note explaining why not.

## 4. Counting during screening and synthesis

The counts follow the PRISMA 2020 distinction between **reports** (records) and **studies**.
`[RECOMMENDATION]`

| Stage | Primary record | Secondary / duplicate / notice |
|---|---|---|
| Record flow ("records identified") | Counted | Counted. Every retrieved record stays visible in the flow |
| Duplicates removed before screening | — | `duplicate_of` records are counted here (same publication, other route). They are not screened |
| Title/abstract and full-text screening | Screened; the decision is made for the **work** | `version_of` secondaries are **not screened separately**. Their status is shown as "linked to Pxxxx" and follows the primary. If the screener finds that the two versions differ materially (e.g., another cohort), the link is withdrawn and both are screened |
| Correction notices | Article screened normally | Notice excluded at Stage 0 (E5, existing rule) and shown as linked to the article |
| Included studies | One per `version_group` | Not counted again |
| Included reports | Counted | Secondary versions counted as additional reports of the same study |
| Extraction and evidence synthesis | Data from the primary (peer-reviewed) version | The preprint is used only for information missing from the article, marked as such. A difference in results between versions is recorded, and the peer-reviewed values are used. A correction is applied to the article's extracted data and cited |
| Preprint only (no journal version found) | The preprint is primary and flagged `preprint` | — |

**Difference from A-4:** A-4 gives the secondary version `exclude E8`. That would count a
preprint as an *excluded record* although it is a report of an included study, and E8 is
defined as a duplicate code. D-030 keeps E8 for true duplicates and counts versions as linked
reports. Both options stay open until the researcher chooses.

## 5. What is needed before any pair is resolved

1. Approval of the representation (D-030, or A-4 instead).
2. Q-024: who decides the 15 pairs (researcher, or assistant with an audit).
3. Implementation of the approved option, with tests, before decisions are entered.
4. Each pair decided from the papers themselves (title page, "version of record" notes, DOIs), not from title similarity alone. P1421/P1488 in particular cannot be decided from metadata.
