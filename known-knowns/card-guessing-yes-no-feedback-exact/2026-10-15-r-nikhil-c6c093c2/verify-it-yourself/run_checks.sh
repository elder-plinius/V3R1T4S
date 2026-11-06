#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh ; last line PASS or FAIL. Python 3 standard library only.
# 1. object/values.json is the packaged object (sha256) and lists reduced fractions whose decimals match.
# 2. Certificates are verified on EVERY state against Luo's recursion by verify_cert.py (which recomputes C from (A.1)
#    and reads the claimed value from values.json): the shipped n = 2..9 files, and n = 11 (shipped in <1 MB parts,
#    reassembled with cat). FULL=1 also verifies n = 10, 12 and 13 (shipped in parts; about 6 minutes more);
#    FULL=2 also recomputes P+_{2,11} from scratch with the independent standard-library solver (about 2-3 minutes).
#    Archived certificates n = 14..16 put into object/cert/ as n<n>.txt.gz are verified too (n = 16: 30 min, 1.5 GB).
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
H=$(python3 -c "import hashlib;print(hashlib.sha256(open('object/values.json','rb').read()).hexdigest())")
if [ "$H" != "c6c093c29439e54a3f475c3ef71b274cf402e1d417512bb26c3abc24b678bdf2" ]; then echo "object/values.json does not match the packaged object (sha256 $H)"; echo FAIL; exit 1; fi
python3 - <<'PY' || { echo FAIL; exit 1; }
import json
from math import gcd
from decimal import Decimal, getcontext
getcontext().prec = 40
V = json.load(open('object/values.json'))
assert sorted(int(k) for k in V['values']) == list(range(2, 17)), 'values for n = 2..16 expected'
for n, s in V['values'].items():
    a, b = map(int, s.split('/')); assert gcd(a, b) == 1, 'not reduced: ' + s
    d = Decimal(a) / Decimal(b); assert str(d)[:22] == V['decimal20'][n], 'decimal mismatch for n=' + n
print('values.json: 15 reduced fractions, decimals consistent')
PY
TMP=verify-it-yourself/reassembled_scratch; rm -rf "$TMP"; mkdir -p "$TMP"
verify_one() {  # $1 = n, $2 = file
  v=$(python3 -c "import json;print(json.load(open('object/values.json'))['values']['$1'])")
  OUT=$(python3 -I verify-it-yourself/verify_cert.py "$2" --claimed "$v" 2>&1); echo "$OUT" | tail -2
  echo "$OUT" | tail -1 | grep -q '^PASS$' || { echo "certificate for n=$1 failed"; rm -rf "$TMP"; echo FAIL; exit 1; }
}
for n in 2 3 4 5 6 7 8 9; do verify_one $n object/cert/n$n.txt.gz; done
set_default="11"; [ "${FULL:-0}" -ge 1 ] && set_default="10 11 12 13"
for n in $set_default; do cat object/cert/n$n.txt.gz.part-* > "$TMP/n$n.txt.gz"; verify_one $n "$TMP/n$n.txt.gz"; rm -f "$TMP/n$n.txt.gz"; done
for n in 14 15 16; do [ -f object/cert/n$n.txt.gz ] && verify_one $n object/cert/n$n.txt.gz; done
if [ "${FULL:-0}" -ge 2 ]; then v11=$(python3 -c "import json;print(json.load(open('object/values.json'))['values']['11'])"); python3 -I verify-it-yourself/recompute_value.py 11 2 --expect "$v11" || { rm -rf "$TMP"; echo FAIL; exit 1; }; fi
rm -rf "$TMP"
echo PASS
