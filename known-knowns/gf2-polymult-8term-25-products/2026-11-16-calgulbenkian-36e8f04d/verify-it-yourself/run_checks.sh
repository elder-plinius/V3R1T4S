#!/bin/sh
set -u
if [ -f data/gf128-730-mult.slp ]; then
  python3 verify-it-yourself/verify_gf2m.py data/gf128-730-mult.slp --m 7 --poly 0x89 --max-gates 85 >/dev/null || { echo "FAIL"; exit 1; }
fi
python3 verify-it-yourself/verify_gf2m.py object/gf128_0x89_81gates.slp.txt --m 7 --poly 0x89 --max-gates 82 || exit 1
