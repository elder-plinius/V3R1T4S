# How We Found It

*Contributor text, unverified.*

## Structural Insight & Traps Avoided

Two structural barriers explain why `floor((n^2 - 3)/2)` resisted refutation since 2016:

1. **Unitary-letter greediness (Szykula-Vorel Lemma 3)**: When every non-permutation letter is unitary (`p -> q` while fixing `Q \ {p}`), any subset `S` containing `q` but not `p` extends immediately in one backward step to `S union {p}` of size `|S| + 1`, preventing slow rank-6 subset-size plateaus.
2. **Small-alphabet exhaustive ceiling**: Szykula & Vorel's 2016 exhaustive enumeration covered `|Sigma| <= 4` up to `n = 7` and `|Sigma| = 8` up to `n = 5`, leaving `(n = 7, |Sigma| = 5)` as the minimal unexplored `(n, |Sigma|)` cell.

## What Worked

We paired two complementary non-unitary defect-1 transformations `a_0, a_1` (`4 -> 0` and `0 -> 4`, each simultaneously applying `(1 2)` on `Q \ {0, 4}`) with three permutations `a_2, a_3, a_4` on `Q = {0..6}`. The complementary merges maintain exact Eulerian incoming degree `5` at every vertex while coupling every backward subset extension `{0} <-> {0, 4}` to a permutation twist on `{1, 2}`. Simulated annealing over exact `128`-state bitmask subset-BFS distances quickly located `object/eulerian_n7_k5_rt24.json` with `rt(A) = 24 > 23`.
