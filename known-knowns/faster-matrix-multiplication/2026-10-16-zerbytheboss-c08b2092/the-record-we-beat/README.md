# The record we beat (metadata only)

Each row is one honest GET (Python `urllib.request`, User-Agent naming V3R1T4S, no retries) made by the author. No page is copied here.

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| tree.json | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-17T06:16:24Z | 200 | 0cb3669d76a7e34604a34d2a204c0bf4e27525ba5348675bea6605d7e7032fab | addition_reduced_ZT files for 2x5x6 rank 47: minimum cr 181 (2x5x6_m47_cr181_fv63_cn332_ZT_reduced.json) |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-17T06:16:24Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | no 2x5x6 rank-47 entry |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-17T06:16:24Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | 2x5x6 rank 47 listed; no lower addition count stated |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-17T06:16:24Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | no lower count for 2x5x6 |
| lille_2x5x6.html | https://fmm.univ-lille.fr/2x5x6.html | 2026-10-17T06:16:24Z | 200 | 30ed5cd77c8c3fc6f41935e706b9d4353bf06b2bcdd8f2c06eac34d97b3f3fd9 | rank 47; no operation-count variant cited |
| COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-17T06:16:24Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | 2x5x6: best 47, adds +332 (naive count, not comparable) |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-17T06:16:24Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | [2, 5, 6]: rank 47 |

Compared cell: 2x5x6 at rank 47, reduced additions. Reference (minimum over Perminov's files for this format and rank): 181 (and merged V3R1T4S PR #230 at 179). This object: 177.

## Reference scheme file (not shipped: third-party data)

https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x5x6_m47_cr181_fv63_cn332_ZT_reduced.json (sha256 `7a4e4cf9b1f925b865f97e1b1e1040bc7e91fb3711761fa14be12708be0ec10d`); running `verify-it-yourself/check_slp.py` on it reports 181 (`adds_U: 40, adds_V: 65, adds_W: 76`).

## V3R1T4S pull requests

Searched all open and closed pull requests of elder-plinius/V3R1T4S on 2026-10-17: merged PR #230 claims `<2,5,6>` rank 47 with 179 additions (`38 + 65 + 76`, keeping Perminov's `V` and `W` maps unchanged); by applying flip+isotopy moves to the bilinear basis together with Boyar-Peralta cancellation on `U`, `V`, and `W^T`, this package achieves **177** additions (`38 + 64 + 75`, 2 fewer than #230 and 4 fewer than Perminov's 181).
