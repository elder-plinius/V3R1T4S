# How the object was built

Files here:
- `PREREG.md`: the run's pre-registration (criterion, rule and null-test decision, frozen 2026-11-08T09:20:10Z before
  any listing or counting program of run 2026-11-08-0917). No null test: the claim is an exact count of explicit
  objects, each checked against the definition (no search statistic).
- `source/`: the claim's programs, unchanged: `acclist.c` (SM lister, single-threaded meet in the middle, output in
  canonical order) and `mitm.c` (no-list counter: meet in the middle on (Q, L, nu) | (u, d, e), Moebius over common
  factors, Burnside over the sign; prints the count in the published convention).
- `claim/`: the claim as the panel saw it (`CLAIM.md`, `REPRODUCE.md`, `status.md`). The claim's `checker/` holds
  `check_list.py` and `checklist.c`, which are `verify-it-yourself/check_list.py` and `verify-it-yourself/checklist.c`
  here (same bytes). The claim's `source/atlas/` (text extractions of the paper and the erratum, the fetched arXiv
  pages) is third-party material and is not copied; `the-record-we-beat/` gives its hashes and the quoted lines.

The object `object/counts.txt` and `object/receipts/` are the claim's files, unchanged. Commands used in the run
(bash, `set -o pipefail`; scripts of the run's lenses, gcc -O3):

```sh
gcc -O3 -march=native -o acclist source/acclist.c -lm
gcc -O3 -o checklist checker/checklist.c -lm
gcc -O3 -march=native -o mitm source/mitm.c -lm
set -o pipefail
# SM 39 and 40, in parallel on two cores (walls 872 s and 1072 s, with mitm on a third core)
for q in 39 40; do   # one process per q
  ./acclist $q 0 2> SM$q.lister.log | tee >(sha256sum > SM$q.sha256) | ./checklist $q 0 > SM$q.checker.txt 2>&1
done
# counter without lists, regression rows first (all equal the confirmed values)
for a in "SMnuR 12" "SM 20" "SMnuR 20" "SM 36" "SM 37" "SM 38" "SM 39" "SM 40"; do ./mitm $a | grep RESULT; done > mitm.txt
# Python checker on the first 200000 lines of a fresh stream of each row
for q in 39 40; do ./acclist $q 0 2>/dev/null | head -n 200000 > s$q.txt; python3 checker/check_list.py $q 0 s$q.txt; done
```

`checklist.c` prints the number of valid lines but does not compare it with an expected count;
`verify-it-yourself/run_checks.sh` does that comparison and checks the lister's exit status.
