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
echo "step 3: re-certification with Arb"
OUT=$("$RUNPY" -B object/verify_final2.py 40) || { echo "$OUT"; finish 1; }
echo "$OUT"
echo "$OUT" | grep -q '^rho_hat(0,Q) used = .* CERTIFIED density <= 1 - 4.501141e-15' || finish 1
echo "$OUT" | grep -q 'strictly larger: True' || finish 1
trap - EXIT
finish 0
