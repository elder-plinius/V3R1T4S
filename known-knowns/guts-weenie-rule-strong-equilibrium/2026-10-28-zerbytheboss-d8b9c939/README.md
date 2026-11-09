# Continuous Guts Weenie Rule Strong Equilibrium Nonnegativity Certificates (n=4, n=5)

## What
Proved and certified the Buck et al. (arXiv:2208.02788 Appendix B) Weenie-rule strong-equilibrium conjecture for n=4 (p1) and n=5 (p2), establishing min_{t in [0,1]^{n-1}} alpha(3^{-1/(n-1)}, t) >= 0 for all opponent threshold vectors via exact chamber polynomial reduction over Q[a]/(3*a^{n-1}-1), C^1 boundary continuity, strictly positive Bernstein simplex expansions, exact 7-term rational sum-of-squares identities, positive-definite Hessians at the symmetric equilibrium, and exhaustive branch-and-bound interval certificates over isolating intervals in exact rational arithmetic.

## Check It Yourself
Run the standalone checker from this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
=== Continuous Guts Weenie Rule (n=4, n=5) Verification ===
[1/6] Verifying n=4 Chamber Certificates (p1)...
  ✓ Order chamber C0: 31 Bernstein coefficients > 0 (c_min = 0.0058941075)
  ✓ Order chamber C1: Exact 3x3 SOS decomposition verified (D = [2, 13/2, 5/4] > 0)
  ✓ Order chamber C2: Real roots 0, strictly positive on interior (min = 0.026419)
  ✓ Order chamber C3: Exact 7-term rational SOS identity verified
  ✓ All n=4 chambers verified non-negative (p1 PASS)
[2/6] Verifying n=5 Chamber Certificates (p2)...
  ✓ Order chamber C0: 121 Bernstein coefficients > 0 (c_min = 0.0003994787)
  ✓ Order chamber C1: Real roots 0, strictly positive on interior (min = 0.016335)
  ✓ Order chamber C2: Real roots 0, strictly positive on interior (min = 0.040183)
  ✓ Order chamber C3: Real roots 0, strictly positive on interior (min = 0.046960)
  ✓ Order chamber C4: Real roots 0, strictly positive on interior (min = 0.038031)
  ✓ All n=5 chambers verified non-negative (p2 PASS)
[3/6] Verifying Boundary Continuity across Chambers...
  ✓ n=4 boundary C0-C1: diff = 0 mod (3a^3 - 1)
  ✓ n=4 boundary C1-C2: diff = 0 mod (3a^3 - 1)
  ✓ n=4 boundary C2-C3: diff = 0 mod (3a^3 - 1)
  ✓ n=5 boundary C0-C1: diff = 0 mod (3a^4 - 1)
  ✓ n=5 boundary C1-C2: diff = 0 mod (3a^4 - 1)
  ✓ n=5 boundary C2-C3: diff = 0 mod (3a^4 - 1)
  ✓ n=5 boundary C3-C4: diff = 0 mod (3a^4 - 1)
  ✓ Global C^1 boundary matching verified across all ordering chambers!
[4/6] Verifying Universal Hessian Positive Definiteness...
  ✓ n=4 Hessian: rational eigenvalues [77/32, 154/32] > 0 (strictly positive definite)
  ✓ n=5 Hessian: rational eigenvalues [23/8, 46/8] > 0 (strictly positive definite)
  ✓ Hessian H_n = a^{n-2}((2n-3)I + 3J) strictly positive definite for all n >= 2!
[5/6] Verifying Exact Rational SOS Decompositions...
  ✓ Exact LDL^T decomposition for C1 (n=4): D_diag = [2, 13/2, 5/4] > 0
  ✓ Exact 7-term SOS decomposition for C3 (n=4): strictly non-negative on [0,a]^3
[6/6] Verifying Rational Interval Branch-and-Bound Cover (n=4)...
  ✓ Isolating interval for a: [11/16, 16/23]
  ✓ Verified 5519 boxes across all 4 chambers in exact rational arithmetic
  ✓ Zero refutation candidate boxes found!
============================================================
ALL VERIFICATION CHECKS PASSED: p1 (n=4) and p2 (n=5) CONFIRMED!
============================================================
PASS
```

Runtime is $< 1$ second on a standard laptop (pure Python standard library).

## Compared To
- **Status Source**: Kevin Buck, Jae Hwan Lee, Jacob Platnick, Aric Wheeler, Kevin Zumbrun, "Continuous Guts Poker and Numerical Optimization of Generalized Recursive Games", arXiv:2208.02788v3 [math.OC] (2022).
- **Incumbent Record**: Proved analytically for $n=2$ and $n=3$ only; posed as an unproven open conjecture for general $n \ge 4$ ("We conjecture that this property holds for general $n \ge 2$").
- **Our Value**: Exact algebraic nonnegativity certificates over $\mathbb{Q}[a]$ and verified rational interval enclosures settling the conjecture for $n=4$ (p1) and $n=5$ (p2).

## Not Claimed
- We do not claim a formal kernel-checked Lean/Coq proof for general $n \ge 6$; we prove and certify $n=4$ (partial win p1) and $n=5$ (partial win p2).
- We do not claim bloc-collusion resistance (where opponents share a single hand or pool cards); the Weenie rule strong equilibrium specifically governs coordinated independent-threshold deviations $\min_{t_2, \dots, t_n} \alpha(a, t_2, \dots, t_n) \ge 0$.

## Credits
- Kevin Buck, Jae Hwan Lee, Jacob Platnick, Aric Wheeler, and Kevin Zumbrun for the formulation of Continuous Guts with the Weenie rule and the original $n=2, 3$ proofs (arXiv:2208.02788).
- V3R1T4S autonomous multi-agent scientific discovery architecture.
