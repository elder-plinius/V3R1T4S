# How it was built

All programs here are the run's own and are byte-identical to the run's claim/code/. benzZQ.c, benzB64.c,
benzB128.c and indep_check.py are also in verify-it-yourself/, and their sha256 are pinned in object/VALUE.txt.

## Programs
- benzZQ.c (Program A, found and reproduced the term): region from the inequalities -(a-1) <= j-i, k-j, i-k <= b-1
  with k = 1-i-j. It is a row-sweep frontier DP along lines i = const. The state is a 64-bit covered mask of the next
  W cells. Counts are u64 with overflow-checked additions. Pruning (zone check) drops a state only if a complete MRV
  exact-cover search proves that the uncovered cells of the next K rows cannot be covered, and keeps the state when
  the node limit NL (default 4000) is hit. It is parallelized with OpenMP and has checkpoint/resume (BENZ_CKPT,
  BENZ_CKPT_SEC). Note: the header comment says "unsigned __int128 counts", but the counting code uses u64 with
  overflow checks. The comment is stale (panel/criterion.md).
- benzB64.c (Program B, the second, independent n = 20 run): region from the complex-plane hexagon vertices
  aw+b, -aw^2-b, aw^2+bw, -a-bw, a+bw^2, -aw-bw^2 (w = e^(2 pi i/3)). Tiles come from Euclidean distances. The sweep
  runs along lines k = const ascending, then i descending. It has its own hash table, its own feasibility search
  (budget exhausted means keep the state) and u64 overflow-flagged counts. Checkpointing uses BENZB_CKPT.
- benzB128.c: the same program as benzB64.c with unsigned 128-bit counts and a different hash load factor, used for
  B's published-term runs n = 3..18. PREREG.v2.md records the switch to benzB64.c for n = 20 (memory) before B
  produced any n = 20 output.
- indep_check.py: a definition-level counter (memoized exact cover on the full covered set, no transfer matrix),
  for small n only.
- repro_matrix.py: the run's comparison of all saved outputs with the OEIS DATA files (the run's claim/data/, not
  shipped because they are third-party pages). Its role here is taken by verify-it-yourself/check_value.py
  evidence, which compares against the published terms written in object/VALUE.txt.
- timed.sh: the wrapper that wrote each .out/.err/.time triple. Its peak_rss_kb samples the timeout wrapper process,
  not the counter, so the .time files do not measure memory.

## Commands the run used (compiler gcc, x86_64, 8 cores, 16 GB)

    gcc -O3 -march=native -fopenmp -o benzZQ   benzZQ.c
    gcc -O3 -march=native -fopenmp -o benzB64  benzB64.c
    gcc -O3 -march=native -fopenmp -o benzB128 benzB128.c
    # Program A, (20,37), checkpointed; stopped once by SIGTERM (exit 143) to change thread count, resumed at t=210:
    BENZ_M=5 OMP_NUM_THREADS=7 BENZ_CKPT=... BENZ_CKPT_SEC=... ./benzZQ 20 37 3
    #   -> 225354012176304818, exit 0, overflow=0, peak 49,914,147 states, 2222 s after the resume
    # Program B, (20,37), one uninterrupted run:
    OMP_NUM_THREADS=7 ./benzB64 20 37 3 5
    #   -> 225354012176304818, exit 0, overflow 0, max 50,055,349 states, 2385 s
    # Published terms (object/evidence/A_repro, B_repro), for each n, b = 2n-4 (A364416) and 2n-3 (A364417):
    BENZ_M=5 ./benzZQ n b 3
    ./benzB128 n b 3 5
    # Checkpoint test (object/evidence/A_ckpt_test): (16,28) stopped and resumed -> 6902094928308 = A364416(16)
    python3 indep_check.py 8 3     # object/evidence/out_indep_n3_8.txt
    python3 indep_check.py 11 9    # object/evidence/out_indep_n9_11.txt

Each run was wrapped as `sh timed.sh PREFIX command...`, which writes PREFIX.out (stdout), PREFIX.err (stderr) and
PREFIX.time (exit code, wall seconds). object/evidence/A_repro/repro_log.txt is the run's one-line-per-run summary.

## Other files
- REPRODUCE_run.md and claim_run.md: the run's claim/REPRODUCE.md and claim/claim.md. They are copied unchanged
  except that the temporary-folder prefix is written as $TMPDIR/ (the kit's leak scan rejects absolute temporary
  paths). Their paths code/... and result/... are the run's names. Here they are verify-it-yourself/ or
  how-we-built-it/ for code, and object/evidence/ for results. claim_run.md lists data/ files (OEIS pages, Propp's
  text) that are not shipped.
- PREREG.md (frozen 2026-11-02T04:01:02Z, after the A run had started but before it had produced a result) and
  PREREG.v2.md (2026-11-02T04:48:19Z, the switch from benzB128 to benzB64 for B's n = 20 run, made before B started),
  copied unchanged. null_test: not needed (an exact integer from deterministic counting programs checked against
  published terms).
- The exploratory programs of the run's other lenses (plain frontier DP, lookahead variants, invariant probes) are
  not shipped. None of them contributed to the value.
