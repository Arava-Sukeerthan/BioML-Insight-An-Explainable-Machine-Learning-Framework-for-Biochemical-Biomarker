# Search-Accessibility Report (LIT-003)

| Field | Value |
|---|---|
| Task | LIT-003 |
| Date of attempts | 2026-10-23 (UTC 16:54–17:17) |
| Exact probe rows | `search_queries.csv`, `LIT003-PROBE-01` … `LIT003-PROBE-19` |
| Environment | Claude Code cloud container; all outbound HTTPS goes through an agent proxy with a network allow-list |

Every source was **tested**, not assumed. Blocked hosts were probed **once** each (single `curl`
request, 15–20 s timeout). They were not retried in a loop, and no attempt was made to get around the proxy.

## 1. Sources and outcomes

| Source | Endpoint / tool | Attempt | Outcome | HTTP status / actual error | Useful records? | Reproducible? |
|---|---|---|---|---|---|---|
| PubMed | PubMed connector `search_articles` | 15 planned queries + 15 check re-fetches | **Accessible** | tool JSON; `max_results` > 200 rejected ("max_results exceeds limit (max: 200)") | Yes: 3,413 hits, 2,866 unique PMIDs | Yes: `[edat]`-capped queries; PMID sets matched exactly on re-fetch |
| PubMed | PubMed connector `get_article_metadata` | 144 calls | **Accessible, with a limit** | accepts ≤ 100 PMIDs but **returns at most 20 articles per call**, silently; 200 rejected ("max: 100"); 3 transient `RATE_LIMIT_EXCEEDED` (retryAfter 2 s), retried | Yes: metadata for 2,866/2,866 PMIDs | Yes (metadata may be corrected by PubMed later) |
| PubMed E-utilities (official API) | `eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi` | 1 curl | **Blocked** | `curl: (56) CONNECT tunnel failed, response 403` (HTTP 000) | No | n/a |
| PubMed website | `pubmed.ncbi.nlm.nih.gov` | 1 curl | **Blocked** | CONNECT 403 | No | n/a |
| PMC ID converter | `www.ncbi.nlm.nih.gov/pmc/utils/idconv` | 1 curl | **Blocked** | CONNECT 403 | No | n/a |
| Europe PMC | REST `search` | 1 curl | **Blocked** | CONNECT 403 | No | n/a |
| Crossref | `api.crossref.org/works` | 1 curl | **Blocked** | CONNECT 403 | No | n/a |
| OpenAlex | `api.openalex.org/works` | 1 curl | **Blocked** | CONNECT 403 | No | n/a |
| Semantic Scholar | Graph API `paper/search` | 1 curl | **Blocked** | CONNECT 403 | No | n/a |
| arXiv API | `export.arxiv.org/api/query` | 1 curl | **Blocked** | CONNECT 403 | No | n/a |
| arXiv (via alphaXiv) | alphaXiv connector `discover_papers` | 5 planned queries | **Accessible** | tool text list (rank, arXiv ID, title, date; **no authors/venue/DOI**) | Yes: 76 records | No (relevance ranking changes over time) |
| Consensus | Consensus connector `search` | 1 query (Q-CN-01) | **Blocked (quota)** | tool error: "You've used all 30 searches this month; resets on November 1st." | No | n/a |
| DOI resolver | `doi.org/api/handles` | 1 curl | **Blocked** | CONNECT 403 | No | n/a |
| Unpaywall | `api.unpaywall.org` | 1 curl | **Blocked** | CONNECT 403 | No | n/a |
| DataCite | `api.datacite.org/dois` | 1 curl | **Blocked** | CONNECT 403 | No | n/a |
| dblp | `dblp.org/search/publ/api` | 1 curl | **Blocked** | CONNECT 403 | No | n/a |
| CORE | `api.core.ac.uk` | 1 curl | **Blocked** | CONNECT 403 | No | n/a |
| bioRxiv/medRxiv API | `api.biorxiv.org` | 1 curl | **Blocked** | CONNECT 403 | No | n/a |
| Metabolomics Workbench | REST `study` | 1 curl | **Blocked** | CONNECT 403 | No | n/a |
| MetaboLights | `www.ebi.ac.uk/metabolights/ws` | 1 curl | **Blocked** | CONNECT 403 | No | n/a |
| Publisher websites (search only) | WebSearch with `allowed_domains` | 5 queries (Q-WS-01…05) + 1 repository fallback (Q-RP-03) | **Accessible (search only)** | link lists returned; **the domain filter was not honoured** (results from ncbi.nlm.nih.gov, arxiv.org, medrxiv.org, uspto.gov) | Partly: 54 title/URL records; no authors/years | No |
| Publisher pages (reading) | WebFetch | not attempted in LIT-003 (failed in LIT-001, PROBE-10) | Not available | — | — | — |
| Google Scholar | — | not attempted (not automatable under the service's terms; LIT-001 PROBE-05/11) | Manual only | — | — | — |
| Control | `api.github.com` | 1 curl | reachable (HTTP 200) | — | — | — |

## 2. Blocked searches and unresolved access issues

| Planned search(es) | Reason not run | What would unblock it | Tracking |
|---|---|---|---|
| Q-EP-01 … Q-EP-06 (Europe PMC, incl. preprints and repository citations) | `www.ebi.ac.uk` blocked | Allow-list the host, or researcher runs the stored queries and provides exports | Q-003 |
| Q-CR-01 … Q-CR-03 (Crossref), and Crossref DOI verification | `api.crossref.org` blocked | Allow-list the host | Q-003 |
| Q-S2-01 … Q-S2-05 (Semantic Scholar) | API blocked; the proxy route (Consensus) is out of quota | Allow-list the host, or wait for Consensus quota reset (2026-11-01) | Q-003, Q-020 |
| Q-CN-01 … Q-CN-10 (Consensus) | Monthly free-tier quota used up (30/30) | Quota reset on 2026-11-01, or a paid plan (researcher decision) | Q-020 |
| Q-RP-01, Q-RP-02 (repository APIs) | Metabolomics Workbench and MetaboLights blocked | Allow-list the hosts | Q-003 |
| Q-GS-01 … Q-GS-04 (Google Scholar) | Manual-only by design | Researcher runs them (optional, ~30 min) | Q-009 |
| Official E-utilities route (`fetch_pubmed_eutils.py`) | `eutils.ncbi.nlm.nih.gov` blocked | Allow-list the host. This would remove the PMID transcription step | Q-003 |
| OpenAlex, DOI resolver, Unpaywall, DataCite, dblp, CORE, bioRxiv API (not in the original strategy; tried as possible alternatives) | Blocked | Allow-list if wanted. They would provide a second bibliographic source for verification | Q-003 |
| Second-source verification for the PubMed records | No independent bibliographic index is reachable | Crossref or Europe PMC access, or the Consensus quota | Q-021 |
| Full-text access for extraction | Pages cannot be fetched. PMC full text is reachable only through the PubMed connector (`get_full_text_article`, not used in LIT-003) | Use the connector in the extraction task; researcher provides PDFs for paywalled papers | Q-009 |

How to enable a host: the environment's network policy is changed in the cloud environment
settings (Network access → allowed domains). This is outside the assistant's control and was
not changed.

## 3. Consequences for the evidence base

- PubMed is the only complete and reproducible source in this collection. arXiv (via alphaXiv) and the web results are small, supplementary and not reproducible. Coverage of CS venues, preprints and non-MEDLINE journals is therefore **reduced**. The collection must **not** be described as comprehensive.
- Most records have only one authoritative source, so most are `partially_verified` (`verification_report.md`).
