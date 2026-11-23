#!/bin/sh
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
PKG="$(cd "$DIR/.." && pwd)"

if [ -x /opt/homebrew/bin/python3 ]; then
    PY=/opt/homebrew/bin/python3
else
    PY=python3
fi

"$PY" -B "$DIR/verify.py" --cert "$PKG/object/p2_0725_optimality_certificate.json"
