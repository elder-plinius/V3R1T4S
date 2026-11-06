#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Last line: PASS or FAIL.
python3 verify-it-yourself/check_thomson.py object/thomson-436.txt 90020.68126807301182651446 90020.71608562 \
  41e0a75b4b6d5bbb4a7c8f3d951ab712da44e958b69641eb2ac2c2da3967f979
