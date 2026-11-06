#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
PY=${PYTHON:-python3}
FAILED=0
$PY -I verify-it-yourself/check_claim.py object/sequence_L401.txt || FAILED=1
# a checker that cannot fail proves nothing: flip one symbol of a copy and require a rejection
TMPF=verify-it-yourself/.flipped_copy.txt
$PY -I -c "import sys; t=open('object/sequence_L401.txt').read().strip(); i=len(t)//3; open(sys.argv[1],'w').write(t[:i]+('0' if t[i]=='1' else '1')+t[i+1:]+chr(10))" "$TMPF"
if $PY -I verify-it-yourself/check_claim.py "$TMPF" >/dev/null 2>&1; then echo "a corrupted copy was ACCEPTED"; FAILED=1; else echo "a corrupted copy is rejected"; fi
rm -f "$TMPF"
if [ $FAILED -eq 0 ]; then echo PASS; exit 0; else echo FAIL; exit 1; fi
