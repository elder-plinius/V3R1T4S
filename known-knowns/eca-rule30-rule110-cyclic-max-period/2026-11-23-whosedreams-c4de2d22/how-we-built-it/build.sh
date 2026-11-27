#!/bin/bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
cc -O3 -march=native -o "$ROOT/impl1/maxcycle" "$ROOT/impl1/maxcycle.c"
cc -O3 -march=native -o "$ROOT/impl2/maxcycle" "$ROOT/impl2/maxcycle.c"
echo "built impl1 and impl2"
