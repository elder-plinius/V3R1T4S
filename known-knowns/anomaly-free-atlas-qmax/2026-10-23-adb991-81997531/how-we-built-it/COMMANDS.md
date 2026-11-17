# How the object was built

Files here:
- `PREREG.md`: the run's pre-registration (criterion, rule and null-test decision, frozen 2026-10-18 08:18:58 UTC
  before any attack output of the run). No null test: the claim is an exact count of explicit objects, each checked
  against the definition (no search statistic).
- `source/`: the claim's programs, unchanged: `acclist.c` (first lister: meet in the middle, output already sorted),
  `csenum.c` (second lister, written independently: hash join per block, memory passes, OpenMP threads),
  `count.c` and `count2.c` (raw counters with two different splits), `fix.py` and `conventions.py` (Burnside for the
  overall sign, Moebius for common factors; the published convention is `prim_incl0`).
- `claim/`: the claim as the panel saw it (`CLAIM.md`, `REPRODUCE.md`, `status.md`). `status.md` is the run's status
  record of 2026-10-18 (PENDING TABLE CHECK at the time); the table was read later from the owner-supplied PDFs
  (`the-record-we-beat/`). The claim's `checker/` holds `check_list.py` and `checklist.c`, which are
  `verify-it-yourself/check_list.py` and `verify-it-yourself/checklist.c` here (same bytes).

The object `object/counts.txt` is the claim's file, unchanged. Commands used in the run (from the claim folder,
`claim/REPRODUCE.md`; the lens folders ran the same programs). The run's shell was bash: `>(...)` is bash process
substitution.

```sh
gcc -O2 -o acclist source/acclist.c
gcc -O2 -fopenmp -o csenum source/csenum.c
gcc -O2 -o checklist checker/checklist.c
gcc -O2 -o count source/count.c
./acclist 12 0 | tee >(sha256sum) | ./checklist 12 0        # SM rows, Q_max 12..31: seconds to 5 minutes each
./acclist 13 1 | tee >(sha256sum) | ./checklist 13 1        # SMnuR 13: about 4 min + checker, about 5 GB of memory
./csenum 13 1 4 2 | tee >(sha256sum) | ./checklist 13 1     # the same bytes from the second lister
./csenum 16 1 26 1 | tee >(sha256sum) | ./checklist 16 1    # SMnuR 16: about 10-20 min
for q in $(seq 1 16); do ./count $q 1; done > N_nu.txt; (cd source && python3 conventions.py ../N_nu.txt 1)
for q in $(seq 1 31); do ./count $q 0; done > N_sm.txt; (cd source && python3 conventions.py ../N_sm.txt 0)
```

`csenum QMAX NU NPASS NTHR`: NPASS splits the memory (2 at Q_max 12, 4 at 13, 10 at 14, 16 at 15, 26 at 16) and
does not change the output bytes; NTHR is the number of threads. `checklist.c` prints the number of valid lines but
does not compare it with an expected count; `verify-it-yourself/run_checks.sh` does that comparison.
