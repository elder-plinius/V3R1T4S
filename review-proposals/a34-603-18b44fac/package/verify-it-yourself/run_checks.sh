#!/bin/sh
set -eu
python3 verify-it-yourself/validate.py
python3 verify-it-yourself/upstream_cwcheck.py object/A34_8_7_603.txt 34 8 7 --M 603 --sha256 18b44fac5d5ff1d4895fd9de1240669eb71543b3e15599f7f864e090aa1491ad
printf 'PASS\n'
