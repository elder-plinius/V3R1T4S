#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh ; last line PASS or FAIL. Needs a C compiler (cc).
# Method 1: reverse-search enumeration of every ideal of the rotation poset, each converted to its matching and re-checked
# against the stability definition (memory O(rotations)); must report 530528 ideals and 0 unstable matchings.
# Method 2 (n <= 25): memoised ideal count cross-checked by a visited-set lattice walk with per-matching re-check.
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
cc -O2 -o verify-it-yourself/smcount3 verify-it-yourself/smcount3.c -lm || { echo FAIL; exit 1; }
OUT=$(./verify-it-yourself/smcount3 enumerate object/instance_n18.txt 2>&1); echo "$OUT"
echo "$OUT" | grep -q "enumerated_ideals: 530528" || { echo FAIL; exit 1; }
echo "$OUT" | grep -q "unstable_matchings_found: 0" || { echo FAIL; exit 1; }
echo "$OUT" | grep -q "agree: yes" || { echo FAIL; exit 1; }
  OUT1=$(./verify-it-yourself/smcount3 count object/instance_n18.txt 1 2>&1); echo "$OUT1"; echo "$OUT1" | grep -q "count_lattice_verified: 530528" || { echo FAIL; exit 1; }
echo PASS
