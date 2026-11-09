#!/bin/sh
python3 verify-it-yourself/check_v24.py
if [ $? -eq 0 ]; then
    echo "PASS"
    exit 0
else
    echo "FAIL"
    exit 1
fi
