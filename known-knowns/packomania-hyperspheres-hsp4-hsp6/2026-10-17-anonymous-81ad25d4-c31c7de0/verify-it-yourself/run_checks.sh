#!/bin/sh
set -eu
if command -v python3 >/dev/null 2>&1; then
  exec python3 verify-it-yourself/check.py
else
  exec python verify-it-yourself/check.py
fi
