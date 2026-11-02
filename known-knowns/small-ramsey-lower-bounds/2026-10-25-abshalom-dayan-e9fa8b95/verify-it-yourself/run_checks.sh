#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Checks the object's sha256, then runs verify_circ.py (Python standard library only): every distance gets
# exactly one colour, and for each colour an exhaustive branch and bound finds no forbidden clique through
# vertex 0 (rotations are automorphisms of a circulant, so every clique can be moved to contain 0).
WANT=e9fa8b95605e0f8e8d7b020855f7905ff9c02269c9d49a48abd725e7858d6a40
got=$(python3 -c "import hashlib; print(hashlib.sha256(open('object/R_3_4_7.txt', 'rb').read()).hexdigest())")
echo "sha256 $got"
out=$(python3 verify-it-yourself/verify_circ.py object/R_3_4_7.txt 3 4 7 2>&1)
rc=$?
printf '%s\n' "$out"
if [ "$got" = "$WANT" ] && [ $rc -eq 0 ] && printf '%s\n' "$out" | grep -qxF "proves R(3,4,7) >= 154"; then
  echo PASS
else
  echo FAIL
  exit 1
fi
