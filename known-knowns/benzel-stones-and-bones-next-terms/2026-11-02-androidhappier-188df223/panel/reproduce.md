# Reproduce skeptic — runs/2026-11-02-0316

context: subagent (reproduce)

Scratch copy: $TMPDIR/claim-reproduce-0316 (byte-identical to claim/ per `diff -rq`; nothing written into claim/).

## Checks
1. **Independent B20 rerun (fresh):** rebuilt `claim/code/benzB64.c` (gcc -O3 -march=native -fopenmp), ran
   `OMP_NUM_THREADS=7 benzB64 20 37 3 5`. Status `exit=0 wall=3349`. stdout `225354012176304818`, which matches the claim.
   stderr ends `max states 50055349 overflow 0`. That is identical to the saved `claim/result/B_final/B_A364417_n20.err`
   (same max states, same value), so the run is deterministic.
2. **Saved final runs:** `claim/result/A_final/A364417_n20.out` = 225354012176304818, `.time` exit=0, `.err` ends overflow=0.
   The interruption is declared: `A364417_n20.seg1.time` exit=143 (SIGTERM), the run checkpointed at t=210 and resumed.
   `claim/result/B_final/B_A364417_n20.out` = 225354012176304818, exit=0, overflow 0. A and B agree.
3. **`claim/code/repro_matrix.py`** (run in the scratch copy): every published A364416(3..20) and A364417(3..19) is A:OK.
   B is OK through n=18; B was not run for A364417(19) and A364416(19,20), which matches the claim, since only A must reproduce all terms.
   Output: `published mismatches=0 A missing=0 n20 agree=True`, `RESULT PASS`. I read the script: it parses %S/%T/%U from
   `claim/data/A364416.txt` and `claim/data/A364417.txt` and requires value equality, exit=0 and the overflow-0 string.
4. **Own checker** (`skeptic/mycount.py`, written from Propp's definition, separate from claim code): for n=3..11 it gives
   A364416 = 1,10,84,724,6516,60900,586404,5777916,57952212 and
   A364417 = 3,18,142,1266,12030,118650,1198230,12296202,127633590. All match the OEIS DATA.
5. **Rebuild:** recompiling `claim/code/benzZQ.c`, `claim/code/benzB64.c` and `claim/code/benzB128.c` gives binaries byte-identical to the ones used.
   The sha256 of the sources equals the sha256 of claim/code.
6. **Pruning soundness:** in `claim/code/benzZQ.c`, a state is dropped only when the exact-cover search returns 0 (proven infeasible).
   A node-limit result (undecided) keeps the state. `claim/code/benzB64.c` works the same way: budget exhausted gives -1, which means keep.
   I checked this empirically for (n,b) = (10..13, 2n-4 / 2n-3). benzZQ with M=5 and with M=1, benzB128 (Z=3, every=5) and
   benzB64 (Z=2, every=3) all give identical values equal to OEIS, so the count does not depend on how much pruning runs.
7. **Checkpoint soundness:** `claim/result/A_ckpt_test/r2.out` = 6902094928308 = A364416(16). In `r2.err` the resumed run
   finished with overflow=0, and `r1.err` shows the checkpoints were written. The A_final resume is logged ("resumed t=210", exit 0).

## Verdict
No mismatches, no missing objects, no unjustified drops, no non-determinism. My B20 rerun agrees with the claimed value.

pass: true
