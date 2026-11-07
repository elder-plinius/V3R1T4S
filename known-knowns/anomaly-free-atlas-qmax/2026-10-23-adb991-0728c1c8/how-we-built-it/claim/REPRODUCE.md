# REPRODUCE (fresh shell, inside a copy of this claim/ folder; needs gcc with OpenMP, python3, bash)

```
gcc -O2 -fopenmp -o csenum2 source/csenum2.c
gcc -O2 -o checklist checker/checklist.c
gcc -O2 -o count source/count.c

# The list, streamed (never stored): line count, sha256 and checker on the same bytes.
# csenum2 QMAX NU NPASS NTHR: NPASS bounds memory (about 26 GB / NPASS of sort buffers at Q_max 17; 16 passes ~
# 1.7 GB), NTHR threads (output is identical for any NPASS and NTHR). About 1-2 h on 1 thread, less on 3.
set -o pipefail   # a lister crash must not look like an empty PASS
./csenum2 17 1 16 3 | tee >(sha256sum > list17.sha256) | ./checklist 17 1   # about 25 min on 3 threads
./csenum2 18 1 25 3 | tee >(sha256sum > list18.sha256) | ./checklist 18 1   # about 45 min on 3 threads
cat list17.sha256 list18.sha256   # expect the sha256 values in object/counts.txt
# expect "valid solutions: 1643386479" / "2720672221" and PASS (checklist.c does not compare with an expected
# count: compare it yourself)

# Check the lister on known rows first (seconds to minutes): these hashes are certified in earlier rows
./csenum2 12 1 2 2 | sha256sum   # c92c6342e2f70126cb61a620f36e589f9b430e3002e1a180af77a088fcd7df84 (SMnuR 12)
./csenum2 20 0 3 2 | sha256sum   # f8e2ce35236a5792c3795608aaafcd3f2d4a68f7dfd3bdb0c65bc6efad23e770 (SM 20)

# Independent count (no list): raw count, then the published convention (column prim_incl0); calibration values
# (status.md) come out of the same table.
for q in $(seq 1 18); do ./count $q 1; done > N_nu.txt     # Q_max 17, 18 take about 25 and 40 min on one core
(cd source && python3 conventions.py ../N_nu.txt 1)       # expect prim_incl0 = 1643386480 (17), 2720672222 (18)
```
