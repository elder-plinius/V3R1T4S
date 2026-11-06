#!/bin/sh
# Standalone stdlib check (2-4 min). Last line: PASS or FAIL.
cd "$(dirname "$0")"
PY=""
for c in python3 python py; do
    if command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then
    echo "FAIL: no python interpreter found"
    exit 1
fi
"$PY" verify_standalone.py
