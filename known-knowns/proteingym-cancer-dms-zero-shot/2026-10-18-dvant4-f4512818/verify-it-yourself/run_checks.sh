#!/bin/sh
# Partial win p1: recompute all 13 pre-registered assays from object/ and the official ProteinGym v1.3 reference zip
# (downloaded once, 43 MB, sha256-verified; cached in DATA_DIR, default ./data). Python 3 standard library only.
# Optional: TABLE_CSV=<fresh copy of the live table>. Last line: PASS or FAIL.
set -u
PY=${PYTHON:-python3}
$PY -I -B verify-it-yourself/check_p1.py
