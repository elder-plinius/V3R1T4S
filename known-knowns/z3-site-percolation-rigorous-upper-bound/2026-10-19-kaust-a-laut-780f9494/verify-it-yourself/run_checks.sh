#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
# Default: fast exact checks (stdlib Python, seconds). FULL=1: also rebuild the Go engine and rerun the whole
# exhaustive certificate (counts over all 2^27 states, then all seven links), about 12 minutes on 6 cores, ~2 GB.
PY=${PYTHON:-python3}
command -v "$PY" >/dev/null 2>&1 || PY=python
"$PY" -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null || PY=python
"$PY" verify-it-yourself/check_fast.py || { echo "FAIL"; exit 1; }
if [ "${FULL:-0}" = "1" ]; then
  set -e
  W=$(mktemp -d)
  cp -R object/code "$W/code"
  (cd "$W/code/cert" && GOTOOLCHAIN=auto go build -o cert.exe .)
  "$W/code/cert/cert.exe" 3 3 3 6 6 counts "$W/counts.txt"
  cmp "$W/counts.txt" object/counts_b333_s6.txt
  "$PY" "$W/code/chain.py" "$W/counts.txt" "$W/chainB" q1=501/1000 2317/5000 9/20 1781/4000 | tee "$W/b.txt"
  "$PY" "$W/code/chain.py" "$W/counts.txt" "$W/chainA" q1=1781/4000 1109/2500 443/1000 1107/2500 4427/10000 | tee "$W/a.txt"
  npass=$(cat "$W/b.txt" "$W/a.txt" | grep -c "CERTIFICATE: PASS")
  rm -rf "$W"
  if [ "$npass" -ne 7 ]; then echo "FAIL (only $npass of 7 links passed)"; exit 1; fi
  echo "PASS (full: counts reproduced byte for byte, 7 of 7 links certified)"
else
  echo "PASS"
fi
