#!/bin/sh
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
EXPECT=4a2c00fcdc3549bda75224082644d3f131ed369573e4784c5af00e1d82e2ad52
GOT=$(python3 -c "import hashlib;print(hashlib.sha256(open('object/riesz_3552_polished.txt','rb').read()).hexdigest())")
echo "object sha256 $GOT"
if [ "$GOT" != "$EXPECT" ]; then echo "object sha256 differs from the published one"; echo FAIL; exit 1; fi
if python3 verify-it-yourself/check_thomson.py; then echo PASS; else echo FAIL; exit 1; fi
