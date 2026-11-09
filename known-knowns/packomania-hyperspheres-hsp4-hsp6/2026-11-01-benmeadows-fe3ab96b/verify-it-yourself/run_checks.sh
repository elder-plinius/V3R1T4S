#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (Python 3 standard library only)
cd "$(dirname "$0")/.." || exit 1
# 1. the object is exactly the file this package claims (its sha256 also names the submission)
python3 -c "import hashlib,sys; h=hashlib.sha256(open('object/hsp4-160.txt','rb').read()).hexdigest(); print('object sha256 = '+h); sys.exit(h!='fe3ab96bf8a15a69dce5665ad60f28d88aa23ccb85c1239f2761375074d6e394')" || { echo "error: object/hsp4-160.txt is not the claimed file"; echo FAIL; exit 1; }
# 2. the object beats the table cell, computed from the definition
python3 verify-it-yourself/check_hsp4.py object/hsp4-160.txt 160 0.218358476129
