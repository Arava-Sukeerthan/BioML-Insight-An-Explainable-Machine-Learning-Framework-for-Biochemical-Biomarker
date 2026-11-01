"""Repository data-protection checks (PROTOCOL-DRAFT-002; extended in PROTOCOL-DRAFT-003).

The repository is public. These checks guard against committing raw NHANES files,
participant-level derived data, per-participant model outputs and serialized models.

Files checked: every tracked file, plus every untracked file that is NOT ignored. The second
group is what `git add -A` would stage.

What is checked:
1. Representative sensitive paths are ignored (`git check-ignore`). Representative legitimate
   paths (source code, documentation, schemas and configs in JSON, aggregate outputs, the planned
   committed manifest) are not ignored, so the rules do not hide project files.
2. No checked file has a sensitive data or serialized-model extension (any letter case).
3. No checked file lies under a participant-level directory.
4. No checked file starts with a known content signature, whatever its name: SAS transport
   ("HEADER RECORD*******"; the version-5 form is verified on the NHANES files, other versions
   are assumed to share this prefix but were not verified against real files), Apache Parquet ("PAR1"), NumPy .npy ("\\x93NUMPY"), HDF5.
5. No checked CSV/TSV header, JSON object key or JSONL object key is a participant identifier
   (`SEQN`, any letter case, surrounding whitespace ignored). Files listed in
   identifier_allowlist.txt (variable dictionaries or configs) are exempt from this check only.
6. Self-tests: the detectors work on SYNTHETIC byte strings and synthetic headers (no real data).

Git: if the git executable is missing or the directory is not a Git working tree, the tests are
SKIPPED, unless the environment variable DATA_PROTECTION_STRICT=1 is set, in which case they FAIL.
scripts/run_checks.sh sets strict mode. Any unexpected `git check-ignore` error is a failure,
never silently treated as "not ignored".

What these checks CANNOT detect (do not read a pass as proof that no sensitive data exist):
- participant-level rows in other formats or names (e.g. .txt, .md, .yaml, notebooks, images,
  PDFs, CSV files without a header row, spreadsheets outside /data/);
- archives are not opened: a .zip, .tar or .gz outside /data/ and /outputs/, or a spreadsheet
  (itself a zip) anywhere outside /data/, is not inspected;
- pickle/joblib/ONNX/PyTorch content renamed to an innocent extension (no reliable signature
  check is implemented for these), and SAS7BDAT content under another name;
- fitted models saved as .json outside the model directories;
- identifiers that were renamed (e.g. `id`, `respondent`) or data without any identifier column;
- JSON/JSONL files that fail to parse (reported as failures, not scanned);
- anything already in Git history (only the current working tree is checked);
- disclosure through small cells in aggregate tables.

Run from the repository root:
    python3 -I -m unittest discover -s tests/data_protection -v
or all project checks:
    sh scripts/run_checks.sh
"""
import csv
import json
import os
import re
import shutil
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ALLOWLIST_FILE = Path(__file__).resolve().parent / "identifier_allowlist.txt"
STRICT = os.environ.get("DATA_PROTECTION_STRICT") == "1"

IDENTIFIERS = {"SEQN"}
SIGNATURES = {  # leading bytes -> description
    b"HEADER RECORD*******": "SAS transport (XPT)",
    b"PAR1": "Apache Parquet",
    b"\x93NUMPY": "NumPy .npy array",
    b"\x89HDF\r\n\x1a\n": "HDF5",
}
SENSITIVE_EXTENSIONS = re.compile(
    r"\.(xpt|sas7bdat|sav|dta|rds|parquet|feather|npy|npz|h5|hdf5|pkl|pickle|joblib|"
    r"onnx|pt|pth|safetensors|cbm|ubj)$", re.IGNORECASE)
PARTICIPANT_LEVEL_DIRS = ("data/raw/", "data/interim/", "data/processed/", "data/derived/",
                          "outputs/participant_level/", "outputs/models/", "models/")

