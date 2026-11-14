#!/bin/sh
# Verify the pricing050 dual certificate from a clean copy of this package.
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Downloads the public MINLPLib instance (not shipped in the package), checks its
# sha256, installs python-flint into a local venv if needed, then verifies every
# leaf of object/cert_arb_leaves.json with Arb ball arithmetic.
# Last line: PASS or FAIL.
set -u
GMS_URL=https://www.minlplib.org/gms/pricing050.gms
GMS_SHA=192dd92d69cdcd131462d40c137df73dc101afef0739cc7ba98c130a79313715
D=verify-it-yourself/_instance
VENV=verify-it-yourself/_venv
OBJ_LAM=object/lambda.txt
OBJ_LEAVES=object/cert_arb_leaves.json
mkdir -p "$D"
if [ ! -s "$D/pricing050.gms" ]; then
  curl -fsS -A "V3R1T4S-verify (curl)" -o "$D/pricing050.gms" "$GMS_URL" || {
    echo "download failed: pricing050.gms"
    echo FAIL
    exit 1
  }
fi
got=$(sha256sum "$D/pricing050.gms" | awk '{print $1}')
if [ "$got" != "$GMS_SHA" ]; then
  echo "gms sha256 mismatch: got $got expected $GMS_SHA"
  echo FAIL
  exit 1
fi
echo "instance sha256 ok $got"
if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV" || { echo "venv failed"; echo FAIL; exit 1; }
  "$VENV/bin/pip" install -q --upgrade pip || { echo "pip upgrade failed"; echo FAIL; exit 1; }
  "$VENV/bin/pip" install -q 'python-flint==0.9.0' || {
    echo "python-flint install failed"
    echo FAIL
    exit 1
  }
fi
"$VENV/bin/python" -I verify-it-yourself/check_dual_certificate.py \
  "$D/pricing050.gms" "$OBJ_LAM" "$OBJ_LEAVES"
rc=$?
if [ "$rc" -eq 0 ]; then
  exit 0
fi
echo FAIL
exit 1
