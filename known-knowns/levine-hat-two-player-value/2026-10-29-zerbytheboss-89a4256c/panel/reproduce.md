# Reproduce Skeptic Report — `levine-hat-two-player-value`

context: subagent (fresh invocation)
target_id: levine-hat-two-player-value
review_utc: 2026-10-29T16:15:00Z

## Verification Audit

1. **Independent Verification of Bucket-Weight Reduction**:
   - The two-player hat problem on stack height $h$ has $2^h \times 2^h = 4^h$ configurations $(x, y) \in \{0,1\}^h \times \{0,1\}^h$.
   - Player 1 uses strategy $f: \{0,1\}^h \to \{0..h-1\}$ and Player 2 uses strategy $g: \{0,1\}^h \to \{0..h-1\}$.
   - They win iff $x_{f(y)} = 1$ and $y_{g(x)} = 1$.
   - Given Player 1's strategy $f$, Player 2 sees $x$ and chooses level $j = g(x)$ to maximize:
     $$\sum_{y: x_{f(y)}=1} y_j = \sum_{k: x_k=1} c_{k, j}, \quad c_{k, j} \equiv \sum_{y: f(y)=k} y_j$$
   - Total wins under optimal response is:
     $$\text{Wins}(f) = \sum_{x \in \{0,1\}^h} \max_{0 \le j < h} \sum_{k: x_k=1} c_{k, j}$$
   - This exact formula reduces the $4^h$ configuration evaluation to $2^h$ subset summations, enabling exact evaluation in $O(2^h)$ operations.
   - Verified that $\text{Wins}(f, g^*) = \text{Wins}(f)$ holds with zero error across 1,000 random strategy pairs.

2. **Finite-Stack Calibrations**:
   - $h=1$: $1/4 = 0.25$ [PASS]
   - $h=2$: $5/16 = 0.3125$ [PASS]
   - $h=3$: $22/64 = 11/32 = 0.34375$ [PASS] (matches Carter-Reyes/Tiefenbruck OEIS A345255)

3. **Exhaustive Canonical Search for $h=4$ ($V_{2,4}$)**:
   - Evaluated across all $S(16,1) + \dots + S(16,4) = 178,973,355$ canonical restricted growth strings (representing all $4^{16} = 4,294,967,296$ strategy pairs).
   - Rayon-parallel branch-and-bound search in compiled Rust completed in 2.180s.
   - 27,497,355 subtrees pruned using the admissible remaining-ones upper bound.
   - 11,505,600 full strategy nodes evaluated.
   - Maximum win count is strictly 89 wins out of 256 configurations ($89/256 = 0.34765625$). Exactly 1,152 canonical strategies achieve 89 wins. Zero strategies achieve $\ge 90$ wins.
   - Unconditionally proves $V_{2,4} = 89/256 = 0.3476562500$ (Partial Win p1).

4. **Matrix Hint Game Calibrations (Lens 2)**:
   - Evaluated matrix game formula:
     $$V(M; \sim) = \frac{1}{C \cdot 2^K} \sum_{b \in \{0,1\}^K} \max_{0 \le i < R} (r_i \cdot v(b))$$
   - $2 \times 2$ Identity Matrix: $V(M) = 3/8 = 0.375000$ [PASS]
   - $4 \times 6$ Balanced Matrix ($R=4, C=6$): $V(M) = 18/48 = 3/8 = 0.375000$ [PASS] with partition `[0, 0, 1, 2, 1, 2]`.
   - $8 \times 14$ Affine Matrix ($R=8, C=14$): $V(M) = 81/224 \approx 0.3616071429$ [PASS]
   - $16 \times 30$ Affine Hint Matrix: Multi-start 1-opt local hill climbing over 24,000 trials reproduced the known partition achieving $342/960 = 57/160 = 0.3562500000$, establishing the lower bound $V(M_{16 \times 30}) \ge 57/160$.

5. **Standalone Python Verification**:
   - `verify_all.py` executed in pure Python with exact `fractions.Fraction` arithmetic verified all witness pairs, direct $4^4 = 256$ game simulation (89/256), and calibration matrices with zero numerical discrepancy.

pass: true
