# Honesty Gate — `coin-basket-random-expected-values`

status: CONFIRMED_SOLUTION
confirmed_scope: Exact optimal expected values for Jehn's random-basket coin game: A391791(23)=884741548, A391791(24)=1922512940, A391791(25)=4164198462 (k=2) and A391792(19)=45245088184, A391792(20)=149627079790, A391792(21)=492482601295 (k=3), with all published terms reproduced and Jehn's conjecture confirmed for all n in 10..25.

## Gate Audit Summary
- **REPRODUCE (`panel/reproduce.md`)**: `pass: true` (Independent verification by two compiled exact integer solvers in Rust and C++ confirms exact integer agreement across all terms, 100% reproduction of published tables A391791 n=1..22 and A391792 n=1..18, and full reproduction of optimal first moves for n=10..25).
- **NOVELTY (`panel/novelty.md`)**: `pass: true` (Status checked against live OEIS A391791 and A391792 entries; new terms A391791(23..25) and A391792(19..21) do not appear in the literature, b-files, or edit history; TROPHY_CASE.md and open PRs contain zero prior claims; Jehn's conjecture was unverified for n >= 23).
- **CRITERION (`panel/criterion.md`)**: `pass: true` (Meets verbatim bank criteria for full CONFIRMED_SOLUTION with K=3 new terms for each sequence computed by two independent exact integer programs, plus settled status p2 for Jehn's conjecture over n=10..25).
- **Downgrade Checks**: Zero hedging, zero reproduction mismatches, zero floating-point calculations, zero leaks. Final status is CONFIRMED_SOLUTION.
