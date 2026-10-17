# How we found it

Contributor text, unverified.

An agent working for the contributor started from Perminov's rank-47 `<2,5,6>` scheme (`2x5x6_m47_cr181_fv63_cn332_ZT_reduced.json`, 181 reduced additions). It walked the space of rank-47 ternary schemes using flip-graph moves combined with ternary-preserving isotopy moves (elementary row and column additions/subtractions on the three factor matrices `U`, `V`, `W`), coupled with Boyar-Peralta cancellation-guided common-subexpression elimination on `U`, `V`, and `W^T` (transposed back via the transposition principle `cost(W) = cost(W^T) + r - n*p`) and canonical binary DAG exclusive-cone reduction (`dag_cone_collapse.py`), reaching **177** reduced additions (`U 38 + V 64 + W 75 = 177`).

Before claiming, Perminov's live tree listing, `reduced_known.json`, `README.md`, `CHANGELOG.md`, the Lille `<2,5,6>` page, `COVERAGE.md`, and `fmm_sota.json` were fetched once each, and all open and closed pull requests of this repository were checked.
