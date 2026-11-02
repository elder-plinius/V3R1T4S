#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (Python 3 standard library only)
cd "$(dirname "$0")/.." || exit 1
# 1. the object is exactly the file this package claims (its sha256 also names the submission)
python3 -c "import hashlib,sys; h=hashlib.sha256(open('object/hsp4-156.txt','rb').read()).hexdigest(); print('object sha256 = '+h); sys.exit(h!='a7ced3321fa76c13cb6372501334593f81d9a0385864873726b3b9fb87483f3b')" || { echo "error: object/hsp4-156.txt is not the claimed file"; echo FAIL; exit 1; }
# 2. the object beats the table cell, computed from the definition
python3 verify-it-yourself/check_hsp4.py object/hsp4-156.txt 156 0.220308265077
