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
