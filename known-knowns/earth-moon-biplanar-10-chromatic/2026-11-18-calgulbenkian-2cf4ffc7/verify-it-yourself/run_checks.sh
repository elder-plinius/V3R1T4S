#!/bin/sh
set -eu
DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
python3 "$DIR/verify_claim.py" || { echo "FAIL"; exit 1; }
