"""Regression tests for the NHANES safeguard corrections (audit of 2026-10-31).

ALL DATA IN THIS FILE ARE SYNTHETIC SOFTWARE-TEST FIXTURES built in memory: participant IDs start at
9,000,001 (outside the NHANES SEQN ranges), frames carry attrs["synthetic"] = True and a
SYNTHETIC_FIXTURE column, and values are hand-chosen only to exercise each rule. No test reads data
files, uses the network or fits a model. Passing these tests says nothing about behaviour on the
real NHANES files, which have not been used.

Run from the repository root:
    python3 -I -m unittest discover -s tests/nhanes -v
"""
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
NHANES = REPO / "scripts" / "nhanes"
sys.path.insert(0, str(NHANES))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import safeguards as sg  # noqa: E402
from test_safeguards import SYNTHETIC_ID_START, candidate_predictors, synthetic_frame  # noqa: E402

BASE = dict(RIDSTATR=2, RIDAGEYR=45, in_fasting_glucose_file=True, WTSAF_SYNTH=1000.0,
            LBXGLU=95.0, LBXGH=5.4, RIDEXPRG=None, DIQ010=2, DIQ070=None)


class TestE3MissingAndInvalidValues(unittest.TestCase):
    """B1: missing or invalid E3 values are rejected, never coerced to True."""

    def test_invalid_values_raise(self):
        import numpy as np
        import pandas as pd
        for bad in (np.nan, None, "both", "left_only", 1, 0, 1.0, pd.NA):
            with self.subTest(bad=bad):
                d = synthetic_frame([dict(BASE), dict(BASE, in_fasting_glucose_file=bad)])
                with self.assertRaises(ValueError) as cm:
                    sg.eligibility_cascade(d, "WTSAF_SYNTH")
                self.assertIn("not coerced", str(cm.exception))

    def test_nullable_boolean_with_missing_raises_and_true_false_pass(self):
        import numpy as np
        import pandas as pd
        d = synthetic_frame([dict(BASE), dict(BASE)])
        d["in_fasting_glucose_file"] = pd.array([True, pd.NA], dtype="boolean")
        with self.assertRaises(ValueError):
            sg.eligibility_cascade(d, "WTSAF_SYNTH")
        d["in_fasting_glucose_file"] = pd.array([True, False], dtype="boolean")
        self.assertEqual(sg.eligibility_cascade(d, "WTSAF_SYNTH")[0]["E3_in_fasting_glucose_file"], 1)
        d["in_fasting_glucose_file"] = [np.bool_(True), False]
        self.assertEqual(sg.eligibility_cascade(d, "WTSAF_SYNTH")[0]["E3_in_fasting_glucose_file"], 1)

    def test_merge_indicator_must_be_mapped_explicitly(self):
        d = synthetic_frame([dict(BASE), dict(BASE)])
        d["in_glu"] = ["both", "left_only"]
        d["in_fasting_glucose_file"] = d["in_glu"] == "both"           # the documented mapping
        self.assertEqual(sg.eligibility_cascade(d, "WTSAF_SYNTH")[0]["E3_in_fasting_glucose_file"], 1)

    def test_duplicate_or_missing_seqn_raises(self):
        d = synthetic_frame([dict(BASE), dict(BASE)])
        d.loc[1, "SEQN"] = d.loc[0, "SEQN"]
        with self.assertRaises(ValueError):
            sg.eligibility_cascade(d, "WTSAF_SYNTH")


