#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
# Needs python3 (standard library only) and a C compiler (cc). About 2 CPU-minutes, run as 3 parallel parts.
V=verify-it-yourself; O=object/eaqecc_28_5_15_11.json; W="$V/tmp_work"; rm -rf "$W"; mkdir -p "$W"
fail() { echo "$1"; rm -rf "$W"; echo FAIL; exit 1; }
cc -O3 -o "$W/enum_min" "$V/enum_min.c" || fail "could not compile enum_min.c"
python3 "$V/check_eaqecc.py" prepare "$O" "$W/basis.txt" > "$W/results.txt" || fail "prepare failed (object malformed?)"
cat "$W/results.txt"
for p in 0 1 2; do "$W/enum_min" $p 3 < "$W/basis.txt" > "$W/part$p.out" & done; wait
for p in 0 1 2; do cat "$W/part$p.out"; done
cat "$W/part0.out" "$W/part1.out" "$W/part2.out" >> "$W/results.txt"
python3 "$V/check_eaqecc.py" verdict "$O" "$W/results.txt" || fail "parameters do not match the claim"
rm -rf "$W"; echo PASS
