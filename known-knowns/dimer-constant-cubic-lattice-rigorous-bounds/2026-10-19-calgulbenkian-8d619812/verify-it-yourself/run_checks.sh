#!/bin/sh
# Integrity first: every object/ file must match the package SHA256SUMS (added by the orchestrator, 2026-10-19).
_PKG=$(cd "$(dirname "$0")/.." && pwd)
if command -v shasum >/dev/null 2>&1; then _S="shasum -a 256"; else _S="sha256sum"; fi
( cd "$_PKG" && grep "  object/" SHA256SUMS > "${TMPDIR:-/tmp}/objsums.$$" && $_S -c "${TMPDIR:-/tmp}/objsums.$$" >/dev/null 2>&1 ) || { echo "object file sha256 MISMATCH against SHA256SUMS"; echo "FAIL"; exit 1; }
echo "all object/ files match SHA256SUMS"
# Checks for the l3 upper bound at (5,5).  python3 (3.8 or later), standard library only, for the default check.
# DEFAULT RUN checks in Python: the object (sha256), the trace identity, property C, and SECTOR 12 (the headline sector) exactly.
# If a C compiler exists it ALSO checks all 13 sectors with cwsec.c (sector 12 with the shipped vector, sectors 0..11 with sectors/*.txt).
# Without a C compiler, sectors 0..11 can be checked in Python with CW_SMALL=1 (slow: about 5 minutes for sector 11 on 16 processes).
# CW_PROCS=n sets the number of Python worker processes (default: all CPUs).
cd "$(dirname "$0")" || exit 1
python3 -I check_main.py || { echo "SOME CHECK FAILED"; exit 1; }
if command -v cc >/dev/null 2>&1; then
  T=$(mktemp -d)
  cat ../object/cert_he_55_converged_sector12.txt.part1 ../object/cert_he_55_converged_sector12.txt.part2 ../object/cert_he_55_converged_sector12.txt.part3 > "$T/cert12.txt"
  cc -O2 -o "$T/cwsec" cwsec.c -lpthread || exit 1
  "$T/cwsec" check 5 5 12 "$T/cert12.txt" > "$T/c.out" || exit 1
  grep -E '^(CHECK sector|LISTED)' "$T/c.out"
  for i in 0 1 2 3 4 5 6 7 8 9 10 11; do "$T/cwsec" check 5 5 $i sectors/vec_55_s$i.txt | grep -E '^CHECK sector' >> "$T/c.out"; done
  python3 -I c_aggregate.py "$T/c.out"; R=$?
  python3 -I -c "
import os,sys
d=sys.argv[1]
for f in os.listdir(d): os.remove(os.path.join(d,f))
os.rmdir(d)" "$T"
  [ $R -eq 0 ] || { echo "SOME CHECK FAILED"; exit 1; }
else
  echo "NOTE no C compiler: only sector 12 was checked (Python); sectors 0..11 need CW_SMALL=1 or a compiler"
fi
echo "ALL CHECKS PASS"
