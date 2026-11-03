#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh   (last line PASS or FAIL)
# Default: Python 3 standard library only, under 1 s on a laptop.
#   1. sha256 of object/ROW6.txt and object/VALUE.txt against the pinned hashes (ROW6 also in INDEX.csv)
#   2. verify_a131449.py: all rooted ordered trees with n <= 6 non-root vertices as nested tuples, increasing
#      labelings counted by a recursive multinomial from the definition; indices 0..65 must equal OEIS DATA,
#      row lengths Catalan(n), row sums (2n-1)!!, row 6 = object/ROW6.txt, index 66 = object/VALUE.txt = 360
#   3. negative control: dropping "increasing" (n! per tree) must not reproduce DATA
#   4. if a C compiler is on PATH: build how-we-built-it/pB_c/progB.c, run it to n = 6; its row 6 must match the object
V=verify-it-yourself
H=how-we-built-it
OBJ=object/ROW6.txt
VAL=object/VALUE.txt
WANT=c3661e45bbff1f5a2fb05098c2940739a0d096689e593c1095142858cb66f120
WANTV=f60260e656ad57721144aa337d701695322e53d2973b6ff8b384cd0d331bc382
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3chk)
trap 'rm -rf "$T"' EXIT
fail=0
sha() { python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$1"; }
echo "== 1. sha256 of $OBJ and $VAL"
GOT=$(sha "$OBJ"); GOTV=$(sha "$VAL")
echo "got  $GOT"; echo "want $WANT"
if [ "$GOT" = "$WANT" ] && [ "$GOTV" = "$WANTV" ]; then echo "sha256: match"; else echo "sha256: MISMATCH"; fail=1; fi
echo "== 2. independent count from the definition (n = 0..6)"
python3 $V/verify_a131449.py "$OBJ" "$VAL" || fail=1
echo "== 3. negative control: labelings without the increasing condition"
if python3 $V/verify_a131449.py --control; then echo "control: unexpectedly reproduced DATA"; fail=1; else echo "control: differs from DATA as expected"; fi
echo "== 4. Program B (C) row 6"
CC=${CC:-cc}
if command -v "$CC" >/dev/null 2>&1 && "$CC" -O2 -o "$T/pB" $H/pB_c/progB.c 2>/dev/null; then
  "$T/pB" 6 > "$T/pB.out" 2>/dev/null || fail=1
  B6=$(awk '$1>=65 && $1<=196 {print $2}' "$T/pB.out" | paste -sd, -)
  if [ "$B6" = "$(cat $OBJ)" ]; then echo "pB row 6 identical to $OBJ"; else echo "pB row 6 differs"; fail=1; fi
else
  echo "skip: no C compiler"
fi
echo "summary: A131449 index 66 = $(cat $VAL); row 6 head $(cut -d, -f1-8 $OBJ),..."
if [ $fail -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
