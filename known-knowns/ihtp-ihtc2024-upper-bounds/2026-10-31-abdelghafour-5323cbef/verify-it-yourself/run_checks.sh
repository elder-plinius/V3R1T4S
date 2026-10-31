#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Downloads the organisers' instance archive once (not redistributed here), checks its sha256,
# extracts m19.json and checks object/sol_m19.json. Last line: PASS or FAIL.
set -u
T=$(mktemp -d) || { echo FAIL; exit 1; }
trap 'rm -rf "$T"' EXIT
curl -sS -A 'V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)' -o "$T/a.zip" https://ihtc2024.github.io/assets/files/ihtc2024_final_instances.zip || { echo "download failed"; echo FAIL; exit 1; }
python3 - "$T/a.zip" "$T/m19.json" <<'PY' || { echo FAIL; exit 1; }
import hashlib, sys, zipfile
z = open(sys.argv[1], 'rb').read()
h = hashlib.sha256(z).hexdigest()
print('archive sha256', h)
assert h == 'f2037aaf982531f6e21c13334f82c74d7baabbdf4fcda481147c30426b1a10fd', 'archive changed since the claim'
open(sys.argv[2], 'wb').write(zipfile.ZipFile(sys.argv[1]).read('m19.json'))
PY
python3 verify-it-yourself/check_ihtp.py "$T/m19.json" object/sol_m19.json
