#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
# Needs python3 (standard library only) and a C compiler (cc). About 10 seconds (3 parallel parts of the subset test,
# then a 1-second check with no distance search: onepoint_check.py, the Goppa-type bound for the one-point code).
V=verify-it-yourself; O=object/eaqecc_28_7_13_9.json; W="$V/tmp_work"; rm -rf "$W"; mkdir -p "$W"
fail() { echo "$1"; rm -rf "$W"; echo FAIL; exit 1; }
cc -O3 -o "$W/subset_ea64" "$V/subset_ea64.c" || fail "could not compile subset_ea64.c"
python3 "$V/gf3prep.py" "$O" "$W/basis.txt" > "$W/results.txt" || fail "gf3prep failed (object malformed?)"
python3 "$V/check_eaqecc.py" prepare "$O" "$W/enum_basis.txt" >> "$W/results.txt" || fail "GF(9) check failed (object malformed?)"
D=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['d'] - 1)" "$O") || fail "no claimed d"
for p in 0 1 2; do "$W/subset_ea64" $D $p 3 < "$W/basis.txt" > "$W/part$p.out" & done; wait
cat "$W/part0.out" "$W/part1.out" "$W/part2.out" >> "$W/results.txt"
python3 "$V/witness.py" "$O" 12,13,14,18,19,20,21,22,23,24,25,26,27 >> "$W/results.txt" || fail "witness check failed"
WORD=0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,7,7,7,3,3,3,1,1,1,4
python3 "$V/onepoint_check.py" "$O" 15 "$WORD" > "$W/onepoint.txt" 2>&1 || fail "no-search check failed to run (object malformed?)"
cat "$W/onepoint.txt" >> "$W/results.txt"
cat "$W/results.txt"
DD=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['d'])" "$O")
grep -q "^RESULT: d_EA = $DD exactly (no distance search): True$" "$W/onepoint.txt" || fail "no-search check (one-point code + Goppa-type bound) does not give d = $DD"
python3 "$V/verdict.py" "$O" "$W/results.txt" || fail "parameters do not match the claim"
rm -rf "$W"; echo PASS
