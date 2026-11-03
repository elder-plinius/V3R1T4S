#!/bin/sh
set -e
DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$DIR"
PY="${PYTHON:-python3}"
"$PY" verify-it-yourself/check_68_14_5.py
