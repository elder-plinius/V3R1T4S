# Run it yourself (fresh shell, from this folder)

## 1. Quick checks (about 10 seconds)
    sh verify-it-yourself/run_checks.sh          # last line: PASS

## 2. Recompute a(10) with both programs (needs gcc and nauty's geng on PATH; about 3 minutes each on 8 cores)
    gcc -O2 -o lifeA how-we-built-it/lifeA.c && gcc -O2 -o lifeB how-we-built-it/lifeB.c
    for k in 1 2 3 4 5 6 7 8 9; do geng -q $k | ./lifeA | head -1; done        # maxperiod 1 1 1 1 2 4 8 14 27
    for r in 0 1 2 3 4 5 6 7; do geng -q 10 $r/8 | ./lifeA > A10_$r.txt & done; wait
    grep -h '^n=' A10_*.txt                                                     # graph counts sum to 12005168, max 46
    mkdir -p out; for k in 1 2 3 4 5 6 7 8 9; do geng -cq $k | ./lifeB > out/B_order$k.txt; done
    for r in 0 1 2 3 4 5 6 7; do (geng -cq 10 $r/8 | ./lifeB > out/B_order10_part$r.txt; echo "exit $?" >> out/B_order10_part$r.txt) & done; wait
    python3 how-we-built-it/merge_parts.py && python3 how-we-built-it/combine.py out 10   # n=10 a(n)=46

Expected: the saved outputs in object/evidence/ (A_n10_part*.txt, B_order10_part*.txt; witness graphs chosen as
"first seen" may differ with a different residue split, the counts and maxima may not).

## 3. The witness alone
    python3 how-we-built-it/stepper.py 'I?zUvYujw' 62                          # preperiod=0 cycle_length=46
