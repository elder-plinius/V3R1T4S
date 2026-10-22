#!/bin/sh
# Standalone check for object/A27_8_11_2422.txt. Run from the package folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
PY="${PYTHON:-python3}"
OBJ="$HERE/object/A27_8_11_2422.txt"
CHK="$HERE/verify-it-yourself/check_cw_std.py"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
echo "== check_cw_std.py (standard library): count, distinct, weight, no two words share 8 ones"
out=$("$PY" -I "$CHK" "$OBJ" 27 8 11 2422 2>&1); rc=$?
echo "$out"
if [ "$rc" -ne 0 ]; then fail=1; echo "checker verdict: FAIL"; else echo "checker verdict: PASS"; fi
if "$PY" -I -c "import numpy" >/dev/null 2>&1; then
  echo "== check_cw.py (needs numpy; the panel's checker): count, distinct, weight, all pairwise distances"
  out=$("$PY" -I "$HERE/verify-it-yourself/check_cw.py" "$OBJ" 27 8 11 2422 2>&1); rc=$?
  echo "$out"
  if [ "$rc" -ne 0 ]; then fail=1; echo "second checker verdict: FAIL"; else echo "second checker verdict: PASS"; fi
else
  echo "== check_cw.py skipped (numpy is not installed; it is optional)"
fi
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
echo "== negative control 1: a copy whose last word is replaced by a copy of the first word must FAIL"
head -n 1 "$OBJ" > "$TMP/first.txt"
sed '$d' "$OBJ" > "$TMP/dup.txt"; cat "$TMP/first.txt" >> "$TMP/dup.txt"
if "$PY" -I "$CHK" "$TMP/dup.txt" 27 8 11 2422 >"$TMP/n1.txt" 2>&1; then echo "negative control 1 NOT rejected"; fail=1; else echo "negative control 1 rejected as expected"; fi
echo "== negative control 2: the same object checked against a claim of one more word must FAIL"
if "$PY" -I "$CHK" "$OBJ" 27 8 11 2423 >"$TMP/n2.txt" 2>&1; then echo "negative control 2 NOT rejected"; fail=1; else echo "negative control 2 rejected as expected"; fi
echo "== negative control 3: a copy with the last word moved to a word sharing 8 ones with the first must FAIL"
"$PY" -I -c "
import sys
rows=[l.strip() for l in open(sys.argv[1]) if l.strip()]
first=rows[0]; ones=[i for i,c in enumerate(first) if c=='1']; t=int(sys.argv[2])
keep=set(ones[:t]); zeros=[i for i,c in enumerate(first) if c=='0']
new=['0']*len(first)
for i in keep: new[i]='1'
need=sum(1 for c in first if c=='1')-t
for i in zeros[:need]: new[i]='1'
rows[-1]=''.join(new)
open(sys.argv[3],'w').write('\n'.join(rows)+'\n')
" "$OBJ" 8 "$TMP/share.txt"
if "$PY" -I "$CHK" "$TMP/share.txt" 27 8 11 2422 >"$TMP/n3.txt" 2>&1; then echo "negative control 3 NOT rejected"; fail=1; else echo "negative control 3 rejected as expected"; fi
rm -f "$TMP/first.txt" "$TMP/dup.txt" "$TMP/share.txt" "$TMP/n1.txt" "$TMP/n2.txt" "$TMP/n3.txt"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
