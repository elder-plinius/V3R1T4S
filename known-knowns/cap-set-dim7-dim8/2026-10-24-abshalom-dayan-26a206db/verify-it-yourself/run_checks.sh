#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Checks the object's sha256, then runs capcheck.py (Python standard library only): two exact routes
# (every pair x != y: -(x+y) mod 3 not in S; every line through two members), plus distinctness, range and dimension.
WANT=26a206db2dafae4a7f2c6f7478738acf5550af13998da2d4d0dff610ba83f82e
got=$(python3 -c "import hashlib; print(hashlib.sha256(open('object/cap_1104_n9.txt', 'rb').read()).hexdigest())")
echo "sha256 $got"
out=$(python3 verify-it-yourself/capcheck.py object/cap_1104_n9.txt 9 2>&1)
rc=$?
printf '%s\n' "$out"
if [ "$got" = "$WANT" ] && [ $rc -eq 0 ] && printf '%s\n' "$out" | grep -q "^VERDICT: CAP size 1104 n 9$"; then
  echo PASS
else
  echo FAIL
  exit 1
fi
