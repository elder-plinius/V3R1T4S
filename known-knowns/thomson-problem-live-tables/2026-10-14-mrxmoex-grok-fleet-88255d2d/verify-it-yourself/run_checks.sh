#!/bin/sh
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
EXPECT=88255d2d000d027818f81d6b3eb6a3d6206bc8788f6d1ab7010decbbcb1e195c
GOT=$(python3 -c "import hashlib;print(hashlib.sha256(open('object/cand_777.txt','rb').read()).hexdigest())")
echo "object sha256 $GOT"
if [ "$GOT" != "$EXPECT" ]; then echo "object sha256 differs from the published one"; echo FAIL; exit 1; fi
if python3 verify-it-yourself/check_thomson.py; then echo PASS; else echo FAIL; exit 1; fi
