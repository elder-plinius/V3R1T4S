#!/bin/sh
# Verify the seven macro rules in object/rules.json for 1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB.
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs: a Python 3 with sympy (set PYTHON to choose one; default python3) and a C compiler (cc or gcc).
# Last line is PASS or FAIL.
PY=${PYTHON:-python3}
V=verify-it-yourself
CC=$(command -v cc || command -v gcc)
T=$(mktemp -d)
ok=1
fail() { echo "check failed: $1"; ok=0; }
asm() { cat $V/prove.py; printf "RULES_JSON = r'''"; cat object/rules.json; printf "'''\n"; cat "$1"; }
asm $V/main_proofs.py | $PY -u - > $T/proofs.log 2>&1
n=$(grep -c "RESULT .*: PROVED" $T/proofs.log); echo "symbolic proofs: $n of 7 PROVED"; [ "$n" = 7 ] || fail proofs
asm $V/main_controls.py | $PY -u - > $T/controls.log 2>&1
tail -1 $T/controls.log; grep -q "all controls rejected: True" $T/controls.log || fail controls
asm $V/parser_test.py | $PY -u - > $T/parser.log 2>&1
tail -1 $T/parser.log; grep -q "parser test pass: True" $T/parser.log || fail parser
{ printf "RULES_JSON = r'''"; cat object/rules.json; printf "'''\n"; cat $V/bruteforce.py; } | $PY -u - > $T/brute.log 2>&1
grep -E "all real pass|all mutants caught" $T/brute.log
grep -q "all real pass: True" $T/brute.log && grep -q "all mutants caught: True" $T/brute.log || fail bruteforce
$CC -O2 -o $T/replay $V/replay_v2.c || fail compile
$T/replay sim 1RB1LC_1RC1RB_1RD0LE_1LA1LD_---0LA 100000000 > $T/bb5.log 2>&1
grep -q "defined_transitions=47176869" $T/bb5.log && echo "BB(5) champion: 47176869 defined transitions, then halt" || fail bb5
$T/replay rules 1000000000 0 > $T/replay.log 2>&1
tail -1 $T/replay.log; grep -q "TOTAL scheduled=8365935 passed=8365935 failures=0" $T/replay.log || fail replay
$T/replay rules 1000000000 1 > $T/ctl1.log 2>&1; grep -q "passed=0 " $T/ctl1.log || fail "replay control 1"
$T/replay rules 1000000000 2 > $T/ctl2.log 2>&1; grep -q "passed=0 " $T/ctl2.log || fail "replay control 2"
echo "replay controls (steps+1, flipped bit): $(tail -1 $T/ctl1.log | grep -o 'passed=[0-9]*'), $(tail -1 $T/ctl2.log | grep -o 'passed=[0-9]*')"
rm -rf $T
if [ $ok = 1 ]; then echo PASS; exit 0; else echo FAIL; exit 1; fi
