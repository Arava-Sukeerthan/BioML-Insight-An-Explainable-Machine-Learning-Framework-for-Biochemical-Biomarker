#!/bin/sh
# Run all project checks (PROTOCOL-DRAFT-003). Run from the repository root:  sh scripts/run_checks.sh
# 1. literature unit tests   2. data-protection checks (strict: fail if Git is unavailable)
# 3. literature query-table validation.
# The descriptive NHANES counts (scripts/nhanes/descriptive_counts.py) are NOT run here because they
# need the git-ignored raw data files; run that script separately (see scripts/nhanes/README.md).
set -eu
cd "$(dirname "$0")/.."
echo "== literature tests"
python3 -I -m unittest discover -s tests/literature
echo "== data-protection checks (strict)"
DATA_PROTECTION_STRICT=1 python3 -I -m unittest discover -s tests/data_protection -v
echo "== query-table validation"
python3 -I scripts/literature/validate_search_queries.py research/literature/search_queries.csv | tail -1
echo "== all checks passed"
