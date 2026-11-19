#!/bin/sh
set -e
DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
python3 "$DIR/verify-it-yourself/check_akkadian_package.py"
