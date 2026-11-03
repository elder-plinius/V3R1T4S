#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh      (well under a minute; last line PASS or FAIL)
# Optional: SMALL=7 extends step 4 to n = 7 (a few minutes, pure Python).
# Optional full recomputation of A357952(9) with both programs (needs nauty's geng, a C compiler and Go;
# about 16 minutes on 8 cores):  FULL=1 sh verify-it-yourself/run_checks.sh   (GENG=/path/to/geng if not on PATH)
V=verify-it-yourself
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3chk)
trap 'rm -rf "$T"' EXIT
fail=0
echo "== 1. object/VALUE.txt: hash vs INDEX.csv and every pinned file"
python3 $V/check_pins.py || fail=1
echo "== 2. saved outputs: graph counts (A001349), published a(1..8), A and B agree graph by graph on a(9) = 200"
python3 $V/check_self.py outputs object/evidence || fail=1
echo "== 3. witness simulation from the definition (pure Python, node counts itself)"
python3 $V/check_self.py witness 'H?o|]|~' 1,3,5 1 200 || fail=1
python3 $V/check_self.py witness 'H?o|]|~' 1,3,5,9 1 200 || fail=1
python3 $V/check_self.py graph 'H?o|]|~' 200 || fail=1
echo "== 4. definition-level exhaustive check, n = 1..${SMALL:-6}, from all labelled graphs (no nauty)"
python3 $V/check_self.py small ${SMALL:-6} || fail=1
echo "== 5. saved optimal graphs n = 1..8, the OEIS examples n = 7, 8 and the n = 9 witness: pure Python, C and Go"
CC=${CC:-cc}
if $CC -O2 -o "$T/totA" object/code/totA_pg.c 2>/dev/null; then havec=1; else havec=0; echo "skip C part: no C compiler"; fi
if command -v go >/dev/null 2>&1 && go build -o "$T/totB" object/code/totB.go 2>/dev/null; then havego=1; else havego=0; echo "skip Go part: no Go toolchain"; fi
for gp in '@ 2' 'A_ 2' 'BW 4' 'CU 6' 'DCw 8' 'EEjo 18' 'FCrfw 42' 'G?bevw 112' 'F@Unw 42' 'G?Dlvw 112' 'H?o|]|~ 200'; do
  g=${gp% *}; p=${gp##* }
  python3 $V/check_self.py graph "$g" "$p" >/dev/null || { echo "$g python MISMATCH"; fail=1; }
  a=-; b=-
  [ $havec = 1 ] && a=$(printf '%s\n' "$g" | "$T/totA" self | sed -n 's/.*maxperiod=\([0-9]*\).*/\1/p')
  [ $havego = 1 ] && b=$(printf '%s\n' "$g" | WORKERS=1 "$T/totB" | sed -n 's/^summary.*max_cycle=\([0-9]*\).*/\1/p')
  if { [ $havec = 0 ] || [ "$a" = "$p" ]; } && { [ $havego = 0 ] || [ "$b" = "$p" ]; }; then
    echo "$g python=$p totA=$a totB=$b expected=$p ok"
  else echo "$g totA=$a totB=$b expected=$p MISMATCH"; fail=1; fi
done
G=${GENG:-geng}
if [ "${FULL:-0}" = 1 ]; then
  if [ $havec = 1 ] && [ $havego = 1 ] && command -v "$G" >/dev/null 2>&1; then
    echo "== 6. FULL: Programs A and B over all connected graphs with 1..9 nodes"
    for k in 1 2 3 4 5 6 7 8; do "$G" -cq $k | "$T/totA" self | head -1; done > "$T/A_n1_8.txt"
    for k in 1 2 3 4 5 6 7 8; do "$G" -cq $k | WORKERS=1 "$T/totB" | grep summary; done > "$T/B_n1_8.txt"
    cmp -s "$T/A_n1_8.txt" object/evidence/A_n1_8.txt && cmp -s "$T/B_n1_8.txt" object/evidence/B_n1_8.txt \
      && echo "n = 1..8: fresh A and B outputs identical to saved" || { echo "n = 1..8: fresh output differs from saved"; fail=1; }
    for r in 0 1 2 3 4 5 6 7; do "$G" -cq 9 $r/8 | PERGRAPH=1 "$T/totA" self > "$T/A9_part$r.txt" & done; wait
    for r in 0 1 2 3 4 5 6 7; do "$G" -cq 9 $r/8 | WORKERS=1 "$T/totB" > "$T/B9_part$r.txt" & done; wait
    for r in 0 1 2 3 4 5 6 7; do
      cmp -s "$T/A9_part$r.txt" object/evidence/A9_part$r.txt && cmp -s "$T/B9_part$r.txt" object/evidence/B9_part$r.txt \
        && echo "part $r: fresh A and B outputs identical to saved" || { echo "part $r: fresh output differs from saved"; fail=1; }
    done
  else echo "FULL requested but geng, a C compiler or Go is missing"; fail=1; fi
fi
echo "summary: A357952(9) = 200 (witness H?o|]|~, rule {1,3,5}, start 1, node counted in its own sum)"
if [ $fail -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