SHOULD_BE_IGNORED = [
    # raw and statistical-package files
    "data/raw/nhanes/2017-2020/P_GHB.xpt", "data/raw/nhanes/MANIFEST_local.csv", "P_GHB.XPT",
    "anywhere/GHB_L.Xpt", "data/raw/charls/blood.dta", "x/analysis.sas7bdat", "x/SURVEY.SAV",
    "x/survey.sav",
    # participant-level derived data and outputs
    "data/interim/merged.csv", "data/processed/analytic.parquet", "data/derived/analytic_dataset.csv",
    "outputs/participant_level/temporal_predictions.csv", "outputs/participant_level/shap_values.csv",
    "outputs/participant_level/conformal_sets.json", "outputs/participant_level/predictions.xlsx",
    "outputs/tmp/scratch.csv",
    # models and serialized objects
    "outputs/models/bl3_xgboost.json", "models/framework_final.joblib", "models/booster.json",
    "outputs/shap_values.npy", "results/arrays.npz", "anywhere/table.feather", "anywhere/model.pkl",
    "anywhere/model.pickle", "anywhere/store.h5", "anywhere/UPPER.PARQUET", "anywhere/Model.Joblib",
    "anywhere/ARRAY.NPY", "anywhere/net.onnx", "anywhere/net.pt", "anywhere/NET.PTH",
    "anywhere/weights.safetensors", "anywhere/model.cbm", "anywhere/booster.ubj",
    # archives and spreadsheets in data locations; archives in outputs
    "data/export.zip", "data/derived/analytic.csv.gz", "data/raw/nhanes/bundle.tar",
    "data/participants.xlsx", "data/manifest/scratch.XLS", "outputs/aggregate/bundle.zip",
    "outputs/report.tar.gz",
]

SHOULD_NOT_BE_IGNORED = [
    "outputs/README.md", "outputs/aggregate/table1_counts.csv",
    "outputs/aggregate/metrics_temporal_validation.csv", "outputs/aggregate/table1_counts.xlsx",
    "outputs/aggregate/descriptive_counts.json", "data/manifest/nhanes_files.csv",
    "src/bioml/models/logistic.py", "src/bioml/models/params.json", "configs/model_params.json",
    "configs/protocol_v1.0.yaml", "scripts/data/build_analytic_dataset.py",
    "scripts/nhanes/descriptive_counts.py", "scripts/nhanes/README.md", "scripts/run_checks.sh",
    "research/methodology/experimental_protocol_v0.1_draft.md",
    "research/literature/schemas/paper_inventory.schema.json", "research/literature/raw_exports/MANIFEST.csv",
    "tests/data_protection/test_data_protection.py", "tests/data_protection/identifier_allowlist.txt",
    "docs/figures/calibration.pdf", "research/reviews/notes.xlsx",
]


def git_available():
    return shutil.which("git") is not None


def git(*args):
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)


def checked_files():
    """Tracked files plus untracked files that are not ignored (what `git add -A` would add)."""
    tracked = git("ls-files", "-z")
    untracked = git("ls-files", "-z", "--others", "--exclude-standard")
    for r in (tracked, untracked):
        if r.returncode != 0:
            raise AssertionError(f"git ls-files failed: {r.stderr.strip()}")
    names = tracked.stdout.split("\0") + untracked.stdout.split("\0")
    return sorted({p for p in names if p and (REPO / p).is_file()})


def is_ignored(path):
    # --no-index: test the rules themselves, even for paths that are already tracked.
    r = git("check-ignore", "-q", "--no-index", path)
    if r.returncode not in (0, 1):  # 0 = ignored, 1 = not ignored, anything else = error
        raise AssertionError(f"git check-ignore failed for {path!r} (exit {r.returncode}): {r.stderr.strip()}")
    return r.returncode == 0


def signature(head):
    for magic, desc in SIGNATURES.items():
        if head.startswith(magic):
            return desc
    return None


def has_identifier(names):
    return sorted({str(n).strip() for n in names if str(n).strip().upper() in IDENTIFIERS})


