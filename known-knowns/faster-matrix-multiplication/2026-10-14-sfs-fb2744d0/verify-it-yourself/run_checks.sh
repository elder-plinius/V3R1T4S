#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1
python3 - <<'PYCODE'
import hashlib,json,sys
sys.path.insert(0,'verify-it-yourself')
from basis_check import check
p='object/scheme.json'
assert hashlib.sha256(open(p,'rb').read()).hexdigest() == 'fb2744d037444d6e5f84f56628cf97a01ad2650e374421fbe4961bfafefd7ca2'
r=check(json.load(open(p)))
assert r['rank']==40 and r['format']==[2,5,5] and r['additions']==148
print(json.dumps(r))
PYCODE
python3 verify-it-yourself/independent_check.py object/scheme.json --expected-additions 148
python3 verify-it-yourself/semantic_controls.py
printf 'PASS\n'
