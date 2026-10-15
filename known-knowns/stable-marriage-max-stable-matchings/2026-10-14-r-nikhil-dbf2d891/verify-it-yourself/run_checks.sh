#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh ; last line PASS or FAIL. Needs a C compiler (cc) and about 2 GB of memory.
# Method 1 (always): memoised count of the ideals of the rotation poset; must print 2497797760 (a few seconds).
# Method 2 (FULL=1 sh verify-it-yourself/run_checks.sh): reverse-search enumeration of every ideal, each converted to its
# matching and re-checked against the stability definition; must report 2497797760 ideals and 0 unstable matchings (about 45
# minutes on one core). The packaging machine ran method 2 as well (see RECEIPTS.md and the panel files).
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
cc -O2 -o verify-it-yourself/smcount3 verify-it-yourself/smcount3.c -lm || { echo FAIL; exit 1; }
OUT=$(MEMO_MAX_STATES=40000000 ./verify-it-yourself/smcount3 count object/instance_n28.txt 0 2>&1); echo "$OUT"
echo "$OUT" | grep -q "count_poset: 2497797760" || { echo FAIL; exit 1; }
if [ "$FULL" = "1" ]; then
  OUT2=$(./verify-it-yourself/smcount3 enumerate object/instance_n28.txt 2>&1); echo "$OUT2"
  echo "$OUT2" | grep -q "enumerated_ideals: 2497797760" || { echo FAIL; exit 1; }
  echo "$OUT2" | grep -q "unstable_matchings_found: 0" || { echo FAIL; exit 1; }
fi
echo PASS
