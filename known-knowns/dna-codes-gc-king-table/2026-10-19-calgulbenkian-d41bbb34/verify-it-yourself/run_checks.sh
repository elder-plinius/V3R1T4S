#!/bin/sh
# Standalone check for object/gc_13_9_6.txt. Run from this folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/gc_13_9_6.txt"
CHK="$HERE/verify-it-yourself/check_dna.py"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
echo "== check_dna.py on object/gc_13_9_6.txt (n=13, d=9, w=6, mode gc)"
python3 -I "$CHK" "$OBJ" 13 9 gc | tee "$HERE/verify-it-yourself/.last_check.json"
python3 -I -c "import json,sys; r=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); ok=r.get('VALID') is True and r.get('size')==52 and r.get('w')==6; print('checker verdict:', 'PASS' if ok else 'FAIL', '(VALID=%s, size=%s, w=%s)'%(r.get('VALID'),r.get('size'),r.get('w'))); sys.exit(0 if ok else 1)" "$HERE/verify-it-yourself/.last_check.json" || fail=1
rm -f "$HERE/verify-it-yourself/.last_check.json"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
echo "== negative control 1: the last word replaced by a copy of the first word must FAIL"
python3 -I -c "import sys; L=[l for l in open(sys.argv[1]).read().split() if l]; L[-1]=L[0]; open(sys.argv[2],'w').write('\n'.join(L)+'\n')" "$OBJ" "$TMP/neg1.txt"
python3 -I "$CHK" "$TMP/neg1.txt" 13 9 gc >"$TMP/neg1.out" 2>&1
if python3 -I -c "import json,sys; r=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); sys.exit(0 if r.get('VALID') is True else 1)" "$TMP/neg1.out"; then echo "negative control 1 NOT rejected"; fail=1; else echo "negative control 1 rejected as expected (VALID false)"; fi
echo "== negative control 2: one letter of the first word changed so that its GC count is wrong must FAIL"
python3 -I -c "
import sys
L=[l for l in open(sys.argv[1]).read().split() if l]
x=L[0]
i=[k for k,c in enumerate(x) if c in 'CG'][0]
L[0]=x[:i]+('A' if x[i]=='C' else 'T')+x[i+1:]
open(sys.argv[2],'w').write('\n'.join(L)+'\n')" "$OBJ" "$TMP/neg2.txt"
python3 -I "$CHK" "$TMP/neg2.txt" 13 9 gc >"$TMP/neg2.out" 2>&1
if python3 -I -c "import json,sys; r=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); sys.exit(0 if r.get('VALID') is True else 1)" "$TMP/neg2.out"; then echo "negative control 2 NOT rejected"; fail=1; else echo "negative control 2 rejected as expected (VALID false)"; fi
rm -f "$TMP"/neg1.txt "$TMP"/neg1.out "$TMP"/neg2.txt "$TMP"/neg2.out; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
