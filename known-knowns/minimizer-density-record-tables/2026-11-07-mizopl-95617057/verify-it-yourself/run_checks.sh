#!/bin/sh
set -eu
PY="python3"
if [ -x "/opt/homebrew/bin/python3" ]; then
    PY="/opt/homebrew/bin/python3"
fi

MIN_TXT_URL="https://raw.githubusercontent.com/OrensteinLab/Minimizers/7b9430fce07a1fcf6b0fe023e9c7c135d6a5bf46/lowest-density/binary/individual-orders/ranks/k4-w12.txt"
MIN_TXT_SHA256="9a8f7447e569399a594588e695a963da59078b34cf4aac23a6fd3d998d06d877"
CSV_URL="https://raw.githubusercontent.com/OrensteinLab/10-minimizers/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/GM%20paper%20densities/k_extension_k16_w12.csv"
CSV_SHA256="88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa"
GM_URL="https://raw.githubusercontent.com/OrensteinLab/10-minimizers/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/GM/w12_k4.gm"
GM_SHA256="7c04487e1489e8d37302230424f32522f3c9af537680c631bf2fa"
GM_SHA256="7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131"

FETCH_DIR="$(mktemp -d)"
trap 'rm -rf "$FETCH_DIR"' EXIT

if ! curl -fsSL "$MIN_TXT_URL" -o "$FETCH_DIR/k4-w12.txt" || \
   ! curl -fsSL "$CSV_URL" -o "$FETCH_DIR/k_extension_k16_w12.csv" || \
   ! curl -fsSL "$GM_URL" -o "$FETCH_DIR/published_w12_k4.gm"; then
    echo "ERROR: failed to fetch upstream reference files"
    echo "FAIL"
    exit 1
fi

"$PY" - "$FETCH_DIR/k4-w12.txt" "$MIN_TXT_SHA256" "$FETCH_DIR/k_extension_k16_w12.csv" "$CSV_SHA256" "$FETCH_DIR/published_w12_k4.gm" "$GM_SHA256" << 'EOF'
import hashlib, sys
pairs = [
    (sys.argv[1], sys.argv[2]),
    (sys.argv[3], sys.argv[4]),
    (sys.argv[5], sys.argv[6]),
]
for path, expected in pairs:
    with open(path, "rb") as f:
        actual = hashlib.sha256(f.read()).hexdigest()
    if actual != expected:
        print(f"ERROR: sha256 mismatch for {path}: got {actual}, expected {expected}")
        print("FAIL")
        sys.exit(1)
EOF

"$PY" verify-it-yourself/verify.py object/w12_k4_4ary.gm object/w12_k4_4ary.csv "$FETCH_DIR/k4-w12.txt" "$FETCH_DIR/published_w12_k4.gm" "$FETCH_DIR/k_extension_k16_w12.csv"
