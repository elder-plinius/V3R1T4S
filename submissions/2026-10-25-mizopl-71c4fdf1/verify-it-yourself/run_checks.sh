#!/bin/sh
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -x python3 ]; then
    PY=python3
else
    PY=python3
fi
"$PY" -B "$DIR/verify.py"
