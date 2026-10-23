#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1
python3 - <<'PYCODE'
import hashlib,json,sys
sys.path.insert(0,'verify-it-yourself')
from basis_check import check
p='object/scheme.json'
assert hashlib.sha256(open(p,'rb').read()).hexdigest() == '289432a72c0f86a04925e6475d31d4ff86d92a65fb8d57f4b57f918c3866d654'
r=check(json.load(open(p)))
assert r['rank']==51 and r['format']==[2, 4, 8] and r['additions']==182
print(json.dumps(r))
PYCODE
python3 verify-it-yourself/independent_check.py object/scheme.json
python3 verify-it-yourself/semantic_controls.py
printf 'PASS\n'
