#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs: a C compiler (cc), python3 (standard library) and xz (or python3's lzma module). Last line: PASS or FAIL.
set -u
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
trap 'rm -rf "$T"' EXIT
fail() { echo "$1"; echo FAIL; exit 1; }
cat object/n14_orders.txt.xz > "$T/list.xz" || fail "object parts missing"
python3 -I -B -c 'import hashlib,sys; h=hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest(); print("joined xz sha256", h); sys.exit(0 if h==sys.argv[2] else 1)' "$T/list.xz" a9454cdf3b9a1d0081cef9b7f1ddd2f8d06395c7cb638380054b633113aac205 || fail "the joined object does not match its sha256"
cc -O2 -o "$T/check_condorcet" verify-it-yourself/check_condorcet.c || fail "no C compiler"
if command -v xz >/dev/null 2>&1; then xz -dc "$T/list.xz"; else python3 -I -B -c 'import lzma,shutil,sys; shutil.copyfileobj(lzma.open(sys.argv[1]), sys.stdout.buffer)' "$T/list.xz"; fi | "$T/check_condorcet" 14 27040 object/n14_assignment.txt > "$T/list.out" 2>&1
cat "$T/list.out"
[ "$(tail -n 1 "$T/list.out")" = PASS ] || fail "the list check failed"
python3 -I -B verify-it-yourself/dpcount.py 14 object/n14_assignment.txt 27040 27027 > "$T/dp.out" 2>&1
cat "$T/dp.out"
[ "$(tail -n 1 "$T/dp.out")" = PASS ] || fail "the exact count of D(A) failed"
echo "the list has 27040 distinct orders, all obeying the assignment, and |D(A)| = 27040: the list is exactly D(A)"
echo "27040 > 27026 (Table 4 of arXiv:2601.07336v1, n = 14)"
echo PASS
