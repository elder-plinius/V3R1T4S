#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (Python 3 standard library only)
cd "$(dirname "$0")/.." || exit 1
# 1. the object is exactly the file this package claims (its sha256 also names the submission)
python3 -c "import hashlib,sys; h=hashlib.sha256(open('object/hsp4-163.txt','rb').read()).hexdigest(); print('object sha256 = '+h); sys.exit(h!='7c6a8a80df2a86665a9af3715802976054a9223efa6181be86d745d1264299c6')" || { echo "error: object/hsp4-163.txt is not the claimed file"; echo FAIL; exit 1; }
# 2. the object beats the table cell, computed from the definition
python3 verify-it-yourself/check_hsp4.py object/hsp4-163.txt 163 0.217115168538
