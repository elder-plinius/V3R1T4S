#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs only python3 (standard library). Last line: PASS or FAIL.
# object/u.txt and object/v.txt are stored as two parts each (the 1 MB per-file limit); this script joins them,
# checks the sha256 of the three factor files against the files the panel checked (FAIL on any other file), then runs
# both checkers.
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
PY=$(command -v python3 || command -v python)
[ -n "$PY" ] || { echo "no python3 found"; echo FAIL; exit 1; }
T=$(mktemp -d "${TMPDIR:-/tmp}/assembled.XXXXXX") || { echo FAIL; exit 1; }
cat object/u.part1.txt object/u.part2.txt > "$T/u.txt" && cat object/v.part1.txt object/v.part2.txt > "$T/v.txt" && cp object/w.txt "$T/" || { echo FAIL; exit 1; }
"$PY" -I -c "import hashlib,sys
want={'u.txt':'abae4fc7429a9c3b715405717c52e2dfcd36ab0f41cd137f3e1327252b1ff56e','v.txt':'a05bcf35e2018bde9600457e4776483969b8b6c0de6c3a1463847f8ca3ae08bb','w.txt':'041992e80c316daa766acecffae71c0c7839fa5f189c77365109f2e63fe7c32d'}
bad=0
for f in ('u.txt','v.txt','w.txt'):
    h=hashlib.sha256(open(sys.argv[1]+'/'+f,'rb').read()).hexdigest(); ok=h==want[f]; bad+=not ok
    print(h, f, 'matches' if ok else 'MISMATCH')
sys.exit(1 if bad else 0)" "$T" || { rm -rf "$T"; echo "sha256 mismatch: not the files the panel checked"; echo FAIL; exit 1; }
echo "== exact Brent-equation check (check_scheme.py)"
"$PY" -I verify-it-yourself/check_scheme.py "$T" > "$T/out1.txt" 2>&1; s1=$?
cat "$T/out1.txt"
echo "== random exact evaluation against AB (check_random_eval.py)"
"$PY" -I verify-it-yourself/check_random_eval.py "$T" 3 > "$T/out2.txt" 2>&1; s2=$?
cat "$T/out2.txt"
rm -rf "$T"
if [ "$s1" -eq 0 ] && [ "$s2" -eq 0 ]; then echo PASS; exit 0; fi
echo FAIL; exit 1
