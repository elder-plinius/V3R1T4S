#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs python3 and a C compiler (gcc or clang); OpenMP is used when available. About 5 minutes on 4 cores.
OBJ=object/a002224_42.json
T=$(mktemp -d) || { echo FAIL; exit 1; }
trap 'rm -rf "$T"' EXIT
python3 verify-it-yourself/check.py object "$OBJ" || { echo FAIL; exit 1; }
CC=${CC:-cc}
$CC -O3 -fopenmp -o "$T/enum" verify-it-yourself/enum.c 2>/dev/null || $CC -O3 -o "$T/enum" verify-it-yourself/enum.c || { echo "compile error"; echo FAIL; exit 1; }
Q=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["value"])' "$OBJ") || { echo FAIL; exit 1; }
"$T/enum" "$Q" "$T/survivors.txt" 2>"$T/enum.log" || { cat "$T/enum.log"; echo FAIL; exit 1; }
grep -E "M=|periods|DONE" "$T/enum.log"
python3 verify-it-yourself/check.py minimality "$OBJ" "$T/survivors.txt" "$Q" || { echo FAIL; exit 1; }
echo PASS
