#!/bin/sh
set -u

python3 verify-it-yourself/verify_bb_logical.py \
  object/bb504_logical_wt28.txt \
  -l 42 -m 6 \
  -a "x^27+y+y^2" \
  -b "y^3+x^37+x^38" \
  --k 12 \
  --max-weight 29 || exit 1
