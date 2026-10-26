#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
# Default: fast exact checks (stdlib Python, about half a minute).
# GO=1: also rebuild the Go enumerator and rerun N = 3..14 and 16 (about a minute on 6 cores).
# FULL=1: also rerun N = 18 (about 10 minutes) and the N = 20 certificate table (about 2.5 hours on 6 cores),
#         then the certificate script on the regenerated table. WORKERS sets the thread count (default 6).
PY=${PYTHON:-python3}
command -v "$PY" >/dev/null 2>&1 || PY=python
"$PY" -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null || PY=python
"$PY" verify-it-yourself/check_fast.py || { echo "FAIL"; exit 1; }
if [ "${GO:-0}" = "1" ] || [ "${FULL:-0}" = "1" ]; then
  WK=${WORKERS:-6}
  W=$(mktemp -d)
  cp -R object/code/par "$W/par"
  (cd "$W/par" && GOTOOLCHAIN=auto go build -o par.exe .) || { echo "FAIL (go build)"; exit 1; }
  for n in 3 4 5 6 7 8 9 10 11 12 13 14; do
    nn=$(printf %02d "$n")
    "$W/par/par.exe" "$n" "$WK" > "$W/p$nn.txt" || { echo "FAIL (N = $n run)"; exit 1; }
    cmp -s "$W/p$nn.txt" "object/outputs/small/p$nn.txt" || { echo "FAIL (N = $n table differs)"; exit 1; }
  done
  "$W/par/par.exe" 16 "$WK" > "$W/p16.txt" && cmp -s "$W/p16.txt" object/outputs/p16.txt || { echo "FAIL (N = 16)"; exit 1; }
  echo "enumerator rebuilt: N = 3..14 and 16 reproduced byte for byte"
  if [ "${FULL:-0}" = "1" ]; then
    for n in 18 20; do
      date -u
      "$W/par/par.exe" "$n" "$WK" > "$W/p$n.txt" && cmp -s "$W/p$n.txt" "object/outputs/p$n.txt" || { echo "FAIL (N = $n)"; exit 1; }
      echo "N = $n reproduced byte for byte"
    done
    date -u
    "$PY" object/code/verify_cert.py "$W/p20.txt" 263376 | tee "$W/v.txt"
    grep -q "PASS: p_c >= 263376/10^6" "$W/v.txt" || { echo "FAIL (certificate on the regenerated table)"; exit 1; }
    rm -rf "$W"
    echo "PASS (full: N = 3..14, 16, 18 and 20 reproduced byte for byte; K_20(263376/10^6) < 1 on the regenerated table)"
  else
    rm -rf "$W"
    echo "PASS (go: N = 3..14 and 16 reproduced byte for byte)"
  fi
else
  echo "PASS"
fi
