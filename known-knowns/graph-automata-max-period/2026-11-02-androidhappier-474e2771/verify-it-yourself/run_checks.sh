#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh      (a few seconds; last line PASS or FAIL)
# Optional full recomputation of A357953(9) with both programs (needs nauty's geng, ~2 + 4 min on 8 cores):
#   FULL=1 sh verify-it-yourself/run_checks.sh        (GENG=/path/to/geng if geng is not on PATH)
V=verify-it-yourself
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3chk)
trap 'rm -rf "$T"' EXIT
fail=0
echo "== 1. object/VALUE.txt: hash vs INDEX.csv and every pinned file"
python3 $V/check_pins.py || fail=1
echo "== 2. saved outputs: graph counts (A001349), published a(1..8), A and B agree on a(9) = 180"
python3 $V/check_tot.py outputs object/evidence || fail=1
echo "== 3. witness simulation from the definition (pure Python)"
python3 $V/check_tot.py witness 'H?`DBbS' 0,2 175 180 || fail=1
python3 $V/check_tot.py samecycle 'H?`DBbS' 0,2 175 2 || fail=1
python3 $V/check_tot.py graph 'H?`DBbS' 180 || fail=1
echo "== 4. definition-level exhaustive check, n = 1..6, from all labelled graphs (no nauty)"
python3 $V/check_tot.py small 6 || fail=1
echo "== 5. the saved optimal graphs for n = 1..8 and the n = 9 witness, pure Python and both C programs"
CC=${CC:-cc}
if $CC -O2 -o "$T/totA" $V/totA.c 2>/dev/null && $CC -O2 -o "$T/totB" $V/totB.c 2>/dev/null; then havec=1; else havec=0; echo "skip C part: no C compiler"; fi
for gp in '@ 1' 'A_ 2' 'BW 2' 'CU 6' 'D]w 7' 'ECrw 18' 'FQzuo 38' 'GCz^nw 96' 'H?`DBbS 180'; do
  g=${gp% *}; p=${gp##* }
  python3 $V/check_tot.py graph "$g" "$p" >/dev/null || { echo "$g python MISMATCH"; fail=1; }
  if [ $havec = 1 ]; then
    a=$(printf '%s\n' "$g" | "$T/totA" | sed -n 's/.*maxperiod=\([0-9]*\).*/\1/p')
    b=$(printf '%s\n' "$g" | "$T/totB" | sed -n 's/.*max_cycle=\([0-9]*\).*/\1/p')
    if [ "$a" = "$p" ] && [ "$b" = "$p" ]; then echo "$g python=$p totA=$a totB=$b expected=$p ok"; else echo "$g totA=$a totB=$b expected=$p MISMATCH"; fail=1; fi
  else echo "$g python=$p expected=$p ok"; fi
done
G=${GENG:-geng}
if [ "${FULL:-0}" = 1 ]; then
  if [ $havec = 1 ] && command -v "$G" >/dev/null 2>&1; then
    echo "== 6. FULL: Programs A and B over all connected graphs with 9 nodes"
    for r in 0 1 2 3 4 5 6 7; do ( "$G" -cq 9 $r/8 | "$T/totA" > "$T/A_n9_part$r.txt"; echo "exit $?" >> "$T/A_n9_part$r.txt" ) & done; wait
    for r in 0 1 2 3 4 5 6 7; do ( "$G" -cq 9 $r/8 | "$T/totB" > "$T/B_n9_part$r.txt"; echo "exit $?" >> "$T/B_n9_part$r.txt" ) & done; wait
    for r in 0 1 2 3 4 5 6 7; do
      cmp -s "$T/A_n9_part$r.txt" object/evidence/A_n9_part$r.txt && cmp -s "$T/B_n9_part$r.txt" object/evidence/B_n9_part$r.txt \
        && echo "part $r: fresh A and B outputs identical to saved" || { echo "part $r: fresh output differs from saved"; fail=1; }
    done
  else echo "FULL requested but geng or a C compiler is missing"; fail=1; fi
fi
echo "summary: A357953(9) = 180 (witness H?\`DBbS, rule {0,2}, start 175)"
if [ $fail -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
