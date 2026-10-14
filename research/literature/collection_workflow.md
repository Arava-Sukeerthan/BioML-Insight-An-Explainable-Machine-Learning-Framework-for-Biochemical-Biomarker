# Publication Collection and Verification Workflow

| Field | Value |
|---|---|
| Task | LIT-002 (Stage A → B preparation) |
| Version | 1.0 — prepared 2026-10-14 |
| Status | **Implemented and unit-tested on synthetic data only. No real publication has been collected.** |
| Code | `scripts/literature/pubrecords.py`, `scripts/literature/fetch_pubmed_eutils.py`, `scripts/literature/validate_search_queries.py` |
| Tests | `tests/literature/test_pubrecords.py` (run: `python3 -I -m unittest discover -s tests/literature -v`) |
| Schemas | `schemas/source_record.schema.json`, `schemas/publication_record.schema.json`, `schemas/paper_inventory.schema.json` |

---

## 1. Overview

```
search_queries.csv (query_id, exact string)
        │
        ▼  (A) official API: fetch_pubmed_eutils.py ──► raw XML/JSON written by the script
        ▼  (B) PubMed connector: tool output saved to a JSON file by the assistant ("transcribed")
        ▼  (C) other tools (Consensus, alphaXiv, web): structured JSON written by the assistant
raw_exports/<file>  ──register──►  raw_exports/MANIFEST.csv  (sha256, query_id, route, UTC timestamp)
        │
        ▼  pubrecords.py build   (checksums verified first; aborts on any edited raw file)
records/source_records.jsonl     one record per hit per search; source metadata kept verbatim in "original"
records/publications.jsonl       deduplicated publication records (required fields, §3)
records/publications_index.csv   same, without abstracts (committable)
records/dedup_review.csv         uncertain matches for manual decision
records/paper_id_registry.csv    append-only identifier → paper_id map (stable IDs)
records/build_report.json        counts, completeness per query, conflicts, retractions
```

Manual inputs are kept in separate files so that rebuilds never overwrite human decisions:

| File | Purpose |
|---|---|
| `records/dedup_decisions.csv` | `paper_id_a,paper_id_b,decision(same/different),reviewer,date,note` |
| `screening/decisions.csv` | `paper_id,stage(title_abstract/full_text),decision,reason_code,screener,date,justification` |
| `records/verification_overrides.csv` | `paper_id,verification_status,note,reviewer,date` |
| `records/fulltext_status.csv` | `paper_id,full_text_availability,note,date` |

## 2. Retrieval routes and access conditions

| Route | Source | Status in this environment | Access conditions respected |
|---|---|---|---|
| **A. NCBI E-utilities** (`fetch_pubmed_eutils.py`) | PubMed | **Blocked** (`eutils.ncbi.nlm.nih.gov` denied by the network policy). Tested only against a fake transport | Official API. ≤ 3 requests/s (≤ 10/s with `NCBI_API_KEY`). `tool` parameter always sent. `email` sent only if the researcher sets `NCBI_EMAIL`. esearch ≤ 10,000 IDs per query (the script stops and asks for a date split beyond that). efetch in POST batches of 200. API key and e-mail are never written to the manifest |
| **B. PubMed connector** | PubMed | **Works** (verified LIT-001) | Uses the host-provided connector as designed: no scraping, no authentication bypass |
| **C. Consensus / alphaXiv / WebSearch** | Semantic Scholar/OpenAlex/PubMed index; arXiv; publisher pages | **Work** (verified LIT-001) | Tool outputs only; publisher pages are not fetched or scraped (and cannot be). Paywalled full text is obtained only from the researcher's legitimate access |
| Europe PMC REST, Crossref REST, Semantic Scholar API, arXiv API, Metabolomics Workbench / MetaboLights APIs | — | **Blocked** | Not implemented. A client is only worth writing once the host is enabled (§6) |
| Google Scholar | — | Not accessible; automated querying is not permitted by the service | Manual, researcher-run only (`Q-GS-*`) |

