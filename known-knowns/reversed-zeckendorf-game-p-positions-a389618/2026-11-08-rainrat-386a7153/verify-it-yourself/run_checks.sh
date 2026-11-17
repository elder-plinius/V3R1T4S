#!/bin/sh
set -eu

OBJ="object/reversed_zeckendorf_n2_250.tsv"
TMP_BIN1="verify-it-yourself/.tmp_solver1_$$"
TMP_OUT1="verify-it-yourself/.tmp_out1_$$.tsv"
TMP_BIN2="verify-it-yourself/.tmp_solver2_$$"
TMP_OUT2="verify-it-yourself/.tmp_out2_$$.tsv"
TMP_MUT="verify-it-yourself/.tmp_mut_$$.tsv"
trap 'rm -f "$TMP_BIN1" "$TMP_OUT1" "$TMP_BIN2" "$TMP_OUT2" "$TMP_MUT"' EXIT

if ! python3 verify-it-yourself/check_table.py "$OBJ"; then
    echo "FAIL"
    exit 1
fi

# Frontier mutation check on the standalone Python verifier (flip winner at n=130 from 1 to 2)
awk -F'\t' 'BEGIN{OFS="\t"} $1==130{$2=($2==1?2:1)} {print}' "$OBJ" > "$TMP_MUT"
if python3 verify-it-yourself/check_table.py "$TMP_MUT" >/dev/null 2>&1; then
    echo "Error: check_table.py accepted a mutated frontier winner at n=130"
    echo "FAIL"
    exit 1
fi

# Recompute full table n=2..250 from scratch with Solver 1 (universal_delta_solver.cpp)
if ! g++ -O3 -std=c++17 how-we-built-it/universal_delta_solver.cpp -o "$TMP_BIN1"; then
    echo "FAIL"
    exit 1
fi
if ! "$TMP_BIN1" "$TMP_OUT1" >/dev/null 2>&1; then
    echo "FAIL"
    exit 1
fi
if ! diff -u "$OBJ" "$TMP_OUT1" >/dev/null 2>&1; then
    echo "Mismatch between $OBJ and Solver 1 (universal_delta_solver) output"
    echo "FAIL"
    exit 1
fi

# Recompute full table n=2..250 from scratch with Solver 2 (colex_rank_solver.cpp)
if ! g++ -O3 -fopenmp -std=c++17 how-we-built-it/colex_rank_solver.cpp -o "$TMP_BIN2"; then
    echo "FAIL"
    exit 1
fi
if ! "$TMP_BIN2" "$TMP_OUT2" >/dev/null 2>&1; then
    echo "FAIL"
    exit 1
fi
if ! diff -u "$OBJ" "$TMP_OUT2" >/dev/null 2>&1; then
    echo "Mismatch between $OBJ and Solver 2 (colex_rank_solver) output"
    echo "FAIL"
    exit 1
fi

echo "Verified byte-identical match against fresh recomputation by both independent C++ solvers (universal_delta_solver and colex_rank_solver) across n=2..250."
echo "PASS"
