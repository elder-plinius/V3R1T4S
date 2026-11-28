#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
PY=$(command -v python3 || command -v python)
"$PY" verify-it-yourself/check_all.py c6c683024171c1fc2a95a3f8699d1d353f358c603c555fcd743941f15b67e13d
