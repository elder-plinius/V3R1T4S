#!/bin/sh
set -eu
DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec python3 "$DIR/verify_flt_subsingleton.py"
