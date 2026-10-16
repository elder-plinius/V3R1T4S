#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Python 3 standard library only; nothing is downloaded or written. Last line: PASS or FAIL.
# 1-4: the original exact checkers (b=2 algebraic certificate, universal all-b polynomial identities, ordered-gap sign
#      certificate from the raw payoff table, finite-deck calibrations). 5: an independently written checker
#      (terminal-utility integrator vs closed forms, polynomial identities over Q, b=2 thresholds and value).
set -u
export PYTHONDONTWRITEBYTECODE=1
V=verify-it-yourself; O=object; fails=0
run() { name=$1; shift; out=$("$@" 2>&1); r=$?; last=$(printf '%s\n' "$out" | tail -1); echo "== $name (exit $r): $last"; if [ $r -ne 0 ]; then fails=$((fails+1)); printf '%s\n' "$out" | tail -5; fi; }
run exact_certificate python3 -I $V/exact_certificate.py $O/equilibrium.json
run universal_check python3 -I $V/universal_check.py $O/universal.json
run ordered_cone_check python3 $V/ordered_cone_check.py $O/raw_payoffs.txt
run finite_calibration python3 -I $V/finite_calibration.py
run independent_check python3 -I $V/independent_check.py
if [ $fails -eq 0 ]; then echo PASS; else echo "FAIL ($fails checker(s) failed)"; echo FAIL; exit 1; fi
