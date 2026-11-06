# Pre-registration, run 2026-10-27-0100 (written 2026-10-27T01:06:01Z, before any [32,18] candidate's distance was computed)

Criterion (verbatim, from target.md): a k x n generator matrix over GF(q) with (1) rank exactly k, computed
independently; (2) the exact minimum distance d computed by full enumeration when feasible, or by two independent
exact minimum-distance implementations that agree, never by sampling; (3) d STRICTLY GREATER than the live
codetables.de lower bound for (q,n,k) at verification time, and at most the upper bound; (4) not a LinCodeEvolve
code (arXiv:2609.37056) or derived from one, and no newer arXiv claim reaches that d.

Applied to this run: (q,n,k) = (9,32,18). Live lower bound 10, upper 13 (scout.md, 2026-10-27T01:02:31Z).

- Statistic: exact minimum distance d of the claimed 18 x 32 generator matrix over GF(9) (encoding a + b*w as a + 3b,
  w^2 = w + 1).
- Threshold: claim only if d >= 11 (and d <= 13), with rank 18.
- Checkers: (a) m3_mindist (column-subset test over all W-subsets of the 32 coordinates, W = 1..10, exhaustive);
  (b) an independent second exact method written this run (enumeration of the 9^14 dual codewords, or a
  Brouwer-Zimmermann style enumeration, both exhaustive). Both must agree on d. Rank by Gaussian elimination.
- Novelty: re-fetch the live cell once right before the panel and again before packaging; search PRs open and closed.
null_test: not needed because the claim is an explicit object checked by deterministic exact checkers against a table value
