#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
if python3 verify-it-yourself/check_route.py; then
  :
else
  echo FAIL
  exit 1
fi
