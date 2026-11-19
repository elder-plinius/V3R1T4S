# PREREG.v2 (frozen 2026-10-24T11:16:11Z, before any abstract-hypergraph output is produced or scored)

Why a v2: PREREG.md (frozen 2026-10-24T10:33:26Z) froze only the full-success rule and p1. This run now also attacks
partial win p2 (abstract hypergraphs), and searches for realizable blocks found through abstract ones. PREREG.md is
unchanged and still governs finite integer sets. No abstract-hypergraph search had been run before this file.

## Partial win p2 (verbatim from target.md)
p2: A frozen abstract target: an explicit 3-uniform hypergraph H on n vertices that satisfies every structural property arXiv:2602.23282 proves for 3-AP hypergraphs of (4,5)-sets (linear, F7-free, at most n-2 edges, and any further listed condition, each checked by script against the paper), with exact independence number alpha(H) and alpha(H)/n strictly below the live best ratio. The skeptic must confirm that the paper does not already exhibit or exclude such an H.

## Properties checked (the paper's list for H(A) of a (4,5)-set, read in data/paper.txt)
- Definition 1.7: 3-uniform, on vertex set {0..n-1}, edges distinct triples.
- Lemma 2.4: the midpoint map is injective and never hits a1 or an. Abstract form: with the vertex labels as the
  order, the middle labels of distinct edges are distinct (this forces middles != 0, n-1 and m <= n-2).
- Lemma 2.5: linear (two distinct edges share at most one vertex).
- Lemma 5.2: F7-free, F7 = {012, 034, 056, 135, 246} as in the paper; checked by two independent exhaustive methods
  (an edge-based embedding search and a vertex-7-subset brute force or a second embedding code).
- m <= n-2 checked separately.
- Lemma 2.3 (h = alpha) is a statement about A, not H; Lemmas 3.x, 4.x and 5.1 are not about H(A) of (4,5)-sets.

## Statistic and thresholds
- alpha(H) exact, two methods that must agree: CP-SAT OPTIMAL with best bound = value, and an independent exact
  method (max-plus DP along the explicit block decomposition, or pysat cardinality UNSAT of alpha+1).
- p2 candidate: alpha(H)/n < 5/9 strictly (5/9 = the live community bound frozen in PREREG.md; also report vs 4/7).
- alpha(H)/n < 9/17 contradicts Henning-Yeo (Theorem 5.3 with m <= n-2): a bug, never a claim.
- Full success still needs a finite integer set under PREREG.md; an abstract block that also realizes is checked
  there with the PREREG.md pipeline, nothing else.
- Limit statements (a chain's ratio limit) are not claims; only an explicit finite H or set is.

null_test: not needed because every claim is an explicit finite object checked by deterministic exact checkers against a fixed threshold (no search statistic or beats-chance claim)