class TestCascadeAuditability(unittest.TestCase):
    """B6: subcategory counts are preserved (the same names as descriptive_counts.period_counts)."""

    def frame(self):
        rows = [dict(BASE),
                dict(BASE, RIDAGEYR=19),                       # E2 (counts in E2_alt_age_ge_18)
                dict(BASE, LBXGLU=None),                       # E5a
                dict(BASE, LBXGH=None),                        # E5 (after E5a)
                dict(BASE, RIDEXPRG=1),                        # E6
                dict(BASE, DIQ010=1),                          # E7 diagnosed
                dict(BASE, DIQ010=7),                          # E7 refused
                dict(BASE, DIQ010=None),                       # E7 missing
                dict(BASE, DIQ010=4),                          # E7 other code
                dict(BASE, DIQ010=3, DIQ070=1)]                # E8
        return synthetic_frame(rows)

    def test_subcategories_and_excluded_counts(self):
        d = self.frame()
        self.assertTrue(d.attrs["synthetic"] and d["SYNTHETIC_FIXTURE"].all())
        details = {}
        counts, mask = sg.eligibility_cascade(d, "WTSAF_SYNTH", details)
        self.assertEqual(counts["E8_analytic_N"], 1)
        self.assertEqual({k: v for k, v in details.items() if k != "excluded_at"},
                         {"E2_alt_age_ge_18": 10, "E5a_valid_fpg": 8, "E6_excluded_pregnant": 1,
                          "E7_excluded_diagnosed": 1, "E7_excluded_refused_dk_missing": 2,
                          "E7_excluded_other_code": 1, "E8_excluded_diabetes_pills": 1})
        self.assertEqual(details["excluded_at"]["E2_age_ge_20"], 1)
        self.assertEqual(details["excluded_at"]["E7_no_diagnosed_diabetes"], 4)
        self.assertEqual(sum(details["excluded_at"].values()), counts["E0_all_participants"] - counts["E8_analytic_N"])

    def test_names_cover_every_count_in_descriptive_counts(self):
        src = (NHANES / "descriptive_counts.py").read_text()
        body = src[src.index("def period_counts"):src.index("a = d[m].copy()")]
        names = set(re.findall(r'cas\["(\w+)"\]', body))
        d = self.frame()
        details = {}
        counts, _ = sg.eligibility_cascade(d, "WTSAF_SYNTH", details)
        self.assertEqual(names - set(counts) - set(details), set())
        self.assertEqual(set(details) - names, {"E7_excluded_other_code", "excluded_at"})


class TestPredictorAliasesAndFalsePositives(unittest.TestCase):
    """B2/B3: aliases and derived indices are caught as whole tokens; substrings are not."""

    def test_aliases_are_caught(self):
        for col in ("glucose", "Fasting_Glucose", "fpg", "FBG", "hba1c", "HbA1c", "a1c", "Hb_A1c",
                    "glycated_hemoglobin", "LBXGLT", "ogtt_2h", "fasting_hours", "FastingHours",
                    "survey_weight", "mec_weight", "stratum", "psu", "exam_session", "exam_month",
                    "diabetes_status", "told_prediabetes", "metformin_use", "medication_count",
                    "homaIR", "HOMA2_IR", "homa_b", "QUICKI", "tyg", "TyG_BMI", "TyG-WC", "mets_ir",
                    "METSIR", "eGDR", "spise", "cti_index"):
            with self.subTest(col=col):
                self.assertTrue(sg.predictor_violations([col]), col)
                with self.assertRaises(sg.LeakageError):
                    sg.check_predictors(["LBXTC", col])

    def test_former_and_plausible_false_positives_pass(self):
        ok = ["BMI_CORRECTION", "INFECTION_FLAG", "FRACTION_X", "SELECTION_WEIGHTED", "BMI_CALC",
              "glutamate", "GLU_GLN_ratio", "body_weight", "BMXWT", "waist_hip_ratio", "LBXSCA",
              "insulin", "LBXIN", "LBXHSCRP", "URDACT", "SBP", "DBP"]
        self.assertEqual(sg.predictor_violations(ok), [])

    def test_candidate_predictors_still_pass(self):
        cols = candidate_predictors()
        self.assertEqual(sg.predictor_violations(cols), [])

    def test_insulin_is_left_undecided(self):
        # S-06 / Q-050 undecided: insulin by name is not prohibited; a declared feature derived from
        # LBXIN keeps the pre-existing rule (flagged). Neither is a new decision.
        self.assertEqual(sg.predictor_violations(["LBXIN", "insulin"]), [])
        self.assertEqual(sg.predictor_violations(["ins_x"], {"ins_x": ["LBXIN"]}),
                         [("ins_x", "derived from a glycaemic measurement")])

    def test_allow_list_rejects_renamed_columns(self):
        allowed = ["LBXTC", "LBDHDD", "LBXTR"]
        self.assertEqual(sg.check_predictors(["LBXTC", "LBDHDD"], allowed=allowed), ["LBXTC", "LBDHDD"])
        self.assertEqual(sg.check_predictors(["tc_hdl"], {"tc_hdl": ["LBXTC", "LBDHDD"]}, allowed=allowed), ["tc_hdl"])
        for cols, derived in ((["renamed_x"], None), (["ratio"], {"ratio": ["LBXTC", "LBXSATSI"]})):
            with self.subTest(cols=cols), self.assertRaises(sg.LeakageError) as cm:
                sg.check_predictors(cols, derived, allowed=allowed)
            self.assertIn("not in the approved predictor list", str(cm.exception))


