# `C(40, 16, 7) <= 7,251` (`covering-designs-record`)

## What

An explicit (40,16,7) covering design object/design_40_16_7.txt (319,951 bytes, sha256 7db03ef01cd698f6764f590955f51732a64cd8a41dbe97efce69a6738d479985) with 7,251 blocks, exhaustively verified over all 18,643,560 7-subsets of a 40-set, strictly improving on the Covering Repository record of 7,470 and the La Jolla Covering Repository record of 7,470 for C(40,16,7) by 219 blocks.

- **Target:** `covering-designs-record` (`combinatorics-covering`)
- **Claim level:** `solution_claim` (`CONFIRMED_SOLUTION`)
- **Object file:** `object/design_40_16_7.txt` (`319,951` bytes, `7,251` lines, one $16$-subset of $\{1, \dots, 40\}$ per line)
- **SHA-256:** `7db03ef01cd698f6764f590955f51732a64cd8a41dbe97efce69a6738d479985`
- **Properties:** $7,251$ distinct blocks, $1$-minimal ($0$ redundant blocks; every block uniquely covers at least $6$ of the $7$-subsets), `uncovered = 0` across all $\binom{40}{7} = 18,643,560$ $7$-subsets, Schonheim lower bound $L(40, 16, 7) = 1,965 \le 7,251$.

## Check It Yourself

Run the standalone exhaustive checker from the root of this package (~4 seconds):

```sh
sh verify-it-yourself/run_checks.sh
```

It checks positive and negative Fano-plane controls ($C(7, 3, 2) = 7$), verifies block count, point range, distinctness, Schonheim lower bound, and exhaustive coverage of all $18,643,560$ $7$-subsets of $\{1, \dots, 40\}$, and prints `PASS` on its final line.

## Compared To

- **Covering Repository (`https://coveringrepository.com/download_archive_vkt.aspx`, fetched `2026-10-18T17:27:33Z`, `sha256: 6d317b207c4f582d7e913c4c7d6ebd0305407fdcd2dbb6de1901adf4f13a2704`):** `7,470` blocks (`40 16 07 07  7470`). Our design improves this upper bound by **$219$ blocks** ($-2.932\%$).
- **La Jolla Covering Repository (`https://dmgordon.org/covering-designs/`, fetched `2026-10-18T17:27:34Z`, `sha256: a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3`; Zenodo record `19735294`, v1.2, https://doi.org/10.5281/zenodo.19735294):** `7,470` blocks. Our design improves this upper bound by **$219$ blocks** ($-2.932\%$).

## Not Claimed

- We do not claim optimality ($C(40, 16, 7) = 7,251$); the Schonheim lower bound is $L(40, 16, 7) = 1,965$, so the exact minimum remains open in $[1,965, \, 7,251]$.
- This package claims only the single parameter triple $(v, k, t) = (40, 16, 7)$.

## Credits

- **Contributor:** `mizopl`
- **External data & literature:** Ingredient covering designs from Daniel M. Gordon's La Jolla Covering Repository (`https://dmgordon.org/covering-designs/`, Zenodo record `19735294`, v1.2, https://doi.org/10.5281/zenodo.19735294; not vendored here: `how-we-built-it/fetch_ingredients.py` downloads each one and checks it against the sha256 in `how-we-built-it/INGREDIENTS.tsv`); record table comparisons against G. Acerbi's Covering Repository (`https://coveringrepository.com`); combining framework generalizing Gordon, Kuperberg, and Patashnik (1995).
