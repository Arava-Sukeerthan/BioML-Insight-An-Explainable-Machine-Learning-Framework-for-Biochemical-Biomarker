#!/usr/bin/env python3
"""Reproduce the AGGREGATE descriptive counts reported in the protocol draft.

Draft: research/methodology/experimental_protocol_v0.1_draft.md (§4, §5.2, §5.3, §6.2, §8.1, §10,
§19 S-07). Added in PROTOCOL-DRAFT-003 (2026-10-24). It consolidates the session-scratchpad scripts
used on 2026-10-24: feasibility_counts.py, group_counts.py / group_counts_nocrp.py,
outcome_variants.py, sanity.py and unit_checks.py. Selection rules and arithmetic are unchanged.

WHAT THIS IS
- Descriptive counts, proportions, medians and fixed-equation arithmetic on the verified public
  NHANES files.
- It does NOT train, fit, tune or evaluate any model, and it produces no prediction.
- It prints aggregate values only (and optionally writes them to a JSON file). It never prints or
  writes a participant identifier or a participant-level row.

INPUTS
32 official NHANES XPT files in the git-ignored folders data/raw/nhanes/{2017-2020,2021-2023}/.
Each file is checked against the SHA-256 values below (protocol draft Appendix A) before use; any
missing file or mismatch stops the script. See scripts/nhanes/README.md for how to obtain the files.

USAGE (from the repository root)
    python3 -I scripts/nhanes/descriptive_counts.py
    python3 -I scripts/nhanes/descriptive_counts.py --json outputs/aggregate/descriptive_counts.json
"""
import argparse
import hashlib
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
RAW = REPO / "data" / "raw" / "nhanes"

# SHA-256 of the official files downloaded 2026-10-24 (protocol draft Appendix A).
EXPECTED_SHA256 = {
    "2017-2020/P_DEMO": "2e46c6c26bf77cd8989f64011ace12cbf42c0f3e03414eb59acc5328c8f87913",
    "2021-2023/DEMO_L": "ca4374a158b493b8b0163e1388da21d57a18d1b9cecff2aa4e2fa2bec494fe23",
    "2017-2020/P_DIQ": "79153f799fc2171792771c4aa250029c62807f14915f1f81405b03233b1e5ae3",
    "2021-2023/DIQ_L": "9535a023673ae869afae19d842d8679e06f6a464606ac15900686b41ef05090f",
    "2017-2020/P_GHB": "dac9e423f56041c2ec46486cb16be16d3347e0a81a575985882ffad5a60e1195",
    "2021-2023/GHB_L": "67aee0353160e2392dc0a33bece99b90764a630c76d82415ac4639105ad9dd03",
    "2017-2020/P_GLU": "91b83c46fb4707c431838159135e93693a0572bce54074f5a890f0ee104732b3",
    "2021-2023/GLU_L": "70f773ab37e3d8485341f32137e280e05b9279e5fe9b6f0362e4052d8fe9a201",
    "2017-2020/P_FASTQX": "2ff1a59eae3b7564373d61abecd585c4d7c39e1ad6826403775bd94def3ce6d1",
    "2021-2023/FASTQX_L": "e687d7ed729e81b256dbf911c9737883d948c1441079b012741d8ea3b115be6b",
    "2017-2020/P_INS": "00b2cebd564df7038451d297df1a1d11e8e69a9443eee16770c24cc2ce3471da",
    "2021-2023/INS_L": "cdbf53b644805e5e67725c81ee32048dad3c06687689435b042a7a144cb9ec65",
    "2017-2020/P_TCHOL": "759cd9c408b5d1b91f6cfb5d5e67920a301f7478c0e90ce7adf4bbd277a45ac8",
    "2021-2023/TCHOL_L": "5c3312e555bb0706fd97cbd63fcbc9e78f00bda8d2d149732d9dd368169b25d3",
    "2017-2020/P_HDL": "04a344f00fe34b3dc4202ee9e47cf61e67d1f985d7c9ece228e25caa85c7fbd7",
    "2021-2023/HDL_L": "c1bb43df5ca366f470b411c043f4aee7ae6552a7f4bca1178bc87b24fb9a7300",
    "2017-2020/P_TRIGLY": "d3eb2df386f24a559ae4db992f0ec9aaf3d2c0caec173aa1921e78100ee88b31",
    "2021-2023/TRIGLY_L": "77679864c33b98d9b6db528f3a0ac0a15ea34bde9731c04d23bc9801277975f4",
    "2017-2020/P_BIOPRO": "f242cb9f9da5787f77d81ffb02822350e01cea4adf072d23bc96eb008182010c",
    "2021-2023/BIOPRO_L": "912b345aad6b71d53a3bc299a7f3bb0d5530e9fa5b6e76d2d00103979861a476",
    "2017-2020/P_CBC": "8a910eacc0fad8d3b817bb01699c5d90761c60be3b2daaaf025396b58de96ef8",
    "2021-2023/CBC_L": "4405da2a5899dcd11e3ef4dbec0b4d2fca6d736a3efa7a85afee668baa95923f",
    "2017-2020/P_HSCRP": "e6954d17afa70755c26004bda6d4f0b256a5f30b0620cb70fdd6f520147218e1",
    "2021-2023/HSCRP_L": "c56098d7c33509087a4645dfdf39936c14213d9123e1e718831a10d5bc4e3a1b",
    "2017-2020/P_ALB_CR": "c493f6b74cc0608bb7083b92e074fc3070b9e614fd5e1e34d0ce943e0f6116bf",
    "2021-2023/ALB_CR_L": "fc011a80d14419884559372a3196f0a268b494f4f2fa972d00be1f3a23ba3c41",
    "2017-2020/P_BMX": "7038d0da3169420a4a3cbaec09ac586a701b38e1c7b925431b60e13ac24fed66",
    "2021-2023/BMX_L": "44440c416d9ad709e8b1708a5975378ab4d5b18edc39eb5015c2ae7186500170",
    "2017-2020/P_BPXO": "5edbcb81e99fe8dad38deb8b642570278b200c525d88ffa29ae3ceb4dd38bde4",
    "2021-2023/BPXO_L": "189aa9bed689d2c69cf8d780b01de85073276fea5694dd52cdf696229f9054a6",
    "2017-2020/P_RXQ_RX": "0ee30345ccfee5ce0ff55e51fca4dec7389d3a8e985c59485d13400e9ec2ee2e",
    "2021-2023/RXQ_RX_L": "b801ca006aa8b505f597c4b28221e6f8c8b033781f214c16d45a114c5b564211",
}

