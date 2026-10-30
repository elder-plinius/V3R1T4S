# Honesty Gate — `bitcoin-selfish-mining-revenue-bounds`

status: CONFIRMED_SOLUTION
confirmed_scope: Machine-checkable average-reward dual certificates verifying that maximum relative revenue REV in the untruncated SSZ Bitcoin selfish mining model (gamma = 0) satisfies U <= 0.70099 at alpha = 0.45 and U <= 0.90466 at alpha = 0.475 (each 1e-4 strictly below published SSZ Table 2 upper bounds 0.70109 and 0.90476), certified in exact rational arithmetic on finite over-paying MDP N_rho^T with zero Bellman violations, reproducing published SSZ Table 2 calibration at alpha = 0.425 and 0.45.

## Gate Audit Summary
- **REPRODUCE (`panel/reproduce.md`)**: `pass: true` (Independent verification of SSZ Section 4.2 MDP dynamics, exact reproduction of SSZ Table 2 calibration at alpha = 0.425 and alpha = 0.45 within 10^-5, confirmation that N_rho^T at alpha = 0.45, rho = 0.66 has positive optimal gain, exact rational verification of 5 dual certificates across up to 98,283 states with zero violations, stationary policy evaluation exceeding published bars by > 10^-6, and successful rejection of corrupted certificates).
- **NOVELTY (`panel/novelty.md`)**: `pass: true` (SSZ Table 2 published upper bounds 0.70109 and 0.90476 have stood uncertified since 2016; this work provides the first exact certified upper bounds 0.70099 and 0.90466 improving upon published literature by 10^-4; TROPHY_CASE.md and open PRs contain zero competing claims).
- **CRITERION (`panel/criterion.md`)**: `pass: true` (Fully satisfies all requirements for CONFIRMED_SOLUTION: machine-checkable certificate format, U <= 0.70099 at alpha = 0.45, U <= 0.90466 at alpha = 0.475, exact rational arithmetic verification with g < 0, independent model calibration, plus partial wins p1 and p2).
- **Downgrade Checks**: Zero hedging, zero reproduction mismatches, zero stretched criteria, zero leaks. Final status is CONFIRMED_SOLUTION.
