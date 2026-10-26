#!/bin/sh
_PKG=$(cd "$(dirname "$0")/.." && pwd)
if command -v shasum >/dev/null 2>&1; then _S="shasum -a 256"; else _S="sha256sum"; fi
( cd "$_PKG" && grep "  object/" SHA256SUMS > "${TMPDIR:-/tmp}/objsums.$$" && $_S -c "${TMPDIR:-/tmp}/objsums.$$" >/dev/null 2>&1 ) || { echo "object file sha256 MISMATCH against SHA256SUMS"; echo "FAIL"; exit 1; }
# Standalone check. Run from this folder:  sh verify-it-yourself/run_checks.sh
# Needs python3 (3.8 or later), standard library only. Single thread.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object"
TR="$HERE/the-record-we-beat"
CHK="$HERE/verify-it-yourself/shannon_check.py"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
echo "== object files already checked against SHA256SUMS by the integrity guard above"
echo "== shannon_check.py: separation property of every table and code used, exact recomputation of M, exact comparison with the live records"
OUTF=$(mktemp 2>/dev/null || mktemp -t v3check)
python3 -I "$CHK" "$OBJ" "$TR" | tee "$OUTF"
rc=$?
if [ "$rc" -ne 0 ]; then fail=1; fi
LAST=$(grep '^RESULT ' "$OUTF" | tail -n 1)
if [ -z "$LAST" ]; then echo "no RESULT line"; fail=1; fi
rm -f "$OUTF"
echo "== negative control 1: one duplicated word in a substitution table must be rejected"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
cp "$OBJ/schedule.json" "$OBJ/argon_shannon_certificates.json" "$TMP/"
python3 -I -c "
import json,sys
r=json.load(open(sys.argv[1])); n=sorted(r['tables'])[0]; t=r['tables'][n]['words']; t['B'].append(list(t['B'][0]))
json.dump(r,open(sys.argv[2],'w'))" "$OBJ/rules.json" "$TMP/rules.json"
if python3 -I "$CHK" "$TMP" "$TR" >"$TMP/n1.txt" 2>&1; then echo "negative control 1 NOT rejected"; fail=1; else echo "negative control 1 rejected as expected"; fi
echo "== negative control 2: one input changed by 1 (a certificate, or the base vector) must change M and be rejected"
cp "$OBJ/rules.json" "$TMP/rules.json"
python3 -I -c "
import json,sys
s=json.load(open(sys.argv[1]))
if 'certificates' in s: s['certificates']['C4']+=1
else: s['schedule']['w0'][0]+=1
json.dump(s,open(sys.argv[2],'w'))" "$OBJ/schedule.json" "$TMP/schedule.json"
if python3 -I "$CHK" "$TMP" "$TR" >"$TMP/n2.txt" 2>&1; then echo "negative control 2 NOT rejected"; fail=1; else echo "negative control 2 rejected as expected"; fi
rm -f "$TMP"/*; rmdir "$TMP" 2>/dev/null
echo "$LAST"
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
