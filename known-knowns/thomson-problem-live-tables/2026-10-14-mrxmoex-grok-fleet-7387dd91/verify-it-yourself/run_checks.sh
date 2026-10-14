#!/bin/sh
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
EXPECT=7387dd9198125fa72fa8cc7fc25cb8523ea4d4e126ab66c7952b010c370dd499
GOT=$(python3 -c "import hashlib;print(hashlib.sha256(open('object/cand_745.txt','rb').read()).hexdigest())")
echo "object sha256 $GOT"
if [ "$GOT" != "$EXPECT" ]; then echo "object sha256 differs from the published one"; echo FAIL; exit 1; fi
if python3 verify-it-yourself/check_thomson.py; then echo PASS; else echo FAIL; exit 1; fi
