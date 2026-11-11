#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs: python3 (standard library). Optional full enumeration (FULL=1): a C compiler and about 20-60 minutes.
set -u
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
trap 'rm -rf "$T"' EXIT
fail() { echo "$1"; echo FAIL; exit 1; }
python3 -I -B -c 'import hashlib,sys; h=hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest(); print("assignment sha256", h)' object/n25_assignment.txt
python3 -I -B verify-it-yourself/dpcount.py 25 object/n25_assignment.txt 178950728 160316047 > "$T/dp.out" 2>&1
cat "$T/dp.out"
[ "$(tail -n 1 "$T/dp.out")" = PASS ] || fail "the exact count of D(A) failed"
if [ "${FULL:-0}" = 1 ]; then
  cc -O3 -o "$T/mdom" verify-it-yourself/mdom.c && cc -O3 -o "$T/mstream" verify-it-yourself/mstream.c || fail "no C compiler"
  "$T/mdom" enum 25 object/n25_assignment.txt 2>/dev/null | "$T/mstream" 25 object/n25_assignment.txt 160316047 > "$T/s.out"
  cat "$T/s.out"; [ "$(tail -n 1 "$T/s.out")" = PASS ] || fail "the streamed check of D(A) failed"
  echo "stream sha256 (expected 2ac0df90378e94892f7af7dc8df27581428be20fb21e90edfc751fee5246bd38):"; "$T/mdom" enum 25 object/n25_assignment.txt 2>/dev/null | shasum -a 256
fi
echo "D(A) has exactly 178950728 orders; every order of D(A) obeys the never condition its triple has in A"
echo "178950728 > 160316046 (Table 4 of arXiv:2601.07336v1, n = 25)"
echo PASS
