# Internal Verification Gate — `qoblib-portfolio-ten-assets-exact`

status: CONFIRMED_SOLUTION
confirmed_scope: Globally optimal integer position schedule for QOBLIB instance po_a010_t10_orig_b004_l1e-03 with objective -8397, certified by a complete 10,606-state two-pass Hasse-diagram Bellman distance transform matching the published -8397 schedule.

## Verification Summary
- **REPRODUCE (`panel/reproduce.md`)**: Recomputed objective of the published schedule `po_a010_t10_orig_b004_l1e-3.bst.sol` (`https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3.bst.sol`, SHA-256 `d0cb3e4a86d01ac2b2884e3275df8219bb1d38dae908830784417b0d4e4b30ea`) in exact rational arithmetic reproduces `-8397` (`risk=25950`, `return=-37218`, `transaction=3831`, `cash_interest=-990`, `short_cost=30`, `liquidation=0`); all 5 Hasse-diagram Bellman equations and inequalities verified across all 10,606 count states.
- **NOVELTY (`panel/novelty.md`)**: Live status checked against QOBLIB `06-portfolio/solutions/README.md`; published incumbent `-8397` is listed as `best known` with Gurobi numerical MIP bound `-15342.65126758` after `3600.03 s`; this certificate establishes global optimality at `-8397`.
- **CRITERION (`panel/criterion.md`)**: Exact integer objective `-8397` accompanied by a complete checkable Bellman lower-bound optimality certificate meeting the target criterion.
