# Prospective Preregistration (`hadamard-maxdet-records`)

- `target_id`: `hadamard-maxdet-records`
- `frozen_utc`: `2026-11-11T00:05:00Z`
- `direction`: `max` (`D_norm = |det(X)| / 2^(n-1)` for `X in {-1, +1}^(n x n)`)
- `open_scope`: Orders `23 <= n <= 119` (`n not divisible by 4`) whose best known determinant in W. P. Orrick's archived MaxDet catalog, G. Butbaia et al. (`arXiv:2608.22518v3` / `Math-AI-Caltech/hadamard-maxdet`), and merged `V3R1T4S` claims lies strictly below the residue-class upper bound (Barba for `n = 1 mod 4`, Ehlich-Wojtas for `n = 2 mod 4`, piecewise Ehlich `s`-block bound for `n = 3 mod 4`).
- `acceptance_rule`: Explicit `n x n` `{+1, -1}` matrix verified by fraction-free Bareiss integer elimination, independent multi-prime Chinese Remainder Theorem determinant computation, and `sympy.Matrix.det(method='bareiss')` to satisfy `D_norm > max(literature_record, live_v3r1t4s_record)` and `|det(X)|^2 <= B_class(n)^2`.
