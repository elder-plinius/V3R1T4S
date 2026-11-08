# Preregistration: erdos757-sidon-in-45-sets

frozen_utc: 2026-10-14T03:20:00Z
target_id: erdos757-sidon-in-45-sets
null_test: not needed because any claimed witness is a finite discrete mathematical object (an integer set A or an explicit 3-uniform hypergraph H) verified exhaustively and deterministically against exact combinatorial criteria and rational thresholds.

## Success Criterion (Verbatim)
Success means a finite set A of distinct integers with all of the following. (1) Every 4-subset has at least 5 distinct absolute differences, checked exhaustively. (2) The exact maximum Sidon subset size s(A) is certified by two independent exact methods (bitmask branch-and-bound and an ILP that forbids every a+b=c+d, including a=b, i.e. 3-APs). (3) The ratio s/|A|, compared in fractions.Fraction, is STRICTLY SMALLER (direction: min) than the best upper bound on c* shown at verification time at https://www.erdosproblems.com/757, on the EinsteinArena 'Sidon Subsets of (4,5)-Sets' leaderboard and in any newer arXiv paper (context: 4/7 on 2026-10-03; a ratio exactly equal to the live best is not a success). (4) s/|A| >= 9/17; a ratio below 9/17 contradicts a theorem and means a bug, never a claim. (5) The verifier confirms in arXiv:2602.23282 the lemma that a finite witness bounds c* (the blow-up lemma or the inf-formula), or else re-derives it. (6) The checker reproduces s=8 on the Ma-Tang 14-set as a calibration test.

## Partial Wins (Verbatim)
- p1: A new extremal witness: a (4,5)-set A with |A| NOT a multiple of 14 (e.g. |A| = 21 with s = 12) whose certified exact maximum Sidon subset gives s/|A| exactly equal to the live best ratio (4/7 on 2026-10-03), verified by the same two-method pipeline. Disjoint unions of dilated copies of the Ma-Tang 14-set only reach multiples of 14, so this is a structurally new extremal example.
- p2: A frozen abstract target: an explicit 3-uniform hypergraph H on n vertices that satisfies every structural property arXiv:2602.23282 proves for 3-AP hypergraphs of (4,5)-sets (linear, F7-free, at most n-2 edges, and any further listed condition, each checked by script against the paper), with exact independence number alpha(H) and alpha(H)/n strictly below the live best ratio. The skeptic must confirm that the paper does not already exhibit or exclude such an H.

## Exact Checker and Thresholds
- Checker script: `verify_erdos757.py`
- Calibration requirement: `A_14 = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]` must pass `is_45 == True` and `s_method1 == s_method2 == 8` (`Fraction(8, 14) == Fraction(4, 7)`).
- Full win threshold: `is_45 == True` and `Fraction(9, 17) <= Fraction(s, n) < Fraction(4, 7)` with `s_method1 == s_method2 == s`.
- Partial win `p1` threshold: `is_45 == True`, `n % 14 != 0`, and `Fraction(s, n) == Fraction(4, 7)` with `s_method1 == s_method2 == s`.
- Partial win `p2` threshold: 3-uniform hypergraph $H$ on $n$ ordered vertices $\{0, \dots, n-1\}$ that is linear, $F_7$-free, has injective midpoint map $\mu(\{i<j<k\}) = j \in \{1, \dots, n-2\}$ (hence $m \le n-2$), and satisfies $\text{Fraction}(9, 17) \le \text{Fraction}(\alpha(H), n) < \text{Fraction}(4, 7)$ certified by two independent exact independence number solvers.
