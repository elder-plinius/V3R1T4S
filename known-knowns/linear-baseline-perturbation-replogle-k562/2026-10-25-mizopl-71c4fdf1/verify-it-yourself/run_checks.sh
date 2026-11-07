#!/bin/sh
# Standalone verification & negative-control test runner for linear-baseline-perturbation-replogle-k562 (p2)
set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PKG_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CERT="$PKG_DIR/object/certificate_replogle_k562.json"
VERIFIER="$SCRIPT_DIR/verify.py"

if [ -x /opt/homebrew/bin/python3 ]; then
    PYTHON=/opt/homebrew/bin/python3
else
    PYTHON=python3
fi

echo "=== [1/3] Running positive verification on $CERT ==="
"$PYTHON" "$VERIFIER" "$CERT"

echo "=== [2/3] Running negative-control test (corrupted certificate must fail) ==="
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/verify_corrupt_XXXXXX")"
trap 'rm -rf "$TMP_DIR"' EXIT INT TERM

for f in "$PKG_DIR/object/"*.tsv; do
    ln -s "$f" "$TMP_DIR/$(basename "$f")"
done

"$PYTHON" -c '
import json, sys
with open(sys.argv[1], "r", encoding="utf-8") as f:
    d = json.load(f)
d["reproduction_and_ablation_panel_A_seeds_1_2"]["replogle_k562_essential"]["hollow_loo_dual_lens"]["l2_mean"] += 5.0
with open(sys.argv[2], "w", encoding="utf-8") as f:
    json.dump(d, f)
' "$CERT" "$TMP_DIR/certificate_replogle_k562.json"

if "$PYTHON" "$VERIFIER" "$TMP_DIR/certificate_replogle_k562.json" >/dev/null 2>&1; then
    echo "[ERROR] Verifier unexpectedly passed on corrupted certificate!" >&2
    exit 1
else
    echo "[PASS] Verifier correctly rejected corrupted certificate with non-zero exit code."
fi

echo "=== [3/3] Running negative-control test (corrupted plain-text prediction TSV must fail) ==="
cp "$CERT" "$TMP_DIR/certificate_replogle_k562.json"
rm -f "$TMP_DIR/k562_seed1_dual_predictions.tsv"
"$PYTHON" -c '
import sys
with open(sys.argv[1], "r", encoding="utf-8") as f:
    lines = f.read().splitlines()
cols = lines[1].split("\t")
cols[7] = f"{float(cols[7]) + 5.0:.4f}"
lines[1] = "\t".join(cols)
with open(sys.argv[2], "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
' "$PKG_DIR/object/k562_seed1_dual_predictions.tsv" "$TMP_DIR/k562_seed1_dual_predictions.tsv"

if "$PYTHON" "$VERIFIER" "$TMP_DIR/certificate_replogle_k562.json" >/dev/null 2>&1; then
    echo "[ERROR] Verifier unexpectedly passed on corrupted plain-text prediction TSV!" >&2
    exit 1
else
    echo "[PASS] Verifier correctly rejected corrupted plain-text prediction TSV with non-zero exit code."
fi

echo "PASS: all verification and negative-control checks succeeded."
exit 0
