#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
python3 verify-it-yourself/check_one.py
