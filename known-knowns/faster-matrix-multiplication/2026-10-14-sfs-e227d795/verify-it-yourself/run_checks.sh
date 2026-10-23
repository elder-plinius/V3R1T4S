#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1
python3 - <<'PYCODE'
import hashlib,json,sys
sys.path.insert(0,'verify-it-yourself')
from basis_check import check
p='object/scheme.json'
assert hashlib.sha256(open(p,'rb').read()).hexdigest() == 'e227d795fa1418070e30f21b18eac6a55d7426e51cfc8f8ef99c57b831d021f2'
r=check(json.load(open(p)))
assert r['rank']==47 and r['format']==[3, 4, 5] and r['additions']==156
print(json.dumps(r))
PYCODE
python3 verify-it-yourself/independent_check.py object/scheme.json
python3 verify-it-yourself/semantic_controls.py
printf 'PASS\n'
