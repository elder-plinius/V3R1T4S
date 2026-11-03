#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh   (last line PASS or FAIL)
# Default: Python 3 standard library only, under 1 s on a laptop.
#   1. sha256 of object/ROW6.txt against the pinned hash (also in INDEX.csv)
#   2. verify_a155520.py: all ordered trees with n <= 6 edges as preorder depth sequences, drawings counted from the
#      definition; rows 1..5 must equal OEIS DATA, row sums Catalan(n), weighted sums A014307(n), row 6 = object
#   3. negative control: counting leaf-deletion sequences (leaves distinguished) must not reproduce DATA
#   4. if a C compiler is on PATH: build how-we-built-it/pB_c/progB.c, run it to n = 6; its row 6 must match the object
V=verify-it-yourself
H=how-we-built-it
OBJ=object/ROW6.txt
PAIRS=object/ROW6_pairs.txt
WANT=9eb90322eeb05dd9fd023d19ae3dc7142c591b06e70bbe00db1e7ece89b706b5
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3chk)
trap 'rm -rf "$T"' EXIT
fail=0
echo "== 1. sha256 of $OBJ"
GOT=$(python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$OBJ")
echo "got  $GOT"; echo "want $WANT"
if [ "$GOT" = "$WANT" ]; then echo "sha256: match"; else echo "sha256: MISMATCH"; fail=1; fi
echo "== 2. independent count from the definition (n = 1..6)"
python3 $V/verify_a155520.py "$OBJ" "$PAIRS" || fail=1
echo "== 3. negative control: deletion sequences instead of distinct tree chains"
if python3 $V/verify_a155520.py --seq; then echo "control: unexpectedly reproduced DATA"; fail=1; else echo "control: differs from DATA as expected"; fi
echo "== 4. Program B (C) row 6"
CC=${CC:-cc}
if command -v "$CC" >/dev/null 2>&1 && "$CC" -O2 -o "$T/pB" $H/pB_c/progB.c 2>/dev/null; then
  "$T/pB" 6 > "$T/pB.out" || fail=1
  B6=$(awk '$1=="6" {sub(/.*row: /,""); print}' "$T/pB.out")
  if [ "$B6" = "$(cat $OBJ)" ]; then echo "pB row 6 identical to $OBJ"; else echo "pB row 6 differs"; fail=1; fi
else
  echo "skip: no C compiler"
fi
echo "summary: A155520 row 6 = $(cat $OBJ); A(6,1) = $(cut -d, -f1 $OBJ)"
if [ $fail -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
