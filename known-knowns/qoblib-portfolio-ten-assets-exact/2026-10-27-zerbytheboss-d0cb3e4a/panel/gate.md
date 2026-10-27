# Honesty Gate — `qoblib-portfolio-ten-assets-exact`

status: CONFIRMED_SOLUTION
confirmed_scope: Globally optimal integer position schedule for QOBLIB instance po_a010_t10_orig_b004_l1e-03 with objective -8397, certified unconditionally by a complete 10,606-state two-pass Hasse-diagram Bellman distance transform matching the -8397 attaining canonical schedule.

## Gate Audit Summary
- **REPRODUCE (`panel/reproduce.md`)**: `pass: true` (recomputed objective of canonical schedule po_a010_t10_orig_b004_l1e-03.sol in exact rational arithmetic reproduces -8397 with risk=25950, return=-37218, transaction=3831, cash_interest=-990, short_cost=30, liquidation=0; all 5 Hasse-diagram Bellman inequalities verified across all 10,606 count states).
- **NOVELTY (`panel/novelty.md`)**: `pass: true` (live status checked against QOBLIB solutions/README.md; published incumbent -8397 has unproved global optimality; TROPHY_CASE.md contains no prior entry for this target; this work proves global optimality unconditionally).
- **CRITERION (`panel/criterion.md`)**: `pass: true` (exact integer objective -8397 accompanied by a complete checkable Bellman lower-bound optimality certificate meeting verbatim bank criteria).
- **Downgrade Checks**: Zero hedging, zero reproduction mismatches, zero stretched criteria, zero leaks. Final status is CONFIRMED_SOLUTION.
