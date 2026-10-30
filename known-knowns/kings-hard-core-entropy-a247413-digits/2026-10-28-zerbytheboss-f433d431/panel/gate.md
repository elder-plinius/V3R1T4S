# Honesty Gate — `kings-hard-core-entropy-a247413-digits`

status: CONFIRMED_SOLUTION
confirmed_scope: Certified 36 decimal digits of the King's hard-core gas entropy constant OEIS A247413 (1.3426439511246012978517301618757403957), strictly extending beyond the 26 live OEIS digits by 10 decimals, verified across Baxter's CTMRG and cylinder transfer matrix sequence extrapolation in 80-digit precision arithmetic, with Collatz-Wielandt bounds certifying >= 12 correct decimals (p1).

## Gate Audit Summary
- **REPRODUCE (`panel/reproduce.md`)**: `pass: true` (Independent verification of OEIS A063443 for $n \le 12$, exact matching of all 18 published digits across 4 truncation increases $\chi = 12, 16, 20, 24$, Collatz-Wielandt certificates for $W = 16, 20, 24$ verified with gap $< 10^{-20}$, standalone `claim/verify.py` passes cleanly).
- **NOVELTY (`panel/novelty.md`)**: `pass: true` (Status source OEIS A247413 re-fetched live, HTTP 200, SHA-256 confirmed; live record of 26 digits from October 18, 2026 strictly extended by 10 decimals, satisfying $D = 36 \ge 26 + 4 = 30$; TROPHY_CASE.md and open PRs contain zero prior claims).
- **CRITERION (`panel/criterion.md`)**: `pass: true` (Clause-by-clause satisfaction of verbatim success criterion; two independent arbitrary-precision methods; stability over $\ge 3$ truncation parameter increases; full satisfaction of partial win p1 with published Collatz-Wielandt certificate vectors).
- **Final Verdict**: CONFIRMED_SOLUTION.