def json_keys(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from json_keys(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from json_keys(v)


def load_allowlist():
    entries = []
    for line in ALLOWLIST_FILE.read_text(encoding="utf-8").splitlines():
        path = line.split("#", 1)[0].strip()
        if path:
            entries.append(path)
    return entries


def identifiers_in(path, low):
    """Return identifier names found in a CSV/TSV header or JSON/JSONL keys; None if not tabular."""
    if low.endswith((".csv", ".tsv")):
        with open(path, newline="", encoding="utf-8-sig", errors="replace") as fh:
            header = next(csv.reader(fh, delimiter="\t" if low.endswith(".tsv") else ","), [])
        return has_identifier(header)
    if low.endswith(".jsonl"):
        hit = set()
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    hit.update(has_identifier(json_keys(json.loads(line))))
        return sorted(hit)
    if low.endswith(".json"):
        with open(path, encoding="utf-8") as fh:
            return has_identifier(json_keys(json.load(fh)))
    return None


class DetectorSelfTests(unittest.TestCase):
    """SYNTHETIC inputs only: checks that the detectors themselves work."""

    def test_signatures_detected(self):
        self.assertIsNotNone(signature(b"HEADER RECORD*******LIBRARY HEADER RECORD!!!!!!!000"))
        # synthetic prefix-only variant; the exact header of other XPT versions is not verified
        self.assertIsNotNone(signature(b"HEADER RECORD*******LIBV8   HEADER RECORD!!!!!!!000"))
        self.assertIsNotNone(signature(b"PAR1\x15\x04"))
        self.assertIsNotNone(signature(b"\x93NUMPY\x01\x00"))
        self.assertIsNotNone(signature(b"\x89HDF\r\n\x1a\n\x00"))
        self.assertIsNone(signature(b"# Markdown heading"))
        self.assertIsNone(signature(b"paper_id,title\n"))

    def test_identifier_detection(self):
        self.assertEqual(has_identifier(["seqn ", "prob"]), ["seqn"])
        self.assertEqual(has_identifier([" SEQN"]), ["SEQN"])
        self.assertEqual(has_identifier(["seqn_count", "paper_id"]), [])
        self.assertEqual(sorted(json_keys({"a": [{"SEQN": 1}]})), ["SEQN", "a"])

    def test_extension_detection_any_case(self):
        for name in ["a.XPT", "b.Sav", "c.parquet", "d.ONNX", "e.pt", "f.SafeTensors", "g.cbm", "h.UBJ"]:
            self.assertTrue(SENSITIVE_EXTENSIONS.search(name), name)
        for name in ["a.py", "b.md", "c.json", "d.csv", "e.yaml", "f.ptx"]:
            self.assertFalse(SENSITIVE_EXTENSIONS.search(name), name)


class DataProtectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reason = None
        if not git_available():
            reason = "git executable not found"
        elif git("rev-parse", "--is-inside-work-tree").stdout.strip() != "true":
            reason = "not a Git working tree"
        if reason:
            if STRICT:
                raise AssertionError(f"DATA_PROTECTION_STRICT=1 but {reason}; checks cannot run")
            raise unittest.SkipTest(f"{reason}; data-protection checks need Git (set DATA_PROTECTION_STRICT=1 to fail instead)")
        cls.files = checked_files()

    def test_sensitive_paths_are_ignored(self):
        missing = [p for p in SHOULD_BE_IGNORED if not is_ignored(p)]
        self.assertEqual(missing, [], f"sensitive paths not ignored: {missing}")

    def test_legitimate_paths_are_not_ignored(self):
        hidden = [p for p in SHOULD_NOT_BE_IGNORED if is_ignored(p)]
        self.assertEqual(hidden, [], f"legitimate paths wrongly ignored: {hidden}")

    def test_no_sensitive_formats(self):
        bad = [p for p in self.files if SENSITIVE_EXTENSIONS.search(p)]
        self.assertEqual(bad, [], f"files with sensitive data formats would be tracked: {bad}")

    def test_no_files_in_participant_level_dirs(self):
        bad = [p for p in self.files if p.startswith(PARTICIPANT_LEVEL_DIRS)]
        self.assertEqual(bad, [], f"files in participant-level directories: {bad}")

    def test_no_known_data_signatures(self):
        bad = []
        for p in self.files:
            with open(REPO / p, "rb") as fh:
                desc = signature(fh.read(32))
            if desc:
                bad.append(f"{p}: {desc}")
        self.assertEqual(bad, [], f"data-file content found (any filename): {bad}")

    def test_allowlist_is_valid(self):
        bad = [p for p in load_allowlist()
               if not (REPO / p).is_file() or p.startswith(("data/", "outputs/"))]
        self.assertEqual(bad, [], f"invalid allowlist entries (missing, or under data/ or outputs/): {bad}")

    def test_no_participant_identifier_in_tabular_files(self):
        # Only VALID entries exempt a file: an entry under data/ or outputs/ (or a missing file)
        # never grants an exemption, even though test_allowlist_is_valid also reports it.
        allowed = {p for p in load_allowlist()
                   if (REPO / p).is_file() and not p.startswith(("data/", "outputs/"))}
        findings, unreadable = [], []
        for p in self.files:
            if p in allowed:
                continue
            try:
                hit = identifiers_in(REPO / p, p.lower())
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                unreadable.append(f"{p}: {type(exc).__name__}")
                continue
            if hit:
                findings.append(f"{p}: {hit}")
        self.assertEqual(unreadable, [], f"tabular files that could not be scanned: {unreadable}")
        self.assertEqual(findings, [], f"participant identifiers found: {findings}")


if __name__ == "__main__":
    unittest.main()
