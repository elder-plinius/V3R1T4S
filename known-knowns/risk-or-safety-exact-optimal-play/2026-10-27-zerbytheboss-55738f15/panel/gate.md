# Honesty Gate — `risk-or-safety-exact-optimal-play`

status: CONFIRMED_SOLUTION
confirmed_scope: Exact reduced rationals A387261(n)/A387262(n) = P(0,0,0) and complete n^2(n+1)/2-position Bellman value/action certificates P(a,b,c) for every n = 31..45 in the coin game Risk or Safety, reproducing published terms n = 1..15 and repository terms n = 16..30, verified by independent exact policy iteration and pure-turn-plan minimax solvers.

## Gate Audit Summary
- **REPRODUCE (`panel/reproduce.md`)**: `pass: true` (Independent verification of all 45 certificates n=1..45: all 408,560 non-terminal positions in claim n=31..45 satisfy the Bellman optimality equations, forced toss at a=0, and action attainment with 0 exact ties; independent integer cross-multiplication confirms coprimality gcd(p,q)=1 on every value; two independent solvers agree on all 45 values).
- **NOVELTY (`panel/novelty.md`)**: `pass: true` (Live status check at https://oeis.org/A387261 on 2026-10-28 confirms published terms exist only for n=1..15; repository known-knowns contains n=16..30; the 15 new terms n=31..45 strictly extend the record frontier with zero overlap).
- **CRITERION (`panel/criterion.md`)**: `pass: true` (All requirements of the bank success criterion for full win CONFIRMED_SOLUTION are satisfied verbatim: exact reduced rationals P(0,0,0) for every n=31..45, complete Bellman certificates for all n=31..45, exact calibration on n=1..15 and n=16..30).
- **Downgrade Checks**: Zero hedging, zero reproduction mismatches, zero stretched criteria, zero leaks. Final status is CONFIRMED_SOLUTION.
