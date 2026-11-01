# evaluator lens (main session)
Hypotheses (guess chance / cost):
1. GPU sieve + shared-memory abs-diff rows beats CPU primesieve rate by >5x for the whole pipeline (60% / 1.5 h). RESULT: sieve 0.19 s per 2.1e9-number window vs primesieve counting 0.25 s per 2.1e9 on 10 threads (so GPU = ~1.3x the 10-thread CPU count rate, and it also emits primes and runs the rows). Dead-condition 5x not met on sieving, but the whole pipeline (emit + rows) is within budget (2.5 h) while CPU only (sieve alone 3.2 h + rows) was not.
2. Byte rows with __vabsdiffu4 after a 16-bit phase while any value > 255 (80% / done, verified against numpy on 29 blocks).
3. Wheel-30 flags halve the big-prime stores (30% / 1 h) - not done.
4. Bucket sieve for big primes (25% / 3 h) - not done.
5. Pre-sieved pattern for 3,5,7,11,13 in the shared tile (done, -30% small kernel).
6. Larger small/big threshold (tested 2^19, 2^20: no gain).
7. (imported: stencil temporal blocking from GPU PDE codes) all rows of a block done in shared memory: done, rows cost 10 ms per 6e7 primes.
8. (too strange) skip sieving: Miller-Rabin test of candidates on GPU: not tried (cost far above sieve).

## Outcome (after the run)
Dead/changed lines: first run v1 aborted at window 1130 after the formalist lens showed first-clean depth is not a bound (closure only on a shrinking segment); restarted with the fixed-row K*=1280 check (PREREG.v2.md). Wheel-30 flags and a bucket sieve were not needed. The GPU was shared with the human's own GPU work for about 2.5 h of the 5.1 h.
