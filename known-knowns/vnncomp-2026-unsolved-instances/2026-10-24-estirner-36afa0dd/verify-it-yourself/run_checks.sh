#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
# Python: $VNN_PYTHON if set, else $PYTHON, else python3 (needs numpy and onnxruntime; onnx for the second runtime).
# Set VNN_CACHE to a folder holding the two benchmark files to skip the downloads (the network file is 132.6 MB).
cd "$(dirname "$0")/.." || exit 1
${VNN_PYTHON:-${PYTHON:-python3}} verify-it-yourself/check.py "$@"
