#!/bin/sh
set -e
DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$DIR"
if [ -x /opt/homebrew/bin/python3 ]; then
    PY="/opt/homebrew/bin/python3"
else
    PY="python3"
fi
"$PY" -B verify-it-yourself/check_jarvis_clss_package.py
