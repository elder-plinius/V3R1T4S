# PREREG, run 2026-10-29-0100 (written 2026-10-29T01:03:15Z, before any code of this run is built or measured)

Note: the candidate object was built and measured by run 2026-10-28-0100 (dossier live lead). This run rebuilds it
from the construction text and measures it again; this file freezes the rule before any of this run's measurements.

## Criterion (verbatim, bank/targets.json)

Success means a k x n generator matrix over GF(q) with these properties. (1) Rank is exactly k over GF(q), computed independently. (2) The exact minimum distance d is computed by full enumeration of all q^k - 1 nonzero codewords when feasible (2^k <= ~2^32), or, for large k (or large k with small n-k, via the dual and MacWilliams identities), by two independent exact minimum-distance implementations that agree; never by sampling. (3) d is STRICTLY GREATER (direction: max) than the lower bound in the live http://www.codetables.de/ cell for (q,n,k) at verification time, and at most the upper bound. (4) The code is not one of the 7 LinCodeEvolve codes (arXiv:2609.37056) or a code derived from them, and no newer arXiv claim already reaches that d.

## Statistic and checkers

- Object: a 17 x 31 generator matrix over GF(9) (encoding a + 3b, w^2 = w + 1) built by build_tail.py 16 19 0,1,2,13.
- Rank: Gaussian elimination over GF(9) (rref9 in Python), must equal 17.
- Exact d: two independent exact programs that must agree: m3_mindist (primal column-subset test, all W-subsets,
  W = 1..10 must be empty) and hdep (dual side, smallest dependent set of parity-check columns, exhaustive). A third
  check in the self-break step if time allows.
- Threshold: claim only if d >= 11 (strictly above the live lower bound 10) and d <= 13 (upper bound), by both
  programs, and the cell re-fetched right before the panel still reads lower bound <= d - 1.
- Leads found by other lenses: same rule for their cells (d >= live lower bound + 1 by two exact programs); they are
  carried as leads, not claimed this run (one claim per run, NEXT_RUN.md).

null_test: not needed because the claim is an explicit object checked by deterministic exact minimum-distance programs against a table value; no search statistic or "beats chance" claim is made.
