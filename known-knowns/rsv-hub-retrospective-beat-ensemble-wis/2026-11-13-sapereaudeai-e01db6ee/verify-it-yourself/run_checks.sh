#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs Python 3 with pandas and pyarrow, and network access to raw.githubusercontent.com,
# or local copies: HUB=/path/to/rsv-forecast-hub EXT=/path/to/folder/with/scores.parquet+rsv_summary.csv
#   EXT2=/path/to/folder/with/rsv25-26_complete-model-scores.parquet, b2screen_leaderboard.csv, manifest.json, per-seed.csv, native-location-scores.csv sh verify-it-yourself/run_checks.sh
PY=${PYTHON:-python3}
if [ -n "$HUB" ]; then
  "$PY" verify-it-yourself/check_claim.py --hub "$HUB"
else
  "$PY" verify-it-yourself/check_claim.py
fi
exit $?
