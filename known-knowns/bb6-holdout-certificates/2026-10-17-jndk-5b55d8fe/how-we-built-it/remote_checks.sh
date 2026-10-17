#!/bin/bash
# Runs every repair-lens check from a fresh copy of claim/ (current directory = that copy).
P=${PYTHON:-python3}   # a Python 3 with sympy; set PYTHON to override
$P -c "import sympy;print('sympy', sympy.__version__)"
asm() { cat code/prove.py; printf "RULES_JSON = r'''"; cat result/rules.json; printf "'''\n"; cat "$1"; }
echo "== parser"; asm code/parser_test.py | $P -u - 2>&1 | tail -12
echo "== proofs"; asm code/main_proofs.py | $P -u - 2>&1 | grep -E "RESULT|sha256|SUMMARY"
echo "== controls"; asm code/main_controls.py | $P -u - 2>&1 | tail -2
echo "== brute"; { printf "RULES_JSON = r'''"; cat result/rules.json; printf "'''\n"; cat code/bruteforce.py; } | $P -u - 2>&1 | tail -4
echo "== replay"; gcc -O2 -o replay_v2 code/replay_v2.c
./replay_v2 sim 1RB1LC_1RC1RB_1RD0LE_1LA1LD_---0LA 100000000
./replay_v2 rules 1000000000 0 | tail -9
./replay_v2 rules 1000000000 1 | tail -1
./replay_v2 rules 1000000000 2 | tail -1
