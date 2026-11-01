# Local Gilbreath depths for every block of the primes from 1.5e15 to 1.6e15 (bank partial win p2)

## What

For the contiguous range of 2,859,087,706,237 primes from 1500000000000013 (first prime >= 1.5e15) up to the prime 1600001870813867 (> 1.6e15), cut into 349,009,729 blocks owning 8192 row-1 gap entries with overlap 1536, the recorded run (aggregates internally consistent, 95/95 primecount anchors, 28 of 28 blocks re-derived by an independent numpy/primesieve recomputation) has local depth D(c) between 85 and 783 (maximum 783 at block 344572324, first prime 1598729274569041), all below 1536, with row 1280 clean in every block and hence all later rows clean on the range shrunk by one entry per row; it says nothing about d_k(1) from p_1 = 2, G(pi(X)), or the full success criterion.

Plainly: Gilbreath's conjecture asks that every row of the triangle of iterated absolute differences of the primes starts with 1. Odlyzko (1993) and Colonna with Delahaye (2025-26) verify it in blocks of consecutive primes that overlap by more than the depth G at which a row contains only 0 and 2. This package covers the extension step toward Colonna's next bound for the range that follows his published 1.5e15: it cuts the 2,859,087,706,237 primes from 1500000000000013 into 349,009,729 blocks that own 8,192 prime-gap entries and read 1,536 more (the overlap), and records for every block the first row whose owned entries are all in {0,2} (local depth; minimum 85, median 189, maximum 783) and whether row 1,280 is all in {0,2} (yes in every block). Because row 1,280 is clean on the whole range, closure of {0,2} under absolute difference gives clean rows after it on the range shrunk by one entry per row. The range starts at 1.5e15, so nothing is said about the leading entries d_k(1).

**Disclosed change of the pre-registration (prominent).** `how-we-built-it/PREREG.md` contained a false closure sentence ("every row >= D(c) is in {0,2} on the owned entries"; it only holds on a shrinking segment, because the last owned entry reads one entry of the next block). A formalist lens found this by exhaustive small cases. `how-we-built-it/PREREG.v2.md` corrects the wording and adds the fixed-row check (row 1,280 over every block); the first GPU run (about 2.4 percent of the range) was aborted and the whole range recomputed with the check, thresholds fixed before any window of the restarted run was computed. The depth D(c) itself is unchanged.

## Check it yourself

Needs only Python 3.9+ (standard library), a POSIX shell (Git Bash works):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (about 3 to 8 minutes; pure-Python sieve). It checks the sha256 of every file in `object/`, the internal consistency of the recorded run (46,567 windows, cumulative counts, block count, histogram, maximum depth, 95 recorded primecount comparisons), and recomputes the local depth of 15 sample blocks (including the maximum block) from their first primes with an independent pure-Python sieve. The full per-block data (`depth.u16`, 698,019,458 bytes, and `clean1280.u8`, 349,009,729 bytes) are not in this package (size); their sha256 are in `object/RESULT.json`. Recomputing them takes the GPU program in `object/code` (`RUN_IT_YOURSELF.md`). Any block can be checked by hand: `object/block_firstprimes_*.csv` give the first prime and depth of every 4096th block.

## Compared to

| target | cell | table value | status page | fetched (UTC) | this package |
|---|---|---|---|---|---|
| gilbreath-conjecture-verification-beyond-1-5e15 | p2: local depths for every block of a contiguous range of primes from 1.5e15 to at least 1.6e15, overlaps larger than the depths, maximum depth reported, at least three sampled blocks recomputed independently | Colonna's page lists "Verification up to 1.5x10^15" (2026-03-18), G(pi(10^15)) = 800, G(pi(1.2125x10^15)) = 811 and a relative record 969 at 1.6931x10^15; it publishes no block data | https://www.lactamme.polytechnique.fr/Mosaic/descripteurs/GilbreathConjecture.01.Ang.html (HTTP 200, sha256 5641cdd6fc098132d1a51efc0f9889d22882ecd11d1b537325906dc9f8fdae2f) | 2026-11-01T04:45:13Z (the novelty skeptic re-read it the same day, same sha256) | all 349,009,729 blocks, maximum depth 783 at block 344,572,324 (first prime 1598729274569041), 0 flagged, 0 unclean at row 1,280 |

Block-wise depths are smaller than Colonna's G values because G is a maximum over much larger spans and blocks here have 8,192 owned entries; they are not comparable one to one. Snapshot data is under `the-record-we-beat/`.

## Not claimed

- Not a verification of Gilbreath's conjecture beyond 1.5e15: that needs the whole range from p_1 = 2 (success criterion of the bank target; Colonna's and Plouffe's block data are unpublished); nothing about d_k(1), no bound X, no G(pi(X)) and no comparison with Colonna's G values.
- Not independently recomputed for every block: the 349,009,729 depths come from the author's GPU program; the panel's skeptics recomputed 14, 15 and 28 blocks with their own programs (all agree), and a lens another 20, the run compared 748 blocks with numpy during the run and 95 window boundaries with primecount (all agree).
- No null test (deterministic exhaustive computation; stated in the pre-registration).
- The first-clean depth is a local statement (it is not monotone at the block's right edge); the row-1,280 check is what supports statements about later rows.
- The author's pipeline runs on an NVIDIA GPU; the quick check does not re-run it.

## Credits

- Andrew Odlyzko, "Iterated absolute values of differences of consecutive primes", Math. Comp. 61 (1993) 373-380 (https://www-users.cse.umn.edu/~odlyzko/doc/arch/gilbreath.conj.pdf); Norman Gilbreath (1958) and Francois Proth (1878), the conjecture.
- Jean-Francois Colonna and Jean-Paul Delahaye: the overlapping-block method and the verification to 1.5e15 (https://www.lactamme.polytechnique.fr/Mosaic/descripteurs/GilbreathConjecture.01.Ang.html); Simon Plouffe, arXiv:2510.06688 (independent verification to 1e14).
- Kim Walisch, primesieve and primecount (https://github.com/kimwalisch/primesieve, https://github.com/kimwalisch/primecount, releases v12.16 and v8.8 used for prime counts and cross-checks).
- CuPy and NVIDIA NVRTC for the GPU kernels; NumPy.
- The panel skeptics (`panel/`) and the lens agents wrote their own checks.
