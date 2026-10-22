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
trap 'rm -f "$TMP_BAD"; rm -rf verify-it-yourself/__pycache__' EXIT

echo "=== [1/2] Verifying polaris-moleculeace-activity-cliff-mse predictions and 30-target sweep ==="
if ! "$PY" verify-it-yourself/check_moleculeace_clss.py; then
    echo "FAIL"
    exit 1
fi

echo "=== [2/2] Negative control: constant-mean predictions on CHEMBL287_Ki (must fail) ==="
"$PY" -c '
import pandas as pd, sys
df = pd.read_csv("object/CHEMBL287_Ki_test_predictions.csv")
df["y_pred_clss"] = df["y_true"].mean()
df.to_csv(sys.argv[1], index=False)
' "$TMP_BAD"

if "$PY" verify-it-yourself/check_moleculeace_clss.py --predictions "$TMP_BAD" >/dev/null 2>&1; then
    echo "ERROR: negative control unexpectedly passed!"
    echo "FAIL"
    exit 1
fi
echo "Negative control rejected as expected."

rm -rf verify-it-yourself/__pycache__
echo "ALL CHECKS PASS"
