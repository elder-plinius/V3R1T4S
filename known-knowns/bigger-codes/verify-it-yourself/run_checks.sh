#!/bin/sh
# Check the 30 codes and the 5 Delsarte certificates; compare file hashes with INDEX.csv / INDEX_delsarte.csv.
# About 10 minutes single-threaded on an idle machine.  Exit 0 iff everything passes.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
SECTION=known-knowns/bigger-codes
CONTRACT="$HERE/../check_harness_contract.py"
[ -f "$CONTRACT" ] || { echo "missing known-knowns/check_harness_contract.py (keep the shared helper with this family)"; exit 2; }
require() {  # input files must be present
  for o in "$@"; do
    [ -f "$HERE/$o" ] || { echo "missing $SECTION/$o"; exit 2; }
  done
}
require codes/A29_6_11_41219.txt codes/A29_6_12_61823.txt
python3 "$CONTRACT" inventory --root "$HERE" || { echo "SOME CHECK FAILED"; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
fail=0
check_dir() {  # dir-with-codes index-csv path-prefix
  for f in "$1"/A*.txt; do
    b=$(basename "$f" .txt); set -- "$1" "$2" "$3" $(echo "$b" | sed 's/^A//; s/_/ /g')
    echo "== $3$b.txt"
    echo "sha256 verified by inventory preflight"
    python3 "$HERE/verify-it-yourself/cwcheck.py" "$f" "$4" "$5" "$6" --M "$7" || fail=1
  done
}
check_dir "$HERE/codes" "$HERE/INDEX.csv" "codes/"
echo "== Delsarte certificates"
python3 "$HERE/verify-it-yourself/delsarte_check.py" "$HERE"/certificates/cert_A*.json || fail=1
[ $fail = 0 ] && echo "ALL CHECKS PASSED" || echo "SOME CHECK FAILED"
exit $fail
