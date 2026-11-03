#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Downloads the organisers' instance archive once (not redistributed here), checks its sha256,
# extracts i18.json and checks object/sol_i18.json. Last line: PASS or FAIL.
set -u
T=$(mktemp -d) || { echo FAIL; exit 1; }
trap 'rm -rf "$T"' EXIT
curl -sS -A 'V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)' -o "$T/a.zip" https://ihtc2024.github.io/assets/files/ihtc2024_competition_instances.zip || { echo "download failed"; echo FAIL; exit 1; }
python3 - "$T/a.zip" "$T/i18.json" <<'PY' || { echo FAIL; exit 1; }
import hashlib, sys, zipfile
z = open(sys.argv[1], 'rb').read()
h = hashlib.sha256(z).hexdigest()
print('archive sha256', h)
assert h == '365a05227c156029d3653d6997ddf28392a728521722f37ad9edf4368ac6f681', 'archive changed since the claim'
open(sys.argv[2], 'wb').write(zipfile.ZipFile(sys.argv[1]).read('i18.json'))
PY
python3 verify-it-yourself/check_ihtp.py "$T/i18.json" object/sol_i18.json
