# arXiv transcription spot-check (Q-036, D-012) — 2026-10-30

| Field | Value |
|---|---|
| Task | SCREENING-PREREQ-DECISIONS-2 (2026-10-30; assistant label) |
| Authorisation | Q-036 answered by the owner on 2026-10-30: run the arXiv spot-check (ballot Item 11 option (a) for arXiv) and document the web-transcription gap as a limitation (option (b) for web) |
| Result | **PASSED: 25 of 25 sampled records match, in all 5 files** |
| Evidence file | `arxiv_transcription_spot_check_2026-10-30.csv` (one row per sampled record) |
| Recorded | `raw_exports/MANIFEST.csv`: `transcription_check=passed` and a note for the 5 files (`pubrecords.py set-check`, 2026-10-30); no other cell changed; `verify` OK |
| Not changed | Raw files, inventory, verification statuses (recomputed only at the next build) |

## 1. Scope
- **Checked:** the 5 transcribed arXiv raw files named in Q-036, `Q-AX-01` … `Q-AX-05_2026-10-23.json` (LIT-003; 76 records in total: 13, 18, 16, 15, 14).
- **Not checked:** `Q-AX-G9_2026-10-28.json` (LIT-005, 15 records). It is also `transcription_check=not_done` but is outside Q-036's wording; its records stay capped at `partially_verified` (D-012).
- **Web files (6):** not checked, by the owner's choice (ballot Item 11 (b)). Web results are not reproducible; this is recorded as a **limitation**, and web records stay `unverified`.

## 2. Procedure
Rule applied: `collection_workflow.md` §2.1 (D-012): ≥ 10 % of records per transcribed file, minimum 5, seed recorded.
1. **Sample.** Per file `n = max(5, ceil(0.10 × records))` = 5 for every file. Records drawn with Python `random.Random("3036:<query_id>").sample(...)` (seed string recorded per file). 25 records in total.
2. **Re-fetch** through the alphaXiv connector on 2026-10-30:
   - each file's original request was re-run with `discover_papers` (same question, keywords, difficulty 3, prioritize default; from the file's `provenance.request`). 24 of the 25 sampled records reappeared in the re-run listings;
   - the one record not in its re-run listing (`2607.09649`, Q-AX-04) was re-fetched at record level (`answer_pdf_queries`, first page): title and the arXiv stamp `arXiv:2607.09649v1 [cs.AI] 10 Jul 2026`;
   - two records were additionally checked at record level against the PDF stamp (`2509.15349`: v1, 18 Sep 2025; `2605.12917`: v1, 13 May 2026).
3. **Compare** the transcribed fields that exist in these files: arXiv ID, title (compared after case-folding and whitespace normalisation), year, and the tool's "Published" date. The files carry no authors, venue, DOI or abstract (left empty at transcription, not inferred), so those fields cannot be compared. Rank was not compared (the listing is relevance-ranked and not reproducible).

## 3. Result

| File | Records | Sampled | Match | Mismatch |
|---|---|---|---|---|
| Q-AX-01 | 13 | 5 | 5 | 0 |
| Q-AX-02 | 18 | 5 | 5 | 0 |
| Q-AX-03 | 16 | 5 | 5 | 0 |
| Q-AX-04 | 15 | 5 | 5 | 0 |
| Q-AX-05 | 14 | 5 | 5 | 0 |
| **Total** | **76** | **25** | **25** | **0** |

Pass criterion (D-012; `collection_workflow.md` §2.1): sample ≥ 10 % per file (minimum 5) re-fetched independently of the transcription, with no field mismatch. **Met for all 5 files.**

## 4. Limitations
- The re-fetch used the **same connector** (alphaXiv) as the original transcription. It tests the transcription step (what was written into the files), not the correctness of alphaXiv's own metadata. A second, independent bibliographic source is a separate verification requirement (Q-021, Q-064, Q-068).
- Only identifier, title, year and date could be compared; author lists, venues and DOIs were never transcribed.
- 24 of 25 records were re-observed through re-run listings. The listing is not reproducible over time, so a record missing from a future re-run would not indicate an error.
- Q-AX-G9 and the 6 web files remain unchecked (see §1).

## 5. Consequences
- D-012 and D-023: the condition in `proposed_owner_responses_LIT-004.md` §11 ("recorded as approved only after the arXiv spot-check passes") is met for the 5 files named in Q-036. Recorded in `logs/DECISION_LOG.md` (Status history, 2026-10-30).
- **Recorded** in `MANIFEST.csv` on 2026-10-30 (`set-check … passed`, 5 files; dry run on a copy first showed only the target row changes). **No rebuild was run.** At the next build the 76 records read "single source: arxiv" (`partially_verified`), except possibly 2 records also retrieved by Q-WS-02/Q-WS-04 (P2870, P2941), which could become `verified` under the current two-source rule if their web members carry metadata (not checkable here: `records/publications.jsonl` is absent); Q-068 (open) questions whether a web result is an adequate second source.
- Verification status never becomes `verified` from this check alone: `verified` also needs a second agreeing source (`collection_workflow.md` §4.3).
