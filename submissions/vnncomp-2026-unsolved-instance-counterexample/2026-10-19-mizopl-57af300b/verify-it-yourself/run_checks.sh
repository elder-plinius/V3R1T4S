#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PKG_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
cd "$PKG_ROOT"

if [ -x /opt/homebrew/bin/python3 ]; then
    PY="/opt/homebrew/bin/python3"
else
    PY="python3"
fi

TMP_BAD="$(mktemp)"
trap 'rm -f "$TMP_BAD"; rm -rf cachier verify-it-yourself/__pycache__' EXIT

echo "=== [1/2] Verifying VNN-COMP 2026 counterexample tinyimagenet_eps1_wide_cnn7_idx7687_sample8 ==="
if ! "$PY" verify-it-yourself/check_vnncomp_cex.py; then
    echo "FAIL"
    exit 1
fi

echo "=== [2/2] Negative control: corrupting X_0 to 1.0 (must fail strict interior box check) ==="
"$PY" -c '
import pathlib, re, sys
s = pathlib.Path("object/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample").read_text()
s_bad = re.sub(r"\(X_0\s+[-0-9.eE+]+\)", "(X_0 1.0)", s, count=1)
pathlib.Path(sys.argv[1]).write_text(s_bad)
' "$TMP_BAD"

if "$PY" verify-it-yourself/check_vnncomp_cex.py --counterexample "$TMP_BAD" >/dev/null 2>&1; then
    echo "ERROR: negative control unexpectedly passed!"
    echo "FAIL"
    exit 1
fi
echo "Negative control rejected as expected."

rm -rf cachier verify-it-yourself/__pycache__
echo "ALL CHECKS PASS"
