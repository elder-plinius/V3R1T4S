#!/bin/sh
if ! python3 -B verify-it-yourself/tests.py; then
  echo FAIL
  exit 1
fi
if ! python3 -B verify-it-yourself/verify.py object/A35_6_6_2225.txt 2225; then
  echo FAIL
  exit 1
fi
