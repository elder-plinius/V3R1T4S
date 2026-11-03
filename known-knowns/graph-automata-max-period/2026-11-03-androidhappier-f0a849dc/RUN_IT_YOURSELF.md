# Run it yourself (fresh shell, from this folder)

## 1. Quick checks (a few seconds)
    sh verify-it-yourself/run_checks.sh          # last line: PASS

## 2. Recompute a(11) with both programs
Needs gcc on x86-64 with BMI2 (pext), python3, and nauty 2.8.8's geng on PATH. Cost on 8 cores: Program A about
40 minutes; Program B about 3.5 hours (the run's figure on heavily shared cores). Peak memory about 2 MB per job.

    gcc -O3 -march=native -o lifeA11 how-we-built-it/lifeA11.c && gcc -O3 -march=native -o lifeB2 how-we-built-it/lifeB2.c
    for k in 1 2 3 4 5 6 7 8 9; do geng -q $k | ./lifeA11 | grep '^n='; done      # maxperiod 1 1 1 1 2 4 8 14 27
    mkdir -p out/A11 out/B11 out/B
    seq 0 63 | xargs -P 8 -I{} sh -c 'geng -q 11 {}/64 | ./lifeA11 > out/A11/A11_r{}of64.txt'
    for k in 1 2 3 4 5 6 7 8 9 10; do geng -cq $k | ./lifeB2 > out/B/B_order$k.txt; done
    seq 0 63 | xargs -P 8 -I{} sh -c 'geng -cq 11 {}/64 | ./lifeB2 > out/B11/B_order11_r{}of64.txt'
    python3 how-we-built-it/merge_orders.py out/B11 11 > out/B/B_order11.txt
    python3 how-we-built-it/combine.py out/B 11 > out/combine.txt                 # last line: n=11 a(n)=71
    python3 how-we-built-it/compare_AB.py out/A11 out/B/B_order11.txt out/combine.txt   # last line: VERDICT AGREE

Expected: the counts, histograms and maxima in object/evidence/ (A11_r*of64.txt, B11_parts/, B_order*.txt,
combine_n1_11.txt, compare_AB.txt). The saved outputs can be compared the same way:
`python3 how-we-built-it/compare_AB.py object/evidence object/evidence/B_order11.txt object/evidence/combine_n1_11.txt`.
Program A alone: `FULL=1 sh verify-it-yourself/run_checks.sh` (this mode was not run for the receipts in this
folder; the reproduce skeptic's own full n = 11 recompute is in panel/reproduce.md).

## 3. The witnesses alone
    python3 how-we-built-it/stepper.py 'J?qrdjivb}_' 752                        # preperiod=0 cycle_length=71
    python3 how-we-built-it/stepper.py 'JCpbdo}ttv_' 1728                       # preperiod=0 cycle_length=71
    python3 how-we-built-it/stepper.py 'HCZJtzm' 47                             # OEIS n = 9 example: cycle_length=27
