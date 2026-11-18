# Pre-Registration: `mint-net-below-digital-bound`

frozen_utc: 2026-11-17T15:25:37Z
target_id: mint-net-below-digital-bound
null_test: not needed because exact rational dual LP certificate verified across all 8855 primal agreement types

## Verbatim Gates (Partial Win `p1`)

1. Live MinT query page (`query.php?b=3&s=19&m=11&p=smt`) displays `Lower bound on t: 3` strictly below `Lower bound on t (digital): 4`.
2. Exact rational dual solution `u_f` for the embedded `OOA(M, 19, S_3, T = 4, k = 8)` satisfying `u_f <= 0` for `|f| >= 9`, `1 + sum_f u_f K_f(X) >= 0` across all `8,854` non-diagonal shapes `X`, and `1 + sum_f u_f K_f(0, 0, 0, 0, 19) > 3^11 = 177,147`, verified independently in Python `Fraction` and C99 `__int128`.
