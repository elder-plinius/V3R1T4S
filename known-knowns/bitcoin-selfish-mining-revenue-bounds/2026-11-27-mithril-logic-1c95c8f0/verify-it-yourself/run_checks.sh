#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh   (python3 standard library only, ~25 s)
set -u
D=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 "$D/verify_all.py"
