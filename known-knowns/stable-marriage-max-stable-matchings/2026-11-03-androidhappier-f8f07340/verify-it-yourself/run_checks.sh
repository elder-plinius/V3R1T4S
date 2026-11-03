#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh ; last line PASS or FAIL.
# Method 1 (Python, standard library, written from the definition): rotation-lattice walk with per-matching stability
# re-check AND brute-force backtracking over perfect matchings; both must give 412.
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
OUT=$(python3 -I verify-it-yourself/count_stable.py --prefs object/instance_n9.txt --brute --expect 412 2>&1)
echo "$OUT"
echo "$OUT" | grep -q "expected: 412 PASS" || { echo FAIL; exit 1; }
echo "$OUT" | grep -q "brute_count: 412" || { echo FAIL; exit 1; }
# Method 2 (C, optional if no compiler): exhaustive check of all 9! perfect matchings against the definition (allperm.c),
# and ideals of the rotation poset cross-checked by a verified lattice walk (smcount3.c).
if command -v cc >/dev/null 2>&1; then
  if cc -O2 -o verify-it-yourself/allperm verify-it-yourself/allperm.c 2>/dev/null; then
    OUT2=$(./verify-it-yourself/allperm object/instance_n9.txt 2>&1); echo "$OUT2"
    echo "$OUT2" | grep -q "stable_matchings=412$" || { echo FAIL; exit 1; }
  fi
  if cc -O2 -o verify-it-yourself/smcount3 verify-it-yourself/smcount3.c -lm 2>/dev/null; then
    OUT3=$(./verify-it-yourself/smcount3 count object/instance_n9.txt 1 2>&1); echo "$OUT3"
    echo "$OUT3" | grep -q "count_lattice_verified: 412" || { echo FAIL; exit 1; }
    echo "$OUT3" | grep -q "count_poset: 412" || { echo FAIL; exit 1; }
  fi
fi
echo PASS
