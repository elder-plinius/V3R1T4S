#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Checks the object's sha256, then runs verify_circ.py (Python standard library only): every distance gets
# exactly one colour, and for each colour an exhaustive branch and bound finds no forbidden clique through
# vertex 0 (rotations are automorphisms of a circulant, so every clique can be moved to contain 0).
WANT=622b79c6646d2617cd7f0b74c224ad3d5bd6cb856c6824ace5a5e30664461270
got=$(python3 -c "import hashlib; print(hashlib.sha256(open('object/R_3_3_11.txt', 'rb').read()).hexdigest())")
echo "sha256 $got"
out=$(python3 verify-it-yourself/verify_circ.py object/R_3_3_11.txt 3 3 11 2>&1)
rc=$?
printf '%s\n' "$out"
if [ "$got" = "$WANT" ] && [ $rc -eq 0 ] && printf '%s\n' "$out" | grep -qxF "proves R(3,3,11) >= 183"; then
  echo PASS
else
  echo FAIL
  exit 1
fi
