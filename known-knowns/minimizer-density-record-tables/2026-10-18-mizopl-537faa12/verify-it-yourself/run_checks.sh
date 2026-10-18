#!/bin/sh
set -eu
PY="python3"
if [ -x "/opt/homebrew/bin/python3" ]; then
    PY="/opt/homebrew/bin/python3"
fi
"$PY" verify-it-yourself/author_checker_minimizer_check.py object/w12_k4_improved.gm the-record-we-beat/published_w12_k4.gm the-record-we-beat/k_extension_k16_w12.csv
