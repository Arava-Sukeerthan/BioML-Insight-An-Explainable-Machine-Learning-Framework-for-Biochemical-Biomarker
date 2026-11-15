#!/usr/bin/env bash
# Install and verify the D-002 environment (approval item A3). READY, NOT RUN without --install.
#
# Usage (from the repository root):
#   bash environment/install_and_verify.sh --q048 xgboost-cpu --authorisation D-nnn [--install]
#     --q048          xgboost | xgboost-cpu   (the researcher's Q-048 choice; no default)
#     --authorisation decision-log ID approving A3 (required with --install)
#     --install       actually install; without it, only a pip dry-run resolution is performed
#
# What it does:
#   1. builds the requirement list from environment/requirements-proposed.txt, replacing the xgboost
#      line by the chosen Q-048 package (same version 3.4.1) and adding wrapt==2.5.2 (final release,
#      instead of the 2.6.0.dev1 pre-release pulled by statsmodels -> formulaic);
#   2. resolves it with `pip install --dry-run --only-binary=:all: --report` (no installation);
#   3. with --install: creates environment/.venv (git-ignored), installs exactly that resolution,
#      writes environment/requirements-lock.txt (name==version --hash=sha256:... from the pip report),
#      runs an import check and the full test suite (scripts/run_checks.sh) inside the venv.
# Any failure stops the script; no pin is changed silently (a failing pin is reported for a decision).
set -euo pipefail

Q048=""; AUTH=""; INSTALL=0
while [ $# -gt 0 ]; do
  case "$1" in
    --q048) Q048="${2:-}"; shift 2 ;;
    --authorisation) AUTH="${2:-}"; shift 2 ;;
    --install) INSTALL=1; shift ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done
case "$Q048" in xgboost|xgboost-cpu) ;; *) echo "refused: --q048 must be xgboost or xgboost-cpu (researcher decision)" >&2; exit 2 ;; esac
if [ "$INSTALL" = 1 ] && [ -z "$AUTH" ]; then echo "refused: --install needs --authorisation (A3)" >&2; exit 2; fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENVDIR="$ROOT/environment"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
REQ="$WORK/requirements.txt"

# 1. requirement list (comments stripped; xgboost line replaced; wrapt pinned)
grep -v '^\s*#' "$ENVDIR/requirements-proposed.txt" | sed 's/\s*#.*$//' | sed '/^\s*$/d' \
  | sed "s/^xgboost==/${Q048}==/" > "$REQ"
echo "wrapt==2.5.2" >> "$REQ"
echo "== requirements"; cat "$REQ"

# 2. resolution only
python3 -m pip install --dry-run --quiet --only-binary=:all: --ignore-installed -r "$REQ" --report "$WORK/report.json"
python3 - "$WORK/report.json" <<'EOF'
import json, sys
rep = json.load(open(sys.argv[1]))
items = sorted((i["metadata"]["name"].lower(), i["metadata"]["version"]) for i in rep["install"])
pre = [f"{n}=={v}" for n, v in items if any(t in v for t in ("dev", "a", "b", "rc")) and not v.replace(".", "").isdigit()]
gpu = [n for n, _ in items if n.startswith("nvidia-")]
print(f"== resolution: {len(items)} packages; pre-releases: {pre or 'none'}; GPU libraries: {gpu or 'none'}")
if pre:
    sys.exit("stop: a pre-release was selected; report it for a pin decision (no silent change)")
EOF

if [ "$INSTALL" = 0 ]; then echo "== dry run only: nothing installed"; exit 0; fi

# 3. install, lock, verify
python3 -m venv "$ENVDIR/.venv"
"$ENVDIR/.venv/bin/python" -m pip install --quiet --only-binary=:all: -r "$REQ" --report "$WORK/install.json"
"$ENVDIR/.venv/bin/python" - "$WORK/install.json" "$ENVDIR/requirements-lock.txt" "$AUTH" "$Q048" <<'EOF'
import json, sys, platform
rep, out, auth, q048 = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
lines = [f"# D-002 lock; authorisation {auth}; Q-048 {q048}; Python {platform.python_version()} "
         f"{platform.machine()}; generated from the pip install report"]
for i in sorted(json.load(open(rep))["install"], key=lambda i: i["metadata"]["name"].lower()):
    h = i.get("download_info", {}).get("archive_info", {}).get("hashes", {}).get("sha256")
    if not h:
        sys.exit(f"stop: no sha256 for {i['metadata']['name']}")
    lines.append(f"{i['metadata']['name']}=={i['metadata']['version']} --hash=sha256:{h}")
open(out, "w").write("\n".join(lines) + "\n")
print(f"== wrote {out} ({len(lines) - 1} packages)")
EOF
"$ENVDIR/.venv/bin/python" -I -c "import numpy, pandas, scipy, sklearn, xgboost, shap, statsmodels, matplotlib; print('== imports OK; xgboost', xgboost.__version__, '; sklearn', sklearn.__version__)"
PATH="$ENVDIR/.venv/bin:$PATH" sh "$ROOT/scripts/run_checks.sh"
echo "== environment installed and verified (authorisation $AUTH)"
