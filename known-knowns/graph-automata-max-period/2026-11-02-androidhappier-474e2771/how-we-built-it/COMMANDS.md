# Exact commands used to build the result (from this folder, Linux x86-64, gcc -O2, nauty 2.8.8 geng)

    gcc -O2 -o totA totA.c && gcc -O2 -o totB totB.c
    for k in 1 2 3 4 5 6 7 8; do geng -cq $k | ./totA | head -1; done > A_n1_8.txt     # maxperiod 1 2 2 6 7 18 38 96
    for k in 1 2 3 4 5 6 7 8; do geng -cq $k | ./totB | head -1; done > B_n1_8.txt     # max_cycle 1 2 2 6 7 18 38 96
    sh run_A_n9.sh                                  # out/A_n9_part0..7.txt, about 2 minutes on 8 cores
    sh run_B_n9.sh                                  # out/B_n9_part0..7.txt, about 4 minutes on 8 cores
    python3 merge_parts.py out                      # out/A_n9_merged.txt, out/B_n9_merged.txt
    python3 tstepper.py 'H?`DBbS' 0,2 175           # witness_simulation.txt: preperiod=0 cycle_length=180

The run itself launched the two n = 9 jobs from its own scripts with the same commands (plus `nice` and a
2-hour `timeout`). The merge step was done inline in the run and not saved as a script; merge_parts.py was written
while packaging and reproduces both saved merged files in object/evidence/ byte for byte from the saved parts.
Every part file ends with the line `exit 0` written by the wrapper.
