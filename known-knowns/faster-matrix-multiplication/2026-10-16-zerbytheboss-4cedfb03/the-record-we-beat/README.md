# The record we beat (metadata only)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the author. No page is copied here.

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| tree.json | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-16T17:43:11Z | 200 | 0cb3669d76a7e34604a34d2a204c0bf4e27525ba5348675bea6605d7e7032fab | addition_reduced_ZT files for 3x4x4 rank 38: cr 125 (3x4x4_m38_cr125_cn224_ZT_reduced.json) and cr 133 (3x4x4_m38_cr133_cn194_ZT_reduced.json); minimum 125 |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-16T17:43:13Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | 3x4x4-38: Z 198, Z2 166 (a different, non-reduced-count measure; not comparable) |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-16T17:43:13Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | 3x4x4 rank 38 listed; no lower addition count stated |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-16T17:43:13Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | mentions the cr125 file; no lower count |
| lille_3x4x4.html | https://fmm.univ-lille.fr/3x4x4.html | 2026-10-16T17:43:13Z | 200 | 08ad36fbf18ee1c3d1acef1e81e2c66f16f1b44c4035dd0d2853bd30ee2f7730 | rank 38; no addition-count variant cited |
| COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-16T17:43:14Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | 3x4x4: best 38, adds +216 (naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable) |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-16T17:43:15Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | [3, 4, 4]: rank 38 |

Compared cell: 3x4x4 at rank 38, reduced additions. Reference (minimum over Perminov's files for this format and rank): 125. This object: 124.

## Reference scheme file (not shipped: third-party data)

https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/3x4x4_m38_cr125_cn224_ZT_reduced.json ; running verify-it-yourself/check_slp.py on it reports 125.

## V3R1T4S pull requests

Searched all open and closed pull requests of elder-plinius/V3R1T4S on 2026-10-16: none claims 3x4x4 (or a permutation); #173 (<6,8,8>) mentions 3x4x4:38 only as a Kronecker factor.
