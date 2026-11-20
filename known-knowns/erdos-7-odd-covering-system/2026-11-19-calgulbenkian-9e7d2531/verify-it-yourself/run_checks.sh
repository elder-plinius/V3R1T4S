#!/bin/sh
set -u

DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PKG=$(CDPATH= cd -- "$DIR/.." && pwd)
CERT="$PKG/object/lcm_lower_bound_certificate.tsv"

WORK=$(mktemp -d) || {
    echo "FAIL"
    exit 1
}
cleanup() {
    rm -rf "$WORK"
}
trap cleanup EXIT INT TERM

fail_out() {
    echo "FAIL"
    exit 1
}

CC_BIN=${CC:-cc}
"$CC_BIN" -std=c99 -O2 -Wall -Wextra -Werror -Wpedantic "$DIR/verify_lcm_bound_c.c" -o "$WORK/verify_lcm_bound_c" || fail_out
"$WORK/verify_lcm_bound_c" "$CERT" || fail_out

PY_BIN=${PYTHON:-python3}
"$PY_BIN" "$DIR/verify_lcm_bound_py.py" "$CERT" || fail_out

echo "PASS"
exit 0
