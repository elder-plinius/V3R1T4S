# How we found it

Contributor text, unverified.

An agent working for the contributor started from Perminov's rank-45 `<2,4,7>` scheme (`2x4x7_m45_cr174_cn308_ZT_reduced.json`, 174 reduced additions). It walked the space of rank-45 schemes using flip-graph moves combined with ternary-preserving isotopy moves (elementary row and column additions/subtractions on the three factor matrices `U`, `V`, `W`), invoking Perminov's `ternary_addition_reducer` after candidate moves to reach 167 reduced additions (`U 35 + V 61 + W 71`). Finally, converting the straight-line program for `V` into a canonical binary DAG and applying an exact exclusive-cone 2-sum rewrite (`dag_cone_collapse.py`) eliminated one additional intermediate node in `V` (`v_fresh` reduced from 38 to 37 while keeping 23 output additions), lowering the total reduced addition count to **161** (`U 35 + V 58 + W 68 = 161`).

Before claiming, Perminov's live tree listing, `reduced_known.json`, `README.md`, `CHANGELOG.md`, the Lille `<2,4,7>` page, `COVERAGE.md`, and `fmm_sota.json` were fetched once each, and all open and closed pull requests of this repository were checked (open PR #229 claims 169 additions on `<2,4,7>` rank 45; our 161-addition scheme is 3 additions lower, and the maintainer invited a separate package in PR #241).
