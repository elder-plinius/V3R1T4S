#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Decides whether the windmill K_8^(2) has a harmonious labeling, from scratch, and checks object/DECISION.txt.
# Needs python3 (standard library). A C compiler (cc or gcc) is optional: with it, program P1 runs too.
# Last output line: PASS or FAIL.
ok=1
W=$(mktemp -d 2>/dev/null || mktemp -d -t windmill)
trap 'rm -rf "$W"' EXIT
V=verify-it-yourself

echo "== 1. object/DECISION.txt: header and pinned sha256 of the evidence files and of these checkers"
python3 $V/check_decision.py pins || ok=0

echo "== 2. P2 (mitm.py, Python, enumerate all sum-distinct sets then join complementary sum masks), n = 3..8"
for n in 3 4 5 6 7 8; do
  python3 $V/mitm.py $n > "$W/P2_$n.txt" || ok=0
  grep -v '^SOLUTION' "$W/P2_$n.txt"
done

echo "== 3. P1 (wsearch.c, C, nested backtracking clique A then clique B), n = 3..8"
CC=$(command -v cc || command -v gcc || true)
if [ -n "$CC" ] && "$CC" -O2 -o "$W/wsearch" $V/wsearch.c 2>"$W/cc.err"; then
  for n in 3 4 5 6 7 8; do
    "$W/wsearch" $n > "$W/P1_$n.txt" || ok=0
    grep -v '^SOLUTION' "$W/P1_$n.txt"
  done
else
  echo "no working C compiler (or it does not support unsigned __int128): P1 skipped; P2 and steps 4-6 still decide"
fi

echo "== 4. unreduced brute force over all injective labelings of K_4^(2) (validates the translation reduction)"
python3 $V/brute_n4.py | tee "$W/brute_4.txt" || ok=0

echo "== 5. every fresh number against the expect lines of object/DECISION.txt"
python3 $V/check_decision.py compare "$W" || ok=0

echo "== 6. n = 4 positive control: the 48 ordered pairs, enumerated independently here; label checker controls"
python3 $V/check_decision.py n4list || ok=0
if python3 $V/check_label.py 4 "0 1 2 8" "5 7 11"; then echo "known K_4^(2) labeling: VALID as expected"; else ok=0; fi
if python3 $V/check_label.py 4 "0 1 2 8" "5 7 10"; then echo "repeated-sum control: unexpected VALID"; ok=0; else echo "repeated-sum control: INVALID as expected"; fi
if python3 $V/check_label.py 4 "0 1 2 8" "5 7 8"; then echo "repeated-label control: unexpected VALID"; ok=0; else echo "repeated-label control: INVALID as expected"; fi

if [ $ok -eq 1 ]; then echo "summary: K_8^(2) has no harmonious labeling mod 56 (0 labelings; 449472 sum-distinct 8-sets containing 0)"; echo PASS; exit 0; else echo FAIL; exit 1; fi
