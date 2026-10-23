#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1
python3 - <<'PYCODE'
import hashlib,json,sys
sys.path.insert(0,'verify-it-yourself')
from basis_check import check
p='object/scheme.json'
assert hashlib.sha256(open(p,'rb').read()).hexdigest() == '04997c5844e0968c43b347b7e911059ac1464c5da653b29bd3838a489723df7c'
r=check(json.load(open(p)))
assert r['rank']==58 and r['format']==[3, 5, 5] and r['additions']==214
print(json.dumps(r))
PYCODE
python3 verify-it-yourself/independent_check.py object/scheme.json
python3 verify-it-yourself/semantic_controls.py
printf 'PASS\n'
