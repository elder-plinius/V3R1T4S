#!/bin/sh
set -eu
DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
python3 "$DIR/verify-it-yourself/verify_qrac333.py" "$DIR/object/qrac_333_naimark_dual_p1.json"
