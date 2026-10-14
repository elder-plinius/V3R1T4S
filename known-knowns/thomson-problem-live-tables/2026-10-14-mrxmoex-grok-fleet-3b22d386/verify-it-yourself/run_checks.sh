#!/bin/sh
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
EXPECT=3b22d38684a4aa0d8278bcca59ab9ea52bcc53357d1c09f01da653efa44d5329
GOT=$(python3 -c "import hashlib;print(hashlib.sha256(open('object/t2_550_polished.txt','rb').read()).hexdigest())")
echo "object sha256 $GOT"
if [ "$GOT" != "$EXPECT" ]; then echo "object sha256 differs from the published one"; echo FAIL; exit 1; fi
if python3 verify-it-yourself/check_thomson.py; then echo PASS; else echo FAIL; exit 1; fi
