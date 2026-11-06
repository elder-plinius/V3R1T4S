#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
# Needs python3 (standard library only) and a C compiler (cc). About 5 seconds (3 parallel parts of the
# information-set test).
V=verify-it-yourself; O=object/eaqecc_33_8_16_15.json; W="$V/tmp_work"; rm -rf "$W"; mkdir -p "$W"
fail() { echo "$1"; rm -rf "$W"; echo FAIL; exit 1; }
cc -O3 -o "$W/infoset" "$V/infoset.c" || fail "could not compile infoset.c"
python3 "$V/gf3prep.py" "$O" "$W/basis.txt" > "$W/results.txt" || fail "gf3prep failed (object malformed?)"
python3 "$V/check_eaqecc.py" prepare "$O" "$W/enum_basis.txt" >> "$W/results.txt" || fail "GF(9) check failed (object malformed?)"
python3 "$V/gf9info.py" prep "$O" "$W/G9.txt" >> "$W/results.txt" || fail "GF(9) recovery failed (object malformed?)"
M=$(python3 -c "import json,sys; o=json.load(open(sys.argv[1])); print(o['n'] - o['d'] + 1)" "$O") || fail "no claimed d"
for p in 0 1 2; do "$W/infoset" $M $p 3 < "$W/G9.txt" > "$W/part$p.out" & done; wait
cat "$W/part0.out" "$W/part1.out" "$W/part2.out" >> "$W/results.txt"
python3 "$V/witness.py" "$O" 9,10,11,15,16,17,21,22,23,24,25,26,27,29,30,31 >> "$W/results.txt" || fail "witness check failed"
cat "$W/results.txt"
python3 "$V/verdict.py" "$O" "$W/results.txt" || fail "parameters do not match the claim"
rm -rf "$W"; echo PASS
