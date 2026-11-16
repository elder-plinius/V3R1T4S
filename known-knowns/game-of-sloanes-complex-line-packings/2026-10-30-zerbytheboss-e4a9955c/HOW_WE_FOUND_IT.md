# How We Found It

contributor text, unverified

We investigated the Chebyshev minimax overlap optimization problem for complex line packings in complex projective space $\mathbb{C}P^{d-1}$.
Starting from incumbent configurations on the Game of Sloanes leaderboard, we identified active contact sets $\mathcal{A} = \{(j, k) : u_{jk} \ge \mu - \epsilon_{\text{active}}\}$ and set up linearized direction-finding subproblems on the horizontal tangent bundle.
Using high-precision Active-Set Sequential Quadratic Programming with HiGHS linear programming and backtracking linesearch, we equalized contact manifolds and iteratively drove down maximum coherence.
The resulting configurations were verified using 40-digit arbitrary precision arithmetic in `mpmath`, lowering the live records across multiple open rows including $(5,47)$, $(6,40)$, $(6,41)$, and $(4,11)$ by margins up to $6.80 \times 10^{-5}$.
