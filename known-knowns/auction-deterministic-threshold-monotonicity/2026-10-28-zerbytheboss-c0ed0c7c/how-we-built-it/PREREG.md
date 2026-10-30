# PREREG — auction-deterministic-threshold-monotonicity

frozen: 2026-10-28T22:18:00Z

## Criterion (Verbatim)
An explicit admissible pair of densities (g1 on [0,b1] and g2 on [0,b2], each normalized, strictly positive, nondecreasing and continuously differentiable, as in Theorem 4 of arXiv:2608.22371), preferably polynomials with rational coefficients, and two shifts 0 <= c < c' < 1/g1(0) with certified values showing c2*(c) > c2*(c') strictly, where c2* = max(c2^th1, c2^th2, c2^th3) exactly as defined in Section 3.1 of the paper (the statement above restates the definitions in shifted coordinates). Every quantity that enters the comparison (the monopoly price q at each shift, the maximum in c2^th2, the root defining c2^th3) must be certified by exact algebra (Sturm sequences, isolating intervals with rational endpoints) or rigorous interval arithmetic, and the two enclosures of c2* must be strictly separated. Alternatively, a positive resolution counts only as a kernel-checked formal proof (Lean, Rocq/Coq or Isabelle, with no sorry, admit or extra axioms, and an axiom audit) that c2* is nondecreasing in the shift for the full density class of Theorem 4, stating whether 'increasing' is meant weakly or strictly and handling the equality case; a written or computer-assisted proof whose analytic steps are not formalised does not count. A strict decrease refutes monotonicity in both the weak and the strict sense. Before claiming, re-check arXiv and the journal version for a later answer.

## Exact Checker & Decision Rule
1. **Admissibility**:
   - $g_1(x) = \frac{7}{57} + \frac{350}{57} x^6$ on $[0, 1]$, $g_2(x) = 1$ on $[0, 1]$.
   - Normalize: $\int_0^1 g_1(x) dx = 1$, $\int_0^1 g_2(x) dx = 1$.
   - Positivity: $g_1(x) \ge 7/57 > 0$, $g_2(x) = 1 > 0$.
   - Nondecreasing: $g_1'(x) = \frac{700}{19} x^5 \ge 0$, $g_2'(x) = 0 \ge 0$.
2. **Shifts**:
   - Choose two explicit rational shifts $0 \le c_A < c_B < 1/g_1(0) = 57/7$:
     $c_A = \frac{11702081697}{2754078775} \approx 4.249000$ (corresponding to $y_A = 12/25$),
     $c_B = \frac{939499441}{214943135} \approx 4.370921$ (corresponding to $y_B = 19/40$).
   - Also evaluate the prompt pair $c(y=1/2) = 500/133 \approx 3.759398$ and $c'(y=2/5) = 52859/8785 \approx 6.016961$ to document the $h_2$ and $\max(h_1, h_2)$ drop from $24.417887$ to $18.361972$ / $19.778481$.
3. **Threshold Calculation**:
   - For any shift $c$, find unshifted monopoly price $y(c) \in (0, 1]$ solving $\frac{1 - G_1(y)}{g_1(y)} - y = c$.
   - Compute $h_1(c) = \frac{1}{g_2(0) G_1(y(c))}$.
   - Compute $h_2(c) = \frac{1}{g_2(0)} [ 2 + \max_{0 \le x \le y(c)} (c + x) \frac{g_1'(x)}{g_1(x)} ]$ by checking endpoints $x = 0, y(c)$ and all real stationary roots of the derivative of $\phi(x) = (c+x) g_1'(x)/g_1(x)$ inside $[0, y(c)]$.
   - Compute $R(c) = (c + y(c)) (1 - G_1(y(c)))$, solve for unique $t(c) \in (0, 1]$ such that $\frac{\int_0^t x g_1(x) dx}{G_1(t)} = R(c) - c$, and compute $h_3(c) = \frac{1}{g_2(0) G_1(t(c))}$.
   - Form $c_2^*(c) = \max(h_1(c), h_2(c), h_3(c))$.
4. **Success Threshold**:
   - Certification across Lens 1 (Sturm root isolation) and Lens 2 (80-digit interval arithmetic) establishing:
     $\underline{c_2^*(c_A)} > \overline{c_2^*(c_B)}$ with disjoint certified intervals.
   - Strict decrease $\Delta = c_2^*(c_A) - c_2^*(c_B) > 0.10$ certified.
   - Calibration check on uniform distribution reproducing $2 b_2 b_1^2 / (b_1 - c)^2$.

null_test: not needed because deterministic algebraic and certified interval checks on explicit rational densities
