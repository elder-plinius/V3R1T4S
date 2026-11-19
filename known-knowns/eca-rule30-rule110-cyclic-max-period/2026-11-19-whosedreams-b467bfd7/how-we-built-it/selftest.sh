#!/bin/bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
"$ROOT/build.sh"
OUT=${WORKDIR:-$ROOT/work/selftest}
mkdir -p "$OUT"
# Reproduce A334497(1..24) and A204371(1..30); report A334497(25..30)
export ROOT OUT
bash "$ROOT/scripts/selftest_run.sh" "$OUT"
# Fail if any BUG line
if grep -q '^BUG\| BUG ' "$OUT/selftest.log"; then
  echo "SELFTEST: FAIL (see $OUT/selftest.log)"
  exit 1
fi
echo "SELFTEST: PASS"
