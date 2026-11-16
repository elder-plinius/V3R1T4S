#!/bin/sh
set -u
if [ -f data/gf128-740-mult.slp ]; then
  python3 verify-it-yourself/verify_gf2m.py data/gf128-740-mult.slp --m 7 --poly 0x91 --max-gates 84 >/dev/null || { echo "FAIL"; exit 1; }
fi
python3 verify-it-yourself/verify_gf2m.py object/gf128_0x91_82gates.slp.txt --m 7 --poly 0x91 --max-gates 83 || exit 1
