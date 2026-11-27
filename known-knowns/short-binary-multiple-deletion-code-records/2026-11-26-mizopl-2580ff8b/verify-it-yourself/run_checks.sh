#!/bin/sh
set -eu
python3 verify-it-yourself/verify.py
if python3 verify-it-yourself/verify.py --corrupt >/dev/null 2>&1; then
  echo 'ERROR: --corrupt control did not fail'
  exit 1
fi
echo '[OK] --corrupt negative control exited 1'
echo 'PASS'
