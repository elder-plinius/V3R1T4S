# Pre-Registration: qrac-qutrit-three-trits-smallest-open

- **Frozen UTC**: `2026-11-16T03:00:30Z`
- **Target ID**: `qrac-qutrit-three-trits-smallest-open`
- `null_test: not needed because explicit mathematical object or exact rational SDP dual certificate deterministically verified in exact rational / outward-rounded interval arithmetic against published mathematical bounds`

## Verbatim Success Criterion and Partial Wins

- **Full win**: Success means EITHER (a) 27 density matrices on C^3 and three 3-outcome POVMs (positive semidefinite, summing to the identity, given exactly or to 30 digits and verified in exact or interval arithmetic) whose ASP for n = d = D = 3, computed by the formula above at 40 digits, is STRICTLY GREATER (direction: max) than 0.69715, the best value in arXiv:2312.14142 (re-fetched live before claiming, plus an arXiv check for newer results), by at least 1e-5 (ASP >= 0.69716); OR (b) a proven upper bound on the ASP valid for ALL states and POVMs in dimension 3 that is STRICTLY LESS (direction: min) than 0.69853, given as an exact (rational or algebraic) dual certificate or a machine-checked proof.
- **Partial win p1**: A proven upper bound of at most 0.6990 on the ASP for n = d = D = 3, valid for general POVMs, given as an exactly verified certificate (a rational SDP dual whose feasibility and value are checked in exact arithmetic, for a relaxation that does not assume projective measurements) or as a machine-checked proof. This is the first rigorous POVM-valid bound at the level of the floating-point Pauwels et al. value.
- **Partial win p2**: For another n = 3 cell of the arXiv:2312.14142 table with (d,D) in {(3,4), (3,5), (4,4), (4,5), (2,3)}, an explicit strategy beating the tabulated seesaw value by at least 1e-5, verified as in (a).

## Exact Mathematical Quantity and Frozen Thresholds

For $(n, d, D)$, states $\{\rho_x\}_{x \in \{0,\dots,d-1\}^n}$ on $\mathbb{C}^D$ ($\rho_x = \rho_x^\dagger \succeq 0$, $\operatorname{Tr}(\rho_x) = 1$) and $d$-outcome POVMs $\{M^i_a\}_{a=0}^{d-1}$ on $\mathbb{C}^D$ ($M^i_a = (M^i_a)^\dagger \succeq 0$, $\sum_{a=0}^{d-1} M^i_a = I_D$ for each $i \in \{0,\dots,n-1\}$):
$$\mathrm{ASP}(\{\rho_x\}, \{M^i_a\}) = \frac{1}{n d^n} \sum_{x \in \{0,\dots,d-1\}^n} \sum_{i=0}^{n-1} \operatorname{Tr}(\rho_x M^i_{x_i}).$$

1. **Mandatory calibration checks in standalone checker `verify_qrac333.py`**:
   - Positive check 1 (`(n,d,D) = (2,3,3)` MUB optimum): $\mathrm{ASP} = \frac{1}{2}(1 + \frac{1}{\sqrt{3}}) = 0.78867513459481288225...$.
   - Positive check 2 (`(n,d,D) = (3,3,3)` 3-MUB baseline): $\mathrm{ASP} = \frac{4}{9} + \frac{4\sqrt{3}}{27}\cos(\frac{\pi}{18}) = 0.69714623168961306818...$.
   - Negative check: reject non-PSD operators, trace $\neq 1$, POVM sum $\neq I_D$, or corrupted dual $LDL^T$ / moment-balance certificates.

2. **Frozen certification thresholds**:
   - **Full win `(b)`**: Exact rational upper bound $U \in \mathbb{Q}$ satisfying $U < \frac{69853}{100000} = 0.69853$ on $\mathcal{P}^Q_{3,3,3}$, valid for ALL density matrices and ALL general 3-outcome POVMs on $\mathbb{C}^3$ (without assuming projectivity of $M^i_a$ on $\mathbb{C}^3$), certified by an exact rational SDP dual certificate ($Z = L D L^T$ with $D \ge 0$ in `fractions.Fraction` and exact rational operator-moment identity check).
   - **Full win `(a)`**: Explicit rational / 30+ digit states and POVMs for `(3,3,3)` verified PSD with $\operatorname{Tr}(\rho_x)=1$ and $\sum_a M^i_a = I_3$, whose interval-certified lower bound at 50 digits satisfies $\mathrm{ASP} \ge 0.69716$.
   - **Partial win `p1`**: Exact rational upper bound $U \in \mathbb{Q}$ satisfying $U \le \frac{699}{1000} = 0.6990$ on $\mathcal{P}^Q_{3,3,3}$ valid for all general POVMs on $\mathbb{C}^3$, verified in exact `fractions.Fraction` arithmetic.
   - **Partial win `p2`**: Explicit rational / 30+ digit states and POVMs for one cell `(d,D)` in `n = 3` Table 2 of `arXiv:2312.14142v3` whose 50-digit interval-certified ASP lower bound satisfies:
     - `(2,3)`: $\mathrm{ASP} \ge 0.80795$ (beating `0.80794` by $\ge 10^{-5}$),
     - `(3,4)`: $\mathrm{ASP} \ge 0.72568$ (beating `0.72567` by $\ge 10^{-5}$),
     - `(3,5)`: $\mathrm{ASP} \ge 0.76242$ (beating `0.76241` by $\ge 10^{-5}$),
     - `(4,4)`: $\mathrm{ASP} \ge 0.64435$ (beating `0.64434` by $\ge 10^{-5}$),
     - `(4,5)`: $\mathrm{ASP} \ge 0.66332$ (beating `0.66331` by $\ge 10^{-5}$).

## Baseline Reproduction Note

Not an empirical dataset benchmark (`kit/RUN.md` step 3c); deterministic mathematical checker calibrated directly on the exact `(2,3,3)` MUB optimum and `(3,3,3)` 3-MUB baseline from `arXiv:2312.14142v3`.
