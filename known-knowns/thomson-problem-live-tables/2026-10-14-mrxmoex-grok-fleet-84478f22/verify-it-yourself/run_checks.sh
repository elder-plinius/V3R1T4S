#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
EXPECT=84478f227719968b370a72c37f1189cf5f618436411f1127fcae99e464a01ce2
GOT=$(python3 -c "import hashlib;print(hashlib.sha256(open('object/cand_1382.txt','rb').read()).hexdigest())")
echo "object sha256 $GOT"
if [ "$GOT" != "$EXPECT" ]; then echo "object sha256 differs from the published one"; echo FAIL; exit 1; fi
if python3 verify-it-yourself/check_thomson.py; then echo PASS; else echo FAIL; exit 1; fi