### 2.1 The transcription problem (routes B and C)
Connector and tool responses reach the assistant, not the file system. To keep them, the
assistant must write them into files. That is a **transcription step**, and it can introduce
errors. Controls:
1. Files are registered with `--transcribed`. Every derived record carries `transcribed: true`.
2. **Spot-check.** For each transcribed metadata file, an independent re-fetch of a random
   sample of PMIDs is saved and registered. `pubrecords.py spot-check ORIGINAL REFETCH` compares
   title, year, journal, DOI, PMCID, author surnames and abstract (normalised), and records
   `passed`/`failed` in the manifest. Sample size: ≥ 10 % of PMIDs per file, minimum 5, with the
   seed recorded.
3. A publication whose only authoritative source is transcribed and not yet spot-checked is capped at
   `partially_verified`.
4. Volume and cost. The 15 PubMed queries total about 3,400 hits before deduplication. Transcribing
   that many abstracts is slow and error-prone. **Route A is strongly preferred**; it needs one
   host to be allow-listed (Q-003).

## 3. Publication record (required fields → implementation)

| Required field | Field in `publications.jsonl` | Notes |
|---|---|---|
| Internal paper ID | `paper_id` | `P0001…`; stable across rebuilds via the append-only registry |
| Title | `title` | From the highest-priority source (`field_provenance.title` says which). Markup stripped. Other sources' values kept in `metadata_conflicts` when they differ |
| Authors | `authors` | List of `{last_name, fore_name, initials}` or `{collective_name}` |
| Year | `year` | Publication year (PubDate Year, MedlineDate, or ArticleDate fallback) |
| Journal | `journal` | Full journal title where available |
| DOI | `doi` | Lower-case, resolver prefix removed |
| PMID | `pmid` | |
| Source database | `source_databases` | All sources that returned the record, in priority order |
| Source URL | `source_urls` | e.g., `https://pubmed.ncbi.nlm.nih.gov/<PMID>/` and tool-provided URLs |
| Abstract | `abstract` | Structured abstracts flattened as `LABEL: text` |
| Search query | `search_provenance[].query_id`, `.query_string` | Every search that returned the record, with its rank |
| Search date | `search_provenance[].search_timestamp` | UTC timestamp of the API or tool call |
| Duplicate status | `duplicate_status`, `n_source_records`, `possible_duplicates` | `unique` / `merged_duplicates` / `possible_duplicate_review` |
| Verification status | `verification_status`, `verification_note` | §4.3 |
| Full-text availability | `full_text_availability` | Auto: `pmc_record` (has PMCID), `arxiv_preprint`, else `not_checked`; manual updates via `fulltext_status.csv` |
| Screening decision | `screening_decision`, `screening_stage` | `not_screened` until `screening/decisions.csv` has an entry |
| Exclusion reason | `exclusion_reason` | Codes E1–E12 from `screening_criteria.md` |
| (additional) | `pmcid`, `arxiv_id`, `publication_types`, `language`, `retracted`, `metadata_conflicts`, `field_provenance`, `primary_source_record_id` | |

## 4. Processing rules

### 4.1 Normalisation (matching keys only; originals are kept)
* DOI: lower-case; `https://doi.org/`, `dx.doi.org`, `doi:` prefixes and a trailing period removed. Must match `10.NNNN/…`.
* PMID: digits only, no leading zero. PMCID: `PMC` + digits. arXiv ID: version suffix and URL prefix removed.
* Title: HTML removed, Unicode NFKD, diacritics dropped, lower-case, punctuation → space.

### 4.2 Deduplication
| Step | Rule | Action |
|---|---|---|
| 1 | Same PMID, DOI, PMCID or arXiv ID | Merge, **unless** the two clusters carry different values of the same identifier type (e.g., same PMID but different DOIs) |
| 1a | Identifier conflict | **Not merged**; flagged `identifier_conflict:<field>`; never given the same paper ID |
| 2 | Researcher decision `same` in `dedup_decisions.csv` | Merge |
| 3 | Identical normalised title (≥ 20 characters) + same year + same first-author surname (or one missing) | Merge |
| 3a | Identical title, year differs by 1 (typical preprint/epub vs issue year) | Flag `same_title_year_differs_by_1` |
| 3b | Identical title, other differences | Flag `same_title_other_differences` |
| 4 | Title similarity ≥ 0.90 (difflib ratio) within a first-author block | Flag `fuzzy_title` (never merged automatically) |
| — | Researcher decision `different` | Suppresses the flag in later builds |

