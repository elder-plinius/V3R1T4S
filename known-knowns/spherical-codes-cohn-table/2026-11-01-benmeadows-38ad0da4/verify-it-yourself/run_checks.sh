#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (Python 3 standard library only)
cd "$(dirname "$0")/.." || exit 1
# 1. the object is exactly the file this package claims (its sha256 also names the submission)
python3 -c "import hashlib,sys; h=hashlib.sha256(open('object/31_64.txt','rb').read()).hexdigest(); print('object sha256 = '+h); sys.exit(h!='38ad0da445de5d19f7c844db0f7bc44333c26366abf258b5118f9e00abcf421a')" || { echo "error: object/31_64.txt is not the claimed file"; echo FAIL; exit 1; }
# 2. the object beats the table cell, computed from the definition
python3 verify-it-yourself/check_sph.py object/31_64.txt 31 64 0.030322662292
