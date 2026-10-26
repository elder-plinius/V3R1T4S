#!/bin/sh
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
/opt/homebrew/bin/python3 "$DIR/verify.py"
