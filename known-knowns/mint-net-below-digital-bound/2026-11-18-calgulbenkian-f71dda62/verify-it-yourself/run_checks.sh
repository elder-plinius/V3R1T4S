#!/bin/sh
DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
CERT="$DIR/object/certificate_b3_m11_s19_t3.json"
VIY="$DIR/verify-it-yourself"

fail_out() {
    echo "FAIL"
    exit 1
}

if [ ! -f "$CERT" ]; then
    echo "Missing object file"
    fail_out
fi

python3 "$VIY/verify_python_exact.py" "$CERT" --corrupt-test || fail_out

TMP_DIR=$(mktemp -d "${TMPDIR:-.}/v3_mint.XXXXXX") || fail_out
cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT INT TERM

CC_BIN="${CC:-cc}"
"$CC_BIN" -O2 -std=c99 -Wall -Wextra -o "$TMP_DIR/verify_c99_int128" "$VIY/verify_c99_int128.c" || fail_out
"$TMP_DIR/verify_c99_int128" "$CERT" --corrupt-test || fail_out

echo "PASS"
exit 0
