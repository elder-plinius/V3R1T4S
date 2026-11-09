#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh      (well under a minute; last line PASS or FAIL)
# Optional: SMALL=7 extends step 4 to n = 7 (pure Python, slower).
# Optional recomputation with both programs (needs nauty 2.8.8's geng, a C compiler and Go):
#   FULL=1 sh verify-it-yourself/run_checks.sh     a(1..9) with A and B, plus geng residue class 7/32 (the witness class)
#                                                  with A and B; ~1 core-hour, mostly B
#   FULL=2 sh verify-it-yourself/run_checks.sh     all 32 classes with A (~2 core-hours) and B (~12+ core-hours)
#   (GENG=/path/to/geng if geng is not on PATH; JOBS=8 parallel jobs by default)
V=verify-it-yourself
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3chk)
trap 'rm -rf "$T"' EXIT
fail=0
echo "== 1. object/VALUE.txt: hash vs INDEX.csv and every pinned file"
python3 $V/check_pins.py || fail=1
echo "== 2. saved outputs: graph counts (A001349), published a(1..8), A and B agree class by class on a(10) = 624"
python3 $V/check_tot.py outputs object/evidence || fail=1
echo "== 3. witness simulation from the definition (pure Python, neighbours only, node itself not counted)"
python3 $V/check_tot.py witness 'I?AAD@oIg' 0,2 2 624 || fail=1
python3 $V/check_tot.py graph 'I?AAD@oIg' 624 all || fail=1
python3 $V/check_tot.py graph 'ICQfRh|z_' 470 all || fail=1
python3 $V/check_tot.py witness 'FJe~O' 0,2 1 38 || fail=1
echo "== 4. definition-level exhaustive check, n = 1..${SMALL:-6}, from all labelled graphs (no nauty)"
python3 $V/check_tot.py small ${SMALL:-6} || fail=1
echo "== 5. saved optimal graphs n = 1..9, the OEIS n = 7 example, the n = 10 witness and runner-up: pure Python, C and Go"
CC=${CC:-cc}
if $CC -O2 -o "$T/totF" object/code/A/totF.c 2>/dev/null; then havec=1; else havec=0; echo "skip C part: no C compiler"; fi
if command -v go >/dev/null 2>&1 && mkdir -p "$T/B" && cp object/code/B/main.go object/code/B/go.mod "$T/B/" \
   && (cd "$T/B" && go build -o "$T/totBgo" . ) 2>/dev/null; then havego=1; else havego=0; echo "skip Go part: no Go toolchain"; fi
for gp in '@ 1' 'A_ 2' 'BW 2' 'CU 6' 'D]w 7' 'ECrw 18' 'FQzuo 38' 'FJe~O 38' 'GCz^nw 96' 'H?`DBbS 180' 'I?AAD@oIg 624' 'ICQfRh|z_ 470'; do
  g=${gp% *}; p=${gp##* }
  python3 $V/check_tot.py graph "$g" "$p" >/dev/null || { echo "$g python MISMATCH"; fail=1; }
  a=-; b=-
  [ $havec = 1 ] && a=$(printf '%s\n' "$g" | "$T/totF" | sed -n 's/^n=.*maxperiod=\([0-9]*\).*/\1/p')
  [ $havego = 1 ] && b=$(printf '%s\n' "$g" | "$T/totBgo" nbr | sed -n 's/^n=.*maxperiod=\([0-9]*\).*/\1/p')
  if { [ $havec = 0 ] || [ "$a" = "$p" ]; } && { [ $havego = 0 ] || [ "$b" = "$p" ]; }; then
    echo "$g python=$p totF=$a totBgo=$b expected=$p ok"
  else echo "$g totF=$a totBgo=$b expected=$p MISMATCH"; fail=1; fi
done
G=${GENG:-geng}
J=${JOBS:-8}
if [ "${FULL:-0}" != 0 ]; then
  if [ $havec = 1 ] && [ $havego = 1 ] && command -v "$G" >/dev/null 2>&1; then
    echo "== 6. FULL=$FULL: Programs A and B from geng"
    for k in 1 2 3 4 5 6 7 8 9; do "$G" -cq $k | "$T/totF" | grep '^n='; done > "$T/A_n1_9.txt"
    for k in 1 2 3 4 5 6 7 8 9; do "$G" -cq $k | "$T/totBgo" nbr | grep '^n='; done > "$T/B_n1_9.txt"
    cmp -s "$T/A_n1_9.txt" object/evidence/A_n1_9.txt && cmp -s "$T/B_n1_9.txt" object/evidence/B_n1_9.txt \
      && echo "n = 1..9: fresh A and B outputs identical to saved" || { echo "n = 1..9: fresh output differs from saved"; fail=1; }
    if [ "$FULL" = 2 ]; then RS=$(seq 0 31); else RS=7; fi
    export G T
    for p in A B; do
      printf '%s\n' $RS | xargs -P "$J" -I{} sh -c 'if [ '"$p"' = A ]; then "$G" -cq 10 {}/32 | "$T/totF" 150; else "$G" -cq 10 {}/32 | "$T/totBgo" nbr 150; fi > "$T/'"$p"'10_r{}of32.txt"'
    done
    for r in $RS; do
      cmp -s "$T/A10_r${r}of32.txt" object/evidence/A10_r${r}of32.txt && cmp -s "$T/B10_r${r}of32.txt" object/evidence/B10_r${r}of32.txt \
        && echo "class $r/32: fresh A and B outputs identical to saved" || { echo "class $r/32: fresh output differs from saved"; fail=1; }
    done
  else echo "FULL requested but geng, a C compiler or Go is missing"; fail=1; fi
fi
echo "summary: A357953(10) = 624 (witness I?AAD@oIg, rule {0,2}, start 2, neighbours-only totalistic)"
if [ $fail -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
