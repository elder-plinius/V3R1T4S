#!/bin/sh
# run from the package folder: sh verify-it-yourself/run_checks.sh   (last line PASS or FAIL)
cd "$(dirname "$0")/.." || exit 1
# Every file under object/ must match its digest; any one-digit flip must fail.
fail() { echo "$1"; echo FAIL; exit 1; }
[ -f object/minimisers.txt ] || fail "missing object/minimisers.txt"
sha256sum -c verify-it-yourself/OBJECT_SHA256 >/dev/null 2>&1 || fail "object sha256 mismatch"
# Also require the listed k=6 onset digit to appear (semantic check beyond hash)
grep -q '^k=6 onset=139 ' object/minimisers.txt || fail "k=6 line missing or altered"
python3 verify-it-yourself/verify.py object/minimisers.txt || fail "verify.py failed"
