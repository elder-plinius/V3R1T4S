# Notes: Lens 1 — Exact Decision-Bracket Minimax Solver

## Hypotheses
1. **Canonical State Packing (Bitmask + Sorted Basket Pairs)** (Chance: 98%, Cost: Low):
   Encoding remaining coins in a 32-bit bitmask and sorting the three basket sums ($s_0 \le s_1 \le s_2$) completely quotients out the $S_3$ basket permutation symmetry. Because the total sum of placed coins $T_{\text{placed}} = n(n+1)/2 - \sum_{c \in R} c = s_0 + s_1 + s_2$ is an invariant, $s_2$ is strictly determined by $(R, s_0, s_1)$. Packing `(mask: u32, s0: u8, s1: u8)` into a single 64-bit integer allows zero-allocation fast hashing or direct array addressing.

2. **Decision-Bracket Boolean Search (AND-OR Game Tree Cutoffs)** (Chance: 95%, Cost: Low):
   Evaluating a scalar minimax value $v$ via boolean queries `can_placer_force_ge(v)` allows aggressive dual-sided alpha-beta pruning: Placer breaks out on the first coin returning `true`, and Presenter breaks out on the first basket returning `false`. Testing $v = a(n-1)$ and $v = a(n-1) + 1$ settles exact values in minimal node evaluations.

3. **Descending Placer Coin Ordering & Ascending Presenter Basket Ordering** (Chance: 90%, Cost: Low):
   Placer ordering moves from largest available coin down to smallest maximizes the likelihood of hitting an early `true` cutoff. Presenter ordering moves from smallest basket sum $s_0$ to largest $s_2$ maximizes the likelihood of presenting an underfilled basket that Placer cannot salvage to reach the target, triggering early `false` cutoffs.

4. **Cross-Domain Import: Nim-Sum / Combinatorial Game Theory Parity Invariants** (Chance: 40%, Cost: Medium):
   Import from impartial game theory / Sprague-Grundy theorem: analyze parity transitions of $\sum s_i$ and the distribution of odd/even coins. If remaining coins contain an imbalance of parities, certain basket residue classes modulo 2 or 3 may be unreachable, providing a priori pruning bounds.

5. **Cross-Domain Import: Zero-Suppressed Binary Decision Diagrams (ZDD) Level-by-Level Synthesis** (Chance: 50%, Cost: Medium):
   Import from VLSI logic synthesis and combinatorics: treat the set of reachable game states as a layered decision diagram indexed by remaining coin count $m \in \{0, \dots, n\}$. Evaluating states level by level from $m = 0$ upward permits compact scratch arrays per depth level, avoiding global hash table collision overhead.

6. **Upper-Bound Pruning via Remaining Coin Sum Partitioning** (Chance: 85%, Cost: Low):
   At state $(R, s_0, s_1, s_2)$, the total remaining coin sum is $C_{\text{rem}} = \sum_{c \in R} c$. In A391538, if $s_2 + C_{\text{rem}} < v$, then even if all remaining coins were routed to the largest basket, it cannot reach $v$, allowing immediate `false` return without exploring child moves.

7. **Wildcard: Negative Margin Invariant & Asymptotic Ratio Convergence** (Chance: 25%, Cost: Low):
   The sequence A392305 grows extremely slowly (1, 1, 1, 2, 3, 3, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6), advancing by at most 1 every 3-5 steps. If the optimal basket balance at turn $n$ maintains $|s_i - s_j| \le \text{const}$, the margin $S_{\max} - S_{\text{mid}}$ is bounded by a sublinear function of $n$. We test whether A392305(17) remains 6 or advances to 7.

8. **Two-Sided Strategy Certificate Synthesis** (Chance: 95%, Cost: Medium):
   During boolean decision search at the exact minimax value $v = a(n)$, extracting the winning move choices generates two verifiable strategy lookup tables: Placer policy $\pi_P(R, s_0, s_1, s_2, b)$ guaranteeing margin $\ge v$, and Presenter policy $\pi_O(R, s_0, s_1, s_2)$ holding margin $\le v$.

## Decisive Testing Plan
- Implement high-speed Rust bitmask + canonical state decision minimax engine.
- Calibrate on A392305 for $n=1..16$ and A391538 for $n=1..14$.
- Compute A392305 for $n=17, 18, 19, 20$.
- Compute A391538 for $n=15..22$ and compare against $\lfloor n(n-1)/6 \rfloor + n$.
- Export strategy certificates to JSON for independent verification.
