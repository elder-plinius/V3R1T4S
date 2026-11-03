# Spherical code: 365 points in dimension 7 (Cohn's table row d=7, N=365)

## What

In dimension 7, a code of 365 unit vectors whose largest pairwise inner product, computed at 50 significant digits over all pairs, is 0.670467035142, which is 2.034e-7 below the live /plain cosine 0.670467238587 of the (7, 365) row of Henry Cohn's table. The row is not marked proven optimal and does not carry the "needs more optimization" label; no row with more points in dimension 7 has a cosine at or below this value.

The object is `object/7x365.txt` (365 lines, 7 comma-separated coordinates each), listed with its sha256 in `INDEX.csv`. The package identifier uses the first 8 hex digits of that file's sha256 (fcb7516bada8a9fe8aee81aca8579d82f739661f0d91e4397cf2bd0804e7cf37).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: under ten seconds.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Henry Cohn, spherical-codes.org `/plain` | d=7, N=365 | 0.670467238587 | https://spherical-codes.org/plain | 2026-11-03T18:04:22Z |
| Henry Cohn, spherical-codes.org HTML index | d=7, N=365 | 0.670467238587; no proven-optimal mark, no "needs more optimization" label; credited to Antoine Jay, 2026 | https://spherical-codes.org/ | 2026-11-03T18:04:23Z |
| Henry Cohn, spherical-codes.org `/plain` | d=7, N > 365 | no row at or below 0.670467035142 (N = 366 reads 0.670923693486) | https://spherical-codes.org/plain | 2026-11-03T18:04:22Z |

Page hashes and the saved rows: `the-record-we-beat/README.md`. Our value to 20 digits: 0.67046703514181086524.

## Not claimed

- Only the (7, 365) row. Nothing is claimed for other N in dimension 7 or for other dimensions.
- The code is not proven optimal and is not claimed to be converged.
- The table changes often. The comparison above is with the fetch of 2026-11-03; the row may change again.
- The panel files in `panel/` were written on 2026-10-18 for the earlier 24-row package and are left as written; see `panel/NOTE_2026-11-03.md`.
- The Zenodo data set behind arXiv:2610.19988 (https://doi.org/10.5281/zenodo.23270586) was not fetched; an unposted better code could exist there.
- Nothing was uploaded to the table (its /upload-code route); that needs the contributor's explicit permission and is a separate step.
- Not peer reviewed.

## Filing history

First filed on 2026-10-18 as a batch of 24 dimension-7 rows labelled "needs more optimization" (partial win p2), in folder `2026-10-18-calgulbenkian-f2033d82`. By 2026-11-03 the table had superseded 23 of them and the N = 365 row had lost its label, so at the maintainer's request (this pull request, 2026-11-03) the package was cut down to N = 365 and renamed after that object's sha256. The contributor's earlier closed filings on this target (V3R1T4S pull requests 70 to 77, 427, 430 and 434) are different rows.

## Credits

- **Henry Cohn**, *Table of spherical codes* (https://spherical-codes.org/): the table and its /plain file this claim is compared against.
- **Antoine Jay**, with the program of A. Jay, M. Poberznik, M. Brut, A. Hemeryck, L.-H. Hoang, M. Gunde, N. Salles, G. Cruchon and M. Roux, *Equidistribution of points on the hypersphere including symmetries*, preprint, 2026, doi:10.2139/ssrn.6427919: the live (7, 365) row.
- **Ilmari Vahteristo**, *New spherical codes by tuning an annealing solver*, arXiv:2610.19988 (https://arxiv.org/abs/2610.19988): closely related published work cited by the table.
- **mpmath** (https://mpmath.org/): used to polish the object to 30 significant digits; the shipped checker needs only the Python standard library.
- Search tool: the solver `sc_opt.c` in `how-we-built-it/` was written by the contributor's AI search agent for the contributor `calgulbenkian`; it is a Riemannian L-BFGS with a log-sum-exp objective and basin hopping, a standard technique with no third-party code in it.
- Contributor credit: `calgulbenkian`.
