#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1
python3 - <<'PYCODE'
import hashlib,json,sys
sys.path.insert(0,'verify-it-yourself')
from basis_check import check
p='object/scheme.json'
assert hashlib.sha256(open(p,'rb').read()).hexdigest() == '6e554e0ee89a3fda23f7c59d261ca1f27bcb089e141db911246437ca50e931e9'
r=check(json.load(open(p)))
assert r['rank']==47 and r['format']==[2, 5, 6] and r['additions']==179
print(json.dumps(r))
PYCODE
python3 verify-it-yourself/independent_check.py object/scheme.json --expect-additions 179
python3 verify-it-yourself/semantic_controls.py
printf 'PASS\n'