PERIODS = {
    "2017-2020": dict(name=lambda c: "P_" + c, fw="WTSAFPRP", tg="LBXTR", ses="PHDSESN"),
    "2021-2023": dict(name=lambda c: c + "_L", fw="WTSAF2YR", tg="LBXTLG", ses="PHDSESNZ"),
}

# Candidate predictor group A (protocol §6.1, revision 1: hs-CRP excluded) and group C.
GROUP_A = {"BIOPRO": ["LBXSATSI", "LBXSASSI", "LBXSGTSI", "LBXSAPSI", "LBXSAL", "LBXSTP", "LBXSTB",
                      "LBXSCR", "LBXSBU", "LBXSUA"],
           "TCHOL": ["LBXTC"], "HDL": ["LBDHDD"], "TRIGLY": ["<tg>"],
           "CBC": ["LBXWBCSI", "LBDNENO", "LBDLYMNO", "LBXHGB", "LBXMCVSI", "LBXRDW", "LBXPLTSI"],
           "ALB_CR": ["URDACT"]}
GROUP_C = ["RIDAGEYR", "RIAGENDR", "BMXBMI", "BMXWAIST", "SBP", "DBP"]
# Per-variable missingness list used in the 2026-10-24 feasibility check (includes insulin and
# hs-CRP for completeness; neither is in the primary groups).
MISSINGNESS_VARS = {"BIOPRO": ["LBXSATSI", "LBXSASSI", "LBXSGTSI", "LBXSAPSI", "LBXSAL", "LBXSTP",
                               "LBXSTB", "LBXSCR", "LBXSBU", "LBXSUA"],
                    "TCHOL": ["LBXTC"], "HDL": ["LBDHDD"], "TRIGLY": ["<tg>"], "INS": ["LBXIN"],
                    "CBC": ["LBXWBCSI", "LBXHGB", "LBXPLTSI", "LBXNEPCT", "LBXLYPCT"],
                    "HSCRP": ["LBXHSCRP"], "ALB_CR": ["URDACT"], "BMX": ["BMXBMI", "BMXWAIST"],
                    "BPXO": ["BPXOSY1", "BPXODI1"]}
