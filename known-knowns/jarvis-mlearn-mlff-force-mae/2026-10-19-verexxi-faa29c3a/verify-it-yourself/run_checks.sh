#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh   (last line PASS or FAIL; exit status non-zero on FAIL)
cd "$(dirname "$0")/.." || exit 1
PY=${PYTHON:-$(command -v python3 || command -v python)}
$PY verify-it-yourself/fetch_sources.py benchmark.json.zip || { echo FAIL; exit 1; }
$PY verify-it-yourself/check_predictions.py | grep -v "^PASS$"
$PY verify-it-yourself/check_predictions.py >/dev/null || { echo FAIL; exit 1; }  # second run only for the exit status
# optional heavy step: re-run the saved models (needs numpy ase torch mace-torch); set MLFF_PYTHON to a python that has them
MP=${MLFF_PYTHON:-$PY}
if $MP -c "import numpy, ase, torch, mace.calculators" >/dev/null 2>&1; then
  $MP verify-it-yourself/fetch_sources.py mlearn_figshare.zip || { echo FAIL; exit 1; }
  $MP verify-it-yourself/rerun_models.py || { echo FAIL; exit 1; }
else
  echo "SKIPPED rerun_models.py (numpy/ase/torch/mace-torch not importable; set MLFF_PYTHON to run it)"
fi
echo PASS
