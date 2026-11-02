#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (Python 3 standard library only)
cd "$(dirname "$0")/.." || exit 1
# 1. the object is exactly the file this package claims (its sha256 also names the submission)
python3 -c "import hashlib,sys; h=hashlib.sha256(open('object/hsp4_N214.txt','rb').read()).hexdigest(); print('object sha256 = '+h); sys.exit(h!='c0fc1b302af41f2cd3b2fe423c866d95d9695c4dc46705a49b55113d2694dc67')" || { echo "error: object/hsp4_N214.txt is not the claimed file"; echo FAIL; exit 1; }
# 2. the object beats the table cell, computed from the definition
python3 verify-it-yourself/check_hsp4.py object/hsp4_N214.txt 214 0.203884464476
