#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh      (well under a minute; last line PASS or FAIL)
# Optional: SMALL=7 extends step 4 to n = 7 (pure Python, slower).
# Optional full recomputation of A357951(8) with both programs (needs nauty's geng, a C compiler and Go;
# a few minutes on 8 cores):  FULL=1 sh verify-it-yourself/run_checks.sh   (GENG=/path/to/geng if not on PATH)
V=verify-it-yourself
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3chk)
trap 'rm -rf "$T"' EXIT
fail=0
echo "== 1. object/VALUE.txt: hash vs INDEX.csv and every pinned file"
python3 $V/check_pins.py || fail=1
echo "== 2. saved outputs: graph counts (A001349), published a(1..7), A and B agree graph by graph on a(8) = 150"
python3 $V/check_ot.py outputs object/evidence || fail=1
echo "== 3. witness simulation from the definition (pure Python, outer-totalistic: own state + number of ON neighbours)"
python3 $V/check_ot.py witness 'GCQfBg' 0,2 1,3,4 1 150 || fail=1
python3 $V/check_ot.py graph 'GCQfBg' 150 all || fail=1
python3 $V/check_ot.py graph 'G?rfUw' 124 || fail=1
python3 $V/check_ot.py witness 'FBjng' 0,1,3 2,4,5 1 66 || fail=1
echo "== 4. definition-level exhaustive check, n = 1..${SMALL:-6}, from all labelled graphs (no nauty)"
python3 $V/check_ot.py small ${SMALL:-6} || fail=1
echo "== 5. saved optimal graphs n = 1..7, the OEIS n = 7 example, the n = 8 witness and runner-up: pure Python, C and Go"
CC=${CC:-cc}
if $CC -O2 -o "$T/otA" object/code/otA.c 2>/dev/null; then havec=1; else havec=0; echo "skip C part: no C compiler"; fi
if command -v go >/dev/null 2>&1 && go build -o "$T/otB" object/code/otB.go 2>/dev/null; then havego=1; else havego=0; echo "skip Go part: no Go toolchain"; fi
for gp in '@ 2' 'A_ 2' 'BW 4' 'CU 6' 'DUw 16' 'EQzW 26' 'FEjvW 66' 'FBjng 66' 'G?rfUw 124' 'GCQfBg 150'; do
  g=${gp% *}; p=${gp##* }
  python3 $V/check_ot.py graph "$g" "$p" >/dev/null || { echo "$g python MISMATCH"; fail=1; }
  a=-; b=-
  [ $havec = 1 ] && a=$(printf '%s\n' "$g" | "$T/otA" | sed -n 's/^n=.*maxperiod=\([0-9]*\).*/\1/p')
  [ $havego = 1 ] && b=$(printf '%s\n' "$g" | "$T/otB" | sed -n 's/^n=.*maxperiod=\([0-9]*\).*/\1/p')
  if { [ $havec = 0 ] || [ "$a" = "$p" ]; } && { [ $havego = 0 ] || [ "$b" = "$p" ]; }; then
    echo "$g python=$p otA=$a otB=$b expected=$p ok"
  else echo "$g otA=$a otB=$b expected=$p MISMATCH"; fail=1; fi
done
G=${GENG:-geng}
if [ "${FULL:-0}" = 1 ]; then
  if [ $havec = 1 ] && [ $havego = 1 ] && command -v "$G" >/dev/null 2>&1; then
    echo "== 6. FULL: Programs A and B over all connected graphs with 1..8 nodes"
    for k in 1 2 3 4 5 6 7; do "$G" -cq $k | "$T/otA" | head -1; done > "$T/A_n1_7.txt"
    for k in 1 2 3 4 5 6 7; do "$G" -cq $k | "$T/otB" | head -1; done > "$T/B_n1_7.txt"
    cmp -s "$T/A_n1_7.txt" object/evidence/A_n1_7.txt && cmp -s "$T/B_n1_7.txt" object/evidence/B_n1_7.txt \
      && echo "n = 1..7: fresh A and B outputs identical to saved" || { echo "n = 1..7: fresh output differs from saved"; fail=1; }
    for r in 0 1 2 3 4 5 6 7; do "$G" -cq 8 $r/8 | "$T/otA" pg > "$T/A8_part$r.txt" & done; wait
    for r in 0 1 2 3 4 5 6 7; do "$G" -cq 8 $r/8 | "$T/otB" -pg > "$T/B8_part$r.txt" & done; wait
    for r in 0 1 2 3 4 5 6 7; do
      cmp -s "$T/A8_part$r.txt" object/evidence/A8_part$r.txt && cmp -s "$T/B8_part$r.txt" object/evidence/B8_part$r.txt \
        && echo "part $r: fresh A and B outputs identical to saved" || { echo "part $r: fresh output differs from saved"; fail=1; }
    done
  else echo "FULL requested but geng, a C compiler or Go is missing"; fail=1; fi
fi
echo "summary: A357951(8) = 150 (witness GCQfBg, rule B={0,2} S={1,3,4}, start 1, outer-totalistic)"
if [ $fail -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
