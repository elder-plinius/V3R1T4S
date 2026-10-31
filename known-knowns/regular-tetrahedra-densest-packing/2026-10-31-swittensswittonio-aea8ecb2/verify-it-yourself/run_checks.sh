#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh   (last output line: PASS or FAIL)
# Needs python (3.9+) and network access (pip install python-flint==0.9.0 numpy) unless python-flint is importable.
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
PY=python
command -v "$PY" >/dev/null 2>&1 || PY=python3
TMP=
finish() {
  rc=$1
  [ -n "$TMP" ] && rm -rf "$TMP" 2>/dev/null || true
  if [ "$rc" -eq 0 ]; then echo PASS; exit 0; else echo FAIL; exit 1; fi
}
trap 'finish 1' EXIT INT TERM HUP
set -u
echo "step 1: sha256 of every file in object/"
"$PY" -I -B verify-it-yourself/check_hashes.py || finish 1
echo "step 2: python-flint (Arb)"
if "$PY" -c "import flint; assert flint.__version__ == '0.9.0'" >/dev/null 2>&1; then
  RUNPY="$PY"; echo "using installed python-flint 0.9.0"
else
  TMP=$(mktemp -d) || finish 1
  "$PY" -m venv "$TMP/venv" || finish 1
  if [ -x "$TMP/venv/Scripts/python.exe" ]; then RUNPY="$TMP/venv/Scripts/python.exe"; else RUNPY="$TMP/venv/bin/python"; fi
  "$RUNPY" -m pip install --quiet python-flint==0.9.0 numpy || finish 1
fi
echo "step 3: exact-integer branch-and-bound for K4 (eps = 1/1000)"
KOUT=$("$PY" -B object/code/k4_bb.py 1 1000) || { echo "$KOUT" | tail -3; finish 1; }
echo "$KOUT" | tail -3
echo "$KOUT" | tail -1 | grep -q '^RESULT: PROVED (all boxes certified)' || finish 1
echo "step 4: re-certification with Arb"
OUT=$("$RUNPY" -B object/code/verify_final.py 40 1000) || { echo "$OUT"; finish 1; }
echo "$OUT" | tail -4
echo "$OUT" | tail -1 | grep -q '^CERTIFIED (Arb, modulo the Residual trust list) density <= 1 - 4.501166e-15' || finish 1
trap - EXIT
finish 0
