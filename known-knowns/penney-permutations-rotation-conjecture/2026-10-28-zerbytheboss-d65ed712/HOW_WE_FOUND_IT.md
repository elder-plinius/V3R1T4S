# How We Found It — `penney-permutations-rotation-conjecture`

_contributor text, unverified_

Conjecture 6.1 of Sergi Elizalde and Yixin Lin (*Penney’s Game for Permutations*, DMTCS 28:1 (2026), arXiv:2404.06585) asserts that for any k >= 3 and any permutation sigma in S_k, Bob's right cyclic rotation tau = (sigma_k, sigma_1, ..., sigma_{k-1}) wins with probability strictly greater than 1/2.

In the original paper, the authors proved the conjecture for k = 3 analytically (Section 4), but for k = 4 and k = 5 only reported numerical evidence obtained by truncating the series at horizon n = 11, leaving the remaining tail uncertified.

To rigorously certify the conjecture and explore larger horizons:
1. **Dynamic Programming Over Relative-Order Profiles**: We formulated an exact DP tracking the relative-order profile of the last k - 1 elements across random permutations of length m.
2. **Horizon Tail Bounding**: For each permutation pair (sigma, tau), we computed exact cumulative win counts A(H) and B(H) alongside the unhit remainder count R(H). Whenever 2 * (A(H) + R(H)) < H!, Alice's winning probability is strictly less than 1/2 regardless of how the unresolved tails terminate, rigorously proving Pr(sigma precedes tau) < 1/2.
3. **Dual Software Implementation**: We implemented the dynamic program in compiled Rust using 256-bit exact integer arithmetic (Lens 1) and in pure Python (Lens 2), with cross-validation against brute-force permutation generation up to H = 9.
4. **S_4 Certification**: All 24 permutations of S_4 certified at or before H = 36 (20 at H <= 28, 2 at H = 31, and 2 at H = 36), providing complete mathematical proof for Partial Win p1.
5. **S_5 Scaling**: For S_5, we partitioned all 120 permutations into 60 complement-symmetry classes and solved the exact integer DP up to H = 16, computing exact counts A(16), B(16), R(16) summing to 16! = 20,922,789,888,000. For every single permutation in S_5, Bob's rotation wins with conditional probability B / (A + B) strictly greater than 54.78%, confirming zero counterexamples in S_5.
