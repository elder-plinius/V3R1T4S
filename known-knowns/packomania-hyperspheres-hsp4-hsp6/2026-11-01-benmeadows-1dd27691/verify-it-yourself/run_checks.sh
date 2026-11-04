#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (Python 3 standard library only)
cd "$(dirname "$0")/.." || exit 1
# 1. the object is exactly the file this package claims (its sha256 also names the submission)
python3 -c "import hashlib,sys; h=hashlib.sha256(open('object/hsp4_N213.txt','rb').read()).hexdigest(); print('object sha256 = '+h); sys.exit(h!='1dd2769172958fa1083d9614660de9dfb4e262f6235d897100991024b4839e8c')" || { echo "error: object/hsp4_N213.txt is not the claimed file"; echo FAIL; exit 1; }
# 2. the object beats the table cell, computed from the definition
python3 verify-it-yourself/check_hsp4.py object/hsp4_N213.txt 213 0.204053178162
