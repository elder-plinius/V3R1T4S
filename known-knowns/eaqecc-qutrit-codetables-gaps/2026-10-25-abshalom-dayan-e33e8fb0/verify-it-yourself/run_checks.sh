#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
# Needs python3 (standard library only) and a C compiler (cc). Seconds on one core: the three parts of the GF(3)
# subset test one after another, then a check with no distance search (punct_check.py: the Goppa-type bound of the
# extended one-point code E_13 minus the 3 deleted coordinates).
V=verify-it-yourself; O=object/eaqecc_25_5_12_8.json; W=$(mktemp -d) || { echo "could not make a temporary folder"; echo FAIL; exit 1; }
fail() { echo "$1"; rm -rf "$W"; echo FAIL; exit 1; }
cc -O3 -o "$W/subset_ea64" "$V/subset_ea64.c" || fail "could not compile subset_ea64.c"
python3 "$V/gf3prep.py" "$O" "$W/basis.txt" > "$W/results.txt" || fail "gf3prep failed (object malformed?)"
python3 "$V/check_eaqecc.py" prepare "$O" "$W/enum_basis.txt" >> "$W/results.txt" || fail "GF(9) check failed (object malformed?)"
D=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['d'] - 1)" "$O") || fail "no claimed d"
for p in 0 1 2; do "$W/subset_ea64" $D $p 3 < "$W/basis.txt" >> "$W/results.txt" || fail "subset test failed"; done
python3 "$V/witness.py" "$O" 1,8,11,14,15,16,17,18,19,21,23,24 >> "$W/results.txt" || fail "witness check failed"
WORD=0,1,0,0,0,0,0,0,5,0,0,7,0,0,8,1,4,8,6,1,0,5,0,1,3
python3 "$V/punct_check.py" "$O" 13 0,1,2 6,7,8,12,13,14,15,16,17,18,19,20,24 "$WORD" > "$W/punct.txt" 2>&1 || fail "no-search check failed to run (object malformed?)"
cat "$W/punct.txt" >> "$W/results.txt"
cat "$W/results.txt"
DD=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['d'])" "$O")
grep -q "^RESULT: d_EA = $DD exactly (no distance search): True$" "$W/punct.txt" || fail "no-search check (punctured one-point code + Goppa-type bound) does not give d = $DD"
python3 "$V/verdict.py" "$O" "$W/results.txt" || fail "parameters do not match the claim"
rm -rf "$W"; echo PASS
