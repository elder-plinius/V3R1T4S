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

TMP_BAD_DIR="$(mktemp -d)"
TMP_UPSTREAM_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_BAD_DIR" "$TMP_UPSTREAM_DIR" verify-it-yourself/__pycache__' EXIT

echo "=== [1/2] Verifying immrep22-tcr-epitope-microauc predictions, evaluate.py stats, and p1/p2/p3 audit ==="
if ! "$PY" verify-it-yourself/check_immrep22_clss.py --upstream-cache-dir "$TMP_UPSTREAM_DIR"; then
    echo "FAIL"
    exit 1
fi

echo "=== [2/2] Negative control: negated scores on SPRWYFYYL.txt (must fail) ==="
cp -R object/clss_tcr_scores/* "$TMP_BAD_DIR/"
"$PY" -c '
import pandas as pd, sys
df = pd.read_csv(sys.argv[1], sep="\t")
df["score"] = -df["score"]
df.to_csv(sys.argv[1], sep="\t", index=False)
' "$TMP_BAD_DIR/SPRWYFYYL.txt"

if "$PY" verify-it-yourself/check_immrep22_clss.py --scores-dir "$TMP_BAD_DIR" --upstream-cache-dir "$TMP_UPSTREAM_DIR" >/dev/null 2>&1; then
    echo "ERROR: negative control unexpectedly passed!"
    echo "FAIL"
    exit 1
fi
echo "Negative control rejected as expected."

rm -rf verify-it-yourself/__pycache__
echo "ALL CHECKS PASS"
