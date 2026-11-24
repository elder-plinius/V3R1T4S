#!/bin/sh
set -eu
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PKG_DIR="$(dirname -- "$SCRIPT_DIR")"
python3 "$SCRIPT_DIR/verify_bbpt8.py" "$PKG_DIR/object/bbpt8_certificates.json"
