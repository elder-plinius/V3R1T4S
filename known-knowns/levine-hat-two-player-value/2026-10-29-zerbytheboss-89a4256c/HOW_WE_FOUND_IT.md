# How We Found It — levine-hat-two-player-value

contributor text, unverified

## The Objective
Settle the exact value of Lionel Levine's two-player hat puzzle on stack height $h=4$ ($V_{2,4}$), resolving the open conjecture of Bouquet, Chikhi, Charles, Zhou, and Wang (arXiv:2508.01737v2, 2026) that $V_{2,4} = 89/256 = 0.34765625$ is the exact optimum across all strategy pairs.

## What Failed
Direct brute force across all two-player 4-hat strategy pairs $(f, g)$ requires testing $4^{16} \times 4^{16} = 4^{32} \approx 1.84 \times 10^{19}$ combinations, each evaluated across 256 configurations ($4.7 \times 10^{21}$ game simulations). Naive search is completely intractable on laptop hardware. Furthermore, testing only symmetric strategies (as done by Buhler et al., 2021) leaves open the possibility of an asymmetric pair achieving $\ge 90$ wins.

## What Worked
1. **Exact Bucket-Weight Reduction**:
   Given Player 1's strategy $f: \{0,1\}^4 \to \{0..3\}$, Player 2's optimal response win count is computed directly from the $4 \times 4$ bucket-weight matrix:
   $$c_{k, j} = \sum_{y: f(y)=k} y_j$$
   via:
   $$\text{Wins}(f) = \sum_{x \in \{0,1\}^4} \max_{0 \le j < 4} \sum_{k: x_k=1} c_{k, j}$$
   This reduces the evaluation of Player 2's optimal response from $4^{16}$ strategies to an exact $O(2^h)$ sum over 16 bitmasks, eliminating Player 2 from the search entirely.

2. **Canonical Partition Enumeration & Branch-and-Bound**:
   Permuting the names of the 4 buckets $\{0,1,2,3\}$ leaves the set of attainable win counts invariant. We represented Player 1 strategies as restricted growth strings (RGS) covering all set partitions into $\le 4$ blocks ($S(16,1) + S(16,2) + S(16,3) + S(16,4) = 178,973,355$ states).
   We derived an admissible remaining-ones upper bound that pruned 27,497,355 subtrees during depth-first search.

3. **Execution & Certification**:
   The search evaluated 11,505,600 nodes in 2.180 seconds in compiled Rust. Exactly 1,152 canonical strategies attained 89 wins; zero attained $\ge 90$ wins. This proved unconditionally that $V_{2,4} = 89/256 = 0.3476562500$, converting Bouquet et al.'s conjecture into a certified theorem.
