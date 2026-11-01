#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs Python 3 with numpy. Last line of output: PASS or FAIL.
PY=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c "import numpy" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then echo "needs Python 3 with numpy on PATH (python3 or python)"; echo FAIL; exit 1; fi
want=31155172b650ba08dc63be96d76a7f189e754612e2d6e7183a744ac6c1270fe1
got=$("$PY" -I -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" object/N38_Ne.xyz)
echo "sha256 object/N38_Ne.xyz = $got"
[ "$got" = "$want" ] && echo "sha256 matches INDEX.csv: ok" || echo "sha256 does not match INDEX.csv"
out=$("$PY" -I verify-it-yourself/check_lj_zpe.py object/N38_Ne.xyz --bar Ne=-107.42431 --margin 5e-4 2>&1)
rc=$?
echo "$out"
if [ "$got" = "$want" ] && [ $rc -eq 0 ] && echo "$out" | grep -q "^RESULT: PASS"; then echo PASS; exit 0; fi
echo FAIL
exit 1
