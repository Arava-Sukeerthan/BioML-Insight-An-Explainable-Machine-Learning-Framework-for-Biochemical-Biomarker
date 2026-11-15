"""Tests for scripts/nhanes/safeguards.py.

ALL DATA IN THIS FILE ARE SYNTHETIC SOFTWARE-TEST FIXTURES, built in memory. They are NOT NHANES
observations and are never written to disk: participant IDs start at 9,000,001 (outside the NHANES
SEQN ranges), every frame carries attrs["synthetic"] = True and a SYNTHETIC_FIXTURE column, and the
values are chosen by hand only to exercise each rule. No test reads data files, uses the network or
fits a model.

Run from the repository root:
    python3 -I -m unittest discover -s tests/nhanes -v
"""
import ast
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
NHANES = REPO / "scripts" / "nhanes"
sys.path.insert(0, str(NHANES))
import safeguards as sg  # noqa: E402

SYNTHETIC_ID_START = 9_000_001


def synthetic_frame(rows):
    import pandas as pd
    d = pd.DataFrame(rows)
    d.insert(0, "SEQN", range(SYNTHETIC_ID_START, SYNTHETIC_ID_START + len(d)))
    d["SYNTHETIC_FIXTURE"] = True
    d.attrs["synthetic"] = True
    return d


def candidate_predictors():
    """Candidate predictors named in descriptive_counts.py (draft protocol section 6.1), read from its
    source so the two stay in step; '<tg>' stands for the period's triglyceride variable."""
    tree = ast.parse((NHANES / "descriptive_counts.py").read_text())
    names = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and \
                node.targets[0].id in ("GROUP_A", "GROUP_C", "MISSINGNESS_VARS"):
            names[node.targets[0].id] = ast.literal_eval(node.value)
    out = set(names["GROUP_C"])
    for group in (names["GROUP_A"], names["MISSINGNESS_VARS"]):
        for cols in group.values():
            out |= {c for c in cols if c != "<tg>"}
    return sorted(out | {"LBXTR", "LBXTLG"})


class TestPredictorRules(unittest.TestCase):
    def test_candidate_predictors_are_not_flagged(self):
        cols = candidate_predictors()
        self.assertIn("LBXSATSI", cols)
        self.assertIn("LBXIN", cols)        # insulin: excluded from primary sets, allowed in S-06
        self.assertEqual(sg.predictor_violations(cols), [])
        self.assertEqual(sg.check_predictors(cols), cols)

    def test_every_prohibited_category_is_caught(self):
        cases = {"LBXGH": "outcome", "LBXGLU": "outcome", "LBDGLUSI": "outcome",
                 "LBXSGL": "other glucose", "LBDSGLSI": "other glucose",
                 "SEQN": "survey", "SDMVSTRA": "survey", "SDMVPSU": "survey", "RIDEXMON": "survey",
                 "PHAFSTHR": "survey", "PHAFSTMN": "survey", "PHDSESN": "survey", "PHDSESNZ": "survey",
                 "DIQ010": "questionnaire", "DID040": "questionnaire", "RXQ033": "medication",
                 "RXDDRUG": "medication", "WTSAFPRP": "weight", "WTSAF2YR": "weight", "WTMECPRP": "weight",
                 "LBDHDDLC": "comment", "HOMA_IR": "derived", "tyg_bmi": "derived", "METS-IR": "derived"}
        for col, kind in cases.items():
            with self.subTest(col=col):
                (bad,) = sg.predictor_violations([col])
                self.assertIn(kind.split()[0], bad[1])
                with self.assertRaises(sg.LeakageError):
                    sg.check_predictors(["LBXTC", col])

    def test_lower_case_names_are_caught(self):
        self.assertEqual(len(sg.predictor_violations(["lbxgh", "seqn", "wtsafprp"])), 3)

    def test_declared_derived_feature_from_glucose_is_caught_whatever_its_name(self):
        bad = sg.predictor_violations(["ratio_x", "ratio_y"],
                                      {"ratio_x": ["LBXTR", "LBXGLU"], "ratio_y": ["LBXTR", "LBDHDD"]})
        self.assertEqual(bad, [("ratio_x", "derived from a glycaemic measurement")])


