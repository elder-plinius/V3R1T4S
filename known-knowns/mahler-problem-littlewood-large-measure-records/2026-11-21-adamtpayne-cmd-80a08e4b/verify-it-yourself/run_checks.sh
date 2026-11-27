#!/bin/sh
set -eu
DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
python3 "$DIR/check_mahler.py" "$DIR/../object/littlewood_d36.txt" 5.823385551581 18
