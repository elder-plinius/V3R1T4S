#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (python3 >= 3.8; pip access once if mpmath is missing). Last line PASS or FAIL.
# Checks object/certificate.json at 200 and 300 bits with mpmath interval arithmetic; PASS only if both pass.
D=verify-it-yourself
if python3 -c "import mpmath" 2>/dev/null; then PY=python3
else
  V="$D/.venv"
  if [ ! -x "$V/bin/python" ]; then
    python3 -m venv "$V" >/dev/null 2>&1 && "$V/bin/python" -m pip install -q -r "$D/requirements.txt" >/dev/null 2>&1 || { echo "could not set up mpmath==1.3.0"; echo FAIL; exit 1; }
  fi
  PY="$V/bin/python"
fi
"$PY" "$D/check_threshold.py" object/certificate.json || { echo FAIL; exit 1; }
