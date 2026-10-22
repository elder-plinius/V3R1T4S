# The record we beat (metadata only)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the author. No page is copied here.

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| tree.json | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T11:55:16Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | addition_reduced_ZT files for 2x5x5 rank 40: ['2x5x5_m40_cr153_cn283_ZT_reduced.json']; minimum cr 153 |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-15T09:46:09Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | 2x5x5-40: {'Z': 313, 'Z2': 218} |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:44:30Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | no lower count for this format and rank stated |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T09:44:31Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | no lower count for this format and rank stated |
| lille_2x5x5.html | https://fmm.univ-lille.fr/2x5x5.html | 2026-10-15T22:25:36Z | 200 | b1284cd181e11906ca3da9dbf7af7bc64f00eabc5a1b807111a8968c7608bcc4 | rank 40; Commentaries section present: False |
| COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T09:44:32Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | adds column is a naive count (nz(U)+nz(V)+nz(W)-2r-np), not comparable; no cell below the reduced counts |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T11:55:17Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | [2, 5, 5]: rank 40 |

Compared cell: 2x5x5 at rank 40, reduced additions. Reference (minimum over Perminov's files for this format and rank): 153. This object: 147.

## Reference scheme file (not shipped: third-party data)

The reference count comes from Perminov's file https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x5x5_m40_cr153_cn283_ZT_reduced.json (sha256 of the copy the author fetched on 2026-10-15: 89296c6dd94e052ca7cb517fa4d59b8a1dc335dc08c7dfc73edb420bba0c1bab). Its expanded U, V and W rows are the same products as this object's; only the straight-line programs differ. To recount the reference, download it and run verify-it-yourself/check_slp.py on it; the author's counter reproduces its cr value.

## IACR ePrint 2026/849 (Martensson and Stankovski Wagner), read by the author

The PDF refuses automated download (Cloudflare challenge). The operator downloaded it by hand on 2026-10-15; the author read it (sha256 c095482d4bc6a410171092bc6b37ef4e2a1d07808c076149f0f183704fbff3d6). Its counts are additions of straight-line programs without change of basis, over Z (Tables 3.1 to 3.4, comparable) or over Z2 (Tables 3.5 and 3.6, not comparable). Rows for the scheme code 255-40: 255-40       283         156        154          0.29, 0, 0         156; 255-40        682        323         313      369    54.1       0.1, 0.12, 0.06; 255-40     546            226       218      328     60.1    0.135, 0.005, 0.055; 255-40          256      148       144     112   43.8    0.28, 0, 0.01. The paper's best Z count for any scheme it lists for this format is above 153; nothing in it is below this object's 147.

## Other sources compared (read by the author, not copied here)

| Source | What it says for 2x5x5 at rank 40 | Our value |
|---|---|---|
| Perminov, arXiv:2512.13365 Table 1 | 153 (same convention) | 147 |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 (PDF sha256 c095482d4bc6a410171092bc6b37ef4e2a1d07808c076149f0f183704fbff3d6, downloaded by hand after an automated fetch met a challenge page) | lowest count listed for 255-40: 154 over Z (Table 3.3); 144 over Z2 (Table 3.6, a scheme with naive count 256, not comparable; below the reference 153 and below our 147, which is over Z); author's reading of a hand-downloaded PDF | 147 |
| V3R1T4S open pull requests on this target | none | 147 |
| V3R1T4S TROPHY_CASE.md | no row for this target | 147 |

The panel's novelty skeptic fetched every primary page again on 2026-10-15 (times and sha256 in panel/novelty.md); all pages
matched the author's record.

## Re-fetched by the author before filing

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| Perminov repository tree, re-fetched by the author before filing | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-16T02:30:40Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | addition_reduced_ZT files for 2x5x5 rank 40: 1 file(s), minimum cr 153; unchanged |
| fmm_sota.json, re-fetched by the author before filing | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-16T02:30:43Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | 2x5x5: rank 40, unchanged |
