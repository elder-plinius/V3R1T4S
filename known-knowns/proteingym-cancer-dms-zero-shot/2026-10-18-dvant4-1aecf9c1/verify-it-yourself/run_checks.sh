#!/bin/sh
# Recompute the claim from the saved object and the official ProteinGym v1.3 reference file (downloaded once, 43 MB,
# sha256-verified; cached in DATA_DIR, default ./data). Python 3 standard library only. Last line: PASS or FAIL.
# Optional: TABLE_CSV=<fresh copy of the live DMS-level Spearman CSV> sh verify-it-yourself/run_checks.sh
set -u
PY=${PYTHON:-python3}
$PY -I -B verify-it-yourself/check_spearman.py
