# How the object was built

Files here:
- `PREREG.md`: the run's pre-registration (criterion, rule and null-test decision, frozen 2026-10-20 08:18:25 UTC
  before any attack output of the run). No null test: the claim is an exact count of explicit objects, each checked
  against the definition (no search statistic).
- `source/`: the claim's programs, unchanged: `csenum2.c` (the lister: hash join per block, memory passes on the
  first two canonical charges, OpenMP threads; output bytes do not depend on the number of passes or threads),
  `count.c` and `count2.c` (raw counters with two different splits), `fix.py` and `conventions.py` (Burnside for the
  overall sign, Moebius for common factors; the published convention is `prim_incl0`).
- `claim/`: the claim as the panel saw it (`CLAIM.md`, `REPRODUCE.md`, `status.md`). `status.md` is the run's status
  record (PENDING TABLE CHECK at the time); the table was read later from the owner-supplied PDFs
  (`the-record-we-beat/`). The claim's `checker/` holds `check_list.py` and `checklist.c`, which are
  `verify-it-yourself/check_list.py` and `verify-it-yourself/checklist.c` here (same bytes).

The object `object/counts.txt` is the claim's file, unchanged. Commands used in the run (bash, from the claim folder;
`claim/REPRODUCE.md`):

```sh
gcc -O2 -fopenmp -o csenum2 source/csenum2.c
gcc -O2 -o checklist checker/checklist.c
gcc -O2 -o count source/count.c
set -o pipefail   # a lister crash must not look like an empty PASS
./csenum2 17 1 16 3 | tee >(sha256sum > list17.sha256) | ./checklist 17 1   # 1301 s in the run
./csenum2 18 1 25 3 | tee >(sha256sum > list18.sha256) | ./checklist 18 1   # 2357 s in the run
cat list17.sha256 list18.sha256      # the sha256 values in object/counts.txt
./csenum2 12 1 2 2 | sha256sum       # c92c6342...df84, the certified SMnuR 12 list (lister self-test)
./csenum2 20 0 3 2 | sha256sum       # f8e2ce35...e770, the certified SM 20 list
for q in $(seq 1 18); do ./count $q 1; done > N_nu.txt
(cd source && python3 conventions.py ../N_nu.txt 1)   # prim_incl0 = 1643386480 (17), 2720672222 (18)
```

`csenum2 QMAX NU NPASS NTHR`: NPASS bounds the memory (about 26 GB / NPASS of sort buffers at Q_max 17); keep it
well below 2e8 (the contrarian lens found a crash with empty output there). `checklist.c` prints the number of valid
lines but does not compare it with an expected count; `verify-it-yourself/run_checks.sh` does that comparison and
checks the lister's exit status.