class TestFoldsAndPeriods(unittest.TestCase):
    def test_participants_in_both_periods_are_rejected(self):
        sg.check_disjoint_participants([9_000_001, 9_000_002], [9_000_003])
        with self.assertRaises(sg.LeakageError):
            sg.check_disjoint_participants([9_000_001, 9_000_002], [9_000_002])

    def test_invalid_folds_are_rejected(self):
        bad = {"overlap": [([0, 1, 2], [2, 3])], "duplicate": [([0, 0, 1], [2])],
               "out of range": [([0, 1], [9])], "empty": [([], [0, 1])]}
        for name, folds in bad.items():
            with self.subTest(name=name), self.assertRaises(sg.LeakageError):
                sg.check_folds(folds, 4)
        self.assertTrue(sg.check_folds([([0, 1], [2, 3]), ([2, 3], [0, 1])], 4))

    def test_preprocessing_is_fitted_on_training_rows_only(self):
        rows = [{"id": i, "value": float(v), "test_only": i >= 4} for i, v in enumerate([1, 2, 3, 4, 100, 200])]
        folds = [([0, 1, 2, 3], [4, 5]), ([2, 3, 4, 5], [0, 1])]
        seen = []

        def fit(train):                 # a mean imputer: the statistic must come from training rows
            seen.append(sorted(r["id"] for r in train))
            return sum(r["value"] for r in train) / len(train)

        def apply(mean, test):
            return mean, sorted(r["id"] for r in test)

        results = sg.fit_within_folds(rows, folds, fit, apply)
        self.assertEqual(seen, [[0, 1, 2, 3], [2, 3, 4, 5]])
        self.assertEqual(results[0], (2.5, [4, 5]))            # not the all-row mean 51.67
        self.assertEqual(results[1], (76.75, [0, 1]))
        with self.assertRaises(sg.LeakageError):
            sg.fit_within_folds(rows, [([0, 1, 4], [4, 5])], fit, apply)


class TestEligibilityCascade(unittest.TestCase):
    def test_each_rule_on_a_synthetic_frame(self):
        base = dict(RIDSTATR=2, RIDAGEYR=45, in_fasting_glucose_file=True, WTSAF_SYNTH=1000.0,
                    LBXGLU=95.0, LBXGH=5.4, RIDEXPRG=None, DIQ010=2, DIQ070=None)
        rows = [dict(base),                                   # eligible
                dict(base, DIQ010=3, DIQ070=2),               # borderline, no pills: eligible
                dict(base, RIDSTATR=1),                       # E1: not examined
                dict(base, RIDAGEYR=19),                      # E2: under 20
                dict(base, in_fasting_glucose_file=False),    # E3
                dict(base, WTSAF_SYNTH=0.0),                  # E4
                dict(base, LBXGH=None),                       # E5
                dict(base, RIDEXPRG=1),                       # E6
                dict(base, DIQ010=1),                         # E7: diagnosed
                dict(base, DIQ010=9),                         # E7: don't know
                dict(base, DIQ010=3, DIQ070=1)]               # E8: pills
        d = synthetic_frame(rows)
        self.assertTrue(d.attrs["synthetic"] and d["SYNTHETIC_FIXTURE"].all())
        self.assertGreaterEqual(int(d["SEQN"].min()), SYNTHETIC_ID_START)
        counts, mask = sg.eligibility_cascade(d, "WTSAF_SYNTH")
        self.assertEqual(counts, {"E0_all_participants": 11, "E1_mec_examined": 10, "E2_age_ge_20": 9,
                                  "E3_in_fasting_glucose_file": 8, "E4_fasting_weight_gt_0": 7,
                                  "E5_valid_fpg_and_hba1c": 6, "E6_not_pregnant": 5,
                                  "E7_no_diagnosed_diabetes": 3, "E8_analytic_N": 2})
        self.assertEqual(list(d.loc[mask, "SEQN"]), [9_000_001, 9_000_002])

    def test_rules_match_the_descriptive_counts_script(self):
        """The cascade rules must stay identical to descriptive_counts.period_counts (source check)."""
        src = (NHANES / "descriptive_counts.py").read_text()
        for expr in ("d.RIDSTATR == 2", "d.RIDAGEYR >= 20", 'd.in_glu == "both"', "d[fw] > 0",
                     "d.LBXGLU.notna()", "d.LBXGH.notna()", "~(d.RIDEXPRG == 1)", "d.DIQ010.isin([2, 3])",
                     "~(d.DIQ070 == 1)"):
            self.assertIn(expr, src)


class TestSeparation(unittest.TestCase):
    MODEL_LIBS = {"sklearn", "xgboost", "lightgbm", "catboost", "torch", "tensorflow", "keras", "shap",
                  "mapie", "interpret"}
    NETWORK_LIBS = {"urllib", "requests", "http", "socket", "httpx", "aiohttp"}

    def imports(self, path):
        names = set()
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Import):
                names |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module:
                names.add(node.module.split(".")[0])
        return names

    def test_no_nhanes_script_fits_models_or_uses_the_network(self):
        for path in sorted(NHANES.glob("*.py")):
            with self.subTest(script=path.name):
                found = self.imports(path)
                self.assertFalse(found & self.MODEL_LIBS, f"model library imported: {found & self.MODEL_LIBS}")
                self.assertFalse(found & self.NETWORK_LIBS, f"network library imported: {found & self.NETWORK_LIBS}")


if __name__ == "__main__":
    unittest.main()
