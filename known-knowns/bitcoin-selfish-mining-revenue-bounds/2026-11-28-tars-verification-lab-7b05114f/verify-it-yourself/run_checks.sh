#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
set -eu
if [ ! -f object/exact_dual_rho169_250.json ] || [ ! -f object/over_bias.npy ] || [ ! -f object/over_policy.npy ]; then
    echo "missing object files" >&2
    echo FAIL
    exit 1
fi
if ! sha256sum -c verify-it-yourself/object.sha256; then
    echo FAIL
    exit 1
fi
if ! python3 verify-it-yourself/exact_dual_check.py; then
    echo FAIL
    exit 1
fi
echo PASS
