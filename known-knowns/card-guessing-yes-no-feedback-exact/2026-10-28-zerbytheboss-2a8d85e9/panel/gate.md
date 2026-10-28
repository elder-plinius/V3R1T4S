# Honesty Gate — `card-guessing-yes-no-feedback-exact`

status: CONFIRMED_SOLUTION
confirmed_scope: Exact values of P+_{2,n} (two copies of each of n labels, yes/no feedback, maximizing the expected number of correct guesses) as reduced rationals for EVERY n from 11 through 16, reproducing Diaconis-Graham-Spiro Table 3 for n=2..10 and confirming the persistence conjecture across 27M+ reachable transitions.

## Gate Audit Summary
- **REPRODUCE (`panel/reproduce.md`)**: `pass: true` (Independent verification of Table 3 calibration within 0.00007; exact bit-level agreement between compiled Rust and Python engines on all reduced rationals for n = 11..16; all values are irreducible rationals satisfying Luo analytical bounds).
- **NOVELTY (`panel/novelty.md`)**: `pass: true` (Literature halted at n = 10; Luo arXiv:2609.25062 left exact values for n >= 11 open; TROPHY_CASE.md and open PRs contain zero competing claims; advances solved frontier to n = 16).
- **CRITERION (`panel/criterion.md`)**: `pass: true` (Exact reduced rationals provided for all n = 11..16; calibration matches published values; certificates chunked to <= 900 KB; verification executes in sub-second time).
- **Downgrade Checks**: Zero hedging, zero reproduction mismatches, zero stretched criteria, zero leaks. Final status is CONFIRMED_SOLUTION.
