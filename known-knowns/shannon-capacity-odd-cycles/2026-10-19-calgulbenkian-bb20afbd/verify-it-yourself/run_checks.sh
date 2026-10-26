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
echo "== object files against INDEX.csv"
for f in schedule.json rules.json argon_shannon_certificates.json base_g5.json cert_input.json bpz_lean_c7_schedule.json; do
  exp=$(grep ",object/$f," "$HERE/INDEX.csv" | awk -F, '{print $NF}')
  got=$($SHA "$OBJ/$f" | cut -d' ' -f1)
  if [ "$got" = "$exp" ]; then echo "sha256 ok  object/$f"; else echo "sha256 MISMATCH object/$f (got $got, expected $exp)"; fail=1; fi
done
echo "== shannon_check.py: separation property of every table and code used, exact recomputation of M, exact comparison with the live records"
OUTF=$(mktemp 2>/dev/null || mktemp -t v3check)
python3 -I "$CHK" "$OBJ" "$TR" | tee "$OUTF"
rc=$?
if [ "$rc" -ne 0 ]; then fail=1; fi
LAST=$(grep '^RESULT ' "$OUTF" | tail -n 1)
ALLR="$LAST"
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

VY="$HERE/verify-it-yourself"
run_sub() {
  title="$1"; shift
  echo "== $title"
  O2=$(mktemp 2>/dev/null || mktemp -t v3check)
  python3 -I "$1" "$2" ${3:+"$3"} | tee "$O2"
  R2=$(grep '^RESULT ' "$O2" | tail -n 1)
  if [ -z "$R2" ]; then echo "no RESULT line"; fail=1; fi
  case "$R2" in *FAILED*) fail=1;; esac
  ALLR="$ALLR
$R2"
  rm -f "$O2"
}
run_sub "G5 base gadget: every axiom of Definition 2, exhaustive" "$VY/check_g5.py" "$OBJ"
run_sub "BPZ Lean C7 schedule: known answer (the integer defined in CertC7.lean)" "$VY/bpz_lean_c7_check.py" "$OBJ" "$TR"
run_sub "set-level test: Lemma 1, Theorem 1, sigma, Phi, S3b, K4a on explicit vertex sets" "$VY/set_level_test.py" "$OBJ"
run_sub "box-level axioms: I15 and I30++ independent, dimension-15 private pairs, condition (33) for Xhat30 at dimension 30" "$VY/check_box_axioms.py" "$OBJ"
run_sub "certificates C1 to C4 re-derived from their definitions (not Tandon's script), with a word-by-word enumeration for C2" "$VY/derive_certificates.py" "$OBJ" --brute
echo "== negative control 3: a corrupted base set (one word of I5 replaced by another word of I5) must fail the G5 check"
TMP2=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
python3 -I -c "
import json,sys
d=json.load(open(sys.argv[1])); d['I'][0]=d['I'][1]
json.dump(d,open(sys.argv[2],'w'))" "$OBJ/base_g5.json" "$TMP2/base_g5.json"
if python3 -I "$VY/check_g5.py" "$TMP2" >/dev/null 2>&1; then echo "negative control 3 NOT rejected"; fail=1; else echo "negative control 3 rejected as expected"; fi
echo "== negative control 4: a wrong value for C1 in the comparison ledger must be reported as a mismatch"
cp "$OBJ/base_g5.json" "$TMP2/base_g5.json"
python3 -I -c "
import json,sys
d=json.load(open(sys.argv[1])); d['paper_values']['C1']+=1
json.dump(d,open(sys.argv[2],'w'))" "$OBJ/cert_input.json" "$TMP2/cert_input.json"
if python3 -I "$VY/derive_certificates.py" "$TMP2" >/dev/null 2>&1; then echo "negative control 4 NOT rejected"; fail=1; else echo "negative control 4 rejected as expected"; fi
rm -f "$TMP2"/*; rmdir "$TMP2" 2>/dev/null
echo "$ALLR"
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
