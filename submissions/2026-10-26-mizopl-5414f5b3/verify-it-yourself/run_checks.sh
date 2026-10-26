#!/bin/sh
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -x /opt/homebrew/bin/python3 ]; then
    /opt/homebrew/bin/python3 "$DIR/verify.py"
else
    python3 "$DIR/verify.py"
fi
