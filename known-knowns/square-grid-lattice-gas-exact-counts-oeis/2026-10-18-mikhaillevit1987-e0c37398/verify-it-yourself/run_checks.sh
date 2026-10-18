#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
PY=
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c "import sys; sys.exit(0 if sys.version_info >= (3,) else 1)" >/dev/null 2>&1; then PY=$c; break; fi
done
[ -n "$PY" ] || { echo "no working Python 3"; echo FAIL; exit 1; }
status=PASS
echo "== sha256 of the object"
$PY -c "import hashlib;print(hashlib.sha256(open('object/a054759_16.txt','rb').read()).hexdigest())"
echo "== checker on the object (must be VALID)"
$PY verify-it-yourself/check_a054759.py object/a054759_16.txt || status=FAIL
echo "== checker on a corrupted copy (last digit changed; must be INVALID)"
tmp=$(mktemp)
$PY -c "import sys;v=open('object/a054759_16.txt').read().strip();open(sys.argv[1],'w').write(v[:-1]+str((int(v[-1])+1)%10)+chr(10))" "$tmp"
if $PY verify-it-yourself/check_a054759.py "$tmp" >/dev/null; then echo "corrupted copy was accepted"; status=FAIL; else echo "corrupted copy rejected"; fi
rm -f "$tmp"
echo $status
[ "$status" = PASS ]
