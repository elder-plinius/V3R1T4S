#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(dirname "$HERE")
python3 "$HERE/check_graph.py" "$ROOT/object/G_13_4_n6631.edges" 13 4
echo PASS
