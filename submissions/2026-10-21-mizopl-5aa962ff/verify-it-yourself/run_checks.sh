#!/bin/sh
set -e
PY="/opt/homebrew/bin/python3"
if [ ! -x "$PY" ]; then
  PY="python3"
fi
"$PY" -B "$(dirname "$0")/check_akkadian_package.py"
