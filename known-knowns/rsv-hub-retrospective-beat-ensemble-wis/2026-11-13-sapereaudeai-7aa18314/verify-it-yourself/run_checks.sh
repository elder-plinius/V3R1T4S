#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs Python 3 with pyarrow (to read the hub's parquet files) and network access to raw.githubusercontent.com,
# or a local copy of the hub at the pinned commit: HUB=/path/to/rsv-forecast-hub sh verify-it-yourself/run_checks.sh
PY=${PYTHON:-python3}
if [ -n "$HUB" ]; then
  "$PY" verify-it-yourself/check_claim.py --hub "$HUB"
else
  "$PY" verify-it-yourself/check_claim.py
fi
exit $?
