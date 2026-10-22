# Run it yourself
From this folder in a fresh shell:
    sh verify-it-yourself/run_checks.sh
Expected output:
    VALID size=44 table=34 BEATS
    PASS
Rebuild the search program and run it (about 10 minutes, time-limited; may return a different code):
    gcc -O3 -fopenmp -o blockcyc how-we-built-it/blockcyc.c
    ./blockcyc 10 5 7 999999 out.txt 400000 600
Here 10 = length, 5 = block length m (the group Z_5 rotates both blocks of 5 coordinates at once), 7 = distance, then
a stop weight, the output file, an orbit cap and the branch-and-bound time limit in seconds.
