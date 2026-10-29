# PREREG, run 2026-10-28-0100 (written 2026-10-28T01:04:23Z, before any code of this run is built or measured)

## Criterion (verbatim, bank/targets.json)


Success means a k x n generator matrix over GF(q) with these properties. (1) Rank is exactly k over GF(q), computed independently. (2) The exact minimum distance d is computed by full enumeration of all q^k - 1 nonzero codewords when feasible (2^k <= ~2^32), or, for large k (or large k with small n-k, via the dual and MacWilliams identities), by two independent exact minimum-distance implementations that agree; never by sampling. (3) d is STRICTLY GREATER (direction: max) than the lower bound in the live http://www.codetables.de/ cell for (q,n,k) at verification time, and at most the upper bound. (4) The code is not one of the 7 LinCodeEvolve codes (arXiv:2609.37056) or a code derived from them, and no newer arXiv claim already reaches that d.

## Statistic and checkers

- Object: a 19 x 32 generator matrix over GF(9) (encoding a + 3b, w^2 = w + 1) built from the tailg solution.
- Rank: Gaussian elimination over GF(9) (rref9 in Python), must equal 19.
- Exact d: two independent exact programs that must agree: m3_mindist (primal column-subset test, all W-subsets) and
  hdep (dual side, smallest dependent set of parity-check columns, exhaustive up to Wmax). Plus a third check in the
  self-break step if time allows.
- Threshold: claim only if d >= 10 (strictly above the live lower bound 9) and d <= 12 (upper bound), by both
  programs, and the cell re-fetched right before the panel still reads lower bound <= d - 1.
- Same rule for the lead cell (9,31,17): d >= 11 and <= 13 (carried as a lead, not claimed this run: one claim per
  run, NEXT_RUN.md).

null_test: not needed because the claim is an explicit object checked by deterministic exact minimum-distance programs against a table value; no search statistic or "beats chance" claim is made.
