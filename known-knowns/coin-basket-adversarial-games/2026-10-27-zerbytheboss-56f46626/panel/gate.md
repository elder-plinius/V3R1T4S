# Honesty Gate — `coin-basket-adversarial-games`

status: CONFIRMED_SOLUTION
confirmed_scope: CONFIRMED_SOLUTION: The exact minimax values of Ruediger Jehn's 'Fill your basket' adversarial game (OEIS A392305) for n = 17, 18, 19, 20 are 7, 7, 8, 8 under optimal play with two-sided decision-bracket certificates, reproducing n = 1..16 bit-for-bit; and the guaranteed win sum (OEIS A391538) for n = 15..21 matches the conjectured formula floor(n(n-1)/6) + n (50, 56, 62, 69, 76, 83, 91), reproducing n = 1..14.

## Gate Audit Summary
- **REPRODUCE (`panel/reproduce.md`)**: `pass: true` (Two independently compiled exact Rust minimax solvers verify exact integer minimax values across all terms, reproducing published calibration sequences A392305 n=1..16 and A391538 n=1..14 with 100% agreement, and proving negative mutation controls fail).
- **NOVELTY (`panel/novelty.md`)**: `pass: true` (Checked against live OEIS entries A392305 and A391538; new terms A392305(17..20) and A391538(15..21) do not appear in the literature, b-files, or edit history; TROPHY_CASE.md and open PRs contain zero prior claims).
- **CRITERION (`panel/criterion.md`)**: `pass: true` (Meets verbatim bank criteria for full CONFIRMED_SOLUTION with K=4 new terms for A392305, two-sided decision brackets, and independent game-graph walking).
- **Downgrade Checks**: Zero hedging, zero reproduction mismatches, zero floating-point operations, zero leaks. Final status is CONFIRMED_SOLUTION.
