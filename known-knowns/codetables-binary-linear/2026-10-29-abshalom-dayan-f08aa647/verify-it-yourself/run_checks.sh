#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
# Needs python3 (standard library only) and a C compiler (cc). About 17 seconds on one core.
V=verify-it-yourself; O=object/code_q9_n31_k17_d11.json
# All scratch files go to a temporary folder outside the package, removed on exit; nothing is written inside the package.
W=$(mktemp -d 2>/dev/null || mktemp -d -t v3r1t4s) || { echo "could not create a temporary folder"; echo FAIL; exit 1; }
trap 'rm -rf "$W"' EXIT
fail() { echo "$1"; echo FAIL; exit 1; }
cc -O2 -o "$W/m3_mindist" "$V/m3_mindist.c" || fail "could not compile m3_mindist.c"
python3 -I "$V/check_code.py" prepare "$O" "$W/code.txt" || fail "object malformed or rank deficient"
"$W/m3_mindist" < "$W/code.txt" > "$W/m3.out" || fail "m3_mindist failed"
cat "$W/m3.out"
python3 -I "$V/check_code.py" verdict "$O" "$W/m3.out" || fail "parameters do not match the claim"
echo PASS
