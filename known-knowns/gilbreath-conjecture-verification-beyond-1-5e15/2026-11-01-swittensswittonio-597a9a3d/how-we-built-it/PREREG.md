# PREREG (frozen Sun Nov  1 04:56:36 UTC 2026)
target: gilbreath-conjecture-verification-beyond-1-5e15, partial win p2.
null_test: not needed because the claim is a deterministic exhaustive computation (every block of a contiguous prime range) checked by independent recomputation, not a search or a statistical claim.
baseline: not applicable (explicit computation; no published code or released predictions exist for local depths; Colonna's and Plouffe's block data are unpublished).

## Criterion (p2, verbatim from the bank)
Local Gilbreath depths for every block of a contiguous range of primes from 1.5 x 10^15 to at least 1.6 x 10^15 (block overlaps larger than the depths), with the maximum depth reported and at least three sampled blocks recomputed independently: the extension step toward the next bound.

## Definitions (frozen)
- Range: all primes q_0 < q_1 < ... that are >= A = 1.5e15, up to the last owned prime, which must exceed B = 1.6e15 (the run keeps sieving until the first prime of the unprocessed carry exceeds B).
- Gap sequence g_i = q_{i+1} - q_i = row 1 entry i. Row k entry i = |row_{k-1}(i) - row_{k-1}(i+1)| (row 0 = the primes themselves, as in Colonna's d_k).
- Block c (c = 0,1,2,...) OWNS gap entries i in [c*M, c*M+M) and READS gap entries [c*M, c*M+M+O): M = 8192 entries, overlap O = 1536 entries. Owned entries of consecutive blocks tile the range with no gaps or overlaps; owned entries of row k (k <= O) only depend on read entries.
- Local depth D(c) = the smallest k >= 1 such that every owned entry of row k lies in {0,2}. Because |a-b| of values in {0,2} stays in {0,2}, every row >= D(c) is then in {0,2} on the owned entries (Odlyzko's closure used by Colonna). The overlap condition is D(c) < O (strict) for every block; a block with no such k < O is flagged 0xFFFF and would void the run for that block.
- All gaps for primes >= 1.5e15 are even, so '1' never occurs; {0,2} means value & ~2 == 0.

## Integrity checks that must hold for the claim (thresholds frozen, results are not thresholded)
1. flagged blocks = 0 (all D(c) < O = 1536).
2. Prime counts: for window starts, cumulative count of sieved primes equals primecount pi(lo_w - 1) - pi(A - 1) for every 500th window plus the final window end; the final total equals primecount pi(last sieved odd number) - pi(A - 1).
3. In-run numpy re-computation of >= 4 blocks every 250 windows agrees with the GPU depth exactly.
4. At least 3 sampled blocks (chosen by the verifier, not by the run) are recomputed by an independent skeptic program using primes printed by primesieve.exe (v12.16), and the depth agrees.
5. The maximum depth over all blocks is reported with its block id and first prime; nothing else (no x-bound, no G(pi(X))) is claimed.
Disclosure: a 3-window smoke test of the pipeline ran before this file was written (windows 0-2, depths 141..489 in the first 22,504 blocks); no threshold above depends on it.
