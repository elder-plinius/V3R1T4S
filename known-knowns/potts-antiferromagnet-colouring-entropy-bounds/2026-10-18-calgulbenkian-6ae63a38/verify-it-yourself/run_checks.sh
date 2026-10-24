#!/bin/sh
# Checks for potts-wsq4-ub. Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs python3 (3.8 or later), standard library only. No numpy is needed. Takes about 15 seconds.
# The optional long check (an independent C program, 25 to 40 minutes) is NOT run here: see verify-it-yourself/full-check/.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
PY=${PYTHON:-python3}
V="$HERE/verify-it-yourself"
fail=0
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
trap 'rm -f "$TMP/q4_cyl_18_cert.bin" "$TMP/neg.bin" "$TMP/neg2.bin"; rmdir "$TMP" 2>/dev/null' EXIT
echo "== 1. reassemble the parts and check every sha256 (parts and whole file)"
$PY "$V/reassemble.py" "$HERE/object/PARTS.txt" "$TMP/q4_cyl_18_cert.bin" || fail=1
echo "== 1b. sha256 of the other object files"
$PY "$V/check_object_files.py" "$V/object_files.sha256" "$HERE" || fail=1
echo "== 2. parse the certificate, check positivity, compute the bound from the exact integer ratios"
$PY "$V/check_cert.py" "$TMP/q4_cyl_18_cert.bin" 18 2.33606022655545835815 2.33606820555777 || fail=1
echo "== 3. exact check that y = (orbit-quotient matrix) v on the three small certificates (validates the file format)"
for w in 6 8 9; do
  $PY "$V/orbit_check.py" "$HERE/object/format_examples/q4_cyl_${w}_cert.bin" 4 "$w" || fail=1
done
echo "== 4. independent small-width eigenvalues (double precision) against the table"
out4=$($PY "$V/small_check.py" 4 "$HERE/object/THETA_TABLE_q4.txt" 10) || fail=1
echo "$out4" | tail -n 4
echo "== 5. negative controls (each must be rejected)"
$PY - "$TMP/q4_cyl_18_cert.bin" "$TMP/neg.bin" <<'PYEOF'
import sys, struct
raw = bytearray(open(sys.argv[1], 'rb').read()); n = struct.unpack('<I', raw[:4])[0]
raw[4 + 32 * n + 31] ^= 0x01      # set a high bit of the first y entry
open(sys.argv[2], 'wb').write(raw)
PYEOF
if $PY "$V/check_cert.py" "$TMP/neg.bin" 18 2.33606022655545835815 2.33606820555777 >/dev/null 2>&1; then echo "negative control (corrupted y entry) NOT rejected"; fail=1; else echo "negative control (corrupted y entry) rejected as expected"; fi
cp "$HERE/object/format_examples/q4_cyl_6_cert.bin" "$TMP/neg2.bin"
$PY - "$TMP/neg2.bin" <<'PYEOF'
import sys, struct
raw = bytearray(open(sys.argv[1], 'rb').read()); n = struct.unpack('<I', raw[:4])[0]
raw[4 + 32 * n + 1] ^= 0x01
open(sys.argv[1], 'wb').write(raw)
PYEOF
if $PY "$V/orbit_check.py" "$TMP/neg2.bin" 4 6 >/dev/null 2>&1; then echo "negative control (corrupted small certificate) NOT rejected"; fail=1; else echo "negative control (corrupted small certificate) rejected as expected"; fi
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