Merged records keep **all** source records. Bibliographic fields come from the highest-priority
source (PubMed > Europe PMC > Crossref > arXiv > Semantic Scholar > Consensus > others). Within a source the order is E-utilities > connector >
transcription. Empty fields are filled from the next source and the provenance is recorded.
Disagreeing values of title, year, journal, DOI, PMID, PMCID or arXiv ID are listed in
`metadata_conflicts`. Nothing is silently overwritten.

Fuzzy matching uses cheap filters first (length ratio, word overlap ≥ 0.5, quick ratio). A
benchmark on 3,405 synthetic records with deliberately large author blocks ran in 1.6 s and
found all 5 planted near-duplicates. A theoretical recall limit remains: pairs that reach the
0.90 character similarity but share fewer than half their words are not compared. This is
judged very unlikely for titles.

### 4.3 Automatic verification status (`search_strategy.md` §7)
| Status | Rule |
|---|---|
| `needs_review` | Conflicting title, year, DOI or PMID among merged sources |
| `verified` | ≥ 2 distinct sources agree, ≥ 1 is an authoritative index (PubMed, Europe PMC, Crossref, arXiv) with a persistent identifier, and that authoritative record is either script-retrieved or transcription spot-check `passed` |
| `partially_verified` | One authoritative source only, or the authoritative record is transcribed and not yet spot-checked |
| `unverified` | No authoritative record with a persistent identifier (e.g., Consensus- or web-only), or no metadata |
| `failed` | Manual only, via `verification_overrides.csv` |

`verified` here means that the bibliographic metadata is confirmed. It says nothing about the
paper's scientific content. Claims extracted from a paper are checked separately against its
full text.

### 4.4 Completeness and retractions
`build_report.json → search_completeness` compares, for each query, the total reported by
PubMed with the number of unique PMIDs actually retrieved. Any query with
`complete: false` must be finished before screening. Records with publication type
*Retracted Publication* are flagged (`retracted: true`) for exclusion code E7.

## 5. Operating procedure (for LIT-003 onwards; not yet executed)

**Route A (if `eutils.ncbi.nlm.nih.gov` is enabled):**
```
python3 -I scripts/literature/fetch_pubmed_eutils.py Q-PM-01 --dry-run         # check substituted query
python3 -I scripts/literature/fetch_pubmed_eutils.py Q-PM-01 --run-date 2026-10-16
python3 -I scripts/literature/pubrecords.py build
```

**Route B (connector):**
1. `search_articles` with the stored query (date substituted), `max_results` and `retstart` to page
   through all hits. Save each page verbatim as `raw_exports/<QID>_<date>_search_<k>.json` in the
   form `{"provenance": {...}, "response": <tool JSON>}`.
2. Register each file:
   ```
   python3 -I scripts/literature/pubrecords.py register <file> --query-id Q-PM-01 --source pubmed \
       --route pubmed_connector_search --endpoint-or-tool "PubMed connector search_articles" \
       --request-json '{"retstart": 0, "max_results": 200}' --retrieved-at <UTC ISO> --n-items <n> --transcribed
   ```
3. `get_article_metadata` for the union of PMIDs in batches. Save as `META_<date>_<k>.json` and
   register with route `pubmed_connector_metadata` and `--query-id META`.
4. Spot-check each metadata file (§2.1), then run `build`.

**Route C (Consensus / alphaXiv / web):** write `{"provenance": {...}, "response": {"records": [...]}}`
with the fields `title, authors, year, journal, doi, pmid, pmcid, arxiv_id, url, abstract`, using
only what the tool returned. Register with route `structured_transcription`.

After every build: run `pubrecords.py verify`, review `dedup_review.csv`, record decisions, and log the
run in `logs/EXPERIMENT_LOG.md`.

## 6. Unavailable databases and accessible alternatives

