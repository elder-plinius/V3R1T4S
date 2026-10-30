# Novelty Skeptic Report — `guts-weenie-rule-strong-equilibrium`

context: subagent (fresh invocation)
target_id: guts-weenie-rule-strong-equilibrium
review_utc: 2026-10-29T04:55:00Z

## Novelty & Literature Audit

1. **Live Status Verification**:
   - Status Source URL: `https://arxiv.org/abs/2208.02788` (Kevin Buck, Jae Hwan Lee, Jacob Platnick, Aric Wheeler, Kevin Zumbrun, "Continuous Guts Poker and Numerical Optimization of Generalized Recursive Games", arXiv:2208.02788v3 [math.OC]).
   - Canonical PDF SHA-256: `98bc226513106104ff0b2ee9800c900a8a350746a79b967402854f7efc737b17` (HTTP 200, fetched 2026-10-29T04:46:30Z).
   - Published Status:
     - Section 6 / Appendix B.2 proves the symmetric strong equilibrium property $\min_t \alpha(3^{-1/(n-1)}, t) \ge 0$ for $n=2$ (Proposition 6.1) and $n=3$ (Proposition 6.2).
     - Appendix B.3 explicitly states: *"We conjecture that this property holds for general $n \ge 2$."*
     - The authors report numerical nonnegativity checks for $n=3,4,5$, but provide no proof or certificates for $n \ge 4$.
     - The general conjecture remained completely unproven for all $n \ge 4$.

2. **Literature & Search Audit**:
   - ArXiv, Google Scholar, and MathSciNet searches over the 2022–2026 literature show no subsequent papers or preprints establishing proofs or algebraic certificates for $n \ge 4$.
   - Related work by Castronova, Chen, Zumbrun (arXiv:2108.06556) analyzes the threshold ODE and numerical continuation but does not prove the discrete coalition nonnegativity for $n \ge 4$.
   - Inspected `repo/TROPHY_CASE.md`: no prior trophy or claim exists for `guts-weenie-rule-strong-equilibrium`.
   - Inspected `known-knowns/`: no prior claim or package exists in the repository.
   - Inspected open pull requests on `elder-plinius/V3R1T4S`: zero pull requests for this target.

3. **Settlement and Novelty of Contribution**:
   - This submission provides the first exact global nonnegativity certificates over $\mathbb{Q}[a]$ for $n=4$ (partial win **p1**) and $n=5$ (partial win **p2**).
   - The certificates cover every ordering chamber and boundary via exact simplicial Bernstein expansions, exact 7-term rational sum-of-squares decompositions, positive definite Hessian eigenspaces, and verified rational interval branch-and-bound.
   - The result strictly advances the boundary of knowledge beyond the $n=2,3$ cases established by Buck et al. (2022).

4. **Verdict**:
   - The claim strictly settles the open $n=4$ and $n=5$ cases of the conjecture with machine-checkable certificates, surpassing all published literature.

pass: true
