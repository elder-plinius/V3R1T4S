#!/bin/sh
# Standard-library check of object/thomson_743.txt. Run from the package folder: sh verify-it-yourself/run_checks.sh
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
EXPECT=1e5a75909e58d1a4347aaaad37053aa7e22cd164f8da0d8fd26cc2870d78471b
GOT=$(python3 -c "import hashlib;print(hashlib.sha256(open('object/thomson_743.txt','rb').read()).hexdigest())")
echo "object sha256 $GOT"
if [ "$GOT" != "$EXPECT" ]; then echo "object sha256 differs from the published one"; echo FAIL; exit 1; fi
# energy (decimal, 40 digits), tangent gradient, margin under the lowest previously known value (merged #125)
if python3 -I verify-it-yourself/verify_stdlib.py object/thomson_743.txt --bar 264837.5287041150044362828 --expect 264837.4538033452076921018; then echo PASS; else echo FAIL; exit 1; fi
