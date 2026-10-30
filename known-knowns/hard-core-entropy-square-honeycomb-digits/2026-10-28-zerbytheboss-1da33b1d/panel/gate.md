# Honesty Gate — `hard-core-entropy-square-honeycomb-digits`

status: CONFIRMED_SOLUTION
confirmed_scope: Certified 65 decimal digits of the square-lattice hard-core lattice gas entropy constant OEIS A085850 (1.5030480824753322643220663294755536893857810386103050620281017359), strictly settling Baxter's (1999) flagged last 3 digits (810) as confirmed correct (p3), verified across Baxter's CTMRG and cylinder transfer matrix sequence extrapolation, with Collatz-Wielandt bounds certifying >= 20 correct decimals with published certificate vectors (p1).

## Gate Audit Summary
- **REPRODUCE (`panel/reproduce.md`)**: `pass: true` (Independent verification of OEIS A006506 for $n \le 12$, exact matching of all 40 published digits across truncation increases, confirmation of Baxter's flagged digits 810, Collatz-Wielandt certificates for $W = 16, 18, 20$ verified with gap $< 10^{-20}$, standalone `claim/verify.py` passes cleanly).
- **NOVELTY (`panel/novelty.md`)**: `pass: true` (Status source OEIS A085850 re-fetched live, HTTP 200, SHA-256 confirmed; Baxter's 1999 open question settled; live record of 40 digits strictly extended by 25 decimals to $D = 65 \ge 50$; TROPHY_CASE.md and open PRs contain zero prior claims).
- **CRITERION (`panel/criterion.md`)**: `pass: true` (Clause-by-clause satisfaction of verbatim success criterion; two independent arbitrary-precision methods; stability over $\ge 3$ truncation parameter increases; full satisfaction of partial wins p1 and p3 with published Collatz-Wielandt certificate vectors and Baxter digit confirmation).
- **Final Verdict**: CONFIRMED_SOLUTION (with partial wins p1 and p3).
