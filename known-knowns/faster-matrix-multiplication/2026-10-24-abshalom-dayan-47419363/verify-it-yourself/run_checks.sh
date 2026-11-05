#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs only python3 (standard library). Last line: PASS or FAIL.
# object/u.txt is stored as two parts (the 1 MB per-file limit); this script joins them, prints the sha256 of the
# three factor files (u.txt must be 47419363...298a, the file the panel checked), then runs both checkers.
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
PY=$(command -v python3 || command -v python)
[ -n "$PY" ] || { echo "no python3 found"; echo FAIL; exit 1; }
T=verify-it-yourself/.assembled
mkdir -p "$T" || { echo FAIL; exit 1; }
cat object/u.part1.txt object/u.part2.txt > "$T/u.txt" && cp object/v.txt object/w.txt "$T/" || { echo FAIL; exit 1; }
"$PY" -I -c "import hashlib,sys
for f in ('u.txt','v.txt','w.txt'): print(hashlib.sha256(open(sys.argv[1]+'/'+f,'rb').read()).hexdigest(), f)" "$T"
echo "== exact Brent-equation check (check_scheme.py)"
"$PY" -I verify-it-yourself/check_scheme.py "$T" > verify-it-yourself/.out1.txt 2>&1; s1=$?
cat verify-it-yourself/.out1.txt
echo "== random exact evaluation against AB (check_random_eval.py)"
"$PY" -I verify-it-yourself/check_random_eval.py "$T" 3 > verify-it-yourself/.out2.txt 2>&1; s2=$?
cat verify-it-yourself/.out2.txt
rm -f verify-it-yourself/.out1.txt verify-it-yourself/.out2.txt "$T/u.txt" "$T/v.txt" "$T/w.txt"
rmdir "$T"
if [ "$s1" -eq 0 ] && [ "$s2" -eq 0 ]; then echo PASS; exit 0; fi
echo FAIL; exit 1
