#!/bin/sh
set -u
if ! python3 verify-it-yourself/check_assignment.py object/assignment.txt 25 180870896; then
  echo FAIL
  exit 1
fi
if ! python3 verify-it-yourself/check_assignment_independent.py object/assignment.txt; then
  echo FAIL
  exit 1
fi
echo PASS
