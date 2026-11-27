#!/bin/sh
# V3R1T4S package self-check for 2026-10-17-nukewire-f09f5eec.
# Invoked as `sh verify-it-yourself/run_checks.sh` in the package folder; the
# final output line of the run is PASS or FAIL.
# Any Python 3.8+ works; no third-party packages are needed.
cd "$(dirname "$0")/.." || { echo "FAIL: cannot locate package root"; exit 1; }
PY=""
for c in python3 python py; do
    command -v "$c" >/dev/null 2>&1 && PY="$c" && break
done
if [ -z "$PY" ]; then
    echo "FAIL: no python interpreter found"
    exit 1
fi
"$PY" verify-it-yourself/check.py
