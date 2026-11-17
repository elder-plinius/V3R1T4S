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
./csenum2 19 1 40 3 | tee >(sha256sum > nu19.sha256) | ./checklist 19 1     # ~80 min on 3 threads, < 3 GB
for q in 32 33 34 35; do ./acclist $q 0 2>/dev/null | tee >(sha256sum > sm$q.sha256) | ./checklist $q 0; done
cat nu19.sha256 sm3?.sha256   # expect object/counts.txt; "valid solutions" = count - 1 and PASS
# (checklist.c does not compare with an expected count: compare it yourself)

# Counters (no list), published convention:
./mitm SMnuR 19 | grep RESULT                 # a few minutes
for q in 32 33 34 35; do ./mitm SM $q | grep RESULT; done
# count.c: raw count per bound, then (cd source && python3 conventions.py ../N.txt 0), column prim_incl0
```
