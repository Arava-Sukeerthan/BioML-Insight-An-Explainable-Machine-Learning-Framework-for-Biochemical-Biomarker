"""Synthetic equivalence test: safeguards.eligibility_cascade vs descriptive_counts.period_counts.

ALL DATA ARE SYNTHETIC SOFTWARE-TEST FIXTURES built in memory (participant IDs from 9,000,001,
outside the NHANES SEQN ranges; hand-chosen values). descriptive_counts.read() is replaced by a
function returning these synthetic tables, and pandas.read_sas is patched to fail, so no NHANES file
is read; the input-hash check (verify_inputs) is not called. No model is fitted.

What this establishes: on these synthetic tables, which exercise every E0-E8 rule and its
subcategories (including missing values and unexpected codes), the two implementations give the same
cascade counts when in_fasting_glucose_file is derived as in_glu == "both". What it does NOT
establish: equivalence on the real NHANES files, whose value encodings, missing-value handling in
the XPT reader and merge behaviour have not been checked here (real-data equivalence remains
unverified).

Run from the repository root:
    python3 -I -m unittest discover -s tests/nhanes -p test_cascade_equivalence.py -v
"""
import sys
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
NHANES = REPO / "scripts" / "nhanes"
sys.path.insert(0, str(NHANES))
import safeguards as sg  # noqa: E402

START = 9_000_001
NAN = float("nan")
# (RIDSTATR, RIDAGEYR, RIDEXPRG, in GLU file, weight, LBXGLU, LBXGH, DIQ010, DIQ070)
ROWS = [
    (2, 45, NAN, True, 1000.0, 95.0, 5.4, 2, NAN),      # eligible
    (2, 60, NAN, True, 1200.0, 105.0, 5.8, 2, NAN),     # eligible (positive by FPG and HbA1c)
    (2, 33, 2, True, 900.0, 99.0, 5.6, 3, 2),           # eligible: borderline, no pills
    (2, 52, NAN, True, 800.0, 101.0, 5.2, 3, NAN),      # eligible: borderline, pill item missing
    (1, 45, NAN, True, 1000.0, 95.0, 5.4, 2, NAN),      # E1: interviewed only
    (2, 19, NAN, True, 1000.0, 95.0, 5.4, 2, NAN),      # E2 (counted in the >= 18 alternative)
    (2, 17, NAN, True, 1000.0, 95.0, 5.4, 2, NAN),      # E2 (not counted in the >= 18 alternative)
    (2, 45, NAN, False, NAN, NAN, 5.4, 2, NAN),         # E3: not in the fasting file
    (2, 45, NAN, True, 0.0, 95.0, 5.4, 2, NAN),         # E4: weight 0
    (2, 45, NAN, True, NAN, 95.0, 5.4, 2, NAN),         # E4: weight missing
    (2, 45, NAN, True, 1000.0, NAN, 5.4, 2, NAN),       # E5a: FPG missing
    (2, 45, NAN, True, 1000.0, 95.0, NAN, 2, NAN),      # E5: HbA1c missing
    (2, 30, 1, True, 1000.0, 95.0, 5.4, 2, NAN),        # E6: pregnant
    (2, 45, NAN, True, 1000.0, 130.0, 7.1, 1, 1),       # E7: diagnosed
    (2, 45, NAN, True, 1000.0, 95.0, 5.4, 7, NAN),      # E7: refused
    (2, 45, NAN, True, 1000.0, 95.0, 5.4, 9, NAN),      # E7: don't know
    (2, 45, NAN, True, 1000.0, 95.0, 5.4, NAN, NAN),    # E7: missing
    (2, 45, NAN, True, 1000.0, 95.0, 5.4, 4, NAN),      # E7: unexpected code
    (2, 45, NAN, True, 1000.0, 110.0, 6.0, 3, 1),       # E8: borderline, takes pills
]
PERIOD = "2021-2023"


def synthetic_tables(dc):
    import pandas as pd
    cfg = dc.PERIODS[PERIOD]
    fw, tg, ses = cfg["fw"], cfg["tg"], cfg["ses"]
    seqn = list(range(START, START + len(ROWS)))
    col = lambda i: [r[i] for r in ROWS]
    demo = pd.DataFrame({"SEQN": seqn, "RIDSTATR": col(0), "RIDAGEYR": col(1), "RIDEXPRG": col(2),
                         "RIAGENDR": [1, 2] * (len(ROWS) // 2) + [1] * (len(ROWS) % 2),
                         "SDMVSTRA": [1, 2] * (len(ROWS) // 2) + [1] * (len(ROWS) % 2), "SDMVPSU": 1})
    diq = pd.DataFrame({"SEQN": seqn, "DIQ010": col(7), "DIQ160": NAN, "DIQ050": NAN, "DIQ070": col(8)})
    ghb = pd.DataFrame({"SEQN": seqn, "LBXGH": col(6)})
    in_glu = [s for s, r in zip(seqn, ROWS) if r[3]]
    glu = pd.DataFrame({"SEQN": in_glu, fw: [r[4] for r in ROWS if r[3]], "LBXGLU": [r[5] for r in ROWS if r[3]]})
    fastqx = pd.DataFrame({"SEQN": seqn, "PHAFSTHR": 10.0, "PHAFSTMN": 0.0, ses: 1})
    names = {v for vs in list(dc.GROUP_A.values()) + list(dc.MISSINGNESS_VARS.values()) for v in vs}
    names = {tg if v == "<tg>" else v for v in names} | {"BPXOSY1", "BPXOSY2", "BPXOSY3", "BPXODI1",
                                                          "BPXODI2", "BPXODI3", "LBXHSCRP"}
    other = pd.DataFrame({"SEQN": seqn, **{n: 1.0 for n in sorted(names)}})
    tables = {"DEMO": demo, "DIQ": diq, "GHB": ghb, "GLU": glu, "FASTQX": fastqx}

    def read(period, component):
        assert period == PERIOD, period
        return tables.get(component, other).copy()
    merged = (demo.merge(diq, on="SEQN", how="left").merge(ghb, on="SEQN", how="left")
              .merge(glu, on="SEQN", how="left", indicator="in_glu"))
    merged["in_fasting_glucose_file"] = merged["in_glu"] == "both"
    merged.attrs["synthetic"] = True
    return read, merged, fw


class TestCascadeEquivalenceSynthetic(unittest.TestCase):
    def test_same_counts_as_period_counts_on_synthetic_tables(self):
        import pandas as pd
        import descriptive_counts as dc
        read, merged, fw = synthetic_tables(dc)
        no_files = mock.patch.object(pd, "read_sas", side_effect=AssertionError("no data files in tests"))
        with mock.patch.object(dc, "read", read), no_files:
            reference = dc.period_counts(PERIOD)["cascade"]
        details = {}
        counts, mask = sg.eligibility_cascade(merged, fw, details)
        ours = {**counts, **details}
        self.assertEqual({k: ours[k] for k in reference}, reference)
        self.assertEqual(counts["E8_analytic_N"], 4)
        self.assertEqual(details["E7_excluded_other_code"], 1)      # reported only by eligibility_cascade
        self.assertEqual(list(merged.loc[mask, "SEQN"]), [START, START + 1, START + 2, START + 3])

    def test_fixture_exercises_every_cascade_step(self):
        import descriptive_counts as dc
        _, merged, fw = synthetic_tables(dc)
        details = {}
        sg.eligibility_cascade(merged, fw, details)
        self.assertTrue(all(v > 0 for v in details["excluded_at"].values()), details["excluded_at"])


if __name__ == "__main__":
    unittest.main()
