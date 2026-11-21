#!/bin/sh
set -eu
DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
python3 "$DIR/check_mahler.py" "$DIR/../object/littlewood_d40.txt" 6.153645888590 18
