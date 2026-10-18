#!/bin/sh
set -u
PYTHON=${PYTHON:-python3}
if "$PYTHON" verify-it-yourself/check_object_identity.py &&
   "$PYTHON" verify-it-yourself/independent_check.py &&
   "$PYTHON" verify-it-yourself/verify_algebraic_core_direct.py object/algebraic-core-direct.json
then
  echo PASS
else
  echo FAIL
  exit 1
fi
