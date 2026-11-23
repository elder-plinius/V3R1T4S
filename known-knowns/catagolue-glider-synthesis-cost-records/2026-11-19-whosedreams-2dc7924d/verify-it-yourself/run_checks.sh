#!/bin/sh
# run from the package folder: sh verify-it-yourself/run_checks.sh   (last line PASS or FAIL)
cd "$(dirname "$0")/.." || exit 1
fail() { echo "$1"; echo FAIL; exit 1; }
[ -f object/xs25_69ar1mkiczx643.rle ] || fail "missing object/xs25_69ar1mkiczx643.rle"
python3 verify-it-yourself/life_check.py --rle object/xs25_69ar1mkiczx643.rle --target xs25_69ar1mkiczx643 --table-cost 49 > verify-it-yourself/.last_run.txt 2>&1
st=$?
grep -v '^PASS$' verify-it-yourself/.last_run.txt
rm -f verify-it-yourself/.last_run.txt
[ $st -eq 0 ] || fail "life_check.py did not pass"
sha256sum -c verify-it-yourself/OBJECT_SHA256 >/dev/null 2>&1 || fail "object sha256 mismatch"
echo PASS
