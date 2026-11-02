#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (Python 3 standard library only)
cd "$(dirname "$0")/.." || exit 1
# 1. the object is exactly the file this package claims (its sha256 also names the submission)
python3 -c "import hashlib,sys; h=hashlib.sha256(open('object/hsp4_N216.txt','rb').read()).hexdigest(); print('object sha256 = '+h); sys.exit(h!='bacd6f0e9c0c6e94c1b7a2afea1b4872922c1cdd2f69e69c07d06d35b9f5e968')" || { echo "error: object/hsp4_N216.txt is not the claimed file"; echo FAIL; exit 1; }
# 2. the object beats the table cell, computed from the definition
python3 verify-it-yourself/check_hsp4.py object/hsp4_N216.txt 216 0.203582040585
