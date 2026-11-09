# Preregistered Evaluation Bar (`levine-hat-two-player-value`)

frozen_utc: 2026-10-29T15:08:00Z
target_id: levine-hat-two-player-value
category: graphs-games-automata
null_test: not needed because explicit combinatorial objects (finite-stack hat strategies and matrix hint partitions) are evaluated by deterministic exact-integer and rational arithmetic evaluators checking all 4^h configurations and 2^K partition states with zero numerical tolerance

## 1. Verbatim Target Bank Criteria
> Fair coin (p = 1/2) throughout. FULL WIN is either (A) or (B). (A) Upper bound: a 0/1 matrix M (any size, duplicate columns allowed) in which EVERY column has exactly half of its entries equal to 1, together with an exhaustive certificate, evaluated in exact rational arithmetic, that the matrix-game value V(M) = max over all partitions ~ of the columns of V(M;~) is at most some U STRICTLY LESS THAN 81/224 (direction: min). Here, per Buhler et al. Section 3.2, V(M;~) = (1/n) * E[max_i r_i . v], where r_i are the rows of M, n is the number of columns, and v in {0,1}^n is constant on each class of ~ with independent fair bits across classes; by their Section 3.4 this proves V2 <= U. (B) Beyond the conjecture: an explicit two-player strategy pair (finite h, or a recursive infinite strategy with its renewal formula written out) whose exact success probability is STRICTLY GREATER THAN 7/20 (direction: max), refuting Conjecture 1 of Bouquet et al. In both cases the result must also beat any newer value found on the status source at verification time. The improvement bar includes the best valid composition of published objects under these same rules, as well as direct published objects. Unmerged submissions are not bars. State whether the submitted object is a composition and identify all components and their sources.

## 2. Partial Wins (Verbatim)
- **p1:** Exact V_{2,4}: an exhaustive, re-runnable search (symmetry reduction allowed if the verifier re-checks it) over ALL pairs of 4-hat strategies, not only symmetric ones, giving the maximum success probability as an exact rational with an optimal pair. If the maximum exceeds 89/256 it is also a new best 4-hat strategy.
- **p2:** Exact V_{2,5} with an exhaustive or branch-and-bound certificate, OR an explicit h-hat strategy pair for some 4 <= h <= 13 whose exact success probability strictly exceeds the larger of the two values listed for that h in Bouquet et al. (arXiv:2508.01737v2, Section 3). Compare with the best valid composition of published strategies for that h and disclose whether the strategy is a composition. Recover exact published win-count fractions where possible; if only a rounded decimal bar is available, clear it by one unit of its last printed digit.
- **p3:** The exact, certified value V(M) of the 16x30 hint matrix (rows: the 16 points of F_2^4; columns: the 30 non-constant affine functions on 4 bits) proposed by Buhler et al., even if it is not below 81/224 (settling the computation they called infeasible).

## 3. Preregistered Thresholds and Checkers
1. **Lens 1: Exact Bucket-Weight Reduction & Finite-Stack Certification**:
   - Bucket-weight reduction theorem: For Player 1 strategy $f: \{0,1\}^h \to \{0..h-1\}$, bucket weight matrix $c_{k, j} = \sum_{y: f(y)=k} y_j$. The exact maximum win count over all $4^h$ configurations is $\text{Wins}(f) = \sum_{x \in \{0,1\}^h} \max_{0 \le j < h} \sum_{k: x_k=1} c_{k, j}$.
   - Exact $V_{2,4}$ search (p1): Exhaustive canonical search over all $S_4 \times S_4$ symmetry orbits of 4-hat strategies ($\approx 3.7 \times 10^6$ orbits). Threshold to certify: either prove $\max \text{Wins} = 89 \implies V_{2,4} = 89/256 = 0.34765625$ unconditionally, or find $\text{Wins} \ge 90 \implies V_{2,4} \ge 90/256 > 89/256$.
   - Exact $V_{2,5}$ and $h \in [4..13]$ search (p2): Branch-and-bound and canonical partition search for $V_{2,5}$ against Bouquet et al. incumbent $358/1024 = 179/512 = 0.349609375$.
2. **Lens 2: Matrix Hint Game & 16x30 Affine Matrix Local Search**:
   - Exact matrix game formula: $V(M; \sim) = \frac{1}{C \cdot 2^K} \sum_{b \in \{0,1\}^K} \max_{0 \le i < R} (r_i \cdot v(b))$.
   - Calibration check: $V(M_{2 \times 2}) = 3/8 = 0.375$, $V(M_{4 \times 6}) = 3/8 = 0.375$, $V(M_{8 \times 14}) = 81/224 \approx 0.36160714$.
   - Affine hint matrix $M_{16 \times 30}$: 16 points of $\mathbb{F}_2^4$, 30 non-constant affine functions. Threshold: evaluate local search payoff; note that local search establishes only a lower bound on $V(M_{16 \times 30})$.
