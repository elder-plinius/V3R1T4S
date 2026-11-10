# Pre-Registration — `mint-linear-ooa-depth-2-to-8`

- `target_id`: `mint-linear-ooa-depth-2-to-8`
- `frozen_utc`: `2026-11-10T18:10:00Z`
- `cell`: `(b, T, m, s) = (3, 2, 8, 8)` over prime field `F_3 = {0, 1, 2}`
- `criterion`: Explicit `8 x 16` matrix over `F_3` grouped into `s = 8` blocks of `T = 2` columns whose strength `k` (checked exhaustively across all `1,016` left-justified selections `(d_1, ..., d_8)` in `{0, 1, 2}^8` with `d_1 + ... + d_8 = 7` having rank `7` over `F_3`) is strictly greater than `m - t_live = 8 - 2 = 6` (`k = 7 > 6`, `k > T = 2`), matching MinT's generalized Rao/Hamming lower bound `t >= 1` (`k <= 7`).
- `null_test`: `not needed because exact finite-field matrix rank over F_3 across all 1016 left-justified selections is a deterministic algebraic property`
