# How We Found It

_Note: contributor text, unverified._

## Brief

We targeted `mint-linear-ooa-depth-2-to-8` in the unexplored ternary (`b = 3`, prime field `F_3`) depth `T = 2` table of MinT (`http://mint.sbg.ac.at/table.php?i=x&b=3&col=1&mode=cd&opt=bd&de=2&p=smt&minx=1&maxx=20&miny=0&maxy=15`). For `(m, s) = (8, 8)`, MinT's constructive linear entry is `t = 2` (`k = 6`), coming from the extended genus-2 algebraic-geometric NRT code `AG_e(2; F, 9P)` over `F_3`, whereas the generalized Rao / dual Hamming lower bound on `t` is `t >= 1` (`k <= 7`, since the ordered sphere volume `7,457 > 3^8 = 6,561`).

## What Failed First

1. An initial exhaustive non-randomized DFS run (`exhaustive_if_small = 1` with `20,000,000` node cap) spent over `60` seconds exploring the earlier `(m, s, k) = (6, 8, 5)` gap cell before reaching `(8, 8, 7)`.

## What Worked

1. In `how-we-built-it/search_ooa_f3.c`, we precomputed the `6,561 x 6,561` addition table of `F_3^8`, fixed the canonical `GL_8(F_3)` basis prefix across blocks `0..2` (`[e_{2i}, e_{2i+1}]`) and block `3`'s first column (`e_6`), pruned projective scalar multiples `{1, 2}` in `F_3^*` (since scaling either column `u` or `v` by `2 mod 3` preserves both `span(u)` and `span(u, v)`), and maintained the exact minimum left-justified selection cost `dp_stack[blk][x]` for every vector `x in F_3^8`.
2. Switching to bounded randomized-restart DFS (`8,000` nodes per restart with deterministic Xorshift64 seed `0x9e3779b97f4a7c15ULL`) skipped past `(6, 8, 5)` in `< 1` second and found an explicit `OOA(3^8, 8, F_3, 2, 7)` at `(m, s, k) = (8, 8, 7)` on restart `10` in under `2` seconds total runtime.
3. Exhaustive verification confirmed rank `7` over `F_3` on all `1,016` left-justified selections `(d_1, ..., d_8)` in `{0, 1, 2}^8` with `sum d_i = 7`, and confirmed minimum Rosenbloom-Tsfasman weight `d_RT = 8` across all `6,560` nonzero codewords of its Euclidean dual `[(8, 2), 8, 8]`-NRT code.
