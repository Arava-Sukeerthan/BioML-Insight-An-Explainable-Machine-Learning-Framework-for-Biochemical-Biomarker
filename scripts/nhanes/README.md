# scripts/nhanes/: descriptive NHANES counts

`descriptive_counts.py` reproduces the **aggregate descriptive counts** quoted in
`research/methodology/experimental_protocol_v0.1_draft.md`. Added in PROTOCOL-DRAFT-003 (2026-10-24).

| Draft section | Content |
|---|---|
| §4 | Eligibility cascade |
| §5.2, §5.3 | Outcome and sensitivity-label counts, discordance |
| §6.2 | Complete cases per predictor group |
| §6.4 | Analytic-sample medians |
| §8.1 | Unit-consistency arithmetic |
| §10 | Survey design clusters |
| §19 | S-07 drug-name count |

**This is not modelling.** The script computes counts, proportions, medians and fixed published-equation arithmetic. It trains, fits, tunes and evaluates no model and produces no predictions. It prints aggregate values only; it never prints or writes participant identifiers or participant-level rows. The protocol is a draft and inactive; running this script does not activate it.

## Inputs (not in Git)
32 official CDC NHANES public-use XPT files, 16 components × 2 periods:
- **Components:** DEMO, DIQ, GHB, GLU, FASTQX, INS, TCHOL, HDL, TRIGLY, BIOPRO, CBC, HSCRP, ALB_CR, BMX, BPXO, RXQ_RX.
- **Locations:**
  - `data/raw/nhanes/2017-2020/P_<COMPONENT>.xpt`, from `https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_<COMPONENT>.xpt`;
  - `data/raw/nhanes/2021-2023/<COMPONENT>_L.xpt`, from `https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/<COMPONENT>_L.xpt`.
- **Not in Git:** `data/raw/` is git-ignored; raw files are never committed (public repository).
- **Hash check:** the script compares every file with the SHA-256 values recorded on 2026-10-24 (also in protocol draft Appendix A). It stops, without producing counts, if a file is missing or differs. CDC can revise files; a mismatch means the recorded counts may not apply.

## Run (from the repository root)
```
python3 -I scripts/nhanes/descriptive_counts.py                 # prints JSON to stdout
python3 -I scripts/nhanes/descriptive_counts.py --json outputs/aggregate/descriptive_counts.json
```
- Tested 2026-10-24 with Python 3.13, pandas 3.0.5 and numpy 2.5.3 (no other packages).
- The optional JSON file contains aggregates only. `outputs/aggregate/` is the committed aggregate location (`outputs/README.md`), but writing there does not commit anything.
- Small cells (for example the S-07 count of 15) are aggregate but should be reviewed before publication.

## Verification on 2026-10-24
All 85 compared values matched the protocol draft except one. Draft v0.1 gave median FPG as "103 vs 101 mg/dL" in the analytic-sample context; those are the medians of the broader reference population that this script also reports (`reference_adults18_fasting`). The analytic-sample medians are 101 and 100 mg/dL. Draft revision 2 corrects the sentence.

## Provenance
The script consolidates the session-scratchpad scripts used on 2026-10-24: `feasibility_counts.py`, `group_counts.py` / `group_counts_nocrp.py`, `outcome_variants.py`, `sanity.py` and `unit_checks.py`. Selection rules and arithmetic are unchanged. The originals were not committed. The original scripts produced the protocol figures (re-run in the pre-commit review of 2026-10-24); this script's output was compared with those figures value by value (85 values; one wording discrepancy, above).
