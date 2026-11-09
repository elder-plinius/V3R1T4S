# Preregistered Evaluation Bar (`guts-weenie-rule-strong-equilibrium`)

frozen_utc: 2026-10-29T04:47:19Z
target_id: guts-weenie-rule-strong-equilibrium
category: graphs-games-automata
null_test: not needed because deterministic algebraic certificates (exact rational Bernstein expansion, Handelman representations, and certified rational SOS decompositions) prove nonnegativity on all chambers without statistical hypothesis testing

## 1. Verbatim Target Bank Criteria
> EITHER (a) a refutation: one n >= 4 and an explicit threshold vector (t2, ..., tn) for which the exact alpha value alpha(3^(-1/(n-1)), t2, ..., tn) is strictly negative. A counterexample must specify every threshold as a rational or real algebraic number with isolating data; the distinguished threshold is the positive root of 3*a^(n-1)-1=0. OR (b) a kernel-checked formal proof (Lean, Rocq/Coq or Isabelle, with no sorry, admit or extra axioms, and an axiom audit) of the displayed inequality for every integer n >= 2 and every opponent threshold vector. For the proof route, a written or computer-assisted proof whose analytic steps are not formalised does not count; exact or interval computations may support it only inside the formal proof, where the proof assistant checks them. A finite grid with no counterexample is not a proof.

## 2. Partial Wins (Verbatim)
- **p1:** The inequality for n=4 for ALL (t2,t3,t4) in [0,1]^3, with an exact global nonnegativity certificate: on every ordering chamber and boundary, a rational sum-of-squares, Bernstein or Positivstellensatz identity (or a replayable real-algebraic decision certificate) that an independent checker verifies in exact arithmetic.
- **p2:** The same exact global nonnegativity certificate for n=5, for ALL four opponent thresholds.

## 3. Preregistered Checkers & Thresholds
1. **Target Claims:**
   - **p1:** Exact global nonnegativity certificate for $n=4$ across all 4 ordering chambers $C_0, C_1, C_2, C_3$ of the sorted threshold simplex $0 \le t_2 \le t_3 \le t_4 \le 1$ partitioned at $a = 3^{-1/3}$.
   - **p2:** Exact global nonnegativity certificate for $n=5$ across all 5 ordering chambers $C_0, C_1, C_2, C_3, C_4$ of the sorted threshold simplex $0 \le t_2 \le t_3 \le t_4 \le t_5 \le 1$ partitioned at $a = 3^{-1/4}$.
2. **Two Independent Lenses:**
   - **Lens 1 (`attempts/chamber_bernstein_positivity/`):** Exact chamber decomposition, affine mapping to standard simplices, and rational Bernstein / Handelman certificate over $\mathbb{Q}[a]$ with rational isolating intervals for $a$ ($a \in [11/16, 16/23]$ for $n=4$; $a \in [3/4, 4/5]$ for $n=5$), verifying that all certificate coefficients are strictly positive on the chamber interiors and certify the strictly positive definite Hessian at $(a, \dots, a)$.
   - **Lens 2 (`attempts/sos_interval_refutation/`):** Certified rational Sum-of-Squares (SOS) decomposition on each chamber, combined with exhaustive rational interval branch-and-bound verification over $[0,1]^{n-1}$ proving that no negative counterexample exists anywhere in the domain.
3. **Reproducibility Checks:**
   - Reproduction of closed-form $n=2$ and $n=3$ formulas from Buck et al. (arXiv:2208.02788 Propositions 6.1 and 6.2) with 0 error.
   - Verification that $\alpha(a, a, \dots, a) = 0$ exactly across all chambers.
   - Exact rational arithmetic check confirming every term and expansion identity in `fractions.Fraction`.
