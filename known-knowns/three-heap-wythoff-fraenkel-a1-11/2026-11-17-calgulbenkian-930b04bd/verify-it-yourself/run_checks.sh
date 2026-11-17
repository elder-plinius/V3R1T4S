#!/bin/sh
set -eu
DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
python3 "$DIR/verify-it-yourself/verify_wythoff.py" "$DIR/object/wythoff_a1_11_certificate.json"
