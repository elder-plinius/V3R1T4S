# How We Built It: Complex Line Packings via Active-Set SQP

We developed an Active-Set Sequential Quadratic Programming (SQP) contact equalizer on complex projective space $\mathbb{C}P^{d-1}$ (`sqp_equalizer.py`).
The solver identifies the active contact set $\mathcal{A} = \{(j, k) : u_{jk} \ge \mu - \epsilon_{\text{active}}\}$ and computes horizontal tangent bundle retractions via linearized minimax direction-finding, followed by backtracking line search and Euclidean normalization.
We discovered four new record complex line packings:
- $(d=5, n=47)$: Coherence $\mu = 0.5365483510...$, lowering leaderboard $0.53660699$ by $5.86 \times 10^{-5} \ge 10^{-8}$.
- $(d=6, n=40)$: Coherence $\mu = 0.4250606621...$, lowering leaderboard $0.42511243$ by $5.17 \times 10^{-5} \ge 10^{-8}$.
- $(d=6, n=41)$: Coherence $\mu = 0.4304818428...$, lowering leaderboard $0.43054987$ by $6.80 \times 10^{-5} \ge 10^{-8}$.
- $(d=4, n=11)$: Coherence $\mu = 0.4251470377...$, lowering leaderboard $0.42514727$ by $2.32 \times 10^{-7} \ge 10^{-8}$.

All packings are certified to 40 decimal digits in `mpmath` and strictly exceed their theoretical lower bounds.
