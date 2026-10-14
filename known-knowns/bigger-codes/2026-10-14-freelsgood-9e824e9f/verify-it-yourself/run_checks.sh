#!/bin/sh
set -eu
python3 -I -B verify-it-yourself/check_witness.py object/A27_6_10_13026.txt
python3 -I -B verify-it-yourself/check_rebuild.py how-we-built-it/reconstruction.py object/A27_6_10_13026.txt
python3 -I -B verify-it-yourself/check_encodings.py
printf 'PASS\n'
