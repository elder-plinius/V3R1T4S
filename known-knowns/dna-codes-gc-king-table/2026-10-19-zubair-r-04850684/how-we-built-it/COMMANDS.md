# Exact commands that produced object/gc_n10_d7_m44.txt (C, standard library + OpenMP; no other requirements)
    gcc -O3 -march=native -fopenmp -o blockcyc blockcyc.c
    OMP_NUM_THREADS=1 nice -n 10 timeout 1500 ./blockcyc 10 5 7 999999 code_n10_d7.txt 400000 600
Log of that run: generation_log.txt (time-limited branch and bound; ended at its 600 s limit with a 44-word clique).
The run's pre-registrations are PREREG.md and PREREG.v2.md (v2 was written after a first result and says so).
null_test: not needed (an explicit object checked by a deterministic checker against a table value).
