# Honesty Gate — `guts-weenie-rule-strong-equilibrium`

status: CONFIRMED_PARTIAL
confirmed_scope: Proved and certified the Buck et al. (arXiv:2208.02788 Appendix B) Weenie-rule strong-equilibrium conjecture for n=4 (p1) and n=5 (p2), establishing min_{t in [0,1]^{n-1}} alpha(3^{-1/(n-1)}, t) >= 0 for all opponent threshold vectors via exact chamber polynomial reduction over Q[a]/(3*a^{n-1}-1), C^1 boundary continuity, strictly positive Bernstein simplex expansions, exact 7-term rational sum-of-squares identities, positive-definite Hessians at the symmetric equilibrium, and exhaustive branch-and-bound interval certificates over isolating intervals in exact rational arithmetic.

## Gate Audit Summary
- **REPRODUCE (`panel/reproduce.md`)**: `pass: true` (Independent verification of all 6 stages of `claim/verify.py` in $< 1$s, exact Bernstein expansions on simplices, LDL^T and 7-term rational SOS decompositions, C^1 boundary continuity, strictly positive definite Hessian eigenvalues, and 5,519-box rational interval verification).
- **NOVELTY (`panel/novelty.md`)**: `pass: true` (Status source arXiv:2208.02788v3 re-fetched live, HTTP 200, SHA-256 confirmed; literature search confirms conjecture unproven for $n \ge 4$; TROPHY_CASE.md and open PRs contain zero prior claims).
- **CRITERION (`panel/criterion.md`)**: `pass: true` (Literal clause-by-clause satisfaction of partial win p1 for $n=4$ and partial win p2 for $n=5$ with exact certificates in rational arithmetic).
- **Final Verdict**: CONFIRMED_PARTIAL (p1 and p2).
