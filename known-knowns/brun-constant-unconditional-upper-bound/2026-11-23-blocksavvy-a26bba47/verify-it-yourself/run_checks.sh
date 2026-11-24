#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (needs python3 >= 3.9, a C compiler, internet for pip once)
# Last output line is PASS or FAIL.
D=verify-it-yourself
if python3 -c "import flint, sys; sys.exit(0 if flint.__version__ == '0.9.0' else 1)" 2>/dev/null; then PY=python3
else
  V="$D/.venv"
  if [ ! -x "$V/bin/python" ]; then
    python3 -m venv "$V" >/dev/null 2>&1 && "$V/bin/python" -m pip install -q -r "$D/requirements.txt" >/dev/null 2>&1 || { echo "could not set up python-flint==0.9.0"; echo FAIL; exit 1; }
  fi
  PY="$V/bin/python"
fi
"$PY" "$D/check.py" || exit 1
