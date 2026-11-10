#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (about 160 s, one thread, about 0.85 GB)
# REQUIREMENT: a Python 3 with python-flint 0.9.0 (pip install python-flint==0.9.0).
# The script tries, in order: $PYTHON, python3, python, "py -3", and ./.venv or ./venv in this folder or its parent.
# If none of them can import flint, it says so and prints FAIL; then set PYTHON=/path/to/that/python and rerun.
# Last line: PASS or FAIL.
try_py() {
  [ -z "$1" ] && return 1
  # shellcheck disable=SC2086
  $1 -c "import flint" >/dev/null 2>&1
}
PY=""
for c in "$PYTHON" python3 python "py -3" ./.venv/bin/python ./.venv/Scripts/python.exe ./venv/bin/python ./venv/Scripts/python.exe ../.venv/bin/python ../.venv/Scripts/python.exe; do
  if try_py "$c"; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then
  echo "This check needs Python 3 with python-flint 0.9.0 (pip install python-flint==0.9.0)."
  echo "None of \$PYTHON, python3, python, py -3 or a .venv/venv next to this folder can import flint."
  echo "Set PYTHON=/path/to/a/python/with/python-flint and run again: PYTHON=... sh verify-it-yourself/run_checks.sh"
  echo FAIL
  exit 1
fi
echo "using: $PY"
# shellcheck disable=SC2086
$PY verify-it-yourself/check_enclosure.py
