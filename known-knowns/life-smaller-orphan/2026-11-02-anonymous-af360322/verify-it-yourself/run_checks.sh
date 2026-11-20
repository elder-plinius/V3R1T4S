#!/bin/sh
# run from the package folder: sh verify-it-yourself/run_checks.sh   (last line PASS or FAIL)
cd "$(dirname "$0")/.." || exit 1
fail() { echo "$1"; echo FAIL; exit 1; }
[ -f object/certificate.tsv ] || fail "missing object/certificate.tsv"
sha256sum -c verify-it-yourself/OBJECT_SHA256 >/dev/null 2>&1 || fail "object sha256 mismatch"
python3 verify-it-yourself/verify.py object/certificate.tsv || fail "verify.py failed"
echo PASS