# Fixed drug-name list used for sensitivity S-07 on 2026-10-24 (Q-057: list not yet approved).
GLUCOSE_LOWERING = ["METFORMIN", "GLIPIZIDE", "GLIMEPIRIDE", "GLYBURIDE", "SITAGLIPTIN",
                    "LINAGLIPTIN", "SAXAGLIPTIN", "ALOGLIPTIN", "PIOGLITAZONE", "ROSIGLITAZONE",
                    "CANAGLIFLOZIN", "DAPAGLIFLOZIN", "EMPAGLIFLOZIN", "ERTUGLIFLOZIN", "LIRAGLUTIDE",
                    "SEMAGLUTIDE", "DULAGLUTIDE", "EXENATIDE", "TIRZEPATIDE", "INSULIN", "ACARBOSE",
                    "REPAGLINIDE", "NATEGLINIDE"]


def verify_inputs():
    problems = []
    for key, expected in EXPECTED_SHA256.items():
        path = RAW / (key + ".xpt")
        if not path.is_file():
            problems.append(f"missing: {path.relative_to(REPO)}")
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            problems.append(f"SHA-256 mismatch: {path.relative_to(REPO)}")
    if problems:
        sys.exit("Input check failed (no counts produced):\n  " + "\n  ".join(problems))


def read(period, component):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        df = pd.read_sas(RAW / period / (PERIODS[period]["name"](component) + ".xpt"), format="xport")
    num = df.select_dtypes("number").columns
    df[num] = df[num].mask(df[num].abs() < 1e-70, 0.0)  # SAS XPORT stores 0 as ~5.4e-79
    return df


def pct(x):
    return round(float(x) * 100, 1)


