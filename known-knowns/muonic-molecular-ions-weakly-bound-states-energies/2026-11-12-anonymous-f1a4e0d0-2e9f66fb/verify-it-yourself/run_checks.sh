#!/bin/sh
# run from the package folder: sh verify-it-yourself/run_checks.sh
# needs Python 3.9+ with python-flint and sympy (pip install python-flint sympy); set V3R1T4S_PYTHON to that interpreter.
# about 3 minutes of CPU on a laptop
PY=${V3R1T4S_PYTHON:-python3}
$PY - <<'PYEOF' || { echo FAIL; exit 1; }
import hashlib, sys
want = {'object/basis.txt': '2e9f66fb6bcf8bc2f25dbec1de05659ac3f9b8c404fbaa6d984928d811cebe87', 'object/vector.txt': 'b4fcb8160b75f3ae4e8f25e6a1da9b62bc3fc4e4a050100d5219d848c7381230'}
for f, h in want.items():
    if hashlib.sha256(open(f, 'rb').read()).hexdigest() != h:
        print('sha256 mismatch for', f); sys.exit(1)
PYEOF
$PY verify-it-yourself/check_cert.py object/basis.txt object/vector.txt --bar -0.5125686450010 --margin 1e-13 --procs 2 || { echo FAIL; exit 1; }
echo PASS
