#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (Python 3 standard library only)
cd "$(dirname "$0")/.." || exit 1
# 1. the object is exactly the file this package claims (its sha256 also names the submission)
python3 -c "import hashlib,sys; h=hashlib.sha256(open('object/hsp4_N215.txt','rb').read()).hexdigest(); print('object sha256 = '+h); sys.exit(h!='08d402ae2020be2bab2b33b7f3dd9846efc5ff6e7fe71f8715d4071c74238687')" || { echo "error: object/hsp4_N215.txt is not the claimed file"; echo FAIL; exit 1; }
# 2. the object beats the table cell, computed from the definition
python3 verify-it-yourself/check_hsp4.py object/hsp4_N215.txt 215 0.203682998566
