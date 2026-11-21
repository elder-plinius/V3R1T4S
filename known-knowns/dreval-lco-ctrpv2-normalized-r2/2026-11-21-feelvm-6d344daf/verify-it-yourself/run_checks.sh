#!/bin/sh
# Run from the package folder. Last line: PASS or FAIL.
python3 verify-it-yourself/checker.py || python verify-it-yourself/checker.py