def period_counts(period):
    c = PERIODS[period]
    fw, tg, ses = c["fw"], c["tg"], c["ses"]
    get = lambda comp: read(period, comp)
    d = (get("DEMO")
         .merge(get("DIQ")[["SEQN", "DIQ010", "DIQ160", "DIQ050", "DIQ070"]], on="SEQN", how="left")
         .merge(get("GHB")[["SEQN", "LBXGH"]], on="SEQN", how="left")
         .merge(get("GLU")[["SEQN", fw, "LBXGLU"]], on="SEQN", how="left", indicator="in_glu")
         .merge(get("FASTQX")[["SEQN", "PHAFSTHR", "PHAFSTMN", ses]], on="SEQN", how="left"))
    out = {"cascade": {}}
    cas = out["cascade"]
    m = pd.Series(True, index=d.index); cas["E0_all_participants"] = int(m.sum())
    m &= d.RIDSTATR == 2; cas["E1_mec_examined"] = int(m.sum())
    cas["E2_alt_age_ge_18"] = int((m & (d.RIDAGEYR >= 18)).sum())
    m &= d.RIDAGEYR >= 20; cas["E2_age_ge_20"] = int(m.sum())
    m &= d.in_glu == "both"; cas["E3_in_fasting_glucose_file"] = int(m.sum())
    out["session_codes_E3"] = {str(k): int(v) for k, v in d.loc[m, ses].value_counts(dropna=False).items()}
    m &= d[fw] > 0; cas["E4_fasting_weight_gt_0"] = int(m.sum())
    hours = (d.PHAFSTHR + d.PHAFSTMN / 60)[m]
    out["fasting_hours_E4"] = {"min": round(float(hours.min()), 2), "max": round(float(hours.max()), 2)}
    m &= d.LBXGLU.notna(); cas["E5a_valid_fpg"] = int(m.sum())
    m &= d.LBXGH.notna(); cas["E5_valid_fpg_and_hba1c"] = int(m.sum())
    cas["E6_excluded_pregnant"] = int((m & (d.RIDEXPRG == 1)).sum())
    m &= ~(d.RIDEXPRG == 1); cas["E6_not_pregnant"] = int(m.sum())
    cas["E7_excluded_diagnosed"] = int((m & (d.DIQ010 == 1)).sum())
    cas["E7_excluded_refused_dk_missing"] = int((m & (d.DIQ010.isin([7, 9]) | d.DIQ010.isna())).sum())
    m &= d.DIQ010.isin([2, 3]); cas["E7_no_diagnosed_diabetes"] = int(m.sum())
    cas["E8_excluded_diabetes_pills"] = int((m & (d.DIQ070 == 1)).sum())
    m &= ~(d.DIQ070 == 1); cas["E8_analytic_N"] = int(m.sum())

    a = d[m].copy()
    w = a[fw]
    h, g = a.LBXGH >= 5.7, a.LBXGLU >= 100
    outcomes = {
        "primary_hba1c57_or_fpg100": h | g,
        "S-01_hba1c57": h,
        "S-03_hba1c57_or_fpg110": h | (a.LBXGLU >= 110),
        "S-15a_both_discordant_negative": h & g,
    }
    out["outcomes"] = {k: {"positive": int(y.sum()), "pct_unweighted": pct(y.mean()),
                           "pct_fasting_weighted": pct(np.average(y, weights=w))}
                       for k, y in outcomes.items()}
    conc = (h & g) | (~h & ~g)
    out["outcomes"]["S-15b_both_discordant_excluded"] = {
        "N": int(conc.sum()), "positive": int((h & g).sum()), "pct_unweighted": pct((h & g)[conc].mean())}
    out["discordance"] = {"hba1c_only": int((h & ~g).sum()), "fpg_only": int((~h & g).sum()),
                          "both": int((h & g).sum()), "neither": int((~h & ~g).sum())}
    out["fpg_100_109_and_hba1c_lt_57"] = int(((a.LBXGLU >= 100) & (a.LBXGLU < 110) & ~h).sum())
    out["undiagnosed_diabetes_range"] = int(((a.LBXGH >= 6.5) | (a.LBXGLU >= 126)).sum())
    out["borderline_DIQ010_3_retained"] = int((a.DIQ010 == 3).sum())
    out["told_prediabetes_DIQ160_1_retained"] = int((a.DIQ160 == 1).sum())
    out["S-04_remaining_N"] = int((~((a.DIQ160 == 1) | (a.DIQ010 == 3))).sum())
    out["median_fpg_analytic_sample"] = float(a.LBXGLU.median())
    out["median_hba1c_analytic_sample"] = float(a.LBXGH.median())

    # Complete cases per candidate predictor group (protocol §6.2).
    feats = a[["SEQN", "RIDAGEYR", "RIAGENDR", "SDMVSTRA", "SDMVPSU"]]
    for comp, vs in GROUP_A.items():
        vs = [tg if v == "<tg>" else v for v in vs]
        feats = feats.merge(get(comp)[["SEQN"] + vs], on="SEQN", how="left")
    feats = feats.merge(get("BMX")[["SEQN", "BMXBMI", "BMXWAIST"]], on="SEQN", how="left")
    bp = get("BPXO")
    bp["SBP"] = bp[["BPXOSY1", "BPXOSY2", "BPXOSY3"]].mean(axis=1)
    bp["DBP"] = bp[["BPXODI1", "BPXODI2", "BPXODI3"]].mean(axis=1)
    feats = feats.merge(bp[["SEQN", "SBP", "DBP"]], on="SEQN", how="left")
    ga = [tg if v == "<tg>" else v for vs in GROUP_A.values() for v in vs]
    crp = feats[["SEQN"]].merge(get("HSCRP")[["SEQN", "LBXHSCRP"]], on="SEQN", how="left")["LBXHSCRP"]
    out["complete_cases"] = {
        "A_21": int(feats[ga].notna().all(axis=1).sum()),
        "C_6": int(feats[GROUP_C].notna().all(axis=1).sum()),
        "B_27": int(feats[ga + GROUP_C].notna().all(axis=1).sum()),
        "v0.1_A_22_with_hscrp": int((feats[ga].notna().all(axis=1) & crp.notna().values).sum()),
        "v0.1_B_28_with_hscrp": int((feats[ga + GROUP_C].notna().all(axis=1) & crp.notna().values).sum()),
    }
    clusters = feats.groupby(["SDMVSTRA", "SDMVPSU"]).size()
    out["design_clusters"] = {"strata": int(feats.SDMVSTRA.nunique()), "stratum_x_psu": int(len(clusters)),
                              "min_size": int(clusters.min()), "median_size": int(clusters.median())}

    # Per-variable missingness in the analytic sample (feasibility list, 2026-10-24).
    mv = a[["SEQN"]]
    for comp, vs in MISSINGNESS_VARS.items():
        vs = [tg if v == "<tg>" else v for v in vs]
        mv = mv.merge(get(comp)[["SEQN"] + vs], on="SEQN", how="left")
    out["pct_missing"] = {k: pct(v) for k, v in mv.drop(columns="SEQN").isna().mean().items()}

    # Broader reference population used by the 2026-10-24 sanity check: adults >= 18 in the fasting
    # subsample with valid FPG and HbA1c, not pregnant (diagnosed diabetes NOT excluded).
    s = d[(d.RIDAGEYR >= 18) & (d[fw] > 0) & d.LBXGLU.notna() & d.LBXGH.notna() & (d.RIDEXPRG != 1)]
    out["reference_adults18_fasting"] = {"N": int(len(s)), "median_fpg": float(s.LBXGLU.median()),
                                         "median_hba1c": float(s.LBXGH.median())}

    if period == "2017-2020":  # S-07: drug names exist only in 2017-March 2020 (RXQ_RX_L has none)
        rx = get("RXQ_RX")
        names = rx.RXDDRUG.apply(lambda x: x.decode("latin1") if isinstance(x, bytes) else str(x)).str.upper()
        hit = names.str.contains("|".join(GLUCOSE_LOWERING), regex=True)
        k = a.SEQN.isin(rx.loc[hit, "SEQN"].unique())
        found = sorted({n for n in names[hit & rx.SEQN.isin(a.SEQN[k])]
                        for g_ in GLUCOSE_LOWERING if g_ in n})
        out["S-07_glucose_lowering_drug_name"] = {"participants": int(k.sum()),
                                                  "of_whom_positive_primary": int((h | g)[k].sum()),
                                                  "drug_names_found": found}
    return out


