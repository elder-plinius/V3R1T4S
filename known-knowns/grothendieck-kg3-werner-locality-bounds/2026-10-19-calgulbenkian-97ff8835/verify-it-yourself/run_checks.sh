#!/bin/sh
# Standalone check. Run from the claim folder: sh verify-it-yourself/run_checks.sh
# Needs python3 (3.8 or later), standard library only, and curl: the instance matrix d8_n1_120x120.mat is not
# shipped; it is fetched from Zenodo record 10.5281/zenodo.13693164 and checked against its sha256.
# To use a copy you already have, run: MAT=/path/to/d8_n1_120x120.mat sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
cd "$HERE" || exit 1
fail=0
MAT_URL=https://zenodo.org/records/13693164/files/d8_n1_120x120.mat
MAT_SHA=a78361f200b669741a4a0636bb4e1027a1e6cdfeca174c84ef67269a17bbeaac
CERT=object/dual_certificates.txt
WIT=object/lower_bound_witness.txt
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
sha() { python3 -I -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$1"; }
exp_sha=$(tail -n 1 INDEX.csv | awk -F, '{print $NF}')
got_sha=$(sha "$CERT")
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 of $CERT matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
if [ -z "${MAT:-}" ]; then
  MAT="$TMP/d8_n1_120x120.mat"
  echo "== fetching the instance matrix from Zenodo: $MAT_URL"
  if ! curl -sSfL -A "V3R1T4S run_checks.sh (curl)" -o "$MAT" "$MAT_URL"; then
    echo "could not fetch the matrix; download it yourself and run with MAT=/path/to/d8_n1_120x120.mat"
    echo "FAIL"; exit 1
  fi
fi
got_mat=$(sha "$MAT")
if [ "$got_mat" = "$MAT_SHA" ]; then echo "sha256 of the instance matrix d8_n1_120x120.mat matches Zenodo record 10.5281/zenodo.13693164 ($got_mat)"; else echo "matrix sha256 MISMATCH (got $got_mat, expected $MAT_SHA)"; fail=1; fi
echo "== e8_check.py: identification with the E8 roots, Q, lower bound, 18454 dual certificates (about 5 s)"
python3 -I verify-it-yourself/e8_check.py "$MAT" "$CERT" "$WIT" | tee "$TMP/last.txt"
tail -n 1 "$TMP/last.txt" | grep -q "^RESULT PASS: L = 6104, Q = 9240" || fail=1
echo "== negative control 1: one symmetric pair of matrix entries changed; the check must FAIL"
python3 -I - "$MAT" "$TMP/neg.mat" <<'PYEOF'
import sys, struct
sys.path.insert(0, 'verify-it-yourself')
import e8_check as E
A, (off, k) = E.load_matrix(sys.argv[1])
b = bytearray(open(sys.argv[1], 'rb').read())
i, j = 0, 0
for jj in range(1, 120):
    if A[0][jj] == 3:
        j = jj; break
for (r, c) in ((i, j), (j, i)):
    pos = off + 8 * (k + r * 120 + c)
    struct.pack_into('<q', b, pos, 0)
open(sys.argv[2], 'wb').write(bytes(b))
PYEOF
if python3 -I verify-it-yourself/e8_check.py "$TMP/neg.mat" "$CERT" "$WIT" >"$TMP/o1.txt" 2>&1; then echo "negative control 1 NOT rejected"; fail=1; else echo "negative control 1 rejected as expected: $(tail -n 1 "$TMP/o1.txt" | cut -c1-120)"; fi
echo "== negative control 2: the certificate of the first tight vector is replaced by zeros; the check must FAIL"
python3 -I - "$CERT" "$TMP/dual_bad.txt" <<'PYEOF'
import sys
out = []
for line in open(sys.argv[1]):
    t = line.split()
    if tuple(t[:8]) == ('0', '0', '0', '0', '5', '0', '1', '0'):
        t[8:16] = ['0'] * 8
    out.append(' '.join(t))
open(sys.argv[2], 'w').write('\n'.join(out) + '\n')
PYEOF
if python3 -I verify-it-yourself/e8_check.py "$MAT" "$TMP/dual_bad.txt" "$WIT" >"$TMP/o2.txt" 2>&1; then echo "negative control 2 NOT rejected"; fail=1; else echo "negative control 2 rejected as expected: $(grep 'above 6104' "$TMP/o2.txt" | cut -c1-140)"; fi
rm -f "$TMP"/*; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
