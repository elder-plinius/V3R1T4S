#!/bin/sh
# Run from the package folder. Checks the small certificates with all three checkers and the exact tests of the proof steps.
# The full N = 17 check is in RUN_IT_YOURSELF.md. Last output line: PASS or FAIL.
PY=${PYTHON:-python3}
$PY -I - <<'EOF' || { echo FAIL; exit 1; }
import hashlib,json
h=json.load(open('verify-it-yourself/object_hashes.json'))
for f,v in h.items():
    assert hashlib.sha256(open('object/'+f,'rb').read()).hexdigest()==v,f
print('object hashes ok')
EOF
T=$(mktemp -d) || { echo FAIL; exit 1; }
for c in check_a17 check_d check_e; do
  cc -O2 -D_FILE_OFFSET_BITS=64 -o "$T/$c" verify-it-yourself/$c.c || { echo FAIL; rm -rf "$T"; exit 1; }
done
for row in "3 12326115" "4 12621691" "5 12776965" "8 13020558"; do
  set -- $row
  O="object/small/c$1.counts object/small/c$1.states object/small/c$1.V"
  for c in check_a17 check_d check_e; do
    "$T/$c" $1 16777216 $2 $O | tail -1 | grep -q ACCEPT || { echo "$c N=$1 refused"; echo FAIL; rm -rf "$T"; exit 1; }
    if "$T/$c" $1 16777216 $(($2+1)) $O >/dev/null 2>&1; then echo "$c accepted m+1 at N=$1"; echo FAIL; rm -rf "$T"; exit 1; fi
    if "$T/$c" $1 16777216 $2 $O perturb >/dev/null 2>&1; then echo "$c accepted perturb at N=$1"; echo FAIL; rm -rf "$T"; exit 1; fi
    if "$T/$c" $1 16777216 $2 $O drop >/dev/null 2>&1; then echo "$c accepted drop at N=$1"; echo FAIL; rm -rf "$T"; exit 1; fi
  done
  echo "N=$1 m=$2 accepted by three checkers; m+1, perturb and drop refused by all three"
done
rm -rf "$T"
$PY -I verify-it-yourself/lemma1_small.py | tail -1 | grep -q True || { echo FAIL; exit 1; }
echo "Lemma 1 small cases hold"
for row in "3 12326115" "4 12621691" "5 12776965"; do
  set -- $row
  OUT=$($PY -I verify-it-yourself/exact_small.py $1 object/small_old/c$1.states object/small_old/c$1.V 16777216 $2 10) || { echo FAIL; exit 1; }
  echo "$OUT" | grep -q "all starts: True" || { echo "$OUT"; echo FAIL; exit 1; }
  echo "$OUT" | grep -q "ok=True" || { echo "$OUT"; echo FAIL; exit 1; }
  echo "$OUT" | grep -q "violations of F_p<=LCS: 0" || { echo "$OUT"; echo FAIL; exit 1; }
  echo "exact tests N=$1 ok"
done
echo PASS
