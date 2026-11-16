#!/bin/sh
set -eu
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/verify_qrac4.py" "$SCRIPT_DIR/../object/certificate_qrac4.json"
