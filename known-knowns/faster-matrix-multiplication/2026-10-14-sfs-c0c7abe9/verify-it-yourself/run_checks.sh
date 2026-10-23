#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1
python3 - <<'PYCODE'
import hashlib,json,sys
sys.path.insert(0,'verify-it-yourself')
from basis_check import check
p='object/scheme.json'
assert hashlib.sha256(open(p,'rb').read()).hexdigest() == 'c0c7abe9136e5f773d01c5c276cb1f6c3f565afab183499fdda63ac67947e02e'
r=check(json.load(open(p)))
assert r['rank']==93 and r['format']==[5, 5, 5] and r['additions']==354
print(json.dumps(r))
PYCODE
python3 verify-it-yourself/independent_check.py object/scheme.json
python3 verify-it-yourself/semantic_controls.py
printf 'PASS\n'
