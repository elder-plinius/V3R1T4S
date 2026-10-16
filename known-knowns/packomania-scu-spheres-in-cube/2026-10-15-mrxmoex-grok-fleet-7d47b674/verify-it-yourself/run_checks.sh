#!/bin/sh
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
EXPECT=7d47b6743b44dbc43db4eb30485052b2702e3f210ec008288cde135425034c4e
GOT=$(python3 -c "import hashlib;print(hashlib.sha256(open('object/scu83_refined.txt','rb').read()).hexdigest())")
echo "object sha256 $GOT"
if [ "$GOT" != "$EXPECT" ]; then echo "object sha256 differs from the published one"; echo FAIL; exit 1; fi
if python3 verify-it-yourself/check_scu_p3.py; then echo PASS; else echo FAIL; exit 1; fi
