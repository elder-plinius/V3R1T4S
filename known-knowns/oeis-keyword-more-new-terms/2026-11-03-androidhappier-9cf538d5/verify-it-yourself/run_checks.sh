#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh   (last line PASS or FAIL)
# Default: Python 3 standard library only, about 1 minute on a laptop.
#   1. sha256 of object/VALUE.txt against the pinned hash (also in INDEX.csv)
#   2. verify_a325786.py: exhaustive count from the definition for n = 1..21; a(1..20) must equal OEIS DATA and
#      a(21) must equal the value in object/VALUE.txt
#   3. negative control: the same count without the necklace test must not reproduce DATA
#   4. if a C compiler is on PATH: build how-we-built-it/pA_neck.c and run it for n = 1..21 (must match step 2)
V=verify-it-yourself
H=how-we-built-it
OBJ=object/VALUE.txt
WANT=9cf538d5a41058aa72a6ce79df5852e594cd1d0c0ff8c68b3354332ec38125c5
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3chk)
trap 'rm -rf "$T"' EXIT
fail=0
echo "== 1. sha256 of $OBJ"
GOT=$(python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$OBJ")
echo "got  $GOT"; echo "want $WANT"
if [ "$GOT" = "$WANT" ]; then echo "sha256: match"; else echo "sha256: MISMATCH"; fail=1; fi
echo "== 2. independent exhaustive count from the definition (n = 1..21)"
python3 $V/verify_a325786.py "$OBJ" > "$T/v.out" 2>&1 || fail=1
cat "$T/v.out"
echo "== 3. negative control: no necklace test"
if python3 $V/verify_a325786.py --no-necklace; then echo "control: unexpectedly reproduced DATA"; fail=1; else echo "control: differs from DATA as expected"; fi
echo "== 4. Program A (C) for n = 1..21"
CC=${CC:-cc}
if command -v "$CC" >/dev/null 2>&1 && "$CC" -O2 -o "$T/pA" $H/pA_neck.c 2>/dev/null; then
  "$T/pA" 1 21 > "$T/pA.out" || fail=1
  grep -E '^[0-9]+ [0-9]+$' "$T/v.out" > "$T/v.pairs"
  if cmp -s "$T/pA.out" "$T/v.pairs"; then echo "pA 1 21 identical to the checker's a(1..21): $(tail -1 "$T/pA.out")"; else echo "pA output differs"; fail=1; fi
else
  echo "skip: no C compiler"
fi
echo "summary: $(cat $OBJ)"
if [ $fail -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
