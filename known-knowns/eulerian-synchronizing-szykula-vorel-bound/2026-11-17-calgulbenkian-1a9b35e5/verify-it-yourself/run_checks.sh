#!/bin/sh
DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
OBJ="$DIR/object/eulerian_n7_k5_rt24.json"

fail_out() {
    echo "FAIL"
    exit 1
}

if [ ! -f "$OBJ" ]; then
    echo "Missing object file"
    fail_out
fi

python3 "$DIR/verify-it-yourself/verify_python_set_bfs.py" "$OBJ" || fail_out

CC_BIN="${CC:-cc}"
BUILD_DIR=$(mktemp -d "${TMPDIR:-.}/v3_cchk.XXXXXX") || fail_out
cleanup() {
    rm -rf "$BUILD_DIR"
}
trap cleanup EXIT INT TERM

"$CC_BIN" -O2 -std=c99 "$DIR/verify-it-yourself/verify_c_bitmask.c" -o "$BUILD_DIR/verify_c_bitmask" || fail_out
"$BUILD_DIR/verify_c_bitmask" "$OBJ" || fail_out

echo "PASS"
exit 0
