#!/bin/sh
set -eu
DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
python3 "$DIR/check_cami2_binning.py"