def unit_checks():
    """Protocol §8.1 descriptive unit-consistency checks. Fixed published equations, no fitting.
    These numbers are supporting only and are NOT used to decide units (protocol §6.4, §8)."""
    a = read("2017-2020", "TRIGLY").merge(read("2017-2020", "BIOPRO")[["SEQN", "LBXSTR"]], on="SEQN") \
        .dropna(subset=["LBXTR", "LBXSTR"])
    b = read("2021-2023", "TRIGLY").merge(read("2021-2023", "BIOPRO")[["SEQN", "LBXSTR"]], on="SEQN") \
        .dropna(subset=["LBXTLG", "LBXSTR"])
    str6000 = -0.8463 + 0.9879 * b.LBXSTR  # BIOPRO_L backward equation for LBXSTR
    tg = {"median_2017_LBXTR_minus_LBXSTR": round(float((a.LBXTR - a.LBXSTR).median()), 2),
          "median_2021_LBXTLG_minus_LBXSTR6000": round(float((b.LBXTLG - str6000).median()), 2),
          "median_2021_backward_mgdl_minus_LBXSTR6000":
              round(float((-12.19 + 0.9785 * b.LBXTLG - str6000).median()), 2),
          "median_2021_backward_intercept_div10_minus_LBXSTR6000":
              round(float((-1.219 + 0.9785 * b.LBXTLG - str6000).median()), 2)}
    c = read("2017-2020", "HSCRP").LBXHSCRP.dropna()
    c = c[c > 0]
    crp = {}
    for label, x in [("as_stored", c), ("divided_by_10", c / 10)]:
        y = -0.08653 + 0.9672 * x
        ok = y > 0
        r = (x[ok] - y[ok]) / y[ok]
        crp[label] = {"mean_pct": pct(r.mean()), "median_pct": pct(r.median()),
                      "pct_nonpositive_prediction": pct((~ok).mean())}
    u = read("2017-2020", "ALB_CR").URXUMS.dropna()
    u = u[u > 0]
    r = (1.381 + 0.8407 * u - u) / u
    alb = {"mean_pct": pct(r.mean()), "median_pct": pct(r.median())}
    return {"triglycerides": tg, "hscrp_NOT_APPLIED": crp, "urine_albumin": alb}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", help="also write the aggregate results to this JSON file")
    args = ap.parse_args()
    verify_inputs()
    result = {"note": "Aggregate descriptive counts only; no model was trained or evaluated.",
              "inputs_verified": len(EXPECTED_SHA256),
              "periods": {p: period_counts(p) for p in PERIODS},
              "unit_checks": unit_checks()}
    text = json.dumps(result, indent=2)
    if "SEQN" in text.upper():  # defensive: results must never carry the participant identifier
        sys.exit("refusing to output: participant identifier name found in results")
    print(text)
    if args.json:
        Path(args.json).write_text(text + "\n")


if __name__ == "__main__":
    main()
