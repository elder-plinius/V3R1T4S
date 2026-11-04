# Exact commands the run used (run folder claim/, which is this package's object/ plus the geng binary in tools/)

Linux x86-64 with BMI2 (pext), gcc, python3; nauty 2.8.8 geng (sha256 75d1bf016a93b090ca471254605b735865162a864e4682c544df90a81e91f450, not shipped).

    gcc -O3 -march=native -o lifeA11 code/lifeA11.c && gcc -O3 -march=native -o lifeB2 code/lifeB2.c
    for k in 1 2 3 4 5 6 7 8 9; do tools/geng -q $k | ./lifeA11 | grep '^n='; done   # result/A_n1_9.txt
    for k in 1 2 3 4 5 6 7 8 9 10; do tools/geng -cq $k | ./lifeB2 > result/B_order$k.txt; done
    tools/geng -q 10 | ./lifeA11 > result/A10_r0of1.txt
    seq 0 63 | xargs -P 8 -I{} sh -c 'tools/geng -q 11 {}/64 | ./lifeA11 > result/A11_r{}of64.txt'
    seq 0 63 | xargs -P 8 -I{} sh -c 'tools/geng -cq 11 {}/64 | ./lifeB2 > result/B11_parts/B_order11_r{}of64.txt'
    python3 code/merge_orders.py result/B11_parts 11 > result/B_order11.txt
    python3 code/combine.py result 11 > result/combine_n1_11.txt
    python3 code/compare_AB.py result result/B_order11.txt result/combine_n1_11.txt > result/compare_AB.txt
    python3 code/stepper.py 'J?qrdjivb}_' 752; python3 code/stepper.py 'JCpbdo}ttv_' 1728   # result/witness_simulation.txt

No third-party Python packages are used. PREREG.md is the run's pre-registration, frozen before any n = 11 program ran.
