#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1
python3 - <<'PYCODE'
import hashlib,json,sys
sys.path.insert(0,'verify-it-yourself')
from basis_check import check
p='object/scheme.json'
assert hashlib.sha256(open(p,'rb').read()).hexdigest() == '61917376617f1db0a75f5e9f5efd8bbd748713896418760b469126ea042ae5ee'
r=check(json.load(open(p)))
assert r['rank']==118 and r['format']==[4, 5, 8] and r['additions']==486
print(json.dumps(r))
PYCODE
python3 verify-it-yourself/independent_check.py object/scheme.json --expected-candidate
python3 verify-it-yourself/semantic_controls.py
printf 'PASS\n'
