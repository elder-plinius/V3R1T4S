id: gilbreath-conjecture-verification-beyond-1-5e15
picked: Sun Nov  1 04:50:30 UTC 2026

# Why this target (charter quarries 4 and 5; both open, remaining quarries 1-3 have uploaded results)
Compared with kissing-number-low-dim (weight 3, same as Gilbreath):
- kissing p1 needs an exact configuration in a dimension >= 24 strictly above the live Cohn table value, and p2 needs a new exact
  SDP/LP upper bound strictly below the live table. Both are research-grade discoveries with no known method that is
  reachable by compute alone on this machine in a run; success is not a matter of running a program longer.
- Gilbreath p2 is a pure compute task with a deterministic, mechanically checkable output (local depths per block over
  a contiguous prime range 1.5e15 .. 1.6e15, overlaps larger than depths, three sampled blocks recomputed
  independently) that this machine can do: measured here, primesieve counts a 1e10 range at 1.5e15 in 1.167 s on 10 threads
  (8.6e9 numbers/s), so a CPU-only run of the 1e14 range would need 3.2 h of sieving alone; the RTX 3080 (cupy + NVRTC, installed in the
  workspace venv) can sieve and run the row recurrence on the GPU, which brings the range into this run's budget.
  The whole range from 2 to above 1.5e15 (the full success criterion) is about 16x larger and is not reachable in one run; p2 is the extension step.
- Honest limit: p2 is a partial win only. It is not the success criterion (a bound X above 1.5e15 from p_1 = 2).

# Success criterion (verbatim from bank)
Success means the claimant's own computation, starting from p_1 = 2, showing that the leading entry of difference row k is 1 for every k <= pi(X), for some X STRICTLY GREATER (direction: max) than the largest verified bound on Colonna's live page (1.5 x 10^15 on 2026-10-30), in the same convention: X is the bound on the primes, the rows covered are k <= pi(X), and G(pi(X)) is reported. Colonna's and Plouffe's block data are not published, so the whole range from 2 must be covered by the claimant's logs. The claim gives the code, the depth G used, the block and overlap scheme (each block's overlap must exceed its depth so that no row is cut) and pi(X) checked against an independent pi(x) value (primecount). The skeptic re-runs the algorithm with an independently written difference-table routine on at least three randomly chosen blocks, and runs the full computation from scratch if compute allows. Colonna's page and arXiv are re-checked immediately before claiming.

# Partial wins (verbatim from bank)
- p1: An independent reproduction of Colonna's G values at x = 10^14 (693) and x = 10^15 (800), or a documented discrepancy, with code.
- p2: Local Gilbreath depths for every block of a contiguous range of primes from 1.5 x 10^15 to at least 1.6 x 10^15 (block overlaps larger than the depths), with the maximum depth reported and at least three sampled blocks recomputed independently: the extension step toward the next bound.

# Chosen partial win: p2 (primary). p1 reproduction is a low-scale cross-check only; its x = 1e14 and x = 1e15 values are not claimed.
