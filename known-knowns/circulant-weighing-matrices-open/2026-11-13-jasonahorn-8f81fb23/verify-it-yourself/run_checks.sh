#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1
if ! python3 -B verify-it-yourself/test_verifier.py; then
    printf 'FAIL\n'
    exit 1
fi
exec python3 -B verify-it-yourself/check.py
