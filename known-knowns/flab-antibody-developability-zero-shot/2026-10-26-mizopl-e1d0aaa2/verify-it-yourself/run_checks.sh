#!/bin/sh
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -x /opt/homebrew/bin/python3 ]; then
    PY=/opt/homebrew/bin/python3
else
    PY=python3
fi
"$PY" -B "$DIR/verify.py"
