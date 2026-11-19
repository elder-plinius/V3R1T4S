#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh      (about 15 seconds; last line PASS or FAIL)
# Optional full recomputation of a(11) with Program A (needs nauty's geng on PATH or GENG=..., x86-64 with BMI2;
# about 40 min on 8 cores):  FULL=1 sh verify-it-yourself/run_checks.sh
V=verify-it-yourself
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3chk)
trap 'rm -rf "$T"' EXIT
fail=0
echo "== 1. object/VALUE.txt: hash vs INDEX.csv and every pinned file"
python3 $V/check_pins.py || fail=1
echo "== 2. saved outputs: graph counts (A000088, A001349), a(1..9) published, A and B agree on a(11) = 71"
python3 $V/check_life.py outputs object/evidence || fail=1
echo "== 3. witness simulation from the definition (pure Python)"
python3 $V/check_life.py witness 'J?qrdjivb}_' 752 71 || fail=1
python3 $V/check_life.py witness 'JCpbdo}ttv_' 1728 71 || fail=1
python3 $V/check_life.py graph 'J?qrdjivb}_' 71 || fail=1
python3 $V/check_life.py graph 'JCpbdo}ttv_' 71 || fail=1
python3 $V/check_life.py graph 'JCpbbqkVt^_' 61 || fail=1
python3 $V/stepper.py 'J?qrdjivb}_' 752 | grep -q 'cycle_length=71' || { echo "stepper.py witness MISMATCH"; fail=1; }
echo "== 4. definition-level exhaustive check over all labelled graphs, n = 1..6 (no nauty)"
python3 $V/check_life.py small 6 || fail=1
echo "== 5. both C programs on the published optimal graphs and the witnesses (no nauty needed)"
CC=${CC:-cc}
if $CC -O2 -mbmi2 -o "$T/lifeA" $V/lifeA11.c 2>/dev/null && $CC -O2 -o "$T/lifeB" $V/lifeB2.c 2>/dev/null && printf 'D]{\n' | "$T/lifeA" >/dev/null 2>&1; then
  for gp in 'D]{ 2' 'E]yw 4' 'FE~vw 8' 'GEnvZ{ 14' 'HCZJtzm 27' 'I?zUvYujw 46' 'J?qrdjivb}_ 71' 'JCpbdo}ttv_ 71' 'JCpbbqkVt^_ 61'; do
    g=${gp% *}; p=${gp##* }
    a=$(printf '%s\n' "$g" | "$T/lifeA" | sed -n 's/^n=.*maxperiod=\([0-9]*\).*/\1/p')
    b=$(printf '%s\n' "$g" | "$T/lifeB" | sed -n 's/.*max_cycle=\([0-9]*\).*/\1/p')
    if [ "$a" = "$p" ] && [ "$b" = "$p" ]; then echo "$g lifeA=$a lifeB=$b expected=$p ok"; else echo "$g lifeA=$a lifeB=$b expected=$p MISMATCH"; fail=1; fi
  done
else
  echo "skip: no C compiler with BMI2 support; steps 1-4 still decide the package checks"
fi
GENG=${GENG:-geng}
if [ "${FULL:-0}" = 1 ] && command -v "$GENG" >/dev/null 2>&1 && [ -x "$T/lifeA" ]; then
  echo "== 6. FULL: Program A over all graphs on 11 vertices (64 residue classes, 8 at a time)"
  mkdir -p "$T/A11"
  seq 0 63 | xargs -P 8 -I{} sh -c "\"$GENG\" -q 11 {}/64 | \"$T/lifeA\" > \"$T/A11/A11_r{}of64.txt\""
  for f in object/evidence/A11_r*of64.txt; do cmp -s "$f" "$T/A11/$(basename "$f")" || { echo "differs: $(basename "$f")"; fail=1; }; done
  echo "FULL: fresh A11 outputs compared byte by byte with object/evidence"
fi
echo "summary: A384209(11) = 71 (witness J?qrdjivb}_ from state 752)"
if [ $fail -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
