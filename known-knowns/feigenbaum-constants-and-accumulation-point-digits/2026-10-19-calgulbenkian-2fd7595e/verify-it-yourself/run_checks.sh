#!/bin/sh
# Standalone check. Run from the claim folder: sh verify-it-yourself/run_checks.sh
# Needs python3 (3.8 or later), standard library only.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
cd "$HERE" || exit 1
fail=0
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
echo "== reassemble the object from its 6 numbered parts and check sha256 (whole file first)"
python3 -I - object "$TMP/whole.json" <<'PYEOF' || fail=1
import sys, hashlib, re
d, out = sys.argv[1], sys.argv[2]
name = 'feigenbaum_z4_certificates.json'
lines = open(d + '/PARTS.sha256').read().strip().split('\n')
whole_sha = lines[0].split()[0]
exp_idx = open('INDEX.csv').read().strip().split('\n')[-1].split(',')[-1]
data = b''
bad = 0
for l in lines[1:]:
    sha, pn = l.split()[0], l.split()[1]
    b = open(d + '/' + pn, 'rb').read()
    if hashlib.sha256(b).hexdigest() != sha:
        print('part sha256 MISMATCH', pn); bad += 1
    data += b
got = hashlib.sha256(data).hexdigest()
print('whole file sha256 %s ; PARTS.sha256 says %s ; INDEX.csv says %s ; parts checked: %d, bad: %d' % (got, whole_sha, exp_idx, len(lines) - 1, bad))
open(out, 'wb').write(data)
sys.exit(0 if (got == whole_sha == exp_idx and bad == 0) else 1)
PYEOF
echo "== z4_check.py: fixed-point and eigenfunction residuals at 1300 digits, two resolutions (about 30 s)"
python3 -I verify-it-yourself/z4_check.py "$TMP/whole.json" the-record-we-beat/thurlby_table_4_6_excerpt.txt the-record-we-beat/oeis_A195102_data.txt | tee "$TMP/out.txt"
tail -n 1 "$TMP/out.txt" | grep -q "^RESULT PASS" || fail=1
echo "== negative control: one Chebyshev coefficient of the first resolution changed by 1e-900; the check must FAIL"
python3 -I - "$TMP/whole.json" "$TMP/neg.json" <<'PYEOF'
import sys, json
from decimal import Decimal, getcontext
getcontext().prec = 1300
o = json.load(open(sys.argv[1]))
o['c_coeffs_N1'][5] = str(Decimal(o['c_coeffs_N1'][5]) + Decimal(10) ** -900)
json.dump(o, open(sys.argv[2], 'w'))
PYEOF
if python3 -I verify-it-yourself/z4_check.py "$TMP/neg.json" >"$TMP/neg_out.txt" 2>&1; then echo "negative control NOT rejected"; fail=1; else echo "negative control rejected as expected: $(grep '^worst fixed-point' "$TMP/neg_out.txt")"; fi
rm -f "$TMP"/*; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
