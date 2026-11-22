# Live table values for 11x14x16 (metadata and short excerpts only)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made for the contributor. No whole third-party page is copied here.

| Source | URL | UTC fetch time | HTTP | sha256 |
|---|---|---|---|---|
| Perminov `docs/ranks.md` (live rank table) | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 2026-10-26T16:55:46Z | 200 | e71786dda6669d49fb1af448046cd294d7246977ba5372eeab5f536bf58dcbe4 |
| Perminov `CHANGELOG.md` | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-26T16:55:45Z | 200 | 2423783b98fe1d364d40244cb29eae5fb089d47914525b1d91cc832fdccad582 |
| Perminov `schemes/results/Z/11x14x16_m1540_Z.json` | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/Z/11x14x16_m1540_Z.json | 2026-10-26T16:56:03Z | 200 | c67ebf468faa3baa93d8058f8eee7fed2b699ccc11c43d9e1c4385f0599689fe |
| Perminov repository tree, again | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-26T16:56:59Z | 200 | 892c1d6ab1fab01d905e49a91b93628f791e894492f08495f7fc14617b75677d |
| Perminov README (dated note, 2026-10-18) | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-18T13:47:52Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 |
| Perminov repository tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-18T13:48:17Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 |
| MerlijnW70/fmm-schemes tree | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/HEAD?recursive=1 | 2026-10-18T13:48:19Z | 200 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-18T14:15:41Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 |

## Perminov `docs/ranks.md`, fetched 2026-10-26T16:55:46Z (verbatim header and row)

```
|   Format   |  `ZT` rank  |   `Z` rank   |   `Q` rank   |        ω        |
|:----------:|:-----------:|:------------:|:------------:|:---------------:|
| `11x14x16` |  1550 (?)   |   1540 (?)   | 1520 (1571)  |   2.814428649   |
```

This is the live comparator. The page says the best ranks of previously known schemes are given in brackets; `(?)` means none is listed. The claim is in the ZT column, current value 1550; the claimed rank is 1547.

The Z cell was 1550 when the claim was filed. It became 1540 on 25/10/2026: Perminov's `CHANGELOG.md` entry for that date lists `11x14x16`: found scheme `schemes/results/Z/11x14x16_m1540_Z.json` with `1540` multiplications, under "Integer ring improvement (`Z`)". The ZT cell did not change, and his entry lists no ZT scheme for this format. 13 of the 1540 terms of his scheme have a coefficient of 2, so splitting it into ternary terms gives 1553.

## Dated note: Perminov README on 2026-10-18, table headed `Format | ZT rank | Z rank | Q rank` (verbatim header and row)

On 2026-10-18 the table was in the README. It has since moved to `docs/ranks.md`; the ZT and Q cells are unchanged, and the Z cell is now 1540 (see above).

```
|   Format   |  `ZT` rank  |   `Z` rank   |   `Q` rank   |        ω        |
|:----------:|:-----------:|:------------:|:------------:|:---------------:|
| `11x14x16` |  1550 (?)   |   1550 (?)   | 1520 (1571)  |   2.814428649   |
```

Reading: ZT rank 1550 (?); Z rank 1550 (?); Q rank 1520 (1571). The first number in a cell is the current rank, a number in brackets is the best rank of previously known schemes, and `?` means none was recorded (the README's own legend). The claim in this folder is in the ZT column, listed value 1550 (?); the claimed rank is 1547.

## Condition (3): minimum rank of existing scheme files for 11x14x16, any permutation of the dimensions

Searched: file names of the form {n}x{m}x{p}_m{rank}_{CLASS}.json whose sorted dimensions equal 11, 14, 16, in the saved trees above. Only the rank in the file name was used; the files were not downloaded.

Perminov, schemes/results/ZT, schemes/results/Z and schemes/results/Q:

| Class | Minimum rank | File(s) at the minimum |
|---|---|---|
| ZT | 1550 | schemes/results/ZT/11x14x16_m1550_ZT.json |
| Z | no file | - |
| Q | 1520 | schemes/results/Q/11x14x16_m1520_Q.json |

All matching files in Perminov's schemes/results tree:
- rank 1520, Q: schemes/results/Q/11x14x16_m1520_Q.json
- rank 1521, Q: schemes/results/Q/11x14x16_m1521_Q.json
- rank 1528, Q: schemes/results/Q/11x14x16_m1528_Q.json
- rank 1530, Q: schemes/results/Q/11x14x16_m1530_Q.json
- rank 1548, Q: schemes/results/Q/11x14x16_m1548_Q.json
- rank 1550, ZT: schemes/results/ZT/11x14x16_m1550_ZT.json
- rank 1564, ZT: schemes/results/ZT/11x14x16_m1564_ZT.json

MerlijnW70/fmm-schemes (schemes/ folder; every file there is ZT):

| Class | Minimum rank | File(s) at the minimum |
|---|---|---|
| ZT | no file | - |
| Z | no file | - |
| Q | no file | - |

All matching files in MerlijnW70/fmm-schemes:
- none

Perminov tree fetched again at 2026-10-26T16:56:59Z: the same seven files, plus one new Z file.

| Class | Minimum rank | File(s) at the minimum |
|---|---|---|
| ZT | 1550 | schemes/results/ZT/11x14x16_m1550_ZT.json |
| Z | 1540 | schemes/results/Z/11x14x16_m1540_Z.json |
| Q | 1520 | schemes/results/Q/11x14x16_m1520_Q.json |

## Best rank in fmm_sota.json

Entries for format 11x14x16 (sorted dimensions): ranks [1520]. Best (minimum): 1520.
