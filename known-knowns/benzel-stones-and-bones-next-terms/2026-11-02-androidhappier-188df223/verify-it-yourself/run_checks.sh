#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Optional: NMAX=16 sh verify-it-yourself/run_checks.sh  (fresh C runs up to n = NMAX instead of 14; n=16 adds ~2 min)
# Last line: PASS or FAIL.
V=verify-it-yourself
NMAX=${NMAX:-14}
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3chk)
trap 'rm -rf "$T"' EXIT
fail=0
echo "== 1. object/VALUE.txt: hash vs INDEX.csv, pinned evidence and programs"
python3 $V/check_value.py pins || fail=1
echo "== 2. saved run outputs vs VALUE.txt (n=20 runs A and B, published-term runs, checkpoint test)"
python3 $V/check_value.py evidence || fail=1
echo "== 3. fresh definition-level count (indep_check.py: memoized exact cover, no transfer matrix), n = 3..11"
python3 $V/indep_check.py 11 3 > "$T/indep.txt" || fail=1
awk '$1=="n"{print $3, $2, "indep_check.py", $4; print $5, $2, "indep_check.py", $6}' "$T/indep.txt" > "$T/fresh_indep.txt"
python3 $V/check_value.py fresh "$T/fresh_indep.txt" || fail=1
echo "== 4. fresh runs of the two n=20 programs (benzZQ.c, benzB64.c) on published terms, n = 3..$NMAX"
CC=${CC:-cc}
if $CC -O2 -fopenmp -o "$T/benzZQ" $V/benzZQ.c 2>"$T/cc1.log" && $CC -O2 -fopenmp -o "$T/benzB64" $V/benzB64.c 2>"$T/cc2.log"; then
  : > "$T/fresh_c.txt"
  n=3
  while [ $n -le $NMAX ]; do
    for s in A364416 A364417; do
      if [ $s = A364416 ]; then b=$((2*n-4)); else b=$((2*n-3)); fi
      a=$(BENZ_M=5 "$T/benzZQ" $n $b 3 2>"$T/a.err") || a=ERR
      grep -q "overflow=0" "$T/a.err" || a=OVERFLOW_OR_ERR
      z=$("$T/benzB64" $n $b 3 5 2>"$T/b.err") || z=ERR
      grep -q "overflow 0" "$T/b.err" || z=OVERFLOW_OR_ERR
      echo "$s $n benzZQ.c $a" >> "$T/fresh_c.txt"
      echo "$s $n benzB64.c $z" >> "$T/fresh_c.txt"
    done
    n=$((n+1))
  done
  python3 $V/check_value.py fresh "$T/fresh_c.txt" || fail=1
else
  echo "skip: no C compiler with OpenMP (-fopenmp); steps 1-3 still decide the package checks"
fi
V20=$(sed -n 's/^value: //p' object/VALUE.txt)
echo "summary: A364417(20) = $V20 (two independent programs, saved runs verified; published terms reproduced fresh)"
if [ $fail -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
