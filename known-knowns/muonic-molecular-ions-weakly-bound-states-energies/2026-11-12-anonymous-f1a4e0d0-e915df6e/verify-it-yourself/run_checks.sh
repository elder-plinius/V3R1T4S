#!/bin/sh
# run from the package folder: sh verify-it-yourself/run_checks.sh
# needs Python 3.9+ with python-flint and sympy (pip install python-flint sympy); set V3R1T4S_PYTHON to that interpreter.
# about 3 minutes of CPU on a laptop
PY=${V3R1T4S_PYTHON:-python3}
$PY - <<'PYEOF' || { echo FAIL; exit 1; }
import hashlib, sys
want = {'object/basis.txt': 'e915df6e2f13869a026e88b0365fdac647640d110f74d3ba43efc31445b8af62', 'object/vector.txt': 'c09c7fd025ef88f3ff425a2c4e198673f02968398c59268dd20eed4007c5089a'}
for f, h in want.items():
    if hashlib.sha256(open(f, 'rb').read()).hexdigest() != h:
        print('sha256 mismatch for', f); sys.exit(1)
PYEOF
$PY verify-it-yourself/check_cert.py object/basis.txt object/vector.txt --bar -0.4887083249914 --margin 1e-13 --procs 2 || { echo FAIL; exit 1; }
echo PASS