| Unavailable | Purpose in strategy | Accessible alternative now | Better option (needs host allow-listing) |
|---|---|---|---|
| PubMed E-utilities (direct) | Script-based reproducible retrieval | PubMed connector (route B) with transcription spot-checks | Allow `eutils.ncbi.nlm.nih.gov` → route A (implemented) |
| Europe PMC | Preprints, full-text search for repository citations | PubMed (`Q-PM-15`); arXiv via alphaXiv for ML preprints. medRxiv/bioRxiv coverage remains a gap | Allow `www.ebi.ac.uk` and add a small Europe PMC client |
| Crossref | DOI/metadata verification of non-PubMed records | arXiv metadata via alphaXiv; PubMed `convert_article_ids` for PubMed-indexed DOIs; Consensus records as a second source | Allow `api.crossref.org` |
| Semantic Scholar | CS-venue coverage | Consensus connector (top-10 per query); alphaXiv | Allow `api.semanticscholar.org` |
| Google Scholar | Grey/CS literature | Optional manual searches by the researcher | Not automatable (service terms) |
| Metabolomics Workbench / MetaboLights | Repository-linked publications | `Q-PM-15` (PubMed) and `Q-RP-03` (web search) | Allow `www.metabolomicsworkbench.org`, `www.ebi.ac.uk` |

## 7. What is committed to Git (repository is **public**)
PubMed abstracts may be under publisher copyright, and the GitHub repository is public
(checked 2026-10-14). Proposed default (decision D-010):
* **Committed:** `raw_exports/MANIFEST.csv` (checksums, timestamps, queries),
  `records/publications_index.csv` (no abstracts), `records/paper_id_registry.csv`,
  `records/dedup_review.csv`, `records/dedup_decisions.csv`, `records/build_report.json`,
  screening decision files.
* **Not committed** (`.gitignore`): raw tool and API responses, `source_records.jsonl` and
  `publications.jsonl`. These are regenerated from the raw files; the raw files can be re-obtained
  with the snapshot-capped queries.
* **Consequence:** the container is ephemeral, so uncommitted raw files are lost when a session ends.
  Options: (a) make the repository private and commit everything; (b) store the raw files in private
  storage the researcher controls; (c) accept re-fetching. Researcher decision: Q-011.

## 8. Test coverage (LIT-002, 2026-10-14)

**Tested (19 unit tests, all passing, synthetic fixtures only):**
* Normalisation of DOI, PMID, PMCID, arXiv ID and titles.
* Parsing of the PubMed-connector metadata structure (field layout taken from a real response
  observed in LIT-001; fixture values synthetic).
* Parsing of E-utilities efetch XML: structured abstract, MedlineDate, ELocationID DOI, collective
  author, retraction type. The fixture follows the documented PubMed XML element names and is
  synthetic.
* Manifest registration, refusal to re-register, and checksum detection of an edited raw file
  (the build aborts).
* End-to-end build:
  - search hits joined to metadata;
  - merging by PMID across queries, and by DOI variant across sources;
  - preservation of a journal conflict;
  - year-differs and fuzzy-title flags;
  - an identifier conflict that is never merged and never shares a paper ID;
  - search-completeness detection;
  - schema validation of every output record.
* Paper-ID stability after new data arrive; manual dedup decisions (`same`/`different`) and
  screening decisions surviving rebuilds.
* Transcription spot-check: a planted title discrepancy is detected and recorded as `failed`; a
  `passed` check upgrades verification to `verified`.
* E-utilities client against a fake transport:
  - `{RUN_DATE}` substitution;
  - `tool` parameter sent;
  - raw files written and registered;
  - credentials kept out of the manifest;
  - refusal to overwrite existing exports;
  - refusal to run a non-PubMed query.
* The project's real `search_queries.csv` still validates. A dry run of `Q-PM-01` substitutes the
  run date.
* Dedup speed on 3,405 synthetic records (manual benchmark, not part of the suite): 1.6 s.

**Not tested:**
* Any live API call (E-utilities is blocked). Real E-utilities responses may differ from the
  documented format in edge cases (e.g., `<sup>` markup, `Year` absent, book articles).
* Real PubMed-connector pagination at scale, and the actual transcription error rate.
* Real Consensus/alphaXiv transcriptions.
* Deduplication quality on real data (precision/recall of flags). This will be measured on the
  first real build through the manual review of `dedup_review.csv`.
* Europe PMC, Crossref, Semantic Scholar and repository routes (not implemented).
