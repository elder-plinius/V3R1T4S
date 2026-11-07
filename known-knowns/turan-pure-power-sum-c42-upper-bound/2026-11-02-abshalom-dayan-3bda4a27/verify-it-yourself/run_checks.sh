#!/bin/sh
# Run from the package folder. Checks the object files, joins and decompresses the table parts and checks their hash, the exact small cases, rebuilds the table and checks a few rows.
# The full check of all 1600 rows is in RUN_IT_YOURSELF.md. Last output line: PASS or FAIL.
PY=${PYTHON:-python3}
$PY -I - <<'EOF' || { echo FAIL; exit 1; }
import hashlib,json
h=json.load(open('verify-it-yourself/object_hashes.json'))
for f,v in h.items():
    assert hashlib.sha256(open('object/'+f,'rb').read()).hexdigest()==v,f
print('object hashes ok')
EOF
$PY -I - <<'EOF' || { echo FAIL; exit 1; }
import hashlib,glob,lzma
parts=sorted(glob.glob('object/V_b_parts/V_b.npy.xz.part*'))
assert len(parts)==25,len(parts)
xz=b''.join(open(p,'rb').read() for p in parts)
assert hashlib.sha256(xz).hexdigest()=='3511d3527f799d504c0db8ef8707ea63a2d50d2ff1da8137c25b7564dc9af7a9','xz'
npy=lzma.decompress(xz)
assert hashlib.sha256(npy).hexdigest()=='b1712e642ea9a80c1731556369451bb7afb4dcfab14fa71a218c3351440def0c','npy'
print('V_b.npy joined, decompressed, hash ok')
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
