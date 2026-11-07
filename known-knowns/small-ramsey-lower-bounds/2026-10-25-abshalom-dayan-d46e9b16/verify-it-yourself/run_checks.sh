#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Checks the object's sha256, then runs verify_circ.py (Python standard library only): every distance gets
# exactly one colour, and for each colour an exhaustive branch and bound finds no forbidden clique through
# vertex 0 (rotations are automorphisms of a circulant, so every clique can be moved to contain 0).
WANT=d46e9b167a93492eb02cabc1d2d9f81c975ea68698cb55944a4afac2463034ba
got=$(python3 -c "import hashlib; print(hashlib.sha256(open('object/R_3_3_14.txt', 'rb').read()).hexdigest())")
echo "sha256 $got"
out=$(python3 verify-it-yourself/verify_circ.py object/R_3_3_14.txt 3 3 14 2>&1)
rc=$?
printf '%s\n' "$out"
if [ "$got" = "$WANT" ] && [ $rc -eq 0 ] && printf '%s\n' "$out" | grep -qxF "proves R(3,3,14) >= 267"; then
  echo PASS
else
  echo FAIL
  exit 1
fi
