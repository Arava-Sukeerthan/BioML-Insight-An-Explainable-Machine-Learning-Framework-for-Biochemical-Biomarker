# Environment Assessment

Assessed: 2026-10-14, prompt `P001`. All results below come from commands actually run in
this session (see `logs/session_logs/2026-10-14_P001.md`).

## Execution environment
- Managed cloud container (ephemeral). Work survives only if committed and pushed to Git.
- Linux, 4 CPU cores, 15 GiB RAM, no GPU checked/needed at this stage.
- Git available; repository was empty (no commits) on branch `claude/happy-hawking-rxptfv`.
- Python 3.13.16, pip 24.0, pandoc available. R, conda, Jupyter, LaTeX: **not installed**.

## Python packages
| Present | Missing (installable from PyPI, which is reachable) |
|---|---|
| numpy 2.5.3, pandas 3.0.5, requests 2.34.2, pypdf 6.17.0, jsonschema 4.26.0 | scipy, scikit-learn, statsmodels, matplotlib, seaborn, xgboost, lightgbm, catboost, shap, lime, mapie, optuna, imbalanced-learn, pytest, bibtexparser, PyMuPDF, pyreadstat, torch |

PyPI access confirmed by downloading a scikit-learn 1.7.2 wheel (deleted afterwards).
Nothing was installed. Package versions will be pinned in a lock file when Stage F/G begins.

## Network access from the container (HTTPS through egress proxy)
| Host | Result |
|---|---|
| pypi.org / files.pythonhosted.org | reachable |
| github.com | reachable |
| eutils.ncbi.nlm.nih.gov (PubMed E-utilities) | **blocked (403)** |
| www.ebi.ac.uk (Europe PMC) | **blocked** |
| api.crossref.org, doi.org | **blocked** |
| api.openalex.org, api.semanticscholar.org | **blocked** |
| archive.ics.uci.edu (UCI ML Repository) | **blocked** |
| wwwn.cdc.gov (NHANES) | **blocked** |
| physionet.org, zenodo.org, figshare.com, kaggle.com, huggingface.co, cran.r-project.org | **blocked** |

The server-side `WebFetch` tool also failed for eutils.ncbi.nlm.nih.gov (DNS not resolved).

## Research tools available to the assistant (via connectors)
| Tool | Status | Intended use |
|---|---|---|
| PubMed connector (search, metadata, ID conversion, full text where open) | loaded, not yet exercised | Primary biomedical literature search and PMID/DOI verification |
| Consensus connector (Semantic Scholar / OpenAlex / PubMed index) | loaded, not yet exercised | Secondary search, citation context |
| alphaXiv connector | available, not yet exercised | ML-methods literature (arXiv) |
| WebSearch | available, not yet exercised | Locating dataset documentation pages |
| maven-bio connector | **failed to connect (proxy 403)** | Not needed for this project |

"Not yet exercised" is deliberate: the literature search must not start before the search
strategy is approved.

## Limitations and consequences
1. **Reference verification**: Crossref/doi.org are blocked from scripts, so DOI verification
   must go through the PubMed connector (PMID ↔ DOI) or Consensus. Papers not indexed by either
   (e.g., some IEEE/ACM/Springer CS venues) may be hard to verify automatically and will be
   flagged `verification_status = unverified` rather than assumed correct.
2. **Dataset acquisition (Stage F)**: Candidate public sources (NHANES, UCI, PhysioNet,
   Zenodo, Kaggle) cannot be downloaded from this container under the current policy. Either
   the researcher adds those hosts to the environment's allowed domains (cloud environment
   menu → Edit → Network access; docs: https://code.claude.com/docs/en/cloud-environments#network-access),
   or the researcher downloads files and commits/uploads them with checksums. This must be
   resolved before Day 17.
3. **Ephemeral container**: uncommitted files are lost when the session ends.
4. No R/LaTeX: manuscript tooling will use pandoc/Markdown unless installed later.

## Addendum — LIT-001 (2026-10-14): research-tool capabilities verified
Details and exact probe strings: `research/literature/search_queries.csv` (PROBE-01…12).
- **PubMed connector:** works (search with total counts and query translation; metadata incl. DOI/PMCID/publication types; ID conversion; related articles; PMC full text). **Limits:** ≤ 20 boolean operators and ≤ 5 wildcards per query; `max_results` ≥ 1. The `[edat]` date-range clause is accepted.
- **Consensus connector:** works on the free tier: 10 results per search, no paging, no DOIs.
- **alphaXiv connector:** works (arXiv only; ranked; 2 searches per message).
- **WebSearch:** works, including `allowed_domains` restriction. Google Scholar pages are never returned.
- **WebFetch:** fails for every tested host (DNS not resolved): Europe PMC, Crossref, Semantic Scholar, Google Scholar, Metabolomics Workbench. Web pages cannot be read in full.
- Container `curl` additionally blocked for pubmed.ncbi.nlm.nih.gov, PMC, arXiv API, bioRxiv/medRxiv, major publishers, HMDB and MetaboLights.

