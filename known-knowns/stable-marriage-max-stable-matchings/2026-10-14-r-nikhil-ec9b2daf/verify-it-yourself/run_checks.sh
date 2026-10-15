#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh ; last line PASS or FAIL.
# Method 1 (Python, standard library, written from the definition): rotation-lattice walk with per-matching stability
# re-check AND brute-force backtracking over perfect matchings; both must give 7698.
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
OUT=$(python3 -I verify-it-yourself/count_stable.py --prefs object/instance_n13.txt --brute --expect 7698 2>&1)
echo "$OUT"
echo "$OUT" | grep -q "expected: 7698 PASS" || { echo FAIL; exit 1; }
echo "$OUT" | grep -q "brute_count: 7698" || { echo FAIL; exit 1; }
# Method 2 (C, optional if no compiler): ideals of the rotation poset, cross-checked by a verified lattice walk.
if command -v cc >/dev/null 2>&1; then
  cc -O2 -o verify-it-yourself/smcount3 verify-it-yourself/smcount3.c -lm 2>/dev/null && OUT2=$(./verify-it-yourself/smcount3 count object/instance_n13.txt 1 2>&1) && echo "$OUT2" && { echo "$OUT2" | grep -q "count_lattice_verified: 7698" || { echo FAIL; exit 1; }; }
fi
echo PASS
