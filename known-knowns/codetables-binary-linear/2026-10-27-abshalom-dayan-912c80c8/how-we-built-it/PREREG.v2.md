# Pre-registration v2, run 2026-10-27-0100 (written 2026-10-27T01:54:24Z)

Why a v2: PREREG.md froze the rule for cell (9,32,18). That cell's attack ended negative (attempts/constructor,
attempts/search-engineer). The human's queue (NEXT_RUN.md item 2) then moved the run to other classical GF(9) cells
with n = 28..36. This v2 was written AFTER the cell-picker sweep had already computed d = 8 for a [29,19] code (three
exact checkers, 01:47Z-01:50Z) and after the self-break's fourth method; it does not change any threshold of PREREG.md,
it only names the new cell. The criterion is deterministic (an explicit object, exact distance, a table value), so
nothing here can be tuned to the result.

Criterion (verbatim from target.md): a k x n generator matrix over GF(q) with (1) rank exactly k, computed
independently; (2) the exact minimum distance d by two independent exact implementations that agree, never by
sampling; (3) d STRICTLY GREATER than the live codetables.de lower bound for (q,n,k) at verification time, and at most
the upper bound; (4) not a LinCodeEvolve code (arXiv:2609.37056) or derived from one, and no newer arXiv claim
reaches that d.

Applied: (q,n,k) = (9,29,19). Live cell 7-9 (data/bklc_q9_n29_k19.html, fetched 2026-10-27T01:50:01Z).
- Statistic: exact d of the 19 x 29 generator matrix (encoding a + b*w as a + 3b, w^2 = w + 1).
- Threshold: claim only if d >= 8 and d <= 9, rank 19.
- Checkers: m3_mindist (column-subset test, exhaustive W <= 8) and hdep (dual-side column dependency, exhaustive);
  bz9t (Brouwer-Zimmermann) and dualenum + MacWilliams (all 9^10 dual words) as third and fourth methods.
- Novelty: live cell re-fetched right before the panel (done 01:50:01Z) and again before packaging; PRs open and
  closed searched (data/prs_0151_*.json).
null_test: not needed because the claim is an explicit object checked by deterministic exact checkers against a table value