## Addendum — 2026-10-29: second-source access re-check (Q-021, Q-064)
Assistant-labelled task "SECOND-SOURCE-ACCESS-RECHECK" (no researcher task ID); details in `logs/session_logs/2026-10-29_SECOND-SOURCE-ACCESS-RECHECK.md`. Everything below comes from commands actually run on 2026-10-29. Nothing was searched, downloaded, verified or rebuilt.

**Container network (curl through the session proxy, one request per host, status only, no retry as the proxy README advises for policy denials)**

| Host (endpoint) | Time (UTC) | Result |
|---|---|---|
| api.crossref.org (`/`) | 14:50:09 | **blocked**: CONNECT 403 |
| doi.org (`/`) | 14:50:09 | **blocked**: CONNECT 403 |
| www.ebi.ac.uk (`/europepmc/webservices/rest/`) | 14:50:09 | **blocked**: CONNECT 403 |
| eutils.ncbi.nlm.nih.gov (`/entrez/eutils/einfo.fcgi`) | 14:50:09 | **blocked**: CONNECT 403 |
| pubmed.ncbi.nlm.nih.gov (`/`) | 14:50:10 | **blocked**: CONNECT 403 |
| www.ncbi.nlm.nih.gov (`/pmc/`) | 14:50:10 | **blocked**: CONNECT 403 |
| api.openalex.org (`/`) | 14:50:10 | **blocked**: CONNECT 403 |
| api.semanticscholar.org (`/`) | 14:50:10 | **blocked**: CONNECT 403 |
| export.arxiv.org (`/api/query`) | 14:50:11 | **blocked**: CONNECT 403 |
| diabetesjournals.org (`/`; Q-061) | 14:50:11 | **blocked**: CONNECT 403 |

The proxy status endpoint reported the proxy enabled and not selective. Its only recent relay failures were for a connector host unrelated to this project. The 403 comes from the environment's network policy, not from TLS or the tools. The remedy is the researcher's: in the cloud environment menu (session title bar → Edit → Network access), add the hosts under Allowed domains with "Allow package managers" left ticked, or choose a broader access level (https://code.claude.com/docs/en/cloud-environments#network-access). Unchanged since 2026-10-14 (above) and 2026-10-28 (LIT-005).

**Second-source routes for the current inventory** (read-only counts from `paper_inventory.json` at `a280e01`)

| Records | Count | Route that could provide a second source | Available now? |
|---|---|---|---|
| `partially_verified`, total | 3,334 | — | — |
| PubMed records with a PMCID | 2,282 | PMC full text via the PubMed connector, named in `search_strategy.md` §7 as an example second source; whether PubMed + PMC count as two sources is Q-021/Q-064 (c) | Connector reachable (LIT-001); **not run**, as it depends on the researcher's Q-021/Q-064 decision |
| PubMed records without a PMCID (incl. A2, `P0303`) | 964 | Crossref or Europe PMC (blocked); Consensus (quota resets 2026-11-01, LIT-005); a web-search result with the same DOI/PMCID (the route used for the 14 `verified` records, see below) | No independent bibliographic index reachable |
| arXiv records (transcribed, not spot-checked) | 88 | Re-fetch spot-check through alphaXiv (D-012, Q-036) | Needs the raw exports (absent from this container) and the researcher's answer to Q-036 |

**Inconsistency found (recorded as Q-068, not resolved).** `verification_report.md` states that the 14 `verified` records used "a web-search result whose URL carried the same DOI or PMCID and whose title did not conflict" as the second source, with agreement on title and identifier only. `collection_workflow.md` §4.3 ("≥ 2 distinct sources agree") allows this. `search_strategy.md` §7 and `research_plan.md` §6 require agreement on title, first author, year, venue and identifier, and give Consensus, arXiv or PMCID full text as example second sources. Web search is not named there as a second source.

**Not done**: no Consensus call (out of quota until 2026-11-01 per LIT-005; a probe would be an unregistered search); no PubMed, PMC, alphaXiv or web-search call; no change to `verification_status`; no rebuild.
