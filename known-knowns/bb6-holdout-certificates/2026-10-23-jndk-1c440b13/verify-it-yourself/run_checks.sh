#!/bin/sh
set -u
TMP=".runcheck.$$"
fail() {
    echo FAIL
    exit 1
}
if ! mkdir "$TMP"; then
    echo FAIL
    exit 1
fi
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
if ! python3 verify-it-yourself/check_bundle.py "$TMP/expanded"; then
    fail
fi
if ! python3 "$TMP/expanded/claim/verify.py" --out "$TMP/replay"; then
    fail
fi
echo PASS
