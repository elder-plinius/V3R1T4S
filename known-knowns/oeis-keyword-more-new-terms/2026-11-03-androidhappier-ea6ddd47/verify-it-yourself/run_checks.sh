#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh   (last line PASS or FAIL)
# Default: Python 3 standard library only, a few seconds on a laptop.
#   1. sha256 of object/VALUE.txt against the pinned hash (also in INDEX.csv)
#   2. verify_a214570.py: (a) all ordered trees with n <= 10 vertices as nested tuples, grouped by rooted-tree class
#      (pure definition); (b) every rooted tree with n <= 17 vertices built once as a multiset of smaller trees,
#      c(t) = deg!/prod(mult!) * prod c(child); self-checks #trees = A000081(n), sum c(t) = Catalan(n-1);
#      a(1..16) must equal OEIS DATA and a(17) must equal object/VALUE.txt
#   3. negative control: dropping the multiplicity division must not reproduce DATA
#   4. if a C compiler is on PATH: build how-we-built-it/pB_c/progB.c, run it to n = 17; its a(17) must match the object
V=verify-it-yourself
H=how-we-built-it
VAL=object/VALUE.txt
WANT=ea6ddd47e1fce10db26cc83619ee6f58bbaac89d49bc9fc9c559aa68d54c4456
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3chk)
trap 'rm -rf "$T"' EXIT
fail=0
sha() { python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$1"; }
echo "== 1. sha256 of $VAL"
GOT=$(sha "$VAL")
echo "got  $GOT"; echo "want $WANT"
if [ "$GOT" = "$WANT" ]; then echo "sha256: match"; else echo "sha256: MISMATCH"; fail=1; fi
echo "== 2. independent count from the definition (n = 1..17)"
python3 $V/verify_a214570.py "$VAL" || fail=1
echo "== 3. negative control: no multiplicity division"
if python3 $V/verify_a214570.py --control; then echo "control: unexpectedly reproduced DATA"; fail=1; else echo "control: differs from DATA as expected"; fi
echo "== 4. Program B (C) a(17)"
CC=${CC:-cc}
if command -v "$CC" >/dev/null 2>&1 && "$CC" -O2 -o "$T/pB" $H/pB_c/progB.c 2>/dev/null; then
  "$T/pB" 17 > "$T/pB.out" 2>/dev/null || fail=1
  B17=$(awk '$1==17 {print $2}' "$T/pB.out")
  if [ "$B17" = "$(cat $VAL)" ]; then echo "pB a(17) = $B17 identical to $VAL"; else echo "pB a(17) = $B17 differs"; fail=1; fi
  if cmp -s "$T/pB.out" $H/outputs/progB_17.out; then echo "pB output identical to $H/outputs/progB_17.out"; else echo "pB output differs from saved output"; fail=1; fi
else
  echo "skip: no C compiler"
fi
echo "summary: A214570(17) = $(cat $VAL)"
if [ $fail -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
