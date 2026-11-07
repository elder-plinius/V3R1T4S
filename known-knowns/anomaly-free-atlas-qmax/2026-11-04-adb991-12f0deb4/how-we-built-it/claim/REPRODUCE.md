# REPRODUCE (fresh shell, inside a copy of this claim/ folder; needs gcc with OpenMP, python3, bash)

```
gcc -O2 -fopenmp -o csenum2 source/csenum2.c
gcc -O2 -o acclist source/acclist.c
gcc -O2 -o checklist checker/checklist.c
gcc -O3 -o mitm source/mitm.c
gcc -O2 -o count source/count.c
set -o pipefail   # a lister crash must not look like an empty PASS

# Listers on certified rows first (seconds): expect these hashes
./csenum2 12 1 2 2 | sha256sum   # c92c6342e2f70126cb61a620f36e589f9b430e3002e1a180af77a088fcd7df84 (SMnuR 12)
./acclist 20 0 | sha256sum       # f8e2ce35236a5792c3795608aaafcd3f2d4a68f7dfd3bdb0c65bc6efad23e770 (SM 20)

# Rows, streamed (never stored): sha256 and checker on the same bytes
./csenum2 20 1 80 3 | tee >(sha256sum > nu20.sha256) | ./checklist 20 1     # ~2 h on 3 threads, peak ~4.7 GB (NPASS 40 exceeds a 7.4 GB cap)
for q in 36 37 38; do ./acclist $q 0 2>/dev/null | tee >(sha256sum > sm$q.sha256) | ./checklist $q 0; done   # ~9-14 min each
cat nu20.sha256 sm3?.sha256   # expect object/counts.txt; "valid solutions" = count - 1 and PASS
# (checklist.c does not compare with an expected count: compare it yourself)

# Counters (no list), published convention:
./mitm SMnuR 20 | grep RESULT                 # ~4 min
for q in 36 37 38; do ./mitm SM $q | grep RESULT; done
# count.c (optional third code; needs ~10 GB per bound at Q >= 37): raw count per bound, then
# (cd source && python3 conventions.py ../N.txt 0), column prim_incl0
```
