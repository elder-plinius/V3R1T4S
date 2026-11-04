#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (Python 3 standard library only)
cd "$(dirname "$0")/.." || exit 1
# 1. the object is exactly the file this package claims (its sha256 also names the submission)
python3 -c "import hashlib,sys; h=hashlib.sha256(open('object/hsp4-141.txt','rb').read()).hexdigest(); print('object sha256 = '+h); sys.exit(h!='54f4b71bb63ae5ba84e04efa6555129c96d9d1d72f79a3c05c4fc24c98c0f1d3')" || { echo "error: object/hsp4-141.txt is not the claimed file"; echo FAIL; exit 1; }
# 2. the object beats the table cell, computed from the definition
python3 verify-it-yourself/check_hsp4.py object/hsp4-141.txt 141 0.224016561889
