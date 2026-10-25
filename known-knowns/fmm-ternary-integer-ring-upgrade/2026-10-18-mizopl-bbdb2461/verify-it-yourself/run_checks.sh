#!/bin/sh
set -e
DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$DIR"
PY="/opt/homebrew/bin/python3"
[ -x "$PY" ] || PY="python3"
"$PY" verify-it-yourself/check_14x15x15.py
