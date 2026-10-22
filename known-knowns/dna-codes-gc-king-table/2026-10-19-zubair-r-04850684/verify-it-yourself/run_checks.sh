#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
out=$(python3 -I verify-it-yourself/check_gc_code.py object/gc_n10_d7_m44.txt 10 7 34) ; echo "$out"
case "$out" in "VALID size=44 table=34 BEATS") echo PASS ;; *) echo FAIL ;; esac
