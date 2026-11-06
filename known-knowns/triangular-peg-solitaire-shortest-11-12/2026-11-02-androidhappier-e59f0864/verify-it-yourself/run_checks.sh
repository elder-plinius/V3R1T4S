#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh   (a few seconds; last line PASS or FAIL)
# Needs python3 (standard library only); a C compiler (cc, or $CC) for step 4, which is skipped without one.
V=verify-it-yourself
F=$V/fixtures
OBJ=object/T11_22moves.txt
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3chk)
trap 'rm -rf "$T"' EXIT
fail=0
expect() { # expect <label> <wanted exit 0|1> <grep pattern> <command...>
  lab=$1; want=$2; pat=$3; shift 3
  out=$("$@" 2>&1); rc=$?
  [ $rc -ne 0 ] && rc=1
  if [ $rc -eq $want ] && printf '%s\n' "$out" | grep -q -- "$pat"; then echo "ok   $lab: $out"; else echo "BAD  $lab: $out (exit $rc)"; fail=1; fi
}
echo "== 1. object hash matches INDEX.csv"
python3 - "$OBJ" <<'PY' || fail=1
import csv, hashlib, sys
rows = list(csv.reader(open("INDEX.csv")))
want = rows[1][rows[0].index("sha256")]
got = hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest()
print("object sha256", got, "ok" if got == want else "MISMATCH (INDEX.csv says %s)" % want)
sys.exit(0 if got == want else 1)
PY
echo "== 2. standalone checker (explicit start vacancy a2): 22 moves, 64 jumps, one peg at j11, no mergeable moves"
expect "check_peg T11" 0 "moves=22 jumps=64 pegs_left=1 finish=j11 merges=0 VALID" python3 $V/check_peg.py 11 $OBJ a2 22 j11
echo "== 3. second simulator (Python, vacancy inferred from the first jump)"
expect "pegcheck T11" 0 "start_vacancy=a2 pegs_left=1 finish=j11 jumps=64 moves=22 VALID" python3 $V/pegcheck.py 11 $OBJ
echo "== 4. third simulator (C, cube coordinates)"
CC=${CC:-cc}
if $CC -O2 -o "$T/pegsim2" $V/pegsim2.c 2>/dev/null; then
  expect "pegsim2 T11" 0 "jumps=64 moves=22 pegs_left=1 VALID" "$T/pegsim2" 11 $OBJ
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
echo "summary: Triangle(11) a2 -> j11 in 22 moves, so A127500(11) <= 22 (published upper bound 28)"
if [ $fail -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
