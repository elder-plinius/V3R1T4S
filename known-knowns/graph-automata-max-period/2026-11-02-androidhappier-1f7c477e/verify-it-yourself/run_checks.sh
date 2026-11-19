#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh      (about 10 seconds; last line PASS or FAIL)
# Optional full recomputation of a(10) (needs nauty's geng on PATH, ~3 min per program on 8 cores): FULL=1 sh verify-it-yourself/run_checks.sh
V=verify-it-yourself
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3chk)
trap 'rm -rf "$T"' EXIT
fail=0
echo "== 1. object/VALUE.txt: hash vs INDEX.csv and every pinned file"
python3 $V/check_pins.py || fail=1
echo "== 2. saved outputs: graph counts (A000088, A001349), published a(1..9), A and B agree on a(10) = 46"
python3 $V/check_life.py outputs object/evidence || fail=1
echo "== 3. witness simulation from the definition (pure Python)"
python3 $V/check_life.py witness 'I?zUvYujw' 62 46 || fail=1
python3 $V/check_life.py witness 'IEhffT{^w' 842 46 || fail=1
echo "== 4. definition-level exhaustive check over all labelled graphs, n = 1..6 (no nauty)"
python3 $V/check_life.py small 6 || fail=1
echo "== 5. both C programs on the published optimal graphs and the witness (no nauty needed)"
CC=${CC:-cc}
if $CC -O2 -o "$T/lifeA" $V/lifeA.c 2>/dev/null && $CC -O2 -o "$T/lifeB" $V/lifeB.c 2>/dev/null; then
  for gp in 'D]{ 2' 'E]yw 4' 'FE~vw 8' 'GEnvZ{ 14' 'HCZJtzm 27' 'I?zUvYujw 46' 'IEhffT{^w 46'; do
    g=${gp% *}; p=${gp##* }
    a=$(printf '%s\n' "$g" | "$T/lifeA" | sed -n 's/.*maxperiod=\([0-9]*\).*/\1/p')
    b=$(printf '%s\n' "$g" | "$T/lifeB" | sed -n 's/.*max_cycle=\([0-9]*\).*/\1/p')
    if [ "$a" = "$p" ] && [ "$b" = "$p" ]; then echo "$g lifeA=$a lifeB=$b expected=$p ok"; else echo "$g lifeA=$a lifeB=$b expected=$p MISMATCH"; fail=1; fi
  done
else
  echo "skip: no C compiler; steps 1-4 still decide the package checks"
fi
if [ "${FULL:-0}" = 1 ] && command -v geng >/dev/null 2>&1; then
  echo "== 6. FULL: Program A over all graphs on 10 vertices"
  for r in 0 1 2 3 4 5 6 7; do geng -q 10 $r/8 | "$T/lifeA" > "$T/A$r.txt" & done; wait
  python3 - "$T" <<'PY' || fail=1
import sys,glob,re
tot=0;mx=0
for f in glob.glob(sys.argv[1]+"/A[0-7].txt"):
    l=open(f).readline(); tot+=int(re.search(r"graphs=(\d+)",l).group(1)); mx=max(mx,int(re.search(r"maxperiod=(\d+)",l).group(1)))
print("graphs",tot,"max",mx); sys.exit(0 if (tot,mx)==(12005168,46) else 1)
PY
fi
echo "summary: A384209(10) = 46 (witness I?zUvYujw from state 62)"
if [ $fail -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
