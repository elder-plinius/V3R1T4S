# How the object was built

Files here:
- `PREREG.md`: the run's pre-registration (criterion, rule and null-test decision, frozen 2026-11-03 before any attack output of
  run 2026-11-03-0919). No null test: the claim is an exact count of explicit objects, each checked
  against the definition (no search statistic).
- `source/`: the claim's programs, unchanged: `acclist.c` (SM lister, single-threaded meet in the middle, output in
  canonical order), `csenum2.c` (SMnuR lister: hash join per block, memory passes on the first two canonical
  charges, OpenMP threads), `mitm.c` (no-list counter: meet in the middle on (Q, L, nu) | (u, d, e), Moebius over
  common factors, Burnside over the sign; prints the count in the published convention), `count.c` with `fix.py` and
  `conventions.py` (raw counter on the (Q, u, d) | (L, e, nu) split, then Burnside and Moebius; column `prim_incl0`).
- `claim/`: the claim as the panel saw it (`CLAIM.md`, `REPRODUCE.md`, `status.md`). The claim's `checker/` holds
  `check_list.py` and `checklist.c`, which are `verify-it-yourself/check_list.py` and `verify-it-yourself/checklist.c`
  here (same bytes). The claim's `source/atlas/` (text extractions of the paper and the erratum, the fetched arXiv
  page) is third-party material and is not copied; `the-record-we-beat/` gives its hashes and the quoted lines.
  `REPRODUCE.md` gives the SMnuR 20 run's memory as about 4.7 GB at NPASS 80 (the receipts: peak 4.66 GB).

The object `object/counts.txt` and `object/receipts/` are the claim's files, unchanged. Commands used in the run
(bash, `set -o pipefail`; scripts of the run's lenses):

```sh
gcc -O2 -fopenmp -o csenum2 source/csenum2.c
gcc -O2 -o acclist source/acclist.c
gcc -O2 -o checklist checker/checklist.c
gcc -O3 -o mitm source/mitm.c
gcc -O2 -o count source/count.c
set -o pipefail
./csenum2 12 1 2 2 | sha256sum   # c92c6342...df84 (certified SMnuR 12), test before the attack
./acclist 20 0 | sha256sum       # f8e2ce35...e770 (certified SM 20)
# SM 36..38 (walls 540, 660, 843 s; run beside the SMnuR stream)
for q in 36 37 38; do
  ./acclist $q 0 2> SM$q.enum.log | tee >(sha256sum > SM$q.sha256) | ./checklist $q 0 > SM$q.checker.txt 2>&1
done
# SMnuR 20 (7112 s, 80 passes, 3 threads, peak resident memory 4.66 GB, logged every 30 s)
./csenum2 20 1 80 3 2> SMnuR20.enum.log | tee >(sha256sum > SMnuR20.sha256) | ./checklist 20 1 > SMnuR20.checker.txt 2>&1
# counter without lists (regression rows first)
for a in "SMnuR 12" "SM 20" "SM 36" "SM 37" "SM 38" "SMnuR 20"; do ./mitm $a | grep RESULT; done > mitm.txt
# count.c at SM q = 37, 38 was killed by the session's memory limit (about 10 GB); not used
```

`csenum2 QMAX NU NPASS NTHR`: NPASS bounds the memory; keep it well below 2e8 (an earlier run found a crash with
empty output there). `checklist.c` prints the number of valid lines but does not compare it with an expected count;
`verify-it-yourself/run_checks.sh` does that comparison and checks the lister's exit status.
