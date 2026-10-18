#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs: a C compiler (cc), python3 (standard library) and xz (or python3's lzma module). Last line: PASS or FAIL.
set -u
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
trap 'rm -rf "$T"' EXIT
fail() { echo "$1"; echo FAIL; exit 1; }
cat object/n15_orders.txt.xz > "$T/list.xz" || fail "object parts missing"
python3 -I -B -c 'import hashlib,sys; h=hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest(); print("joined xz sha256", h); sys.exit(0 if h==sys.argv[2] else 1)' "$T/list.xz" 939915eecbe091921d93805b5d7e72597d24b41d214605edaf2252652fb12b07 || fail "the joined object does not match its sha256"
cc -O2 -o "$T/check_condorcet" verify-it-yourself/check_condorcet.c || fail "no C compiler"
if command -v xz >/dev/null 2>&1; then xz -dc "$T/list.xz"; else python3 -I -B -c 'import lzma,shutil,sys; shutil.copyfileobj(lzma.open(sys.argv[1]), sys.stdout.buffer)' "$T/list.xz"; fi | "$T/check_condorcet" 15 60956 object/n15_assignment.txt > "$T/list.out" 2>&1
cat "$T/list.out"
[ "$(tail -n 1 "$T/list.out")" = PASS ] || fail "the list check failed"
python3 -I -B verify-it-yourself/dpcount.py 15 object/n15_assignment.txt 60956 59431 > "$T/dp.out" 2>&1
cat "$T/dp.out"
[ "$(tail -n 1 "$T/dp.out")" = PASS ] || fail "the exact count of D(A) failed"
echo "the list has 60956 distinct orders, all obeying the assignment, and |D(A)| = 60956: the list is exactly D(A)"
echo "60956 > 59430 (Table 4 of arXiv:2601.07336v1, n = 15)"
echo PASS
