# Live table values for 12x16x16 (metadata and short excerpts only)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the orchestrator. No whole third-party page is copied here.

| Source | URL | UTC fetch time | HTTP | sha256 |
|---|---|---|---|---|
| Perminov README | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-18T13:47:52Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 |
| Perminov repository tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-18T13:48:17Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 |
| MerlijnW70/fmm-schemes tree | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/HEAD?recursive=1 | 2026-10-18T13:48:19Z | 200 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-18T14:15:41Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 |

## Perminov README, table headed `Format | ZT rank | Z rank | Q rank` (verbatim header and row)

```
|   Format   |  `ZT` rank  |   `Z` rank   |   `Q` rank   |        ω        |
|:----------:|:-----------:|:------------:|:------------:|:---------------:|
| `12x16x16` |  1862 (?)   |   1862 (?)   | 1815 (1824)  | **2.803398069** |
```

Reading: ZT rank 1862 (?); Z rank 1862 (?); Q rank 1815 (1824). The first number in a cell is the current rank, a number in brackets is the best rank of previously known schemes, and `?` means none was recorded (the README's own legend). The claim in this folder is in the Z column, listed value 1862 (?); the claimed rank is 1830.

## Condition (3): minimum rank of existing scheme files for 12x16x16, any permutation of the dimensions

Searched: file names of the form {n}x{m}x{p}_m{rank}_{CLASS}.json whose sorted dimensions equal 12, 16, 16, in the saved trees above. Only the rank in the file name was used; the files were not downloaded.

Perminov, schemes/results/ZT, schemes/results/Z and schemes/results/Q:

| Class | Minimum rank | File(s) at the minimum |
|---|---|---|
| ZT | 1862 | schemes/results/ZT/12x16x16_m1862_ZT.json |
| Z | no file | - |
| Q | 1815 | schemes/results/Q/12x16x16_m1815_Q.json |

All matching files in Perminov's schemes/results tree:
- rank 1815, Q: schemes/results/Q/12x16x16_m1815_Q.json
- rank 1862, ZT: schemes/results/ZT/12x16x16_m1862_ZT.json

MerlijnW70/fmm-schemes (schemes/ folder; every file there is ZT):

| Class | Minimum rank | File(s) at the minimum |
|---|---|---|
| ZT | no file | - |
| Z | no file | - |
| Q | no file | - |

All matching files in MerlijnW70/fmm-schemes:
- none

## Best rank in fmm_sota.json

Entries for format 12x16x16 (sorted dimensions): ranks [1815]. Best (minimum): 1815.
