#!/bin/sh
# Standalone check. Run from the claim folder: sh verify-it-yourself/run_checks.sh
# Needs python3 (3.8 or later), standard library only.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
cd "$HERE" || exit 1
fail=0
exp_sha=$(tail -n 1 INDEX.csv | awk -F, '{print $NF}')
got_sha=$(python3 -I -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "object/d8_n1_120x120.mat")
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 of object/d8_n1_120x120.mat matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
echo "== e8_check.py: identification with the E8 roots, Q, lower bound, 18454 dual certificates (about 5 s)"
python3 -I verify-it-yourself/e8_check.py object/d8_n1_120x120.mat verify-it-yourself/data/dual_certificates.txt verify-it-yourself/data/lower_bound_witness.txt | tee "$HERE/verify-it-yourself/.last.txt"
tail -n 1 "$HERE/verify-it-yourself/.last.txt" | grep -q "^RESULT PASS: L = 6104, Q = 9240" || fail=1
rm -f "$HERE/verify-it-yourself/.last.txt"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
echo "== negative control 1: one symmetric pair of matrix entries changed; the check must FAIL"
python3 -I - object/d8_n1_120x120.mat "$TMP/neg.mat" <<'PYEOF'
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
if python3 -I verify-it-yourself/e8_check.py "$TMP/neg.mat" verify-it-yourself/data/dual_certificates.txt verify-it-yourself/data/lower_bound_witness.txt >"$TMP/o1.txt" 2>&1; then echo "negative control 1 NOT rejected"; fail=1; else echo "negative control 1 rejected as expected: $(tail -n 1 "$TMP/o1.txt" | cut -c1-120)"; fi
echo "== negative control 2: the certificate of the first tight vector is replaced by zeros; the check must FAIL"
python3 -I - verify-it-yourself/data/dual_certificates.txt "$TMP/dual_bad.txt" <<'PYEOF'
import sys
out = []
for line in open(sys.argv[1]):
    t = line.split()
    if tuple(t[:8]) == ('0', '0', '0', '0', '5', '0', '1', '0'):
        t[8:16] = ['0'] * 8
    out.append(' '.join(t))
open(sys.argv[2], 'w').write('\n'.join(out) + '\n')
PYEOF
if python3 -I verify-it-yourself/e8_check.py object/d8_n1_120x120.mat "$TMP/dual_bad.txt" verify-it-yourself/data/lower_bound_witness.txt >"$TMP/o2.txt" 2>&1; then echo "negative control 2 NOT rejected"; fail=1; else echo "negative control 2 rejected as expected: $(grep 'above 6104' "$TMP/o2.txt" | cut -c1-140)"; fi
rm -f "$TMP"/*; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
