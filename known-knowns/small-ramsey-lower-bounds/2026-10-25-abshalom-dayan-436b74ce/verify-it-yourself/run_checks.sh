#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Checks the object's sha256, then runs verify_circ.py (Python standard library only): every distance gets
# exactly one colour, and for each colour an exhaustive branch and bound finds no forbidden clique through
# vertex 0 (rotations are automorphisms of a circulant, so every clique can be moved to contain 0).
WANT=436b74cecb10c8263ed5c3413d66993ce1f9d34993718f7b5bb4b31890896826
got=$(python3 -c "import hashlib; print(hashlib.sha256(open('object/R_3_5_6.txt', 'rb').read()).hexdigest())")
echo "sha256 $got"
out=$(python3 verify-it-yourself/verify_circ.py object/R_3_5_6.txt 3 5 6 2>&1)
rc=$?
printf '%s\n' "$out"
if [ "$got" = "$WANT" ] && [ $rc -eq 0 ] && printf '%s\n' "$out" | grep -qxF "proves R(3,5,6) >= 183"; then
  echo PASS
else
  echo FAIL
  exit 1
fi
