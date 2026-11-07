#!/bin/sh
set -eu
if command -v python >/dev/null 2>&1; then
  exec python verify-it-yourself/check.py
fi
exec python3 verify-it-yourself/check.py
