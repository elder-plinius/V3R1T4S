#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh ; last line PASS or FAIL.
# Method 1 (Python, standard library): rotation-lattice walk with per-matching stability re-check; must give 206728.
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
OUT=$(python3 -I verify-it-yourself/count_stable.py --prefs object/instance_n17.txt --expect 206728 2>&1)
echo "$OUT"
echo "$OUT" | grep -q "expected: 206728 PASS" || { echo FAIL; exit 1; }
# Method 2 (C, optional if no compiler): ideals of the rotation poset, cross-checked by a verified lattice walk.
if command -v cc >/dev/null 2>&1; then
  cc -O3 -o verify-it-yourself/smcount3 verify-it-yourself/smcount3.c -lm 2>/dev/null && OUT2=$(./verify-it-yourself/smcount3 count object/instance_n17.txt 1 2>&1) && echo "$OUT2" && { echo "$OUT2" | grep -q "count_lattice_verified: 206728" || { echo FAIL; exit 1; }; }
fi
echo PASS
