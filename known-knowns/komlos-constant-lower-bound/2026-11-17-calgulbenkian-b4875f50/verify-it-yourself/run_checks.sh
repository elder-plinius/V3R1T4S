#!/bin/sh
DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
OBJ="$DIR/object/komlos_15x15_p2.txt"
VIY="$DIR/verify-it-yourself"

fail_out() {
    echo "FAIL"
    exit 1
}

if [ ! -f "$OBJ" ]; then
    echo "Missing object file"
    fail_out
fi

python3 "$VIY/check_komlos_py.py" "$OBJ" || fail_out

TMP_DIR=$(mktemp -d "${TMPDIR:-.}/v3_komlos.XXXXXX") || fail_out
cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT INT TERM

CC_BIN="${CC:-cc}"
"$CC_BIN" -O3 -std=c99 "$VIY/check_komlos_c.c" -o "$TMP_DIR/check_komlos_c" || fail_out
COUT=$("$TMP_DIR/check_komlos_c" "$OBJ" 2>&1) || { echo "$COUT"; fail_out; }
echo "$COUT"
case "$COUT" in
    *"exact_disc=2059565086610/1000000000000"*"p1=1 p2=1"*) ;;
    *) echo "C verifier output mismatch"; fail_out ;;
esac

echo "PASS"
exit 0
