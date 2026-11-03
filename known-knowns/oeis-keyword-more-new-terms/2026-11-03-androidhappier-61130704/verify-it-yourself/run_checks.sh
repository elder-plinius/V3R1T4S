#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh   (last line PASS or FAIL)
# About 30 s on a laptop (pure-Python exhaustive count over all 4,213,597 set partitions of {1..12}).
V=verify-it-yourself
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3chk)
trap 'rm -rf "$T"' EXIT
fail=0
DATA="1 0 3 6 30 96 461 2000 10727 57092 342348"
echo "== 1. object/VALUE.txt: hash vs INDEX.csv, and the claimed value"
want=$(sed -n 2p INDEX.csv | awk -F, '{print $NF}')
got=$(python3 -c "import hashlib,sys;print(hashlib.sha256(open('object/VALUE.txt','rb').read()).hexdigest())")
if [ "$want" = "$got" ]; then echo "sha256 $got ok"; else echo "sha256 mismatch: INDEX $want, file $got"; fail=1; fi
claim=$(sed -n 's/^A361864(12) = \([0-9][0-9]*\)$/\1/p' object/VALUE.txt)
[ -n "$claim" ] || { echo "object/VALUE.txt does not read 'A361864(12) = <number>'"; fail=1; }
echo "claimed a(12) = $claim"
echo "== 2. definition-level exhaustive count, n = 1..12 (Python, exact Fractions)"
python3 $V/check_medmed.py 12 > "$T/py.txt" || fail=1
cat "$T/py.txt"
pyd=$(awk '$1<=11{printf "%s ", $2}' "$T/py.txt" | sed 's/ $//')
py12=$(awk '$1==12{print $2}' "$T/py.txt")
if [ "$pyd" = "$DATA" ]; then echo "a(1..11) = OEIS DATA ok"; else echo "a(1..11) differ from OEIS DATA"; fail=1; fi
if [ -n "$claim" ] && [ "$py12" = "$claim" ]; then echo "a(12) = $py12 = claim ok"; else echo "a(12) = $py12, claim $claim MISMATCH"; fail=1; fi
echo "== 3. Program A (C, restricted growth strings), if a C compiler is present"
CC=${CC:-cc}
if $CC -O2 -o "$T/pA" $V/medmed.c 2>/dev/null; then
  "$T/pA" 1 12 > "$T/c.txt"
  if cmp -s "$T/c.txt" "$T/py.txt"; then echo "C output identical to the Python count ok"; else echo "C output differs"; cat "$T/c.txt"; fail=1; fi
else
  echo "skip: no C compiler; steps 1-2 decide"
fi
echo "summary: A361864(12) = $claim"
if [ $fail -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
