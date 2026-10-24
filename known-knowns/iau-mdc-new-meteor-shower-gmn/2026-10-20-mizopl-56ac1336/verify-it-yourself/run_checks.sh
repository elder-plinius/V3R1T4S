#!/bin/sh
set -eu
DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
if [ -x /opt/homebrew/bin/python3 -B ]; then
    PY=/opt/homebrew/bin/python3
else
    PY=python3
fi
"$PY" "$DIR/verify-it-yourself/check_meteor_claim.py"
