# `C(68, 14, 5) <= 15,675` (`covering-designs-record`)

## What

An explicit (68,14,5) covering design with 15,675 blocks (sha256 2b72790b8149daebd293b91cddae0105bc2a19b798b414d405e66f81828bcf07), exhaustively verified over all 10,424,128 5-subsets of a 68-set, strictly improving on the Covering Repository record of 16,004 and the La Jolla Covering Repository record of 16,004 for C(68,14,5).

- **Target:** `covering-designs-record` (`combinatorics-covering`)
- **Claim level:** `solution_claim` (`CONFIRMED_SOLUTION`)
- **Object file:** `object/design_68_14_5.txt` (`632,514` bytes, `15,675` lines, one $14$-subset of $\{1, \dots, 68\}$ per line)
- **SHA-256:** `2b72790b8149daebd293b91cddae0105bc2a19b798b414d405e66f81828bcf07`
- **Properties:** $15,675$ distinct blocks, $1$-minimal ($0$ redundant blocks; every block uniquely covers at least $6$ of the $5$-subsets), `uncovered = 0` across all $\binom{68}{5} = 10,424,128$ $5$-subsets, Schonheim lower bound $L(68, 14, 5) = 5,785 \le 15,675$.

## Check It Yourself

Run the standalone exhaustive checker from the root of this package (~3 seconds):

```sh
sh verify-it-yourself/run_checks.sh
```

It checks positive and negative Fano-plane controls ($C(7, 3, 2) = 7$), verifies block count, point range, distinctness, Schonheim lower bound, and exhaustive coverage of all $10,424,128$ $5$-subsets of $\{1, \dots, 68\}$, and prints `PASS` on its final line.

## Compared To

- **Covering Repository (`https://coveringrepository.com/download_archive_vkt.aspx`, fetched `2026-10-18T10:33:16Z`, `sha256: f02f5fc233aa66ca835b8f0b1b4d751fd35ad721c5264043ceb515ee95da9277`):** `16,004` blocks (`68 14 05 05  16004`). Our design improves this upper bound by **$329$ blocks** ($-2.06\%$).
- **La Jolla Covering Repository (`https://dmgordon.org/covering-designs/`, fetched `2026-10-18T10:33:20Z`, `sha256: a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3`; Zenodo `19472830` / v1.2 `19735294`):** `16,004` blocks. Our design improves this upper bound by **$329$ blocks** ($-2.06\%$).

## Not Claimed

- We do not claim optimality ($C(68, 14, 5) = 15,675$); the Schonheim lower bound is $L(68, 14, 5) = 5,785$, so the exact minimum remains open in $[5,785, \, 15,675]$.
- This package claims only the single parameter triple $(v, k, t) = (68, 14, 5)$.

## Credits

- **Contributor:** `mizopl`
- **External data & literature:** Ingredient covering designs from Daniel M. Gordon's La Jolla Covering Repository (`https://dmgordon.org/covering-designs/`, Zenodo `19472830`); record table comparisons against G. Acerbi's Covering Repository (`https://coveringrepository.com`); combining framework generalizing Gordon, Kuperberg, and Patashnik (1995).
