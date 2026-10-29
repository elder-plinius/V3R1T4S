#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Checks the object's sha256, then runs verify_join.py (Python standard library only): symmetric matrix with
# colours 1..3; colours 1 and 2 have no triangle (every edge checked); vertices 0..265 form a circulant whose
# colour-3 clique number is found by exhaustive branch and bound through vertex 0; vertices 266..270 have no
# colour-3 edge among themselves, so a colour-3 clique holds at most one of them.
WANT=4e457e7ee1232a6b4c5ea299b7616c6e4329f04ba11531cadacd4a0d715e9ca7
got=$(python3 -c "import hashlib; print(hashlib.sha256(open('object/R_3_3_15.txt', 'rb').read()).hexdigest())")
echo "sha256 $got"
out=$(python3 verify-it-yourself/verify_join.py object/R_3_3_15.txt 266 2>&1)
rc=$?
printf '%s\n' "$out"
if [ "$got" = "$WANT" ] && [ $rc -eq 0 ] && printf '%s\n' "$out" | grep -qxF "proves R(3,3,15) >= 272"; then
  echo PASS
else
  echo FAIL
  exit 1
fi
