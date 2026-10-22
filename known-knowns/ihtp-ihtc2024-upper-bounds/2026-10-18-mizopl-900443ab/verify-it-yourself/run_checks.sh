#!/bin/sh
set -eu
PY="python3"
if [ -x "/opt/homebrew/bin/python3" ]; then
    PY="/opt/homebrew/bin/python3"
fi
"$PY" verify-it-yourself/author_checker_ihtp_check.py verify-it-yourself/i27.json object/sol_i27.json 50063
