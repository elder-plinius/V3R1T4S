# REPRODUCE (fresh shell, inside a copy of this claim/ folder; needs gcc with OpenMP, python3, bash)

```
gcc -O2 -o acclist source/acclist.c
gcc -O2 -fopenmp -o csenum source/csenum.c
gcc -O2 -o checklist checker/checklist.c
gcc -O2 -o count source/count.c

# One row = one list, streamed: line count, sha256 and checker on the same bytes (no file is stored).
# acclist: ./acclist QMAX NU ; csenum: ./csenum QMAX NU NPASS NTHR (NPASS splits memory: 2 at Q12, 4 at Q13,
# 10 at Q14, 16 at Q15, 26 at Q16; NTHR <= 2).  Expect "valid solutions: <lines>" and PASS, and the sha256 in
# object/counts.txt.
./acclist 12 0 | tee >(sha256sum) | ./checklist 12 0                 # SM rows: seconds each, Q_max 12..31
./acclist 13 1 | tee >(sha256sum) | ./checklist 13 1                 # SMnuR 13: about 4 min + checker, ~5 GB RAM
./csenum 13 1 4 2 | tee >(sha256sum) | ./checklist 13 1              # same bytes from the second lister
./csenum 16 1 26 1 | tee >(sha256sum) | ./checklist 16 1             # SMnuR 16: about 10-20 min
# The Python checker (checker/check_list.py QMAX NU FILE) applies the same rules; checklist.c was shown to agree
# with it on every list it was run on.

# Independent counts (no list): raw count, then the published convention (column prim_incl0)
for q in $(seq 1 16); do ./count $q 1; done > N_nu.txt; (cd source && python3 conventions.py ../N_nu.txt 1)
for q in $(seq 1 31); do ./count $q 0; done > N_sm.txt; (cd source && python3 conventions.py ../N_sm.txt 0)
# Calibration: the same convention gives the published values in status.md (SM Q_max 1,3,5,7,10; SMnuR 6..10).
```
