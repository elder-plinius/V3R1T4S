#!/bin/sh
# run from the package folder: sh verify-it-yourself/run_checks.sh   (last line PASS or FAIL)
cd "$(dirname "$0")/.." || exit 1
fail() { echo "$1"; echo FAIL; exit 1; }
[ -f object/a334497_37.txt ] || fail "missing object/a334497_37.txt"
sha256sum -c verify-it-yourself/OBJECT_SHA256 >/dev/null 2>&1 || fail "object sha256 mismatch"
python3 verify-it-yourself/check_period.py object/a334497_37.txt || fail "check_period.py did not pass"
echo PASS
