#!/bin/sh
set -eu
DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
python3 "$DIR/check_mahler.py" "$DIR/../object/littlewood_d32.txt" 5.456083591785 18
