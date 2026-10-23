#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1
python3 - <<'PYCODE'
import hashlib,json,sys
sys.path.insert(0,'verify-it-yourself')
from basis_check import check
p='object/scheme.json'
assert hashlib.sha256(open(p,'rb').read()).hexdigest() == '733891ac541bd4c85da049a68dfcafd680d7fa5f006718668d1e8d38f7478900'
r=check(json.load(open(p)))
assert r['rank']==73 and r['format']==[4, 4, 6] and r['additions']==264
print(json.dumps(r))
PYCODE
python3 verify-it-yourself/independent_check.py object/scheme.json --candidate
python3 verify-it-yourself/semantic_controls.py
printf 'PASS\n'
