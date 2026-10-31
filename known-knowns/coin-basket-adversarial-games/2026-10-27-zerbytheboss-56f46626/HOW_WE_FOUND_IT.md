# How We Found It — `coin-basket-adversarial-games`

*contributor text, unverified*

## The Brief
Ruediger Jehn's adversarial 3-basket coin games were published to the OEIS in late 2025 and early 2026:
- OEIS A392305 ('Fill your basket' fair compensation) had only 16 known terms ($n = 1..16$), with terms beyond 16 open due to combinatorial state explosion.
- OEIS A391538 ('Game of Chests' guaranteed win) had 14 known terms ($n = 1..14$) with an unproved conjectured formula $a(n) = \lfloor n(n-1)/6 \rfloor + n$ for $n > 4$.

The success criterion required computing $K = 4$ new terms for A392305 ($n = 17..20$) with two-sided strategy certificates and exact reproduction of all 16 published terms.

## What Failed
- **Naive Alpha-Beta Minimax**: Standard minimax trees evaluate unbounded integer payoffs. Because payoff branches span many distinct integers, alpha-beta windowing produced frequent hash collisions and shallow cutoffs, failing to scale beyond $n=15$ in reasonable time.
- **Whole-Tree Strategy Serialization**: Dumping full state-by-state explicit strategy decision trees for $n=17$ generated JSON files exceeding 40 MB, violating storage parsimony.
- **Unbounded Hash Growth**: Using standard library dynamic hash maps incurred heavy re-hashing and allocator overhead once state graphs exceeded $10^7$ nodes.

## What Worked
1. **$S_3$ Quotienting & Compact State Representation**:
   Permutation symmetry across the 3 baskets was quotiented out by maintaining sorted basket sums $s_0 \le s_1 \le s_2$. The third basket sum is implicitly $s_2 = T_{\text{placed}} - s_0 - s_1$. States were packed into a single 64-bit integer: `((mask as u64) << 32) | ((s0 as u64) << 16) | (s1 as u64)`.
2. **Two-Sided Boolean Decision Brackets**:
   Instead of searching for exact payoff integers, the game was converted into exact boolean decision queries: `can_placer_force_ge(mask, s0, s1, c_rem, target)`.
   This enables structural bounding: if $(s_2 - s_1) + C_{\text{rem}} < \text{target}$, the branch is pruned immediately.
   A value $v$ is proved exact if and only if Placer forces $\ge v$ and Placer cannot force $\ge v + 1$ (meaning Presenter caps $\le v$).
3. **High-Performance Open-Addressing Transposition Table**:
   A zero-allocation open-addressing table with power-of-2 capacity and SplitMix64 hashing was pre-allocated, achieving sub-15s solve times for $n=17$ and solving through $n=20$ in a single session.
4. **Clean-Room Independent Verification**:
   An independent game-graph walker was constructed in clean-room Rust, verifying calibration sequences, confirming the new terms, and validating that negative controls (corrupted claims) are rejected.
