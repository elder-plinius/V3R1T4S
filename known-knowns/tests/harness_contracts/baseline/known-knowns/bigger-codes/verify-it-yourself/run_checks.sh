#!/bin/sh
# Check the 30 codes and the 5 Delsarte certificates; compare file hashes with INDEX.csv / INDEX_delsarte.csv.
# About 10 minutes single-threaded on an idle machine.  Exit 0 iff everything passes.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
SECTION=known-knowns/bigger-codes
require() {  # input files must be present
  for o in "$@"; do
    [ -f "$HERE/$o" ] || { echo "missing $SECTION/$o"; exit 2; }
  done
}
require codes/A29_6_11_41219.txt codes/A29_6_12_61823.txt
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
fail=0
check_dir() {  # dir-with-codes index-csv path-prefix
  for f in "$1"/A*.txt; do
    b=$(basename "$f" .txt); set -- "$1" "$2" "$3" $(echo "$b" | sed 's/^A//; s/_/ /g')
    echo "== $3$b.txt"
    exp=$(grep ",$3$b.txt," "$2" | sed 's/.*,//')
    got=$($SHA "$f" | cut -d' ' -f1)
    [ "$got" = "$exp" ] && echo "sha256 matches $(basename "$2")" || { echo "sha256 MISMATCH ($got)"; fail=1; }
    python3 "$HERE/verify-it-yourself/cwcheck.py" "$f" "$4" "$5" "$6" --M "$7" || fail=1
  done
}
check_dir "$HERE/codes" "$HERE/INDEX.csv" "codes/"
echo "== Delsarte certificates"
python3 "$HERE/verify-it-yourself/delsarte_check.py" "$HERE"/certificates/cert_A*.json || fail=1
for f in "$HERE"/certificates/cert_A*.json; do
  b=$(basename "$f"); exp=$(grep ",certificates/$b," "$HERE/INDEX_delsarte.csv" | sed 's/.*,//'); got=$($SHA "$f" | cut -d' ' -f1)
  [ "$got" = "$exp" ] && echo "sha256 ok $b" || { echo "sha256 MISMATCH for $b"; fail=1; }
done
[ $fail = 0 ] && echo "ALL CHECKS PASSED" || echo "SOME CHECK FAILED"
exit $fail