class TestParticipantsFoldsAndPartitions(unittest.TestCase):
    """B4/B5: duplicate participant rows, coverage and train/calibration/validation separation."""

    IDS = [SYNTHETIC_ID_START + i for i in range(6)]

    def test_duplicate_participant_rows_across_train_and_test_are_rejected(self):
        ids = [9_000_001, 9_000_001, 9_000_002, 9_000_003]             # rows 0 and 1: one participant
        with self.assertRaises(sg.LeakageError) as cm:
            sg.check_folds([([0, 2], [1, 3])], 4, ids=ids)
        self.assertIn("participants have rows in both", str(cm.exception))
        sg.check_folds([([0, 1], [2, 3])], 4, ids=ids)                   # kept together: allowed
        with self.assertRaises(sg.LeakageError):
            sg.check_folds([([0, 1], [2, 3])], 4, ids=[1, None, 2, 3])
        with self.assertRaises(sg.LeakageError):
            sg.check_folds([([0, 1], [2, 3])], 4, ids=[1, 2, 3])

    def test_partition_coverage(self):
        good = [([2, 3, 4, 5], [0, 1]), ([0, 1, 4, 5], [2, 3]), ([0, 1, 2, 3], [4, 5])]
        sg.check_folds(good, 6, ids=self.IDS, require_partition=True)
        gap = [([2, 3, 4, 5], [0, 1]), ([0, 1, 4, 5], [2, 3])]
        double = good + [([0, 1, 2, 3], [4, 5])]
        partial = [([2, 3], [0, 1]), ([0, 1, 4, 5], [2, 3]), ([0, 1, 2, 3], [4, 5])]
        for name, folds in (("row never tested", gap), ("row tested twice", double), ("train incomplete", partial)):
            with self.subTest(name), self.assertRaises(sg.LeakageError):
                sg.check_folds(folds, 6, require_partition=True)
        with self.assertRaises(sg.LeakageError):
            sg.check_folds([([0, 1.5], [2])], 3)
        with self.assertRaises(sg.LeakageError):
            sg.check_folds([([0, True], [2])], 3)

    def test_fit_within_folds_checks_participants(self):
        rows = [{"v": float(i)} for i in range(4)]
        with self.assertRaises(sg.LeakageError):
            sg.fit_within_folds(rows, [([0, 2], [1, 3])], lambda tr: 0, lambda f, te: 0,
                                ids=[9_000_001, 9_000_001, 9_000_002, 9_000_003])

    def test_train_calibration_validation_separation(self):
        ids = self.IDS
        parts = {"D-train": ids[:3], "D-cal": ids[3:5], "validation": ids[5:]}
        self.assertIs(sg.check_partitions(parts, expected_ids=ids), parts)
        bad = {"overlap": ({"D-train": ids[:3], "D-cal": ids[2:5]}, None),
               "empty": ({"D-train": ids, "D-cal": []}, None),
               "duplicate": ({"D-train": [ids[0], ids[0]], "D-cal": ids[1:]}, None),
               "missing ID": ({"D-train": [None], "D-cal": ids[1:]}, None),
               "participant lost": ({"D-train": ids[:2], "D-cal": ids[2:5]}, ids),
               "participant added": ({"D-train": ids[:3], "D-cal": ids[3:] + [9_999_999]}, ids),
               "single partition": ({"D-train": ids}, None)}
        for name, (p, expected) in bad.items():
            with self.subTest(name), self.assertRaises(sg.LeakageError):
                sg.check_partitions(p, expected_ids=expected)

    def test_disjoint_periods_reject_missing_ids(self):
        with self.assertRaises(sg.LeakageError):
            sg.check_disjoint_participants([9_000_001, None], [9_000_002])
        with self.assertRaises(sg.LeakageError):
            sg.check_disjoint_participants([9_000_001], [float("nan")])

    def test_unique_participants(self):
        sg.check_unique_participants(self.IDS)
        for ids in ([1, 1], [1, None], [1, float("nan")]):
            with self.subTest(ids=ids), self.assertRaises(sg.LeakageError):
                sg.check_unique_participants(ids)


if __name__ == "__main__":
    unittest.main()
