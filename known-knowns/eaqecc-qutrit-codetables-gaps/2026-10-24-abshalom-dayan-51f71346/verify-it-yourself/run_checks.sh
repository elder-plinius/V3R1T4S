#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
# Needs python3 (standard library only) and a C compiler (cc). About 10 seconds (4 parallel parts of the subset test).
V=verify-it-yourself; O=object/eaqecc_28_6_12_6.json; W="$V/tmp_work"; rm -rf "$W"; mkdir -p "$W"
fail() { echo "$1"; rm -rf "$W"; echo FAIL; exit 1; }
cc -O3 -o "$W/subset_ea" "$V/subset_ea.c" || fail "could not compile subset_ea.c"
python3 "$V/gf3prep.py" "$O" "$W/basis.txt" > "$W/results.txt" || fail "gf3prep failed (object malformed?)"
python3 "$V/check_eaqecc.py" prepare "$O" "$W/enum_basis.txt" >> "$W/results.txt" || fail "GF(9) check failed (object malformed?)"
D=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['d'] - 1)" "$O") || fail "no claimed d"
for p in 0 1 2 3; do "$W/subset_ea" $D $p 4 < "$W/basis.txt" > "$W/part$p.out" & done; wait
cat "$W/part0.out" "$W/part1.out" "$W/part2.out" "$W/part3.out" >> "$W/results.txt"
python3 "$V/witness.py" "$O" 15,16,17,18,19,20,21,22,23,24,25,26 >> "$W/results.txt" || fail "witness check failed"
cat "$W/results.txt"
python3 "$V/verdict.py" "$O" "$W/results.txt" || fail "parameters do not match the claim"
rm -rf "$W"; echo PASS
