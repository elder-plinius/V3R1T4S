#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
PY=
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c "import sys; sys.exit(0 if sys.version_info >= (3,) else 1)" >/dev/null 2>&1; then PY=$c; break; fi
done
[ -n "$PY" ] || { echo "no working Python 3"; echo FAIL; exit 1; }
status=PASS
echo "== sha256 of the object"
$PY -c "import hashlib;print(hashlib.sha256(open('object/code_20_15_16.txt','rb').read()).hexdigest())"
echo "== checker on the object (must be VALID)"
$PY verify-it-yourself/check_dna_code.py object/code_20_15_16.txt 20 15 || status=FAIL
echo "== checker on a corrupted copy (first letter of word 1 changed; must be INVALID)"
tmp=$(mktemp)
$PY -c "import sys;w=open('object/code_20_15_16.txt').read().split();w[0]={'A':'C','C':'A','G':'T','T':'G'}[w[0][0]]+w[0][1:];open(sys.argv[1],'w').write(chr(10).join(w)+chr(10))" "$tmp"
if $PY verify-it-yourself/check_dna_code.py "$tmp" 20 15; then echo "corrupted copy was accepted"; status=FAIL; else echo "corrupted copy rejected"; fi
rm -f "$tmp"
echo "== size must be 16, strictly above the table entry 15"
n=$(grep -c . object/code_20_15_16.txt); [ "$n" = 16 ] || status=FAIL; echo "size $n"
echo $status
