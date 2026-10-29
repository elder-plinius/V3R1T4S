# The record we beat

## The VarBench table (status source)

| UTC fetch | HTTP | URL | sha256 of the bytes |
|---|---|---|---|
| 2026-10-23T15:07:57Z | 200 | https://github.com/varbench/varbench | b0dc3fbcd837342aa75a77e9fc54ba2e905ad7038e91aaa0ccf9a430e81de339 |
| 2026-10-23T15:07:59Z | 200 | https://api.github.com/repos/varbench/varbench/commits?per_page=3 | f9fc2aea136af39b5572f2d24baff0f26ba36e0bb4ac88dddb5ed4b983f04aeb |
| 2026-10-23T15:08:00Z | 200 | https://raw.githubusercontent.com/varbench/varbench/main/J1J2/square_100_P_0.9.md | 0d0e85250570199179a9696a8ab8e71292b99993788ab492f64039b5d8c5a34d |
| 2026-10-23T15:08:01Z | 200 | https://raw.githubusercontent.com/varbench/varbench/main/lattice.md | aca652ddf56420491618a353d95dcf9c1eebf0fe61a14ab187e541a8c2addf20 |
| 2026-10-23T15:08:01Z | 200 | https://raw.githubusercontent.com/varbench/varbench/main/J1J2/square_16_P_0.5.md | 9335cb7bd71564a67195aba96575dc30cc393dee62446396d98223b8437a8650 |

Extracted rows of J1J2/square_100_P_0.9.md (Pauli convention; varbench/varbench last commit 390a21eab7eb,
2024-10-22T08:50:50Z): DMRG (bond dimension = 1024) -250.78657331066935 (energy variance 42.34801436871931);
RBM (alpha = 1) -238.966 (sigma 0.013); Jastrow baseline -235.905 (sigma 0.010).

## The lowest published variational energy for the identical system (the bar)

Golubev, Iakovlev and Mazurenko, arXiv:2606.04558v2, Table I, row J2 = 0.90, column "10 x 10, ViT (this work)":
-0.634170 per site (H = J1 sum S.S + J2 sum S.S, periodic, N = 100), i.e. -253.668 in Pauli units; no error bar printed.
PDF fetched 2026-10-22T16:49:41Z from https://arxiv.org/pdf/2606.04558v2 (HTTP 200), sha256 9064b3c7893c4e6692524eb19fc2ef73b82e04096b5c4431664c5030da414f19.
Literature searches of 2026-10-22 and 2026-10-23 and the panel's NOVELTY search found nothing lower (panel/novelty.md).
