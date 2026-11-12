# REPRODUCE (fresh shell, inside a copy of this claim/ folder; needs gcc, python3, bash)

```
gcc -O2 -o acclist source/acclist.c
gcc -O2 -o checklist checker/checklist.c
gcc -O3 -o mitm source/mitm.c
set -o pipefail   # a lister crash must not look like an empty PASS

# Lister on a certified row first (seconds): expect this hash
./acclist 20 0 2>/dev/null | sha256sum   # f8e2ce35236a5792c3795608aaafcd3f2d4a68f7dfd3bdb0c65bc6efad23e770 (SM 20)

# Rows, streamed (never stored): sha256 and checker on the same bytes
for q in 41 42; do ./acclist $q 0 2>/dev/null | tee >(sha256sum > sm$q.sha256) | ./checklist $q 0; done   # ~20 and ~24 min
cat sm41.sha256 sm42.sha256   # expect object/counts.txt; "valid solutions" = count - 1 and PASS
# (checklist.c does not compare with an expected count: compare it yourself)

# Independent counter (no list), published convention; first reproduce the published values:
for q in 1 2 3 4 5 6 7 8 9 10; do ./mitm SM $q | grep RESULT; done   # expect 8 22 82 251 626 1983 3902 7068 14354 23800
for q in 41 42; do ./mitm SM $q | grep RESULT; done                  # ~1.5 min each

# Python checker on a sample:
./acclist 41 0 2>/dev/null | head -n 200000 > s41.txt; python3 checker/check_list.py 41 0 s41.txt
```
