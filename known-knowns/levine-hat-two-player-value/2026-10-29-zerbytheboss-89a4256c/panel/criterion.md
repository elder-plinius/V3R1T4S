# Criterion Skeptic Report — `levine-hat-two-player-value`

context: subagent (fresh invocation)
target_id: levine-hat-two-player-value
review_utc: 2026-10-29T16:15:00Z

## Success Criterion Clause-by-Clause Audit

### 1. Verbatim Success Criterion:
> Fair coin (p = 1/2) throughout. FULL WIN is either (A) or (B). (A) Upper bound: a 0/1 matrix M (any size, duplicate columns allowed) in which EVERY column has exactly half of its entries equal to 1, together with an exhaustive certificate, evaluated in exact rational arithmetic, that the matrix-game value V(M) = max over all partitions ~ of the columns of V(M;~) is at most some U STRICTLY LESS THAN 81/224 (direction: min). Here, per Buhler et al. Section 3.2, V(M;~) = (1/n) * E[max_i r_i . v], where r_i are the rows of M, n is the number of columns, and v in {0,1}^n is constant on each class of ~ with independent fair bits across classes; by their Section 3.4 this proves V2 <= U. (B) Beyond the conjecture: an explicit two-player strategy pair (finite h, or a recursive infinite strategy with its renewal formula written out) whose exact success probability is STRICTLY GREATER THAN 7/20 (direction: max), refuting Conjecture 1 of Bouquet et al. In both cases the result must also beat any newer value found on the status source at verification time. The improvement bar includes the best valid composition of published objects under these same rules, as well as direct published objects. Unmerged submissions are not bars. State whether the submitted object is a composition and identify all components and their sources.

### 2. Verbatim Partial Win p1:
> - **p1:** Exact V_{2,4}: an exhaustive, re-runnable search (symmetry reduction allowed if the verifier re-checks it) over ALL pairs of 4-hat strategies, not only symmetric ones, giving the maximum success probability as an exact rational with an optimal pair. If the maximum exceeds 89/256 it is also a new best 4-hat strategy.

### 3. Clause Analysis:

- **Assessment against Full Success Criteria:**
  - Route (A) (Upper bound $U < 81/224$ via matrix hint game): Not claimed. The $16 \times 30$ affine hint matrix was investigated via local hill climbing, reproducing the known payoff $57/160$. In accordance with preregistered traps, finding a partition $\sim^*$ establishes only a lower bound $V(M_{16 \times 30}) \ge 57/160$, not an upper bound on $V(M)$ or $V_2$.
  - Route (B) (Success probability $> 7/20 = 0.35$): Not claimed.
  - The submission specifically targets and satisfies Partial Win **p1**.

- **Assessment against Partial Win p1:**
  - **Exhaustive Re-runnable Search over ALL Pairs of 4-hat Strategies**:
    - The search space consists of all $4^{16} = 4,294,967,296$ strategy pairs $(f, g)$.
    - Player 2's best response is computed exactly via the bucket-weight matrix $c_{k, j} = \sum_{y: f(y)=k} y_j$.
    - The full space of Player 1 strategies is canonically partitioned into $S(16,1) + \dots + S(16,4) = 178,973,355$ restricted growth string states.
    - An admissible branch-and-bound bound prunes subtrees provably incapable of reaching $\ge 89$ wins.
    - All $178.9\text{M}$ canonical states are exhaustively explored by compiled Rust binary `crate_bucket` in 2.180s.
  - **Maximum Success Probability as an Exact Rational**:
    - Certified maximum win count is exactly 89 wins out of 256 configurations:
      $$V_{2,4} = \frac{89}{256} = 0.3476562500$$
    - Exactly 1,152 canonical strategies achieve 89 wins; zero strategies achieve $\ge 90$ wins.
  - **Optimal Pair Provided**:
    - Optimal witness strategy pair $(f^*, g^*)$ is archived in `attempts/lens1_bucket_reduction_v24_v25/lens1_bucket_reduction_output.json`.
    - Verified by direct $4^4 = 256$ configuration simulation in `verify_all.py` to yield exactly 89 wins.
  - Partial Win **p1** is fully and rigorously satisfied.

### 4. Confirmed Scope:
confirmed_scope: Exact rational certification of V_{2,4} = 89/256 = 0.34765625 via exhaustive canonical search over all 4-hat strategies (Partial Win p1).

pass: true
