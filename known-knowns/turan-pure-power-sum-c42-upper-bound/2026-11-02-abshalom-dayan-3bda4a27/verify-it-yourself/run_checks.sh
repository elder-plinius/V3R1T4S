#!/bin/sh
# Run from the package folder. Checks the object files, the exact small cases, rebuilds the table and checks a few rows.
# The full check of all 1600 rows is in RUN_IT_YOURSELF.md. Last output line: PASS or FAIL.
PY=${PYTHON:-python3}
$PY -I - <<'EOF' || { echo FAIL; exit 1; }
import hashlib,json
h=json.load(open('verify-it-yourself/object_hashes.json'))
for f,v in h.items():
    assert hashlib.sha256(open('object/'+f,'rb').read()).hexdigest()==v,f
print('object hashes ok')
EOF
$PY -I verify-it-yourself/exact_tests.py || { echo FAIL; exit 1; }
T=$(mktemp -d) || { echo FAIL; exit 1; }
cp how-we-built-it/build_V.py verify-it-yourself/check_hjb.py "$T"/ || { echo FAIL; exit 1; }
HERE=$(pwd)
( cd "$T" && $PY -I build_V.py V_b .501 .0035 1600 .0042 .5 .015 ) || { echo FAIL; rm -rf "$T"; exit 1; }
OUT=$(cd "$T" && $PY -I check_hjb.py V_b 1e-6 1500 1505)
echo "$OUT" | tail -5
rm -rf "$T"
cd "$HERE"
case "$(echo "$OUT" | tail -1)" in PASS) echo PASS;; *) echo FAIL; exit 1;; esac
