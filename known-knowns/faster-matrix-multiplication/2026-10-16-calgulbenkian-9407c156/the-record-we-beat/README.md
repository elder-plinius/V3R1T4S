# The record we beat (metadata only)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the author. No page is copied here.

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| tree.json | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T11:55:16Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | addition_reduced_ZT files for 3x5x5 rank 58: ['3x5x5_m58_cr221_cn357_ZT_reduced.json']; minimum cr 221 |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-15T09:46:09Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | 3x5x5-58: {'Z': 326, 'Z2': 255} |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:44:30Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | no lower count for this format and rank stated |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T09:44:31Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | no lower count for this format and rank stated |
| lille_3x5x5.html | https://fmm.univ-lille.fr/3x5x5.html | 2026-10-15T22:25:31Z | 200 | be33b9a99092ed2cec4c4d39f3bdbb2c62bd272885668be05e04d0303fee406a | rank 58; Commentaries section present: False |
| COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T09:44:32Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | adds column is a naive count (nz(U)+nz(V)+nz(W)-2r-np), not comparable; no cell below the reduced counts |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T11:55:17Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | [3, 5, 5]: rank 58 |

Compared cell: 3x5x5 at rank 58, reduced additions. Reference (minimum over Perminov's files for this format and rank): 221. This object: 211.

## Reference scheme file (not shipped: third-party data)

The reference count comes from Perminov's file https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/3x5x5_m58_cr221_cn357_ZT_reduced.json (sha256 of the copy the author fetched on 2026-10-15: 17cdcab30fdacdaf92464bbfd7ff135a1d39fada357114d400586e8cad1dcd9e). Its expanded U, V and W rows are the same products as this object's; only the straight-line programs differ. To recount the reference, download it and run verify-it-yourself/check_slp.py on it; the author's counter reproduces its cr value.

## Other sources compared (read by the author, not copied here)

| Source | What it says for 3x5x5 at rank 58 | Our value |
|---|---|---|
| Perminov, arXiv:2512.13365 Table 1 | 221 (same convention) | 211 |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 (PDF sha256 c095482d4bc6a410171092bc6b37ef4e2a1d07808c076149f0f183704fbff3d6, downloaded by hand after an automated fetch met a challenge page) | lowest count listed for 355-58: 222 over Z (Table 3.3); 220 over Z2 (Table 3.6, not comparable; below the reference 221, above our 211); author's reading of a hand-downloaded PDF | 211 |
| V3R1T4S open pull requests on this target | none | 211 |
| V3R1T4S TROPHY_CASE.md | no row for this target | 211 |

The panel's novelty skeptic fetched every primary page again on 2026-10-15 (times and sha256 in panel/novelty.md); all pages
matched the author's record.

## Re-fetched by the author before filing

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| Perminov repository tree, re-fetched by the author before filing | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-16T02:30:40Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | addition_reduced_ZT files for 3x5x5 rank 58: 1 file(s), minimum cr 221; unchanged |
| fmm_sota.json, re-fetched by the author before filing | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-16T02:30:43Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | 3x5x5: rank 58, unchanged |
