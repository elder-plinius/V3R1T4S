# How We Found It

_Note: contributor text, unverified._

## Brief & Scouting Insight
Before running any search, our literature scout uncovered three crucial 2026 results:
1. Spogreev (Oct 2026, Zenodo `10.5281/zenodo.23113159`) proved `K_5 + C_8^2` is biplanar with fractional chromatic number `chi_f = 9`, raising the true `p1` threshold from `8.5` to `> 9` (which forces `chi >= 10`).
2. Doria (Aug 2026) and Patil (Aug 2026) showed `n <= 16` biplanar graphs are 9-colorable, and Szeider (Sep 2026, `arXiv:2609.28102`) proved all `alpha <= 2` biplanar graphs are 9-colorable and have `n <= 18`.
3. Across all published 9-critical biplanar lists — Sulanke (`n = 11`), Boutin–Gethner–Sulanke 2008 (`n = 12..16`), Gethner–Sulanke 2009 / Alalqam 2012 (`n <= 17`), and Patil 2026 Hajós sums (`n >= 21`) — orders `n = 18, 19` lay completely unpopulated, and `n = 19` is strictly below the smallest possible Hajós sum (`11 + 11 - 1 = 21`) or Ore composition (`20`) of smaller 9-critical biplanar graphs.

## What Failed (`full` & `p1`)
We built two C99 Wagner diagonal-flip engines maintaining exact sphere triangulations `(T_0, T_1)` in `O(1)` time per flip via L1-cached opposite-vertex tables (`~18.5M` flips/s per thread):
- Over `11.1` billion Iterated Local Search (ILS) flips across `n = 22..30` minimizing 4-independent-set counts (`i_4`) and `23.8` million direct Bron–Kerbosch + Multiplicative-Weights Dual-LP evaluations across `n = 19..28`, `chi_f` never exceeded `9.0` and all `1,520` `DSATUR >= 10` candidates were 9-colorable.
- Over `4.65` billion flips on `n = 18` targeting Gethner–Sulanke Open Problem 2 (`alpha = 2`, i.e. `i_3 = 0`), the minimum number of complement triangles plateaued at `i_3 = 2`.

## What Worked (`p2`)
Naively searching for 9-chromatic biplanar graphs on `n = 19` collapses to padded 11- to 14-vertex cores when peeling edges. We solved this by introducing an exact discrete gradient `bad_v = #{v : chi(G - v) == 9}` inside the C99 Wagner flip loop (using fast bitmask clique-fixed 8-coloring) while penalizing universal vertices so `overline(G)` stays connected. Driving `bad_v -> 0` on `n = 19` immediately produced spanning vertex-9-critical triangulation unions, whose edge-peeled 9-critical cores include our 5-connected, 92-edge graph (`degrees 8..12`, `alpha = 3`, `0` clique cutsets).
