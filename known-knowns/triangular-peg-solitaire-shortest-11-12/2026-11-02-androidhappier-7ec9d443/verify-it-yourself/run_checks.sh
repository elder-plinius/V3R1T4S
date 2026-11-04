#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh   (a few seconds; last line PASS or FAIL)
# Needs python3 (standard library only); a C compiler (cc, or $CC) for the C simulator, skipped without one.
PYTHONDONTWRITEBYTECODE=1; export PYTHONDONTWRITEBYTECODE
V=verify-it-yourself
F=$V/fixtures
OBJ=object/T12_25moves.txt
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3chk)
trap 'rm -rf "$T"' EXIT
fail=0
expect() { # expect <label> <wanted exit 0|1> <grep pattern> <command...>
  lab=$1; want=$2; pat=$3; shift 3
  out=$("$@" 2>&1); rc=$?
  [ $rc -ne 0 ] && rc=1
  if [ $rc -eq $want ] && printf '%s\n' "$out" | grep -q -- "$pat"; then echo "ok   $lab: $out"; else echo "BAD  $lab: $out (exit $rc)"; fail=1; fi
}
echo "== 1. object: solution hash vs INDEX.csv, and object/BOUND.txt recomputed from the solution"
python3 $V/check_bound.py || fail=1
echo "== 2. standalone checker (explicit start vacancy a3): 25 moves, 76 jumps, one peg at j12, no mergeable moves"
expect "check_peg T12" 0 "moves=25 jumps=76 pegs_left=1 finish=j12 merges=0 VALID" python3 $V/check_peg.py 12 $OBJ a3 25 j12
echo "== 3. second simulator (Python, vacancy inferred from the first jump)"
expect "pegcheck T12" 0 "start_vacancy=a3 pegs_left=1 finish=j12 jumps=76 moves=25 VALID" python3 $V/pegcheck.py 12 $OBJ
echo "== 4. third simulator (C, cube coordinates)"
CC=${CC:-cc}
if $CC -O2 -o "$T/pegsim2" $V/pegsim2.c 2>/dev/null; then
  expect "pegsim2 T12" 0 "jumps=76 moves=25 pegs_left=1 VALID" "$T/pegsim2" 12 $OBJ
else
  echo "skip: no C compiler; steps 1-3 and 5 still decide"
  : > "$T/nocc"
fi
echo "== 5. calibration on G. I. Bell's published solutions (expect VALID with his move counts) and two corrupted T11 orders (expect ILLEGAL)"
for spec in "9 bell_T9_16 a2 16 i9" "10 bell_T10_18 a3 18 c6" "11 bell_T11_28 a4 28 a1" "12 bell_T12_29 e11 29 a3"; do
  set -- $spec
  expect "check_peg $2" 0 "moves=$4 .*finish=$5 merges=0 VALID" python3 $V/check_peg.py $1 $F/$2.txt $3 $4 $5
  expect "pegcheck $2" 0 "start_vacancy=$3 .*finish=$5 .*moves=$4 VALID" python3 $V/pegcheck.py $1 $F/$2.txt
  [ -f "$T/nocc" ] || expect "pegsim2 $2" 0 "moves=$4 pegs_left=1 VALID" "$T/pegsim2" $1 $F/$2.txt
done
for neg in neg_T11_swapped neg_T11_order; do
  expect "check_peg $neg" 1 "ILLEGAL" python3 $V/check_peg.py 11 $F/$neg.txt a4
  expect "pegcheck $neg" 1 "ILLEGAL" python3 $V/pegcheck.py 11 $F/$neg.txt
  [ -f "$T/nocc" ] || expect "pegsim2 $neg" 1 "ILLEGAL" "$T/pegsim2" 11 $F/$neg.txt
done
echo "summary: Triangle(12) a3 -> j12 in 25 moves, so A127500(12) <= 25 (published upper bound 29)"
if [ $fail -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
