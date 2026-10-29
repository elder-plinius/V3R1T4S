#!/bin/sh
set -eu
PY="python3"
if [ -x "/opt/homebrew/bin/python3" ]; then
    PY="/opt/homebrew/bin/python3"
fi

CSV_URL="https://raw.githubusercontent.com/OrensteinLab/10-minimizers/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/GM%20paper%20densities/k_extension_k16_w12.csv"
CSV_SHA256="88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa"
GM_URL="https://raw.githubusercontent.com/OrensteinLab/10-minimizers/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/GM/w12_k3.gm"
GM_SHA256="c592519b57ad8104860b7e1559b28c2d37ef329db82298b151a65e056ce27f1d"

FETCH_DIR="$(mktemp -d)"
trap 'rm -rf "$FETCH_DIR"' EXIT

if ! curl -fsSL "$CSV_URL" -o "$FETCH_DIR/k_extension_k16_w12.csv" || ! curl -fsSL "$GM_URL" -o "$FETCH_DIR/published_w12_k3.gm"; then
    echo "ERROR: failed to fetch upstream reference files"
    echo "FAIL"
    exit 1
fi

"$PY" - "$FETCH_DIR/k_extension_k16_w12.csv" "$CSV_SHA256" "$FETCH_DIR/published_w12_k3.gm" "$GM_SHA256" << 'EOF'
import hashlib, sys
for path, expected in [(sys.argv[1], sys.argv[2]), (sys.argv[3], sys.argv[4])]:
    with open(path, "rb") as f:
        actual = hashlib.sha256(f.read()).hexdigest()
    if actual != expected:
        print(f"ERROR: sha256 mismatch for {path}: got {actual}, expected {expected}")
        print("FAIL")
        sys.exit(1)
EOF

"$PY" verify-it-yourself/author_checker_minimizer_check.py object/w12_k3_improved.gm "$FETCH_DIR/published_w12_k3.gm" "$FETCH_DIR/k_extension_k16_w12.csv"
