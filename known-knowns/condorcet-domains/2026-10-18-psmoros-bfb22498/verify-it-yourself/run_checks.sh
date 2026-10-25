#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs: python3 (standard library). Optional full enumeration (FULL=1): a C compiler and about 10-30 minutes.
set -u
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
trap 'rm -rf "$T"' EXIT
fail() { echo "$1"; echo FAIL; exit 1; }
python3 -I -B -c 'import hashlib,sys; h=hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest(); print("assignment sha256", h)' object/n24_assignment.txt
python3 -I -B verify-it-yourself/dpcount.py 24 object/n24_assignment.txt 81912986 73279873 > "$T/dp.out" 2>&1
cat "$T/dp.out"
[ "$(tail -n 1 "$T/dp.out")" = PASS ] || fail "the exact count of D(A) failed"
if [ "${FULL:-0}" = 1 ]; then
  cc -O3 -o "$T/mdom" verify-it-yourself/mdom.c && cc -O3 -o "$T/mstream" verify-it-yourself/mstream.c || fail "no C compiler"
  "$T/mdom" enum 24 object/n24_assignment.txt 2>/dev/null | "$T/mstream" 24 object/n24_assignment.txt 73279873 > "$T/s.out"
  cat "$T/s.out"; [ "$(tail -n 1 "$T/s.out")" = PASS ] || fail "the streamed check of D(A) failed"
  echo "stream sha256 (expected 54baf18b85aecce8a420ce8c1b7350f86b3bf27590741ba9b23193ca0e4a0605):"; "$T/mdom" enum 24 object/n24_assignment.txt 2>/dev/null | shasum -a 256
fi
echo "D(A) has exactly 81912986 orders; every order of D(A) obeys the never condition its triple has in A"
echo "81912986 > 73279872 (Table 4 of arXiv:2601.07336v1, n = 24)"
echo PASS
