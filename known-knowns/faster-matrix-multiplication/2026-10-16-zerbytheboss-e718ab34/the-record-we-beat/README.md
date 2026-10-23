# The record we beat (metadata only)

Each row is one honest GET (Python `urllib.request`, User-Agent naming V3R1T4S, no retries) made by the author. No page is copied here.

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| tree.json | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-17T05:18:50Z | 200 | 0cb3669d76a7e34604a34d2a204c0bf4e27525ba5348675bea6605d7e7032fab | addition_reduced_ZT file for 2x4x7 rank 45: single file 2x4x7_m45_cr174_cn308_ZT_reduced.json (cr 174); minimum 174 |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-17T05:18:51Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | no 2x4x7 (or permutation) entry |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-17T05:18:51Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | 2x4x7 rank 45 listed; no lower addition count stated |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-17T05:18:51Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | no lower count for 2x4x7 |
| lille_2x4x7.html | https://fmm.univ-lille.fr/2x4x7.html | 2026-10-17T05:18:52Z | 200 | 3d668f206f15825f65def9e7cfe3c4982ddc524817e2f702eb6fd485bbb059d3 | rank 45 (cites AlphaEvolve, Novikov et al. May 2025, arXiv:2506.13131); no operation-count variant cited |
| COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-17T05:18:53Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | 2x4x7: best 45, adds +308 (naive count, not comparable) |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-17T05:18:53Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | [2, 4, 7]: rank 45 |

Compared cell: 2x4x7 at rank 45, reduced additions. Reference (minimum over Perminov's files for this format and rank): 174 (and open V3R1T4S PR #229 at 169). This object: 161.

## Reference scheme file (not shipped: third-party data)

https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x4x7_m45_cr174_cn308_ZT_reduced.json (sha256 `b839eb6e30cfd9e0b045d249dfdacfd832ad2d7a5770f6a8d88c29f6ff486e84`); running `verify-it-yourself/check_slp.py` on it reports 174 (`adds_U: 35, adds_V: 69, adds_W: 70`).

## V3R1T4S pull requests

Searched all open and closed pull requests of elder-plinius/V3R1T4S on 2026-10-17: open PR #229 claims `<2,4,7>` rank 45 with 169 additions; this package achieves 161 additions (8 fewer than #229 and 13 fewer than the live table's 174) and was invited as its own package by the maintainer on PR #241.
