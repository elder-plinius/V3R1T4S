# How We Found It

*Contributor text, unverified.*

## Why `(b = 3, m = 11, s = 19)` Was Open in MinT

Inspecting MinT's `desc_OBoundLP.html` revealed that MinT's Martin-Stinson / Bierbrauer linear-programming lower bounds for `OOA(M, s, S_b, T, k)` were precomputed only up to `s <= 8` when `T = 4` (and, for `k <= 20`, `s <= 15` when `T = 3`), leaving `(b = 3, m = 11, s = 19)` at `t >= 3` while the digital lower bound already stood at `t >= 4`.

## Exact Depth-4 Dual LP Extraction

Evaluating the `8,855` agreement shapes of `OOA(M, 19, S_3, T = 4, k = 8)` (`k = m - t = 8`) and solving a restricted dual LP over `60` dual types (`1 <= |f| <= 11`), followed by exact rationalization over a 62-bit common integer denominator `L = 3,554,572,650,025,767,480`, yielded `M >= 177,478.655491... > 177,147 = 3^11`.
