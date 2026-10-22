#!/bin/sh
# Integrity first: every object/ file must match the package SHA256SUMS (added by the orchestrator, 2026-10-19).
_PKG=$(cd "$(dirname "$0")/.." && pwd)
if command -v shasum >/dev/null 2>&1; then _S="shasum -a 256"; else _S="sha256sum"; fi
( cd "$_PKG" && grep "  object/" SHA256SUMS > "${TMPDIR:-/tmp}/objsums.$$" && $_S -c "${TMPDIR:-/tmp}/objsums.$$" >/dev/null 2>&1 ) || { echo "object file sha256 MISMATCH against SHA256SUMS"; echo "FAIL"; exit 1; }
echo "all object/ files match SHA256SUMS"
# Reproduction of He's Table 2.  Python 3.8+ standard library for 11 entries (CW_QUICK=1 skips the slowest, (5,4));
# the (5,5) entry at p = 2 uses cwsec.c (needs a C compiler; libc and pthreads only) for all 13 sectors.
cd "$(dirname "$0")" || exit 1
if command -v cc >/dev/null 2>&1; then
  T=$(mktemp -d)
  cc -O2 -o "$T/cwsec" cwsec.c -lpthread || exit 1
  "$T/cwsec" iter 5 5 2 > "$T/iter55.txt" || { echo "SOME CHECK FAILED"; exit 1; }
  "$T/cwsec" iter 4 4 4 | grep 'sector=8 p=4' | head -1
  python3 -I check_table2.py "$T/iter55.txt"; R=$?
  python3 -I -c "
import os,sys
d=sys.argv[1]
for f in os.listdir(d): os.remove(os.path.join(d,f))
os.rmdir(d)" "$T"
  exit $R
else
  python3 -I check_table2.py
  echo "NOTE no C compiler found: the (5,5) entry was not checked; the line above covers 11 of 12 entries"
fi
