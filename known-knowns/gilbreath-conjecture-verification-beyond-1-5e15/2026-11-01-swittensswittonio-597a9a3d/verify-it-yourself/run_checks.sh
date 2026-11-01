#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh   (last output line: PASS or FAIL)
# Needs only Python 3.9+ (standard library). About 1-8 minutes (the block recomputation sieves with pure Python).
# Steps: 1 sha256 of object/ files; 2 consistency of the recorded run summary (windows, counts, histogram, primecount values);
#        3 recompute the local depth of the 15 sample blocks (incl. the maximum-depth block) from their first primes, own sieve, pure Python.
# The FULL recomputation (GPU, about 3-5 hours) is RUN_IT_YOURSELF.md; its recorded output is object/run.log.
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
PY=python
command -v "$PY" >/dev/null 2>&1 || PY=python3
echo "step 1: hashes"
"$PY" -B verify-it-yourself/check_hashes.py || { echo FAIL; exit 1; }
echo "step 2: consistency"
R2=$("$PY" -B verify-it-yourself/check_consistency.py) || { echo "$R2"; echo FAIL; exit 1; }
echo "$R2"
echo "$R2" | grep -q '^PASS' || { echo FAIL; exit 1; }
echo "step 3: recompute sample blocks"
R3=$("$PY" -B verify-it-yourself/check_blocks.py object/sample_blocks.csv) || { echo "$R3"; echo FAIL; exit 1; }
echo "$R3"
echo "$R3" | grep -q '^PASS' || { echo FAIL; exit 1; }
echo PASS
