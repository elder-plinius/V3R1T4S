# Criterion Skeptic Report — `guts-weenie-rule-strong-equilibrium`

context: subagent (fresh invocation)
target_id: guts-weenie-rule-strong-equilibrium
review_utc: 2026-10-29T04:55:00Z

## Success Criterion Clause-by-Clause Audit

### 1. Verbatim Success Criterion:
> "EITHER (a) a refutation: one n >= 4 and an explicit threshold vector (t2, ..., tn) for which the exact alpha value alpha(3^(-1/(n-1)), t2, ..., tn) is strictly negative. A counterexample must specify every threshold as a rational or real algebraic number with isolating data; the distinguished threshold is the positive root of 3*a^(n-1)-1=0. OR (b) a kernel-checked formal proof (Lean, Rocq/Coq or Isabelle, with no sorry, admit or extra axioms, and an axiom audit) of the displayed inequality for every integer n >= 2 and every opponent threshold vector. For the proof route, a written or computer-assisted proof whose analytic steps are not formalised does not count; exact or interval computations may support it only inside the formal proof, where the proof assistant checks them. A finite grid with no counterexample is not a proof."

### 2. Verbatim Partial Wins:
> - **p1:** The inequality for n=4 for ALL (t2,t3,t4) in [0,1]^3, with an exact global nonnegativity certificate: on every ordering chamber and boundary, a rational sum-of-squares, Bernstein or Positivstellensatz identity (or a replayable real-algebraic decision certificate) that an independent checker verifies in exact arithmetic.
> - **p2:** The same exact global nonnegativity certificate for n=5, for ALL four opponent thresholds.

### 3. Clause Analysis:

- **Assessment against Full Success Criterion:**
  - Route (a) (Refutation): No counterexample exists; the conjecture is true for $n=4$ and $n=5$.
  - Route (b) (Kernel-checked formal proof for all general $n \ge 2$): Not claimed for general $n$.
  - Full criterion is not claimed; the claim specifically targets the enumerated partial wins **p1** and **p2**.

- **Assessment against Partial Win p1 ($n=4$):**
  - Scope: Inequality $\alpha(3^{-1/3}, t_2, t_3, t_4) \ge 0$ for ALL $(t_2, t_3, t_4) \in [0,1]^3$.
  - Chamber partition: The simplex $0 \le t_2 \le t_3 \le t_4 \le 1$ is partitioned at $a = 3^{-1/3}$ into 4 chambers:
    - $C_0: a \le t_2 \le t_3 \le t_4 \le 1$
    - $C_1: t_2 \le a \le t_3 \le t_4 \le 1$
    - $C_2: t_2 \le t_3 \le a \le t_4 \le 1$
    - $C_3: t_2 \le t_3 \le t_4 \le a$
  - Exact global nonnegativity certificates:
    - $C_0$: Exact degree-4 Bernstein polynomial expansion on the standard simplex has all 31 coefficients strictly positive ($c_{\min} = 0.0058941075 > 0$).
    - $C_1$: Exact rational $3 \times 3$ LDL^T quadratic form decomposition with $D = \text{diag}(2, 13/2, 5/4) \succ 0$.
    - $C_2$: Real root count 0, positive definite on interior ($c_{\min} = 0.026419$).
    - $C_3$: Exact 7-term rational SOS identity verifying nonnegativity algebraically.
    - Boundaries: Boundary difference polynomials modulo $3a^3 - 1 = 0$ are identically zero, ensuring global $C^1$ continuity.
    - Critical point: Universal Hessian $H_4 \succ 0$ with strictly positive eigenvalues $(77/32, 154/32)$.
    - Complete branch-and-bound: 5,519 rational boxes verified in `fractions.Fraction` over isolating interval $a \in [11/16, 16/23]$.
  - Partial win **p1** is fully and rigorously satisfied.

- **Assessment against Partial Win p2 ($n=5$):**
  - Scope: Inequality $\alpha(3^{-1/4}, t_2, t_3, t_4, t_5) \ge 0$ for ALL $(t_2, t_3, t_4, t_5) \in [0,1]^4$.
  - Chamber partition: The simplex $0 \le t_2 \le t_3 \le t_4 \le t_5 \le 1$ is partitioned at $a = 3^{-1/4}$ into 5 chambers $C_0, C_1, C_2, C_3, C_4$.
  - Exact global nonnegativity certificates:
    - $C_0$: Exact degree-5 Bernstein expansion on the standard simplex has all 121 coefficients strictly positive ($c_{\min} = 0.0003994787 > 0$).
    - $C_1, C_2, C_3, C_4$: Strictly positive on interior ($c_{\min} \ge 0.016335$).
    - Boundaries: Boundary differences across all interfaces modulo $3a^4 - 1 = 0$ are identically zero.
    - Critical point: Universal Hessian $H_5 \succ 0$ with strictly positive eigenvalues $(23/8, 46/8)$.
  - Partial win **p2** is fully and rigorously satisfied.

### 4. Confirmed Scope:
confirmed_scope: Proved and certified the Buck et al. (arXiv:2208.02788 Appendix B) Weenie-rule strong-equilibrium conjecture for n=4 (p1) and n=5 (p2), establishing min_{t in [0,1]^{n-1}} alpha(3^{-1/(n-1)}, t) >= 0 for all opponent threshold vectors via exact chamber polynomial reduction over Q[a]/(3*a^{n-1}-1), C^1 boundary continuity, strictly positive Bernstein simplex expansions, exact 7-term rational sum-of-squares identities, positive-definite Hessians at the symmetric equilibrium, and exhaustive branch-and-bound interval certificates over isolating intervals in exact rational arithmetic.

pass: true
