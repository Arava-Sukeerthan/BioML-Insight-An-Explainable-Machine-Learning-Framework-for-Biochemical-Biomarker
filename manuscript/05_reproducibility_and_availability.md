# Reproducibility, data and code availability (manuscript draft section)

> **Draft, 2026-11-12.** Describes what exists in the repository now. The bracketed items are completed only when they exist; nothing is described as done before it is done.

## Data availability
- **NHANES:** the data are public and were downloaded from the CDC website. The exact files and their SHA-256 checksums are listed in the protocol (v0.1 Appendix A). No participant-level data are redistributed: derived datasets are written only to Git-ignored locations, and the build refuses any other location.
- **Literature records:**
  - **Public:** search queries, the query table, decision records and the 1,470-record screening-scope list (identifiers only).
  - **Not redistributed:** raw search exports and abstracts.

## Code availability
- **Repository:** the public repository at [URL and archived release DOI: to be added at submission; no DOI exists yet].
- **Analysis code:**
  - dataset build: `scripts/nhanes/build_dataset.py`;
  - experiment harness and metrics: `scripts/models/`;
  - literature pipeline: `scripts/literature/`.
- **Tests:** all tests use clearly labelled synthetic data or fixtures.

## Reproducibility measures
- **Fixed in advance:** the eligibility criteria, screening protocol and experimental protocol are frozen and hashed before use. The screening freeze is `criteria_v1.1+protocol_v0.2`; the experimental freeze is [pending: D-019].
- **Run records:** each experiment run appends a record containing:
  - the configuration hash and protocol version;
  - the derived seeds and the data fingerprint;
  - the Git commit and the package versions;
  - every per-seed result.
- **Data labels:** run records are labelled SYNTHETIC or REAL. Tables never mix the two labels.
- **Real-data guard:** a run on real data is refused unless:
  - it references a researcher authorisation;
  - the frozen protocol file matches the SHA-256 recorded in the configuration;
  - the Git working tree is clean.
- **Validation fingerprint:** the temporal-validation data fingerprint is recorded with every run.
- **Software environment:** the proposed pins are listed in `environment/requirements-proposed.txt`. [Installed versions: recorded at the authorised installation; pending A3.]

## Competing interests, funding, ethics
[To be completed by the researcher. NHANES is public, de-identified data; whether the target journal requires an ethics statement is checked at journal selection (D-020).]
